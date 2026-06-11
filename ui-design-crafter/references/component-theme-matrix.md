# Component Theme Matrix

Use this file when a UI has a named theme, genre, mood, audience, game world, or product tone and includes reusable components such as panels, buttons, tabs, cards, modals, shop items, mission cards, bottom action bars, inventory slots, HUD meters, or toasts.

## Core Rule

Theme changes component material, proportion, density, state treatment, and feedback. It is not only a palette swap. A horror button, hyper casual button, finance button, and fantasy inventory slot should not look like the same kit with different colors.

## Use Order

1. Select the closest theme row in `theme-style-guides.md`.
2. Use `component-specs.md` for anatomy, sizing, target size, and baseline component behavior.
3. Use `component-state-matrix.md` for required states and accessibility.
4. Use this file to translate the component into theme-native material, shape, density, and state language.
5. Check `anti-patterns.md` and `visual-qa-checklist.md` before calling the UI complete.

## State Translation Model

Every interactive component should define these states in theme-native language:

- Default: quiet, readable, lower than selected/focus/error.
- Hover: slight fill, elevation, material shift, underline, or preview cue. Do not add a permanent border if the component already sits in a framed cluster.
- Active/pressed: tactile depression, fill darken/lighten, brief scale, or physical response that matches the theme.
- Focus-visible: accessible ring or outline with at least 3:1 non-text contrast. It can be theme-colored, but must remain visible.
- Disabled: muted content plus reason where useful. Do not hide the control completely.
- Selected/current: strongest non-critical state. It must be clearer than hover but quieter than danger/error.
- Locked/unavailable: lock mark, label, requirement, dimmed art, or blocked affordance. Do not rely on gray alone.
- Loading/pending: stable dimensions, spinner/progress/skeleton, no layout shift.
- Error/danger: semantic danger treatment plus icon/text/shape. Do not reuse the same red as decorative mood color.

## Component Rules

### Panel

- Defines a group, state, or workflow region. It is not decoration.
- One structural frame per cluster is enough. Use either panel frame, child dividers, or item surfaces.
- The panel material should match the theme: matte, paper, toy plastic, tactical glass, leather, metal, clean neutral, or product photography surface.

### Button

- One primary action per region gets the strongest fill.
- Secondary actions use lower emphasis: text, subtle fill, outline, underline, or icon-only controls.
- Default buttons should not all have visible borders, glows, and shadows. Save strong outlines for focus, selected, error, rarity, or warning.

### Tabs And Segmented Controls

- Tabs should show current context without looking like many competing CTAs.
- Use indicator, text weight, fill, or segmented selection. Avoid boxed borders on every tab plus an active ring plus underline.
- For game UI, controller focus and selected/current must be distinct.

### Cards, Mission Cards, And Shop Items

- Cards carry repeated choices. They need title, state, primary metadata, and one clear action.
- Mission cards should show availability, threat/difficulty, reward, completion, locked reason, and selected/current state.
- Shop cards should show price, owned/equipped, affordable/unaffordable, selected preview, purchase-pending, success, and error.
- Keep card dimensions stable across states.

### Inventory Slots

- Slots need empty, occupied, hover, focus, selected, equipped, locked, invalid drop, rarity/quality, and stack count states.
- Rarity and equipped state should not resize the slot.
- Use color plus label, mark, icon, or weight. Color alone is not enough.

### Bottom Action Bar / Hotbar

- Treat the bar as one tray/device or as separate floating controls, not both at the same visual strength.
- Inner slots can use recesses, fills, dividers, or pressed states. Avoid full framed cards inside a fully framed tray.
- Cooldown overlays and counts must not move or resize slots.

### HUD Meter

- A HUD meter is a readout first. Value, threshold, and state change must be glanceable.
- Use tabular numbers or fixed-width slots for changing values.
- Low/critical state needs color plus shape, label, flash, tick, icon, or position.

### Modal And Toast

- Modals interrupt; toasts inform. Do not put required decisions only in a toast.
- Modal frame and backdrop should match the theme but keep action hierarchy clear.
- Toasts should use semantic icon/color/label and avoid covering core gameplay or primary app controls.

## Theme Matrix

Theme rows below must match the canonical list in `theme-style-guides.md` (its Theme Execution Matrix). When adding or renaming a theme, update `theme-style-guides.md`, this file, and `background-composition.md` in the same change.

### Horror / Dark Survival

- Panels: matte dark surfaces, worn edges, low chrome, small dividers, bone text, rust or sickly accent only where meaningful.
- Buttons: restrained solid primary for one action; secondary text/subtle fill; pressed state feels heavy and physical.
- Tabs/cards: quiet list/table cards, low radius, selected as a single edge accent or surface shift. No gold/yellow full-card frame.
- Mission/shop/inventory: dossier notes, evidence tags, locker/inventory trays, locked reasons as missing key, contamination, danger, or inaccessible area.
- Bottom action bar/HUD: sparse tray, fixed slots, muted icons, critical red only for danger/damage/alarm.
- Modal/toast: stark title, clear consequence, low-motion danger pulse only for urgent state.
- State language: selected equals edge accent plus fill; locked equals obstruction/label; focus remains visible but not neon.

### Hyper Casual

- Panels: minimal bright surfaces, large padding, simple rounded cards, playful but clean.
- Buttons: chunky large tap targets, strong fill, short labels, brief scale on press, elastic feedback.
- Tabs/cards: pill or segmented selection, high clarity, oversized labels, few choices per view.
- Mission/shop/inventory: reward-first cards, large item art, simple price, locked state as friendly requirement/progress.
- Bottom action bar/HUD: very large icons/counters, stable top or bottom trays, minimal decoration.
- Modal/toast: reward panels, level-complete cards, short celebratory feedback.
- State language: selected can use fill, scale, check mark, or progress glow; avoid dark tactical surfaces and tiny text.

### Fun / Party / Arcade

- Panels: bold but readable surfaces, badge shapes, stage/prize context, strong hierarchy.
- Buttons: lively fills, capsule or badge-like shapes, one main CTA, bouncy but stable press feedback.
- Tabs/cards: active tabs can use spotlight/fill/indicator; inactive tabs stay calm.
- Mission/shop/inventory: prize wall, event banner, reward card, limited-time tag, owned/equipped badge.
- Bottom action bar/HUD: score/reward meters with bright accent and stable numbers.
- Modal/toast: celebratory success, clear warning, no confetti behind dense text.
- State language: selected uses spotlight, fill, badge, or check. Do not put neon glow on every component.

### Casual Puzzle

- Panels: board-adjacent trays, goal panels, booster shelves, clean white or warm surfaces.
- Buttons: friendly rounded controls, large enough for touch, primary action stronger than boosters.
- Tabs/cards: level/reward cards with stable goal and move data.
- Mission/shop/inventory: booster card, goal tray, progress path, locked level with requirement.
- Bottom action bar/HUD: booster bar and moves/goal counters stay fixed and do not cover the board.
- Modal/toast: level complete, out-of-moves, reward, and retry states must preserve board context.
- State language: selected uses fill/check/ring only on the chosen level or booster; avoid sale chrome over gameplay.

### Fantasy RPG

- Panels: parchment, leather, worn metal, stone, wood, or spellbook material; decorative detail must not shrink content.
- Buttons: crafted plates, engraved tabs, restrained rarity highlight, readable labels.
- Tabs/cards: inventory, quest, stats, and shop surfaces use material hierarchy: parchment for text, metal/leather for slots.
- Mission/shop/inventory: quest cards, item slots, rarity labels, compare panels, equipped marks, locked requirement.
- Bottom action bar/HUD: spell/action slots can be crafted but should read as one bar or grid.
- Modal/toast: quest accepted, item gained, warning, and confirmation styles use the same material system.
- State language: rarity may use gem color plus label/mark. Do not make every slot glow gold.

### Sci-Fi Tactical

- Panels: compact edge panels, low-noise glass/metal, command-grid alignment, restrained data accents.
- Buttons: technical rectangular controls, concise labels, active states as system lock, scan, or route preview.
- Tabs/cards: segmented filters, command cards, alert rows; active/current gets data indicator plus weight.
- Mission/shop/inventory: loadout cards, unit cards, equipment slots, locked tech prerequisites.
- Bottom action bar/HUD: command bar, cooldown grid, minimap/radar, fixed readouts.
- Modal/toast: alert stack with severity; avoid equal-priority warnings.
- State language: cyan/amber/green only for real system state. Avoid all-neon and animated noise behind text.

### Cozy / Lifestyle

- Panels: soft surfaces, gentle hierarchy, calm spacing, friendly but not washed out.
- Buttons: rounded but controlled, warm primary, subtle secondary, calm pressed feedback.
- Tabs/cards: diary, calendar, task, collection, or room cards with soft dividers.
- Mission/shop/inventory: collection shelves, recipe cards, garden plots, checklist cards, friendly locked/progress copy.
- Bottom action bar/HUD: quiet progress, habit streak, collection count, or gentle navigation.
- Modal/toast: small completion feedback, no pressure-heavy warning language.
- State language: selected uses soft fill/check/underline; disabled remains legible. Avoid beige-only low contrast.

### Racing / Sports

- Panels: compact stat strips, asphalt/metal/rubber surfaces, team or vehicle accent.
- Buttons: strong start/race CTA, directional press feedback, secondary controls lower chrome.
- Tabs/cards: garage, loadout, leaderboard, bracket, stat compare cards.
- Mission/shop/inventory: vehicle parts, upgrades, race events, locked class/license, equipped part state.
- Bottom action bar/HUD: speed/timer/lap data first; fixed-width numbers; warning colors only for race state.
- Modal/toast: finish result, new record, penalty, repair, or purchase confirmation.
- State language: selected uses team accent, underline, fill, or stat highlight. Avoid random neon unless the race world supports it.

### Strategy / War Room

- Panels: dense but organized edge panels, map margins, command surfaces, clear grouping.
- Buttons: tactical commands, filters, unit actions; active state tied to selected tool/range/path.
- Tabs/cards: unit cards, objective tracker, faction filters, territory panels.
- Mission/shop/inventory: operation cards, unit upgrades, locked tech/territory requirement.
- Bottom action bar/HUD: command bar, unit stance, action points, cooldown/resource meters.
- Modal/toast: orders, alerts, territory change, failed action, confirmation.
- State language: selected uses map/faction accent and clear indicator; too many equal alerts are a failure.

### Historical / Period

- Panels: era-specific surfaces such as ledger paper, archive card, wood, stone, enamel sign, brass plate, instrument panel, cloth, or map margin. Material must match the named era and region.
- Buttons: modern hit targets with period cues: stamp, tab, carved plate, paper slip, enamel control, brass switch, wax mark, or printed label. Do not sacrifice clarity for ornament.
- Tabs/cards: dossier tabs, catalog cards, museum labels, route slips, shop ledgers, quest notices, artifact trays, or period signage.
- Mission/shop/inventory: missions can be contracts, maps, dispatches, orders, wanted posters, tickets, or archive folders; shop/inventory states use owned/equipped/locked labels plus material cues.
- Bottom action bar/HUD: compact tool belt, command strip, instrument row, card tray, or ledger footer. It must respect touch safe areas and never cover the board/playfield.
- Modal/toast: stamp, receipt, telegram, notice, seal, instrument alert, or dispatch format, with modern action hierarchy.
- State language: selected uses stamp/check/slip/fill/edge marker; locked uses seal, missing permit, rank, date, key, or requirement. Avoid generic gold frames and old-English text as a universal period style.

### Kids / Education

- Panels: large, simple, forgiving, bright but controlled.
- Buttons: big targets, plain labels, positive feedback, obvious disabled reasons.
- Tabs/cards: lesson cards, progress badges, workbook sheets, simple navigation.
- Mission/shop/inventory: activity cards, reward stickers, locked lesson requirement, safe store states.
- Bottom action bar/HUD: simple progress and next/back controls, no hidden navigation.
- Modal/toast: encouraging success/error, short copy, no scary or punishment-heavy visuals.
- State language: selected uses check/star/fill plus label. Do not rely on subtle state differences.

### Premium / Luxury

- Panels: minimal chrome, precise alignment, high-quality imagery, restrained material accents.
- Buttons: refined solid primary, low-noise secondary, generous spacing, deliberate hover.
- Tabs/cards: editorial product cards, gallery filters, comparison panels with careful typography.
- Mission/shop/inventory: product tiles, reservation/booking/purchase cards, availability and owned states.
- Bottom action bar/HUD: rare; if needed, minimal floating control with high contrast.
- Modal/toast: elegant confirmation, clear consequence, low-amplitude motion.
- State language: selected uses spacing, weight, underline, or subtle accent. Do not fake luxury with gold everywhere.

### Productive SaaS / Admin

- Panels: neutral surfaces, table/detail grouping, low chrome, dense but scannable.
- Buttons: one solid primary per workflow; secondary outline/text; destructive explicit.
- Tabs/cards: table tabs, filters, detail cards, command bars with predictable states.
- Mission/shop/inventory: translate to task row, plan card, billing item, or asset card when relevant.
- Bottom action bar/HUD: usually command bar, bulk action tray, or sticky footer.
- Modal/toast: focused forms, confirmation, non-blocking status.
- State language: selected row/current tab/focus must be obvious without decorative chrome. Avoid game-like glow and hero-card styling.

### Finance / Analytics

- Panels: metric strips, chart cards, account surfaces, explicit units and time ranges.
- Buttons: trustworthy restrained actions, high-risk actions confirmed, disabled reasons explicit.
- Tabs/cards: range tabs, portfolio cards, comparison panels, alert rows.
- Mission/shop/inventory: translate to product/account/plan/transaction card; status and affordability must be explicit.
- Bottom action bar/HUD: sticky action/footer for review, transfer, or compare flows.
- Modal/toast: confirmation and risk language must be clear; live values should not be distracted by motion.
- State language: gain/loss/risk uses color plus arrow, sign, label, or pattern. Avoid red/green-only decisions.

### Consumer Mobile

- Panels: clean sheets, cards, bottom navigation, snackbars, branded but readable.
- Buttons: one primary action per screen, thumb-friendly height, clear loading and disabled states.
- Tabs/cards: bottom nav, segmented filters, item cards, list rows with familiar mobile behavior.
- Mission/shop/inventory: translate to task, content, product, cart, favorite, or profile cards.
- Bottom action bar/HUD: sticky CTA, bottom nav, media/action tray; respect safe areas.
- Modal/toast: sheet or snackbar when possible; full modal only for blocking decisions.
- State language: selected nav/current filter must be clear; destructive actions require confirmation or undo.

## State Cheat Sheet By Theme

| Theme | Default | Hover | Active/Pressed | Focus | Selected | Locked/Disabled |
|---|---|---|---|---|---|---|
| Horror | Matte, quiet | Slight surface lift | Heavy press/dim | Bone or rust ring | Edge accent/fill | Dim plus reason/key clue |
| Hyper casual | Bright simple | Scale/fill | Elastic press | High-contrast ring | Fill/check/scale | Friendly requirement |
| Fun arcade | Bold surface | Spotlight/tint | Bounce | Clear outline | Badge/fill/check | Muted with event gate |
| Puzzle | Clean tray/card | Soft lift | Squash/press | Ring or high-contrast outline | Fill/check/goal cue | Locked level requirement |
| Fantasy RPG | Material plate | Material highlight | Engraved press | Readable aura/ring | Rarity/edge plus label | Prerequisite/lock mark |
| Sci-fi tactical | Compact panel | Data highlight | System lock | Sharp system ring | Indicator/scan/fill | Tech prerequisite |
| Cozy | Soft surface | Gentle lift | Calm press | Friendly outline | Soft fill/check | Muted plus progress |
| Racing/sports | Stat strip | Accent underline | Directional press | Team/signal outline | Team accent/stat cue | License/class gate |
| Strategy | Command surface | Range/tool preview | Tool armed | Clear tactical outline | Faction/map indicator | Tech/territory gate |
| Historical/period | Period material | Ink/stamp/material cue | Physical press/stamp | Visible era-fit ring | Stamp/fill/edge marker | Permit/key/rank/date reason |
| Kids/education | Big simple | Bright feedback | Simple press | Thick visible ring | Check/star/fill | Plain reason |
| Premium/luxury | Minimal | Subtle tone/elevation | Low-amplitude press | Refined visible outline | Underline/weight/accent | Muted but legible |
| SaaS/admin | Neutral | Subtle fill | Standard press | Accessible ring | Row/tab indicator | Muted plus reason |
| Finance | Neutral data | Slight fill | Standard press | Accessible ring | Range/row highlight | Muted plus risk/reason |
| Consumer mobile | Native surface | Subtle fill | Press opacity | Platform-visible ring | Nav/filter fill | Muted plus helper |

## Anti-Pattern Fixes

- If every card has a border, selected state must use fill, indicator, weight, or label instead of another border.
- If a tray has a strong frame, inner hotbar slots should be quiet recesses or fills.
- If the theme is serious, do not use gold/yellow/neon frames as generic polish.
- If the theme is playful, do not inherit dark tactical chrome just because the UI is a game.
- If rarity uses color, add a label, icon, mark, or weight.
- If locked state is only gray, add reason, lock icon, requirement, progress, or tooltip.
- If hover and selected look similar, make selected persistent and semantic; keep hover transient and lighter.
- If focus looks like decoration, change its timing or shape so it appears only on keyboard/controller focus.

## Handoff Template

For each themed component, document:

- Component:
- Theme row:
- Default material:
- Shape/radius:
- Primary action style:
- Secondary action style:
- Hover:
- Active/pressed:
- Focus-visible:
- Selected/current:
- Disabled/locked:
- Loading/pending:
- Error/warning:
- Mobile/touch behavior:
- Controller/keyboard behavior:
- What not to do:

## Sources

- See `references/source-bibliography.md` for the standards and research behind these rules.
