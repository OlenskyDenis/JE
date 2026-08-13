# Tasks: Database Hierarchy Creator with Excel Integration

**Feature Branch**: `001-database-hierarchy-creator` | **Spec**: [`specs/001-database-hierarchy-creator/spec.md`](file:///E:/JE/specs/001-database-hierarchy-creator/spec.md) | **Plan**: [`specs/001-database-hierarchy-creator/plan.md`](file:///E:/JE/specs/001-database-hierarchy-creator/plan.md)

---

## Constitution Compliance Notice
This task list strictly enforces project constitution rules:
- **SDD Phase Enforcement**: Code modifications reserved for implement phase.
- **SOLID / OOP / GoF**: Core hierarchy components follow the Composite pattern.
- **Library-First & TDD**: Unit tests written and verified passing.
- **Self-Contained Excel**: `openpyxl` tasks execute without requiring MS Excel desktop software.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project directory initialization and environment configuration

- [x] T001 Create project package directory structure: `src/hierarchy_lib/models`, `src/hierarchy_lib/services`, `src/hierarchy_lib/adapters`, `src/app`, `src/web/css`, `src/web/js`, `tests/unit`, `tests/integration`
- [x] T002 Create dependency configuration file `requirements.txt` specifying `eel>=0.16.0`, `openpyxl>=3.1.0`, and `pytest>=8.0.0`
- [x] T003 [P] Create pytest configuration file `pytest.ini` with test discovery paths and pythonpath configuration

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core GoF Composite pattern classes and hierarchy domain models.

- [x] T004 Create `HierarchyComponent` abstract base class in `src/hierarchy_lib/models/base.py` with `id`, `name`, `parent`, and `get_absolute_path()` method signature
- [x] T005 [P] Create `LeafNode` class inheriting from `HierarchyComponent` in `src/hierarchy_lib/models/leaf.py`
- [x] T006 [P] Create `CompositeNode` class inheriting from `HierarchyComponent` in `src/hierarchy_lib/models/composite.py` with `children` list
- [x] T007 Implement cycle prevention method `is_ancestor_of()` in `src/hierarchy_lib/models/composite.py`
- [x] T008 Implement `WorkspaceForest` multi-root container class in `src/hierarchy_lib/services/forest.py`

**Checkpoint**: Foundation ready - core class abstractions created.

---

## Phase 3: User Story 1 - Core Hierarchy Modeling & Path Generator Library (Priority: P1) MVP

**Goal**: Standalone Python library (`hierarchy_lib`) implementing backslash-separated (`Root\Folder\Subfolder\Item`) path calculation, multi-root forest management, covered 100% by unit tests (TDD).

### TDD Unit Tests for User Story 1

- [x] T009 [P] [US1] Write unit tests for `HierarchyComponent`, `CompositeNode`, `LeafNode`, and cycle detection in `tests/unit/test_composite.py`
- [x] T010 [P] [US1] Write unit tests for `PathGenerator` and `WorkspaceForest` multi-root path generation in `tests/unit/test_path_generator.py`

### Implementation for User Story 1

- [x] T011 [US1] Implement recursive path calculation `get_absolute_path()` in `src/hierarchy_lib/models/base.py` and `src/hierarchy_lib/services/path_generator.py`
- [x] T012 [US1] Add node addition, removal, and reparenting logic to `CompositeNode` and `WorkspaceForest`
- [x] T013 [US1] Verify TDD unit test suite passes 100% (`pytest tests/unit/test_composite.py tests/unit/test_path_generator.py`)

**Checkpoint**: Core library functionality is fully working, testable, and verified independently.

---

## Phase 4: User Story 2 - Self-Contained Single-Line Excel Import & Export (Priority: P2)

**Goal**: Import Excel workbooks (reading Row 1 / Cell A1 path strings per sheet) into Composite node trees, and export path strings (one element per cell per row) using `openpyxl`.

### TDD Unit Tests for User Story 2

- [x] T014 [P] [US2] Write unit tests for Row 1 path string Excel import in `tests/unit/test_excel_import.py`
- [x] T015 [P] [US2] Write unit tests for vertical segment cell Excel export in `tests/unit/test_excel_export.py`

### Implementation for User Story 2

- [x] T016 [US2] Implement `ExcelHierarchyAdapter.import_from_workbook()` using `openpyxl` in `src/hierarchy_lib/adapters/excel_adapter.py`
- [x] T017 [US2] Implement `ExcelHierarchyAdapter.export_to_workbook()` using `openpyxl` in `src/hierarchy_lib/adapters/excel_adapter.py`
- [x] T018 [US2] Verify TDD unit test suite passes 100% for Excel adapters (`pytest tests/unit/test_excel_import.py tests/unit/test_excel_export.py`)

**Checkpoint**: Excel import/export functionality is fully working and verified independently.

---

## Phase 5: User Story 3 - Interactive Drag-and-Drop Desktop UI (Priority: P3)

**Goal**: Eel desktop application hosting responsive HTML5/CSS3/Vanilla JS UI with Three-Zone hit testing (top/bottom 25% for sibling reorder, center 50% for child nesting), prohibited cursor, snap-back animation, and warning toast notifications.

### Integration Tests for User Story 3

- [x] T019 [P] [US3] Write contract tests for Eel RPC backend methods in `tests/integration/test_eel_bridge.py`

### Implementation for User Story 3

- [x] T020 [P] [US3] Implement Eel RPC bridge methods (`get_workspace_tree`, `add_node`, `move_node`, `delete_node`, `import_excel`, `export_excel`) in `src/app/eel_bridge.py`
- [x] T021 [P] [US3] Create Eel application launcher in `src/app/main.py`
- [x] T022 [P] [US3] Create HTML5 workspace template in `src/web/index.html`
- [x] T023 [P] [US3] Create CSS styles for responsive workspace layout, 3-zone drop targets, and toast notifications in `src/web/css/style.css` and `src/web/css/drag_drop.css`
- [x] T024 [US3] Implement Eel JS RPC client wrapper and state synchronization in `src/web/js/app.js`
- [x] T025 [US3] Implement tree DOM renderer with backslash path badges in `src/web/js/tree_renderer.js`
- [x] T026 [US3] Implement Three-Zone hit-testing (top/bottom 25% for sibling, center 50% for child) and real-time cycle rejection validation in `src/web/js/drag_drop.js`
- [x] T027 [US3] Wire Excel import/export toolbar buttons to Eel RPC methods in `src/web/js/app.js`

**Checkpoint**: Complete desktop application is fully integrated and functional.

---

## Phase 6: Polish & Verification

**Purpose**: Cross-cutting validation, documentation, and test suite verification

- [x] T028 [P] Update developer documentation and verify commands in `quickstart.md`
- [x] T029 Execute full test suite (`pytest tests/`) ensuring 100% pass rate across unit and integration tests
- [x] T030 Perform desktop GUI end-to-end verification launching `python -m src.app.main`
