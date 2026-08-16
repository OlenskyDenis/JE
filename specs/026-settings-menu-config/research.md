# Research & Architecture Analysis: Settings Menu Configuration

**Feature Branch**: `026-settings-menu-config`  
**Spec**: [specs/026-settings-menu-config/spec.md](spec.md)  
**Date**: 2026-08-16

---

## 1. Baseline Architecture Analysis

### Current Delimiter Behavior
- **`HierarchyNode.get_absolute_path()`**:
  ```python
  def get_absolute_path(self) -> str:
      if self.parent is None:
          return self.name
      parent_path = self.parent.get_absolute_path()
      return f"{parent_path}\\{self.name}"
  ```
  Hardcoded backslash `\` delimiter prevents users from formatting paths for Unix/Linux style systems (`/`), nested namespaces (`::`), or database schema representations (`.`).

- **`PathParserService.parse_header_paths()`**:
  ```python
  segments = [seg.strip() for seg in path_str.split("\\") if seg.strip()]
  ```
  Hardcoded `.split("\\")` fails when importing headers exported or created with non-backslash delimiters.

### Current Excel Default Data Type Behavior
- **`ExcelHierarchyAdapter._map_format_to_data_type()`**:
  ```python
  num_fmt = (number_format or "").strip().lower()
  if not num_fmt or num_fmt in ("@", "general"):
      if data_type_flag == "d":
          return "Date"
      return "Text"
  ```
  Hardcoded `"Text"` fallback prevents users who primarily work with numeric or float datasets from defaulting unassigned Excel columns to `"Integer"` or `"Decimal"`.

---

## 2. Technical Decisions & Solution Design

### Decision 1: Centralized Settings Manager (`SettingsService`)
- Create `src/hierarchy_lib/services/settings_service.py` responsible for:
  - Loading settings from `settings.json` in project root or returning default configuration.
  - Validating delimiter (1–3 characters, non-empty, stripped).
  - Validating default data type against `HierarchyNode.VALID_DATA_TYPES`.
  - Persisting settings to disk atomically.
  - Default values:
    ```json
    {
      "delimiter": "\\",
      "default_data_type": "Text"
    }
    ```

### Decision 2: Delimiter Propagation Across Domain Model
- Pass `delimiter: Optional[str] = None` to `HierarchyNode.get_absolute_path(delimiter)` and `to_dict(delimiter)`.
- If `delimiter` is omitted, fallback to `SettingsService.get_delimiter()`.
- Update `PathParserService.parse_header_paths(paths, delimiter=None)` to split segments using the active delimiter.
- Update `PathGenerator.calculate_path(component, delimiter=None)` and `calculate_all_paths(forest, delimiter=None)`.

### Decision 3: Excel Adapter Default Type Injection
- Update `ExcelHierarchyAdapter._map_format_to_data_type()` to accept `default_data_type: str = "Text"`.
- Propagate `default_data_type` and `delimiter` into:
  - `read_row1_headers_and_types()`
  - `import_from_file()`
  - `import_excel_file()` in `eel_bridge.py`
  - `refresh_excel_session()` in `eel_bridge.py`

### Decision 4: Frontend Settings Modal & Dual Persistence
- Add `#btnSettings` in `.toolbar-actions` of `.app-header` in `src/web/index.html`.
- Add `#settingsModal` with:
  - Input `#inputSettingDelimiter` (text input with max 3 characters).
  - Select `#selectSettingDefaultType` populated with the 9 Excel types.
  - Buttons `#btnSettingsSave`, `#btnSettingsCancel`, `#btnSettingsReset`.
- When saved:
  - Updates `localStorage.setItem('je_settings_config', ...)`.
  - Calls `eel.update_settings(delimiter, default_data_type)`.
  - Instantly calls `App.renderActiveTree()` and `TreeRenderer.renderPaths()` with the updated tree roots returned from backend.

### Decision 5: Complete Bilingual Dictionary Assets (`i18n.js`)
- Add keys for both Ukrainian (`uk`) and English (`en`):
  - `btn_settings`: `"Налаштування"` / `"Settings"`
  - `settings_title`: `"Налаштування додатку"` / `"Application Settings"`
  - `settings_delimiter_label`: `"Символ розподілу шляхів"` / `"Path Delimiter Symbol"`
  - `settings_delimiter_help`: `"Символ для розділення рівнів у шляхах (за замовчуванням: \\)"` / `"Character used to separate hierarchy levels in paths (default: \\)"`
  - `settings_default_type_label`: `"Тип даних колонок Excel за замовчуванням"` / `"Default Excel Column Data Type"`
  - `settings_default_type_help`: `"Застосовується для колонок без явного формату (General)"` / `"Applied to columns without explicit format (General)"`
  - `settings_btn_reset`: `"Скинути за замовчуванням"` / `"Reset to Defaults"`
  - `settings_btn_save`: `"Зберегти налаштування"` / `"Save Settings"`
  - `toast_settings_saved`: `"Налаштування успішно збережено."` / `"Settings saved successfully."`
  - `toast_settings_reset`: `"Налаштування скинуто до значень за замовчуванням."` / `"Settings reset to default values."`
  - `error_delimiter_empty`: `"Символ розподілу не може бути порожнім."` / `"Path delimiter cannot be empty."`
