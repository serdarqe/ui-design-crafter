# Accessibility (Structure, Keyboard, Screen Reader)

Use this for the parts of accessibility beyond color. Contrast, target size, RTL, and reduced motion are covered in `color-theory-for-ui.md`, `internationalization.md`, `motion-and-feedback.md`, and the `scripts/check_ui_tokens.py` checks; this file covers semantics, names, keyboard, focus, and screen-reader behavior. Accessibility is a build-time spec, not a final polish pass.

## Semantics First

- Use real elements for their behavior: `<button>` for actions, `<a href>` for navigation, real form controls, real headings in order (one h1, no skipped levels), and landmarks (header/nav/main/footer).
- ARIA only fills gaps native HTML cannot express. No ARIA is better than wrong ARIA; do not put `role="button"` on a div when a `<button>` works.
- Lists, tables, and tabs use the correct structures so assistive tech announces relationships (a table is a `<table>`, not a grid of divs).

## Accessible Names

- Every control, icon-only button, and meaningful image needs an accessible name: visible label, `aria-label`, `aria-labelledby`, or `alt`.
- Decorative images use `alt=""` (or `aria-hidden="true"`) so they are skipped. Informative images describe their meaning, not "image".
- The accessible name should match (or include) the visible label so voice control and screen readers agree.

## Keyboard And Focus

- Everything operable by pointer must be operable by keyboard, in a logical tab order. Do not rely on hover or drag alone - provide a button/keyboard alternative.
- Keep a visible focus indicator (>=3:1 against its surface); never remove `outline` without an equivalent `:focus-visible` style.
- Manage focus on change: move focus into a dialog/sheet when it opens, trap it there, and return it to the trigger on close. On route/view changes, move focus to the new heading.
- Avoid positive `tabindex`; offer a skip link for long headers; do not hijack standard keys.

## Screen Reader And Dynamic Content

- Announce asynchronous changes with live regions: `aria-live="polite"` for status/toasts/validation results, `role="alert"` for urgent errors. Do not spam announcements.
- Hide purely decorative or duplicated content from assistive tech with `aria-hidden="true"`; expose state with `aria-expanded`, `aria-selected`, `aria-checked`, `aria-current`, `aria-disabled` as appropriate.
- Forms: associate every input with a `<label>`, link errors and hints with `aria-describedby`, mark invalid fields with `aria-invalid`, and group related fields with `fieldset`/`legend`.

## Cognitive

- Use plain language and consistent patterns; reduce memory load (show choices, recent values, examples).
- Make errors forgiving: undo, confirm destructive actions, autosave, and avoid hard time limits where possible.
- Do not communicate meaning by color, sound, motion, or position alone (pair with text/icon/shape).

## Games

- Provide input remapping, hold-vs-toggle options, and alternatives to precise timing or rapid input.
- Offer subtitles/captions (with speaker and size options), colorblind modes, and a reduced-motion / reduced-flashing setting. Never flash more than three times per second (seizure risk).
- Keep critical HUD readable at the smallest target resolution and provide text-size options.

## Testing

- Keyboard-only pass: reach and operate everything, focus always visible, no traps (except intended modals), focus returns correctly.
- Screen-reader pass (NVDA/VoiceOver/TalkBack): names, roles, states, and dynamic updates are announced sensibly.
- Zoom to 200% and reflow to 320px without loss; test with reduced motion on.
- Combine automated checks (axe, Lighthouse, and `check_ui_tokens.py` for contrast / tap targets / RTL / reduced-motion / missing alt and accessible names) with manual review - automation catches at most ~30-40% of issues.

## Sources

- W3C WCAG 2.2 and WAI-ARIA Authoring Practices Guide (APG).
- Apple HIG Accessibility, Material Design Accessibility.
- Game Accessibility Guidelines; Xbox Accessibility Guidelines.
