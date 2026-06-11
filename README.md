# UI Design Crafter

**UI Design Crafter** is a practical design skill for **Codex** and **Claude Code** that helps agents design, implement, review, and QA polished interfaces for apps, dashboards, tools, games, HUDs, menus, panels, and store listing assets.

It is not a component library, template pack, or Figma plugin.
It is a structured **UI design intelligence layer**: design rules, focused references, searchable data, and deterministic QA scripts.

The main goal is simple:

> Help AI produce UI that feels intentional, usable, themed, accessible, and production-ready instead of generic, over-framed, over-glowing "AI UI".

## Why This Exists

AI-generated UI often has recognizable problems:

- every panel has a heavy border
- every button has a glow
- every section looks like a card inside another card
- dark purple/blue palettes appear by default
- decorative gradients replace actual product context
- game HUDs cover the playfield
- dashboard screens look like landing pages
- horror, cozy, fantasy, SaaS, finance, health, and casual game themes all start to look the same
- App Store / Google Play screenshots look promotional but do not prove the real app experience

UI Design Crafter is built to fight those habits.

It gives the agent a repeatable process for:

- choosing a visual direction based on product, genre, audience, and platform
- building real usable screens before decorative mockups
- avoiding generic AI styling patterns
- validating accessibility and visual quality
- designing app/game store screenshots from real UI evidence
- checking ASO image and listing metadata before delivery

## Core Capabilities

### 1. App, Dashboard, And Tool UI Design

The skill supports practical UI work for:

- SaaS dashboards
- admin panels
- productivity tools
- mobile apps
- forms and settings screens
- onboarding
- tables, filters, cards, dialogs, and navigation systems
- responsive layouts
- design-system-driven screens

It encourages dense but readable operational UI when appropriate, instead of turning every app into a marketing landing page.

### 2. Game UI, HUDs, Menus, Shops, And Mission Screens

The skill includes focused game UI guidance for:

- main menus
- pause menus
- HUDs
- bottom action bars
- inventory screens
- shops
- mission selection
- level selection
- rewards
- loadouts
- mobile safe areas
- ad banner placement
- touch zones
- playfield protection

A key rule is that the playable space remains dominant. UI should support the game, not cover it.

### 3. Anti-AI UI Rules

UI Design Crafter explicitly targets common "AI-generated UI" patterns.

It tells the agent to avoid:

- frame stacking
- glow-on-everything
- gold/yellow borders without meaning
- generic dark-purple or dark-blue themes
- one-note palettes
- oversized fake background panels
- decorative cards inside cards
- meaningless gradients and blur
- excessive chrome around every control
- fake dashboard data or fake game features
- store screenshots that hide the real product

Instead, it pushes toward:

- theme-native materials
- clear hierarchy
- restrained borders
- semantic color roles
- real product/game context
- continuous backgrounds where appropriate
- visual systems that fit the domain
- accessibility and text-fit checks

### 4. Theme-Aware UI Direction

The skill includes reference material for many app and game directions, including:

- horror
- hyper casual
- cozy
- fantasy
- sci-fi
- racing
- sports
- strategy
- historical / period UI
- kids UI
- luxury
- SaaS
- finance
- healthcare / wellness
- consumer mobile apps
- education
- ecommerce
- productivity tools

It does not use one universal style for every product.
The design should come from the product, audience, genre, mood, platform, and user task.

### 5. Background And Scene Composition Guidance

The skill treats backgrounds as part of the product or game world, not filler.

It discourages:

- random gradient backgrounds
- abstract blobs
- fake scene panels
- split left/right background fragments
- simplified UI copies behind the real UI
- dark fog as a substitute for actual context

It encourages:

- concrete theme-native locations
- real product context
- game-world environments
- lighting that supports hierarchy
- legibility overlays only when needed
- continuous background fields behind UI regions

For example:

- a horror game menu can use a morgue corridor, basement, archive room, or hospital ward atmosphere
- a healthcare dashboard can use calm clinical surfaces and soft daylight, not neon cyberpunk
- a SaaS admin screen should feel operational and restrained, not like a hero landing page

### 6. Accessibility And Visual QA

The skill includes accessibility and quality checks for:

- contrast
- focus states
- touch targets
- text overflow
- clipping
- horizontal scrolling
- missing alt text
- icon-only buttons
- reduced motion
- RTL and localization expansion
- frame/card stacking
- over-dark screenshots
- blank screenshots
- hidden primary actions

It includes scripts that can be run on real code, screenshots, or store assets.

## Store Screenshot And ASO Support

UI Design Crafter includes a complete workflow for App Store and Google Play visual assets.

It supports:

- App Store screenshots
- Google Play screenshots
- Google Play feature graphics
- screenshot sequencing
- caption rules
- real UI evidence checks
- Google Play alt text metadata
- store image dimension validation
- PNG/JPG format validation
- alpha/transparency checks
- App Store exact-size validation
- Google Play min/max/aspect-ratio validation
- ASO-safe caption review
- store listing text checks

The store workflow is intentionally strict:

1. design or verify the real app/game UI first
2. capture or organize raw screenshots
3. compose store-ready assets
4. validate dimensions, captions, alt text, and listing metadata
5. only then call the package ready

The skill avoids fake store visuals. It should not invent gameplay, features, rewards, metrics, claims, testimonials, rankings, or UI states that do not exist in the product.

## ASO Listing Metadata Validation

The included validator can check listing text fields such as:

### App Store

- title / app name
- subtitle
- keywords
- promotional text
- full description

### Google Play

- title
- short description
- full description

It checks:

- character limits
- duplicate App Store keywords
- keyword repetition between title/subtitle and keyword field
- risky ASO claims
- direct install/download CTA language
- third-party/store brand wording
- explicitly blocked competitor brands
- missing locale metadata

This helps move the skill from "screenshot composer" toward a more complete ASO QA workflow.

## Included Tools

Run tools from inside the `ui-design-crafter/` folder.

| Script | Purpose |
|---|---|
| `scripts/search_design_tokens.py` | Search curated palettes, type pairings, icon names, style domains, motion presets, store presets, and ASO caption patterns. |
| `scripts/check_ui_tokens.py` | Audit UI code for contrast, token usage, frame stacking, missing accessibility cues, risky styling, and common AI-look issues. |
| `scripts/visual_smoke_check.py` | Review screenshots and browser metrics for blank screens, overflow, clipping, hidden CTA, over-dark UI, and visual QA issues. |
| `scripts/export_tokens.py` | Export curated palettes into CSS variables, Tailwind config fragments, or W3C DTCG-style token JSON. |
| `scripts/export_store_screenshots.py` | Compose raw app/game screenshots into store-ready HTML assets and optional PNG outputs. |
| `scripts/check_store_assets.py` | Validate App Store / Google Play screenshots, feature graphics, captions, alt text, dimensions, alpha, and listing metadata. |
| `scripts/search_reference_library.py` | Search your own reference image library using a manifest CSV. No reference images are bundled. |

## Searchable Design Data

The skill includes curated metadata for:

- color palettes
- type pairings
- icon names
- style domains
- motion presets
- query aliases
- store screenshot presets
- ASO caption patterns
- store listing limits

This data is meant as a starting point, not a fixed design kit.

For example:

```bash
python scripts/search_design_tokens.py "health mobile dashboard" --design-system
python scripts/search_design_tokens.py "horror mobile game mission screen" --design-system
python scripts/search_design_tokens.py "Google Play phone portrait" --kind store-preset
python scripts/search_design_tokens.py "horror game screenshot 3 shop" --kind store-caption
```

## Installation

Copy the `ui-design-crafter/` folder into your skills directory.

### Claude Code

```bash
~/.claude/skills/ui-design-crafter/
```

### Codex

```bash
~/.codex/skills/ui-design-crafter/
```

On Windows:

```text
%USERPROFILE%\.claude\skills\ui-design-crafter\
%USERPROFILE%\.codex\skills\ui-design-crafter\
```

## Quick Start

### Design A Product UI

```text
Use $ui-design-crafter to redesign this health dashboard.
Make it calm, readable, mobile-first, accessible, and avoid generic dark AI styling.
```

### Design A Game Menu

```text
Use $ui-design-crafter to design a horror mobile game main menu and mission select screen.
Protect safe areas, keep the background theme-native, avoid yellow/gold card borders, and include visual QA.
```

### Search A Design Direction

```bash
python scripts/search_design_tokens.py "cozy farming sim mobile" --design-system
```

### Check UI Code

```bash
python scripts/check_ui_tokens.py src/ --strict
```

### Export Store Screenshots

```bash
python scripts/export_store_screenshots.py \
  --input raw/home.png \
  --preset google-play-phone-app-portrait \
  --caption "Track every habit"
```

### Browserless PNG Fallback

For screenshot-only compliant assets:

```bash
python scripts/export_store_screenshots.py \
  --input raw/home.png \
  --preset google-play-phone-app-portrait \
  --style no-caption/raw-compliant \
  --render pillow \
  --require-png
```

### Validate Store Assets

```bash
python scripts/check_store_assets.py store-assets/google-play/manifest.store.json --min-count 2
```

### Validate Store Listing Metadata

```bash
python scripts/check_store_assets.py \
  --platform google-play \
  --locale en-US \
  --title "CalmCare Health" \
  --short "Track habits and symptoms in one calm dashboard." \
  --full "Daily health notes and gentle reminders for your routine."
```

## Optional PNG Rendering

The store screenshot exporter always writes HTML and `manifest.store.json`.

PNG output can be produced in two ways:

### 1. Playwright Rendering

Best for full CSS compositions with captions, frames, and layout styling.

```bash
npm install -D playwright
npx playwright install chromium
```

Then:

```bash
python scripts/export_store_screenshots.py \
  --input raw/home.png \
  --preset google-play-phone-app-portrait \
  --caption "Track every habit" \
  --render playwright \
  --require-png
```

### 2. Pillow Rendering

Best for simple screenshot-only compliant outputs.

```bash
python scripts/export_store_screenshots.py \
  --input raw/home.png \
  --preset google-play-phone-app-portrait \
  --style no-caption/raw-compliant \
  --render pillow \
  --require-png
```

Pillow fallback is intentionally limited. Captioned layouts and CSS/device-frame compositions still need Playwright or another browser renderer.

## What This Skill Does Not Do

UI Design Crafter does not:

- bundle copyrighted reference images
- bundle fonts
- bundle Lucide SVG files
- bundle Playwright browsers or `node_modules`
- replace a real design system
- guarantee App Store / Google Play approval
- make unverified ASO claims true
- capture iOS Simulator screenshots on Windows
- invent app/game features that do not exist

It helps an AI agent make better design decisions and validate outputs more carefully.

## Licensing And Data Notes

- Code and documentation are MIT licensed.
- No fonts or images are bundled.
- `data/icons.csv` references Lucide icon names only. Lucide is ISC licensed.
- `data/type-pairings.csv` references font family names only. Each font remains under its own license.
- Color palettes are original metadata.
- Reference-image search is bring-your-own: use images you own or have permission to analyze.
- Store platform rules change. Re-check official Apple and Google Play sources before final production uploads.

## Public Release Checks

Before publishing or updating, run:

```bash
python build-ui-design-crafter.py
```

And see:

```text
smoke-tests.md
```

Recommended checks include:

- skill validation
- Python syntax compile
- design token search
- ASO listing validation
- negative App Store keyword test
- Pillow PNG fallback test
- clean build and sync

## Philosophy

Good UI is not just decoration.

It is:

- hierarchy
- rhythm
- readable text
- state clarity
- accessible interaction
- theme-native material
- believable product context
- restraint where restraint helps
- expression where expression serves the product

UI Design Crafter exists to help AI agents remember that.
