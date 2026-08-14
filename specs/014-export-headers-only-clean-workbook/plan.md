# Implementation Plan: Full-Workbook Header Template Export via Clean Workbook Construction (`Шаблон_...xlsx`)

**Branch**: `014-export-headers-only-clean-workbook` | **Date**: 2026-08-14 | **Spec**: [specs/014-export-headers-only-clean-workbook/spec.md](spec.md)

**Input**: Feature specification from `/specs/014-export-headers-only-clean-workbook/spec.md`

---

## Summary

Refactor the Excel export architecture to construct a brand new, clean `openpyxl.Workbook()` entirely from scratch during export instead of modifying/deleting data from the source file. The new workbook replicates all original sheet names in their exact sequence, writes the newly reorganized leaf paths into Row 1 of the active sheet, and writes original streamed Row 1 headers for all other sheets, guaranteeing zero data rows in Row 2+ (`max_row == 1`). Additionally, format the proposed default save filename with the prefix `Шаблон_<original_filename>.xlsx`.

---

## Technical Context

**Language/Version**: Python 3.14 (Core Domain & RPC), Vanilla JavaScript / HTML5 (Frontend)  
**Frameworks/Libraries**: openpyxl (Streaming read & clean workbook generation), Eel (RPC)  
**Testing**: `pytest` test suite (`tests/unit/test_excel_adapter.py`, `tests/unit/test_excel_export.py`, `tests/integration/test_eel_bridge.py`)  
**Target Platform**: Desktop GUI (Windows / Chromium via Eel)  
**Constraints**: Zero data row leakage (`max_row <= 1` across all exported sheets), sub-100ms export execution time, 100% test pass rate.

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I (SDD Scope Enforcement)**: PASSED. Spec, plan, research, and quickstart produced prior to implementation.
- **Principle II (OOP & Clean Resource-Efficient Design)**: PASSED. Fresh workbook creation cleanly separates schema extraction from data storage, eliminating wasteful in-memory row deletions.
- **Principle IV (Library-First & TDD)**: PASSED. Unit tests in `test_excel_adapter.py` and `test_excel_export.py` updated to verify multi-sheet schema preservation with `max_row == 1`.
- **Principle VI (System Map First-Load & Proactive Redundancy Audit)**: PASSED. Consulted [`.specify/system_map.md`](../../.specify/system_map.md); traced `ExcelHierarchyAdapter` -> `eel_bridge.py` -> `app.js`.
- **Principle VII (Proactive Red Teaming & Zero-Data Stress Testing)**: PASSED. Verified that fresh workbook creation operates with $O(H)$ performance (where $H$ is total headers) regardless of source file data size (up to 100,000+ data rows).

---

## Project Structure

### Documentation (this feature)

```text
specs/014-export-headers-only-clean-workbook/
├── spec.md              # Feature specification
├── plan.md              # Implementation plan (this file)
├── research.md          # Architectural decisions & performance comparison
├── quickstart.md        # Verification workflows
└── checklists/
    └── requirements.md  # Quality & compliance checklist
```

### Source Code Architecture

```text
src/
├── app/
│   └── eel_bridge.py        # save_file_dialog default filename with Шаблон_ prefix
├── hierarchy_lib/
│   └── adapters/
│       └── excel_adapter.py # export_horizontal_row1_leaf_paths clean workbook construction
└── web/
    └── js/
        └── app.js           # Passes Шаблон_<fileName> to save_file_dialog on export
tests/
├── integration/
│   └── test_eel_bridge.py   # Assert clean template export & default name
└── unit/
    ├── test_excel_adapter.py # Assert multi-sheet schema retention & max_row == 1
    └── test_excel_export.py  # Assert clean workbook output
```

---

## Implementation Sequence

### Phase 1: Test Suite Updates (TDD)
1. In `tests/unit/test_excel_adapter.py` and `tests/unit/test_excel_export.py`:
   - Update tests to assert that `export_horizontal_row1_leaf_paths` creates a clean workbook containing all sheets from the source file.
   - Assert that target sheet has Row 1 with leaf paths and `max_row == 1`.
   - Assert that other sheets have their original Row 1 headers and `max_row == 1` (zero data rows).
2. In `tests/integration/test_eel_bridge.py`:
   - Verify `save_file_dialog` proposes `Шаблон_<basename>.xlsx`.

### Phase 2: Core Adapter Implementation
1. In `src/hierarchy_lib/adapters/excel_adapter.py`:
   - Refactor `export_horizontal_row1_leaf_paths` to construct a new `openpyxl.Workbook()`.
   - If source file exists, retrieve all sheet names via `get_sheet_names`.
   - Create worksheets for all original sheet names in exact order.
   - For target sheet: write `leaf_paths` to Row 1 (`col_idx=1..N`).
   - For other sheets: stream original Row 1 headers via `read_row1_headers` and write to Row 1.
   - Save clean workbook to `output_path`.

### Phase 3: RPC Bridge & UI Filename Formatting
1. In `src/app/eel_bridge.py`:
   - Update `save_file_dialog` to suggest `Шаблон_<basename>.xlsx` if an active Excel file is loaded.
2. In `src/web/js/app.js`:
   - Track `this.currentFileName` on file import and pass `Шаблон_${this.currentFileName}` to `eel.save_file_dialog()`.

### Phase 4: System Map Sync & Quality Assurance
1. Update `.specify/system_map.md` to document the clean template export architecture and `Шаблон_` filename prefix.
2. Run full test suite `python -m pytest` to verify 100% test pass rate.
3. Validate end-to-end manual workflow per `quickstart.md`.

---

## Complexity Tracking

| Dimension | Risk / Effort | Mitigation |
|---|---|---|
| Multi-Sheet Header Streaming | Low | `read_row1_headers` already uses fast `read_only=True` streaming |
| Memory Overhead | Extremely Low | Only Row 1 headers are ever read and created |
| Filename Encoding | Low | Standard UTF-8 encoding for `Шаблон_` prefix |
