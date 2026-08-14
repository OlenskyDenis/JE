# Task Breakdown: High-Performance Read-Only Excel Header Streaming & Safety Limit

**Feature**: `007-excel-import-optimization`  
**Branch**: `007-excel-import-optimization`  
**Spec**: [specs/007-excel-import-optimization/spec.md](spec.md)  
**Plan**: [specs/007-excel-import-optimization/plan.md](plan.md)  

---

## Phase 1: Setup & Foundational

**Purpose**: Test fixtures and setup for streaming Excel tests

- [x] T001 [P] Verify `tests/unit/test_excel_adapter.py` test suite structure

---

## Phase 2: User Story 1 & 2 - Read-Only Streaming & 10-Empty Cutoff (Priority: P1 / P2) 🎯 MVP

**Goal**: Implement `read_only=True` streaming mode reading exclusively Row 1 via `iter_rows(max_row=1, values_only=True)` with early break on 10 consecutive empty cells in `ExcelHierarchyAdapter.read_row1_headers`.

**Independent Test**: Run unit tests on a workbook with 10,000 data rows and verify it extracts Row 1 in <50ms, and verify a 10-cell empty gap immediately stops scanning.

### Tests (TDD)
- [x] T002 [P] [US1] Write unit test `test_read_row1_headers_read_only_streaming_large_sheet` verifying fast Row 1 loading with 10,000 rows of data in Rows 2+ in `tests/unit/test_excel_adapter.py`
- [x] T003 [P] [US2] Write unit tests `test_read_row1_headers_consecutive_empty_cutoff` and `test_read_row1_headers_small_gap_allowed` in `tests/unit/test_excel_adapter.py`

### Implementation
- [x] T004 [US1/US2] Refactor `read_row1_headers` in `src/hierarchy_lib/adapters/excel_adapter.py` to use `load_workbook(..., read_only=True, data_only=True)`, `iter_rows(max_row=1, values_only=True)`, 10-consecutive-empty tracking counter, and `try...finally: wb.close()` (depends on T002, T003)

**Checkpoint**: User Stories 1 and 2 are fully functional and verified via unit tests.

---

## Phase 3: User Story 3 - Sheet Switching & End-to-End Integration (Priority: P3)

**Goal**: Confirm sheet switching and file dialog import/export flows remain fast, seamless, and leak-free.

### Tests & Integration
- [x] T005 [P] [US3] Verify Eel RPC integration in `tests/integration/test_eel_bridge.py` with multi-sheet workbook

---

## Phase 4: Polish & Regression Testing

**Purpose**: Execute full test suite and verify 0 performance or functionality regressions

- [x] T006 Run complete test suite `python -m pytest` to confirm all unit and integration tests pass cleanly with 0 errors
