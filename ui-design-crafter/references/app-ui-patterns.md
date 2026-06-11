# App UI Patterns

Use this reference for product UI, admin tools, dashboards, mobile apps, websites, editors, and productivity surfaces.

## Layout

- Start with the user's main workflow and place the primary action near the point of decision.
- Prefer dense but breathable layouts for operational tools: sidebar or top navigation, persistent filters, clear tables/lists, and compact detail panels.
- Use full-width page bands or unframed layouts for major sections. Reserve cards for repeated records, contained tools, and modals.
- Keep scan paths predictable: navigation, page title, primary controls, filters, content, secondary details.
- On mobile, collapse sidebars into tabs, drawers, or bottom navigation only when the workflow remains obvious.
- Choose density by task, expertise, and repetition. Enterprise/productivity screens may carry more data; consumer screens should reduce entry cost and memory load.
- Do not shrink desktop UI into mobile. Re-prioritize information and actions for the smaller viewport.

## Navigation

- Use tabs for peer views within one context.
- Use side navigation for broad product areas.
- Use breadcrumbs only when hierarchy matters.
- Keep destructive or rare actions away from primary navigation and confirm them with clear copy.
- Use primary navigation for destinations, tabs for closely related peer sections, and toolbars for action groups.
- When a toolbar contains multiple actions, define keyboard behavior and overflow behavior instead of leaving it as visual decoration.

## Data And Forms

- Tables need sorting, filtering, empty states, loading states, row focus/hover, and readable numeric alignment.
- Forms need labels, helper/error text, required indicators where needed, disabled states, validation, and a clear save/cancel pattern.
- Dashboards need time range controls, comparison context, loading skeletons, and useful empty states.
- Avoid decorative metrics. Every chart or stat should support a decision.
- Prefer one main form column by default. Reduce fields, hide optional complexity, and place validation beside the affected field.
- Search and filters need visible scope, editable autocomplete, clear reset behavior, and useful defaults.
- Tables and grids need focus behavior, keyboard navigation, selected row state, and accessible headers.

## Visual Style

- Use color as hierarchy and meaning, not decoration.
- Keep primary actions visually distinct but not oversized inside dense panels.
- Use borders and subtle background shifts before heavy shadows.
- Use icon+label buttons for important commands and icon-only buttons for compact tool actions with tooltips.
- Use one primary action per region. Secondary actions should be quieter; destructive actions should be semantically distinct and protected when costly.
- Static screenshots are incomplete. Include empty, loading, error, success, disabled, focus, hover, and selected states.

## Responsive Behavior

- Define breakpoints by content needs, not device names.
- Convert multi-column grids to one or two columns before text becomes cramped.
- Keep toolbars wrapping cleanly or move overflow actions into a menu.
- Ensure modals fit small screens and remain scrollable without hiding primary actions.
- Reflow to 320 CSS px without losing content or requiring two-dimensional scrolling except where the content type makes it unavoidable.
- Verify touch target size and spacing separately from desktop pointer behavior.

## Mobile Gestures And Platform

- Every gesture needs a visible control too; gestures are accelerators, not the only path. Swipe-to-delete also needs a button/menu so screen-reader and one-handed users can reach the action.
- Common gestures and their rules: pull-to-refresh on feeds/lists (clear refreshing state, no accidental mid-scroll trigger); swipe actions on rows (labeled, color-coded, confirm or undo for destructive); long-press for context menus (with a non-gesture overflow equivalent); respect the iOS edge-swipe-back zone and do not bind app gestures there.
- Respect platform conventions instead of forcing one design on both:
  - Navigation: iOS uses a nav-bar back chevron plus edge-swipe; Android also honors the system Back (button or gesture). Handle Android system back explicitly - it should close a sheet/dialog or pop the stack, not drop the user out of the app.
  - Components: iOS leans on navigation bars, action sheets, and segmented controls; Android/Material leans on the app bar, bottom sheets, snackbars, and FAB. Match what users on that platform expect; do not ship an iOS clone on Android or vice versa.
  - System UI: respect status-bar style, the Android navigation bar, and safe-area insets; never hide system affordances behind your UI.
- Keep destructive and high-frequency actions out of the easiest accidental swipe/tap path, and test one-handed thumb reach.

## Mobile Input And Dynamic Type

- When the keyboard opens, keep the focused field and the primary action visible (scroll into view, or a sticky CTA above the keyboard); never let the keyboard cover the field being edited or the submit button.
- Use the right input type per field (email, number, tel, url, decimal), enable autofill/autocomplete, and set a sensible return-key action; let the input type handle formatting instead of forcing manual entry.
- Respect OS text-size settings (iOS Dynamic Type, Android font scale): size text in scalable units, let it grow, and verify the largest setting without clipping or overlap. This is distinct from translation expansion in `internationalization.md`.
- Support rotation and landscape when the content allows, and re-test safe areas in both orientations; do not block system zoom where content benefits from it.
- Preserve entered data and scroll position across rotation, backgrounding, and keyboard toggles; keep inline validation and error text visible above the keyboard.

## Landing And Marketing Pages

The default is to build the usable product, not a decorative marketing page. When a landing/marketing page is genuinely the goal, design it for comprehension and conversion, not flourish:

- Lead with one clear value proposition above the fold: what it is, who it is for, and the primary action - understandable in the first screen without scrolling.
- One dominant CTA, repeated down the page with the same label/action; secondary CTAs stay quiet. Never make the visitor hunt for the next step.
- Use a scannable section order, each section earning its place: hero -> proof (real logos/testimonials/metrics) -> key benefits -> deeper features -> pricing -> FAQ -> final CTA -> footer. Cut decorative filler sections.
- Benefits before features: lead with the user outcome, support with specifics. Use real copy and real numbers, never lorem or placeholder (see `ux-writing.md`).
- Social proof must be concrete (named testimonials, real logos, specific metrics), not vague badges.
- Hero imagery proves the product or context, not generic stock or gradient blobs (see `background-composition.md`); keep text legible over it.
- Stay accessible and responsive: heading order, real landmarks, keyboard/focus, contrast, and a mobile layout that reflows (not a shrunk desktop). Cookie/consent banners must not cover the primary CTA or core content.
- Judge it by the conversion path, not the visual flourish: can a first-time visitor understand the offer and reach the action in seconds?

## Web Performance

Treat speed and stability as design constraints, not an afterthought. Core Web Vitals are design decisions:

- LCP: the largest above-the-fold element (hero image/heading) must load fast; keep above-the-fold light and defer the rest.
- CLS: reserve space for every image, ad slot, embed, and async block (set width/height/aspect-ratio) so content does not jump as it loads - the top cause of layout shift.
- INP: interactions must respond quickly; do not block the main thread with heavy scripts.
- Fonts: limit families/weights, use `font-display: swap`, preload critical fonts, and fall back to a metric-compatible system stack to avoid invisible text (FOIT) and reflow (FOUT).
- Images: serve responsive sizes (`srcset`/`sizes`) and modern formats (WebP/AVIF), lazy-load below-the-fold, and never ship a desktop-sized hero to a phone.
- Make loading states (skeletons/placeholders) match the final layout so nothing reflows when content arrives (see `motion-and-feedback.md`).
- Verify on a mid-range device and a throttled network, not only a fast desktop; set a page budget and confirm the design survives slow connections.

## Monetization And Pricing

- Make the value and the price legible before the ask. Pricing pages need clear tiers, what each includes, billing period, currency, and the real total; highlight one recommended plan instead of making all tiers shout.
- Free trials and freemium: state when the trial ends, what is charged, and how to cancel, before the user commits. Send/Show a reminder before a trial converts.
- Upgrade prompts and usage limits should appear in context (when the user hits the limit), explain the benefit, and never block access to data the user already owns.
- Keep purchase and subscribe flows short, with an explicit confirm step, a visible total, and an easy, symmetric path to cancel or downgrade later.
- Translate prices, currencies, and tax/VAT correctly per locale (see `internationalization.md`).

### Ads and banner layout

- Give a banner ad its own reserved region; content ends above it, and the layout reflows when no ad is served (define the no-ad / collapsed state). The banner must not overlap content, bottom navigation, a sticky or primary CTA, the keyboard, or a floating action button.
- Respect the device safe area: a sticky banner and a sticky bottom bar/nav must stack, not cover each other, and neither should sit under the home indicator. Use `env(safe-area-inset-*)`. Re-test with the keyboard open and on short screens.
- Keep a gap between the banner and high-frequency controls so the ad cannot be mis-tapped; never place a tappable control flush against the ad edge.
- Use full-screen / interstitial ads only at natural break points (between tasks, never mid-input), with a real, labeled close (X) of at least 44px. Never use a fake or disguised close/system button (see dark patterns below).
- Keep consent/privacy surfaces for personalized ads clear and dismissible, and do not let them block the core task.

### Avoid dark patterns

Predatory monetization is the commercial cousin of the AI-generated look: it optimizes for the business at the user's expense. Do not ship:

- Confirmshaming ("No thanks, I hate saving money"), or making decline tiny, greyed, or hidden.
- Forced continuity: hard-to-find cancel, or making cancellation require support contact while signup is one click.
- Sneaking: pre-checked add-ons, hidden fees revealed at the last step, or drip pricing.
- Disguised ads or fake system/close buttons that trigger purchase or navigation.
- Nagging: repeated interruptive upsell modals that block the core task.
- Fake urgency/scarcity ("1 seat left", fake countdowns) that is not real.

Make the honest path the easy path: decline is as reachable as accept, cancel is as easy as subscribe, and the total cost is never a surprise.

## Validation

- Check whether a user can reach the main task with one glance and one obvious next action.
- Run keyboard walkthroughs for forms, dialogs, toolbars, tables, and grids.
- Confirm that loading skeletons, error messages, and empty states guide recovery rather than blame the user.

## Sources

- See `references/source-bibliography.md` for the standards and research behind these rules.
