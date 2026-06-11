# Source Bibliography

Use this file when a UI decision needs research grounding, citation-ready rationale, or a stronger bridge between academic evidence, industry practice, and user outcomes.

## Source hierarchy

Prefer sources in this order:

1. Platform and accessibility standards: WCAG, WAI-ARIA APG, Apple HIG, Material Design, Fluent.
2. Peer-reviewed human factors and HCI research: Fitts, Hick-Hyman, cognitive load, Gestalt, affordance/signifier, perception.
3. Specialist UX research: NN/g, Baymard, game UX and accessibility references.
4. Competitor and reference-image analysis: use as inspiration and pattern evidence, not as proof.
5. Taste and trend references: useful for mood, but never enough to justify usability.

## Core sources

| Area | Source | Use for |
|---|---|---|
| Accessibility | W3C WCAG 2.2 | Contrast, non-text contrast, target size, focus visibility, keyboard access, error identification. |
| Interaction patterns | WAI-ARIA Authoring Practices Guide | Expected keyboard behavior and roles for tabs, dialogs, menus, comboboxes, sliders, tooltips, and widgets. |
| Platform conventions | Apple Human Interface Guidelines | iOS/macOS layout, touch targets, navigation, controls, motion, materials, and platform expectations. |
| Platform conventions | Material Design 3 | Android/web component behavior, color roles, type scale, motion, elevation, states, and adaptive layout. |
| Platform conventions | Microsoft Fluent 2 | Enterprise/productivity UI, command bars, panels, density, accessibility, and Windows-style interaction. |
| Usability heuristics | Jakob Nielsen, 10 Usability Heuristics | Visibility of system status, user control, consistency, error prevention, recognition over recall. |
| Cognitive load | John Sweller, Cognitive Load Theory | Reduce avoidable mental effort; chunk information; show only decision-relevant controls. |
| Choice complexity | Hick-Hyman Law | More visible choices slow decisions; group, prioritize, and progressively disclose options. |
| Target acquisition | Fitts's Law | Important and frequent targets should be large, near, and easy to hit. |
| Perceptual grouping | Gestalt psychology | Proximity, similarity, continuity, common region, closure, figure-ground, and visual hierarchy. |
| Affordance | Don Norman; Hartson | Make controls discoverable through signifiers, mapping, feedback, constraints, and conventions. |
| Information visualization | Colin Ware; Tufte | Visual hierarchy, preattentive attributes, data density, chart clarity, and avoiding decoration-as-data. |
| Color accessibility | Okabe and Ito color-universal design; WCAG | Avoid color-only status communication; pair hue with icon, label, shape, or position. |
| Commerce UX | Baymard Institute | Forms, checkout, product cards, filters, search, cart, onboarding, and ecommerce friction. |
| Game UI taxonomy | Fagerholt and Lorentzon, "Beyond the HUD" | Diegetic, spatial, meta, and non-diegetic game UI placement decisions. |
| Game UX | Celia Hodent, The Gamer's Brain | Attention, learning, feedback, onboarding, player psychology, and cognitive friction in games. |
| Game design | Jesse Schell, The Art of Game Design | Player goals, feedback loops, economy visibility, and interface decisions as part of game feel. |
| Game accessibility | Game Accessibility Guidelines; Xbox Accessibility Guidelines | Remapping, text size, contrast, subtitles, colorblind modes, reduced motion, timing flexibility. |
| User-provided research | Any document the user supplies for their project | Optional local grounding and synthesis; not bundled with the skill and not a substitute for the standards above. |

## How to apply sources

- Convert research into design constraints: "Because users scan dashboards under time pressure, make status and priority visible in the first pass."
- Use research to choose tradeoffs, not to decorate explanations. A source should change layout, state behavior, accessibility, or color decisions.
- Do not make exact quantitative claims unless the value is present in the checked source or platform guideline.
- For game UI, separate player cognition from visual style: a beautiful HUD still fails if it hides health, objective, ammunition, cooldown, or danger state at the wrong moment.
- For app UI, separate aesthetics from workflow efficiency: visual polish should reduce decision time, error rate, and confusion.

## Citation notes

When presenting a design rationale to a user, cite sources by title or institution in plain language. Example:

"I am using WCAG 2.2 for contrast and target-size checks, Fitts's Law for primary-action placement, and Material/Apple platform conventions for expected control behavior."

Do not paste long excerpts from source material. Summarize the principle and show how it affects the UI.
