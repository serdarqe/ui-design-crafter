# Visual QA Checklist

Use this before claiming a UI design or implementation is complete.

## Structure

- The first screen is the usable product/game UI requested by the user.
- Primary and secondary actions are visually distinct.
- Layout hierarchy is obvious without explanatory copy.
- Related controls are grouped and unrelated controls are separated.
- Cards are not nested inside cards.
- UI chrome is not stacked: a framed container does not also contain many equally framed buttons/cards unless there is a strong production-quality reason.

## Evidence

- `visual-test-workflow.md` was followed when screenshots or browser inspection are possible.
- At least one mobile and one desktop viewport have screenshot or metrics evidence before the UI is called complete.
- Standard viewports were checked for important app/game screens: 360x740, 390x844, 430x932, 740x360, 844x390, 932x430, 768x1024, and 1366x768.
- `visual_smoke_check.py` was run on available screenshot folders and browser metrics JSON, or the reason it could not run is documented.
- Any `fail` from the visual smoke check was fixed before final delivery.
- Any `warn` from the visual smoke check was inspected and either fixed or explicitly accepted with a reason.

## Store Asset QA

Use this section before App Store / Google Play delivery, after raw captures and store compositions exist.

- `store-capture-workflow.md` and `store-screenshot-aso.md` were followed before composing final assets.
- `export_store_screenshots.py` produced `manifest.store.json`; final delivery has rendered `.png`, `.jpg`, or `.jpeg` assets, not only HTML previews.
- `check_store_assets.py` was run on the final folder or `manifest.store.json`; all `fail` findings were fixed before delivery.
- Exact preset dimensions match the selected App Store / Google Play target.
- Google Play assets use JPEG or 24-bit PNG with no alpha/transparency.
- Google Play screenshots stay within min/max dimension and aspect-ratio rules; feature graphic is exactly 1024x500.
- Google Play feature graphic has a centered focal subject, thumbnail-level clarity, no important content in likely cutoff zones, and no empty pure white/black/dark-gray field.
- Google Play alt text exists for meaningful graphic assets when required, is 140 characters or less, describes the visible app/game value, and does not begin with generic prefixes such as "image of", "photo of", or "screenshot of".
- The set has the required screenshot count for the target platform/device group, or the limitation is documented.
- Portrait and landscape assets are not mixed accidentally in one store set.
- Captions are short, readable, tied to the visible UI/gameplay, and do not cover the main evidence.
- Captions avoid risky store claims such as ranking, fake awards, price urgency, "download now", or unverifiable outcomes.
- Localization expansion was checked; translated captions have enough space without shrinking into unreadable type.
- If preview video or App Preview is included, the first seconds show real UI/gameplay and remain understandable muted.
- If ASO optimization is requested, the asset set has one explicit hypothesis, one main changed variable, platform-specific variants, and a measurement plan beyond "looks better".

## Responsiveness

- Desktop, tablet, and mobile widths do not create overlapping UI.
- Banner and interstitial ads (app or game) sit in a reserved region and do not cover content, bottom navigation, the primary CTA, the keyboard, or the safe-area/home indicator; the no-ad/collapsed state and a real 44px close are handled.
- Text fits inside buttons, tabs, cards, panels, HUD labels, and table cells.
- Toolbars wrap or overflow cleanly.
- Modals and drawers remain usable on small screens.
- Fixed-format elements have stable dimensions and do not shift during state changes.

## Interaction States

- Hover, focus, active, disabled, loading, empty, error, success, selected, and pressed states exist where relevant.
- Icon-only controls have accessible names and tooltips.
- Destructive actions are clearly differentiated and confirmed when needed.
- Keyboard and controller focus order is predictable when those inputs apply.
- Modal focus moves inside on open and returns to the logical trigger on close.
- Drag-only interactions have a keyboard, button, or single-pointer alternative.

## Component Theme Fit

- The UI uses `component-theme-matrix.md` when the request has a theme, genre, mood, audience, game world, or product tone.
- Panels, buttons, tabs, cards, modals, shop items, mission cards, bottom action bars, inventory slots, HUD meters, and toasts express the selected theme through material, shape, density, state language, and motion.
- The component family does not look like one generic kit recolored across themes. Horror, hyper casual, fantasy, racing, SaaS, and finance components should have different material logic.
- Default, hover, active/pressed, focus-visible, disabled, selected/current, locked/unavailable, loading, and error states are present where relevant and remain theme-native.
- Selected/current states are clearer than hover but quieter than danger/error.
- Focus-visible states meet accessibility contrast and are not confused with permanent decoration.
- Locked/unavailable states explain the requirement or reason; they are not only gray and hidden.
- Shop, mission, inventory, and action-bar states do not resize components or shift layout when price, count, cooldown, owned, equipped, locked, or selected states change.
- Serious themes do not use gold/yellow/neon frames as generic polish. Playful themes do not inherit dark tactical chrome unless the world supports it.

## Accessibility

- Text contrast is readable against its actual background.
- Touch targets are large enough for mobile and game touch controls.
- Color is not the only signal for state.
- Motion is purposeful and not excessive.
- Form errors are visible near the fields they affect.
- Normal text targets at least 4.5:1 contrast; large text targets at least 3:1.
- Meaningful non-text UI indicators such as borders, focus rings, selected states, icons, and control boundaries target at least 3:1 contrast against adjacent colors.
- Pointer targets meet WCAG 2.2 minimum target-size expectations, and touch-heavy UI uses larger practical targets where appropriate.
- Focus indicators are visible against both the component and surrounding surface.

## Visual Quality

- Palette uses distinct roles instead of many shades of one hue.
- Palette matches the user's brand, domain, audience, content, and requested mood. It is not a generic dark purple/blue/cyan preset unless that direction was requested or clearly fits the product.
- If the UI was redesigned from a reference screenshot, the palette was challenged instead of copied. Dark/neon/purple-blue source colors are kept only with an explicit product, brand, environment, or user-requested reason.
- Borders and selected-state frames match the theme and status model. Gold/yellow/neon outlines are not used as generic polish; they appear only for reward, rarity, warning, luxury, currency, or a brand/genre that actually supports them.
- The selected theme row from `theme-style-guides.md` is visible in the result: background, palette, panel material, controls, HUD density, and motion all point to the same world.
- Background or scene art has recognizable subject matter that fits the user's genre, product, brand, and requested mood. It is not a generic gradient, fog layer, texture, or stock-like atmosphere.
- Background is not a single oversized panel, fake chart/table, centered board, boxed scene preview, split left-side backdrop panel, or simplified copy of the foreground UI. It must have real composition, environment, product context, or layered task context.
- Spacing follows a consistent scale.
- Typography hierarchy matches the UI density.
- Icons share a consistent style and size.
- Borders, glows, inset highlights, shadows, and radius are used sparingly. Default controls should not all have the same permanent outline.
- Decorative frames are quieter than functional states such as focus, selected, equipped, warning, danger, and active.
- Images or game assets render clearly and are not dark, blurry, or purely decorative when users need to inspect content.
- Overlays protect text contrast without erasing the background's place, object, product, or story cues.
- The palette preserves meaning in light mode, dark mode, grayscale, and colorblind simulation.
- Primary, secondary, destructive, disabled, selected, warning, error, health, and success states remain distinct without relying on hue alone.

## Background And Scene Art

- The background follows a specific theme row from `theme-style-guides.md` and a composition plan from `background-composition.md`.
- The screen's genre, product, or task is identifiable from the background without reading the title or logo.
- The background has foreground, midground, and background depth, or a deliberate clean app surface. It is not only one large rounded rectangle, chart, panel, board, boxed preview, split decorative side panel, or empty placeholder object.
- Left and right UI regions share one continuous backdrop. If one side is framed, it must be real content such as a map, camera feed, image preview, board, monitor, or inspectable object, not decorative background filler.
- There is one clear focal subject and two or three supporting environmental cues, not a collage of unrelated theme objects.
- Main UI clusters sit inside planned safe zones; text is not placed over the busiest part of the image.
- Mobile, tablet, and desktop crops preserve the focal subject and do not crop out the main identity cue.
- Local scrims, edge fades, or surface fills protect readability; the whole scene is not darkened, blurred, or fogged until it becomes meaningless.
- Menu, mission select, shop, inventory, HUD, and dashboard backgrounds use different compositions when their information needs differ.
- Background materials and UI chrome belong to the same world. A horror scene should not receive generic gold frames; a hyper casual scene should not inherit dark tactical chrome.
- Product, item, level, map, or gameplay evidence remains inspectable when the user needs to compare or choose something.
- If external or user-provided references influenced the background, the output extracts principles and composition cues rather than copying protected imagery.

## Artificial / AI-Generated UI Tells

Scan for these signals that a UI looks machine-generated rather than designed. See `references/anti-patterns.md` for the fix for each.

- Frame stacking: an outer panel border plus bordered child cards plus inner item borders, all visible at once.
- Double borders: an element has both a border and a ring/outline, or a card border plus an inset highlight that reads as a second border.
- Card-in-card: a card wraps another card wraps content, adding boxes without adding meaning.
- Glow on everything: every button, icon, and panel has a halo or drop-glow, so nothing reads as special and nothing signals state.
- Repeated identical chrome: the same radius, same border color, same shadow, and same inset on every control, producing a flat UI-kit look instead of a hierarchy.
- Gradient soup: gradients on backgrounds, panels, buttons, and text simultaneously, with no clear surface logic.
- Everything centered: every section centered with equal weight, so there is no scan path and no dominant action.
- Decorative-but-dead panels: framed boxes, corner brackets, or sci-fi/fantasy ornaments that hold no information and only shrink the content area.
- Emoji or mixed-source icons standing in for a real icon set, or icons in inconsistent stroke weights and sizes.
- Ghost buttons everywhere: no solid primary, so the main action is ambiguous; or three solid same-color buttons competing as equal primaries.
- Text overflow: labels clip, truncate mid-word, or spill out of buttons, chips, tabs, HUD readouts, and table cells with real content.
- Mobile overflow: horizontal scroll at 320-390px, fixed desktop widths, or `100vh` cropping behind mobile browser chrome.
- Placeholder filler: lorem text, fake metrics, or "Title goes here" left in a screen presented as finished.
- One-note palette: every surface, border, and accent is a tint of the same hue, with no real neutral and no semantic state colors.
- Default cool-dark palette: near-black surfaces with purple/blue/cyan accents used without user, brand, genre, or domain justification.
- Unquestioned reference palette: source screenshot colors were preserved even though they look generic, AI-like, or unsupported by the product context.
- Mismatched accent frames: gold/yellow/neon outlines on panels or selected cards where the theme calls for muted, material, or semantic state treatment.
- Generic background: abstract gradients, fog, blobs, or dark texture used where a concrete product/game environment should establish mood and identity.
- Single-panel or split-panel background: one large panel/chart/board/table, boxed scene preview, or decorative left-side backdrop used as the whole visual idea, making the screen look like a placeholder instead of a designed environment or product context.

## Game-Specific

- HUD remains readable over bright, dark, and busy gameplay.
- Critical state changes are noticeable without covering gameplay.
- Touch controls do not conflict with gameplay gestures.
- Mobile safe areas are reserved for notch/status bar, rounded corners, home indicator, browser chrome, and platform overlays. Bottom HUD, hotbar, sticky CTA, shop action, and close/back controls are not cut off.
- Ad regions are planned and tested: banner, MREC/rectangle, rewarded-ad CTA, interstitial break, offerwall/store prompt, and consent surface do not cover the board, active playfield, timer, health, inventory, close/back controls, or primary CTA.
- Board/playfield remains the dominant surface. HUD, mission/shop cards, monetization prompts, and bottom action bars do not cover playable cells, drag paths, target zones, aim lines, cooldowns, or critical feedback.
- Controller selected states are unmistakable.
- Timers, counters, meters, and cooldowns do not resize while changing.
- Run a gameplay-pressure glance test for combat, timers, cooldowns, and warnings.
- Check subtitle, colorblind, text-size, input remapping, and controller-only variants when the game supports them.
- Keep the center of fast gameplay screens free from persistent high-detail UI unless the mechanic requires it.
- Action bars read as one tray/device or as separate buttons, not both at equal visual strength.
- Historical/period UI names its era/region assumption, uses period-specific material cues, keeps body text readable, and avoids generic parchment, sepia, gold frames, anachronistic icons, or copied protected imagery.

## Evidence-Based Checks

- Can a new user identify the primary task and CTA within five seconds?
- Does every screen have a complete state set: default, loading, empty, error, success, disabled, focus, selected, and pressed where relevant?
- Are forms preventing errors with constraints, examples, defaults, and suggestions before showing error copy?
- Are references used as extracted principles rather than copied visuals?
