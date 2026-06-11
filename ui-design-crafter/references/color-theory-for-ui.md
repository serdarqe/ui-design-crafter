# Color Theory For UI

Use this reference when defining palettes, themes, component states, HUD color, and semantic UI colors.

## Color Roles

- Separate brand color from functional UI color. Brand may influence accent, but it must not replace semantic success, warning, danger, info, or disabled roles.
- Define at least these roles: background, surface, surface-raised, content-primary, content-secondary, border, primary/accent, focus, selected, success, warning, danger, info, disabled.
- Use color as a hierarchy and state system, not as decoration.
- Keep a restrained color ratio. A useful starting point is 60 percent dominant neutral/surface, 30 percent secondary/supporting color, and 10 percent accent/action color.

## Contrast And Accessibility

- Target at least 4.5:1 contrast for normal text and 3:1 for large text.
- Target at least 3:1 contrast for meaningful non-text UI indicators such as input borders, focus rings, selected outlines, icons that communicate state, and control boundaries.
- Do not communicate meaning by color alone. Pair state color with label, icon, shape, position, pattern, audio, haptic, or motion.
- Test success, error, selected, health, warning, rarity, and disabled states under colorblind simulation.

## Palette Construction

- Start from the user's context: product category, brand cues, audience, content imagery, platform, genre, mood, and existing tokens. Color is a response to the design problem, not an automatic style preset.
- Do not default to dark purple/blue, neon cyan, or generic dark-mode just because the UI is "modern," "game," "AI," "dashboard," or unspecified. Use those directions only when the product, genre, brand, or user request calls for them.
- Think in hue, saturation, lightness/value, and contrast separately. More saturated does not always mean more readable.
- Use color harmony systems such as complementary, analogous, triadic, or split-complementary to build a palette, not to decide semantic state colors.
- Keep semantic colors stable across light and dark themes. Error should not become a decorative accent in one theme and a warning in another.
- Avoid one-note palettes where every surface, border, and accent is only a variation of one hue.

## Avoid AI Default Palettes

- Common generated-looking default: near-black surfaces plus blue/purple/cyan accents everywhere. This often appears when no color decision was made.
- Professional fix: write a one-sentence color rationale before choosing colors. Example: "This is a kids education app, so the palette should be light, warm, high-contrast, and encouraging, not dark neon."
- If the user provides a screenshot, brand, genre, reference, or existing CSS tokens, extract the intended mood and product cues first; do not preserve the palette uncritically. Change the palette when the current colors fail usability, accessibility, tone, brand fit, or when they read like a generic AI/template habit.
- If no color direction exists, choose from the domain: healthcare calm, finance trust, ecommerce product-first, kids playful, cozy lifestyle, fantasy RPG, sci-fi tactical, horror sparse, premium restrained, etc. Use `scripts/search_design_tokens.py` for options.
- Dark mode is not the default. Decide light/dark from platform expectations, environment, content, and user preference. Dashboards, games, and AI tools can be light, warm, editorial, clinical, playful, or neutral depending on the product.

## Reference Palette Challenge

When redesigning from a reference image:

- Ask whether the reference palette is a product/brand decision or just the common generated look. Dark surfaces, neon lime/cyan accents, purple/blue gradients, and black-glass cards need a reason beyond "it looked modern in the source."
- If the user did not explicitly request the original palette, create or at least evaluate a natural alternative: light, warm-neutral, editorial, clinical, sport/outdoor, brand-led, or platform-native.
- Keep dark mode only when it fits a clear context such as night use, OLED/battery preference, low-light gameplay, cinematic horror, tactical monitoring, or an existing brand token system.
- In redesign tasks, state the palette rationale before building. Example: "The source is dark neon, but this is a daytime running dashboard, so the redesign uses warm light surfaces, graphite text, sage progress, sky pace, and coral effort."
- Do not let a reference image's palette override the user's higher-level request to reduce the AI-generated look.

## Dark Theme

- Avoid pure black backgrounds with pure white text as the default reading surface; use dark grays and tuned content colors to reduce glare.
- Lower saturation for large dark-theme surfaces and reserve high-saturation accents for focused action or state change.
- Rebuild elevation with surface layers, borders, and subtle contrast. Do not copy light-theme shadows directly.
- Verify disabled, focus, selected, warning, and error states separately in dark mode.

## Component Color Rules

- Primary buttons use accent/primary fill only when they are the main action in that region. Text/icon contrast must pass.
- Every filled role (primary, accent, success, warning, danger) needs a verified on-color for the text/icon on top. Do not assume white: for mid-tone fills near-black text usually wins (it passes where white fails in roughly four out of five cases). Pick white or near-black by contrast and verify at least 4.5:1 (or 3:1 for large/bold button text). `scripts/export_tokens.py` emits these `on-*` tokens automatically and flags any below 4.5:1.
- Secondary buttons use outline, subtle fill, or neutral surface so they do not compete with primary actions.
- Destructive buttons use danger semantics and confirmation when the result is costly or irreversible.
- Disabled controls may be lower contrast but must still look intentionally unavailable. Explain why if the reason is not obvious.
- Panels and cards should usually be one or two surface steps away from the background, with border or elevation only when grouping needs it.
- Game HUD color should support quick recognition over busy gameplay. Do not depend on hue alone for health, ammo, cooldown, rarity, or warnings.

## Tooling

- For a fast, domain-based starting palette (with semantic roles already separated) and a type pairing, run `scripts/search_design_tokens.py "<domain> <mode>"`. It annotates each palette with real content-on-background contrast. Adapt the result; do not ship it unchanged.
- Verify any foreground/background pair with `scripts/check_ui_tokens.py --contrast "<fg>" "<bg>"` for a WCAG AA/AAA ratio.

## Validation

- Run contrast checks for text and non-text states.
- Compare light and dark theme screenshots side by side for preserved semantics.
- Check the UI in grayscale and colorblind simulation.
- Verify that focus, selected, warning, danger, and disabled states remain distinct when colors are removed.
- Ask: "Would this palette still make sense if the common AI purple/blue/dark trend disappeared?" If not, rebuild it from user intent.

## Sources

- W3C, WCAG 2.2, especially SC 1.4.3 and SC 1.4.11.
- Apple Human Interface Guidelines, Color and Dark Mode.
- Google Material Design / Material 3, color roles and state layers.
- Microsoft Fluent 2, Color and Accessibility.
- Elliot and Maier, "Color Psychology" (2014), DOI 10.1146/annurev-psych-010213-115035.
- Optional: any research the user supplies for their own project (treat as local grounding, not a bundled source).
