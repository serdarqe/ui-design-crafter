# Internationalization, RTL, And Text Expansion

Use this when UI will ship in more than one language, in right-to-left scripts, or to a global audience. Designing for translation late is expensive; design for it from the first layout.

## Core Rules

- Never hardcode user-facing strings in layout logic. Treat every label, button, tooltip, and HUD string as translatable and variable-length.
- Layouts must survive text growing and shrinking. Do not size buttons, tabs, chips, or HUD labels to fit one language exactly.
- Mirror the whole interface for RTL (Arabic, Hebrew, Persian/Farsi, Urdu): layout direction, reading order, navigation, progress, back/forward, icons that imply direction.
- Keep numbers, dates, currency, units, and pluralization locale-aware, not string-concatenated.

## Text Expansion Budget

Translated text is often longer than English. Plan headroom:

- Short UI labels (1-2 words): allow +100% (a 6-char label can become 12+).
- Sentences/paragraphs: allow +30-40%.
- German, Russian, Finnish, and Turkish commonly run long; CJK can run shorter but taller.
- Let containers grow or wrap; avoid fixed widths and single-line truncation on critical labels. If truncation is unavoidable, keep the full value in a tooltip/title.
- Test the longest plausible string, not the placeholder.

## RTL And Bidi

- Use CSS logical properties so RTL mirrors automatically: `margin-inline-start/end`, `padding-inline-*`, `inset-inline-*`, `border-inline-*`, `text-align: start/end`, `float: inline-start`. Avoid `left/right`, `margin-left/right`, `padding-left/right` for layout.
- Set `dir="rtl"` (and `lang`) on the root; do not fake RTL by re-ordering DOM.
- Mirror directional icons (back/forward, next/prev, send, indent, progress, undo/redo, breadcrumbs, sliders). Do NOT mirror: clocks, media play, checkmarks, most logos, numbers, and content that is inherently LTR (code, phone numbers).
- Handle bidi text (an English brand inside an Arabic sentence) with proper isolation; do not let punctuation jump sides.
- Anchor primary actions to the reading-end correctly: in RTL the "forward/primary" affordance flips to the left.

## Scripts And Fonts

- Provide font fallbacks that cover the target scripts (Arabic, Cyrillic, CJK, Devanagari, Thai). A Latin-only display font will tofu or fall back inconsistently.
- CJK: avoid italics and faux-bold; respect line-break rules; vertical rhythm differs; small CJK text needs more size than Latin for legibility.
- Don't letter-space non-Latin scripts (it breaks Arabic joining and harms CJK).
- Keep line-height generous enough for tall scripts (diacritics, Thai, Devanagari).

## App vs Game Notes

- App: locale switcher, formatted numbers/dates/currency, pluralization, form validation messages, and email/notification templates all need translation and RTL. Tables and chart axes must reflow and right-align numerics by locale.
- Game: menus, HUD labels, tutorial text, item/skill names, and subtitles expand too. Reserve flexible space in fixed-format HUD; do not bake one language into a meter or counter. Subtitle systems need length limits, timing, and RTL support. Keep numerals and timers in a stable, locale-correct format.

## Testing

- Run pseudo-localization (accented, +40% length, bracketed strings) to expose clipping, concatenation, and untranslated strings before real translations exist.
- Test at least one RTL locale end-to-end: layout mirrors, icons flip correctly, text aligns to start, primary action lands on the right side.
- Verify the longest real translations on the smallest target viewport.
- Confirm numbers, dates, and currency render per locale, and that nothing relies on English word order.

## Sources

- W3C Internationalization (i18n) Activity; CSS Logical Properties and Values.
- Unicode Bidirectional Algorithm (UAX #9); CLDR for locale data, plurals, and formats.
- Apple HIG and Material Design localization/RTL guidance.
