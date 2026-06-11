# Reference Image Analysis

Use this guide when the user provides UI reference images or points to an external image library. The skill bundles no images; you bring your own.

## Bring Your Own Library

This skill does not ship a reference-image library, and it never embeds images in the package. To use image references:

- Point the skill at a folder you own or are licensed to use, or paste/attach individual references in the conversation.
- For metadata search, keep an `image-library-manifest.csv` next to your image folder and query it with `scripts/search_reference_library.py --manifest path/to/image-library-manifest.csv` (or place the folder next to the skill and run the script with no arguments).
- Never copy copyrighted images into the skill package or a public repo. Keep third-party references analysis-only unless you confirm the license.

### Manifest CSV schema

`scripts/search_reference_library.py` ranks rows by these columns (header row required):

- `path` — relative path to the image inside your library.
- `category` — e.g. `external-references/app-ui`, `external-references/game-ui`, `asset-pack`, `low-value-non-ui`.
- `kind` — app, dashboard, mobile, web, game, hud, shop, inventory, menu, dialog, settings, component, etc.
- `suitability` — `analysis-only`, `license-confirmed`, `study-only`, etc.
- `note` — one line on what the image is useful for.
- `extension` — file extension (png, jpg, webp...).

Rows whose category is `analysis-artifact` or `low-value-non-ui` are hidden unless you pass `--show-internal`.

## Suitability Rules

- Treat app and game screenshots as analysis-only references. Extract layout, hierarchy, density, state, spacing, and color-role ideas; do not copy exact visuals.
- Treat brand, game, platform, logo, character, and store screenshots as copyrighted unless you can prove otherwise.
- Treat asset-pack files as a style/component asset library only after license confirmation.
- Do not use low-value line/logo/splash-only images to define UI rules.
- Prefer reference diversity: use at least one app reference, one game reference, and one component/state reference for broad UI guidance.

## Analysis Method

For each useful reference, capture:

- Surface: app screen, dashboard, mobile flow, title screen, menu, HUD, dialog, settings, shop, inventory, or asset component.
- Purpose: what user/player decision the screen supports.
- Layout: navigation, content regions, safe areas, fixed controls, and responsive concerns.
- Hierarchy: first attention target, primary action, secondary action, destructive action, and muted metadata.
- Color roles: background, surface, border, primary, accent, semantic colors, disabled color, and contrast risks.
- Component states: default, hover, active, focus, disabled, selected, loading, empty, error, and success.
- Asset style: icon stroke/fill, gloss, shadow, radius, outline, texture, and motion affordance.
- Transferable rule: one concise rule the skill can reuse without copying the source.

## ASO And Store Reference Folders

When a reference folder contains App Store / Google Play material, classify each image before learning from it:

- **ASO education slide:** useful for terminology, store surface anatomy, ranking factors, and experiment concepts. Do not treat it as a visual screenshot template.
- **Live store page or search result capture:** useful for seeing thumbnail scale, first-frame pressure, product page order, and how screenshots appear inside real store chrome. Do not copy the listed app's screenshots, logos, claims, or device composition.
- **Store screenshot set example:** useful for sequence, caption density, UI dominance, color-role choices, and first-three-frame clarity. Extract principles only and check it against `store-screenshot-aso.md` before reusing the pattern.
- **Feature graphic or promo banner:** useful for focal point, cutoff safety, and thumbnail clarity. Check Google Play format and no-alpha requirements before treating it as production guidance.

Run a thumbnail pass on ASO references. If the product value, UI/gameplay evidence, or caption cannot be understood in a small contact sheet, the reference is weak for store discovery even if it looks polished at full size.

Mark third-party store screenshots as `analysis-only` unless the user owns them or has confirmed a license. They should never be bundled into a skill package, copied into generated output, or used as visual source material beyond abstract design principles.

## Naming And Catalog

If you organize your own library, a clean convention keeps the manifest searchable:

- Lowercase ASCII, kebab-case words.
- Category-first folders.
- Descriptive file names with surface, product/domain, and sequence where useful.

Example: `external-references/game-ui/hud-and-overlays/game-hud-mobile-combat-01.png`

## Output Rule

When using a reference image, write the extracted design principle, not the image itself. If the source is not licensed for redistribution, keep it out of any generated assets and the repo, and mark the analysis `analysis-only`.
