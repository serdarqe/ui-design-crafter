# Store Capture Workflow

Use this reference when a store screenshot, ASO visual, App Store screenshot, Google Play screenshot, feature graphic input, or store-ready image set needs raw screenshots from a real app, game, prototype, emulator, device, or user-provided image set.

## Core Rule

Capture is evidence collection, not marketing composition. Get real screens first, then compose store assets later. Do not invent missing screens, gameplay, rewards, dashboards, rankings, or platform captures that were not actually produced.

If a requested capture path is unavailable in the current environment, say so and switch to the nearest honest source:

- Web/prototype URL available: capture with Browser or Playwright.
- Android build/emulator available: capture with ADB/emulator.
- iOS screenshots needed on Windows: ask for user-provided iOS screenshots or note that a Mac/Xcode workflow is required.
- Only static screenshots provided: analyze and manifest those files; do not pretend they came from a running app.

## Capture Decision Tree

1. Identify target store: App Store, Google Play, both, or unknown.
2. Identify product type: app, game, hybrid, kids, regulated, large-screen, watch, TV, XR, automotive.
3. Identify source: web prototype, Android emulator/device, iOS device/simulator, game build, desktop app, or user-provided screenshots.
4. Pick screens from the ASO story order in `store-screenshot-aso.md`.
5. Capture raw screenshots in platform-relevant viewports/devices before adding captions or frames.
6. Save every raw capture to a predictable folder and write `manifest.raw.json`.
7. Run visual QA on raw captures before store composition: wrong screen, clipped UI, broken assets, ad overlap, hidden HUD, or placeholder data should be fixed upstream.

## Screen List Selection

Use app/game intent to choose raw screens. Do not capture only the prettiest menu.

App screen candidates:

- Splash or launch only if it proves brand, loading quality, or onboarding start.
- Onboarding or first-run value screen.
- Home/dashboard/main value screen.
- Core workflow: create, scan, search, book, learn, edit, filter, checkout, or review.
- Differentiator: insight, compare, collaboration, offline, personalization, accessibility, or automation.
- Progress/history/profile.
- Settings, privacy, permissions, export, billing, or trust/control screen.
- Empty, loading, and error states only if they are part of the store story.

Game screen candidates:

- Real gameplay with HUD readable.
- Core mechanic moment: drag, aim, match, merge, build, fight, steer, rhythm, timing, solve.
- Mission/level select.
- Shop, upgrade, inventory, character, loadout, or skill tree.
- Boss/challenge/event/biome/enemy variety.
- Reward, collection, achievement, leaderboard, daily loop, or mastery screen.
- Main menu only if it is a strong fantasy signal; it should not replace gameplay-first evidence.

## Web And Prototype Capture

Use Browser or Playwright when the app/game runs at a local or external URL. Capture route by route, not one page after manual scrolling unless that is the actual store story.

Default viewport set:

| Name | Size | Use |
|---|---:|---|
| phone-portrait | 390x844 | Common mobile app/game portrait check. |
| phone-landscape | 844x390 | Mobile game landscape or rotated UI. |
| tablet-portrait | 768x1024 | Tablet app, shop, dashboard, mission map. |
| tablet-landscape | 1024x768 | Tablet game, dashboard, large-screen layout. |
| desktop | 1366x768 | Web app, dashboard, browser game, admin UI. |

For store export, replace generic viewports with preset-driven sizes from:

```powershell
python scripts/search_design_tokens.py "Google Play phone portrait" --kind store-preset
python scripts/search_design_tokens.py "App Store iPhone 6.9 portrait" --kind store-preset
```

Capture checklist:

- Wait for fonts, images, data, and gameplay canvas to settle before screenshot.
- Use deterministic seed/data if the game or dashboard is random.
- Disable dev overlays, inspector highlights, debug FPS counters, and temporary guides.
- Use real or realistic content; avoid lorem ipsum, fake metrics, and empty placeholders unless the empty state is the intended screen.
- Capture after consent modals, cookie banners, tutorial overlays, and ad placeholders are in the intended state.
- For games, verify canvas is nonblank and animated/gameplay state is actually visible.

Recommended raw output path:

```text
store-assets/raw/web/{locale}/{screen_name}-{viewport}.png
```

Playwright capture outline:

```javascript
const screens = [
  { name: "home", url: "/home" },
  { name: "workflow", url: "/create" },
  { name: "settings", url: "/settings" }
];
const viewports = [
  { name: "phone-portrait", width: 390, height: 844 },
  { name: "phone-landscape", width: 844, height: 390 },
  { name: "tablet-portrait", width: 768, height: 1024 },
  { name: "desktop", width: 1366, height: 768 }
];
```

Use the environment's available Browser/Playwright tool to implement the loop. Save one PNG per screen/viewport and include each file in `manifest.raw.json`.

## Android Capture

Use Android emulator or a physical device when the app/game is available as an APK, installed package, or Gradle project.

Pre-capture decisions:

- Device profile: phone, foldable, tablet, TV, automotive, or Wear OS.
- Orientation: portrait, landscape, or both.
- Locale: source locale plus requested localizations.
- Theme: light, dark, high contrast, seasonal, brand variant.
- Chrome: include or exclude status/nav bars. Store screenshots often need clean bars; document the choice in the manifest.
- State setup: logged in/out, tutorial complete, level unlocked, seeded save data, ad/no-ad state.

Common ADB capture flow:

```powershell
adb devices
adb shell monkey -p com.example.app -c android.intent.category.LAUNCHER 1
adb shell settings put system accelerometer_rotation 0
adb shell settings put system user_rotation 0
adb shell screencap -p /sdcard/store-home.png
adb pull /sdcard/store-home.png store-assets/raw/android/en-US/home-phone-portrait.png
```

Landscape rotation commonly uses `user_rotation 1`; exact behavior can vary by emulator/device. Verify orientation visually after capture.

Locale/theme examples:

```powershell
adb shell am force-stop com.example.app
adb shell am start -n com.example.app/.MainActivity
adb shell screencap -p /sdcard/store-dashboard-tr.png
```

Do not claim a locale/theme variant exists unless the running app was actually switched or the user provided that screenshot.

Android quality checklist:

- No system notifications, carrier text, debug toasts, crash dialogs, or permission prompts unless intentionally shown.
- Status/nav bars are either intentionally included and clean, or intentionally cropped later.
- Gameplay/HUD is not covered by ad placeholders, safe-area mistakes, or emulator controls.
- Store/consent/rewarded ad surfaces are in the intended state and not hiding the primary UI.
- Tablet screenshots show a real tablet layout, not a phone layout stretched to a large canvas.

Recommended raw output path:

```text
store-assets/raw/android/{locale}/{screen_name}-{device}-{orientation}-{theme}.png
```

## iOS Capture

On Windows, do not claim to run iOS Simulator capture locally. Use one of these honest paths:

- User-provided iPhone/iPad screenshots.
- Mac/Xcode workflow performed by the user or another machine.
- Existing TestFlight/App Store/device captures supplied as files.
- Web prototype captures clearly labeled as prototype, not native iOS simulator output.

When user-provided iOS screenshots are used:

- Preserve original files in a raw folder.
- Record device model or target preset if known.
- Record whether screenshots include status/home indicators.
- Check size against `store-screenshot-presets.csv` before composing final App Store assets.
- If size/device is unknown, mark `device` as `unknown-ios` and do not assert exact App Store compliance until verified.

Recommended raw output path:

```text
store-assets/raw/ios/{locale}/{screen_name}-{device}-{orientation}.png
```

Mac/Xcode handoff note:

```text
iOS capture requires a Mac/Xcode simulator or physical iOS device. In this Windows Codex environment, provide iOS screenshots or run the capture externally, then place the PNG/JPG files in store-assets/raw/ios/.
```

## User-Provided Screenshot Intake

When the user gives screenshots:

- Do not copy copyrighted reference images into the skill. Only analyze files the user provides in the project/task context.
- Keep raw screenshots separate from generated/composed assets.
- Rename only if the user asked for organization or if a manifest maps original filename to normalized filename.
- Record `original_filename`, `normalized_filename`, image size, source, and any uncertainty in `manifest.raw.json`.
- If screenshots are references rather than actual app/game captures, do not use them as store evidence. Extract patterns only.

## Raw Manifest Schema

Write `manifest.raw.json` next to raw captures. Minimum shape:

```json
{
  "version": 1,
  "created_at": "2026-06-10T00:00:00Z",
  "project": "example-app",
  "target_store": ["app-store", "google-play"],
  "captures": [
    {
      "id": "home-phone-portrait-en",
      "source": "web-prototype",
      "path": "store-assets/raw/web/en-US/home-phone-portrait.png",
      "original_filename": null,
      "screen_name": "home",
      "screen_role": "main-value",
      "platform": "web",
      "target_store": "google-play",
      "device": "phone",
      "viewport": {"name": "phone-portrait", "width": 390, "height": 844},
      "orientation": "portrait",
      "locale": "en-US",
      "theme": "light",
      "status_bar": "not-applicable",
      "nav_bar": "not-applicable",
      "timestamp": "2026-06-10T00:00:00Z",
      "notes": "Captured after dashboard data loaded."
    }
  ]
}
```

Required capture fields:

- `source`: `web-prototype`, `android-emulator`, `android-device`, `ios-user-provided`, `ios-mac-xcode`, `desktop-app`, `game-build`, or `user-provided`.
- `screen_name`: stable screen ID such as `home`, `gameplay`, `shop`, `mission-select`, `settings`.
- `platform`: `web`, `android`, `ios`, `desktop`, or `unknown`.
- `device` or `viewport`: include at least one.
- `locale`: BCP-47-style tag if known, such as `en-US` or `tr-TR`.
- `theme`: `light`, `dark`, genre theme, seasonal variant, or `default`.
- `timestamp`: ISO-8601 capture time.
- `path`: raw screenshot path.

Recommended capture fields:

- `target_store`, `screen_role`, `orientation`, `width`, `height`, `status_bar`, `nav_bar`, `original_filename`, `route`, `package_name`, `activity`, `build`, `commit`, `seed`, `warnings`.

## Naming Rules

Use lowercase, hyphenated names:

```text
{screen_name}-{device_or_viewport}-{orientation}-{locale}-{theme}.png
gameplay-phone-landscape-en-us-dark.png
shop-phone-portrait-tr-tr-default.png
dashboard-tablet-landscape-en-us-light.png
```

Keep original filenames in the manifest when normalizing user-provided files.

## Capture QA Before Store Composition

Before moving to store composition:

- Open the raw captures and confirm they show the intended screen.
- Check width/height and orientation.
- Check text fit, asset loading, and visual clarity.
- Confirm no debug UI, browser chrome, emulator frame, cursor, or tool overlay is visible unless intentionally part of the capture.
- Confirm gameplay captures show real gameplay, not a blank canvas, paused loading state, or unrelated menu.
- Confirm the manifest has every raw file and every raw file has a manifest row.
- Record any limitation honestly: `ios-not-captured-on-windows`, `user-provided-size-unknown`, `android-status-bar-included`, `prototype-not-native`.

## Phase 3 Output Contract

When using this reference for capture planning or execution, output:

- Capture source selected and why.
- Target screens and ASO role for each screen.
- Target platform, device/viewport, orientation, locale, and theme.
- Raw output folder path.
- `manifest.raw.json` fields or produced manifest location.
- Any platform limitation or manual user action needed.
- A short QA note confirming raw captures are real product/prototype evidence.
