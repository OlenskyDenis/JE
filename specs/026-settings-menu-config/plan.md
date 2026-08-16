# Implementation Plan: Settings Menu Configuration

**Feature Branch**: `026-settings-menu-config`  
**Spec**: [specs/026-settings-menu-config/spec.md](spec.md)  
**Created**: 2026-08-16  
**Status**: In Progress

---

## 1. Technical Context & Architecture Overview

### Problem Statement
The path delimiter (`\`) and Excel unformatted column fallback type (`Text`) are currently hardcoded across backend services (`HierarchyNode`, `PathParserService`, `ExcelHierarchyAdapter`) and the frontend tree renderer. Users need a centralized Settings modal in the desktop toolbar to customize the path delimiter (e.g., `/`, `|`, `::`) and change the default Excel data type for unassigned/General columns, with dual persistence (`localStorage` and `settings.json`) and instant real-time UI updates.

### Target Architecture & Strategy
1. **Centralized Configuration Service (`src/hierarchy_lib/services/settings_service.py`)**:
   - Manages application configuration (`delimiter`, `default_data_type`).
   - Handles loading from / writing to `settings.json` in the project root with atomic safety.
   - Provides validation against `VALID_DATA_TYPES` and 1–3 char delimiter strings.
2. **Domain Model & Parsing Layer Propagation**:
   - Update `HierarchyNode.get_absolute_path(delimiter=None)` and `to_dict(delimiter=None)` to use the configured delimiter.
   - Update `PathParserService.parse_header_paths(paths, delimiter=None)` to parse paths based on the active delimiter.
   - Update `ExcelHierarchyAdapter._map_format_to_data_type(..., default_data_type=None)` to map General/unassigned columns to the configured default data type.
3. **Eel Bridge RPC Layer (`src/app/eel_bridge.py`)**:
   - Expose `get_settings()` returning current settings DTO.
   - Expose `update_settings(delimiter, default_data_type)` which updates backend settings, re-evaluates active session forests, and returns updated roots for instant frontend rendering.
   - Synchronize Excel import and session refresh workflows with the active settings.
4. **Web Frontend & Settings Modal (`src/web/index.html`, `src/web/css/style.css`, `src/web/js/app.js`)**:
   - Add `#btnSettings` gear button in `.toolbar-actions`.
   - Add `#settingsModal` dialog containing delimiter text input and default data type dropdown with Save, Cancel, and Reset Defaults buttons.
   - Add full Ukrainian (`uk`) and English (`en`) dictionary entries in `src/web/js/i18n.js`.
   - Persist settings in `localStorage` and trigger instant `TreeRenderer.renderTree` and `TreeRenderer.renderPaths` updates upon save.

---

## 2. Component Implementation Breakdown

### 2.1 Backend Services & Models
- **`src/hierarchy_lib/services/settings_service.py`**:
  - `SettingsService.get_settings() -> Dict[str, str]`
  - `SettingsService.update_settings(delimiter: str, default_data_type: str) -> Dict[str, str]`
  - `SettingsService.reset_to_defaults() -> Dict[str, str]`
- **`src/hierarchy_lib/models/base.py` & `src/hierarchy_lib/models/node.py`**:
  - Update `get_absolute_path(self, delimiter: Optional[str] = None)`
  - Update `to_dict(self, delimiter: Optional[str] = None)`
- **`src/hierarchy_lib/services/path_parser.py`**:
  - Update `parse_header_paths(paths: Sequence[Optional[str]], delimiter: Optional[str] = None)`
- **`src/hierarchy_lib/services/path_generator.py`**:
  - Update `calculate_path(component, delimiter: Optional[str] = None)`
  - Update `calculate_all_paths(forest, delimiter: Optional[str] = None)`
- **`src/hierarchy_lib/adapters/excel_adapter.py`**:
  - Update `_map_format_to_data_type(..., default_data_type: str = "Text")`
  - Update `read_row1_headers_and_types(..., default_data_type: str = "Text")`
  - Update `import_from_file(..., default_data_type: str = "Text", delimiter: str = "\\")`

### 2.2 Eel RPC Integration (`src/app/eel_bridge.py`)
- Wire `SettingsService` into session lifecycle.
- Implement `@eel.expose def get_settings()`.
- Implement `@eel.expose def update_settings(delimiter: str, default_data_type: str)`.
- Pass active settings to `import_excel_file`, `refresh_excel_session`, and `switch_active_sheet`.

### 2.3 Frontend & Localization (`src/web/`)
- **`src/web/index.html`**:
  - Insert `#btnSettings` in `.toolbar-actions`.
  - Add `#settingsModal` template markup with form controls and buttons.
- **`src/web/js/i18n.js`**:
  - Add dictionary entries for Ukrainian and English for all settings titles, labels, placeholders, help texts, and toasts.
- **`src/web/js/app.js`**:
  - Initialize settings from `localStorage` / `eel.get_settings()`.
  - Modal lifecycle management (`openSettingsModal()`, `closeSettingsModal()`, `saveSettings()`, `resetSettings()`).
  - Real-time tree and path preview refresh upon settings changes.

---

## 3. Test Strategy & Plan

1. **Unit Tests (`tests/unit/test_settings_service.py`)**:
   - Validate default settings retrieval.
   - Validate updating delimiter and default data type.
   - Validate rejection of invalid delimiters (empty, whitespace, >3 chars) and invalid data types.
   - Validate resetting to defaults.
2. **Domain Model & Parser Tests**:
   - Test `HierarchyNode.get_absolute_path` with custom delimiters (`/`, `|`, `::`).
   - Test `PathParserService.parse_header_paths` with custom delimiters (`/`, `|`).
   - Test `ExcelHierarchyAdapter` assigning custom `default_data_type` (e.g. `Decimal`) to unformatted columns.
3. **Integration Tests (`tests/integration/test_eel_bridge.py`)**:
   - Test `get_settings()` and `update_settings()` RPC endpoints.
   - Verify tree roots recalculation across active and background session sheets.

---

## 4. Execution Phases

- **Phase 0**: Research & Architecture Specification (`research.md`, `data-model.md`, `quickstart.md`).
- **Phase 1**: Backend `SettingsService` and domain model propagation with unit tests.
- **Phase 2**: Excel adapter default data type & delimiter integration.
- **Phase 3**: Eel bridge RPC endpoints and session synchronization.
- **Phase 4**: Frontend Settings UI, modal styling, i18n dictionaries, and event wiring.
- **Phase 5**: Full test suite validation (`pytest`) and regression testing.
