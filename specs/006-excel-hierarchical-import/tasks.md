# Task Breakdown: Automatic Hierarchical Excel Header Import & Workspace Tree Generator

**Feature**: `006-excel-hierarchical-import`  
**Branch**: `006-excel-hierarchical-import`  
**Spec**: [specs/006-excel-hierarchical-import/spec.md](spec.md)  
**Plan**: [specs/006-excel-hierarchical-import/plan.md](plan.md)  

---

## Phase 1: Setup & Foundational (Prerequisites)

**Purpose**: Set up module structure and test fixtures for hierarchical path parsing

- [x] T001 [P] Create `tests/unit/test_path_parser.py` test suite skeleton
- [x] T002 [P] Verify `CompositeNode`, `LeafNode`, and `WorkspaceForest` models in `src/hierarchy_lib/models/` and `src/hierarchy_lib/services/forest.py`

---

## Phase 2: User Story 1 - Automatic Hierarchical Tree Generation on Excel Import (Priority: P1) 🎯 MVP

**Goal**: Automatically parse Excel Row 1 headers formatted as backslash paths into `CompositeNode` and `LeafNode` hierarchies, merging common ancestor folder branches, and rendering the tree in the workspace canvas upon file load.

**Independent Test**: Load an Excel file with Row 1 headers (`Root\Folder\Leaf1`, `Root\Folder\Leaf2`, `Root\Other\Leaf3`), verify that the workspace canvas tree view immediately populates with the hierarchical tree `Root -> Folder -> [Leaf1, Leaf2]` and `Root -> Other -> [Leaf3]`.

### Tests for User Story 1 (TDD)
- [x] T003 [P] [US1] Write unit tests in `tests/unit/test_path_parser.py` for:
  - Multi-level path parsing (`A\B\C` $\rightarrow$ `A` (Composite) -> `B` (Composite) -> `C` (LeafNode))
  - Common prefix merging (`A\B\C1` and `A\B\C2` share single parent `B`)
  - Single segment headers (`Standalone` $\rightarrow$ top-level root node)
  - Whitespace trimming and edge delimiters (` \A\\B\C\ ` $\rightarrow$ `A\B\C`)
  - Empty/blank header lists handling

### Implementation for User Story 1
- [x] T004 [US1] Implement `PathParserService` in `src/hierarchy_lib/services/path_parser.py` (depends on T003)
- [x] T005 [US1] Update `import_excel_file` endpoint in `src/app/eel_bridge.py` to parse active sheet's headers via `PathParserService`, update global `forest`, and return `"roots"` payload
- [x] T006 [US1] Update `handleImportExcelFile` in `src/web/js/app.js` to render returned `res.roots` via `this.updateUI(res.roots)`

**Checkpoint**: User Story 1 is functional: Importing an Excel file automatically builds and renders the hierarchical tree in the workspace canvas.

---

## Phase 3: User Story 2 - Dynamic Tree Rebuilding on Sheet Switching (Priority: P2)

**Goal**: Automatically rebuild and update the workspace hierarchy tree when the user switches active sheets via the dropdown selector.

**Independent Test**: Load a multi-sheet workbook, switch to a second sheet in the sheet selector dropdown, and verify that the canvas tree clears and renders the hierarchy corresponding to the newly selected sheet.

### Tests for User Story 2
- [x] T007 [P] [US2] Write integration tests in `tests/integration/test_eel_bridge.py` for sheet switching tree regeneration and `roots` return payload

### Implementation for User Story 2
- [x] T008 [US2] Update `switch_active_sheet` endpoint in `src/app/eel_bridge.py` to parse target sheet headers via `PathParserService`, reset `forest`, and return `"roots"` payload
- [x] T009 [US2] Update `handleSwitchSheet` in `src/web/js/app.js` to render returned `res.roots` via `this.updateUI(res.roots)`

---

## Phase 4: User Story 3 - Round-Trip Export and Non-Destructive Editing (Priority: P3)

**Goal**: Verify that automatically generated trees can be edited on canvas (node additions, deletions, moves) and exported back to Row 1 of the target Excel sheet with 100% path notation fidelity.

**Independent Test**: Load an Excel sheet, edit a node, export to a new `.xlsx` file, re-import the file, and confirm identical reconstructed hierarchy.

### Tests & Implementation for User Story 3
- [x] T010 [P] [US3] Verify horizontal Row 1 export integration with parsed hierarchy in `tests/unit/test_excel_adapter.py`
- [x] T011 [US3] Verify canvas node operations (drag-drop, add child, delete) preserve path integrity on automatically generated trees

---

## Phase 5: Polish & Regression Testing

**Purpose**: Complete test execution, error handling edge cases, and documentation

- [x] T012 [P] Add edge case tests (empty row 1, non-string headers, invalid characters) in `tests/unit/test_path_parser.py`
- [x] T013 Run full test suite `python -m pytest` to verify all unit and integration tests pass cleanly with 0 failures
