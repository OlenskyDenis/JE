# Task Breakdown: Excel Header Reorganization & Database Structure Designer

**Feature**: `002-excel-sidebar-reorganizer`  
**Branch**: `feature/excel-sidebar-reorganizer`  
**Spec**: [specs/002-excel-sidebar-reorganizer/spec.md](spec.md)  
**Plan**: [specs/002-excel-sidebar-reorganizer/plan.md](plan.md)  

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and service placeholders

- [ ] T001 Create header service module in `src/hierarchy_lib/services/header_service.py` and test file in `tests/unit/test_header_service.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before user story work begins

- [ ] T002 [P] Verify Composite pattern base models in `src/hierarchy_lib/models/base.py`, `src/hierarchy_lib/models/composite.py`, and `src/hierarchy_lib/models/leaf.py`
- [ ] T003 [P] Verify path generator service for backslash path strings in `src/hierarchy_lib/services/path_generator.py`

---

## Phase 3: User Story 1 - Multi-Sheet Header Extraction & Sidebar View (Priority: P1) 🎯 MVP

**Goal**: Import Excel workbooks, select active sheet via dropdown control, extract unique sorted Row 1 headers using `openpyxl`, and display in a sidebar with real-time text search.

**Independent Test**: Import a multi-sheet `.xlsx` file, switch sheets in dropdown, verify sidebar updates with sorted unique headers, and test real-time search filtering.

### Tests for User Story 1
- [ ] T004 [P] [US1] Write failing unit tests for header extraction, whitespace trimming, deduplication, and alphabetical sorting in `tests/unit/test_header_service.py`
- [ ] T005 [P] [US1] Write failing unit test for `read_row1_headers` and `get_sheet_names` in `tests/unit/test_excel_adapter.py`

### Implementation for User Story 1
- [ ] T006 [US1] Implement `HeaderService` in `src/hierarchy_lib/services/header_service.py` (depends on T004)
- [ ] T007 [US1] Implement Row 1 reading and sheet listing methods in `src/hierarchy_lib/adapters/excel_adapter.py` (depends on T005)
- [ ] T008 [US1] Expose Eel RPC endpoints `import_excel_file` and `switch_active_sheet` in `src/app/eel_bridge.py`
- [ ] T009 [P] [US1] Update HTML layout to add sheet selector dropdown and header sidebar container in `src/web/index.html`
- [ ] T010 [P] [US1] Add CSS styles for sidebar header items and search input in `src/web/css/style.css`
- [ ] T011 [US1] Implement sheet selector handler and real-time sidebar search filtering in `src/web/js/app.js`

**Checkpoint**: At this point, User Story 1 is fully testable and functional (MVP).

---

## Phase 4: User Story 2 - Non-Destructive Drag-and-Drop Header Tree Construction (Priority: P2)

**Goal**: Drag headers from the sidebar into the main tree builder canvas without removing them from the sidebar, creating nested composite tree nodes.

**Independent Test**: Drag a header from the sidebar onto the tree canvas. A new tree node is created while the original header remains visible in the sidebar for reuse.

### Implementation for User Story 2
- [ ] T012 [P] [US2] Implement non-destructive HTML5 dragstart and dragover handlers in `src/web/js/drag_drop.js`
- [ ] T013 [P] [US2] Add drop zone hover and insertion indicator styles in `src/web/css/drag_drop.css`
- [ ] T014 [US2] Connect drop event handler to composite tree node creation in `src/web/js/tree_renderer.js`

**Checkpoint**: User Stories 1 and 2 work seamlessly together.

---

## Phase 5: User Story 3 - Horizontal Row-1 Excel Export by Sheet (Priority: P3)

**Goal**: Write reconstructed tree leaf path strings (`Root\Folder\Item`) sequentially across columns in Row 1 under the active sheet name using `openpyxl`.

**Independent Test**: Construct a tree, trigger export, open the generated `.xlsx` file, and verify Row 1 contains leaf path strings across columns A1, B1, C1...

### Tests for User Story 3
- [ ] T015 [P] [US3] Write failing unit test for horizontal Row 1 export of leaf path strings in `tests/unit/test_excel_adapter.py`

### Implementation for User Story 3
- [ ] T016 [US3] Implement `export_horizontal_paths` method in `src/hierarchy_lib/adapters/excel_adapter.py` (depends on T015)
- [ ] T017 [US3] Expose Eel RPC endpoint `export_reorganized_row1` in `src/app/eel_bridge.py`
- [ ] T018 [US3] Wire Export button in `src/web/js/app.js` to collect tree leaf path strings and call `export_reorganized_row1`

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Edge case verification, integration testing, and documentation

- [ ] T019 [P] Add edge case unit tests (empty Row 1, special characters, whitespace trimming) in `tests/unit/test_header_service.py`
- [ ] T020 [P] Write integration tests for full Eel bridge RPC workflow in `tests/integration/test_eel_bridge.py`
- [ ] T021 Run complete quickstart validation suite (`python -m pytest`) to confirm all tests pass cleanly

---

## Dependencies & Execution Order

### Phase Dependencies
- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion. BLOCKS all user stories.
- **User Story 1 (Phase 3)**: Depends on Foundational phase.
- **User Story 2 (Phase 4)**: Depends on Foundational phase (can run in parallel with US1 frontend work).
- **User Story 3 (Phase 5)**: Depends on Foundational phase and Composite tree node models.
- **Polish (Phase 6)**: Depends on completion of user stories.

---

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Complete Phase 1 & Phase 2.
2. Complete Phase 3 (User Story 1).
3. Test multi-sheet import, sheet switching, and sidebar header search independently.

### Incremental Delivery
1. Deliver US1 (Header Sidebar Catalog & Sheet Selector).
2. Deliver US2 (Non-Destructive Drag-and-Drop Tree Builder).
3. Deliver US3 (Horizontal Row 1 Re-Export).
