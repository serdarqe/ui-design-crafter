---
name: ui-design-crafter
description: Use when designing, implementing, reviewing, or polishing app/game UI systems, including dashboards, mobile screens, HUDs, menus, panels, component states, visual QA, accessibility, themed backgrounds, App Store / Google Play screenshots, feature graphics, and ASO listing assets.
---

# UI Design Crafter

## Overview

Use this skill to turn a UI request into a coherent, production-ready interface. Favor usable screens and complete interaction states over decorative mockups. When the request targets App Store, Google Play, ASO, feature graphics, or store listing visuals, treat store assets as a second-stage deliverable built from real app/game screens.

## Core Workflow

1. Identify the surface: app, dashboard, website, mobile UI, in-game HUD, menu, inventory, shop, editor, or tool panel.
2. Infer the user's goal, audience, platform, input method, and visual tone from the request and codebase. Ask only when missing information would change the design direction.
3. Inspect existing components, tokens, layout conventions, assets, and framework patterns before creating new UI, and check `design-system/MASTER.md` and `design-system/pages/` first inside a project. If a reusable or multi-screen direction is being set and none exists, create one via `references/design-system-persistence.md` and `assets/templates/`.
4. If the request names a theme, genre, mood, or audience, set direction from the Theme Execution Matrix in `references/theme-style-guides.md` first (the single source for themes). Use `references/background-composition.md` for scene/background art and `references/component-theme-matrix.md` for themed components. Then define the UI system: grid, spacing scale, type scale, color roles, background, panel material, icon style, elevation, radius, motion, and density.
5. Design the full workflow, not just the first screen: default, hover, active, focus, disabled, loading, empty, error, success, selected, and pressed states.
6. Implement with existing design primitives where possible. Use familiar controls: icon buttons for tools, segmented controls for modes, toggles for binary settings, sliders or steppers for numeric values, menus for option sets, tabs for views, and clear command buttons for irreversible actions.
7. Validate visually across desktop and mobile sizes. Use `references/visual-test-workflow.md` for screenshot/metrics evidence and run `scripts/visual_smoke_check.py` when screenshots or browser metrics are available. Check text fit, overlap, contrast, touch target size, keyboard/focus behavior, asset rendering, and whether the UI still works with real content.
8. If the user asks for App Store, Google Play, ASO, feature graphics, or store screenshots, run the Store Screenshot Pipeline below after the product UI itself is designed and visually checked.

## Store Screenshot Pipeline

Use this only for store/listing assets. Do not replace real UI work with promotional mockups.

1. Confirm platform, product type, device group, orientation, locale, and whether the user needs raw screenshots, composed store assets, or both.
2. Design or verify the real app/game screens first, then run normal UI QA.
3. Read `references/store-screenshot-aso.md` for platform rules and ASO sequence strategy.
4. Read `references/store-capture-workflow.md` when screenshots must be captured from a web prototype, Android emulator/device, game build, desktop app, or user-provided images.
5. Choose a platform-specific first-frame strategy. For Google Play, plan thumbnail clarity, feature graphic cutoff safety, alt text, and preview-video first seconds. For App Store, plan the search-visible first 1-3 screenshots, App Preview first seconds if used, and Product Page Optimization/custom product page needs.
6. Use `scripts/search_design_tokens.py --kind store-preset` and `--kind store-caption` when choosing dimensions or caption patterns.
7. Capture or organize raw screenshots and create/consume `manifest.raw.json` when there is more than one source screen.
8. Run `scripts/export_store_screenshots.py` to produce HTML compositions, optional PNGs, `manifest.store.json`, captions, and Google Play alt text metadata when applicable.
9. Run `scripts/check_store_assets.py` on the final folder or `manifest.store.json`; fix every `fail` before calling the store package ready. For App Store final QA, pass a preset or exact `--width/--height` because presetless App Store checks cannot prove upload-valid dimensions and now blocks PASS. Use `--require-alt-text` for Google Play handoff-ready packages.
10. When the request is ASO optimization, validate listing metadata too: App Store `--title`, `--subtitle`, `--keywords`, optional `--promotional-text`, and `--full`; Google Play `--title`, `--short`, and `--full`. Check character limits, duplicate App Store keywords, title/subtitle keyword repetition, competitor-brand risk, risky claims, and locale-specific variants.
11. If the request is ASO optimization, record one experiment hypothesis, one main changed variable, the target platform/test surface, and the conversion/downstream metrics to watch.

## Design Rules

- Build the actual usable experience first. Do not create a marketing landing page unless the user asks for one; when they do, follow the landing-page structure in `references/app-ui-patterns.md`.
- Match density to domain. App, tool, and dashboard UI should be quiet, scannable, and low-chrome. Game UI can be expressive and themed, but the HUD must stay glanceable and menus still need one dominant action.
- For mobile games, reserve device safe areas, ad slots, consent/store surfaces, and thumb zones before placing HUD, boards, hotbars, mission cards, or action bars. Banners, rewarded-ad CTAs, interstitial breaks, and monetization prompts are layout constraints, not late overlays.
- Keep the playable board, camera, or playfield dominant. HUD, ads, shop prompts, mission cards, and bottom action bars must not cover playable cells, drag paths, target zones, timers, health, cooldowns, or critical feedback.
- Design with intent. Every border, glow, gradient, shadow, and box must communicate structure, state, or meaning. If hierarchy only works because of chrome, fix the layout and type first. See `references/anti-patterns.md` to avoid the generated-kit look.
- Design for translation and motion sensitivity from the start: leave room for text expansion, use logical properties so layouts mirror in right-to-left languages, and give every animation a `prefers-reduced-motion` path. See `references/internationalization.md` and `references/motion-and-feedback.md`.
- Write and label for people: verb-first buttons, helpful (not blaming) errors, real content instead of placeholder filler, and an accessible name for every control, icon, and image. See `references/ux-writing.md` and `references/accessibility.md`.
- Keep the highest-quality design first; treat performance as a constraint you meet through cheaper equivalent techniques (animate transform/opacity, bake/atlas effects, recycle, throttle non-critical updates), never by lowering visual or interaction quality. Performance flags are suggestions; if a budget truly forces a visible quality cut, raise it as a decision rather than degrading silently. See `references/performance.md`.
- Choose color from the user's product, brand, genre, audience, content, and existing design before inventing a palette. Do not default to dark purple/blue, neon cyan, or generic dark-mode unless the request or context supports it.
- When redesigning from a screenshot or reference, do not preserve its palette by default. First decide whether the source colors are product/brand intent or an AI/template habit; if there is no clear reason to keep dark/neon/purple-blue styling, produce a more natural domain-fit palette such as light, warm neutral, editorial, platform-native, or brand-led.
- Avoid one-note palettes. Use clear semantic roles for primary, secondary, surface, border, accent, success, warning, danger, and muted content.
- Keep borders and selection frames theme-native. Do not default to gold/yellow, neon, or high-saturation outline frames unless the product, genre, rarity system, warning state, or brand explicitly calls for them. For dark horror, tactical, medical, industrial, or serious UI, prefer muted surface shifts, a single edge accent, dividers, or semantic state color over bright full-card frames.
- Keep cards for repeated items, modals, and genuinely framed tools. Do not put cards inside cards.
- Keep cards at 8px radius or less unless the existing design system uses another value.
- Avoid frame stacking: do not give a container, every child button/card, hover state, selected state, and focus state all their own visible border, glow, inset highlight, and heavy shadow. Choose one structural frame per cluster, then use fill, spacing, dividers, or state color for inner controls.
- Use stable dimensions for fixed-format UI such as boards, grids, toolbars, counters, tiles, HUD meters, and icon buttons.
- Do not scale font size with viewport width. Use responsive layout constraints instead.
- Keep letter spacing at 0 unless matching an existing design system.
- Do not use visible instructional text to explain obvious features, visual styling, keyboard shortcuts, or how to use common controls.
- Prefer icons from the app's icon library. If lucide is available, use lucide icons for buttons and tool actions.
- Give unfamiliar icon-only controls tooltips and accessible names.
- Verify that text never overlaps, clips awkwardly, or spills out of buttons, panels, cards, or HUD elements.
- Use real, generated, or project-provided visual assets when the request is for a website, app, or game experience that benefits from imagery.
- Treat backgrounds as part of the product or game world, not filler: concrete theme-native environments, objects, and lighting, never generic gradients, fog, blobs, or stock-like scenery. Do not fake a background with a single oversized panel, a boxed "scene preview," a split left-side backdrop, or a simplified copy of the UI behind the real UI; keep one continuous background field behind all regions and use overlays only to protect legibility. A framed background panel is only for a literal map, camera feed, preview, artwork, or inspectable object. See `references/background-composition.md`.

## Reference Selection

Load only the references the current task needs, not all of them; each file is self-contained. Match the task to the entries below.

- Read `references/ui-research-foundations.md` for evidence-based UI principles, cognitive load, Gestalt, Fitts's Law, Hick's Law, affordance, error prevention, accessibility, and mental models.
- Read `references/source-bibliography.md` when decisions need academic, standards-based, or industry source grounding.
- Read `references/color-theory-for-ui.md` for palette roles, semantic colors, contrast, dark mode, colorblind-safe states, and UI component color decisions.
- Read `references/theme-style-guides.md` when choosing the product/game theme, tone, visual language, background/scene art, panel/chrome style, density, and motion style. Use its Theme Execution Matrix as the single source for themes such as horror, hyper casual, fun/party, cozy, fantasy, sci-fi, racing, sports, strategy, historical/period, kids, luxury, SaaS, finance, and consumer mobile.
- Read `references/background-composition.md` when designing, generating, selecting, or reviewing backgrounds, scene art, hero imagery, menu backdrops, shop/inventory environments, mission maps, HUD backdrops, or product-context imagery.
- Read `references/app-ui-patterns.md` for app screens, dashboards, forms, mobile UI, websites, SaaS tools, and productivity interfaces - including mobile gestures, platform conventions (iOS vs Android, system back), keyboard handling, dynamic type, landing/marketing page structure, and web performance (Core Web Vitals).
- Read `references/game-ui-patterns.md` for HUDs, game menus, inventories, shops, character panels, level select, pause screens, and touch/controller game UI.
- Read `references/component-specs.md` when designing or implementing reusable controls such as panels, buttons, tabs, toggles, sliders, toolbars, dialogs, tooltips, and status elements.
- Read `references/component-state-matrix.md` before component library work, design handoff, or state-completeness reviews.
- Read `references/component-theme-matrix.md` when a themed UI includes panels, buttons, tabs, cards, modals, shop items, mission cards, bottom action bars, inventory slots, HUD meters, toasts, selected states, locked states, or controller/touch states.
- Read `references/internationalization.md` when UI ships in more than one language, in right-to-left scripts, or to a global audience (text expansion, RTL/logical properties, locale formatting, fonts).
- Read `references/motion-and-feedback.md` when adding transitions, animation, micro-interactions, or multi-sensory (visual/haptic/audio) feedback, and for reduced-motion behavior.
- Read `references/ux-writing.md` when writing buttons, labels, errors, empty states, onboarding, tooltips, toasts, or any user-facing or in-game text.
- Read `references/accessibility.md` for semantics, accessible names, keyboard, focus management, screen-reader behavior, and cognitive accessibility (contrast, target size, RTL, and motion are covered in their own references).
- Read `references/performance.md` when UI may affect frame rate, responsiveness, load time, or battery in a game, app, or website. It keeps quality first: meet a budget with cheaper equivalent techniques, never by stripping polish.
- Read `references/design-system-persistence.md` when working inside a project that may receive repeated UI work, when adding multiple related screens, or when existing design decisions must survive future agent runs. Use `assets/templates/design-system-master.md` and `assets/templates/page-override.md` when creating project-local design-system docs.
- Read `references/reference-analysis.md` when collecting or evaluating moodboards, competitor examples, app UI references, or game UI references.
- Read `references/reference-image-analysis.md` when the user provides or points to a UI reference image library.
- Read `references/anti-patterns.md` to avoid generated-kit habits (frame stacking, glow-on-everything, gradient soup, one-note palette) and reduce the AI-generated UI look, with the fix for each.
- Read `references/design-data-guidelines.md` before adding or relying on searchable font, color, icon, or style-domain data.
- Read `references/visual-qa-checklist.md` before claiming a UI is complete or when reviewing visual quality.
- Read `references/visual-test-workflow.md` before finalizing implemented UI, browser prototypes, mobile screens, game menus, HUDs, shops, mission screens, dashboards, or any work where screenshot evidence is possible.
- Read `references/store-capture-workflow.md` when raw screenshots must be captured or organized from a web prototype, Android emulator/device, iOS/user-provided screenshots, game build, or desktop app before App Store / Google Play composition.
- Read `references/store-screenshot-aso.md` when designing, capturing, composing, or reviewing App Store / Google Play screenshots, feature graphics, app previews, ASO presentation assets, or store listing visuals.
- Read `references/example-prompts.md` when the user asks how to invoke, test, or pressure-test this skill.
- Run `scripts/search_reference_library.py` to search your own external reference-image library by metadata (bring your own folder plus a manifest CSV; the skill bundles no images). Optional; see `references/reference-image-analysis.md` for the manifest schema.
- Run `scripts/search_design_tokens.py` for curated, contrast-checked starter color palettes, type pairings, icon meanings, style-domain guidance, motion presets, store screenshot presets, and ASO caption patterns by domain (e.g. "fintech dark dashboard"; `--kind motion`, `--kind store-preset`, or `--kind store-caption` for focused search). Treat results in `data/` as starting points to adapt, not a fixed kit. Add `--design-system` for one consolidated palette + type + style + icon + motion recommendation with contrast verdicts, `--mode light|dark` to force the palette mode, and `--out design-system/MASTER.md` to seed the project design-system file from `assets/templates/`.
- Run `scripts/export_store_screenshots.py` after raw screenshots exist to compose App Store / Google Play HTML store assets and `manifest.store.json`; use `--render playwright` when Node Playwright is installed and full CSS PNG output is required. Use `--render pillow` for browserless PNG output only with `--style no-caption/raw-compliant` and simple contain/cover fitting.
- To enable PNG output in a target workspace, install Node Playwright there with `npm install -D playwright` and `npx playwright install chromium`; the skill package must not bundle `node_modules` or browser binaries.
- Run `scripts/check_store_assets.py` before final store delivery to validate PNG/JPG format, exact preset dimensions, Google Play min/max/aspect rules, alpha/transparency, file size, missing screenshot count, portrait/landscape mismatch, caption overflow, risky ASO claims, localization expansion risk, Google Play alt text, and listing metadata limits/keyword discipline. Use `--json` for CI or handoff reports.
- Run `scripts/export_tokens.py <palette>` to export a chosen palette to developer color tokens (CSS variables, Tailwind theme, or W3C DTCG `tokens.json`) - the design-to-code handoff. Use `--list` to see palette names.
- Run `scripts/check_ui_tokens.py` when reviewing code for obvious UI token, font, focus, palette, frame-stacking, contrast, RTL, reduced-motion, tap-target, missing alt text, or missing accessible-name risks. It also surfaces performance suggestions (layout-animated properties, heavy live effects) as INFO - hints to use a cheaper equivalent, never to cut quality. Use `--contrast FG BG` for a quick WCAG ratio check.
- Run `scripts/visual_smoke_check.py` on screenshot folders and browser metrics JSON to catch missing viewport evidence, horizontal overflow, clipped text, hidden primary CTA, frame/card stacking candidates, blank screenshots, and over-dark backgrounds.

## Output Expectations

When designing only, provide concise specs that include layout, components, states, color roles, typography, spacing, and responsive behavior.

When implementing, edit the project files directly, start the local dev server when needed, and verify the result with screenshots or browser inspection when available.

When reviewing, lead with concrete UI defects, accessibility risks, responsiveness problems, inconsistent component usage, and missing states.

When delivering store assets, include the platform/device preset, screenshot order, source screens, captions, Google Play alt text when applicable, output folder or manifest path, and the result of `check_store_assets.py`. Be explicit if PNG rendering could not run because Playwright or the target runtime is unavailable.

When delivering ASO optimization work, include the hypothesis, changed variable, target audience or store surface, platform-specific variants, and the measurement plan. Do not present untested creative preference as a proven conversion win.
