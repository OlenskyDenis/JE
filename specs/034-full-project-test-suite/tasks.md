# Tasks: Full-Project Comprehensive Automated Test Suite & Multi-Layer Behavioral Verification

**Branch**: `034-full-project-test-suite` | **Date**: 2026-08-17 | **Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Test runner initialization and quality baseline verification

- [x] T001 Initialize feature branch verification and ensure pre-commit hook is active via `python scripts/check_all.py --quick`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Confirm clean test harness baseline and isolated browser execution

- [x] T002 Verify ephemeral Eel test harness and state isolation fixtures in `tests/e2e/conftest.py`

---

## Phase 3: User Story 1 - Core Tree & View Mode E2E Test Matrix (Priority: P1) 🎯 MVP

**Goal**: Establish comprehensive E2E tests for root creation, node editing, branch folding, and all 3 viewing modes (Tree, Matrix, Unique Levels).

**Independent Test**: Execute `pytest tests/e2e/test_tree_crud_and_modals.py tests/e2e/test_view_modes_and_renderers.py` and verify all visual and interactive assertions pass.

### Implementation for User Story 1

- [x] T003 [P] [US1] Expand `tests/e2e/test_tree_crud_and_modals.py` with empty state root creation (`#btnCreateRootEmpty`), header add button (`#btnAddRootHeader`), and input name validation
- [x] T004 [P] [US1] Add node renaming (`.action-btn.rename-node`), deletion (`.action-btn.delete`), branch folding (`.node-toggle`), and global collapse/expand tests to `tests/e2e/test_tree_crud_and_modals.py`
- [x] T005 [P] [US1] Expand `tests/e2e/test_view_modes_and_renderers.py` with Excel Matrix view coordinate rendering (`#btnViewMatrix`, `.matrix-coord-row`) and hierarchical block cells
- [x] T006 [US1] Add Unique Levels view leaf-first grouping (`#btnViewUniqueLevels`, `.level-header-chip`) and duplicate matching synchronized hover highlight (`.highlight-match-sync`) tests in `tests/e2e/test_view_modes_and_renderers.py`

**Checkpoint**: Core Tree and all 3 View Modes fully verified with concrete visibility assertions.

---

## Phase 4: User Story 2 - Multi-Sheet Workbook Lifecycle, File Dialogs & Template Sync (Priority: P1)

**Goal**: Establish comprehensive E2E tests for Excel workbook importing, sheet switching, dirty state protection, and template synchronization.

**Independent Test**: Execute `pytest tests/e2e/test_multi_sheet_and_excel_lifecycle.py` and verify multi-sheet session flows.

### Implementation for User Story 2

- [x] T007 [P] [US2] Expand `tests/e2e/test_multi_sheet_and_excel_lifecycle.py` with multi-sheet workbook loading (`multisheet_retail.xlsx`), sheet selector population, and active sheet switching
- [x] T008 [P] [US2] Add dirty state tracking and unsaved changes modal prompts (`#unsavedModal`: Cancel, Discard, Save) in `tests/e2e/test_multi_sheet_and_excel_lifecycle.py`
- [x] T009 [US2] Add template synchronization badge state (`#templateStatusBadge`) and headers-only clean workbook export verification in `tests/e2e/test_multi_sheet_and_excel_lifecycle.py`

**Checkpoint**: Multi-sheet workbook sessions and template syncing verified against data loss.

---

## Phase 5: User Story 3 - Drag-and-Drop, Zone Placement & Cycle Validation (Priority: P2)

**Goal**: Establish comprehensive E2E tests for catalog header dragging, 3-zone placement, sibling reordering, and cycle detection.

**Independent Test**: Execute `pytest tests/e2e/test_drag_and_drop.py` and verify drag operations.

### Implementation for User Story 3

- [x] T010 [P] [US3] Expand `tests/e2e/test_drag_and_drop.py` with catalog-to-tree drop tests across all 3 zones (`BEFORE_SIBLING`, `AFTER_SIBLING`, `NEST_CHILD`)
- [x] T011 [P] [US3] Add intra-tree sibling reordering and leaf path updates in `tests/e2e/test_drag_and_drop.py`
- [x] T012 [US3] Add cycle detection rejection tests (parent into child) with warning toast assertions in `tests/e2e/test_drag_and_drop.py`

**Checkpoint**: Drag-and-drop placement and cycle validation mathematically verified.

---

## Phase 6: User Story 4 & 5 - Data Types, Settings, Sidebar & Bilingual i18n (Priority: P2/P3)

**Goal**: Establish comprehensive E2E tests for all 9 data types, settings persistence, sidebar interactions, and bilingual UA/EN translation coverage.

**Independent Test**: Execute `pytest tests/e2e/test_settings_and_preferences.py tests/e2e/test_sidebar_tabs_and_resizer.py tests/e2e/test_navigation_and_i18n.py`.

### Implementation for User Stories 4 & 5

- [x] T013 [P] [US4] Expand `tests/e2e/test_settings_and_preferences.py` with custom delimiter propagation (`/`, `.`) and default data type persistence in settings modal
- [x] T014 [P] [US4] Add leaf promotion/demotion and data type badge visibility tests across all 9 standard types in `tests/unit/test_data_types.py` and `tests/e2e/test_settings_and_preferences.py`
- [x] T015 [P] [US5] Expand `tests/e2e/test_sidebar_tabs_and_resizer.py` with catalog vs paths tab switching, search filter visibility, vertical strip expand, and resizer drag/reset
- [x] T016 [US5] Expand `tests/e2e/test_navigation_and_i18n.py` with complete bilingual translation key checks (UA/EN) and toast notification visual styling assertions

**Checkpoint**: Data types, settings, sidebar, and bilingual i18n verified without gaps.

---

## Phase 7: User Story 6 & Polish - Architecture Linters & Full Quality Gate (Priority: P3)

**Purpose**: Automated architecture contracts, full regression suite execution, and quickstart validation

- [x] T017 [P] [US6] Verify Constitution Principle VIII ($\le 200$ lines) and pure domain model imports in `tests/unit/test_architecture_contracts.py`
- [x] T018 [P] Run fast quality gate check via `python scripts/check_all.py --quick`
- [x] T019 [P] Run complete 111+ test full-stack suite via `python scripts/check_all.py --full`
- [x] T020 Execute `specs/034-full-project-test-suite/quickstart.md` validation scenarios and verify zero test warnings or console errors


---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Confirms clean baseline.
- **User Story 1 (Phase 3 - MVP)**: Core Tree & View Modes.
- **User Story 2 (Phase 4)**: Multi-Sheet & Template Lifecycle.
- **User Story 3 (Phase 5)**: Drag-and-Drop & Cycle Validation.
- **User Stories 4 & 5 (Phase 6)**: Data Types, Settings, Sidebar & i18n.
- **Polish (Phase 7)**: Final full regression suite (111+ tests).

### Parallel Opportunities

- `T003`, `T004`, `T005` can run in parallel.
- `T007`, `T008` can run in parallel.
- `T010`, `T011` can run in parallel.
- `T013`, `T014`, `T015` can run in parallel.
