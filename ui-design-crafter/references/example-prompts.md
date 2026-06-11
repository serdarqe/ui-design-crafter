# Example Prompts

Use this file when the user asks how to invoke, test, or pressure-test the skill. These prompts are intentionally specific so the skill has to apply research, components, states, color theory, accessibility, and reference analysis.

## App and product UI

```text
Use $ui-design-crafter to redesign this SaaS analytics dashboard. First inspect the existing components and tokens, then produce a dense but readable layout with tables, filters, metric cards, empty/error/loading states, accessible contrast, and responsive behavior.
```

```text
Use $ui-design-crafter to design a mobile onboarding flow for a habit app. Ground the design in cognitive load, recognition over recall, clear primary actions, touch targets, and friendly but not childish visual style.
```

```text
Use $ui-design-crafter to create a finance app color system. Include semantic roles, chart colors, red/green alternatives for accessibility, dark mode behavior, component states, and rules for alerts and risk indicators.
```

```text
Use $ui-design-crafter to review this settings screen for UI/UX quality. Find problems in hierarchy, grouping, labels, disabled states, focus, contrast, mobile text fit, and whether controls match their function.
```

```text
Use $ui-design-crafter to propose a color system and type pairing for a fintech dark dashboard. Start from scripts/search_design_tokens.py for accessibility-checked options, then adapt the roles to the brand and verify contrast on the real content with check_ui_tokens.py --contrast.
```

```text
Use $ui-design-crafter to bootstrap a full design system for a cozy farming sim mobile game. Run scripts/search_design_tokens.py "cozy farming sim mobile" --design-system to get a consolidated palette, type pairing, style direction, icons, and contrast verdicts, then adapt it and persist with --out design-system/MASTER.md before building screens.
```

## Game UI

```text
Use $ui-design-crafter to design a casual puzzle game HUD. Include board-safe layout, moves counter, goal tray, boosters, pause/settings, win/lose modals, reward states, touch target sizing, and readable effects during combos.
```

```text
Use $ui-design-crafter to design an RPG inventory and shop UI. Include item rarity, equipment slots, compare tooltip, sell/buy confirmation, stack counts, filters, controller/keyboard navigation, and empty/locked states.
```

```text
Use $ui-design-crafter to audit this FPS HUD for accessibility and gameplay clarity. Check health/ammo/objective placement, colorblind safety, low-health warnings, hit feedback, minimap readability, and reduced-motion alternatives.
```

## Reference analysis

```text
Use $ui-design-crafter to analyze the images in my reference-image folder for a sci-fi tactical game UI. Do not copy the images. Extract layout patterns, color roles, component ideas, HUD hierarchy, readability risks, and what to avoid.
```

```text
Use $ui-design-crafter to compare three reference styles for an education app: playful, calm premium, and productivity-focused. Choose the best direction for children aged 8-12 and explain the tradeoffs.
```

## Reduce the AI-generated look

```text
Use $ui-design-crafter to review this UI for an "AI-generated" feel. Find frame stacking, glow on everything, gradient soup, card-in-card, one-note palette, and equal-weight layout, then propose the specific fix for each using references/anti-patterns.md.
```

```text
Use $ui-design-crafter to redesign this game main menu. It currently looks like a generic fantasy UI kit: every item is an identical glowing rounded rectangle. Establish one dominant Play action, a real hierarchy, and theme through type and composition instead of repeated frames.
```

```text
Use $ui-design-crafter to make this dashboard feel designed, not generated. Remove decorative borders and shadows that do not carry meaning, build a neutral-plus-accent palette with semantic states, and prove hierarchy works from layout and type before any chrome.
```

```text
Use $ui-design-crafter to replace the generic dark purple/blue AI palette in this UI. Start from the user's brand, audience, product domain, content, and requested mood; only keep dark mode or cool blue/purple accents if they are justified by that context. Run check_ui_tokens.py afterward and explain the palette rationale.
```

## Store screenshots and ASO

```text
Use $ui-design-crafter to plan a Google Play screenshot set for this habit app. Read references/store-screenshot-aso.md, keep the first three screenshots focused on real UI, create a 5-image sequence with source screen, intent, caption, localization risk, and avoid any ranking, price, urgency, award, or download-now claims.
```

```text
Use $ui-design-crafter to create an App Store screenshot storyboard for this vocabulary app. Use real product screens only, order the set as value, workflow, differentiator, progress, and trust/control, then write 2-6 word captions that survive localization expansion.
```

```text
Use $ui-design-crafter to plan store screenshots for this mobile horror game. Make screenshot 1 real gameplay, screenshot 2 the core mechanic, screenshot 3 progression or shop, screenshot 4 mission/challenge variety, and screenshot 5 collection or mastery. Keep the composition theme-native without fake poster art covering gameplay.
```

```text
Use $ui-design-crafter to audit these store screenshots before export. Check platform fit, first-three UI/gameplay clarity, caption length, visible evidence for every claim, localization expansion, copy-risk words, device-frame risk, and whether any image invents a feature not present in the app/game.
```

## Implementation and QA

```text
Use $ui-design-crafter to implement this screen in the existing project. Reuse the current component library and tokens, define missing states, then run visual QA at desktop and mobile widths.
```

```text
Use $ui-design-crafter to create a component state matrix for this app. Cover buttons, icon buttons, tabs, panels, modals, forms, toasts, toolbars, and any game HUD controls. Include accessibility and responsive rules.
```

```text
Use $ui-design-crafter to run a final visual QA pass. Check overlap, text clipping, contrast, target size, focus-visible, loading/empty/error states, one-note palette risk, and whether the UI feels appropriate for the domain.
```
