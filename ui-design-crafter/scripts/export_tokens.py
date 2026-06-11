#!/usr/bin/env python3
"""Export a curated palette to developer color tokens (CSS / Tailwind / W3C DTCG).

Closes the design->code loop: pick a palette from data/color-palettes.csv (or one
produced by search_design_tokens.py --design-system) and emit ready-to-paste color
tokens. Colors only; adapt fonts/spacing/radius separately.

Usage:
    python export_tokens.py slate-admin-dark
    python export_tokens.py fintech-trust-light --format css
    python export_tokens.py education-study-light --format tailwind
    python export_tokens.py cozy-lifestyle-light --format dtcg --out tokens.json
    python export_tokens.py --list
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# Palette role columns exported as color tokens, in a sensible order.
ROLES = ["bg", "surface", "content", "muted", "border",
         "primary", "accent", "success", "warning", "danger"]
# Filled roles also get an accessible on-color (the text/icon placed on the fill).
FILL_ROLES = ["primary", "accent", "success", "warning", "danger"]
ON_LIGHT, ON_DARK = "#ffffff", "#05070a"


def _lum(hx: str):
    hx = hx.strip().lstrip("#")
    if len(hx) == 3:
        hx = "".join(c * 2 for c in hx)
    if len(hx) != 6 or any(c not in "0123456789abcdefABCDEF" for c in hx):
        return None
    r, g, b = (int(hx[i:i + 2], 16) for i in (0, 2, 4))

    def ch(c):
        c /= 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def _contrast(a: str, b: str) -> float:
    la, lb = _lum(a), _lum(b)
    if la is None or lb is None:
        return 0.0
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def on_color(fill_hex: str):
    """Best readable text color on a fill: white or near-black, whichever has more contrast."""
    light, dark = _contrast(ON_LIGHT, fill_hex), _contrast(ON_DARK, fill_hex)
    return (ON_LIGHT, light) if light >= dark else (ON_DARK, dark)


def on_tokens(tokens: dict[str, str]):
    """Return ({on-role: hex}, [(role, hex, ratio)]) for filled roles; flags ratio < 4.5."""
    out, warn = {}, []
    for role in FILL_ROLES:
        fill = tokens.get(role)
        if not fill:
            continue
        hexv, ratio = on_color(fill)
        out[f"on-{role}"] = hexv
        if ratio < 4.5:
            warn.append((role, hexv, ratio))
    return out, warn


def default_data_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "data"


def load_palettes(data_dir: Path) -> list[dict]:
    path = data_dir / "color-palettes.csv"
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def find_palette(rows: list[dict], name: str):
    name = name.strip().lower()
    for row in rows:
        if (row.get("name", "") or "").strip().lower() == name:
            return row
    return None


def tokens_from(row: dict) -> dict[str, str]:
    return {role: (row.get(role, "") or "").strip() for role in ROLES if (row.get(role, "") or "").strip()}


def emit_css(name: str, mode: str, tokens: dict[str, str]) -> str:
    lines = [f"/* {name} ({mode}) — color tokens. Adapt fonts/spacing/radius separately. */", ":root {"]
    for role, value in tokens.items():
        lines.append(f"  --color-{role}: {value};")
    lines.append("}")
    return "\n".join(lines) + "\n"


def emit_tailwind(name: str, mode: str, tokens: dict[str, str]) -> str:
    body = ",\n".join(f"        '{role}': '{value}'" for role, value in tokens.items())
    return (
        f"// {name} ({mode}) — paste into tailwind.config.js theme.extend.colors\n"
        "module.exports = {\n"
        "  theme: {\n"
        "    extend: {\n"
        "      colors: {\n"
        f"{body}\n"
        "      }\n"
        "    }\n"
        "  }\n"
        "};\n"
    )


def emit_dtcg(name: str, mode: str, tokens: dict[str, str]) -> str:
    payload = {
        "$description": f"{name} ({mode}) color tokens",
        "color": {role: {"$type": "color", "$value": value} for role, value in tokens.items()},
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


EMITTERS = {"css": emit_css, "tailwind": emit_tailwind, "dtcg": emit_dtcg}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Export a curated palette to CSS / Tailwind / DTCG color tokens.")
    parser.add_argument("palette", nargs="?", help="Palette name from data/color-palettes.csv.")
    parser.add_argument("--format", choices=["css", "tailwind", "dtcg", "all"], default="all")
    parser.add_argument("--data", type=Path, default=default_data_dir())
    parser.add_argument("--out", type=Path, default=None, help="Write to a file instead of stdout.")
    parser.add_argument("--list", action="store_true", help="List available palette names and exit.")
    args = parser.parse_args(argv)

    try:
        rows = load_palettes(args.data)
    except FileNotFoundError as exc:
        print(f"color-palettes.csv not found: {exc}\nPass --data <dir> pointing at the skill's data/ folder.", file=sys.stderr)
        return 2

    if args.list or not args.palette:
        print("Available palettes:")
        for row in rows:
            print(f"  {row.get('name')}  [{row.get('mode')}]  {row.get('domain')}")
        if not args.palette and not args.list:
            print("\nPass a palette name, e.g.: export_tokens.py slate-admin-dark", file=sys.stderr)
            return 2
        return 0

    row = find_palette(rows, args.palette)
    if row is None:
        print(f"Palette '{args.palette}' not found. Use --list to see names.", file=sys.stderr)
        return 2

    tokens = tokens_from(row)
    on, on_warnings = on_tokens(tokens)
    tokens.update(on)
    name, mode = row.get("name", args.palette), row.get("mode", "")
    formats = ["css", "tailwind", "dtcg"] if args.format == "all" else [args.format]
    blocks = []
    for fmt in formats:
        if args.format == "all":
            blocks.append(f"===== {fmt.upper()} =====")
        blocks.append(EMITTERS[fmt](name, mode, tokens))
    output = "\n".join(blocks)

    if args.out is not None:
        try:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(output, encoding="utf-8")
            print(f"Wrote {name} tokens ({args.format}) to {args.out}")
        except OSError as exc:
            print(f"Could not write {args.out}: {exc}", file=sys.stderr)
            return 2
    else:
        print(output)
    if on_warnings:
        note = "; ".join(f"on-{r} {h} {ratio:.1f}:1" for r, h, ratio in on_warnings)
        print(f"Note: some on-colors are below 4.5:1 (fine for large/bold button text only): {note}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
