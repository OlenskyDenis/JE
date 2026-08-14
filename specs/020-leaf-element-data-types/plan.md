# Implementation Plan: Leaf Element Data Type Inspection, Editing, and Excel Persistence

**Branch**: `020-leaf-element-data-types` | **Date**: 2026-08-14 | **Spec**: [specs/020-leaf-element-data-types/spec.md](spec.md)

**Input**: Feature specification from `/specs/020-leaf-element-data-types/spec.md`

---

## Summary

Implement full end-to-end data type management for all non-folder (leaf) elements in the Hierarchy Constructor Workspace:
1. **Domain Model**: Add `data_type` field and `set_data_type()` validation to `HierarchyNode`.
2. **Excel Type Detection & Persistence**: Implement column type inference (`read_sheet_columns_metadata`) in `ExcelHierarchyAdapter` and write openpyxl `number_format` strings on multi-sheet template export (`export_multi_sheet_template`).
3. **RPC Bridge**: Expose `update_node(node_id, name, data_type)` / `update_node_type(node_id, data_type)` and return column type metadata in `import_excel_file` and `get_workspace_tree`.
4. **Frontend UI**: Render `.node-type-badge` in `TreeRenderer` (canvas tree and Export Preview tab), integrate `#selectNodeType` into `#nodeModal`, support catalog drag-and-drop type inheritance, and dynamically manage folder $\leftrightarrow$ leaf transitions upon deletion/movement.

---

## Technical Context

**Language/Version**: Python 3.14 (Backend Core & Eel RPC), Vanilla ES6+ JavaScript, HTML5, CSS3  
**Dependencies**: `openpyxl` (streaming read-only / workbook creation), `eel`, `pytest`  
**Testing**: Unit tests in `tests/unit/test_composite.py`, `tests/unit/test_excel_adapter.py`, integration tests in `tests/integration/test_eel_bridge.py`  
**Target Platform**: Desktop GUI (Windows / Chromium via Eel)  
**Constraints**: 100% environment-independent (Principle V, zero MS Excel requirement), zero regression on dynamic composite hierarchy operations, dirty state sync integrity.

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I (SDD Scope Enforcement)**: PASSED. Spec and Plan authored prior to code modifications.
- **Principle II (OOP & Clean State Architecture)**: PASSED. `HierarchyNode` encapsulates `data_type` and validation; services remain decoupled.
- **Principle III (GoF Dynamic Composite Pattern)**: PASSED. Folder vs leaf polymorphism dynamically activates/deactivates data type states.
- **Principle IV (Library-First & TDD)**: PASSED. Domain and adapter unit tests specified before UI assembly.
- **Principle V (Self-Contained Excel Processing)**: PASSED. Uses `openpyxl` number formats without COM interop.
- **Principle VI (System Map First-Load & Proactive Redundancy Audit)**: PASSED. [`.specify/system_map.md`](../../.specify/system_map.md) audited and updated.
- **Principle VII (Red Teaming & Zero-Data Stress Testing)**: PASSED. Validated zero-data scenarios, empty sheets, mixed column types, and folder-to-leaf conversion upon child deletion.

---

## Project Structure

### Documentation (this feature)

```text
specs/020-leaf-element-data-types/
├── spec.md              # Feature specification
├── plan.md              # Implementation plan (this file)
├── research.md          # Architectural decisions & type mappings
├── quickstart.md        # Verification guide
└── checklists/
    └── requirements.md  # Quality & compliance checklist
```

### Source Code Architecture

```text
src/
├── app/
│   └── eel_bridge.py        # update_node/update_node_type RPC, header metadata dispatch
├── hierarchy_lib/
│   ├── models/
│   │   └── node.py          # HierarchyNode.data_type, set_data_type, to_dict serialization
│   └── adapters/
│       └── excel_adapter.py # Column type inference, openpyxl number_format mapping on export
└── web/
    ├── index.html           # #selectNodeType select element in #nodeModal
    ├── css/
    │   └── style.css        # .node-type-badge styling & color themes per type
    └── js/
        ├── app.js           # openEditModal type population, drag-and-drop type inheritance
        └── tree_renderer.js # .node-type-badge rendering on canvas nodes and Export Preview
```

---

## Implementation Sequence

### Phase 1: Core Domain Model & TDD Unit Tests (`src/hierarchy_lib/models/`)
1. In `src/hierarchy_lib/models/node.py`:
   - Add `self.data_type: Optional[str] = "Text"` attribute in `__init__`.
   - Add `set_data_type(self, data_type: str)` with validation against the 9 standard Excel types (`Text`, `Integer`, `Decimal`, `Currency`, `Percentage`, `Date`, `Time`, `DateTime`, `Boolean`).
   - Include `"data_type": self.data_type` in `to_dict()`.
2. In `tests/unit/test_composite.py`:
   - Test default `data_type` initialization.
   - Test `set_data_type` valid mutations and invalid type rejection.
   - Test `to_dict()` serialization.
   - Test child deletion causing folder $\rightarrow$ leaf dynamic conversion and verifying `data_type` accessibility.

### Phase 2: Excel Adapter Type Inference & Formatting (`src/hierarchy_lib/adapters/`)
1. In `src/hierarchy_lib/adapters/excel_adapter.py`:
   - Implement `infer_column_types(file_path_or_stream, sheet_name, max_rows=100) -> Dict[str, str]`.
   - Implement `EXCEL_TYPE_FORMAT_MAP` mapping standard type strings to openpyxl `number_format` strings.
   - Update `export_multi_sheet_template` to accept leaf node metadata (paths + data types) and apply cell `number_format` in exported worksheets.
2. In `tests/unit/test_excel_adapter.py`:
   - Test column type inference across formatted cells (currency, dates, integers, floats, booleans, strings).
   - Test template export verifying applied `number_format` on exported columns.

### Phase 3: Backend Eel RPC Bridge & Integration Tests (`src/app/`)
1. In `src/app/eel_bridge.py`:
   - Expose `@eel.expose def update_node(node_id: str, name: Optional[str] = None, data_type: Optional[str] = None) -> Dict[str, Any]`.
   - Expose `@eel.expose def update_node_type(node_id: str, data_type: str) -> Dict[str, Any]`.
   - Update `import_excel_file` to include `headers_meta` with detected data types in returned payload.
   - Update `add_node` to accept optional `data_type: Optional[str] = None`.
   - Update `save_template_sync` and `export_reorganized_row1` to extract leaf `data_type` from forest nodes and pass to `ExcelHierarchyAdapter`.
2. In `tests/integration/test_eel_bridge.py`:
   - Test full import $\rightarrow$ type inspection $\rightarrow$ type mutation $\rightarrow$ template export persistence workflow.

### Phase 4: Frontend UI Assembly & Tree Rendering (`src/web/`)
1. In `src/web/index.html`:
   - Add `#selectNodeType` form group inside `#nodeModal` with standard Excel type `<option>`s.
2. In `src/web/css/style.css`:
   - Add styling for `.node-type-badge` with subtle semantic color indicators (Currency = green-tint, Date/Time = blue-tint, Number = amber-tint, Text = neutral, Boolean = purple-tint).
3. In `src/web/js/tree_renderer.js`:
   - Render `.node-type-badge` for leaf nodes (`!isFolder`).
   - In `renderPaths()`, display the data type badge on each path card in the `Export Preview` tab.
4. In `src/web/js/app.js`:
   - In `openEditModal()`: display and pre-select `#selectNodeType` for leaf nodes; hide or disable for folder nodes.
   - In `submitModal()`: send `data_type` along with `name` to `eel.update_node` / `eel.rename_node`.
   - In `handleDropPayload()` and `handleAddHeaderNode()`: pass catalog item's `data_type` when creating a node.
   - On node deletion / move: re-render tree, verifying dynamic folder $\leftrightarrow$ leaf badge transitions.

### Phase 5: System Map Synchronization & Regression Verification
1. Update [`.specify/system_map.md`](../../.specify/system_map.md) with all new models, endpoints, format maps, and UI elements.
2. Run full pytest test suite `python -m pytest`.
3. Execute manual verification workflow according to `quickstart.md`.

---

## Complexity Tracking

| Dimension | Risk / Effort | Mitigation |
|---|---|---|
| Excel Type Detection | Low | Sample-based read-only scanning (Rows 2..100) avoids memory bloat |
| openpyxl Formatting | Low | Uses standard built-in number format strings (`@`, `0`, `0.00`, etc.) |
| Dynamic State Polymorphism | Negligible | Already core to `HierarchyNode` design (`len(children) == 0`) |
| Backward Compatibility | Zero | Legacy endpoints and unformatted columns default safely to `"Text"` |
