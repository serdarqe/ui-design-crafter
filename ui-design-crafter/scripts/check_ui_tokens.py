#!/usr/bin/env python3
"""Heuristic UI token/style audit for obvious visual and accessibility risks.

This is a fast, dependency-free linter for common "AI-generated UI" and
accessibility tells. It does not replace visual QA, but it does compute real
WCAG contrast ratios for statically determinable color pairs. See
references/anti-patterns.md and references/visual-qa-checklist.md for the design
rules behind each rule.

Quick contrast check (no scan):
    python check_ui_tokens.py --contrast "#1f2937" "#ffffff"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

try:  # keep non-ASCII output (e.g. snippets with ❧, ş) from crashing on Windows cp125x consoles
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


DEFAULT_EXTENSIONS = {
    ".css", ".scss", ".sass", ".less",
    ".tsx", ".jsx", ".ts", ".js", ".html", ".vue", ".svelte",
}
CSS_LIKE = {".css", ".scss", ".sass", ".less"}
MARKUP_LIKE = {".tsx", ".jsx", ".ts", ".js", ".html", ".vue", ".svelte"}
SKIP_DIRS = {".git", "node_modules", "dist", "build", ".next", ".nuxt", "coverage", "out"}

SUMMARY_PATH = "(summary)"


@dataclass
class Issue:
    severity: str
    rule: str
    path: str
    line: int
    message: str
    snippet: str


# Line-level regex rules (severity, rule, pattern, message).
PATTERNS = [
    (
        "warn",
        "viewport-font-size",
        re.compile(r"font-size\s*:\s*[^;]*(?:vw|vh|vmin|vmax)|text-\[[^\]]*(?:vw|vh|vmin|vmax)[^\]]*\]", re.I),
        "Viewport-scaled font size can break text fit. Prefer responsive layout constraints.",
    ),
    (
        "warn",
        "negative-letter-spacing",
        re.compile(r"letter-spacing\s*:\s*-\s*[\d.]|tracking-\[-", re.I),
        "Negative letter spacing reduces readability and violates this skill's UI rule.",
    ),
    (
        "info",
        "fixed-100vh",
        re.compile(r"height\s*:\s*100vh|\bh-screen\b", re.I),
        "100vh/h-screen can crop mobile browser UI. Verify on mobile or use dynamic viewport units (dvh).",
    ),
    (
        "info",
        "layout-animation",
        re.compile(r"\b(?:transition|transition-property)\s*:[^;{}]*\b(?:width|height|top|left|right|bottom|margin|padding)\b", re.I),
        "Animating layout properties causes reflow. For the same look at 60fps, animate transform/opacity instead (performance suggestion, not a quality cut).",
    ),
]

HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
VAR_DEF_RE = re.compile(r"^\s*(?:--[\w-]+|\$[\w-]+|@[\w-]+)\s*:")
CSS_VAR_DEF_RE = re.compile(r"(--[\w-]+)\s*:\s*([^;{}]+)")
CSS_FONT_SIZE_RE = re.compile(r"font-size\s*:\s*(\d+(?:\.\d+)?)px", re.I)
TAILWIND_ARBITRARY_TEXT_RE = re.compile(r"text-\[(\d+(?:\.\d+)?)px\]", re.I)
TAILWIND_COLOR_RE = re.compile(
    r"\b(?:bg|text|border|from|to|via|ring|outline|decoration)-"
    r"(slate|gray|zinc|neutral|stone|purple|violet|indigo|blue|sky|cyan|teal|emerald|green|lime|yellow|amber|orange|red|rose|pink)-\d{2,3}\b"
)
COOL_DEFAULT_FAMILIES = {"slate", "purple", "violet", "indigo", "blue", "sky", "cyan"}
COOL_ACCENT_FAMILIES = {"purple", "violet", "indigo", "blue", "sky", "cyan"}
CSS_BLOCK_RE = re.compile(r"([^{}]+)\{([^{}]+)\}", re.S)
CLASS_NAME_RE = re.compile(r"\.([A-Za-z_][\w-]*)")
BORDER_DECL_RE = re.compile(
    r"\bborder(?:-(?:top|right|bottom|left|color|style|width))?\s*:\s*([^;}{]+)",
    re.I,
)
BOX_SHADOW_RE = re.compile(r"box-shadow\s*:\s*([^;}{]+)", re.I)
CONTAINER_FRAME_TERMS = (
    "bar", "toolbar", "panel", "window", "modal", "menu", "hud", "overlay", "strip", "tray", "shell",
)
CHILD_FRAME_TERMS = (
    "btn", "button", "card", "slot", "tab", "chip", "control",
)
GENERIC_CLUSTER_TERMS = {
    "bar", "toolbar", "panel", "window", "modal", "menu", "hud", "overlay", "strip", "tray", "shell",
    "btn", "button", "card", "slot", "tab", "chip", "control", "item", "preview", "primary", "secondary",
}
STATE_SELECTOR_RE = re.compile(
    r":focus|:focus-visible|:hover|:active|\.is-selected|\.selected|\.is-active|\.active|"
    r"\.error|\.danger|\.warning|\.equipped|\.locked|\.disabled",
    re.I,
)

GLOW_SHADOW_RE = re.compile(r"(?:box-shadow|text-shadow|drop-shadow)\s*[:(][^;{}]*?\b0\s+0\s+\d", re.I)
GRADIENT_RE = re.compile(r"(?:linear|radial|conic)-gradient\s*\(", re.I)
EXPENSIVE_FX_RE = re.compile(r"backdrop-filter\s*:|will-change\s*:|filter\s*:[^;{}]*blur\(", re.I)

# RTL / logical-property risk (physical left/right layout that does not mirror).
PHYSICAL_DIR_RE = re.compile(
    r"\b(?:margin|padding|border)-(?:left|right)\s*:|(?<![-\w])(?:left|right)\s*:"
    r"|\btext-align\s*:\s*(?:left|right)\b|\bfloat\s*:\s*(?:left|right)\b",
    re.I,
)
# Reduced-motion accessibility.
MOTION_DECL_RE = re.compile(r"@keyframes|\b(?:transition|animation)\s*:", re.I)
STRONG_MOTION_RE = re.compile(r"@keyframes|\banimation\s*:", re.I)
STYLEABLE_FOR_MOTION = CSS_LIKE | {".html", ".vue", ".svelte"}

OUTLINE_NONE_RE = re.compile(
    r"outline\s*:\s*none|outline\s*:\s*0(?:px)?\b|focus:outline-none|focus-visible:outline-none",
    re.I,
)
FOCUS_REPLACEMENT_LINE_RE = re.compile(
    r"focus-visible:(?:ring|outline|shadow|border)|focus:(?:ring|shadow)", re.I
)
FOCUS_VISIBLE_STYLE_RE = re.compile(
    r":focus-visible\b[^{]*\{[^}]*\b(?:outline|box-shadow|border)\b", re.I | re.S
)

CLASS_ATTR_RE = re.compile(
    r"""(?:class|className)\s*=\s*(?:"([^"]*)"|'([^']*)'|`([^`]*)`|\{\s*`([^`]*)`\s*\})""",
    re.I,
)
STATE_VARIANTS = {
    "hover", "focus", "focus-visible", "focus-within", "active", "disabled", "visited", "target",
}
EXCLUDED_BORDER = {
    "border-0", "border-none", "border-transparent", "border-collapse", "border-separate",
    "border-solid", "border-dashed", "border-dotted", "border-double", "border-hidden",
}

# Contrast scanning.
FG_COLOR_RE = re.compile(r"(?<![-\w])color\s*:\s*([^;}{]+)", re.I)
BG_COLOR_RE = re.compile(r"background-color\s*:\s*([^;}{]+)", re.I)
BG_SHORT_RE = re.compile(r"(?<![-\w])background\s*:\s*([^;}{]+)", re.I)
NAMED_COLORS = {
    "white": "#ffffff", "black": "#000000", "red": "#ff0000", "lime": "#00ff00",
    "blue": "#0000ff", "green": "#008000", "gray": "#808080", "grey": "#808080",
    "silver": "#c0c0c0", "maroon": "#800000", "navy": "#000080", "yellow": "#ffff00",
    "cyan": "#00ffff", "aqua": "#00ffff", "magenta": "#ff00ff", "fuchsia": "#ff00ff",
    "orange": "#ffa500", "purple": "#800080", "teal": "#008080", "olive": "#808000",
}
COLOR_TOKEN_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)|var\(\s*--[\w-]+(?:\s*,[^)]*)?\)", re.I)
FORM_CONTROL_SELECTOR_RE = re.compile(
    r"(?:^|[\s,>+~])(?:input|textarea|select)\b|\[type\b|"
    r"\.(?:input|field|form-control|text-?field|select|textarea|combobox|search-input)\b",
    re.I,
)
INTERACTIVE_SELECTOR_RE = re.compile(
    r"(?:^|[\s,>+~])(?:button|input|select|textarea)\b|\[role=['\"]?button|"
    r"\.(?:btn|button|icon-?btn|icon-?button|fab|chip|tab|nav|close|toggle|control)\b",
    re.I,
)
WIDTH_PX_RE = re.compile(r"(?<![-\w])width\s*:\s*(\d+(?:\.\d+)?)px", re.I)
HEIGHT_PX_RE = re.compile(r"(?<![-\w])height\s*:\s*(\d+(?:\.\d+)?)px", re.I)
MIN_DIM_RE = re.compile(r"min-(?:width|height)\s*:", re.I)

# Accessibility structure (markup): alt text, accessible names, lang, tabindex.
IMG_NO_ALT_RE = re.compile(r"<img\b(?![^>]*\balt\s*=)[^>]*>", re.I)
HTML_NO_LANG_RE = re.compile(r"<html\b(?![^>]*\blang\s*=)[^>]*>", re.I)
POSITIVE_TABINDEX_RE = re.compile(r"""tabindex\s*=\s*["']?\s*[1-9]""", re.I)
CTRL_BLOCK_RE = re.compile(r"<(button|a)\b([^>]*)>(.*?)</\1>", re.S)
NAME_ATTR_RE = re.compile(r"\b(?:aria-label|aria-labelledby|title)\s*=", re.I)
ARIA_HIDDEN_TRUE_RE = re.compile(r"""aria-hidden\s*=\s*["']?true""", re.I)
ICON_CHILD_RE = re.compile(r"""<svg\b|class\s*=\s*["'][^"']*\bicon\b""", re.I)
TAG_STRIP_RE = re.compile(r"<[^>]+>")


def _parse_color(value: str, var_map: dict[str, str], depth: int = 0):
    """Return (r, g, b, a) in 0-255 / 0-1, or None if not a single opaque-knowable color."""
    if value is None or depth > 6:
        return None
    value = value.strip().lower().rstrip(";")
    if not value or "gradient" in value or "url(" in value:
        return None
    if value in ("transparent", "inherit", "currentcolor", "none", "initial", "unset"):
        return None

    var_match = re.match(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^)]+))?\)", value)
    if var_match:
        name, fallback = var_match.group(1), var_match.group(2)
        if name in var_map:
            resolved = _parse_color(var_map[name], var_map, depth + 1)
            if resolved is not None:
                return resolved
        if fallback:
            return _parse_color(fallback, var_map, depth + 1)
        return None

    if value in NAMED_COLORS:
        value = NAMED_COLORS[value]

    hex_match = re.fullmatch(r"#([0-9a-f]{3,8})", value)
    if hex_match:
        h = hex_match.group(1)
        if len(h) == 3:
            r, g, b = (int(c * 2, 16) for c in h)
            return (r, g, b, 1.0)
        if len(h) == 4:
            r, g, b, a = (int(c * 2, 16) for c in h)
            return (r, g, b, a / 255)
        if len(h) == 6:
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0)
        if len(h) == 8:
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(h[6:8], 16) / 255)
        return None

    rgb_match = re.match(r"rgba?\(([^)]+)\)", value)
    if rgb_match:
        parts = re.split(r"[,\s/]+", rgb_match.group(1).strip())
        parts = [p for p in parts if p]
        if len(parts) >= 3:
            try:
                channels = []
                for p in parts[:3]:
                    if p.endswith("%"):
                        channels.append(round(float(p[:-1]) * 255 / 100))
                    else:
                        channels.append(int(float(p)))
                alpha = 1.0
                if len(parts) >= 4:
                    a = parts[3]
                    alpha = float(a[:-1]) / 100 if a.endswith("%") else float(a)
                return (channels[0], channels[1], channels[2], alpha)
            except ValueError:
                return None
    return None


def _relative_luminance(rgb) -> float:
    def channel(c):
        c /= 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb[:3]
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def _rgb_hue(rgb) -> float | None:
    r, g, b = [c / 255.0 for c in rgb[:3]]
    mx, mn = max(r, g, b), min(r, g, b)
    delta = mx - mn
    if delta < 0.08:
        return None
    if mx == r:
        hue = (60 * ((g - b) / delta) + 360) % 360
    elif mx == g:
        hue = 60 * ((b - r) / delta) + 120
    else:
        hue = 60 * ((r - g) / delta) + 240
    return hue


def _is_cool_ai_hue(hue: float | None) -> bool:
    return hue is not None and 190 <= hue <= 295


def contrast_ratio(c1, c2) -> float:
    l1 = _relative_luminance(c1)
    l2 = _relative_luminance(c2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def _selector_line(text: str, match) -> int:
    """1-based line of a CSS rule's selector, skipping leading whitespace captured in group 1."""
    sel = match.group(1)
    lead = len(sel) - len(sel.lstrip())
    return text[: match.start(1) + lead].count("\n") + 1


def parse_extensions(raw: str) -> set[str]:
    result = set()
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        result.add(part if part.startswith(".") else f".{part}")
    return result


def iter_files(paths: list[Path], extensions: set[str], max_files: int) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_file() and path.suffix.lower() in extensions:
            files.append(path)
        elif path.is_dir():
            for child in path.rglob("*"):
                if len(files) >= max_files:
                    return files
                if child.is_dir() and child.name in SKIP_DIRS:
                    continue
                if any(part in SKIP_DIRS for part in child.parts):
                    continue
                if child.is_file() and child.suffix.lower() in extensions:
                    files.append(child)
        if len(files) >= max_files:
            return files
    return files


def build_var_map(files: list[Path]) -> dict[str, str]:
    """Collect CSS custom-property color definitions across all CSS-like files."""
    var_map: dict[str, str] = {}
    for path in files:
        if path.suffix.lower() not in CSS_LIKE:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for match in CSS_VAR_DEF_RE.finditer(text):
            name, value = match.group(1), match.group(2).strip()
            var_map.setdefault(name, value)
    return var_map


def add_issue(issues, severity, rule, path, line_no, message, line) -> None:
    issues.append(Issue(severity, rule, str(path), line_no, message, line.strip()[:180]))


def _split_variants(token: str):
    token = token.lstrip("!")
    parts = token.split(":")
    return parts[-1], parts[:-1]


def _is_stateful(variants) -> bool:
    for variant in variants:
        if variant in STATE_VARIANTS or variant.startswith(("group-", "peer-", "aria-", "data-")):
            return True
    return False


def _is_border(base: str) -> bool:
    if base == "border":
        return True
    if base.startswith("border-"):
        return base not in EXCLUDED_BORDER and not base.startswith("border-spacing")
    return False


def _is_ring(base: str) -> bool:
    if base == "ring":
        return True
    if base.startswith("ring-"):
        return base not in {"ring-0", "ring-transparent"} and not base.startswith("ring-offset")
    return False


def _is_shadow(base: str) -> bool:
    if base in {"shadow-none", "drop-shadow-none"}:
        return False
    return base == "shadow" or base.startswith("shadow-") or base.startswith("drop-shadow")


def _has_visible_border(body: str) -> bool:
    """A border that is 0, none, or transparent is not a visible resting frame."""
    for m in BORDER_DECL_RE.finditer(body):
        val = m.group(1).strip().lower()
        if val.startswith(("0", "none")) or "transparent" in val:
            continue
        return True
    return False


def _has_permanent_frame(body: str) -> bool:
    if _has_visible_border(body):
        return True
    m = BOX_SHADOW_RE.search(body)
    return bool(m and "none" not in m.group(1).lower())


def _selector_terms(selector: str) -> set[str]:
    terms: set[str] = set()
    for class_name in CLASS_NAME_RE.findall(selector.lower()):
        terms.update(p for p in re.split(r"[^a-z0-9]+", class_name) if p)
    return terms


def scan_frame_stacking(path: Path, text: str, issues) -> None:
    if path.suffix.lower() not in CSS_LIKE:
        return
    container_frames, child_frames = [], []
    for match in CSS_BLOCK_RE.finditer(text):
        selector = " ".join(match.group(1).split())
        selector_lower = selector.lower()
        body = match.group(2).lower()
        if STATE_SELECTOR_RE.search(selector_lower) or not _has_permanent_frame(body):
            continue
        line_no = _selector_line(text, match)
        has_container = any(term in selector_lower for term in CONTAINER_FRAME_TERMS)
        has_child = any(term in selector_lower for term in CHILD_FRAME_TERMS)
        has_surface = "background" in body or "backdrop-filter" in body or "box-shadow" in body
        if has_container and has_surface:
            container_frames.append((line_no, selector, _selector_terms(selector)))
        if has_child and not has_container and _has_visible_border(body):
            child_frames.append((line_no, selector, _selector_terms(selector)))

    best_match = None
    for container_line, container_selector, container_terms in container_frames:
        matching_children = []
        meaningful_container_terms = container_terms - GENERIC_CLUSTER_TERMS
        if not meaningful_container_terms:
            continue
        for child_line, child_selector, child_terms in child_frames:
            if meaningful_container_terms & (child_terms - GENERIC_CLUSTER_TERMS):
                matching_children.append((child_line, child_selector))
        if matching_children:
            best_match = (container_line, container_selector, matching_children)
            break

    if best_match:
        container_line, container_selector, matching_children = best_match
        examples = ", ".join(sel for _, sel in matching_children[:3])
        add_issue(
            issues, "warn", "frame-stacking", path, container_line,
            f"Container frame ({container_selector}) plus {len(matching_children)} same-cluster bordered child rules "
            f"({examples}). Looks like stacked AI frames; use one structural frame per cluster, then "
            "fill/spacing/dividers/state color for inner controls.",
            container_selector,
        )


def scan_class_framing(path: Path, text: str, issues) -> int:
    if path.suffix.lower() not in MARKUP_LIKE:
        return 0
    double_outline_count = 0
    for match in CLASS_ATTR_RE.finditer(text):
        class_str = next((g for g in match.groups() if g), "")
        if not class_str:
            continue
        has_border = has_ring = has_shadow = False
        for raw in class_str.split():
            base, variants = _split_variants(raw)
            if _is_stateful(variants):
                continue
            if _is_border(base):
                has_border = True
            elif _is_ring(base):
                has_ring = True
            elif _is_shadow(base):
                has_shadow = True
        if has_border and has_ring:
            double_outline_count += 1
            line_no = text[: match.start()].count("\n") + 1
            kind = "border + ring + shadow (over-framed)" if has_shadow else "border + ring (double outline)"
            add_issue(
                issues, "warn", "double-outline", path, line_no,
                f"Resting element stacks {kind}. Use one boundary at rest; reserve the second outline "
                "for focus/selected so state stands out.",
                class_str[:160],
            )
    return double_outline_count


def scan_contrast(path: Path, text: str, var_map: dict[str, str], issues) -> None:
    """Flag color/background pairs in the same CSS rule that fail WCAG AA contrast."""
    if path.suffix.lower() not in CSS_LIKE:
        return
    for match in CSS_BLOCK_RE.finditer(text):
        body = match.group(2)
        fg_match = FG_COLOR_RE.search(body)
        if not fg_match:
            continue
        bg_match = BG_COLOR_RE.search(body) or BG_SHORT_RE.search(body)
        if not bg_match:
            continue
        fg = _parse_color(fg_match.group(1), var_map)
        bg = _parse_color(bg_match.group(1), var_map)
        if not fg or not bg or fg[3] < 1 or bg[3] < 1:
            continue
        ratio = contrast_ratio(fg, bg)
        if ratio < 4.5:
            selector = " ".join(match.group(1).split())[:80]
            line_no = _selector_line(text, match)
            verdict = "fails AA for all text" if ratio < 3 else "passes only for large/bold text (>=18.66px or 14px bold)"
            add_issue(
                issues, "warn", "low-contrast-text", path, line_no,
                f"Text contrast {ratio:.2f}:1 ({selector}) {verdict}. WCAG AA needs 4.5:1 for normal text, 3:1 for large.",
                f"color/background in: {selector}",
            )


def _extract_color_token(value: str):
    m = COLOR_TOKEN_RE.search(value)
    if m:
        return m.group(0)
    for tok in re.split(r"\s+", value.strip()):
        if tok.lower() in NAMED_COLORS:
            return tok
    return None


def scan_control_border_contrast(path: Path, text: str, var_map: dict[str, str], issues) -> None:
    """WCAG 1.4.11: a form control's resting border must reach 3:1 against its own fill."""
    if path.suffix.lower() not in CSS_LIKE:
        return
    for match in CSS_BLOCK_RE.finditer(text):
        selector = " ".join(match.group(1).split())
        if STATE_SELECTOR_RE.search(selector.lower()):
            continue
        if not FORM_CONTROL_SELECTOR_RE.search(selector.lower()):
            continue
        body = match.group(2)
        bg_match = BG_COLOR_RE.search(body) or BG_SHORT_RE.search(body)
        if not bg_match:
            continue
        border_token = None
        for bm in BORDER_DECL_RE.finditer(body):
            raw = bm.group(1).strip().lower()
            if raw.startswith(("0", "none")) or "transparent" in raw:
                continue
            token = _extract_color_token(bm.group(1))
            if token:
                border_token = token
                break
        if not border_token:
            continue
        bc = _parse_color(border_token, var_map)
        bg = _parse_color(bg_match.group(1), var_map)
        if not bc or not bg or bc[3] < 1 or bg[3] < 1:
            continue
        ratio = contrast_ratio(bc, bg)
        if ratio < 3.0:
            line_no = _selector_line(text, match)
            add_issue(
                issues, "warn", "low-contrast-control-border", path, line_no,
                f"Form control border contrast {ratio:.2f}:1 against its own fill ({selector[:60]}). "
                "WCAG 1.4.11 needs 3:1 for control boundaries.",
                f"border/background in: {selector[:80]}",
            )


def scan_tap_targets(path: Path, text: str, issues) -> None:
    """Flag interactive controls with a fixed width and height both below 44px and no min dimension."""
    if path.suffix.lower() not in CSS_LIKE:
        return
    for match in CSS_BLOCK_RE.finditer(text):
        selector = " ".join(match.group(1).split())
        sl = selector.lower()
        if STATE_SELECTOR_RE.search(sl) or not INTERACTIVE_SELECTOR_RE.search(sl):
            continue
        body = match.group(2)
        if MIN_DIM_RE.search(body):
            continue
        wm = WIDTH_PX_RE.search(body)
        hm = HEIGHT_PX_RE.search(body)
        if not wm or not hm:
            continue
        if float(wm.group(1)) < 44 and float(hm.group(1)) < 44:
            line_no = _selector_line(text, match)
            add_issue(
                issues, "info", "small-tap-target", path, line_no,
                f"Interactive control {wm.group(1)}x{hm.group(1)}px is below the 44px touch target ({selector[:50]}). "
                "Add min-height/min-width or padding for touch and game UI.",
                selector[:80],
            )


def scan_a11y_structure(path: Path, text: str, issues) -> None:
    """Markup-level accessibility checks: alt text, accessible names, lang, tabindex."""
    if path.suffix.lower() not in MARKUP_LIKE:
        return
    for m in IMG_NO_ALT_RE.finditer(text):
        line_no = text[: m.start()].count("\n") + 1
        add_issue(issues, "warn", "img-missing-alt", path, line_no,
                  'Image has no alt attribute. Add alt text, or alt="" if purely decorative.', m.group(0)[:120])
    if path.suffix.lower() == ".html":
        for m in HTML_NO_LANG_RE.finditer(text):
            line_no = text[: m.start()].count("\n") + 1
            add_issue(issues, "info", "html-missing-lang", path, line_no,
                      '<html> has no lang attribute; set it (e.g. lang="en") for screen readers and hyphenation.', m.group(0)[:80])
    for m in POSITIVE_TABINDEX_RE.finditer(text):
        line_no = text[: m.start()].count("\n") + 1
        add_issue(issues, "info", "positive-tabindex", path, line_no,
                  'Positive tabindex overrides natural order; prefer tabindex="0"/"-1" and DOM order.', m.group(0)[:80])
    for m in CTRL_BLOCK_RE.finditer(text):
        attrs, inner = m.group(2), m.group(3)
        if NAME_ATTR_RE.search(attrs) or ARIA_HIDDEN_TRUE_RE.search(attrs):
            continue
        if not ICON_CHILD_RE.search(inner) or TAG_STRIP_RE.sub("", inner).strip():
            continue
        line_no = text[: m.start()].count("\n") + 1
        add_issue(issues, "warn", "control-missing-name", path, line_no,
                  f"Icon-only <{m.group(1)}> has no accessible name. Add aria-label or visible text.", m.group(0)[:120])


def scan_file(path: Path, counters: dict) -> list[Issue]:
    issues: list[Issue] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        add_issue(issues, "warn", "read-error", path, 0, str(exc), "")
        return issues

    file_has_focus_visible = bool(FOCUS_VISIBLE_STYLE_RE.search(text))

    for line_no, line in enumerate(text.splitlines(), start=1):
        for severity, rule, pattern, message in PATTERNS:
            if pattern.search(line):
                add_issue(issues, severity, rule, path, line_no, message, line)

        if OUTLINE_NONE_RE.search(line) and not FOCUS_REPLACEMENT_LINE_RE.search(line):
            severity = "info" if file_has_focus_visible else "warn"
            detail = (
                " A focus-visible style exists in this file; confirm it covers this element."
                if file_has_focus_visible
                else " Provide an explicit accessible focus-visible replacement."
            )
            add_issue(issues, severity, "outline-none", path, line_no, "Removed focus outline." + detail, line)

        for value in HEX_RE.findall(line):
            counters["hex_all"][value.lower()] += 1
            if VAR_DEF_RE.match(line):
                counters["hex_token"][value.lower()] += 1
            else:
                counters["hex_inline"][value.lower()] += 1

        for m in CSS_FONT_SIZE_RE.finditer(line):
            if float(m.group(1)) < 12:
                add_issue(issues, "warn", "tiny-font-size", path, line_no,
                          "Text below 12px is risky for UI readability.", line)
        for m in TAILWIND_ARBITRARY_TEXT_RE.finditer(line):
            if float(m.group(1)) < 12:
                add_issue(issues, "warn", "tiny-font-size", path, line_no,
                          "Arbitrary Tailwind text below 12px is risky for UI readability.", line)
        for family in TAILWIND_COLOR_RE.findall(line):
            counters["color_families"][family] += 1
        counters["physical_dir"] += len(PHYSICAL_DIR_RE.findall(line))

    counters["glow"] += len(GLOW_SHADOW_RE.findall(text))
    counters["gradient"] += len(GRADIENT_RE.findall(text))
    counters["expensive_fx"] += len(EXPENSIVE_FX_RE.findall(text))
    if path.suffix.lower() in STYLEABLE_FOR_MOTION and MOTION_DECL_RE.search(text) and "prefers-reduced-motion" not in text:
        strong = bool(STRONG_MOTION_RE.search(text))
        m = MOTION_DECL_RE.search(text)
        line_no = text[: m.start()].count("\n") + 1 if m else 1
        add_issue(
            issues, "warn" if strong else "info", "missing-reduced-motion", path, line_no,
            "Defines " + ("animation/keyframes" if strong else "transitions")
            + " but no prefers-reduced-motion guard. Add a reduced-motion path for vestibular accessibility.",
            "",
        )
    scan_frame_stacking(path, text, issues)
    scan_contrast(path, text, counters["var_map"], issues)
    scan_control_border_contrast(path, text, counters["var_map"], issues)
    scan_tap_targets(path, text, issues)
    counters["double_outline"] += scan_class_framing(path, text, issues)
    scan_a11y_structure(path, text, issues)
    return issues


def build_summary_signals(counters: dict) -> list[Issue]:
    signals: list[Issue] = []
    cool_family_warned = False
    inline_distinct = len(counters["hex_inline"])
    inline_total = sum(counters["hex_inline"].values())
    if inline_distinct >= 12:
        signals.append(Issue("warn", "raw-hex-density", SUMMARY_PATH, 0,
            f"{inline_distinct} distinct raw hex colors used inline ({inline_total} uses). "
            "Move colors into design tokens / CSS variables for a coherent palette.", ""))

    families = counters["color_families"]
    total_families = sum(families.values())
    if total_families >= 12:
        family, count = families.most_common(1)[0]
        ratio = count / total_families
        if total_families >= 20 and ratio >= 0.6:
            signals.append(Issue("warn", "palette-dominance", SUMMARY_PATH, 0,
                f"One Tailwind color family dominates: {family} = {count}/{total_families} ({ratio:.0%}). "
                "Check for a one-note palette; add a true neutral and semantic state colors.", ""))
        cool_count = sum(families.get(f, 0) for f in COOL_DEFAULT_FAMILIES)
        cool_accent_count = sum(families.get(f, 0) for f in COOL_ACCENT_FAMILIES)
        cool_ratio = cool_count / total_families
        if cool_ratio >= 0.65 and cool_accent_count >= 4:
            cool_family_warned = True
            signals.append(Issue("warn", "cool-default-palette", SUMMARY_PATH, 0,
                f"Cool dark-tech families dominate Tailwind color classes ({cool_count}/{total_families}, {cool_ratio:.0%}). "
                "Do not default to purple/blue/cyan/dark UI unless the user's brand, domain, genre, or request justifies it.", ""))

    parsed_colors = []
    for value in counters["hex_all"]:
        color = _parse_color(value, {})
        if color and color[3] >= 1:
            parsed_colors.append(color)
    if len(parsed_colors) >= 8:
        dark_count = sum(1 for color in parsed_colors if _relative_luminance(color) < 0.18)
        chromatic = [color for color in parsed_colors if _rgb_hue(color) is not None]
        cool_count = sum(1 for color in chromatic if _is_cool_ai_hue(_rgb_hue(color)))
        if chromatic:
            dark_ratio = dark_count / len(parsed_colors)
            cool_ratio = cool_count / len(chromatic)
            if not cool_family_warned and dark_count >= 4 and cool_count >= 4 and dark_ratio >= 0.35 and cool_ratio >= 0.45:
                signals.append(Issue("warn", "cool-dark-default-palette", SUMMARY_PATH, 0,
                    f"Palette skews both dark ({dark_count}/{len(parsed_colors)}) and cool blue/purple/cyan "
                    f"({cool_count}/{len(chromatic)} chromatic colors). Confirm this matches the user's design direction; "
                    "otherwise rebuild the palette from brand, domain, audience, content, and mood.", ""))

    if counters["double_outline"] >= 3:
        signals.append(Issue("warn", "frame-stacking", SUMMARY_PATH, 0,
            f"{counters['double_outline']} elements stack border + ring at rest. "
            "This is the Tailwind form of frame stacking; reduce to one resting boundary.", ""))

    if counters["glow"] >= 10:
        signals.append(Issue("info", "glow-density", SUMMARY_PATH, 0,
            f"{counters['glow']} glow-style shadows (0 0 blur) detected. Reserve glow for state changes "
            "(selection, ready, alert); contrast and silhouette should carry legibility.", ""))

    if counters["gradient"] >= 18:
        signals.append(Issue("info", "gradient-density", SUMMARY_PATH, 0,
            f"{counters['gradient']} gradients detected. Watch for gradient soup; prefer a clear surface "
            "logic with at most one signature gradient.", ""))

    if counters["expensive_fx"] >= 6:
        signals.append(Issue("info", "expensive-effects", SUMMARY_PATH, 0,
            f"{counters['expensive_fx']} heavy live effects (backdrop-filter / filter: blur / will-change). "
            "Verify on a low-end device; the same look is often achievable with a cheaper fallback. "
            "Performance suggestion, not a reason to cut quality.", ""))

    if counters["physical_dir"] >= 8:
        signals.append(Issue("info", "rtl-physical-properties", SUMMARY_PATH, 0,
            f"{counters['physical_dir']} physical left/right properties (margin/padding/border/left/right/text-align/float). "
            "If you support right-to-left languages, prefer logical properties "
            "(margin-inline-start, inset-inline, text-align: start). See references/internationalization.md.", ""))

    return signals


def severity_counts(issues) -> Counter:
    counts: Counter = Counter()
    for issue in issues:
        counts[issue.severity] += 1
    return counts


def print_report(files, issues, signals, counters) -> None:
    counts = severity_counts(issues + signals)
    print("UI token heuristic audit")
    print(f"Files scanned: {len(files)}")
    print(f"Issues: {len(issues) + len(signals)} "
          f"(error: {counts.get('error', 0)}, warn: {counts.get('warn', 0)}, info: {counts.get('info', 0)})")

    if counters["hex_all"]:
        print(f"Raw hex colors: {len(counters['hex_all'])} distinct "
              f"({len(counters['hex_token'])} in token definitions, {len(counters['hex_inline'])} inline).")
    families = counters["color_families"]
    if families:
        total = sum(families.values())
        family, count = families.most_common(1)[0]
        print(f"Tailwind color classes: {total}; dominant family: {family} ({count}, {count / total:.0%}).")
    if counters["glow"] or counters["gradient"]:
        print(f"Decorative effects: {counters['glow']} glow shadows, {counters['gradient']} gradients.")
    if counters["double_outline"]:
        print(f"Double-outline elements (border + ring at rest): {counters['double_outline']}.")
    contrast_fail = sum(1 for i in issues if i.rule == "low-contrast-text")
    if contrast_fail:
        print(f"Static contrast failures (color+background in one rule): {contrast_fail}.")

    if signals:
        print("\nProject-level signals:")
        for signal in signals:
            print(f"  {signal.severity.upper()} {signal.rule}: {signal.message}")

    if not issues:
        print("\nNo per-file issues found. This is not a substitute for visual QA or full contrast testing.")
        return

    print()
    for issue in issues[:200]:
        print(f"{issue.severity.upper()} {issue.rule} {issue.path}:{issue.line}")
        print(f"  {issue.message}")
        if issue.snippet:
            print(f"  {issue.snippet}")
    if len(issues) > 200:
        print(f"\nShowing 200 of {len(issues)} per-file issues.")


def run_contrast_cli(fg_raw: str, bg_raw: str) -> int:
    fg = _parse_color(fg_raw, {})
    bg = _parse_color(bg_raw, {})
    if not fg or not bg:
        print(f"Could not parse colors: fg={fg_raw!r} bg={bg_raw!r} (use hex, rgb(), rgba(), or a named color).")
        return 2
    if fg[3] < 1 or bg[3] < 1:
        print("One color has alpha < 1; contrast depends on what is composited underneath. Provide opaque colors.")
        return 2
    ratio = contrast_ratio(fg, bg)
    print(f"Contrast ratio: {ratio:.2f}:1")
    checks = [
        ("Normal text AA (4.5:1)", ratio >= 4.5),
        ("Normal text AAA (7:1)", ratio >= 7.0),
        ("Large text AA (3:1)", ratio >= 3.0),
        ("Large text AAA (4.5:1)", ratio >= 4.5),
        ("Non-text / UI components (3:1)", ratio >= 3.0),
    ]
    for label, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    return 0 if ratio >= 4.5 else 1


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Audit UI code for common token/style/contrast risks.")
    parser.add_argument("paths", nargs="*", type=Path, default=[Path.cwd()])
    parser.add_argument("--ext", default=",".join(sorted(DEFAULT_EXTENSIONS)), help="Comma-separated extensions to scan.")
    parser.add_argument("--max-files", type=int, default=500)
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on warnings, not only errors.")
    parser.add_argument("--contrast", nargs=2, metavar=("FG", "BG"),
                        help="Compute the WCAG contrast ratio between two colors and exit.")
    args = parser.parse_args(argv)

    if args.contrast:
        return run_contrast_cli(args.contrast[0], args.contrast[1])

    extensions = parse_extensions(args.ext)
    files = iter_files(args.paths, extensions, max(args.max_files, 1))
    counters = {
        "hex_all": Counter(), "hex_token": Counter(), "hex_inline": Counter(),
        "color_families": Counter(), "glow": 0, "gradient": 0, "double_outline": 0, "physical_dir": 0, "expensive_fx": 0,
        "var_map": build_var_map(files),
    }
    issues: list[Issue] = []
    for file_path in files:
        issues.extend(scan_file(file_path, counters))

    signals = build_summary_signals(counters)
    all_issues = issues + signals

    if args.json:
        print(json.dumps({
            "files_scanned": len(files),
            "severity_counts": dict(severity_counts(all_issues)),
            "issues": [asdict(i) for i in issues],
            "summary_signals": [asdict(s) for s in signals],
            "raw_hex_colors": dict(counters["hex_all"].most_common()),
            "raw_hex_inline": dict(counters["hex_inline"].most_common()),
            "raw_hex_token": dict(counters["hex_token"].most_common()),
            "tailwind_color_families": dict(counters["color_families"].most_common()),
            "glow_shadows": counters["glow"],
            "gradients": counters["gradient"],
            "double_outline_elements": counters["double_outline"],
            "physical_direction_props": counters["physical_dir"],
            "expensive_effects": counters["expensive_fx"],
        }, indent=2))
    else:
        print_report(files, issues, signals, counters)

    counts = severity_counts(all_issues)
    if counts.get("error"):
        return 1
    if args.strict and counts.get("warn"):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
