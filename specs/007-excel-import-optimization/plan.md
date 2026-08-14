# Implementation Plan: High-Performance Read-Only Excel Header Streaming & Safety Limit

**Branch**: `007-excel-import-optimization` | **Date**: 2026-08-14 | **Spec**: [specs/007-excel-import-optimization/spec.md](spec.md)

**Input**: Feature specification from `/specs/007-excel-import-optimization/spec.md` and user technical guidance:
"Optimize python openpyxl loader: use 'load_workbook(..., read_only=True)' and fetch only the first row using 'iter_rows(max_row=1, values_only=True)'. Implement a tracking counter for consecutive None/empty values in the header row generator, triggering an early break when the counter hits 10. Do not load, process, or store any sheet rows past row 1."

---

## Summary

Refactor `ExcelHierarchyAdapter.read_row1_headers` to stream Excel sheets in read-only mode (`load_workbook(..., read_only=True, data_only=True)`), fetch strictly Row 1 values via `iter_rows(max_row=1, values_only=True)`, and apply an early break cutoff when 10 consecutive empty/None/whitespace cells are encountered. Rows 2+ are never loaded, parsed, or stored into memory.

---

## Technical Context

**Language/Version**: Python 3.14  
**Primary Dependencies**: `openpyxl`, `pytest`  
**Storage**: Native Excel `.xlsx` files  
**Testing**: `pytest` (Unit & Integration tests)  
**Target Platform**: Desktop (Windows / Chrome via Eel)  
**Performance Goals**: <50ms header extraction for 100,000-row sheets; <20MB memory delta  
**Constraints**: Zero Microsoft Excel installation requirement (`openpyxl` self-contained), deterministic stream closing (`try...finally`)  

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I (SDD Scope Enforcement)**: PASSED. Spec, plan, research, data model, contracts, and quickstart produced prior to implementation.
- **Principle II (OOP & SOLID)**: PASSED. Logic is encapsulated in `ExcelHierarchyAdapter` and `HeaderService`.
- **Principle III (GoF Composite Pattern)**: PASSED. Generated headers integrate directly with `WorkspaceForest` / `PathParserService`.
- **Principle IV (Library-First & TDD)**: PASSED. Comprehensive unit tests in `test_excel_adapter.py` written before code modification.
- **Principle V (Self-Contained Excel)**: PASSED. Leverages openpyxl's native read-only streaming parser.

---

## Project Structure

### Documentation (this feature)

```text
specs/007-excel-import-optimization/
├── spec.md              # Feature specification
├── plan.md              # Implementation plan (this file)
├── research.md          # Streaming decisions & early cutoff algorithm
├── data-model.md        # Adapter parameters & component diagram
├── quickstart.md        # Test execution guide
├── contracts/
│   └── excel_adapter.json # Streaming API contract
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code Architecture

```text
src/
└── hierarchy_lib/
    └── adapters/
        └── excel_adapter.py   # Refactor read_row1_headers with streaming & 10-empty cutoff

tests/
├── unit/
│   └── test_excel_adapter.py  # Unit tests for read_only streaming, cutoff, and large sheet performance
└── integration/
    └── test_eel_bridge.py     # End-to-end Eel RPC verification
```

---

## Implementation Sequence

### Phase 1: Unit Tests (TDD)
1. In `tests/unit/test_excel_adapter.py`:
   - Test: `test_read_row1_headers_read_only_streaming_large_sheet` (verifies 10,000 rows in rows 2+ does not slow down or load lower rows).
   - Test: `test_read_row1_headers_consecutive_empty_cutoff` (verifies 10 consecutive empty cells stops iteration and ignores distant cells).
   - Test: `test_read_row1_headers_small_gap_allowed` (verifies gap of <10 empty cells does not prematurely stop iteration).
   - Test: `test_read_row1_headers_entirely_empty_row` (verifies clean empty return).

### Phase 2: Core Adapter Refactoring
1. In `src/hierarchy_lib/adapters/excel_adapter.py`:
   - Refactor `read_row1_headers(file_path_or_stream, sheet_name, max_empty_consecutive=10)`:
     ```python
     wb = openpyxl.load_workbook(file_path_or_stream, read_only=True, data_only=True)
     try:
         if sheet_name not in wb.sheetnames:
             return []
         sheet = wb[sheet_name]
         raw_headers = []
         consecutive_empty = 0
         # Stream strictly Row 1
         row_generator = sheet.iter_rows(max_row=1, values_only=True)
         first_row = next(row_generator, None)
         if first_row is not None:
             for val in first_row:
                 if val is not None and str(val).strip() != "":
                     consecutive_empty = 0
                     raw_headers.append(val)
                 else:
                     consecutive_empty += 1
                     if consecutive_empty >= max_empty_consecutive:
                         break
         return HeaderService.process_headers(raw_headers)
     finally:
         wb.close()
     ```

### Phase 3: Verification & Regression Testing
1. Run `python -m pytest` to confirm all 39+ tests pass cleanly.

---

## Complexity Tracking

Zero added architectural complexity. Reduces time and memory complexity of Excel header extraction from $O(R \times C)$ to $O(C_{headers})$, where $R$ is total rows and $C_{headers} \le C$ is the number of active columns before 10 empty cells.
