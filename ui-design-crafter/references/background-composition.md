# Background Composition

Use this file when a UI needs background art, scene art, environmental imagery, product photography, or a themed backdrop for menus, shops, mission select, HUDs, onboarding, dashboards, or app screens.

## Core Rule

The background must prove the product, genre, world, or task without relying on the logo or title text. It is not filler. Pick concrete subject matter, compose around the UI, and preserve legibility with local value control instead of hiding the scene under a full dark overlay.

## Single-Panel Background Ban

Do not use a single oversized panel, fake dashboard card, centered chart block, boxed "scene preview," split left-side backdrop panel, or one simple rectangle as the background. This is a common AI-looking shortcut: it technically relates to the theme, but it has no real composition, depth, material, or environment.

Bad pattern:

- A huge rounded rectangle behind the UI.
- One simplified chart/table/board drawn in the background.
- A flat "screen inside the screen" that looks like a placeholder panel.
- A separate framed background preview sitting beside the real UI when the screen needs a full environment or quiet app surface.
- A two-part composition where the left side is a decorative background card and the right side is the real UI on a different surface.
- Theme-colored stripes or blocks that do not explain a place, product, or task.
- A background that repeats the foreground UI instead of giving it context.

Professional fix:

- For games, build a location or gameplay context: corridor, garage, track, shop counter, map table, inventory bench, arena, camp, room, field, or level space.
- For apps and dashboards, either keep the background as a clean neutral app surface or use layered product/workflow context: desk, command wall, subtle data wall, device frame, operations room, product photo crop, content canvas, or real task surface.
- Use foreground, midground, and background layers. Even simple CSS or generated imagery should have depth and a focal subject.
- If a panel-like object appears in the background, it must be part of a wider scene and visually quieter than the real UI. It cannot be the whole background idea.
- Prefer full-canvas or integrated background composition. Use a framed background panel only when it is literally a map, camera feed, content preview, artwork, level board, monitor, or inspectable object that belongs to the workflow.
- Keep the left and right sides on the same continuous background field. UI panels may sit on top of it, but the backdrop itself should not be split into unrelated blocks.

## Decision Order

1. Identify the screen purpose: main menu, mission select, shop, HUD, dashboard, form, editor, onboarding, or content view.
2. Select the closest theme row in `theme-style-guides.md` and use its background anchors as the subject pool.
3. Choose one primary focal subject and two or three supporting cues. Do not make a collage of every possible theme object.
4. Reserve UI safe zones before designing the image. Background composition serves the interface, not the other way around.
5. Define the value map: where text sits, where panels sit, where the focal subject sits, and where local scrims or gradients are allowed.
6. Validate with at least one mobile crop and one desktop crop when the implementation has both viewports.

## Composition Recipe

Document these choices before implementing or generating a background:

- Theme row:
- Screen purpose:
- Primary focal subject:
- Supporting environmental cues:
- Foreground, midground, background layers:
- Main UI safe zone:
- Focal point:
- Light source and mood:
- Material cues:
- Overlay plan:
- Crop plan for mobile, tablet, and desktop:

If any line is vague, the result will likely look generic.

## Screen Layout Rules

### Mobile 9:16

- Treat the lower 30-40% as the most likely action/control zone for menus, mission cards, shop actions, and bottom HUD.
- Put the primary focal subject in the upper or middle third, offset from dense text and CTA areas.
- Keep high-detail texture away from small labels, counters, and bottom action bars.
- Use a vertical value gradient only as a readability layer, not as the entire visual idea.
- Check 360x740, 390x844, and 430x932 crops when possible.

### Desktop 16:9

- Use horizontal depth: subject, environment, and UI zones should not all compete at center.
- Keep large menu panels on one side or lower third while the focal subject occupies the opposite third or background center.
- Avoid a single centered card over a centered subject unless the image is intentionally symmetrical and still readable.
- Add side fades or local scrims behind UI clusters rather than darkening the whole canvas.

### Tablet

- Avoid composition that only works as mobile or desktop. Tablet often exposes awkward empty corners and cropped focal subjects.
- Keep important subject matter inside a central 70% safe area unless the layout intentionally uses side panels.
- Test both portrait and landscape for apps or games likely to support rotation.

### Menu And Title Screens

- The background should establish the world within five seconds.
- Keep the title and primary action readable without putting them in a heavy card.
- Use environmental framing, light, and value contrast to guide the eye toward the CTA.
- Do not use abstract gradients, fog, or noise as the main identity signal.

### Mission Select And Level Select

- Use location, map, route, dossier, board, or objective evidence as the visual anchor.
- Cards should sit on calm local surfaces or scrims, not over high-detail art.
- Selected, locked, completed, and danger states must remain visible without using random gold or neon frames.

### Shop, Inventory, And Upgrade Screens

- Use shelves, workbenches, inventory tables, garage bays, armories, closets, product surfaces, or UI-native catalog surfaces.
- Product/item silhouettes should be inspectable. Avoid backgrounds so busy that item cards need heavy frames.
- Keep pricing, rarity, equipped, owned, and unavailable states readable over neutral surfaces.

### In-Game HUD

- Gameplay remains the visual subject. Background art belongs to the game world; HUD surfaces should float only as much as needed for readability.
- Keep persistent HUD away from the center of action unless the mechanic requires it.
- Test HUD over bright, dark, and busy areas of the game scene.

### SaaS, Finance, Health, And Productivity

- The interface, data, and workflow are usually the visual subject. Use subtle product context only if it improves comprehension.
- Avoid decorative scenery behind dense tables, forms, or charts.
- When imagery is used, keep it editorial, product-specific, or contextual, with quiet UI surfaces over it.

## Theme Background Matrix

Use these as composition anchors. If a theme is missing, blend the closest rows deliberately and write the blend down.

Theme rows below must match the canonical list in `theme-style-guides.md` (its Theme Execution Matrix). When adding or renaming a theme, update `theme-style-guides.md`, `component-theme-matrix.md`, and this file in the same change.

### Horror / Dark Survival

- Anchors: morgue drawers, cemetery silhouettes, hospital corridors, autopsy tables, abandoned chapels, wet tile, broken lights, evidence boards.
- Focal point: one readable threat clue or location clue, not generic darkness.
- Safe zones: place menus over matte shadow areas; keep key horror subject visible outside the main panel.
- Overlay: local grime, edge vignette, or panel-side scrim. Avoid full black fog that hides the place.

### Hyper Casual

- Anchors: simple play track, toy platform, collectibles, obstacles, goal line, soft studio or sky plane.
- Focal point: gameplay goal or object path.
- Safe zones: large bottom touch controls and top counters on clean flat value areas.
- Overlay: minimal; use clean solid surfaces for text.

### Fun / Party / Arcade

- Anchors: stage, arcade wall, prize shelf, mascot props, venue lights, audience silhouettes.
- Focal point: reward, stage, or play object.
- Safe zones: leave confetti and bright lights away from labels and CTA text.
- Overlay: small local scrims only behind text-heavy clusters.

### Casual Puzzle

- Anchors: board surface, tiles, booster tray, level path, candy/toy material, goal tray.
- Focal point: board or progress path.
- Safe zones: board first, HUD and reward panels second.
- Overlay: avoid haze over playable pieces; use solid UI trays.

### Fantasy RPG

- Anchors: parchment map, inventory table, camp, forest, castle, forge, spellbook, shrine, faction banners.
- Focal point: quest object, inventory surface, map region, or character context.
- Safe zones: ornate detail near edges; readable item/stat panels on quieter parchment/leather/stone surfaces.
- Overlay: material-native shadows and paper/leather panels, not universal gold frames.

### Sci-Fi Tactical

- Anchors: command room, hangar, cockpit, radar map, tactical grid, unit silhouettes, readable holographic displays.
- Focal point: map, unit, ship, or tactical objective.
- Safe zones: edge panels and command bars on low-noise areas.
- Overlay: restrained data glows for true system state; avoid animated noise behind text.

### Cozy / Lifestyle

- Anchors: room, cafe, garden, kitchen, desk, diary, soft daylight, seasonal objects.
- Focal point: task object or personal place.
- Safe zones: keep text over calm walls, table surfaces, shelves, or soft light zones.
- Overlay: gentle local wash; avoid beige-only low-contrast fog.

### Racing / Sports

- Anchors: track, garage, stadium, pit lane, asphalt, vehicle closeup, scoreboard, bracket.
- Focal point: vehicle/equipment, start line, timer context, or leaderboard moment.
- Safe zones: speed/timer/lap data on stable strips away from motion streaks.
- Overlay: directionally blurred background is acceptable away from text; do not blur labels.

### Strategy / War Room

- Anchors: map table, terrain board, unit markers, command tent, radar grid, territory layers, planning documents.
- Focal point: map objective, unit cluster, route, or command surface.
- Safe zones: edge panels can sit on map margins; keep the center map legible.
- Overlay: grid or paper texture may support meaning; avoid decorative chrome unrelated to faction.

### Historical / Period

- Anchors: archive desk, manuscript, period map, ledger, workshop, market street, ship deck, command table, museum case, signage, coinage, textile, tool, weapon, vehicle, or architecture from the chosen era and region.
- Focal point: one historically specific object or place that explains the screen's purpose: dossier, route map, relic, contract, instrument panel, artifact shelf, tavern board, medical table, radio desk, or storefront.
- Safe zones: place UI over calm paper, wall, table, cloth, stone, or shadow fields; keep intricate ornament away from small text and touch controls.
- Overlay: local paper/ink wash, glass case reflection, lamplight, projector falloff, or table shadow. Avoid universal sepia fog and full-screen grime that erases the period evidence.
- Accuracy note: name the era/region assumption in the composition recipe if the user did not provide it.

### Kids / Education

- Anchors: classroom, playground, workbook, toy blocks, friendly lab, simple learning world, character context.
- Focal point: learning object or friendly task area.
- Safe zones: large text and controls on calm bright surfaces.
- Overlay: use simple solid cards or soft shapes; avoid visual punishment or scary error atmospheres.

### Premium / Luxury

- Anchors: product closeup, gallery, venue detail, refined material, editorial photography.
- Focal point: the actual product, object, place, or service quality signal.
- Safe zones: generous negative space around CTAs and product details.
- Overlay: subtle local dark/light wash; metallic accents only when contrast survives.

### Productive SaaS / Admin

- Anchors: interface data, workflow state, table, chart, command surface. Background imagery is usually unnecessary.
- Focal point: current work object or data priority.
- Safe zones: dense UI needs clean surfaces, not scenic art.
- Overlay: none or very subtle; avoid decorative hero backgrounds inside work tools.

### Finance / Analytics

- Anchors: charts, account context, product/account surfaces, controlled data regions.
- Focal point: metric, trend, portfolio, or decision area.
- Safe zones: text and numbers on stable surfaces with explicit contrast.
- Overlay: avoid atmospheric market imagery behind charts; keep units and time ranges readable.

### Consumer Mobile

- Anchors: user context, product use, service object, clean content surface, brand material.
- Focal point: user task or product value.
- Safe zones: bottom navigation and primary action must sit on stable surfaces.
- Overlay: use native app surfaces and sheets; avoid wallpaper competing with core actions.

## Overlay And Readability Rules

- Use overlays to protect legibility, not to replace art direction.
- Prefer local scrims behind text, panel clusters, or nav bars.
- Whole-screen dark overlays should be light enough that the place, object, or product remains identifiable.
- Avoid blur as a default. Blur can make art feel like disposable stock and can reduce theme evidence.
- Text should sit on a predictable value field. If the background has high local contrast, add a surface or move the text.
- Test actual contrast against the final rendered background, not only against token colors.

## Asset And Reference Rules

- User-provided references may guide composition, mood, material, crop, and UI integration. Do not copy copyrighted images into the skill.
- External images need licensing review before bundling or shipping. Use them for analysis unless rights are clear.
- Generated images should still follow the same composition recipe; generation does not excuse generic scenery.
- If no image asset exists, build a lightweight scene with CSS, SVG, canvas, or gradients only when it still contains recognizable subject matter.

## Failure Patterns

- Generic dark gradient with title text.
- Background so dark that the theme cannot be identified.
- Fog/noise/blobs used as the only mood.
- Important subject cropped out on mobile.
- UI text placed over the busiest part of the image.
- One hero image reused for menu, shop, mission select, and HUD without adapting composition.
- The background and UI chrome express different genres.

## Completion Check

Before calling a UI complete, inspect a screenshot and answer:

- Can the theme or product be identified without reading the title?
- Is there one clear focal subject?
- Are UI safe zones calm enough for real text?
- Does the background survive mobile and desktop crops?
- Are overlays local and meaningful?
- Does the background support the selected theme row in `theme-style-guides.md`?

## Sources

- See `references/source-bibliography.md` for the standards and research behind these rules.
