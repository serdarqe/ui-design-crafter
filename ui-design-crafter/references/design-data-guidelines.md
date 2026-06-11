# Design Data Guidelines

Use this when adding or querying `data/` files. The data layer is a searchable catalog of metadata, not a bundled asset library.

## Safe data policy

- Store names, tags, domains, notes, roles, and source/license metadata.
- Do not store font binaries, icon SVGs, paid UI kits, screenshots, copied Figma assets, or marketplace assets.
- Prefer open sources and generated/custom palettes.
- Keep license/source fields when a row points to an external library.
- Treat search results as starting points, not a finished design system.

## Current data files

- `data/color-palettes.csv`: original curated starter palettes with contrast-aware roles.
- `data/type-pairings.csv`: font pairing metadata. Font files are not included.
- `data/motion-presets.csv`: easing/duration/hover/reduced-motion presets by domain. Values only; no animation code.
- `data/icons.csv`: icon-name metadata only. It references Lucide icon names, not SVG files.
- `data/style-domains.csv`: domain calibration rules for density, chrome, surfaces, and what to avoid.
- `data/query-aliases.csv`: Turkish and synonym query expansion metadata. It maps user wording to searchable domain terms and stores no assets.
- `data/store-screenshot-presets.csv`: App Store / Google Play screenshot and feature-graphic preset metadata, with source URL and `last_checked` date per row.
- `data/store-caption-patterns.csv`: ASO caption/story-order metadata by app/game domain and screenshot position.

Current coverage includes app/product domains plus game genres such as horror, hyper casual, casual puzzle, fantasy RPG, sci-fi tactical, racing, strategy, historical/period, idle/incremental, merge, tower defense, card battler, roguelike, platformer, FPS/action, survival crafting, rhythm/music, casino/slot, sports, city builder, farming/cozy sim, marketplace, wellness, education, personal finance, and medical operations.

## Licensing notes

- Google Fonts font metadata is safe to reference, but if font files are bundled later, include each font license.
- Lucide rows are icon names only; if actual SVG/icon packages are bundled later, include the ISC license notice.
- Generated/custom palettes should use `custom/generated` or equivalent source notes.
- Brand palettes, paid fonts, paid icons, and copied UI kits must not be imported as if they were open data.

## Search behavior

Use `scripts/search_design_tokens.py` to query palettes, type pairings, icons, style domains, motion presets, store screenshot presets, and store caption patterns. Search uses Turkish/synonym expansion plus a lightweight BM25-style score with confidence labels; weak matches must be treated as prompts to clarify or search again, not as final recommendations. Search results should be adapted to the product's existing tokens, target platform, accessibility needs, and visual tone.

The search script normalizes Turkish characters and expands aliases from `query-aliases.csv`, so Turkish or mixed-language prompts such as "korku gorev ana menu" can still find horror, mission, and menu guidance.

Store data examples:

```powershell
python scripts/search_design_tokens.py "Google Play phone portrait" --kind store-preset
python scripts/search_design_tokens.py "App Store iPhone 6.9 landscape" --kind store-preset
python scripts/search_design_tokens.py "horror mobile game screenshot 3 shop" --kind store-caption
python scripts/search_design_tokens.py "magaza gorseli tablet" --kind store-preset
```

## Store screenshot data rules

- Every `store-screenshot-presets.csv` row must include `source_url` and `last_checked`.
- Do not invent exact App Store or Google Play dimensions from memory. Verify official pages before adding or changing preset rows.
- Use one row per exact width/height/orientation pair so scripts can validate assets deterministically later.
- Store only metadata and rules. Do not bundle device mockup images, screenshots, store badges, or paid templates.
- If a platform says a rule is conditional, keep that nuance in `required_or_optional` and `notes`; do not simplify it into a universal requirement.
- Caption pattern rows must avoid store-risk claims such as ranking, price, awards, urgency, testimonials, and direct download/play CTAs.
- Caption examples are patterns, not final copy. They must be tied to visible real UI/gameplay before export.
