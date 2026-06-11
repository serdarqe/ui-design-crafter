# Store Screenshot And ASO

Use this reference when designing, capturing, composing, or reviewing App Store / Google Play screenshots, feature graphics, or ASO presentation assets for apps and games.

Last checked: 2026-06-10.

## Source Rule

Store requirements change. Before generating final assets, check the official source for the target platform and update any preset data with a `last_checked` date.

Official sources checked for this phase:

- Apple App Store Connect Help, screenshot specifications: https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications
- Apple App Store Connect Help, upload app previews and screenshots: https://developer.apple.com/help/app-store-connect/manage-app-information/upload-app-previews-and-screenshots
- Apple App Store Connect Help, app information and metadata fields: https://developer.apple.com/help/app-store-connect/reference/app-information/
- Google Play Console Help, preview assets: https://support.google.com/googleplay/android-developer/answer/9866151
- Google Play Console Help, store listing metadata and descriptions: https://support.google.com/googleplay/android-developer/answer/9859152

Do not rely on memory, blog posts, or old templates for exact store dimensions.

## Core Principle

Store screenshots are evidence of the real product experience first, ASO presentation second. The skill may add caption, framing, background, and layout polish around real screenshots, but it must not invent features, fake gameplay, fake rankings, fake awards, fake sale urgency, or UI that the app/game does not actually contain.

For raw screenshot capture and `manifest.raw.json`, use `store-capture-workflow.md` before composing final store assets.

## Apple App Store Baseline

Checked on 2026-06-10:

- Screenshot upload count: minimum 1 and maximum 10 screenshots.
- Accepted screenshot formats: `.jpeg`, `.jpg`, `.png`.
- Use the highest required resolution when the UI is the same across device sizes and localizations; App Store Connect can scale down to smaller sizes.
- Specific screenshots and app previews for other device sizes/localizations can be added in Media Manager.
- For iOS apps, app previews may be portrait or landscape; app previews appear before screenshots.

Key iPhone screenshot size anchors from the official page:

| Device group | Portrait | Landscape | Note |
|---|---:|---:|---|
| iPhone 6.9 inch | 1260x2736, 1290x2796, or 1320x2868 | 2736x1260, 2796x1290, or 2868x1320 | Prefer as the current primary iPhone family when applicable. |
| iPhone 6.5 inch | 1284x2778 or 1242x2688 | 2778x1284 or 2688x1242 | Required if app runs on iPhone and 6.9 inch screenshots are not provided. |
| iPhone 6.3 inch | 1179x2556 or 1206x2622 | 2556x1179 or 2622x1206 | Scales from larger groups when accepted sizes are missing. |
| iPhone 6.1 inch | 1170x2532, 1125x2436, or 1080x2340 | 2532x1170, 2436x1125, or 2340x1080 | Scales from larger groups when accepted sizes are missing. |

Key iPad screenshot size anchors from the official page:

| Device group | Portrait | Landscape | Note |
|---|---:|---:|---|
| iPad 13 inch | 2064x2752 or 2048x2732 | 2752x2064 or 2732x2048 | Required if app runs on iPad. |
| iPad 12.9 inch | 2048x2732 | 2732x2048 | Scales from 13 inch when accepted sizes are missing. |
| iPad 11 inch | 1488x2266, 1668x2420, 1668x2388, or 1640x2360 | 2266x1488, 2420x1668, 2388x1668, or 2360x1640 | Use official page for the complete device mapping. |

Apple implementation notes:

- Keep each localization deliberate. If localized assets are missing, App Store product pages may use a next-best available language.
- If the project is on Windows, do not claim to capture iOS Simulator screenshots locally. Use user-provided iOS screenshots, a Mac/Xcode workflow, or generated store composition around verified screenshots.
- Do not hardcode the full Apple dimension table into prose. Phase 2 should store exact presets in `data/store-screenshot-presets.csv` with source URL and `last_checked`.

### App Store First Frames, App Previews, And PPO

- Treat the first 1-3 screenshots as the search-result selling surface. They must explain the product or gameplay without relying on the long description.
- App previews appear before screenshots, but they are not automatically better than a strong screenshot. Use a preview only when motion, timing, transformation, gameplay, or workflow speed is the real selling point.
- If an app preview is used, the first seconds must show recognizable product/game action, not a logo-only intro, cinematic fog, abstract mood, or delayed reveal.
- Build Product Page Optimization tests around one clear hypothesis and one visible variable at a time: first frame, screenshot order, caption angle, feature emphasis, or preview-vs-screenshot.
- Use custom product pages when a traffic source, campaign, region, or audience segment needs a different promise or first-frame emphasis.

## Google Play Baseline

Checked on 2026-06-10:

Feature graphic:

- Required for publishing a store listing.
- Format: JPEG or 24-bit PNG, no alpha.
- Size: 1024x500.
- Keep focal content centered and avoid cutoff zones.
- Localize graphic and branding text where appropriate.

Screenshots:

- Up to 8 screenshots per supported device type.
- Supported device types include phones, tablets, Chromebooks, Android TV, Wear OS, Android Automotive OS, and Android XR.
- Minimum requirement to publish: at least 2 screenshots across device types.
- Format: JPEG or 24-bit PNG, no alpha.
- Minimum dimension: 320px.
- Maximum dimension: 3840px.
- The maximum dimension cannot be more than twice the minimum dimension.

Large screen requirements/recommendations:

- For Chromebook and tablets, add at least 4 screenshots to demonstrate in-app experience.
- Upload screenshots between 1080px and 7680px.
- Use 16:9 for landscape and 9:16 for portrait.

Recommendation eligibility:

- Apps: at least 4 screenshots with minimum 1080px resolution; use 16:9 landscape with minimum 1920x1080 or 9:16 portrait with minimum 1080x1920.
- Games: at least 3 16:9 landscape screenshots with minimum 1920x1080 or 3 9:16 portrait screenshots with minimum 1080x1920.
- Game screenshots should depict in-game experience so users understand gameplay before downloading.

Google Play implementation notes:

- Screenshots must demonstrate the actual in-app or in-game experience.
- Use captured footage of the app/game itself. Do not show hands/fingers interacting with the device unless the core experience is off-device.
- Prioritize UI in the first three screenshots when using stylized multi-image screenshot sets.
- Taglines should be used only when necessary and should not take more than 20% of the image.
- Notification/status bar clutter should be removed before submission.
- Do not upload blurry, distorted, stretched, compressed, rotated, or pixelated images unless pixelation is intentional brand/game style.

### Google Play Thumbnail, Feature Graphic, Alt Text, And Video

- Design Google Play screenshots for thumbnail-level clarity. A user should understand the screen's purpose from small store surfaces before reading detail text.
- The feature graphic is a centered hero asset, not an empty banner. Keep the strongest subject, game moment, product object, or value cue near the center and away from cutoff zones.
- Avoid pure white, pure black, dark gray, and low-contrast empty fields in the feature graphic. Use the product/game palette, but preserve readable contrast at small sizes.
- Use at most one compact slogan or value line in a feature graphic, localized where needed. Do not rely on long copy, dense UI, tiny logos, or decorative background detail.
- Add Google Play alt text for every meaningful graphic asset when preparing handoff metadata. Keep it under 140 characters, describe the visible product/game value, and avoid generic prefixes such as `image of`, `photo of`, or `screenshot of`.
- If a Google Play preview video is part of the package, treat the first 10 seconds as the hook and the first 30 seconds as the practical autoplay window. Show real UI/gameplay quickly, make it understandable muted, and avoid ads, misleading cinematics, or unverified claims.

## Copy And Claim Risk

Avoid store text or image claims that suggest:

- Store performance, ranking, or category status: `Best`, `#1`, `Top`, `Million Downloads`.
- Awards or testimonials that are not verified.
- Price or promotion claims: `Free`, `Discount`, `Sale`, limited-time urgency.
- Direct CTA overlays: `Download now`, `Install now`, `Play now`, `Try now`.
- Keyword stuffing or unrelated words added for search.
- Time-sensitive claims that will become stale.
- Third-party trademarked characters, logos, store badges, or device imagery without permission.

Prefer:

- Clear feature/value labels tied to the actual screen.
- Concrete product outcomes: `Track every habit`, `Plan the next mission`, `Compare item stats`.
- Short localized captions that survive text expansion.
- Real gameplay/app UI as the visual proof.

## Store Listing Metadata

ASO is not complete until the visible listing text and hidden/search metadata have been checked alongside screenshots.

Baseline limits checked on 2026-06-10:

| Platform | Field | Limit |
|---|---|---:|
| App Store | Title/app name | 30 characters |
| App Store | Subtitle | 30 characters |
| App Store | Keywords | 100 characters including commas |
| App Store | Promotional text | 170 characters |
| App Store | Description | 4000 characters |
| Google Play | Title | 30 characters |
| Google Play | Short description | 80 characters |
| Google Play | Full description | 4000 characters |

Listing text rules:

- App Store keywords should be unique comma-separated terms, not phrases copied from the title/subtitle.
- Do not repeat title/subtitle words inside the App Store keyword field; those visible fields are already indexed.
- Do not use competitor brands, store brands, third-party marks, or protected product names unless the user has a verified legal/product reason.
- Do not stuff broad unrelated keywords into title, subtitle, short description, or full description.
- Localize listing text per locale. Do not assume the same keyword order, idiom, or title structure works across languages.
- Keep claims tied to real, visible product value. Avoid ranking, price, urgency, award, testimonial, medical, finance, or safety promises unless verified.

Validate listing metadata with the same QA script used for screenshots:

```powershell
python scripts/check_store_assets.py --platform app-store --locale en-US --title "CalmCare Health" --subtitle "Track symptoms gently" --keywords "wellness,habits,symptoms" --full "Daily health notes and gentle reminders..."
python scripts/check_store_assets.py --platform google-play --locale en-US --title "CalmCare Health" --short "Track habits and symptoms in one calm dashboard." --full "Daily health notes and gentle reminders..."
```

Use `--competitor-brand` to add product-specific blocked brands during audits:

```powershell
python scripts/check_store_assets.py --platform app-store --title "My App" --keywords "fitness,tracker" --competitor-brand "Fitbit"
```

## ASO Composition

Use this section when the user asks for store screenshots, ASO visuals, app listing images, Google Play screenshots, App Store screenshots, or a screenshot set for an app/game. The goal is a clear selling sequence built from real screens, not five unrelated decorative panels.

When studying competitor or reference screenshots, classify the source first: ASO education slide, live store page/search result, screenshot set example, or feature graphic. Use education slides for concepts, live store captures for thumbnail/product-page context, and screenshot sets for sequence/hierarchy analysis. Do not copy protected visuals, logos, claims, characters, device layouts, or color systems.

### Story Before Decoration

Every screenshot set needs one ordered story:

1. What is the product or fantasy?
2. What can the user/player do immediately?
3. What makes it different or valuable?
4. What keeps the user/player progressing?
5. What reduces doubt: trust, personalization, settings, social proof, collection, or depth?

If the first three images do not explain the actual experience without reading the long description, reorder the set before polishing visuals.

### App Screenshot Order

Default order for productivity, education, wellness, finance, SaaS, utility, lifestyle, and consumer apps:

| Position | Intent | Best source screen | Caption pattern |
|---:|---|---|---|
| 1 | Main value or outcome | Home, dashboard, completed result, before/after state | Verb + concrete outcome: `Plan your week`, `Track every habit` |
| 2 | Core workflow | Creation, search, scan, edit, lesson, transaction, booking | Action clarity: `Capture ideas fast`, `Review every task` |
| 3 | Differentiating feature | Smart view, comparison, insights, offline mode, collaboration | Specific benefit: `See patterns clearly` |
| 4 | Personalization or proof | Profile, progress, history, achievements, saved items | User-owned progress: `Build your streak` |
| 5 | Trust, control, or support | Settings, privacy, alerts, export, accessibility, plan controls | Reassurance: `Stay in control` |

For regulated, financial, health, children, or trust-sensitive apps, move trust/control earlier if it answers a real adoption concern. Do not imply certification, medical outcome, investment return, or child-safety guarantees unless verified.

### Game Screenshot Order

Default order for mobile, PC, and web games:

| Position | Intent | Best source screen | Caption pattern |
|---:|---|---|---|
| 1 | Real gameplay or core fantasy | Moment-to-moment gameplay, main encounter, puzzle board, race, combat | Fantasy + verb: `Survive the ward`, `Match under pressure` |
| 2 | Core mechanic | Drag, aim, merge, build, fight, solve, steer, rhythm, timing | Mechanic clarity: `Dash past danger` |
| 3 | Progression, upgrade, shop, or loadout | Character upgrade, inventory, shop, skill tree, mission rewards | Progress promise: `Upgrade your kit` |
| 4 | Variety, challenge, or event | Boss, level map, mission select, event, biome, enemy type | Content depth: `Face new threats` |
| 5 | Social, collection, or mastery | Leaderboard, collection, achievements, daily reward, skins | Long-term hook: `Collect rare gear` |

For hyper casual games, the first image should usually be an instantly readable gameplay state, not the main menu. For horror, tactical, simulation, or story games, show atmosphere through the real play space and UI, not by covering the screenshot with a poster-like background.

### Product-Type Sequences

Use these as quick defaults before adapting to the product:

| Product type | Recommended store sequence |
|---|---|
| Casual / hyper casual game | Hook or fantasy, core gameplay, progression, reward or unlock, event or variety |
| Midcore / RPG / strategy game | Hero moment, core loop, squad/build/loadout depth, PvP or social proof, seasonal/live-ops depth |
| Productivity / utility app | Main outcome, core workflow, speed or automation, personalization/history, trust/control |
| Education / language app | Learning outcome, lesson flow, practice or review, progress/streak, personalization or confidence |
| Wellness / finance / health-adjacent app | Safe value proposition, core tracking workflow, insights, privacy/control, reminders/support |

Do not force a sequence if the real product evidence says another order is clearer. The first three frames still carry the heaviest decision weight.

### Caption Rules

- Keep captions short: 2-6 words is the default target.
- Use one claim per screenshot.
- Tie every caption to the visible screen; if the user cannot point to the feature in the image, remove or rewrite the caption.
- Keep the UI screenshot as the evidence. Caption areas should support the screen, not hide the primary action, gameplay, board, map, HUD, form, or data.
- Reserve room for localization. Plan for roughly 30-100% text expansion depending on language and avoid hard-fitting captions to one line.
- Use sentence-style or title-style capitalization consistently. Do not use all caps for emphasis unless it is already part of the brand system.
- Prefer plain benefits over hype: `Review weak words` beats `Best vocabulary app`.
- Avoid tiny captions, thin type over busy imagery, and text on low-contrast backgrounds.

### Real UI Versus Promotional UI

Raw screenshots must come from the real app/game, a faithful prototype, an emulator/device capture, or user-provided screenshots. Store composition may add:

- Background color or scene extension that matches the product.
- Safe caption zone.
- Cropping and scale.
- Simple device-safe framing when allowed and useful.
- Sequence numbering in the manifest, not visible decorative numbers unless part of the design.

Store composition must not add:

- Features, modes, rewards, enemies, dashboard metrics, rankings, reviews, or outcomes that are not in the app/game.
- Fake interaction states that cannot happen.
- Generic device mockups or store badges with unclear license.
- Extra text, graphics, or backgrounds for device categories where the platform asks for interface-only screenshots.

### Layout Patterns

Choose the lowest-chrome pattern that still communicates the value:

- **Raw compliant:** screenshot only. Best for strict device categories, Wear OS-like surfaces, or when the UI itself is strong.
- **Full-bleed gameplay:** game screenshot fills the canvas; caption sits in a protected top/bottom safe zone or is omitted.
- **Top-caption:** caption above a centered screenshot; useful for app value screenshots.
- **Bottom-caption:** caption below the screenshot; useful when top UI carries the main evidence.
- **Split-caption:** caption and screenshot share the canvas; use only when the screenshot remains dominant and readable.
- **Clean-device-frame:** simple frame or rounded mask; avoid if it makes the image feel like a template or if the platform/category discourages device imagery.

Avoid using the same template for all positions. The sequence can repeat a consistent system, but each screenshot should have a distinct screen, intent, and visual rhythm.

### Composition Checklist

Before export, confirm:

- The first three screenshots show actual UI or gameplay and explain the core experience.
- The first three screenshots still read in a small contact sheet or store search-result thumbnail.
- The set has app-first or game-first ordering, not a random gallery.
- Captions are short, localized or localization-ready, and below the platform text-area risk.
- No caption claims ranking, price, awards, urgency, testimonials, or unverifiable outcomes.
- The main UI/gameplay area is not hidden by captions, device frames, glare, shadows, decorative panels, or background art.
- The platform, device group, orientation, and locale are explicit before asset export.
- Screenshots for tablets and large screens demonstrate the real large-screen layout, not just scaled phone UI.
- The final set can be understood without relying on tiny text inside the screenshot.

## Store Asset QA

After export, run the bundled QA script on the final PNG/JPG set or generated manifest:

```bash
python scripts/check_store_assets.py store-assets/google-play/manifest.store.json --min-count 2 --require-alt-text
python scripts/check_store_assets.py store-assets/app-store/ --preset app-store-iphone-6-9-portrait-a --strict
python scripts/check_store_assets.py store-assets/google-play/manifest.store.json --json --out store-assets/store-qa-report.json
```

The script checks:

- PNG/JPG format and unreadable image files.
- Exact width/height when a preset, manifest target, or custom `--width/--height` is supplied.
- App Store exact-size uncertainty when `--platform app-store` is used without a preset, manifest target size, or custom `--width/--height`.
- Google Play min/max dimensions, 2:1 screenshot aspect limit, 1024x500 feature graphic size, and no-alpha PNG requirement.
- File size, screenshot count, portrait/landscape mismatch, and manifest outputs that are still HTML-only.
- Caption word/character length, estimated caption area, risky ASO claims, and localization text-expansion risk.
- Google Play alt text presence when required, 140-character limit, generic alt-text prefixes, and risky claims inside alt text.
- Store listing title/subtitle/keywords/short/full/promotional-text limits, duplicate App Store keywords, repeated title/subtitle keyword terms, competitor-brand wording, risky claims, and missing locale metadata.

Treat any `fail` as a blocker before store upload. Inspect every `warn`; keep it only with an explicit reason, such as a platform-specific exception or verified localized layout.

For App Store delivery, presetless `--platform app-store` image checks intentionally fail. App Store screenshot sizes are exact accepted values, so pass `--preset`, `--width/--height`, or a manifest with target dimensions before calling the asset store-ready.

## ASO Experiment Loop

When the user asks for ASO optimization, do not only generate prettier assets. Run a measurable creative loop:

1. Establish the baseline: last 90 days of impressions, visitors, conversion, source, country/language, ratings/reviews, and downstream quality where available.
2. Audit competitors and category norms, but extract principles instead of copying layouts or claims.
3. Write one hypothesis for the next test: for example, `show gameplay first instead of menu first to improve install conversion for cold traffic`.
4. Change one main variable per experiment: first screenshot, order, caption angle, feature graphic, preview video, or audience-specific product page.
5. Build platform-specific variants. Do not reuse the same App Store and Google Play composition blindly.
6. QA every variant for dimensions, readability, claims, localization, alt text, and real-product evidence.
7. Run the appropriate store experiment path, such as Google Play Store Listing Experiments or App Store Product Page Optimization / custom product pages.
8. Judge results using conversion plus downstream quality signals when available: retained installers, trial starts, purchases, churn, session depth, or target in-app action.
9. Roll out the winner, localize intentionally, and document what was learned before creating the next variant.

## Platform And Screen-Type Separation

Keep these decisions separate before export:

- Platform: App Store, Google Play, both, or another store.
- Product type: app, game, hybrid app/game, kids app, regulated category.
- Device group: phone, tablet, large screen, watch, TV, XR, automotive.
- Orientation: portrait, landscape, or both.
- Asset type: raw screenshot, stylized screenshot, feature graphic, app preview poster frame.
- Locale: source language and target localizations.
- Capture source: web prototype, Android emulator, iOS device screenshot, user-provided screenshot, game build.

Do not reuse one generic screenshot set across all platform/device groups without checking the platform-specific constraints.

## Preset And Caption Data Lookup

For fast lookup, use the searchable data layer before choosing dimensions or caption sequence patterns:

```powershell
python scripts/search_design_tokens.py "Google Play phone portrait" --kind store-preset
python scripts/search_design_tokens.py "App Store iPhone 6.9 landscape" --kind store-preset
python scripts/search_design_tokens.py "horror mobile game screenshot 3 shop" --kind store-caption
```

Use `data/store-screenshot-presets.csv` for exact width, height, platform, orientation, requirement status, source URL, and `last_checked`. Use `data/store-caption-patterns.csv` for app/game/domain-specific caption intent and copy-risk guidance.

Treat preset rows as dated metadata, not permanent law. If final export depends on exact dimensions, re-check the official platform source and update `last_checked`.

## Store Screenshot Composer

After raw captures exist and the ASO sequence is decided, use `scripts/export_store_screenshots.py` to generate composed HTML assets and `manifest.store.json`.

Examples:

```powershell
python scripts/export_store_screenshots.py --input store-assets/raw/web/en-US/home-phone-portrait.png --preset google-play-phone-app-portrait --caption "Track every habit" --style top-caption
python scripts/export_store_screenshots.py --manifest store-assets/raw/manifest.raw.json --preset app-store-iphone-6-9-portrait-a --captions "Plan your week|Review every task" --style clean-device-frame
python scripts/export_store_screenshots.py --input store-assets/raw/gameplay.png --preset google-play-phone-game-landscape --caption "Survive the ward" --style full-bleed-gameplay --theme horror
```

Supported composition styles:

- `clean-device-frame`: simple CSS frame or mask around the screenshot; no bundled device mockup image.
- `full-bleed-gameplay`: screenshot fills the canvas; useful for games when gameplay evidence must dominate.
- `split-caption`: caption and screenshot share the canvas.
- `top-caption`: caption above screenshot.
- `bottom-caption`: caption below screenshot.
- `no-caption/raw-compliant`: screenshot-only composition.

The script always writes HTML and a manifest. Full CSS PNG raster output requires `--render playwright` and Node Playwright in the working environment. Browserless PNG output is available with `--render pillow` only for `--style no-caption/raw-compliant`; it fits the raw screenshot into the target size, flattens transparency, and writes a simple PNG without caption/device-frame styling. Do not fake a PNG-ready status when raster export failed.

### Optional PNG Render Setup

Install Playwright in the target project or workspace that will run `export_store_screenshots.py`:

```powershell
npm install -D playwright
npx playwright install chromium
```

Verify the browser can launch:

```powershell
node -e "const { chromium } = require('playwright'); chromium.launch({ headless: true }).then(async b => { console.log('chromium-ok'); await b.close(); });"
```

Then render PNGs:

```powershell
python scripts/export_store_screenshots.py --input store-assets/raw/home.png --preset google-play-phone-app-portrait --caption "Track every habit" --style top-caption --render playwright --require-png
```

For screenshot-only compliant PNGs, Pillow can be used without Node Playwright:

```powershell
python scripts/export_store_screenshots.py --input store-assets/raw/home.png --preset google-play-phone-app-portrait --style no-caption/raw-compliant --render pillow --require-png
```

Important:

- Install Playwright in the user's target workspace, not inside the skill package.
- Do not bundle `node_modules` or Playwright browser binaries into the skill zip.
- Pillow fallback is intentionally limited to `no-caption/raw-compliant`; captioned layouts and CSS frames need Playwright or another browser renderer.
- If the requested PNG renderer fails, the output is HTML-ready, not PNG-ready. Inspect `manifest.store.json` and the `render_status` field before delivery.

## Phase 0 Output Contract

When this reference is used in Phase 0 work, output:

- The official sources checked.
- The `last_checked` date.
- The platform and device groups in scope.
- The requirements that are mandatory.
- The recommendations that improve eligibility or ASO quality.
- The copy/claim risks that must be avoided.
- Any platform capture limitation, especially iOS capture on Windows.

## Phase 1 Output Contract

When this reference is used for ASO composition work, output:

- Target platform, product type, orientation, device group, and locale assumptions.
- A numbered screenshot sequence with intent, source screen, caption, and why that order matters.
- A short note confirming that every caption is tied to visible real UI/gameplay.
- Any policy or copy-risk edits made to avoid ranking, price, urgency, awards, testimonials, or direct CTA language.
- Any localization/text-expansion risk.

## Phase 2 Output Contract

When this reference is used for preset/data work, output:

- Which store preset query was run and which row(s) matched.
- Which caption pattern query was run and which pattern(s) matched.
- The platform/device/orientation assumptions before export.
- The source URL and `last_checked` date for selected presets.
- Any weak match or missing preset that needs manual source verification.

## Phase 4 Output Contract

When this reference is used for store composition work, output:

- Raw screenshot source or `manifest.raw.json` used.
- Selected preset, width, height, platform, orientation, source URL, and `last_checked`.
- Composition style, caption list, theme tokens, and output folder.
- `manifest.store.json` path.
- HTML output path(s), and PNG output path(s) only if PNG render actually succeeded.
- Any render limitation such as `playwright-render-unavailable`.
