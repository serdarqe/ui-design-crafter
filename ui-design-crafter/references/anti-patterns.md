# UI Anti-Patterns

Use this reference at design time to avoid the habits that make UI look machine-generated instead of designed. This is the "why it happens and how to fix it" companion to `references/visual-qa-checklist.md`, which lists the same tells as review-time checks.

Each entry is: the tell, why it reads as AI-generated, and the professional fix. The goal is not minimalism for its own sake; it is intent. Every border, glow, gradient, and box should earn its place by communicating structure, state, or meaning.

## Structure And Framing

### Frame stacking
- Tell: an outer panel border, bordered child cards, and inner item borders are all visible at once.
- Why it looks AI: the model adds a frame at every nesting level "to be safe," so depth is communicated five times instead of once.
- Fix: choose one structural frame per cluster. Inside it, use fill, spacing, dividers, or state color for the children. A toolbar should read as one tray with slots, not five framed cards inside another framed card.

### Card-in-card
- Tell: a card wraps a card wraps the content.
- Why it looks AI: containers are generated defensively without checking whether the inner box adds meaning.
- Fix: keep one surface step. Promote the inner content to the outer card, or replace the inner card with a heading plus spacing. Reserve nested cards for genuinely repeated items.

### Double borders
- Tell: an element has a border and a ring/outline, or a border plus an inset highlight that reads as a second line.
- Why it looks AI: border, ring, and inset utilities get stacked because each looks "polished" alone.
- Fix: one boundary per edge. Use border OR ring for the resting state; reserve the second outline for focus or selected so it actually means something.

### Decorative-but-dead panels
- Tell: framed boxes, corner brackets, or themed ornaments that hold no information and only shrink the content area.
- Why it looks AI: decoration is added to fill space and signal "game UI" or "premium" without serving a task.
- Fix: cut the panel or give it real content. Express theme through typography, color role, imagery, and composition before adding another frame.

### Single-panel or split-panel background
- Tell: the backdrop is one oversized rounded rectangle, fake chart, fake dashboard, board, table, boxed scene preview, split left-side backdrop panel, or simple panel behind the real UI.
- Why it looks AI: the model tries to make the background "about the theme" by drawing a symbolic UI object, but it does not design a real environment, material surface, product context, or composition.
- Fix: either keep the app background clean and neutral, or build a layered scene/context. For games, use a place or gameplay space. For dashboards/tools, use a quiet work surface, device/context crop, data wall, command room, content canvas, or subtle workflow evidence. The same background field should continue behind left and right UI regions. A panel-like object can be one supporting cue, not the whole background. A framed background panel is allowed only when it is literally a map, camera feed, preview, artwork, level board, monitor, or inspectable object.

## Color And Effects

### Glow on everything
- Tell: every button, icon, slot, and panel has a halo or drop-glow.
- Why it looks AI: glow is applied uniformly as a "juice" effect rather than as a state signal.
- Fix: use contrast and silhouette for legibility; reserve glow for state changes (selection, ready ability, reward, alert). If everything glows, nothing reads as special.

### Gradient soup
- Tell: gradients on background, panels, buttons, and text at the same time.
- Why it looks AI: gradients are sprinkled per element with no shared light model.
- Fix: pick a clear surface logic - usually flat or near-flat surfaces with at most one signature gradient (a hero, a primary action, or a background). Solid fills read as more intentional than a stack of gradients.

### Repeated identical chrome
- Tell: the same radius, border color, shadow, and inset on every control.
- Why it looks AI: one "card style" is cloned onto everything, flattening hierarchy.
- Fix: build a small material system - default, raised, and emphasized surfaces differ on purpose. Vary weight by importance, not at random.

### One-note palette
- Tell: every surface, border, and accent is a tint of the same hue; no true neutral, no semantic colors.
- Why it looks AI: a single brand hue is multiplied into a whole theme.
- Fix: define roles - neutral surfaces (the 60%), a supporting color (30%), one accent (10%), plus stable semantic success/warning/danger/info. See `references/color-theory-for-ui.md`.

### Default dark purple/blue palette
- Tell: near-black surfaces with purple, indigo, blue, or cyan accents appear even when the user did not ask for dark mode, sci-fi, AI, cyber, or neon.
- Why it looks AI: the model falls back to a fashionable "modern tech" preset instead of reading the user's product, brand, audience, or genre.
- Fix: choose colors from the user's context first. If the request is healthcare, education, ecommerce, cozy lifestyle, kids, editorial, or premium retail, start from that domain's emotional and usability needs. Use dark blue/purple only when it is justified by content, brand, environment, or genre.

### Unquestioned reference palette
- Tell: a redesign keeps the source screenshot's dark/neon/purple-blue palette even though the user asked to remove the AI-generated look or did not ask to preserve that styling.
- Why it looks AI: the model treats the reference as a visual skin to copy instead of separating product intent from template habit.
- Fix: extract the purpose, hierarchy, and useful component ideas from the reference, then choose a palette from the product context. If the original palette is kept, write the reason. If no reason exists, produce a light, warm-neutral, editorial, platform-native, or brand-led alternative.

### Mismatched accent frames
- Tell: panels, cards, buttons, or selected states get gold/yellow/neon outline frames even though the theme is horror, serious, gritty, medical, industrial, or otherwise not ornamental.
- Why it looks AI: a generic "premium/game card" treatment is applied as polish without checking whether that color belongs to the world, status model, or brand.
- Fix: make boundary color theme-native and state-driven. In horror, use muted rust, dried blood, sickly green, worn metal, shadow, or a single side accent instead of bright full-card frames. In apps, use the design system's border token, subtle fill shifts, dividers, or focus rings. Reserve gold/yellow for reward, rarity, luxury, currency, or warning states where it has meaning.

## Layout And Hierarchy

### Everything centered
- Tell: every section is centered with equal weight.
- Why it looks AI: centering is a safe default the model reaches for, but it erases scan path.
- Fix: establish hierarchy. Left-align reading content and forms, give one dominant action, and use alignment and size to lead the eye. Center sparingly (empty states, hero moments, single-focus dialogs).

### No dominant action
- Tell: ghost buttons everywhere, or three solid same-color buttons competing as equal primaries.
- Why it looks AI: emphasis is applied evenly instead of ranked.
- Fix: one solid primary per region; secondary actions go outline/ghost/subtle; destructive actions get danger semantics. The user should never have to hunt for the main action.

### Uniform spacing with no rhythm
- Tell: the same gap between every element, related or not.
- Why it looks AI: a single spacing value is applied globally.
- Fix: use proximity - tighter spacing inside a group, larger spacing between groups - so structure is visible without dividers (Gestalt).

## Content And Icons

### Placeholder filler presented as finished
- Tell: lorem text, fake metrics, "Title goes here," or repeated dummy rows in a "done" screen.
- Why it looks AI: scaffolding is left in place.
- Fix: use realistic content, test with long and short real values, and confirm the layout survives empty, loading, and error states.

### Mixed or emoji icons
- Tell: emoji standing in for icons, or icons from different sets at different stroke weights and sizes.
- Why it looks AI: icons are pulled ad hoc per element.
- Fix: use one icon set at consistent size and stroke (lucide or the project's set). Give icon-only controls tooltips and accessible names.

### Explaining the obvious
- Tell: visible helper text describing styling, shortcuts, or how to use a standard control.
- Why it looks AI: the model narrates the UI.
- Fix: let affordances and labels do the work; reserve helper text for genuine constraints, examples, and error recovery.

## App vs Game Calibration

- App/tool/dashboard UI: quiet, scannable, low chrome. Prefer borders and subtle surface shifts over shadows and glow; density follows task and expertise. The failure mode here is decorative noise that slows the task.
- Game UI: more expressive and themed, but the HUD must stay glanceable and the menu still needs one dominant action. The failure mode here is the "fantasy/sci-fi kit" look - identical glowing rounded rectangles everywhere. Theme through art, type, and composition; keep state signals (cooldown, low health, rarity, lock) louder than decoration.

## Fast Self-Check

Before calling a UI done, ask:

1. If I removed every border, glow, and shadow, would hierarchy still read from layout and type alone? (It should.)
2. Is there exactly one obvious primary action in this region?
3. Does each frame, glow, and gradient communicate structure, state, or meaning - or just exist?
4. Do default elements stay quiet so focus/selected/equipped/warning states are the loud ones?
5. Did I choose this palette because it fits the user, or because dark purple/blue felt like the default?
6. Does it survive real content, 320-390px width, grayscale, and colorblind simulation?

## Sources

- See `references/source-bibliography.md` for the standards and research behind these rules.
