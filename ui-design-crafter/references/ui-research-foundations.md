# UI Research Foundations

Use this reference to ground UI decisions in usability, perception, motor behavior, cognitive load, accessibility, and user mental models.

## Core Rules

- Build visual hierarchy around one dominant task focus. Do not create multiple equally loud primary targets in the same region.
- Use Gestalt principles through spacing, grouping, alignment, common region, similarity, and figure-ground contrast. Do not rely on decorative dividers to explain structure.
- Make affordance and signifiers visible. Clickable or tappable controls need recognizable shape, label, icon, state, or placement.
- Apply Fitts's Law by making frequent, risky, or time-critical targets larger, closer to the user's likely pointer/thumb/focus path, and separated from neighboring targets.
- Apply Hick's Law by reducing equal-weight choices at decision points. Group options, choose useful defaults, and use progressive disclosure for secondary choices.
- Reduce cognitive load by preferring recognition over recall: show selected values, recent choices, visible filters, examples, constraints, and inline help.
- Prevent errors before writing error messages. Use constraints, clear defaults, undo, confirmation for destructive actions, and recovery suggestions.
- Design for consistency. The same action must keep the same label, icon, color role, keyboard behavior, and state logic across the product.
- Match user language and mental models. Prefer domain terms users expect over internal system language.
- Treat accessibility as component behavior, not a final polish pass. Contrast, focus, target size, keyboard navigation, labels, and non-color cues are part of the spec.

## Practical Decision Model

When designing any screen, answer in order:

1. What is the user's primary decision or action?
2. What information must be seen before that action is safe?
3. Which controls are frequent, risky, or time-critical?
4. Which choices can be grouped, defaulted, delayed, or hidden?
5. What will the user recognize without remembering prior state?
6. What happens when the user is wrong, slow, colorblind, using keyboard/controller, or on a small screen?

## App And Game Differences

- App and dashboard UI can support higher density when users are trained, tasks repeat, and data comparison matters.
- Consumer app UI should lower entry cost, reduce memory demand, and make the next action obvious.
- Game UI must protect flow and attention. Critical information should be glanceable; detailed information can move to pauses, overlays, inventories, or menus.
- Touch, controller, keyboard, and mouse are not interchangeable. Layout, target size, focus order, and tooltips must follow the input model.

## Validation

- Run a five-second test: can a user identify the task, primary CTA, and current state quickly?
- Walk through the screen with keyboard, touch, controller, or mouse as appropriate.
- Check that the same task does not require both memory and precision under time pressure.
- Check that errors are prevented or recoverable with visible suggestions.
- Check WCAG contrast, focus visibility, and target-size expectations before completion.

## Sources

- John Sweller, "Cognitive load during problem solving" (1988), DOI 10.1016/0364-0213(88)90023-7.
- Wagemans et al., "A century of Gestalt psychology in visual perception" (2012), DOI 10.1037/a0029333.
- Rex Hartson, "Cognitive, physical, sensory, and functional affordances" (2003), DOI 10.1080/01449290310001592587.
- Nielsen Norman Group, "10 Usability Heuristics for User Interface Design."
- W3C, WCAG 2.2.
- Optional: any research the user supplies for their own project (treat as local grounding, not a bundled source).
