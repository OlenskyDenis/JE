# Controllers & RPC Layer: Application Orchestration

**Path**: `.specify/system_map/controllers_and_rpc.md`  
**Architectural Layer**: Controller / RPC Bridge Layer  
**Technologies**: Python Eel (WebSocket JSON-RPC), Vanilla JavaScript (ES2022 Controller)

---

## 1. Frontend Controller ([`app.js`](file:///E:/JE/src/web/js/app.js))

The `App` controller coordinates DOM event handling, RPC communication with Eel, view mode transitions, and session state.

### Key Controller Responsibilities:
1. **Application Lifecycle**: Bootstraps settings, event listeners, view modes, and multi-sheet session state upon `DOMContentLoaded`.
2. **Eel RPC Dispatching**: Calls backend `@eel.expose` endpoints and handles async JSON responses (`res.success`, `res.error`, `res.roots`).
3. **Dirty State & Unsaved Changes**: Manages `isDirty` flag, intercepts tab switches or file imports via `#unsavedModal`, and triggers 1-click sync (`save_template_sync`).
4. **Modal Controllers**:
   * Settings Modal: open, save, reset defaults, and `localStorage` caching (`je_settings_config`).
   * Node Edit Modal: open with type pre-selection, save (name & data type), and keyboard shortcuts (`Enter`/`Escape`).
   * Node Add Modal: child creation under parent or as root.
5. **View Mode Controller**: Switches between Tree, Matrix, and Unique Levels view modes (`switchViewMode()`) with `localStorage` persistence (`je_workspace_view_mode`).
6. **Sidebar & Layout**: Manages tab switching (`TabController`), resizable width dragging (`SidebarResizeController`), and persistent collapse toggle.

---

## 2. Eel RPC Bridge ([`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py))

Exposes Python backend services to JavaScript via `@eel.expose`. Injects active `SettingsService` configuration into domain model method calls.

### Exposed RPC Endpoints:

| Endpoint | Parameters | Returns (DTO) | Description |
|---|---|---|---|
| `get_settings()` | *none* | `{ success, settings }` | Fetches active application settings (`delimiter`, `default_data_type`). |
| `update_settings(...)` | `delimiter: Optional[str]`, `default_data_type: Optional[str]` | `{ success, settings, roots }` | Updates settings in `SettingsService` and recalculates tree roots for UI. |
| `reset_settings()` | *none* | `{ success, settings, roots }` | Resets settings to defaults (`\` and `Text`) and recalculates tree roots. |
| `add_node(...)` | `parent_id, name, is_container, target_id, zone, data_type` | `{ success, node, roots }` | Adds dynamic node as root, under parent, or relative to target node zone. |
| `move_node(...)` | `node_id: str, target_node_id: str, zone: str` | `{ success, rejection_reason, roots }` | Moves node to target zone (`BEFORE_SIBLING`, `AFTER_SIBLING`, `NEST_CHILD`) with cycle check. |
| `delete_node(...)` | `node_id: str` | `{ success, roots }` | Deletes node from parent or forest roots; unlinks parent pointers cleanly. |
| `update_node(...)` | `node_id: str, name: Optional[str], data_type: Optional[str]` | `{ success, node, roots }` | Universal updater for node name and/or standard Excel `data_type`. |
| `import_excel_file(...)`| `file_path: str` | `{ success, sheets, active_sheet, headers, all_headers, headers_meta, all_headers_meta, template_path, roots }` | Imports workbook session, streaming Row 1 headers and inferring types across all sheets. |
| `refresh_excel_session()`| *none* | `{ success, sheets, active_sheet, headers, all_headers, headers_meta, all_headers_meta, template_path, roots }` | Reconnects to disk file, re-parses all sheets streaming Row 1, and updates session. |
| `switch_active_sheet(...)`| `sheet_name: str` | `{ success, sheet_name, headers, template_path, roots }` | Switches active sheet, restoring cached tree from `sheet_forests`. |
| `save_template_sync(...)`| `output_path: Optional[str]` | `{ success, template_path, total_columns, modified_sheets }` | Exports all modified sheets simultaneously to a clean template file with cell `number_format` formatting. |
| `open_file_dialog()` | *none* | `{ success, file_path, canceled }` | Spawns native OS open file picker for `.xlsx` files. |
| `save_file_dialog(...)`| `default_name: Optional[str]` | `{ success, file_path, canceled }` | Spawns native OS save file picker with `Шаблон_` prefix. |

---

## 3. Application Services

### 3.1 [`SettingsService`](file:///E:/JE/src/hierarchy_lib/services/settings_service.py)
* Manages configuration (`delimiter`, `default_data_type`).
* Atomic disk persistence to `settings.json`.

### 3.2 [`HeaderService`](file:///E:/JE/src/hierarchy_lib/services/header_service.py)
* Normalizes, trims, and deduplicates raw header string lists while strictly preserving original Excel column sequence (FIFO).

### 3.3 [`FileDialogService`](file:///E:/JE/src/hierarchy_lib/services/dialog_service.py)
* Encapsulates native desktop file dialogs with hidden Tkinter root window lifecycle management.
