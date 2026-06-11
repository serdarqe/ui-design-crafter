#!/usr/bin/env python3
"""Compose raw screenshots into store-ready HTML assets and optional PNGs.

The script keeps the first step deterministic and dependency-light:

- Always writes HTML/CSS compositions plus manifest.store.json.
- Optionally renders PNGs with Node Playwright when available.
- Can render no-caption/raw-compliant PNGs with Pillow when browser rendering is not needed.
- Uses only metadata from data/store-screenshot-presets.csv; it bundles no device
  mockup images, screenshots, or paid templates.

Examples:
    python scripts/export_store_screenshots.py --input raw/home.png --preset google-play-phone-app-portrait --caption "Track every habit"
    python scripts/export_store_screenshots.py --manifest store-assets/raw/manifest.raw.json --preset app-store-iphone-6-9-portrait-a --captions "Plan your week|Review every task"
    python scripts/export_store_screenshots.py --input raw/gameplay.png --platform google-play --device "phone game" --orientation landscape --style full-bleed-gameplay --render playwright
    python scripts/export_store_screenshots.py --input raw/home.png --preset google-play-phone-app-portrait --style no-caption/raw-compliant --render pillow
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


STYLE_CHOICES = [
    "clean-device-frame",
    "full-bleed-gameplay",
    "split-caption",
    "top-caption",
    "bottom-caption",
    "no-caption/raw-compliant",
]

DEFAULT_THEME = {
    "bg": "#111418",
    "surface": "#171b21",
    "fg": "#f5f7fb",
    "muted": "#b9c0cc",
    "accent": "#6aa5ff",
}

THEMES = {
    "default": DEFAULT_THEME,
    "light": {
        "bg": "#f5f7fb",
        "surface": "#ffffff",
        "fg": "#17202c",
        "muted": "#5c6878",
        "accent": "#2770d8",
    },
    "dark": DEFAULT_THEME,
    "horror": {
        "bg": "#0b0d0f",
        "surface": "#141212",
        "fg": "#f1ece5",
        "muted": "#b9aaa1",
        "accent": "#8c2f2f",
    },
    "hyper-casual": {
        "bg": "#f5fbff",
        "surface": "#ffffff",
        "fg": "#10212e",
        "muted": "#526b7a",
        "accent": "#ff8a3d",
    },
    "saas": {
        "bg": "#eef3f7",
        "surface": "#ffffff",
        "fg": "#172231",
        "muted": "#607184",
        "accent": "#236f8e",
    },
}

RISK_WORDS = [
    "best",
    "#1",
    "top",
    "new",
    "free",
    "discount",
    "sale",
    "million downloads",
    "download now",
    "install now",
    "play now",
    "try now",
]


def default_skill_dir() -> Path:
    return Path(__file__).resolve().parent.parent


def default_data_dir() -> Path:
    return default_skill_dir() / "data"


def default_template_path() -> Path:
    return default_skill_dir() / "assets" / "templates" / "store-screenshot-template.html"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slug(value: str, fallback: str = "item") -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or fallback


def load_rows(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_presets(data_dir: Path) -> list[dict]:
    return load_rows(data_dir / "store-screenshot-presets.csv")


def score_preset(row: dict, platform: str | None, device: str | None, orientation: str | None) -> int:
    score = 0
    if platform and row.get("platform", "").lower() == platform.lower():
        score += 20
    if orientation and row.get("orientation", "").lower() == orientation.lower():
        score += 12
    if device:
        wanted = set(re.split(r"[^a-z0-9]+", device.lower()))
        have = set(re.split(r"[^a-z0-9]+", row.get("device_group", "").lower()))
        score += 5 * len(wanted & have)
    if "primary" in row.get("required_or_optional", ""):
        score += 2
    if "required" in row.get("required_or_optional", ""):
        score += 1
    return score


def select_preset(args) -> dict:
    if args.width and args.height:
        platform = args.platform or "custom"
        return {
            "name": args.preset or f"custom-{args.width}x{args.height}",
            "platform": platform,
            "device_group": args.device or "custom",
            "orientation": args.orientation or ("portrait" if args.height > args.width else "landscape"),
            "width": str(args.width),
            "height": str(args.height),
            "required_or_optional": "custom",
            "notes": "Custom size supplied by CLI.",
            "source_url": "",
            "last_checked": "",
        }

    presets = load_presets(args.data)
    if args.preset:
        wanted = args.preset.strip().lower()
        for row in presets:
            if row.get("name", "").strip().lower() == wanted:
                return row
        raise SystemExit(f"Preset not found: {args.preset}")

    platform = args.platform or "google-play"
    orientation = args.orientation or "portrait"
    device = args.device or ("phone app" if platform == "google-play" else "iphone 6.9 inch")
    candidates = [row for row in presets if row.get("platform") == platform]
    if not candidates:
        candidates = presets
    candidates.sort(key=lambda row: (score_preset(row, platform, device, orientation), row.get("name", "")), reverse=True)
    if not candidates:
        raise SystemExit("No store screenshot presets found.")
    return candidates[0]


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def resolve_capture_path(raw_path: str, manifest_path: Path | None, cwd: Path) -> Path:
    p = Path(raw_path)
    if p.is_absolute():
        return p
    candidates = []
    if manifest_path:
        candidates.append(manifest_path.parent / p)
    candidates.append(cwd / p)
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    return candidates[0].resolve()


def captures_from_manifest(path: Path, cwd: Path) -> list[dict]:
    payload = read_json(path)
    rows = payload.get("captures")
    if not isinstance(rows, list):
        raise SystemExit(f"{path} must contain a 'captures' list.")
    captures = []
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            continue
        raw_path = row.get("path") or row.get("source_path") or row.get("file")
        if not raw_path:
            raise SystemExit(f"Capture row {index} in {path} has no path/source_path/file.")
        source_path = resolve_capture_path(str(raw_path), path, cwd)
        capture = dict(row)
        capture["source_path"] = str(source_path)
        capture.setdefault("screen_name", source_path.stem)
        capture.setdefault("source", "manifest")
        captures.append(capture)
    return captures


def captures_from_inputs(paths: list[str], cwd: Path) -> list[dict]:
    captures = []
    for raw in paths:
        p = Path(raw)
        if not p.is_absolute():
            p = cwd / p
        p = p.resolve()
        captures.append({
            "source_path": str(p),
            "screen_name": p.stem,
            "source": "user-provided",
            "platform": "unknown",
        })
    return captures


def parse_caption_file(path: Path) -> tuple[list[str], dict[str, str]]:
    if not path:
        return [], {}
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        payload = json.loads(text)
        if isinstance(payload, list):
            return [str(item) for item in payload], {}
        if isinstance(payload, dict):
            return [], {str(k): str(v) for k, v in payload.items()}
        raise SystemExit(f"Caption JSON must be a list or object: {path}")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines, {}


def parse_text_sequence_file(path: Path, label: str) -> tuple[list[str], dict[str, str]]:
    if not path:
        return [], {}
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        payload = json.loads(text)
        if isinstance(payload, list):
            return [str(item) for item in payload], {}
        if isinstance(payload, dict):
            return [], {str(k): str(v) for k, v in payload.items()}
        raise SystemExit(f"{label} JSON must be a list or object: {path}")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines, {}


def parse_captions(args) -> tuple[list[str], dict[str, str]]:
    captions = []
    mapping = {}
    if args.captions:
        sep = "||" if "||" in args.captions else "|"
        captions.extend([part.strip() for part in args.captions.split(sep)])
    if args.caption:
        captions.extend(args.caption)
    if args.caption_file:
        file_captions, file_mapping = parse_caption_file(args.caption_file)
        captions.extend(file_captions)
        mapping.update(file_mapping)
    return captions, mapping


def parse_alt_texts(args) -> tuple[list[str], dict[str, str]]:
    alt_texts = []
    mapping = {}
    if args.alt_texts:
        sep = "||" if "||" in args.alt_texts else "|"
        alt_texts.extend([part.strip() for part in args.alt_texts.split(sep)])
    if args.alt_text:
        alt_texts.extend(args.alt_text)
    if args.alt_text_file:
        file_texts, file_mapping = parse_text_sequence_file(args.alt_text_file, "Alt text")
        alt_texts.extend(file_texts)
        mapping.update(file_mapping)
    return alt_texts, mapping


def caption_for(capture: dict, index: int, captions: list[str], mapping: dict[str, str]) -> str:
    keys = [
        str(capture.get("id") or ""),
        str(capture.get("screen_name") or ""),
        Path(str(capture.get("source_path") or "")).stem,
    ]
    for key in keys:
        if key in mapping:
            return mapping[key]
    if index < len(captions):
        return captions[index]
    return ""


def alt_text_for(capture: dict, index: int, alt_texts: list[str], mapping: dict[str, str], caption: str) -> str:
    keys = [
        str(capture.get("id") or ""),
        str(capture.get("screen_name") or ""),
        Path(str(capture.get("source_path") or "")).stem,
    ]
    for key in keys:
        if key in mapping:
            return collapse_text(mapping[key])[:140]
    if index < len(alt_texts):
        return collapse_text(alt_texts[index])[:140]
    screen = str(capture.get("screen_name") or keys[-1] or "store asset")
    if caption:
        return collapse_text(f"{screen}: {caption}")[:140]
    return collapse_text(f"{screen} screen")[:140]


def collapse_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def theme_tokens(args) -> dict[str, str]:
    base = dict(THEMES.get((args.theme or "default").lower(), DEFAULT_THEME))
    for key in ["bg", "surface", "fg", "muted", "accent"]:
        value = getattr(args, key, None)
        if value:
            base[key] = value
    return base


def file_uri(path: Path) -> str:
    try:
        return path.as_uri()
    except ValueError:
        return "file:///" + quote(str(path.resolve()).replace("\\", "/"))


def image_fit_for(style: str, args) -> str:
    if args.image_fit:
        return args.image_fit
    if style == "full-bleed-gameplay":
        return "cover"
    return "contain"


def risk_warnings(text: str) -> list[str]:
    lower = (text or "").lower()
    warnings = []
    for word in RISK_WORDS:
        if word in lower:
            warnings.append(f"copy-risk:{word}")
    return warnings


def render_template(template: str, values: dict[str, str]) -> str:
    out = template
    for key, value in values.items():
        out = out.replace("{{" + key + "}}", str(value))
    missing = sorted(set(re.findall(r"{{([a-zA-Z0-9_]+)}}", out)))
    if missing:
        raise SystemExit(f"Template placeholders were not filled: {', '.join(missing)}")
    return out


def build_html(template: str, capture: dict, preset: dict, caption: str, alt_text: str, args, index: int) -> str:
    width, height = int(preset["width"]), int(preset["height"])
    style = args.style.replace("/", "-")
    source_path = Path(capture["source_path"]).resolve()
    tokens = theme_tokens(args)
    screen = str(capture.get("screen_name") or source_path.stem)
    eyebrow = args.eyebrow or str(capture.get("screen_role") or capture.get("source") or "")
    note = args.note or ""
    copy_hidden = "true" if args.style == "no-caption/raw-compliant" or not caption else "false"
    aria = alt_text or caption or f"{screen} store screenshot"
    values = {
        "lang": html.escape(args.lang or (args.locale.split("-")[0] if args.locale else "en")),
        "title": html.escape(f"{index + 1:02d} {screen} store screenshot"),
        "canvas_width": width,
        "canvas_height": height,
        "bg": tokens["bg"],
        "surface": tokens["surface"],
        "fg": tokens["fg"],
        "muted": tokens["muted"],
        "accent": tokens["accent"],
        "image_fit": image_fit_for(args.style, args),
        "style_class": f"style-{slug(style)}",
        "aria_label": html.escape(aria),
        "copy_hidden": copy_hidden,
        "eyebrow": html.escape(eyebrow),
        "caption": html.escape(caption),
        "note": html.escape(note),
        "image_uri": html.escape(file_uri(source_path), quote=True),
        "image_alt": html.escape(alt_text or f"{screen} source screen", quote=True),
    }
    return render_template(template, values)


def parse_hex_rgb(value: str) -> tuple[int, int, int]:
    raw = (value or "").strip()
    if raw.startswith("#"):
        raw = raw[1:]
    if len(raw) == 3:
        raw = "".join(ch * 2 for ch in raw)
    if len(raw) != 6 or not re.fullmatch(r"[0-9a-fA-F]{6}", raw):
        raise ValueError(f"unsupported color {value!r}; use #RRGGBB")
    return int(raw[0:2], 16), int(raw[2:4], 16), int(raw[4:6], 16)


def render_with_pillow(source_path: Path, png_path: Path, width: int, height: int, args) -> tuple[bool, str]:
    if args.style != "no-caption/raw-compliant":
        return False, "pillow-render-unsupported:style-requires-browser"
    try:
        from PIL import Image
    except Exception:
        return False, "pillow-render-unavailable:pillow-not-found"

    try:
        tokens = theme_tokens(args)
        background_rgb = parse_hex_rgb(tokens["bg"])
        fit = image_fit_for(args.style, args)
        with Image.open(source_path) as image:
            image = image.convert("RGBA")
            scale = min(width / image.width, height / image.height) if fit == "contain" else max(width / image.width, height / image.height)
            resized_size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
            resample = getattr(getattr(Image, "Resampling", Image), "LANCZOS")
            image = image.resize(resized_size, resample)

            if fit == "cover":
                left = max(0, (image.width - width) // 2)
                top = max(0, (image.height - height) // 2)
                image = image.crop((left, top, left + width, top + height))
                paste_at = (0, 0)
            else:
                paste_at = ((width - image.width) // 2, (height - image.height) // 2)

            canvas = Image.new("RGB", (width, height), background_rgb)
            alpha = image.getchannel("A")
            canvas.paste(image.convert("RGB"), paste_at, alpha)
            png_path.parent.mkdir(parents=True, exist_ok=True)
            canvas.save(png_path, "PNG")
        return True, "rendered"
    except Exception as exc:
        return False, f"pillow-render-failed:{exc}"


def write_outputs(captures: list[dict], preset: dict, captions: list[str], caption_map: dict[str, str], args) -> dict:
    template_path = args.template or default_template_path()
    if not template_path.exists():
        raise SystemExit(f"Template not found: {template_path}")
    template = template_path.read_text(encoding="utf-8")

    width, height = int(preset["width"]), int(preset["height"])
    platform = preset.get("platform") or args.platform or "store"
    preset_name = preset.get("name") or f"{width}x{height}"
    out_dir = args.out / slug(platform) / slug(preset_name) / slug(args.locale or "und")
    out_dir.mkdir(parents=True, exist_ok=True)

    outputs = []
    alt_texts, alt_text_map = parse_alt_texts(args)
    for index, capture in enumerate(captures):
        source = Path(capture["source_path"]).resolve()
        if not source.exists():
            raise SystemExit(f"Raw screenshot not found: {source}")
        screen = str(capture.get("screen_name") or source.stem)
        caption = caption_for(capture, index, captions, caption_map)
        alt_text = alt_text_for(capture, index, alt_texts, alt_text_map, caption)
        basename = f"{index + 1:02d}-{slug(screen)}-{slug(args.style.replace('/', '-'))}"
        html_path = out_dir / f"{basename}.html"
        png_path = out_dir / f"{basename}.png"
        page = build_html(template, capture, preset, caption, alt_text, args, index)
        html_path.write_text(page, encoding="utf-8")

        warnings = risk_warnings(caption)
        png_status = None
        if args.render == "playwright":
            ok, message = render_with_playwright(html_path, png_path, width, height)
            png_status = "rendered" if ok else "render-failed"
            if not ok:
                warnings.append(message)
                if args.require_png:
                    raise SystemExit(f"PNG render failed for {html_path}: {message}")
        elif args.render == "pillow":
            ok, message = render_with_pillow(source, png_path, width, height, args)
            png_status = "rendered" if ok else "render-failed"
            if not ok:
                warnings.append(message)
                if args.require_png:
                    raise SystemExit(f"PNG render failed for {source}: {message}")
        else:
            png_status = "not-rendered"

        outputs.append({
            "id": basename,
            "screen_name": screen,
            "screen_role": capture.get("screen_role"),
            "source": capture.get("source"),
            "source_path": str(source),
            "html_path": str(html_path.resolve()),
            "png_path": str(png_path.resolve()) if png_status == "rendered" else None,
            "caption": caption,
            "alt_text": alt_text,
            "style": args.style,
            "width": width,
            "height": height,
            "platform": platform,
            "preset": preset_name,
            "locale": args.locale,
            "theme": args.theme,
            "status": "png-ready" if png_status == "rendered" else "html-ready",
            "render_status": png_status,
            "warnings": warnings,
        })

    manifest = {
        "version": 1,
        "created_at": utc_now(),
        "generator": "ui-design-crafter/scripts/export_store_screenshots.py",
        "source_manifest": str(args.manifest) if args.manifest else None,
        "render_mode": args.render,
        "target": {
            "platform": platform,
            "preset": preset_name,
            "device_group": preset.get("device_group"),
            "orientation": preset.get("orientation"),
            "width": width,
            "height": height,
            "required_or_optional": preset.get("required_or_optional"),
            "source_url": preset.get("source_url"),
            "last_checked": preset.get("last_checked"),
            "locale": args.locale,
            "theme": args.theme,
            "style": args.style,
        },
        "outputs": outputs,
    }
    manifest_path = args.out / "manifest.store.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"manifest_path": manifest_path, "manifest": manifest, "out_dir": out_dir}


def render_with_playwright(html_path: Path, png_path: Path, width: int, height: int) -> tuple[bool, str]:
    node = shutil.which("node")
    if not node:
        return False, "playwright-render-unavailable:node-not-found"
    script = f"""
const fs = require('fs');
let chromium;
try {{
  chromium = require('playwright').chromium;
}} catch (err) {{
  console.error('playwright-render-unavailable:playwright-not-found');
  process.exit(7);
}}
(async () => {{
  const browser = await chromium.launch({{ headless: true }});
  const page = await browser.newPage({{ viewport: {{ width: {width}, height: {height} }}, deviceScaleFactor: 1 }});
  await page.goto({json.dumps(file_uri(html_path.resolve()))}, {{ waitUntil: 'networkidle' }});
  await page.screenshot({{ path: {json.dumps(str(png_path.resolve()))}, fullPage: false }});
  await browser.close();
}})().catch((err) => {{
  console.error(err && err.stack ? err.stack : String(err));
  process.exit(1);
}});
"""
    proc = subprocess.run([node, "-e", script], text=True, capture_output=True)
    if proc.returncode != 0:
        msg = (proc.stderr or proc.stdout or "playwright-render-failed").strip().splitlines()[-1]
        return False, msg
    return True, "rendered"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Compose raw screenshots into store-ready HTML assets and optional PNGs.")
    parser.add_argument("--manifest", type=Path, help="Raw manifest JSON from store-capture-workflow.md.")
    parser.add_argument("--input", action="append", default=[], help="Raw screenshot path. Repeat for multiple screenshots.")
    parser.add_argument("--preset", help="Preset name from data/store-screenshot-presets.csv.")
    parser.add_argument("--platform", choices=["app-store", "google-play", "custom"], default=None)
    parser.add_argument("--device", help="Device group query, e.g. 'phone app', 'phone game', 'iphone 6.9 inch'.")
    parser.add_argument("--orientation", choices=["portrait", "landscape", "any"], default=None)
    parser.add_argument("--width", type=int, help="Custom output width; requires --height.")
    parser.add_argument("--height", type=int, help="Custom output height; requires --width.")
    parser.add_argument("--caption", action="append", default=[], help="Caption for one screenshot. Repeat for sequence order.")
    parser.add_argument("--captions", help="Pipe-separated captions, e.g. 'Plan your week|Review every task'.")
    parser.add_argument("--caption-file", type=Path, help="Text lines, JSON list, or JSON object keyed by screen id/name.")
    parser.add_argument("--alt-text", action="append", default=[], help="Google Play alt text for one asset. Repeat for sequence order.")
    parser.add_argument("--alt-texts", help="Pipe-separated Google Play alt text values.")
    parser.add_argument("--alt-text-file", type=Path, help="Text lines, JSON list, or JSON object keyed by screen id/name.")
    parser.add_argument("--style", choices=STYLE_CHOICES, default="top-caption")
    parser.add_argument("--theme", default="default", help="Theme token preset: default, light, dark, horror, hyper-casual, saas.")
    parser.add_argument("--bg", help="Override background color.")
    parser.add_argument("--surface", help="Override surface color.")
    parser.add_argument("--fg", help="Override foreground/text color.")
    parser.add_argument("--muted", help="Override muted text color.")
    parser.add_argument("--accent", help="Override accent color.")
    parser.add_argument("--image-fit", choices=["contain", "cover"], default=None)
    parser.add_argument("--eyebrow", default="", help="Small label above caption.")
    parser.add_argument("--note", default="", help="Short supporting note below caption.")
    parser.add_argument("--locale", default="en-US")
    parser.add_argument("--lang", default=None)
    parser.add_argument("--out", type=Path, default=Path("store-assets"))
    parser.add_argument("--data", type=Path, default=default_data_dir())
    parser.add_argument("--template", type=Path, default=default_template_path())
    parser.add_argument("--render", choices=["html-only", "playwright", "pillow"], default="html-only")
    parser.add_argument("--require-png", action="store_true", help="Fail if the requested PNG renderer cannot create PNG output.")
    args = parser.parse_args(argv)

    if bool(args.width) ^ bool(args.height):
        raise SystemExit("--width and --height must be used together.")
    if not args.manifest and not args.input:
        raise SystemExit("Pass --manifest or at least one --input raw screenshot.")

    cwd = Path.cwd()
    captures = []
    if args.manifest:
        captures.extend(captures_from_manifest(args.manifest.resolve(), cwd))
    if args.input:
        captures.extend(captures_from_inputs(args.input, cwd))
    if not captures:
        raise SystemExit("No captures found.")

    preset = select_preset(args)
    captions, caption_map = parse_captions(args)
    result = write_outputs(captures, preset, captions, caption_map, args)

    manifest = result["manifest"]
    print(f"Wrote {len(manifest['outputs'])} store composition(s).")
    print(f"Manifest: {result['manifest_path']}")
    print(f"Output folder: {result['out_dir']}")
    if args.render == "html-only":
        print("HTML is ready. Use --render playwright for full CSS compositions, or --render pillow for no-caption/raw-compliant PNGs.")
    elif any(o["render_status"] != "rendered" for o in manifest["outputs"]):
        print("Some PNG renders were skipped or failed; see manifest warnings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
