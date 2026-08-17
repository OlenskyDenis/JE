# Data Model & Architecture Design: Project Audit & Modularity Refactor

**Feature Branch**: `033-project-audit-and-hygiene`  
**Date**: 2026-08-17  
**Spec**: [spec.md](spec.md)

---

## 1. Modular Component Map & Responsibilities

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. Frontend Layer (src/web/js/)                                        │
│   ├── App (app.js) [~160 lines]                                        │
│   │   └── Coordinates Bootstrap, Eel Event Dispatch & Bus              │
│   ├── ModalManager (modal_manager.js) [~170 lines]                      │
│   │   └── Add/Edit/Batch/Unsaved/Settings Modals & State               │
│   ├── SidebarController (sidebar_controller.js) [~150 lines]           │
│   │   └── Tabs, Search, Drag-Resize, Strip Collapse                    │
│   ├── ViewModeManager (view_mode_manager.js) [~130 lines]              │
│   │   └── Tree/Matrix/Unique View Mode Dispatch & Sync                 │
│   ├── UniqueLevelExtractor (unique_level_extractor.js) [~140 lines]    │
│   │   └── Pure Tree Traversal, Level & Leaf Partitioning               │
│   └── UniqueLevelRenderer (unique_level_renderer.js) [~180 lines]      │
│       └── DOM Container, Badges & Event Handlers                       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ JSON-RPC via WebSocket
┌───────────────────────────────────▼────────────────────────────────────┐
│ 2. Application Layer (src/app/)                                        │
│   ├── EelBridge (eel_bridge.py) [~120 lines]                           │
│   │   └── Pure @eel.expose Router & Envelope Builder                   │
│   ├── SessionManager (session_manager.py) [~150 lines]                 │
│   │   └── Multi-Sheet Session Forests, Import/Sync/Switch/Export       │
│   └── NodeController (node_controller.py) [~110 lines]                 │
│       └── Node CRUD Operations & Forest Zone Insertions                │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Pure Python Calls
┌───────────────────────────────────▼────────────────────────────────────┐
│ 3. Core Domain & Adapters (src/hierarchy_lib/)                         │
│   ├── ExcelHierarchyAdapter (excel_adapter.py) [~35 lines]             │
│   │   └── Public Adapter Facade (Backward Compatible)                  │
│   ├── ExcelReader (excel_reader.py) [~120 lines]                       │
│   │   └── Streaming Row 1 Header & Type Heuristic Reading              │
│   ├── ExcelWriter (excel_writer.py) [~110 lines]                       │
│   │   └── Multi-Sheet Template Export Workbook Builder                 │
│   └── Models & Services (node.py, forest.py, data_types.py...)         │
│       └── In Compliance (< 200 lines each)                             │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Class Models & Interfaces

### Frontend Modules (`src/web/js/`)

#### 1. `ModalManager` (`modal_manager.js`)
```javascript
class ModalManager {
  constructor(app) {
    this.app = app;
    // DOM bindings for add, edit, unsaved, settings modals
  }
  openAddModal(parentId, title) {}
  openEditModal(nodeId, currentName, currentType, isFolder, batchCount, batchNodeIds) {}
  closeModal() {}
  submitModal() {}
  showUnsavedChangesModal({ onDiscard, onSave }) {}
  openSettingsModal() {}
  closeSettingsModal() {}
  saveSettingsModal() {}
}
```

#### 2. `SidebarController` (`sidebar_controller.js`)
```javascript
class SidebarController {
  constructor(app) {
    this.app = app;
    // DOM bindings for tabs, search, resizer, collapse
  }
  init() {}
  switchTab(tabName) {}
  handleSearch(query) {}
  initResizer() {}
  toggleCollapse(forceState) {}
}
```

#### 3. `ViewModeManager` (`view_mode_manager.js`)
```javascript
class ViewModeManager {
  constructor(app) {
    this.app = app;
    this.currentMode = 'tree'; // 'tree' | 'excelBlock' | 'uniqueLevel'
  }
  setMode(mode) {}
  renderCurrentView(roots) {}
  setupCanvasEventDelegation() {}
}
```

#### 4. `UniqueLevelExtractor` (`unique_level_extractor.js`)
```javascript
const UniqueLevelExtractor = {
  extractUniqueLevels(roots) {
    // Pure algorithm returning:
    // [{ depth: 1, leaves: [...], branches: [...], totalCount: N }, ...]
  }
};
```

---

### Backend Modules (`src/app/` & `src/hierarchy_lib/adapters/`)

#### 1. `SessionManager` (`src/app/session_manager.py`)
```python
class SessionManager:
    def __init__(self):
        self.forest: WorkspaceForest = WorkspaceForest()
        self.sheet_forests: Dict[str, WorkspaceForest] = {}
        self.current_active_sheet: Optional[str] = None
        self.current_file_path: Optional[str] = None
        self.current_template_path: Optional[str] = None

    def import_excel_file(self, file_path: str) -> Dict[str, Any]: ...
    def refresh_excel_session(self) -> Dict[str, Any]: ...
    def switch_active_sheet(self, sheet_name: str) -> Dict[str, Any]: ...
    def save_template_sync(self, output_path: Optional[str] = None) -> Dict[str, Any]: ...
    def get_forest_leaf_meta(self, sforest: WorkspaceForest, delimiter: Optional[str] = None) -> List[Dict[str, str]]: ...
    def _sync_sheet_forests(self, file_path: str, sheets: List[str], default_type: str, delim: str) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, WorkspaceForest]]: ...
```

#### 2. `NodeController` (`src/app/node_controller.py`)
```python
class NodeController:
    @staticmethod
    def add_node(forest: WorkspaceForest, parent_id=None, name="", target_id=None, zone=None, data_type=None) -> Dict[str, Any]: ...
    @staticmethod
    def update_node(forest: WorkspaceForest, node_id: str, name=None, data_type=None) -> Dict[str, Any]: ...
    @staticmethod
    def delete_node(forest: WorkspaceForest, node_id: str) -> Dict[str, Any]: ...
    @staticmethod
    def move_node(forest: WorkspaceForest, node_id: str, target_node_id: str, zone: str) -> Dict[str, Any]: ...
```

#### 3. `ExcelReader` & `ExcelWriter` (`src/hierarchy_lib/adapters/`)
```python
# excel_reader.py
class ExcelReader:
    @staticmethod
    def get_sheet_names(file_path_or_stream) -> List[str]: ...
    @staticmethod
    def read_row1_headers_and_types(file_path_or_stream, sheet_name, max_empty_consecutive=10, default_data_type=None) -> List[Tuple[str, str]]: ...
    @staticmethod
    def read_row1_headers(file_path_or_stream, sheet_name, max_empty_consecutive=10, default_data_type=None) -> List[str]: ...

# excel_writer.py
class ExcelWriter:
    @staticmethod
    def export_multi_sheet_template(file_path_or_stream, sheet_leaf_paths_map: Dict[str, Any], output_path: str) -> int: ...

# excel_adapter.py (Facade)
class ExcelHierarchyAdapter:
    get_sheet_names = ExcelReader.get_sheet_names
    read_row1_headers_and_types = ExcelReader.read_row1_headers_and_types
    read_row1_headers = ExcelReader.read_row1_headers
    export_multi_sheet_template = ExcelWriter.export_multi_sheet_template
```

---

## 3. Line Count Budget & Threshold Compliance

| Target File | Expected Post-Refactor Line Count | Threshold Limit | Compliance Status |
|---|:---:|:---:|:---:|
| `src/app/eel_bridge.py` | ~120 | $\le 200$ | 🟢 Compliant |
| `src/app/session_manager.py` | ~150 | $\le 200$ | 🟢 Compliant |
| `src/app/node_controller.py` | ~110 | $\le 200$ | 🟢 Compliant |
| `src/hierarchy_lib/adapters/excel_adapter.py` | ~35 | $\le 200$ | 🟢 Compliant |
| `src/hierarchy_lib/adapters/excel_reader.py` | ~120 | $\le 200$ | 🟢 Compliant |
| `src/hierarchy_lib/adapters/excel_writer.py` | ~110 | $\le 200$ | 🟢 Compliant |
| `src/web/js/app.js` | ~160 | $\le 200$ | 🟢 Compliant |
| `src/web/js/modal_manager.js` | ~170 | $\le 200$ | 🟢 Compliant |
| `src/web/js/sidebar_controller.js` | ~150 | $\le 200$ | 🟢 Compliant |
| `src/web/js/view_mode_manager.js` | ~130 | $\le 200$ | 🟢 Compliant |
| `src/web/js/unique_level_extractor.js` | ~140 | $\le 200$ | 🟢 Compliant |
| `src/web/js/unique_level_renderer.js` | ~180 | $\le 200$ | 🟢 Compliant |
| `src/web/js/i18n.js` | ~480 | Exempt | 🟢 Compliant (Exempt) |
| `src/web/css/style.css` | ~1640 | Exempt | 🟢 Compliant (Exempt) |
| `src/web/index.html` | ~295 | Exempt | 🟢 Compliant (Exempt) |
