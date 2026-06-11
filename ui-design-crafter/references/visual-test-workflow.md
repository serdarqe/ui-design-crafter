# Visual Test Workflow

Use this file after implementing or materially changing a UI. The goal is to collect evidence before calling the work complete.

## Required Evidence

Capture at least one mobile and one desktop viewport. For important app/game screens, use all standard viewports:

| Name | Size |
|---|---|
| mobile-small | 360x740 |
| mobile-common | 390x844 |
| mobile-large | 430x932 |
| mobile-small-landscape | 740x360 |
| mobile-common-landscape | 844x390 |
| mobile-large-landscape | 932x430 |
| tablet | 768x1024 |
| desktop | 1366x768 |

Minimum acceptable evidence for a small change:

- One mobile screenshot.
- One desktop screenshot.
- Browser metrics JSON or manual notes covering horizontal overflow, text clipping, primary CTA visibility, and frame/card stacking.

Do not mark a prototype complete when only the desktop viewport has been inspected.

## Store Screenshot Capture

When screenshots will feed App Store / Google Play / ASO assets, treat visual QA as a two-step process:

1. Capture raw product evidence with `references/store-capture-workflow.md`.
2. Run visual QA on the raw screenshots before any store composition, captions, frames, or backgrounds are added.

The raw capture set should include `manifest.raw.json` with source, screen name, platform, device/viewport, locale, theme, orientation, timestamp, and file path. Do not proceed to store composition when raw captures are fake, blank, clipped, debug-only, wrong-platform, or user-provided reference images rather than actual app/game evidence.

After composition with `scripts/export_store_screenshots.py`, inspect `manifest.store.json`. HTML-only outputs should be opened or rendered before claiming final visual quality. PNG outputs created with `--render playwright` can be passed to `scripts/visual_smoke_check.py` like any other screenshot folder.

## What To Check

- Horizontal overflow: `document.documentElement.scrollWidth` must not exceed `clientWidth`.
- Text fit: labels, buttons, tabs, HUD counters, mission cards, shop cards, and table cells must not clip or spill.
- Primary CTA: the main action must be visible in the initial viewport.
- Background: not blank, not hidden by full-screen darkness, still identifiable by theme, and not just one oversized panel/chart/board/boxed preview or split decorative side panel.
- Frame stacking: no framed container full of equally framed child buttons/cards.
- Card nesting: no card inside card unless it is a real repeated item or modal structure.
- Mobile safe area: bottom nav, CTA, hotbar, and HUD are not cut off by browser or device chrome.
- Mobile game ads: banner/MREC/rewarded/interstitial/store/consent regions are reserved, have collapsed/no-ad states, and do not cover board, playfield, timer, health, inventory, close/back controls, or primary CTA.
- Board/HUD balance: board, camera, or playfield remains the dominant surface; HUD/action bars do not cover playable cells, drag paths, target zones, or critical feedback.
- Stable dimensions: counters, cooldowns, price, owned/equipped, selected, and locked states do not shift layout.

## Scripted Smoke Check

After screenshots and metrics exist, run the script from the skill folder:

```bash
python scripts/visual_smoke_check.py --screenshots output/visual-qa --metrics output/visual-qa --strict
```

If you run it from elsewhere, point at your installed skill path, for example
`~/.claude/skills/ui-design-crafter/scripts/visual_smoke_check.py` (Claude) or
`~/.codex/skills/ui-design-crafter/scripts/visual_smoke_check.py` (Codex). On Windows use the
equivalent path under your user profile.

The script is a smoke alarm, not a designer. Passing it does not replace `visual-qa-checklist.md`, but failing it means the UI needs another pass.

## Browser / Playwright Metrics

Use Browser, Playwright, or the local browser automation available in the environment. Save one screenshot and one metrics JSON per viewport.

Example Playwright evaluation to run after navigating to the target page:

```javascript
async function collectVisualMetrics(page, viewportName) {
  const metrics = await page.evaluate((name) => {
    const root = document.documentElement;
    const body = document.body;

    const isVisible = (el) => {
      const rect = el.getBoundingClientRect();
      const style = window.getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 &&
        style.visibility !== "hidden" &&
        style.display !== "none" &&
        rect.bottom > 0 &&
        rect.right > 0 &&
        rect.top < window.innerHeight &&
        rect.left < window.innerWidth;
    };

    const textOverflow = [];
    const textNodes = Array.from(document.querySelectorAll("button, a, label, p, h1, h2, h3, h4, h5, h6, span, li, td, th, [role='button'], [data-ui]"));
    for (const el of textNodes) {
      const text = (el.textContent || "").trim();
      if (!text) continue;
      const rect = el.getBoundingClientRect();
      const style = window.getComputedStyle(el);
      const clipped = el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 1;
      const offscreen = rect.right > window.innerWidth + 1 || rect.left < -1 || rect.bottom > window.innerHeight + 1;
      const hiddenText = style.overflow === "hidden" && clipped;
      if (hiddenText || offscreen) {
        textOverflow.push({
          text: text.slice(0, 80),
          tag: el.tagName.toLowerCase(),
          className: String(el.className || "").slice(0, 120),
          rect: { x: rect.x, y: rect.y, width: rect.width, height: rect.height },
          scrollWidth: el.scrollWidth,
          clientWidth: el.clientWidth,
          scrollHeight: el.scrollHeight,
          clientHeight: el.clientHeight
        });
      }
    }

    const ctaSelectors = [
      "[data-primary-cta]",
      "[data-cta='primary']",
      ".primary",
      ".primary-button",
      ".cta",
      "button[type='submit']",
      "button"
    ];
    let primaryCtaVisible = false;
    for (const selector of ctaSelectors) {
      const el = document.querySelector(selector);
      if (el && isVisible(el)) {
        primaryCtaVisible = true;
        break;
      }
    }

    const frameStackCandidates = Array.from(document.querySelectorAll("*")).filter((el) => {
      const style = window.getComputedStyle(el);
      const rect = el.getBoundingClientRect();
      if (rect.width < 24 || rect.height < 24) return false;
      const hasBorder = ["borderTopWidth", "borderRightWidth", "borderBottomWidth", "borderLeftWidth"].some((prop) => parseFloat(style[prop]) >= 1);
      const hasShadow = style.boxShadow && style.boxShadow !== "none";
      const hasOutline = parseFloat(style.outlineWidth || "0") >= 1;
      return (hasBorder && hasShadow) || (hasBorder && hasOutline);
    }).length;

    const nestedCardCandidates = Array.from(document.querySelectorAll(".card .card, [class*='card'] [class*='card'], [class*='panel'] [class*='panel']")).length;

    const fixedBottom = Array.from(document.querySelectorAll("*")).filter((el) => {
      const style = window.getComputedStyle(el);
      const rect = el.getBoundingClientRect();
      return (style.position === "fixed" || style.position === "sticky") &&
        rect.bottom > window.innerHeight - 28 &&
        rect.height > 32;
    }).length;

    const overlaps = (a, b) =>
      a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top;

    const visibleRects = (selector) => Array.from(document.querySelectorAll(selector))
      .filter(isVisible)
      .map((el) => ({ el, rect: el.getBoundingClientRect() }));

    const collectCriticalAdOverlaps = () => {
      const ads = visibleRects("[data-ad-slot], [data-rewarded-ad], [data-store-prompt], .ad-slot, .banner-ad, .rewarded-ad");
      const critical = visibleRects("[data-playfield], [data-board], [data-primary-cta], [data-critical-ui], .game-board, .playfield, .hotbar, .hud, .primary");
      return ads.flatMap((ad) => critical.filter((item) => overlaps(ad.rect, item.rect)));
    };

    const collectBoardHudOverlaps = () => {
      const boards = visibleRects("[data-playfield], [data-board], .game-board, .playfield");
      const chrome = visibleRects("[data-hud], [data-action-bar], [data-ad-slot], .hud, .hotbar, .action-bar, .ad-slot");
      return boards.flatMap((board) => chrome.filter((item) => overlaps(board.rect, item.rect)));
    };

    return {
      name,
      viewport: { width: window.innerWidth, height: window.innerHeight },
      document: {
        scrollWidth: root.scrollWidth,
        clientWidth: root.clientWidth,
        scrollHeight: Math.max(root.scrollHeight, body ? body.scrollHeight : 0),
        clientHeight: root.clientHeight
      },
      horizontalOverflow: root.scrollWidth > root.clientWidth + 1,
      textOverflow,
      primaryCtaVisible,
      frameStackCandidates,
      nestedCardCandidates,
      safeAreaRisk: window.innerWidth <= 480 && fixedBottom > 0 && !CSS.supports("padding-bottom", "env(safe-area-inset-bottom)"),
      adOverlapCount: collectCriticalAdOverlaps().length,
      boardHudOverlapCount: collectBoardHudOverlaps().length
    };
  }, viewportName);
  return metrics;
}
```

Example Playwright loop:

```javascript
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const url = process.argv[2];
const outDir = process.argv[3] || "output/visual-qa";
const viewports = [
  ["mobile-small", 360, 740],
  ["mobile-common", 390, 844],
  ["mobile-large", 430, 932],
  ["mobile-small-landscape", 740, 360],
  ["mobile-common-landscape", 844, 390],
  ["mobile-large-landscape", 932, 430],
  ["tablet", 768, 1024],
  ["desktop", 1366, 768]
];

(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const results = [];
  for (const [name, width, height] of viewports) {
    await page.setViewportSize({ width, height });
    await page.goto(url, { waitUntil: "networkidle" });
    await page.screenshot({ path: path.join(outDir, `${name}.png`), fullPage: false });
    results.push(await collectVisualMetrics(page, name));
  }
  fs.writeFileSync(path.join(outDir, "visual-metrics.json"), JSON.stringify({ results }, null, 2));
  await browser.close();
})();
```

## Manual Screenshot Review

Open the screenshots side by side and check:

- Can the product/theme be identified without reading the title?
- Is the primary action obvious within five seconds?
- Does mobile show the real first screen, not cropped desktop UI?
- Are mission/shop/inventory cards readable with real names, prices, states, and counts?
- Do selected, locked, disabled, focus, warning, and danger states differ without generic gold/neon frames?
- Does the background remain visible and meaningful after overlays?
- Is the background a real environment/product/workflow context or deliberately clean app surface, not a single large panel behind the UI?
- Do left and right UI regions share one continuous backdrop instead of a decorative background card on one side and the real UI on the other?

## Failure Response

If the smoke script reports `fail`, fix before final delivery.

If it reports `warn`, inspect the screenshot and either fix it or explicitly note why the warning is acceptable.

If only manual screenshots are available, still document the checked viewports and the remaining risk. A visual UI task should not finish with no viewport evidence.
