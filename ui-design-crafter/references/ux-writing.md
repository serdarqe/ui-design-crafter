# UX Writing And Microcopy

Use this when writing any user-facing text: buttons, labels, headings, helper text, errors, empty states, tooltips, toasts, onboarding, and in-game UI strings. Bad copy is a top "AI-generated" tell - placeholder text, vague buttons, blaming errors. Words are part of the interface.

## Core Rules

- Lead with the user's goal in their language, not the system's. Prefer the term the user expects over internal jargon.
- Be specific and brief: cut filler, front-load the point, one idea per line. Shorter is better only if it stays clear.
- Do not explain the obvious or narrate the UI (no "Click the button below to continue"). Reserve text for genuine constraints, examples, and recovery.
- Be consistent: the same action keeps the same word everywhere. Keep a tiny glossary so one thing is not called three names.

## Buttons And Labels

- Buttons are verbs that name the outcome: "Save changes", "Delete account", "Start review" - not "OK", "Submit", "Yes", or "Click here".
- The button label should match the heading/action it completes (a "Delete file?" dialog confirms with "Delete", not "OK").
- Use sentence case for UI text by default ("Daily goal", not "Daily Goal"); pick one case convention and keep it.
- Labels describe the field's content ("Email address"), not instructions ("Enter your email"). Use placeholder text for examples, never as the only label.

## Errors, Empty, And Confirmation

- Error messages say what happened and how to fix it, without blame or raw codes: "That email is already in use - try signing in" beats "Error 409". Put the message next to the field it affects.
- Prevent first: constraints, defaults, examples, and inline validation reduce the need for error copy.
- Empty states explain what goes here and give one clear next action ("No words due - come back tomorrow, or learn 5 new ones"), not just "No data".
- Destructive confirmations name the object and the consequence ("Delete 'Trip notes'? This cannot be undone"), and label the action with the verb.

## Tone, Numbers, And Locale

- Match tone to domain and audience: calm and precise for finance/medical, warm and simple for kids/learning, in-world voice for game narrative - but keep functional UI (objectives, settings, store, errors) plain and scannable even in a stylized game.
- Format numbers, dates, currency, and units by locale, and pluralize properly ("1 day" / "2 days"); humanize when useful ("2 days ago") but show exact values when precision matters. See `internationalization.md`.
- Write for translation: avoid idioms and concatenated sentence fragments; leave room for text to grow.

## Accessibility Of Copy

- Link and button text must make sense out of context (a screen reader may read them alone) - avoid "here"/"read more"; the visible label is the accessible name.
- Keep reading level reasonable; expand unfamiliar abbreviations on first use.
- Loading and status messages should state progress, not just spin ("Saving..." / "Saved").

## Game-Specific

- Separate flavor from function: narrative, item lore, and barks can have voice; tutorials, objectives, HUD labels, store, and settings stay clear and consistent.
- Keep tutorial text short and action-led ("Drag a block to move it"), tied to what is on screen; do not wall-of-text a mechanic that a single prompt can teach.
- Use a consistent term set for mechanics, currencies, and pieces across menus, shop, tooltips, and HUD.

## Validation

- Read each string aloud: does it help the user decide or act? If not, cut or rewrite it.
- Check consistency: same action = same verb; same object = same noun, everywhere.
- Test with the longest realistic translation and with empty/loading/error states present.
- Confirm link/button text is meaningful on its own.

## Sources

- Nielsen Norman Group, writing for the web and UX writing guidelines.
- Apple HIG "Writing" and Material Design "Writing" guidance.
- Plain language principles (plainlanguage.gov); WCAG 2.2 (meaningful link text, labels).
