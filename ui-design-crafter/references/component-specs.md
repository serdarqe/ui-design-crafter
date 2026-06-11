# Component Specs

Use this reference when defining reusable UI components. Always defer to the project's existing design system; the numbers below are common production defaults for when no system exists yet. Pair this with `references/anti-patterns.md` to avoid generated-kit habits.

## Sizing And Spacing Baseline

- Use one spacing scale, ideally a 4px base: 4, 8, 12, 16, 24, 32, 48. Inside a control use 8-12; between groups use 16-24. Do not invent one-off values like 7px or 13px per element.
- Pick one or two radii for the whole product, not a different corner on every box. Common tiers: 4-6 for small controls, 8-10 for cards/panels, 12-16 for sheets/large surfaces. Round nested elements smaller than their parent.
- Control heights: 32 compact (dense desktop tools), 40 default, 44-48 touch/comfortable, 52-60 for hero or game-primary actions. Keep heights from the same set across the UI.
- Hit targets: 44x44 px/pt minimum for touch and game UI; pointer-only UI may go to 32 but keep clickable padding generous.
- Icon sizes: 16 inline with text, 20 default UI, 24 prominent or touch. Keep one stroke weight family.
- Border width: 1px is the default; reserve 2px (or a brighter color) for selected, active, focus, or error so state actually stands out from default.
- Elevation order: surface step, then 1px border, then a single soft shadow. Do not apply border + heavy shadow + inset highlight + glow to the same element by default.
- Reading text line length: target 45-75 characters; do not let body copy run the full width of a wide panel.

## Buttons

- Include default, hover, active, focus, disabled, loading, destructive, and success states.
- Use icon-only buttons for compact tools and icon+label buttons for primary commands.
- Keep text short and make labels wrap or shrink only as a last resort.
- Preserve stable width for buttons that change to loading or success text.
- Primary buttons use the strongest fill only for the main action in a region. Secondary buttons should use outline, subtle fill, or lower emphasis.
- Destructive buttons need danger semantics and confirmation when the action is irreversible or high cost.
- Touch-heavy buttons should generally use 44x44 px/pt or larger hit areas even when the visible shape is smaller.
- Do not put a visible border on every button inside an already framed toolbar, HUD panel, or action bar. Prefer one container surface, then use transparent buttons, subtle fills, separators, or state color for each item.
- Avoid identical radius, identical border color, identical inset glow, and identical shadow on every control. That creates a generated UI-kit look instead of a designed material system.
- Typical anatomy: horizontal padding ~1.5x to 2x the vertical padding (e.g. 10px x 16px), label centered or left-aligned, optional leading icon at 16-20px with 8px gap. Default height from the height set above.
- Give buttons a sensible min-width (e.g. 96-120px for labeled actions) so short labels do not produce tiny pills, but let them grow with content instead of truncating mid-word.
- One emphasis ladder per region: one solid primary, the rest outline/ghost/subtle. Do not render three solid same-color buttons side by side. Ghost buttons should not be the only style on a screen, or nothing reads as the main action.

## Panels

- Use panels to group related controls or information, not as decorative containers.
- Include title, optional description, primary action, secondary actions, content area, empty state, and loading state when applicable.
- Keep panel hierarchy shallow. Avoid nested cards inside panels unless each card is a repeated item.
- App panels should sit one or two surface steps from the page background and use neutral borders before heavy shadows.
- Game HUD panels can use translucent surfaces, but critical text and icons must maintain contrast over gameplay backgrounds.
- Pick one boundary treatment per cluster: outer frame, inner item borders, dividers, or shadow. Do not combine all of them unless the design system already proves that style at production quality.
- Use border/glow as information only when it communicates focus, selection, rarity, warning, danger, or active state. Decorative borders should be quieter than state borders.

## Toolbars

- Group tools by task and separate groups with spacing or dividers.
- Use icon buttons with accessible labels and tooltips.
- Use segmented controls for modes, not multiple independent buttons.
- Move lower-priority actions into an overflow menu on narrow widths.
- For action bars and game HUD toolbars, treat the bar as one physical tray. Inner actions should read as slots or pressable surfaces without repeated heavy outer rings.

## Forms

- Use labels, inputs, helper text, validation messages, required indicators, disabled states, and submission feedback.
- Align related fields and keep action buttons near the form end.
- Use toggles for binary settings, radio groups for small exclusive choices, selects or menus for longer option sets, and sliders/steppers for numeric tuning.

## Tabs And Navigation

- Tabs switch peer views in the same context. Do not use tabs for unrelated destinations.
- Active tab, hover, focus, disabled, and overflow states must be visible.
- Keep tab labels short and avoid wrapping inside tab buttons.
- Choose one tab style: underline/indicator tabs for content sections, or pill/segmented tabs for filters and modes. Do not give every tab a full box border plus a fill plus an indicator at once.
- The active tab should win by weight, fill, or indicator, not by being the only one with a border. Inactive tabs stay quiet.

## Dialogs And Overlays

- Modals need a clear title, focused content, close/back behavior, keyboard focus handling, and primary/secondary actions.
- Confirmation dialogs should state the consequence and name the affected object when possible.
- Toasts should be brief, actionable only when useful, and not block important controls.
- Use modals only when the flow must stop. Prefer inline expansion, popovers, drawers, or toasts for lighter feedback.
- Move focus into a modal when it opens and return focus to the logical trigger when it closes.
- Do not put critical required decisions only in toast messages.
- Size to content: roughly 400-480px wide for confirmations, 560-720px for forms, and a capped large width (e.g. max 960-1120px) for browse/detail modals; cap height and scroll the body, never the whole dialog off-screen.
- One framed surface per modal. The dim backdrop already separates it from the page, so the inner content does not need its own heavy border plus shadow plus cards-in-cards. Header, scrollable body, and a footer action row are usually enough.

## Status Elements

- Badges, chips, meters, progress bars, cooldowns, and counters need semantic color and stable sizing.
- Avoid relying on color alone. Pair color with labels, icons, position, or shape.
- Health bars need readable current state, critical threshold behavior, and optional numeric/segment cues.
- Inventory slots need empty, occupied, selected, equipped, locked, rarity, insufficient-resource, and drag/keyboard states.
- Shop cards need price, affordability, owned/equipped, preview, selected, purchase-pending, success, and error states.

## HUD Elements

- A HUD element is a status readout first and decoration second. Anatomy: icon or glyph, value with tabular numbers, optional label, optional progress fill. Keep the value the loudest part.
- Reserve fixed width for counters, timers, ammo, and resource numbers so the layout does not shift when values change (e.g. 999 -> 1000).
- Put critical readouts on a contrast plate (subtle solid or blurred surface) so they survive bright, dark, and busy backgrounds. Do not rely on a glow halo as the only legibility aid.
- Pick one container model per HUD cluster: either a framed tray holds quiet inner chips, or floating chips each get a subtle surface. Not both framed.
- Animate on state change (damage, low resource, pickup), not continuously.

## Action Bar / Hotbar

- Treat the bar as one physical tray or device, not five framed cards inside another framed card.
- Slot anatomy: square or near-square slot (commonly 48-64px touch, 40-56px desktop), centered icon, optional keybind hint in a corner, optional count, and a cooldown overlay layer.
- The tray gets the structural surface; slots read as recesses or fills, not as fully bordered buttons that repeat the tray's frame.
- Cooldown should overlay the slot (radial sweep or top-down fill) plus a number, and must not resize or move the slot.
- Show empty/assignable slots, active/selected slot, disabled (no resource) slot, and on-cooldown slot. Keep selected state stronger than default but quieter than a danger/alert state.

## Shop Card

- Anatomy: item art or preview, name, short descriptor, rarity/tag, price with currency icon, and one primary action (buy/equip). Keep one clear action per card.
- States: default, hover/focus, selected, affordable, unaffordable (price emphasized, action disabled with reason), owned, equipped, purchase-pending (stable-width spinner), success, error, and limited-time/locked.
- Keep card size stable across states. Owned/equipped should restyle the action, not reflow the card. Reserve the brightest border/glow for selected or rarity, not for every card at rest.
- Price affordability is information: when unaffordable, make the gap obvious (muted action, currency cue) instead of only disabling silently.

## Inventory Slot

- Anatomy: fixed-size cell, item icon, optional rarity frame/tint, stack count in a consistent corner, and equipped/selected indicator.
- States: empty, filled, hover, focus/controller-focused, selected, equipped, locked (with reason), invalid drop target, and insufficient-resource.
- Rarity must not rely on hue alone: pair frame color with a label, corner mark, border weight, or icon so colorblind players still read it.
- Keep all slots the same size; rarity or equipped state changes the frame/badge, never the cell dimensions. Provide a keyboard/controller path in addition to drag.

## Color And State Matrix

- App panel/card: neutral surface, subtle border, stable spacing, clear title, and content hierarchy.
- Game HUD panel: translucent or themed surface, high-contrast foreground, minimal center obstruction, and no color-only critical state.
- Modal/dialog: dim background, focused content surface, visible close/back behavior, and clear primary/secondary actions.
- Primary button: accent fill, high-contrast text/icon, visible focus ring, pressed state, loading state, and disabled reason when needed.
- Secondary button: lower emphasis than primary, clear border or subtle fill, and no competition with the main CTA.
- Destructive button: danger role, confirmation for costly actions, and recovery path when possible.
- Disabled button: desaturated or muted state; do not make it look broken or invisible.
- Toggle: off/on states must differ by more than color; thumb and track need non-text contrast.
- Slider/stepper: value, min/max, disabled state, focus, and keyboard behavior must be visible.
- Notification/toast: success/error/info role, short copy, non-blocking placement, and no hidden critical decision.

## Frame Stacking Anti-Pattern

Frame stacking happens when a UI cluster uses too many boundary effects at once: outer panel border, inner button borders, rounded boxes around every item, inset highlight, glow, thick shadow, hover border, selected border, and focus ring all visible together.

Avoid it by default:

- One visible structural frame per cluster is usually enough.
- Inner controls can use fill, icon contrast, spacing, dividers, active underline, or pressed background instead of their own complete frame.
- Focus rings are allowed for accessibility, but they should appear only on focus and should not be confused with permanent decoration.
- Selected/equipped/error states may use borders, but ordinary default buttons should not compete with those state borders.
- In game UI, a toolbar should feel like a crafted tray or device, not five separate framed cards inside another framed card.

## Sources

- See `references/source-bibliography.md` for the standards and research behind these rules.
