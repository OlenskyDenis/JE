# Task Breakdown: Preservation of Original Excel Column Sequence

**Feature**: `012-preserve-excel-column-order`  
**Branch**: `012-preserve-excel-column-order`  
**Spec**: [specs/012-preserve-excel-column-order/spec.md](spec.md)  
**Plan**: [specs/012-preserve-excel-column-order/plan.md](plan.md)  

---

## Phase 1: Setup & Foundational

**Purpose**: Audit current header service test assertions

- [x] T001 [P] Audit existing header sorting assertions in `tests/unit/test_header_service.py`

---

## Phase 2: User Story 1 & 2 (MVP) - Preservation of Left-to-Right Column Order & Stable Deduplication (Priority: P1 / P2) 🎯 MVP

**Goal**: Eliminate alphabetical sorting from `HeaderService.process_headers` and ensure tree hierarchy structures preserve the exact left-to-right column sequence of Row 1.

**Independent Test**: Pass `["Zebra\\Stripes", "Beta\\Sub", "Alpha\\Item"]` into `read_row1_headers` and `parse_header_paths`, confirming the forest roots and child arrays maintain exact order `["Zebra", "Beta", "Alpha"]`.

### Tests (TDD)
- [x] T002 [P] [US1/US2] Update unit tests in `tests/unit/test_header_service.py` to assert FIFO insertion-order preservation and stable deduplication
- [x] T004 [P] [US1] Add unit test in `tests/unit/test_path_parser.py` verifying multi-root trees and child branches preserve left-to-right column order without alphabetical reordering

### Implementation
- [x] T003 [US1/US2] Refactor `HeaderService.process_headers` in `src/hierarchy_lib/services/header_service.py` to remove `cleaned_headers.sort(...)`

**Checkpoint**: Header processing and path parsing strictly preserve natural column order from left to right.

---

## Phase 3: User Story 3 - System Map Sync & Regression Testing (Priority: P3)

**Purpose**: Update system map and verify full test suite

- [x] T005 [P] [US3] Update `.specify/system_map.md` with column sequence preservation documentation
- [x] T006 Run complete test suite `python -m pytest` to confirm all tests pass cleanly with 0 failures
