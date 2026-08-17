# Controllers & RPC Layer: Application Orchestration

**Path**: `.specify/system_map/controllers_and_rpc.md`  
**Architectural Layer**: Controller / RPC Bridge Layer  
**Technologies**: Python Eel (WebSocket JSON-RPC), Modular JavaScript Sub-Controllers (ES2022)

---

## 1. Frontend Modular Controllers (`src/web/js/`)

Following Feature 033 refactoring, the frontend monolithic controller was decomposed into focused, single-responsibility controllers ($\le 200$ lines each):

| Sub-Controller | File | Responsibilities |
|---|---|---|
| **App Orchestrator** | [`app.js`](file:///E:/JE/src/web/js/app.js) | Sub-module initialization, global DOM bindings, keyboard shortcuts (`Ctrl+Z`, `Escape`), path breadcrumb rendering, and toast notifications. |
| **Modal Manager** | [`modal_manager.js`](file:///E:/JE/src/web/js/modal_manager.js) | Add node modal, Edit node modal (with batch rename notice), and Unsaved changes dialog. |
| **Sidebar Controller** | [`sidebar_controller.js`](file:///E:/JE/src/web/js/sidebar_controller.js) | Catalog tabs, search filter, sidebar drag resizer, and collapsible sidebar strip. |
| **View Mode Manager** | [`view_mode_manager.js`](file:///E:/JE/src/web/js/view_mode_manager.js) | View mode switching (Tree, Matrix, Unique Levels) and double-click event delegation. |
| **Session Controller** | [`session_controller.js`](file:///E:/JE/src/web/js/session_controller.js) | Excel import/refresh, active sheet switching, dirty tracking, template syncing, and pending action queue. |
| **Settings Controller** | [`settings_controller.js`](file:///E:/JE/src/web/js/settings_controller.js) | Delimiter and default data type configuration dialog. |

---

## 2. Backend Controllers & RPC Router (`src/app/`)

| Controller | File | Responsibilities |
|---|---|---|
| **Eel RPC Bridge Router** | [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | Exposes 13 public `@eel.expose` endpoints, delegating cleanly to `SessionManager`, `NodeController`, `SettingsService`, and `FileDialogService`. |
| **Session Manager** | [`session_manager.py`](file:///E:/JE/src/app/session_manager.py) | Manages multi-sheet session forests, active sheet tracking, DRY row 1 parsing, and multi-sheet template export. |
| **Node Controller** | [`node_controller.py`](file:///E:/JE/src/app/node_controller.py) | Node CRUD operations (`add_node`, `update_node`, `delete_node`, `move_node`) on workspace forests with cycle checks. |

---

## 3. Exposed RPC Endpoints

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
