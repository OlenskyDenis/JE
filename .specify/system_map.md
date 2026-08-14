# Global System Map: Database Hierarchy Creator & Excel Reorganizer

**Location**: `.specify/system_map.md`  
**Last Updated**: 2026-08-14  
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
|    - models/base.py (HierarchyComponent - Base Abstract Contract)            |
|    - models/composite.py (CompositeNode - Compatibility Alias)                |
|    - models/leaf.py (LeafNode - Compatibility Alias)                          |
|  Services:                                                                    |
|    - services/forest.py (WorkspaceForest - Multi-Root Canvas Tree Forest)     |
|    - services/path_parser.py (PathParserService - Backslash Header Parser)    |
|    - services/path_generator.py (PathGenerator - Leaf Path Calculator)        |
|    - services/header_service.py (HeaderService - Cleaning & Deduplication)   |
|    - services/dialog_service.py (FileDialogService - Native OS File Pickers)  |
|  Adapters:                                                                    |
|    - adapters/excel_adapter.py (ExcelHierarchyAdapter - openpyxl Streaming)   |
+-------------------------------------------------------------------------------+
```

---

## 2. Component Inventory & Responsibility Matrix

### 2.1 Backend Core Domain (`src/hierarchy_lib/`)

| Module | Primary Class / Functions | Key Responsibility | Active State |
|---|---|---|---|
| [`models/node.py`](file:///E:/JE/src/hierarchy_lib/models/node.py) | `HierarchyNode` | Unified dynamic node. Determines state via `len(children) > 0` (`is_folder`). Encapsulates `data_type` (9 standard Excel types: Text, Integer, Decimal, Currency, Percentage, Date, Time, DateTime, Boolean), validates via `set_data_type()`, handles child add/remove, cycle checks (`is_ancestor_of`), path computation, serialization (`to_dict`). | 🟢 Active Core |
| [`models/base.py`](file:///E:/JE/src/hierarchy_lib/models/base.py) | `HierarchyComponent` | Abstract base class defining common node interfaces and name sanitization. | 🟢 Active Base |
| [`models/composite.py`](file:///E:/JE/src/hierarchy_lib/models/composite.py) | `CompositeNode` | Alias pointing to `HierarchyNode`. | 🟡 Legacy Alias (Retained for backwards compatibility) |
| [`models/leaf.py`](file:///E:/JE/src/hierarchy_lib/models/leaf.py) | `LeafNode` | Alias pointing to `HierarchyNode`. | 🟡 Legacy Alias (Retained for backwards compatibility) |
| [`services/forest.py`](file:///E:/JE/src/hierarchy_lib/services/forest.py) | `WorkspaceForest` | Multi-root canvas tree container. Manages `root_nodes`, positional insertion (`add_node_at_zone`), cycle-safe moves (`move_node`), dynamic leaf path resolution (`get_all_leaf_paths`). | 🟢 Active Core |
| [`services/path_parser.py`](file:///E:/JE/src/hierarchy_lib/services/path_parser.py) | `PathParserService` | Parses lists of backslash-delimited path strings (`Root\Folder\Leaf`) into `HierarchyNode` trees with common prefix folder merging. | 🟢 Active Core |
| [`services/path_generator.py`](file:///E:/JE/src/hierarchy_lib/services/path_generator.py) | `PathGenerator` | Computes full absolute backslash paths for all leaf nodes across the forest. | 🟢 Active Core |
| [`services/header_service.py`](file:///E:/JE/src/hierarchy_lib/services/header_service.py) | `HeaderService` | Trims, deduplicates, and filters raw header string lists while strictly preserving original Excel column sequence (FIFO). | 🟢 Active Core |
| [`services/dialog_service.py`](file:///E:/JE/src/hierarchy_lib/services/dialog_service.py) | `FileDialogService` | Spawns native desktop OS file pickers (`askopenfilename`, `asksaveasfilename`) with hidden Tkinter root. | 🟢 Active Core |
| [`excel_adapter.py`](file:///E:/JE/src/hierarchy_lib/adapters/excel_adapter.py) | `ExcelHierarchyAdapter` | Stream-reads Row 1 headers and inspects Excel column number formatting strictly on Row 1 (`read_row1_headers_and_types`, `infer_column_types`), maps types via `_map_format_to_data_type` & `EXCEL_TYPE_FORMAT_MAP`, and exports clean multi-sheet template workbooks with custom leaf paths and openpyxl `number_format` across modified sheets (`export_multi_sheet_template`). Strictly guarantees `max_row == 1` with 0 data rows read. | 🟢 Active |

---

### 2.2 Eel RPC Bridge Layer (`src/app/eel_bridge.py`)

| Source File | Function / RPC | Description & Behavioral Contract | Status |
|---|---|---|---|
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `get_workspace_tree()` | Returns `{ success: true, roots: [...] }` representing current canvas tree with `data_type` metadata on leaf nodes. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `add_node(...)` | Adds dynamic node under parent, at zone, or as root with optional `data_type`. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `update_node(id, name, data_type)` | Updates node name and/or standard Excel `data_type` in active forest. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `update_node_type(id, data_type)` | Updates leaf element `data_type` with domain validation. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `rename_node(id, name)` | Renames node in active forest with whitespace stripping and empty validation. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `move_node(...)` | Moves node to target with zone (`BEFORE_SIBLING`, `AFTER_SIBLING`, `NEST_CHILD`) & cycle check. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `delete_node(...)` | Removes node from parent or forest roots; triggers dynamic folder-to-leaf conversion if parent loses all children. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `import_excel_file(path)` | Opens workbook in streaming mode, infers column types per sheet, returns `all_headers_meta`, `headers_meta`, and parsed `roots` with detected types. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `refresh_excel_session()` | Reconnects to active `current_file_path` on disk, re-parses all sheets' Row 1 headers/types, retains active sheet selection, and updates workspace with full exception handling. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `get_sheet_headers(name)` | Streams and returns Row 1 headers for a specific sheet in current session. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `switch_active_sheet(name)`| Retains modified tree state in `sheet_forests`, returns restored roots, headers, and bound `template_path`. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `save_template_sync(path)` | Exports all modified sheets in `sheet_forests` simultaneously into a clean template file with cell `number_format` formatting and binds `current_template_path`. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `export_reorganized_row1(...)`| Writes leaf path strings horizontally into Row 1 across columns with number formats in a clean template workbook preserving all sheet names. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `open_file_dialog()` | Opens OS file dialog for `.xlsx` file selection. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `save_file_dialog(...)`| Opens OS save dialog proposing `Шаблон_<original_filename>.xlsx` destination path. | 🟢 Active RPC |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `import_excel(path)` | Legacy vertical column A import from Feature 001. | 🟡 Deprecated (Superceded by `import_excel_file`) |
| [`eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | `export_excel(path)` | Legacy multi-sheet vertical column A export from Feature 001. | 🟡 Deprecated (Superceded by `export_reorganized_row1`) |

---

### 2.3 Frontend Web Components (`src/web/`)

| File / Component | Role & Functionality |
|---|---|
| [`index.html`](file:///E:/JE/src/web/index.html) | Top navigation bar with action buttons (`Import Excel`, `Export Excel`, `Refresh`), segmented bilingual language switcher (`.lang-switcher` with `UA` and `EN` buttons), `#templateStatusBadge` bound template indicator, 2-Column workspace with Hierarchy Constructor Workspace canvas on the left (featuring inline `.workspace-sheet-picker` with `#activeSheetSelector`, `#nodeCountBadge`, `#btnExpandAll`, `#btnCollapseAll`, `#btnCreateRootEmpty` in empty state) and Unified Tabbed Sidebar (`#unifiedSidebar`) on the right. Features draggable left-edge resizer splitter (`#sidebarResizer`), Tab Bar (`#tabBtnCatalog`, `#tabBtnPaths`) with live dual counters (`#headerCountBadge`, `#pathCountBadge`), focused catalog selector (`#catalogSheetSelector`), `Export Preview` tab, Node Edit modal with `#selectNodeType` data type selector and `#folderTypeHint`, and Unsaved Changes confirmation modal (`#unsavedModal`). All static UI elements annotated with `data-i18n` and `data-i18n-attr`. |
| [`js/i18n.js`](file:///E:/JE/src/web/js/i18n.js) | Centralized localization engine (Feature 023). Stores complete Ukrainian (`uk`, default) and English (`en`) translation dictionary registries, parameter interpolation (`I18n.t(key, params)`), declarative DOM translator (`translateDOM`), observer event dispatcher (`onLanguageChanged`), and `localStorage` preference persistence (`app_language`). |
| [`js/app.js`](file:///E:/JE/src/web/js/app.js) | Application controller. Manages DOM events, Eel RPC calls (`update_node`, `rename_node`, `add_node`, `move_node`, `delete_node`), inline canvas active workspace sheet selector (`#activeSheetSelector`), bound template state (`#templateStatusBadge`), 1-click direct template update on dirty sheet switch or file import (`pendingAction`), dirty state lifecycle (`isDirty`, `#unsavedModal` interceptors), node edit modal flow (`openEditModal` with dynamic type dropdown pre-population, double-click on `.node-title` or `.node-type-badge`, `Enter`/`Escape` keybinds), independent catalog header browsing (`#catalogSheetSelector` with `__ALL__` combined support, data type tags, and sheet tags), modal lifecycle, persistent folder collapse state (`collapsedNodeIds`), global expand/collapse controls, tab switching controller (`TabController`), draggable left-edge resizing controller (`SidebarResizeController`), multilingual switcher binding and subscriber synchronization (`I18n.onLanguageChanged`), and localized toast notifications. |
| [`js/tree_renderer.js`](file:///E:/JE/src/web/js/tree_renderer.js) | Renders tree nodes dynamically based on `children.length > 0` (folder icon vs leaf icon), renders leaf element `.node-type-badge` badges inside `.node-actions` before rename action, renders interactive animated chevron toggles (`.node-toggle`) and leaf alignment spacers (`.node-toggle-spacer`), universal `+ Add Child`, `.rename-node` (edit icon), and delete buttons, displays live leaf path cards with data type badges, updates `#pathCountBadge`, with all tooltips, labels, and empty states dynamically localized via `I18n.t()`. |
| [`js/drag_drop.js`](file:///E:/JE/src/web/js/drag_drop.js) | Implements three-zone hit testing (`BEFORE_SIBLING`, `AFTER_SIBLING`, `NEST_CHILD`), cycle prevention highlights (`drop-prohibited`), drag payloads preserving detected `dataType` from sidebar items or existing canvas nodes, and localized cycle prohibition toast feedback. |
| [`css/style.css`](file:///E:/JE/src/web/css/style.css) | Core stylesheet implementing the clean dark UI design system, segmented language switcher (`.lang-switcher`, `.lang-btn`), 2-column flexbox workspace layout, unified sidebar styling, tab controls and active indicators, draggable splitter handle (`.resizer-handle-left`), leaf node type badges (`.node-type-badge`), catalog type tags (`.header-type-tag`), and global drag resizing state (`body.is-resizing`). |
| [`css/drag_drop.css`](file:///E:/JE/src/web/css/drag_drop.css) | Visual feedback indicators for drag-and-drop operations (top line, bottom line, center highlight, prohibited cursor). |

---

### 2.4 Test Suites Inventory (`tests/`)

| Test File | Target Module | Scope |
|---|---|---|
| [`tests/unit/test_composite.py`](file:///E:/JE/tests/unit/test_composite.py) | `HierarchyNode` | Dynamic `is_folder` / `is_container` transitions, `data_type` validation, child add/remove, cycle checks, serialization. |
| [`tests/unit/test_forest_zone_addition.py`](file:///E:/JE/tests/unit/test_forest_zone_addition.py) | `WorkspaceForest` | Positional insertion (`BEFORE_SIBLING`, `AFTER_SIBLING`, `NEST_CHILD`) on roots and nested nodes. |
| [`tests/unit/test_path_parser.py`](file:///E:/JE/tests/unit/test_path_parser.py) | `PathParserService` | Hierarchical backslash parsing, common prefix merging, single nodes, delimiter cleanup. |
| [`tests/unit/test_path_generator.py`](file:///E:/JE/tests/unit/test_path_generator.py) | `PathGenerator` | Leaf path calculation and dynamic state updates across multi-root forests. |
| [`tests/unit/test_excel_adapter.py`](file:///E:/JE/tests/unit/test_excel_adapter.py) | `ExcelHierarchyAdapter`| Read-only streaming, 10-consecutive-empty cutoff, column type inference (`infer_column_types`), sheet listing, horizontal Row 1 export with openpyxl cell `number_format` formatting. |
| [`tests/unit/test_header_service.py`](file:///E:/JE/tests/unit/test_header_service.py) | `HeaderService` | Trimming, deduplication, sorting, and edge cases. |
| [`tests/unit/test_dialog_service.py`](file:///E:/JE/tests/unit/test_dialog_service.py) | `FileDialogService` | Native OS open/save dialog mocking, cancellation handling, root window withdrawal. |
| [`tests/unit/test_excel_import.py`](file:///E:/JE/tests/unit/test_excel_import.py) | Legacy Adapter Import | Legacy Feature 001 import verification. |
| [`tests/unit/test_excel_export.py`](file:///E:/JE/tests/unit/test_excel_export.py) | Legacy Adapter Export | Legacy Feature 001 export verification. |
| [`tests/integration/test_eel_bridge.py`](file:///E:/JE/tests/integration/test_eel_bridge.py) | `eel_bridge.py` | Full RPC workflow: node CRUD, `update_node`, `update_node_type`, zone moves, streaming import with data type metadata, sheet switching, export with formatting persistence. |


---

## 3. Architecture Hygiene & Deprecation Audit

The following items are flagged for maintenance and cleanup in upcoming refactoring cycles:

1. **Legacy Feature 001 RPC Endpoints**:
   - `import_excel(file_path)` and `export_excel(file_path)` in `eel_bridge.py` and corresponding methods in `excel_adapter.py` read/write single paths in column A across sheets. They are superseded by `import_excel_file` and `export_reorganized_row1` (Row 1 horizontal workflow).
   - *Recommendation*: Deprecate and retire when legacy compatibility is no longer required.
2. **CompositeNode & LeafNode Subclass Aliases**:
   - `CompositeNode` in `models/composite.py` and `LeafNode` in `models/leaf.py` are retained as aliases to `HierarchyNode` for backwards compatibility.
   - *Recommendation*: Direct all new code and imports to `from src.hierarchy_lib.models.node import HierarchyNode`.
3. **`is_container` Property**:
   - `is_container` is maintained on `HierarchyNode` as an alias for `is_folder`.
   - *Recommendation*: Prefer `is_folder` in new features; retain `is_container` in serialization for existing API consumers.

---

## 4. Maintenance Guidelines for Feature Designs

Whenever a new feature is specified (`/speckit.specify`) or planned (`/speckit.plan`):
1. **Read this document** to ensure new features build upon existing active components.
2. **Update this document** if any classes, modules, RPC endpoints, or UI controls are added, modified, or retired.
3. **Audit for redundancies**: Verify that new features do not duplicate existing functionality in `ExcelHierarchyAdapter`, `HeaderService`, `PathParserService`, or `WorkspaceForest`.
