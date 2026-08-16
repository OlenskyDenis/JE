# Quickstart & Verification Guide: Settings Menu Configuration

**Feature Branch**: `026-settings-menu-config`  
**Spec**: [specs/026-settings-menu-config/spec.md](spec.md)  
**Date**: 2026-08-16

---

## 1. Automated Verification (Pytest)

Run all unit tests, including new test cases for `SettingsService`, delimiter customization, and Excel default data type handling:

```bash
python -m pytest tests/unit/test_settings_service.py
python -m pytest
```

Expected: All unit and integration tests pass with 0 failures.

---

## 2. Manual Verification Checklist

### Test Scenario 1: Changing Delimiter and Live Tree Update
1. Launch the application:
   ```bash
   python -m src.app.main
   ```
2. Create or import a multi-level tree (e.g. `Root \ Folder \ Item`).
3. Click the **Settings (⚙)** button in the top toolbar.
4. Change the path delimiter to `/` and click **"Save Settings"**.
5. **Verify**:
   - Node badges in the tree canvas immediately update to `Root/Folder/Item`.
   - The **Preview (Попередній перегляд)** tab cards display `/` as separator.
   - Refreshing the browser or restarting the app keeps `/` active.

### Test Scenario 2: Excel Import with Custom Default Data Type
1. Open Settings and change the default column data type to **"Decimal"**.
2. Save settings.
3. Import an Excel spreadsheet containing unformatted/General columns.
4. **Verify**:
   - Unformatted leaf nodes are assigned the **Decimal** (`0.00`) data type badge instead of Text.
   - Explicitly formatted columns (such as Date or Currency) retain their specific types.

### Test Scenario 3: Resetting to Defaults
1. Open Settings.
2. Click **"Reset to Defaults"**.
3. **Verify**:
   - Delimiter resets to `\`.
   - Default data type resets to `Text`.
   - Tree path badges immediately revert to backslash `\`.
   - LocalStorage and `settings.json` reflect the default configuration.

### Test Scenario 4: Multilingual Translation
1. Switch language between **UA** and **EN**.
2. Open Settings modal in both languages.
3. **Verify**: All titles, labels, options, placeholders, help texts, and toast messages are accurately localized without raw translation keys.
