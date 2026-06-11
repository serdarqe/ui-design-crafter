# UI Design Crafter

A skill for **Claude Code** and **Codex** that turns a UI request into a coherent,
production-ready interface for apps, games, dashboards, HUDs, menus, panels, and
store listing assets. It actively fights the "AI-generated UI" look: frame
stacking, glow on everything, gradient soup, one-note dark-purple palettes, and
gold-frame-on-everything.

It is guidance + data + tooling, not a component library or a Figma plugin.

## Why It Exists

Most generated UI looks generated: every box framed, everything glowing, a single
hue tinted into a whole theme, decorative panels with no information. This skill
encodes the "why it happens and how to fix it" as reference docs, plus scripts that
measure common problems such as WCAG contrast, frame stacking, over-dark screenshots,
store screenshot dimensions, and ASO copy risks.

For store work, it keeps the order strict: design the real UI, capture evidence,
compose store assets, then run store asset QA before delivery.

## What's Inside

| Path | What it is |
|---|---|
| `ui-design-crafter/SKILL.md` | Skill entry point: workflow, design rules, and a router to the focused references below. |
| `ui-design-crafter/references/` | Focused guides for research foundations, color, app/game UI, components, theme execution, backgrounds, accessibility, internationalization, motion, performance, UX writing, visual QA, store screenshots, and ASO. |
| `ui-design-crafter/scripts/` | Python tools for token search, contrast/style audits, visual smoke checks, token export, store screenshot composition, and store asset/listing validation. |
| `ui-design-crafter/data/` | Curated metadata: color palettes, type pairings, icon names, style domains, motion presets, query aliases, store screenshot presets, and ASO copy patterns. No fonts or images are bundled. |
| `ui-design-crafter/assets/templates/` | Project-local design-system and store screenshot templates. |
| `ui-design-crafter/agents/openai.yaml` | Codex interface metadata. |

## Install

Drop the `ui-design-crafter/` folder into your skills directory:

- **Claude Code:** `~/.claude/skills/ui-design-crafter/`
- **Codex:** `~/.codex/skills/ui-design-crafter/`

On Windows these live under `%USERPROFILE%\.claude\skills\` and
`%USERPROFILE%\.codex\skills\`.

## Tools

Run commands from inside `ui-design-crafter/`.

```bash
# WCAG contrast of two colors, or audit a codebase for UI/AI-look risks
python scripts/check_ui_tokens.py --contrast "#1f2937" "#ffffff"
python scripts/check_ui_tokens.py src/ --strict

# Domain-based starter design system
python scripts/search_design_tokens.py "fintech dark dashboard" --design-system
python scripts/search_design_tokens.py "cozy farming sim" --design-system --mode light --out design-system/MASTER.md
python scripts/search_design_tokens.py "Google Play phone portrait" --kind store-preset
python scripts/search_design_tokens.py "horror game screenshot 3 shop" --kind store-caption

# Compose raw screenshots into store-ready HTML assets and manifest.store.json
python scripts/export_store_screenshots.py --input raw/home.png --preset google-play-phone-app-portrait --caption "Track every habit"
python scripts/export_store_screenshots.py --manifest store-assets/raw/manifest.raw.json --preset app-store-iphone-6-9-portrait-a --style clean-device-frame

# Browserless PNG output for screenshot-only compliant assets
python scripts/export_store_screenshots.py --input raw/home.png --preset google-play-phone-app-portrait --style no-caption/raw-compliant --render pillow

# Validate final store assets and listing metadata before upload
python scripts/check_store_assets.py store-assets/google-play/manifest.store.json --min-count 2
python scripts/check_store_assets.py store-assets/app-store/ --preset app-store-iphone-6-9-portrait-a --strict
python scripts/check_store_assets.py --platform google-play --locale en-US --title "CalmCare Health" --short "Track habits gently." --full "Daily health notes and gentle reminders."

# Visual smoke check on screenshots + browser metrics
python scripts/visual_smoke_check.py --screenshots out/mobile.png out/desktop.png --strict

# Export a palette to CSS, Tailwind, or W3C DTCG color tokens
python scripts/export_tokens.py slate-admin-light --format css

# Search your own reference-image library by metadata
python scripts/search_reference_library.py "hud inventory" --manifest path/to/image-library-manifest.csv
```

## Data And Licensing Notes

- No fonts or images are bundled.
- `data/icons.csv` lists Lucide icon names only. Lucide is ISC licensed:
  https://lucide.dev
- `data/type-pairings.csv` lists font family names only. Each font remains under
  its own license from its foundry or provider.
- Color palettes are original, contrast-checked metadata.
- Code and docs are MIT licensed. See `ui-design-crafter/LICENSE`.
- Reference-image search is bring-your-own: point it at a folder you own or have
  permission to use.

## Notes For Users

- The skill is opinionated by design: it pushes back on generic dark-tech styling,
  decorative frames, inaccessible contrast, and fake store claims.
- Results from `data/` and `--design-system` are starting points to adapt, not a
  fixed kit.
- Store rules change. Re-check official Apple and Google Play sources before final
  production upload.

