# Global System Map: Database Hierarchy Creator & Excel Reorganizer

**Location**: `.specify/system_map.md`  
**Last Updated**: 2026-08-16  
**Governing Principle**: Constitution Principle VI (Global System Map & Architecture Hygiene)

---

## 1. High-Level System Architecture

The application is an environment-independent Desktop GUI for modeling, restructuring, and persisting database hierarchies from and into Microsoft Excel (`.xlsx`) files.

```
+-------------------------------------------------------------------------------+
|                           Frontend UI (HTML5 / Vanilla JS)                    |
|  - index.html (Main Layout: Toolbar, Sheet Selector, Sidebar Catalog, Canvas) |
|  - js/app.js (App Controller, Eel RPC Dispatcher, State Sync)                 |
|  - js/tree_renderer.js (Dynamic Hierarchy Rendering & Universal Actions)      |
|  - js/drag_drop.js (Three-Zone Drag & Drop Hit-Testing & Cycle Prevention)    |
|  - js/excel_block_renderer.js (2D Spreadsheet Block Matrix Table View)        |
|  - js/unique_level_renderer.js (Unique Header Levels & Duplicate Highlighting)|
|  - js/i18n.js (Centralized Localization Engine: Ukrainian / English)          |
|  - css/style.css & css/drag_drop.css (Dark Design System & Drop Indicators)   |
+---------------------------------------+---------------------------------------+
                                        | Eel RPC (WebSocket / JSON-RPC)
                                        v
+-------------------------------------------------------------------------------+
|                       Backend RPC Bridge & Entry (src/app/)                   |
|  - main.py (App Bootstrapper, Eel Initialization, Chromium/Default Window)    |
|  - eel_bridge.py (Exposed RPC Endpoints, Global WorkspaceForest State)        |
+---------------------------------------+---------------------------------------+
                                        | Domain Service Calls
                                        v
+-------------------------------------------------------------------------------+
|                       Core Domain Library (src/hierarchy_lib/)                |
|  Models:                                                                      |
|    - models/node.py (HierarchyNode - Unified Dynamic Node: Folder vs Leaf)    |
|    - models/data_types.py (VALID_DATA_TYPES & validate_data_type)             |
|  Services:                                                                    |
|    - services/forest.py (WorkspaceForest - Multi-Root Canvas Tree Forest)     |
|    - services/path_parser.py (PathParserService - Path Header Parser)         |
|    - services/header_service.py (HeaderService - Cleaning & Deduplication)   |
|    - services/dialog_service.py (FileDialogService - Native OS File Pickers)  |
|    - services/settings_service.py (SettingsService - Config Persistence)      |
|  Adapters:                                                                    |
|    - adapters/excel_adapter.py (ExcelHierarchyAdapter - openpyxl Streaming)   |
+-------------------------------------------------------------------------------+
```

---

## 2. Component Inventory & Responsibility Matrix

### 2.1 Backend Core Domain (`src/hierarchy_lib/`)

| Module | Primary Class / Functions | Key Responsibility | Active State |
|---|---|---|---|
| [`models/node.py`](file:///E:/JE/src/hierarchy_lib/models/node.py) | `HierarchyNode` | Unified dynamic node. Determines state via `len(children) > 0` (`is_folder`). Encapsulates `data_type` (9 standard Excel types), validates via `set_data_type()`, handles child add/remove, cycle checks (`is_ancestor_of`), path computation, serialization (`to_dict`). Completely decoupled from `SettingsService` (DIP). | 🟢 Active Core |
| [`models/data_types.py`](file:///E:/JE/src/hierarchy_lib/models/data_types.py) | `VALID_DATA_TYPES`, `validate_data_type` | Single source of truth for 9 standard Excel column types (Text, Integer, Decimal, Currency, Percentage, Date, Time, DateTime, Boolean) and validation functions (OCP). | 🟢 Active Core |
| [`services/forest.py`](file:///E:/JE/src/hierarchy_lib/services/forest.py) | `WorkspaceForest` | Multi-root canvas tree container. Manages `root_nodes`, positional insertion (`add_node_at_zone`), cycle-safe moves (`move_node`), dynamic leaf path resolution (`get_all_leaf_paths`). Decoupled from `SettingsService`. | 🟢 Active Core |
| [`services/path_parser.py`](file:///E:/JE/src/hierarchy_lib/services/path_parser.py) | `PathParserService` | Parses lists of delimited path strings into `HierarchyNode` trees with common prefix folder merging. Decoupled from `SettingsService`. | 🟢 Active Core |
| [`services/header_service.py`](file:///E:/JE/src/hierarchy_lib/services/header_service.py) | `HeaderService` | Trims, deduplicates, and filters raw header string lists while strictly preserving original Excel column sequence (FIFO). | 🟢 Active Core |
| [`services/dialog_service.py`](file:///E:/JE/src/hierarchy_lib/services/dialog_service.py) | `FileDialogService` | Spawns native desktop OS file pickers (`askopenfilename`, `asksaveasfilename`) with hidden Tkinter root. | 🟢 Active Core |
| [`services/settings_service.py`](file:///E:/JE/src/hierarchy_lib/services/settings_service.py) | `SettingsService` | Manages application-wide settings (`delimiter`, `default_data_type`) with schema validation, default fallbacks, and atomic persistence to `settings.json`. | 🟢 Active Core |
| [`adapters/excel_adapter.py`](file:///E:/JE/src/hierarchy_lib/adapters/excel_adapter.py) | `ExcelHierarchyAdapter` | Stream-reads Row 1 headers and inspects Excel column formatting strictly on Row 1 (`read_row1_headers_and_types`), maps types via `_map_format_to_data_type` & `EXCEL_TYPE_FORMAT_MAP`, and exports clean multi-sheet template workbooks with custom leaf paths and openpyxl `number_format` across modified sheets (`export_multi_sheet_template`). Strictly guarantees `max_row == 1` with 0 data rows read. | 🟢 Active Core |
| `models/base.py` | `HierarchyComponent` | Abstract base class formerly used in Feature 001. | 🔴 Retired (Feature 029) |
| `models/composite.py` | `CompositeNode` | Class alias formerly used for backwards compatibility. | 🔴 Retired (Feature 029) |
| `models/leaf.py` | `LeafNode` | Class alias formerly used for backwards compatibility. | 🔴 Retired (Feature 029) |
| `services/path_generator.py` | `PathGenerator` | Static path generator utility superceded by `HierarchyNode.get_absolute_path()` and `WorkspaceForest.get_all_leaf_paths()`. | 🔴 Retired (Feature 029) |

---

### 2.2 Eel RPC Bridge Layer (`src/app/eel_bridge.py`)

| Source File | Function / RPC | Description & Behavioral Contract | Status |
|---|---|---|---|
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `get_settings()` | Returns `{ success: true, settings: { delimiter, default_data_type } }` from `SettingsService`. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `update_settings(delim, type)` | Updates application settings in `SettingsService` / `settings.json` and returns recalculated `roots`. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `reset_settings()` | Resets application settings to defaults (`\` and `Text`) and returns recalculated `roots`. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `add_node(...)` | Adds dynamic node under parent, at zone, or as root with optional `data_type`. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `move_node(...)` | Moves node to target with zone (`BEFORE_SIBLING`, `AFTER_SIBLING`, `NEST_CHILD`) & cycle check. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `delete_node(...)` | Removes node from parent or forest roots; unlinks parent pointers safely. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `update_node(id, name, data_type)` | Universal updater for node name and/or standard Excel `data_type` in active forest. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `import_excel_file(path)` | Opens workbook in streaming mode, infers column types per sheet, returns `all_headers_meta`, `headers_meta`, and parsed `roots` with detected types. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `refresh_excel_session()` | Reconnects to active `current_file_path` on disk, re-parses all sheets' Row 1 headers/types, retains active sheet selection, and updates workspace with full exception handling. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `switch_active_sheet(name)`| Retains modified tree state in `sheet_forests`, returns restored roots, headers, and bound `template_path`. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `save_template_sync(path)` | Exports all modified sheets in `sheet_forests` simultaneously into a clean template file with cell `number_format` formatting and binds `current_template_path`. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `open_file_dialog()` | Opens OS file dialog for `.xlsx` file selection. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `save_file_dialog(...)`| Opens OS save dialog proposing `Шаблон_<original_filename>.xlsx` destination path. | 🟢 Active RPC |
| `eel_bridge.py` | `get_workspace_tree()` | Obsolete RPC returning forest roots; superceded by direct returns from action RPCs. | 🔴 Retired (Feature 029) |
| `eel_bridge.py` | `rename_node(id, name)` | Obsolete single-field RPC; superceded by `update_node`. | 🔴 Retired (Feature 029) |
| `eel_bridge.py` | `update_node_type(id, type)` | Obsolete single-field RPC; superceded by `update_node`. | 🔴 Retired (Feature 029) |
| `eel_bridge.py` | `get_sheet_headers(name)` | Obsolete RPC; superceded by `switch_active_sheet`. | 🔴 Retired (Feature 029) |
| `eel_bridge.py` | `export_reorganized_row1(...)` | Single-sheet export wrapper; superceded by `save_template_sync`. | 🔴 Retired (Feature 029) |
| `eel_bridge.py` | `import_excel(path)` | Legacy vertical column A import from Feature 001. | 🔴 Retired (Feature 029) |
| `eel_bridge.py` | `export_excel(path)` | Legacy multi-sheet vertical column A export from Feature 001. | 🔴 Retired (Feature 029) |

---

### 2.3 Frontend Web Components (`src/web/`)

| File / Component | Role & Functionality |
|---|---|
| [`index.html`](file:///E:/JE/src/web/index.html) | Top navigation bar with action buttons (`Import Excel`, `Export Excel`, `Refresh`, `#btnSettings` gear icon), segmented bilingual language switcher (`.lang-switcher` with `UA` and `EN` buttons), `#templateStatusBadge` bound template indicator, 2-Column workspace with Hierarchy Constructor Workspace canvas on the left (featuring inline `.workspace-sheet-picker` with `#activeSheetSelector`, `#nodeCountBadge`, `#viewModeSwitcher` 3-mode segmented switcher for Tree (`#btnViewTree`), Excel Blocks (`#btnViewMatrix`), and Unique Levels (`#btnViewUniqueLevels`), `#btnAddRootHeader` root node creator button, `#btnExpandAll`, `#btnCollapseAll`, `#btnCreateRootEmpty` in empty state) and Unified Resizable/Collapsible Tabbed Sidebar (`#unifiedSidebar`) on the right. Features draggable left-edge resizer splitter (`#sidebarResizer`), `.sidebar-collapsed-strip` (28px) with `#btnExpandSidebarStrip`, compact tab dropdown selector (`#sidebarTabSelector`) with `#headerCountBadge` and `#pathCountBadge`, persistent collapse toggle (`#btnToggleSidebarCollapse`), focused catalog selector (`#catalogSheetSelector`), `Export Preview` tab, Node Edit modal with `#selectNodeType` data type selector and `#folderTypeHint`, Unsaved Changes confirmation modal (`#unsavedModal`), and Settings modal (`#settingsModal`) for delimiter and unformatted column data type configuration. All static UI elements annotated with `data-i18n` and `data-i18n-attr`. |
| [`js/i18n.js`](file:///E:/JE/src/web/js/i18n.js) | Centralized localization engine (Feature 023 & 025). Stores complete Ukrainian (`uk`, default) and English (`en`) translation dictionary registries, parameter interpolation (`I18n.t(key, params)`), declarative DOM translator (`translateDOM`), observer event dispatcher (`onLanguageChanged`), and `localStorage` preference persistence (`app_language`). |
| [`js/app.js`](file:///E:/JE/src/web/js/app.js) | Application controller. Manages DOM events, Eel RPC calls (`update_node`, `add_node`, `move_node`, `delete_node`, `get_settings`, `update_settings`, `reset_settings`), inline canvas active workspace sheet selector (`#activeSheetSelector`), view mode switcher controller (`#viewModeSwitcher`, `switchViewMode`, `localStorage` persistence `je_workspace_view_mode`), bound template state (`#templateStatusBadge`), 1-click direct template update on dirty sheet switch or file import (`pendingAction`), dirty state lifecycle (`isDirty`, `#unsavedModal` interceptors), direct root node creation (`#btnAddRootHeader`, `#btnAddRootCanvas`), node edit modal flow (`openEditModal` with dynamic type dropdown pre-population, double-click on `.node-title` or `.node-type-badge`, `Enter`/`Escape` keybinds), Settings modal controller (`#settingsModal` open, save, reset, `localStorage` caching `je_settings_config`), independent catalog header browsing (`#catalogSheetSelector` with `__ALL__` combined support, data type tags, and sheet tags), modal lifecycle, persistent folder collapse state (`collapsedNodeIds`), global expand/collapse controls, tab switching controller (`TabController`), draggable left-edge resizing controller (`SidebarResizeController`), multilingual switcher binding and subscriber synchronization (`I18n.onLanguageChanged`), and localized toast notifications. |
| [`js/tree_renderer.js`](file:///E:/JE/src/web/js/tree_renderer.js) | Renders tree nodes dynamically based on `children.length > 0` (folder icon vs leaf icon), renders leaf element `.node-type-badge` badges inside `.node-actions` before edit action, renders interactive animated chevron toggles (`.node-toggle`) and leaf alignment spacers (`.node-toggle-spacer`), universal `+ Add Child`, `.edit-node` (edit icon), and delete buttons, renders quick-add root action row (`.tree-footer-actions`, `#btnAddRootCanvas`), displays live leaf path cards with data type badges, updates `#pathCountBadge`, with all tooltips, labels, and empty states dynamically localized via `I18n.t()`. |
| [`js/excel_block_renderer.js`](file:///E:/JE/src/web/js/excel_block_renderer.js) | Translates `WorkspaceForest` trees into a 2D multi-tier Excel block matrix table (`#excelBlockView`), calculating tree depth, leaf column counts, column coordinates (A, B, C...), proportional horizontal `colspan` on parent blocks, terminal leaf vertical `rowspan`, rich hover tooltips, and localized empty states. |
| [`js/unique_level_renderer.js`](file:///E:/JE/src/web/js/unique_level_renderer.js) | Deconstructs `WorkspaceForest` trees into horizontal stacked level rows containing deduplicated unique header terms (`#uniqueLevelView`), calculating per-level unique counts, case-insensitive cross-level duplicate detection (`has-cross-match`), match badges, rich occurrence tooltips, and synchronized interactive hover highlighting (`.highlight-match-sync`). |
| [`js/drag_drop.js`](file:///E:/JE/src/web/js/drag_drop.js) | Implements three-zone hit testing (`BEFORE_SIBLING`, `AFTER_SIBLING`, `NEST_CHILD`), cycle prevention highlights (`drop-prohibited`), drag payloads preserving detected `dataType` from sidebar items or existing canvas nodes, and localized cycle prohibition toast feedback. |
| [`css/style.css`](file:///E:/JE/src/web/css/style.css) | Core stylesheet implementing the clean dark UI design system, segmented language switcher (`.lang-switcher`, `.lang-btn`), view mode switcher (`.view-mode-switcher`, `.view-mode-btn`), Excel block matrix spreadsheet styling (`.excel-matrix-table`, `.matrix-coord-header`, `.matrix-cell`, tier fills), root creation button styles (`.tree-footer-actions`, `.btn-add-root-canvas`), 2-column flexbox workspace layout, unified sidebar styling, tab controls and active indicators, draggable splitter handle (`.resizer-handle-left`), leaf node type badges (`.node-type-badge`), catalog type tags (`.header-type-tag`), settings modal layout (`#settingsModal`, `.modal-footer-split`), and global drag resizing state (`body.is-resizing`). |
| [`css/drag_drop.css`](file:///E:/JE/src/web/css/drag_drop.css) | Visual feedback indicators for drag-and-drop operations (top line, bottom line, center highlight, prohibited cursor). |

---

### 2.4 Test Suites Inventory (`tests/`)

| Test File | Target Module | Scope |
|---|---|---|
| [`tests/unit/test_settings_service.py`](file:///E:/JE/tests/unit/test_settings_service.py) | `SettingsService` | Settings initialization, schema validation, delimiter validation, default data type validation, atomic `settings.json` file saving/loading, and defaults reset. |
| [`tests/unit/test_data_types.py`](file:///E:/JE/tests/unit/test_data_types.py) | `data_types.py` | Canonical Excel data type validation, normalization, and error handling. |
| [`tests/unit/test_composite.py`](file:///E:/JE/tests/unit/test_composite.py) | `HierarchyNode` | Dynamic `is_folder` / `is_container` transitions, `data_type` validation, child add/remove, cycle checks, serialization. |
| [`tests/unit/test_forest_zone_addition.py`](file:///E:/JE/tests/unit/test_forest_zone_addition.py) | `WorkspaceForest` | Positional insertion (`BEFORE_SIBLING`, `AFTER_SIBLING`, `NEST_CHILD`) on roots and nested nodes. |
| [`tests/unit/test_path_parser.py`](file:///E:/JE/tests/unit/test_path_parser.py) | `PathParserService` | Hierarchical path parsing with custom delimiters (`\`, `/`, `::`), common prefix merging, single nodes, delimiter cleanup. |
| [`tests/unit/test_excel_adapter.py`](file:///E:/JE/tests/unit/test_excel_adapter.py) | `ExcelHierarchyAdapter`| Read-only streaming, 10-consecutive-empty cutoff, column type inference with custom default data type (`default_data_type`), sheet listing, multi-sheet horizontal Row 1 export with openpyxl cell `number_format` formatting. |
| [`tests/unit/test_header_service.py`](file:///E:/JE/tests/unit/test_header_service.py) | `HeaderService` | Trimming, deduplication, sorting, and edge cases. |
| [`tests/unit/test_dialog_service.py`](file:///E:/JE/tests/unit/test_dialog_service.py) | `FileDialogService` | Native OS open/save dialog mocking, cancellation handling, root window withdrawal. |
| [`tests/unit/test_frontend_contracts.py`](file:///E:/JE/tests/unit/test_frontend_contracts.py) | Frontend Contracts | Integrity checks: script tag file existence, DOM ID parity, I18n method existence, and Ukrainian/English translation parity. |
| [`tests/integration/test_eel_bridge.py`](file:///E:/JE/tests/integration/test_eel_bridge.py) | `eel_bridge.py` | Full RPC API integration tests including settings endpoints (`get_settings`, `update_settings`, `reset_settings`), live tree recalculation, and error handling. |
| `tests/unit/test_excel_import.py` | Legacy Adapter Import | Legacy Feature 001 import verification. | 🔴 Retired (Feature 029) |
| `tests/unit/test_excel_export.py` | Legacy Adapter Export | Legacy Feature 001 export verification. | 🔴 Retired (Feature 029) |
| `tests/unit/test_path_generator.py` | Legacy PathGenerator | Legacy path calculation tests. | 🔴 Retired (Feature 029) |

---

## 3. Maintenance Guidelines for Feature Designs

Whenever a new feature is specified (`/speckit.specify`) or planned (`/speckit.plan`):
1. **Read this document** to ensure new features build upon existing active components.
2. **Update this document** if any classes, modules, RPC endpoints, or UI controls are added, modified, or retired.
3. **Audit for redundancies**: Verify that new features do not duplicate existing functionality in `ExcelHierarchyAdapter`, `HeaderService`, `PathParserService`, `SettingsService`, or `WorkspaceForest`.
