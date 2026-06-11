# Smoke Tests

Run these from the repository root before publishing or rebuilding the skill.

## 1. Skill Validation

```powershell
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "ui-design-crafter"
```

Expected: `Skill is valid!`

## 2. Python Syntax

```powershell
python -m py_compile `
  "ui-design-crafter\scripts\check_store_assets.py" `
  "ui-design-crafter\scripts\check_ui_tokens.py" `
  "ui-design-crafter\scripts\export_store_screenshots.py" `
  "ui-design-crafter\scripts\export_tokens.py" `
  "ui-design-crafter\scripts\search_design_tokens.py" `
  "ui-design-crafter\scripts\search_reference_library.py" `
  "ui-design-crafter\scripts\visual_smoke_check.py"
```

Expected: no output and exit code `0`.

## 3. Token Search

```powershell
python "ui-design-crafter\scripts\search_design_tokens.py" "health mobile dashboard" --design-system --limit 3
```

Expected: one palette/type/style recommendation with contrast notes.

## 4. ASO Listing Validation

```powershell
python "ui-design-crafter\scripts\check_store_assets.py" `
  --platform google-play `
  --locale en-US `
  --title "CalmCare Health" `
  --short "Track habits and symptoms in one calm dashboard." `
  --full "Daily health notes and gentle reminders for your routine." `
  --json
```

Expected: `ok: true`.

Negative App Store keyword test:

```powershell
python "ui-design-crafter\scripts\check_store_assets.py" `
  --platform app-store `
  --locale en-US `
  --title "Health Tracker" `
  --subtitle "Daily Summary" `
  --keywords "health,tracker,health" `
  --json
```

Expected: `ok: false` with duplicate/repeated keyword findings.

## 5. Pillow PNG Fallback

Use any PNG screenshot you own:

```powershell
python "ui-design-crafter\scripts\export_store_screenshots.py" `
  --input "path\to\raw-screen.png" `
  --preset google-play-phone-app-portrait `
  --style no-caption/raw-compliant `
  --render pillow `
  --require-png `
  --out "reports\smoke-pillow"

python "ui-design-crafter\scripts\check_store_assets.py" `
  "reports\smoke-pillow\manifest.store.json" `
  --preset google-play-phone-app-portrait `
  --min-count 1 `
  --json
```

Expected: generated PNG is `1080x1920`, PNG has no alpha, and the only likely warning is Google Play requiring a larger final screenshot set.

## 6. Clean Build And Sync

```powershell
python "build-ui-design-crafter.py"
```

Expected:

- validation passes
- installed Codex/Claude copies sync
- `ui-design-crafter.zip` rebuilds
- no forbidden entries
- no missing/extra zip entries

