# Component State Matrix

Use this file before designing a component library, implementing reusable UI, or reviewing whether buttons, panels, HUDs, menus, and controls are production-ready.

## Required state rule

Every interactive component must define default, hover, active/pressed, focus-visible, disabled, loading, error when applicable, selected/current when applicable, and empty/skeleton when content can be absent.

| Component | Required states | Color and visual rules | Accessibility and input | App/game notes |
|---|---|---|---|---|
| Primary button | default, hover, pressed, focus, disabled, loading | Strongest action color; disabled still legible; loading preserves width | Accessible name; keyboard activation; target size suitable for platform | Use for one dominant action per surface |
| Secondary button | default, hover, pressed, focus, disabled | Lower emphasis than primary; border or subtle fill | Same target and focus requirements as primary | Good for cancel, back, alternate action |
| Destructive button | default, hover, pressed, focus, disabled, confirmation | Danger color plus label/icon; do not rely on red alone | Confirm or undo for high-risk actions | In games, use extra care for delete/sell/discard |
| Icon button | default, hover, pressed, focus, disabled, selected | Stable square/circle hit area; icon contrast high enough | Tooltip and accessible name required | Use for tools, pause, settings, inventory filters |
| Toggle / switch | on, off, hover, focus, disabled | State must be visible by position and color | Label required; keyboard operable | Avoid for immediate destructive changes |
| Checkbox / radio | unchecked, checked, indeterminate, focus, disabled | Check mark visible without color-only state | Label click area included | Useful for filters/settings |
| Segmented control | default, selected, hover, focus, disabled | Selected segment must be unmistakable | Arrow/key support when implemented as tabs/radio group | Good for modes, chart ranges, inventory filters |
| Tabs | inactive, active, hover, focus, disabled | Active tab uses indicator plus text weight/color | Correct tablist behavior when interactive | Use for sections, not primary actions |
| Slider / stepper | default, hover, focus, disabled, dragging | Track/fill/thumb contrast; value visible when needed | Keyboard and precise value input for critical settings | Use steppers for exact quantities, sliders for ranges |
| Text input | empty, focused, filled, error, disabled, read-only | Label remains visible; error color plus message/icon | Programmatic label, autocomplete when useful | Avoid placeholder-only labels |
| Select / menu | closed, open, hover option, selected option, disabled | Clear trigger affordance; menu above overlays | Keyboard navigation and escape close | Good for option sets, not binary choices |
| App panel / card | default, hover when clickable, selected, loading, empty | Surface, border, and shadow hierarchy consistent | If clickable, expose as button/link semantics | Keep cards for repeated items or framed tools |
| Modal / dialog | open, closing, loading, error | Backdrop, title, primary/secondary action hierarchy | Focus trap, escape behavior, return focus | Use for interruption or confirmation only |
| Toast / notification | info, success, warning, error, loading | Semantic color plus icon/title; readable timeout | Pause/extend for actionable content | In games, avoid blocking core action unless critical |
| Toolbar | default, grouped, active tool, disabled tool | Icon buttons aligned to stable grid | Tooltips, roving focus when complex | Essential for editors/builders |
| Game HUD panel | normal, alert, damaged/critical, hidden, transition | Critical state must be visible during gameplay | Scales across aspect ratios; no tiny text | Keep out of gameplay target area when possible |
| Health/resource bar | full, partial, low, empty, regenerating, damage flash | Shape/label plus color; low state distinct | Do not rely only on red/green | Add tick marks or numbers when precision matters |
| Cooldown / ability | ready, cooling down, locked, insufficient resource, active | Radial/linear progress plus count/label | Must be readable at gameplay speed | Avoid hiding cooldown under effects |
| Inventory slot | empty, filled, hover, selected, equipped, locked, invalid drop | Rarity/quality frame consistent; item icon readable | Keyboard/controller traversal if applicable | Show stack count, compare, sell/discard safeguards |
| Shop card | default, hover, selected, unaffordable, purchased, limited-time | Price and ownership state explicit | Confirm purchase; prevent accidental spend | Avoid paywall clutter over core play |
| Quest tracker | active, completed, failed, updated, hidden | Priority and distance/state visible | Text readable while moving | Keep current objective scannable |
| Skill tree node | locked, unlockable, unlocked, selected, preview, insufficient points | Connection paths clear; state not color-only | Explain prerequisites | Good tooltips prevent planning mistakes |

## Handoff checklist

- Define tokens for surface, border, text, muted text, primary, accent, success, warning, danger, focus, and disabled.
- Document component dimensions, spacing, radius, icon size, text style, and responsive behavior.
- Specify how each component behaves with long text, missing data, loading data, and localization.
- Specify pointer, keyboard, touch, and controller behavior when relevant.
- Include visual examples for normal, focused, disabled, error, loading, and selected states.

## Sources

- See `references/source-bibliography.md` for the standards and research behind these rules.
