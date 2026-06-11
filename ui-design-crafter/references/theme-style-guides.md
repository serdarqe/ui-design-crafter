# Theme Style Guides

Use this file when choosing a visual direction for app UI, game UI, dashboards, panels, HUDs, buttons, menus, or themed component systems.

## Selection rule

Choose the theme from the product goal and audience, not from decoration alone. A good theme defines density, information priority, color roles, component shape, icon style, motion, and error/success language.

After choosing the theme row, use `component-theme-matrix.md` for panel, button, tab, card, modal, shop, mission, inventory, action bar, HUD meter, toast, selected, disabled, and locked state decisions.

## Background And Scene Art

- Use backgrounds to communicate place, genre, mood, and product identity. A good background has recognizable subject matter, not just atmosphere.
- Choose concrete visual anchors from the request: location, object, gameplay state, brand material, character context, or user-provided references.
- Keep UI legible with composition, value control, and localized overlays. Do not darken or blur the whole scene until the image becomes meaningless.
- Avoid generic gradients, fog, abstract blobs, texture-only darkness, or stock-like scenery that could belong to any product.
- For focal point, safe zone, crop, and overlay decisions, use `background-composition.md` after selecting the theme row.

## Theme Execution Matrix

Use this matrix before picking background, palette, panel material, button style, HUD density, or motion. If the user names a theme that is not listed exactly, pick the closest row or blend two rows deliberately. Do not default to dark purple/blue, gold frames, neon outlines, or generic gradients unless the chosen row supports them.

Maintain this matrix as the single source of truth for theme behavior. When adding or changing a theme, update the matching row here instead of creating another duplicate theme section later in the file.

Canonical theme rows (keep `component-theme-matrix.md` and `background-composition.md` aligned to this exact list): Horror / Dark Survival, Hyper Casual, Fun / Party / Arcade, Casual Puzzle, Fantasy RPG, Sci-Fi Tactical, Cozy / Lifestyle, Racing / Sports, Strategy / War Room, Historical / Period, Kids / Education, Premium / Luxury, Productive SaaS / Admin, Finance / Analytics, Consumer Mobile. When adding, renaming, or removing a theme, update all three files in the same change so the theme list never drifts.

### Horror / Dark Survival
- Background anchors: morgue drawers, cemetery silhouettes, hospital corridors, autopsy tables, abandoned chapels, wet tile, broken medical lights, ritual traces, evidence boards.
- Palette: near-black, bone/ivory text, rust, dried blood, sickly green, worn metal; red only for danger, damage, infection, or alarms.
- Panels/buttons/HUD: sparse matte surfaces, low chrome, single edge accent for selected state, readable inventory and objective notes.
- Motion: slow tension, brief danger pulses, no unpredictable essential UI.
- Avoid: generic black fog, red-on-black low contrast, gold fantasy frames, glow on every card, illegible grunge controls.

### Hyper Casual
- Background anchors: clear gameplay track, simple toy-like platform, soft sky/studio plane, oversized collectible objects, readable obstacles, visible goal line.
- Palette: bright varied colors with clean neutrals; use saturated accents, but keep text on solid high-contrast surfaces.
- Panels/buttons/HUD: very large tap targets, chunky buttons, minimal HUD, stable counters, few choices per screen.
- Motion: snappy, elastic, reward-heavy, short loops; feedback should be readable in one glance.
- Avoid: dark mode defaults, complex textures, tiny labels, dense menus, decorative panels that hide the playfield.

### Fun / Party / Arcade
- Background anchors: stage lights, party venue, confetti, arcade cabinet context, mascot props, audience silhouettes, prize wall.
- Palette: energetic multi-color accents balanced by neutral surfaces; avoid making every element the same saturated hue.
- Panels/buttons/HUD: bold cards, badge shapes, capsule buttons, high-energy primary action, readable score/reward areas.
- Motion: bouncy transitions, celebratory bursts, score pop, but keep controls stable.
- Avoid: corporate dashboard layout, all-neon glow, random confetti behind text, every button competing as primary.

### Casual Puzzle
- Background anchors: board surface, tiles, goal tray, boosters, progress map, tactile toy/candy material, level path.
- Palette: bright and friendly; semantic danger/moves/warnings must remain clear.
- Panels/buttons/HUD: board first, goal tray second, booster bar stable, shop/reward surfaces lower priority.
- Motion: satisfying tile, combo, reward, and level-complete feedback.
- Avoid: HUD covering the board, sale panels over gameplay, tiny booster counts, effects hiding targets.

### Fantasy RPG
- Background anchors: parchment maps, inventory table, forest/castle/camp, forge, spellbook, shrine, faction banners.
- Palette: parchment, worn metal, leather, gem/rarity colors, faction colors; semantic states remain stable.
- Panels/buttons/HUD: crafted materials, inventory grids, rarity cues with labels, stat compare panels, readable quest logs.
- Motion: material response, reveal, enchantment, rarity highlight used sparingly.
- Avoid: ornate frames that shrink content, gold everywhere, decorative icons without labels, all slots glowing.

### Sci-Fi Tactical
- Background anchors: command room, hangar, cockpit, radar map, tactical grid, unit silhouettes, holographic but readable displays.
- Palette: dark/neutral technical base with restrained cyan, green, amber, or orange for real system states.
- Panels/buttons/HUD: compact edge panels, command grids, objective tracker, alert stack, minimap/radar, clear cooldowns.
- Motion: scan/lock-on/data transitions only where meaningful.
- Avoid: all-neon palette, animated noise behind text, tiny monospaced body text, equal-priority alerts everywhere.

### Cozy / Lifestyle
- Background anchors: room, cafe, garden, kitchen, desk, diary, soft daylight, personal objects, seasonal scenes.
- Palette: varied muted colors with real contrast; warm neutrals supported by greens, blues, rose, or clay, not beige-only.
- Panels/buttons/HUD: gentle cards, soft hierarchy, friendly controls, clear progress and collection states.
- Motion: calm transitions, small completion feedback, no pressure.
- Avoid: washed-out low contrast, slow interactions, beige-only palette, decorative clutter hiding tasks.

### Racing / Sports
- Background anchors: track, garage, stadium, pit lane, asphalt, speed lines, vehicle/equipment closeups, scoreboard or bracket context.
- Palette: team/vehicle colors, asphalt neutrals, rubber, metal, signal colors; reserve red/yellow for warnings and race status.
- Panels/buttons/HUD: speed/timer/lap data first, compact stat strips, clear start/race action, stable HUD meters.
- Motion: fast directional transitions, speed streaks away from text, celebration on finish.
- Avoid: random neon unless the race world supports it, unreadable motion blur behind labels, tiny timer text.

### Strategy / War Room
- Background anchors: map table, terrain board, unit markers, command tent, radar grid, planning documents, territory layers.
- Palette: muted tactical neutrals, map greens/browns/grays, restrained faction colors, clear warning and objective colors.
- Panels/buttons/HUD: dense but organized edge panels, filters, unit cards, objective tracker, command bar, tooltips.
- Motion: purposeful selection, range preview, route/path reveal, alert transitions.
- Avoid: decorative fantasy/sci-fi chrome unrelated to faction, hiding map under panels, too many equal alerts.

### Historical / Period
- First decision: define era, region, class/context, and source type before styling. Ottoman court archive, Victorian medical ledger, ancient Roman forum, medieval monastery, WWII operations room, and 1980s arcade should not share one "old" UI kit.
- Background anchors: manuscript desk, archive drawer, period map, workshop, market street, ship deck, command room, museum case, signage, coinage, textile, tool, weapon, vehicle, or architectural detail from the chosen era.
- Palette: sample from real materials and pigments: paper, ink, stone, wood, enamel, brass, iron, textile dye, ceramic, print, photograph, or military paint. Avoid universal sepia/brown/gold.
- Panels/buttons/HUD: modern usability with period-native material cues. Use period texture, labels, dividers, seals, tabs, stamps, ledger rules, carved edges, or hardware only when they support hierarchy and remain readable.
- Typography: period-inspired display type only for short titles or labels; body text stays readable. Do not use old-English, calligraphy, or distressed fonts for dense UI.
- Motion: physical page, drawer, stamp, mechanical, lantern, slide, projector, or instrument feedback when it fits; avoid magical glow unless the period world includes it.
- Avoid: generic parchment everywhere, gold frames as authenticity, fake museum clutter, anachronistic icons, illegible ornamental type, and copying protected historical images instead of extracting principles.

### Kids / Education
- Background anchors: classroom, playground, workbook, friendly lab, toy blocks, simple learning world, character context.
- Palette: bright but controlled; semantic success/warning/error colors stay consistent and accessible.
- Panels/buttons/HUD: large controls, few choices, visible progress, forgiving error states, reassuring feedback.
- Motion: positive reinforcement, short and predictable.
- Avoid: dense text, punishment-heavy error language, subtle disabled states, hidden navigation.

### Premium / Luxury
- Background anchors: product closeup, venue/material detail, gallery, editorial photography, refined object context.
- Palette: restrained neutrals with one accent; metallic tones only if contrast is preserved.
- Panels/buttons/HUD: minimal chrome, careful alignment, generous spacing, high-quality imagery as first signal.
- Motion: smooth, low amplitude, deliberate.
- Avoid: fake luxury through gold everywhere, fragile contrast, slow hidden interactions, overdecorated cards.

### Productive SaaS / Admin
- Background anchors: usually none or very subtle product context. The interface surface, data, table, and workflow are the visual subject.
- Palette: neutral surfaces with restrained accent for navigation, active states, and primary actions.
- Panels/buttons/HUD: quiet low-chrome grouping, tables, filters, detail panels, command bars, status chips.
- Motion: minimal continuity and state change.
- Avoid: marketing hero composition, decorative backgrounds, oversized cards, gradient panels behind work data.

### Finance / Analytics
- Background anchors: charts, account/product context, controlled data surfaces; avoid atmospheric scenery.
- Palette: trustworthy neutrals, restrained accent, clear non-color cues for gain/loss/risk.
- Panels/buttons/HUD: metric strips, charts, filters, comparison tables, alert rows, explicit units and time ranges.
- Motion: subtle updates, no distracting motion near live values.
- Avoid: saturated chart backgrounds, red/green-only status, hidden units, vague time ranges.

### Consumer Mobile
- Background anchors: product/user context where helpful, otherwise clean surfaces that keep the primary action clear.
- Palette: branded primary with generous neutral/white or dark surfaces depending on brand and environment.
- Panels/buttons/HUD: bottom navigation, cards, sheets, snackbars, one primary action per screen.
- Motion: short feedback and transitions, reduced-motion aware.
- Avoid: crowded forms, tiny tap targets, hidden destructive actions, color-only feedback.

## Sources

- See `references/source-bibliography.md` for the standards and research behind these rules.
