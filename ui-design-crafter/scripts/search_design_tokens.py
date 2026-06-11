#!/usr/bin/env python3
"""Search curated, accessibility-checked design data by domain.

These are original starting points to adapt, not a fixed kit and not a substitute
for designing in context. Palettes are annotated with real WCAG contrast ratios so
you can see at a glance whether the body text passes on the base and surface colors.

Usage:
    python search_design_tokens.py "fintech dark dashboard"
    python search_design_tokens.py "korku görev ana menü" --kind all
    python search_design_tokens.py "rpg fantasy" --kind palette
    python search_design_tokens.py "code editor" --kind type --limit 3
    python search_design_tokens.py "shop inventory" --kind icon
    python search_design_tokens.py "casual puzzle mobile" --kind style
    python search_design_tokens.py "Google Play phone portrait" --kind store-preset
    python search_design_tokens.py "horror game screenshot 3 shop" --kind store-caption
    python search_design_tokens.py "fintech dark dashboard" --design-system
    python search_design_tokens.py "ecommerce" --design-system --mode dark
    python search_design_tokens.py "cozy farming sim" --design-system --out design-system/MASTER.md
"""

from __future__ import annotations

import argparse
import csv
import math
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

try:  # keep Turkish/Unicode output from crashing on Windows cp125x consoles
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def default_data_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "data"


TURKISH_TRANSLATION = str.maketrans({
    "ç": "c", "Ç": "c",
    "ğ": "g", "Ğ": "g",
    "ı": "i", "I": "i",
    "İ": "i", "i": "i",
    "ö": "o", "Ö": "o",
    "ş": "s", "Ş": "s",
    "ü": "u", "Ü": "u",
})


def normalize_text(value: str) -> str:
    value = (value or "").translate(TURKISH_TRANSLATION).lower()
    value = unicodedata.normalize("NFKD", value)
    return "".join(ch for ch in value if not unicodedata.combining(ch))


def tokens(value: str) -> list[str]:
    return [p for p in re.split(r"[^a-z0-9]+", normalize_text(value)) if p]


def load_aliases(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return load_rows(path)


def expand_query_tokens(raw_query: str, data_dir: Path) -> list[str]:
    base_tokens = tokens(raw_query)
    expanded = list(base_tokens)
    seen = set(expanded)
    base_set = set(base_tokens)
    base_phrase = " ".join(base_tokens)

    for row in load_aliases(data_dir / "query-aliases.csv"):
        alias_tokens = tokens(row.get("alias", ""))
        if not alias_tokens:
            continue
        alias_phrase = " ".join(alias_tokens)
        matched = alias_tokens[0] in base_set if len(alias_tokens) == 1 else (
            alias_phrase in base_phrase or all(token in base_set for token in alias_tokens)
        )
        if not matched:
            continue
        for token in tokens(row.get("expansion", "")):
            if token not in seen:
                expanded.append(token)
                seen.add(token)
    return expanded


def _hex_to_rgb(value: str):
    value = value.strip().lstrip("#")
    if len(value) == 3:
        value = "".join(c * 2 for c in value)
    if len(value) != 6 or any(c not in "0123456789abcdefABCDEF" for c in value):
        return None
    return (int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16))


def _luminance(rgb) -> float:
    def channel(c):
        c /= 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast(a: str, b: str):
    ca, cb = _hex_to_rgb(a), _hex_to_rgb(b)
    if not ca or not cb:
        return None
    la, lb = _luminance(ca), _luminance(cb)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def on_color(fill_hex: str):
    """Best readable text color on a fill: white or near-black, whichever has more contrast."""
    light = contrast(ON_LIGHT, fill_hex) or 0
    dark = contrast(ON_DARK, fill_hex) or 0
    return (ON_LIGHT, light) if light >= dark else (ON_DARK, dark)


def token_matches(token: str, candidates: set[str]) -> bool:
    if token in candidates:
        return True
    if f"{token}s" in candidates:
        return True
    if token.endswith("s") and token[:-1] in candidates:
        return True
    return False


MIN_CONFIDENT_SCORE = 4.0
MIN_WEAK_SCORE = 1.5
ON_LIGHT, ON_DARK = "#ffffff", "#05070a"


def bm25_context(rows: list[dict], fields: tuple[str, ...]) -> tuple[dict[str, float], float]:
    docs: list[set[str]] = []
    lengths: list[int] = []
    for row in rows:
        doc_tokens = tokens(" ".join((row.get(f, "") or "") for f in fields))
        doc_tokens.extend(tokens(row.get("domain", "") or "") * 2)
        docs.append(set(doc_tokens))
        lengths.append(max(1, len(doc_tokens)))
    total = max(1, len(rows))
    avg_len = sum(lengths) / total if lengths else 1.0
    idf: dict[str, float] = {}
    terms = set().union(*docs) if docs else set()
    for term in terms:
        containing = sum(1 for doc in docs if term in doc)
        idf[term] = math.log(1 + (total - containing + 0.5) / (containing + 0.5))
    return idf, avg_len


def score_row_with_context(
    row: dict,
    query_tokens: list[str],
    fields: tuple[str, ...],
    idf: dict[str, float],
    avg_len: float,
) -> float:
    if not query_tokens:
        return 0.0
    haystack = tokens(" ".join((row.get(f, "") or "") for f in fields))
    domain = tokens(row.get("domain", "") or "")
    doc_tokens = haystack + (domain * 2)
    doc_len = max(1, len(doc_tokens))
    haystack_tokens = set(haystack)
    domain_tokens = set(domain)
    k1, b = 1.2, 0.75
    score = 0.0
    for token in set(query_tokens):
        matching_terms = [candidate for candidate in set(doc_tokens) if token_matches(token, {candidate})]
        if not matching_terms:
            continue
        tf = sum(doc_tokens.count(term) for term in matching_terms)
        term_idf = max(idf.get(term, 1.0) for term in matching_terms)
        score += term_idf * ((tf * (k1 + 1)) / (tf + k1 * (1 - b + b * doc_len / max(avg_len, 1))))
        if token_matches(token, domain_tokens):
            score += 2.0
        elif token_matches(token, haystack_tokens):
            score += 0.5
    return round(score, 3)


def score_row(row: dict, query_tokens: list[str], fields: tuple[str, ...]) -> float:
    idf, avg_len = bm25_context([row], fields)
    return score_row_with_context(row, query_tokens, fields, idf, avg_len)


def load_rows(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def rank(rows: list[dict], query_tokens: list[str], fields: tuple[str, ...], limit: int) -> list[dict]:
    idf, avg_len = bm25_context(rows, fields)
    scored = []
    for row in rows:
        s = score_row_with_context(row, query_tokens, fields, idf, avg_len)
        if query_tokens and s == 0:
            continue
        enriched = dict(row)
        enriched["_score"] = s
        scored.append(enriched)
    scored.sort(key=lambda r: (r["_score"], r.get("name", "")), reverse=True)
    deduped = []
    seen_names = set()
    for row in scored:
        name = row.get("name", "")
        if name and name in seen_names:
            continue
        seen_names.add(name)
        deduped.append(row)
    return deduped[:limit] if limit > 0 else deduped


def _aa(ratio) -> str:
    if ratio is None:
        return "n/a"
    return f"{ratio:.1f}:1 {'AA-pass' if ratio >= 4.5 else ('large-only' if ratio >= 3 else 'FAIL')}"


def print_palettes(rows: list[dict]) -> None:
    if not rows:
        print("No matching palettes.")
        return
    print("== Color palettes (content contrast shown for body text) ==")
    for row in rows:
        bg, surface, content = row.get("bg", ""), row.get("surface", ""), row.get("content", "")
        on_bg = contrast(content, bg)
        on_surface = contrast(content, surface)
        print(f"\n{row.get('name')}  [{row.get('mode')}]  domain: {row.get('domain')}")
        print(f"  bg {bg} | surface {surface} | content {content} | muted {row.get('muted')} | border {row.get('border')}")
        print(f"  primary {row.get('primary')} | accent {row.get('accent')} | "
              f"success {row.get('success')} | warning {row.get('warning')} | danger {row.get('danger')}")
        print(f"  content on bg: {_aa(on_bg)}   |   content on surface: {_aa(on_surface)}")
        if row.get("notes"):
            print(f"  note: {row.get('notes')}")


def print_pairings(rows: list[dict]) -> None:
    if not rows:
        print("No matching type pairings.")
        return
    print("== Type pairings ==")
    for row in rows:
        mono = row.get("mono_font") or "-"
        print(f"\n{row.get('name')}  domain: {row.get('domain')}")
        print(f"  heading: {row.get('heading_font')} | body: {row.get('body_font')} | mono: {mono} | scale: {row.get('scale')}")
        if row.get("notes"):
            print(f"  note: {row.get('notes')}")


def print_icons(rows: list[dict]) -> None:
    if not rows:
        print("No matching icons.")
        return
    print("== Icon meanings ==")
    for row in rows:
        print(f"\n{row.get('name')}  meaning: {row.get('meaning')}")
        print(f"  domain: {row.get('domain')} | style: {row.get('style')}")
        print(f"  source: {row.get('source')} | license: {row.get('license')} | {row.get('source_url')}")
        if row.get("notes"):
            print(f"  note: {row.get('notes')}")


def print_styles(rows: list[dict]) -> None:
    if not rows:
        print("No matching style domains.")
        return
    print("== Style domains ==")
    for row in rows:
        print(f"\n{row.get('name')}  domain: {row.get('domain')}")
        print(f"  density: {row.get('density')} | chrome: {row.get('chrome_level')} | surfaces: {row.get('primary_surfaces')}")
        print(f"  good for: {row.get('good_for')}")
        print(f"  avoid: {row.get('avoid')}")
        if row.get("notes"):
            print(f"  note: {row.get('notes')}")


def print_motion(rows: list[dict]) -> None:
    if not rows:
        print("No matching motion presets.")
        return
    print("== Motion presets ==")
    for row in rows:
        print(f"\n{row.get('name')}  domain: {row.get('domain')}")
        print(f"  easing: {row.get('easing')} | base: {row.get('duration_ms')}ms | hover: {row.get('hover_ms')}ms")
        print(f"  reduced-motion: {row.get('reduced_motion')}")
        if row.get("notes"):
            print(f"  note: {row.get('notes')}")


def print_store_presets(rows: list[dict]) -> None:
    if not rows:
        print("No matching store screenshot presets.")
        return
    print("== Store screenshot presets ==")
    for row in rows:
        print(f"\n{row.get('name')}  [{row.get('platform')}]")
        print(f"  device: {row.get('device_group')} | orientation: {row.get('orientation')}")
        print(f"  size: {row.get('width')}x{row.get('height')} | status: {row.get('required_or_optional')}")
        print(f"  source: {row.get('source_url')} | last_checked: {row.get('last_checked')}")
        if row.get("notes"):
            print(f"  note: {row.get('notes')}")


def print_store_captions(rows: list[dict]) -> None:
    if not rows:
        print("No matching store caption patterns.")
        return
    print("== Store caption patterns ==")
    for row in rows:
        print(f"\n{row.get('name')}  domain: {row.get('domain')}")
        print(f"  position: {row.get('screenshot_position')} | intent: {row.get('intent')}")
        print(f"  pattern: {row.get('good_pattern')}")
        print(f"  avoid: {row.get('avoid')}")
        if row.get("localization_notes"):
            print(f"  localization: {row.get('localization_notes')}")


def filter_store_presets(rows: list[dict], query_tokens: list[str]) -> list[dict]:
    """Narrow store preset search when the platform signal is clear."""
    q = set(query_tokens)
    wants_app_store = bool(q & {"apple", "ios", "iphone", "ipad"})
    wants_google_play = bool(q & {"google", "play", "android", "chromebook", "wear", "automotive", "xr", "feature"})
    if wants_app_store and not wants_google_play:
        return [row for row in rows if row.get("platform") == "app-store"] or rows
    if wants_google_play and not wants_app_store:
        return [row for row in rows if row.get("platform") == "google-play"] or rows
    return rows


STORE_PRESET_FIELDS = ("name", "platform", "device_group", "orientation", "required_or_optional", "notes")


def store_preset_boost(row: dict, query_tokens: list[str]) -> float:
    q = set(query_tokens)
    device = set(tokens(row.get("device_group", "")))
    orientation = set(tokens(row.get("orientation", "")))
    boost = 0.0

    def prefer(term: str, candidates: set[str], hit: float = 5.0, miss: float = -2.0) -> None:
        nonlocal boost
        if term in q:
            boost += hit if term in candidates else miss

    prefer("phone", device, 6.0, -3.0)
    prefer("iphone", device, 7.0, -4.0)
    prefer("ipad", device, 7.0, -4.0)
    prefer("wear", device, 5.0, -2.0)
    prefer("automotive", device, 5.0, -2.0)
    prefer("xr", device, 5.0, -2.0)

    if "tablet" in q:
        boost += 6.0 if ({"tablet", "ipad"} & device) else -2.0
    if "portrait" in q or "vertical" in q:
        boost += 5.0 if "portrait" in orientation else -3.0
    if "landscape" in q or "horizontal" in q:
        boost += 5.0 if "landscape" in orientation else -3.0
    if "feature" in q or "graphic" in q:
        boost += 7.0 if ({"feature", "graphic"} & device) else -1.0
    elif {"phone", "tablet", "iphone", "ipad"} & q and ({"feature", "graphic"} & device):
        boost -= 6.0

    return boost


def rank_store_presets(rows: list[dict], query_tokens: list[str], limit: int) -> list[dict]:
    idf, avg_len = bm25_context(rows, STORE_PRESET_FIELDS)
    scored = []
    for row in rows:
        s = score_row_with_context(row, query_tokens, STORE_PRESET_FIELDS, idf, avg_len)
        if query_tokens and s == 0:
            continue
        enriched = dict(row)
        enriched["_score"] = round(s + store_preset_boost(row, query_tokens), 3)
        scored.append(enriched)
    scored.sort(key=lambda r: (r["_score"], r.get("name", "")), reverse=True)
    deduped = []
    seen_names = set()
    for row in scored:
        name = row.get("name", "")
        if name and name in seen_names:
            continue
        seen_names.add(name)
        deduped.append(row)
    return deduped[:limit] if limit > 0 else deduped


def pick(rows: list[dict], query_tokens: list[str], fields: tuple[str, ...]):
    """Return (best_row, score). Always returns a row (score 0 = weak fallback)."""
    idf, avg_len = bm25_context(rows, fields)
    best, best_score = None, -1
    for row in rows:
        s = score_row_with_context(row, query_tokens, fields, idf, avg_len)
        if s > best_score:
            best, best_score = row, s
    return best, best_score


def _confidence(score: float) -> str:
    if score >= MIN_CONFIDENT_SCORE:
        return "strong match"
    if score >= MIN_WEAK_SCORE:
        return "weak match - verify manually"
    return "fallback - no strong match, adapt manually"


def build_master_doc(template_text: str, fill: dict[str, str], raw_query: str) -> str:
    out_lines = []
    for line in template_text.splitlines():
        m = re.match(r"^- ([^:]+):\s*$", line)
        if m:
            label = m.group(1).strip()
            if label in fill and fill[label]:
                out_lines.append(f"- {label}: {fill[label]}")
                continue
        if line.strip() == "- YYYY-MM-DD:":
            out_lines.append(
                f"- {date.today().isoformat()}: Seeded by search_design_tokens.py from query "
                f"'{raw_query}'. Review and complete the blank sections before relying on it."
            )
            continue
        out_lines.append(line)
    return "\n".join(out_lines) + "\n"


def run_design_system(args, query_tokens: list[str], raw_query: str) -> int:
    data = args.data
    try:
        palettes = load_rows(data / "color-palettes.csv")
        pairings = load_rows(data / "type-pairings.csv")
        styles = load_rows(data / "style-domains.csv")
        icons = load_rows(data / "icons.csv")
    except FileNotFoundError as exc:
        print(f"Data file not found: {exc}\nKeep the data/ folder next to scripts/, or pass --data.", file=sys.stderr)
        return 2
    try:
        motions = load_rows(data / "motion-presets.csv")
    except FileNotFoundError:
        motions = []

    mode = getattr(args, "mode", None)
    palette_pool = [p for p in palettes if (p.get("mode") or "").lower() == mode] if mode else palettes
    if not palette_pool:
        palette_pool = palettes
    pal, pal_s = pick(palette_pool, query_tokens, ("name", "domain", "notes"))
    typ, typ_s = pick(pairings, query_tokens, ("name", "domain", "notes", "heading_font", "body_font"))
    sty, sty_s = pick(styles, query_tokens, ("name", "domain", "density", "chrome_level", "primary_surfaces", "good_for", "notes"))
    icon_rows = rank(icons, query_tokens, ("name", "meaning", "domain", "style", "source", "notes"), 6)
    mot, mot_s = pick(motions, query_tokens, ("name", "domain", "notes")) if motions else (None, 0)

    on_bg = contrast(pal.get("content", ""), pal.get("bg", ""))
    on_surface = contrast(pal.get("content", ""), pal.get("surface", ""))

    bar = "=" * 60
    print(bar)
    print("Design System Recommendation")
    print(f'Query: "{raw_query}"')
    print(f"Resolved terms: {', '.join(query_tokens) if query_tokens else '(none - showing generic defaults)'}")
    print(bar)

    print(f"\nDIRECTION  (style-domain: {sty.get('name')} - {_confidence(sty_s)})")
    print(f"  domain:   {sty.get('domain')}")
    print(f"  density:  {sty.get('density')} | chrome: {sty.get('chrome_level')}")
    print(f"  surfaces: {sty.get('primary_surfaces')}")
    print(f"  good for: {sty.get('good_for')}")
    print(f"  avoid:    {sty.get('avoid')}")

    print(f"\nCOLOR ROLES  (palette: {pal.get('name')} [{pal.get('mode')}] - {_confidence(pal_s)})")
    print(f"  background {pal.get('bg')} | surface {pal.get('surface')} | content {pal.get('content')}")
    print(f"  muted {pal.get('muted')} | border {pal.get('border')}")
    print(f"  primary {pal.get('primary')} | accent {pal.get('accent')}")
    print(f"  success {pal.get('success')} | warning {pal.get('warning')} | danger {pal.get('danger')}")
    print(f"  contrast: content-on-bg {_aa(on_bg)} | content-on-surface {_aa(on_surface)}")
    p_on, p_r = on_color(pal.get("primary", ""))
    a_on, a_r = on_color(pal.get("accent", ""))
    print(f"  on-text (auto): on primary {p_on} ({p_r:.1f}:1) | on accent {a_on} ({a_r:.1f}:1)  -- do not assume white")

    print(f"\nTYPOGRAPHY  (pairing: {typ.get('name')} - {_confidence(typ_s)})")
    print(f"  heading {typ.get('heading_font')} | body {typ.get('body_font')} | mono {typ.get('mono_font') or '-'}")
    print(f"  scale {typ.get('scale')}")

    if mot:
        print(f"\nMOTION  (preset: {mot.get('name')} - {_confidence(mot_s)})")
        print(f"  easing {mot.get('easing')} | base {mot.get('duration_ms')}ms | hover {mot.get('hover_ms')}ms")
        print(f"  reduced-motion: {mot.get('reduced_motion')}")

    print("\nICONS  (Lucide names, ISC - adapt to your project icon set)")
    if icon_rows:
        print("  " + ", ".join(f"{r.get('name')} ({r.get('meaning')})" for r in icon_rows))
    else:
        print("  No domain-specific matches. Use one consistent set (Lucide ISC) at a single stroke/size.")

    print("\nAVOID")
    if sty.get("avoid"):
        print(f"  - {sty.get('avoid')}")
    print("  - frame stacking; the same border/glow/shadow/radius on every control")
    print("  - one-note palette; glow on everything; gradient soup; decorative dead panels")
    print("  - do not default to cool dark purple/blue/cyan unless the brand, genre, or request justifies it")

    print("\nWHY")
    matched = sty_s >= MIN_CONFIDENT_SCORE or pal_s >= MIN_CONFIDENT_SCORE
    if matched:
        print(f"  The query maps to '{sty.get('domain')}'. Palette, type, and style were chosen for that domain")
        print("  with body-text contrast verified above. Adjust to the real brand and content.")
    else:
        print("  Domain signal is weak or missing. Treat the result as a starting point and re-run with clearer")
        print("  terms (e.g. 'fintech dark dashboard', 'historical ottoman archive mobile game').")

    print("\nNEXT")
    print("  - Adapt roles/fonts to the brand; this is a starting point, not a final kit.")
    print(f"  - Verify real pairs: check_ui_tokens.py --contrast \"{pal.get('content')}\" \"{pal.get('bg')}\"")
    print("  - Persist: re-run with --out design-system/MASTER.md to seed the project design-system file.")

    if args.out is not None:
        out_path = Path(args.out)
        fill = {
            "Selected theme row": f"{sty.get('name')} ({sty.get('domain')})",
            "What this UI must avoid": sty.get("avoid", ""),
            "Mode": pal.get("mode", ""),
            "Background": pal.get("bg", ""),
            "Surface": pal.get("surface", ""),
            "Content": pal.get("content", ""),
            "Muted content": pal.get("muted", ""),
            "Border/divider": pal.get("border", ""),
            "Primary action": f"{pal.get('primary', '')} (text {on_color(pal.get('primary', ''))[0]})",
            "Secondary/accent": f"{pal.get('accent', '')} (text {on_color(pal.get('accent', ''))[0]})",
            "Success": pal.get("success", ""),
            "Warning": pal.get("warning", ""),
            "Danger": pal.get("danger", ""),
            "Heading font": typ.get("heading_font", ""),
            "Body font": typ.get("body_font", ""),
            "Mono/stat font": typ.get("mono_font", ""),
            "Type scale": typ.get("scale", ""),
            "Icon library": "Lucide (ISC) names as a starting set; adapt to the project icon library",
            "Contrast expectations": (
                f"Body text >= 4.5:1 (seed content-on-bg {_aa(on_bg)}, content-on-surface {_aa(on_surface)}); "
                "re-verify on real rendered backgrounds"
            ),
        }
        if mot:
            fill["Motion tone"] = f"{mot.get('name')} - {mot.get('notes', '')}"
            fill["State-change animation"] = f"{mot.get('easing')}, {mot.get('duration_ms')}ms (hover {mot.get('hover_ms')}ms)"
            fill["Reduced-motion behavior"] = mot.get("reduced_motion", "")
        template_path = data.parent / "assets" / "templates" / "design-system-master.md"
        try:
            template_text = template_path.read_text(encoding="utf-8")
            doc = build_master_doc(template_text, fill, raw_query)
        except OSError:
            lines = ["# Design System Master", "",
                     f"Seeded by search_design_tokens.py from query '{raw_query}'. Review before use.", ""]
            for label, value in fill.items():
                if value:
                    lines.append(f"- {label}: {value}")
            doc = "\n".join(lines) + "\n"
        try:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(doc, encoding="utf-8")
            print(f"\nWrote seeded design system to {out_path} (complete the blank/judgment sections).")
        except OSError as exc:
            print(f"\nCould not write {out_path}: {exc}", file=sys.stderr)
            return 2

    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Search curated UI design data with Turkish/synonym query expansion.")
    parser.add_argument("query", nargs="*", help="Domain/style terms, e.g. fintech dark dashboard.")
    parser.add_argument(
        "--kind",
        choices=["palette", "type", "icon", "style", "motion", "store-preset", "store-caption", "both", "all"],
        default="both",
    )
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--data", type=Path, default=default_data_dir())
    parser.add_argument("--design-system", action="store_true",
                        help="Print one consolidated palette + type + style + icon recommendation with contrast.")
    parser.add_argument("--out", nargs="?", const="design-system/MASTER.md", default=None,
                        help="Also write a seeded design-system MASTER.md (default path: design-system/MASTER.md).")
    parser.add_argument("--mode", choices=["light", "dark"], default=None,
                        help="Restrict palette selection to a light or dark palette.")
    args = parser.parse_args(argv)

    raw_query = " ".join(args.query)
    query_tokens = expand_query_tokens(raw_query, args.data)

    if args.design_system or args.out is not None:
        return run_design_system(args, query_tokens, raw_query)

    kinds = (
        ["palette", "type"] if args.kind == "both"
        else ["palette", "type", "icon", "style", "motion", "store-preset", "store-caption"] if args.kind == "all"
        else [args.kind]
    )

    try:
        if "palette" in kinds:
            palettes = load_rows(args.data / "color-palettes.csv")
            if args.mode:
                palettes = [p for p in palettes if (p.get("mode") or "").lower() == args.mode] or palettes
            print_palettes(rank(palettes, query_tokens, ("name", "domain", "notes"), args.limit))
        if len(kinds) > 1:
            print()
        if "type" in kinds:
            pairings = load_rows(args.data / "type-pairings.csv")
            print_pairings(rank(
                pairings, query_tokens,
                ("name", "domain", "notes", "heading_font", "body_font"), args.limit,
            ))
        if len(kinds) > 1 and "type" in kinds and ("icon" in kinds or "style" in kinds):
            print()
        if "icon" in kinds:
            icons = load_rows(args.data / "icons.csv")
            print_icons(rank(
                icons, query_tokens,
                ("name", "meaning", "domain", "style", "source", "notes"), args.limit,
            ))
        if len(kinds) > 1 and "icon" in kinds and "style" in kinds:
            print()
        if "style" in kinds:
            styles = load_rows(args.data / "style-domains.csv")
            print_styles(rank(
                styles, query_tokens,
                ("name", "domain", "density", "chrome_level", "primary_surfaces", "good_for", "notes"),
                args.limit,
            ))
        if len(kinds) > 1 and "motion" in kinds:
            print()
        if "motion" in kinds:
            motions = load_rows(args.data / "motion-presets.csv")
            print_motion(rank(motions, query_tokens, ("name", "domain", "notes"), args.limit))
        if len(kinds) > 1 and "motion" in kinds and ("store-preset" in kinds or "store-caption" in kinds):
            print()
        if "store-preset" in kinds:
            presets = load_rows(args.data / "store-screenshot-presets.csv")
            presets = filter_store_presets(presets, query_tokens)
            print_store_presets(rank_store_presets(presets, query_tokens, args.limit))
        if len(kinds) > 1 and "store-preset" in kinds and "store-caption" in kinds:
            print()
        if "store-caption" in kinds:
            captions = load_rows(args.data / "store-caption-patterns.csv")
            print_store_captions(rank(
                captions, query_tokens,
                ("name", "domain", "screenshot_position", "intent", "good_pattern", "avoid", "localization_notes"),
                args.limit,
            ))
    except FileNotFoundError as exc:
        print(f"Data file not found: {exc}\nKeep the data/ folder next to scripts/, or pass --data.", file=sys.stderr)
        return 2

    print("\nThese are metadata starting points, not bundled assets or a fixed kit. Adapt to the brand, "
          "verify contrast for real content (check_ui_tokens.py --contrast FG BG), and keep external "
          "font/icon licenses if assets are later bundled.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
