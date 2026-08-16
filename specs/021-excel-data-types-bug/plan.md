# Implementation Plan: Pure Row-1 Streaming Excel Column Data Type Inference

**Feature Branch**: `021-excel-data-types-bug`  
**Spec**: [specs/021-excel-data-types-bug/spec.md](spec.md)  
**Created**: 2026-08-14  
**Status**: In Progress

---

## Technical Context & Architecture Overview

### Problem Statement
The application must dynamically infer standard Excel data types (`Date`, `DateTime`, `Time`, `Currency`, `Percentage`, `Integer`, `Decimal`, `Boolean`, `Text`) upon importing an Excel workbook. Crucially, in strict adherence to the project constitution, this process MUST NOT read Row 2 or any data rows (`max_row=1`). Instead, it directly inspects the column formatting metadata configured in Excel on Row 1 (`cell.number_format`, `column_dimensions[col_letter].number_format`, and `cell.data_type`).

### Architecture Strategy
1. **Unified Row-1 Ingestion in `ExcelHierarchyAdapter`**:
   - Consolidate header reading and type inference into a single openpyxl pass: `read_row1_headers_and_types(file_path_or_stream, sheet_name) -> List[Tuple[str, str]]`.
   - Reads only Row 1 (`max_row=1`) in read-only streaming mode.
   - For each column header on Row 1:
     - Extracts the sanitized header string (`HeaderService.process_headers`).
     - Inspects `cell.number_format`, `ws.column_dimensions[col_letter].number_format`, and `cell.data_type`.
     - Maps the number format string to our 9 canonical data types using regex and pattern matching.
     - Stops reading immediately after Row 1.
2. **Backend Session Ingestion (`eel_bridge.py`)**:
   - `import_excel_file` and `switch_active_sheet` call `read_row1_headers_and_types` once per sheet.
   - Populates `all_headers_meta[sheet_name]` with `[{"name": ..., "type": ...}]`.
   - Initializes each parsed leaf node in `WorkspaceForest` with its detected `data_type`.
3. **Frontend Integration**:
   - Display `.node-type-badge` in the workspace tree canvas and `Export Preview` tab.
   - Display `.header-type-tag` in the sidebar Header Catalog.
   - Preserve detected types when dragging items from the catalog into the tree.
4. **Template Export Persistence**:
   - Write custom leaf paths into Row 1 across columns and apply the corresponding openpyxl `number_format` from `EXCEL_TYPE_FORMAT_MAP`.

---

## Constitution & Principle Gates Checklist

| Constitution Principle | Evaluation | Status |
|---|---|---|
| **I. Spec-Driven Development (SDD)** | Specification approved, plan generated, source code untouched during planning. | 🟢 Passed |
| **II. OOP & SOLID Principles** | Clean separation of concerns: `ExcelHierarchyAdapter` handles Excel I/O format parsing; `HeaderService` handles header processing; `HierarchyNode` encapsulates node state and type validation. | 🟢 Passed |
| **III. Gang of Four Design Patterns** | Dynamic Composite Pattern via `HierarchyNode` (`len(children) > 0`). | 🟢 Passed |
| **IV. Library-First & TDD** | Standalone adapter functions with comprehensive unit tests written first before frontend verification. | 🟢 Passed |
| **V. Self-Contained Excel Processing** | `openpyxl` streaming execution without MS Excel installation or COM dependencies. Strictly Row 1 only (`max_row=1`). | 🟢 Passed |
| **VI. System Map & Architecture Hygiene** | Synchronized with [`.specify/system_map.md`](../../.specify/system_map.md). | 🟢 Passed |
| **VII. Red Teaming & Zero-Data Stress Testing** | Validated against header-only sheets, sparse files, custom number formats, and large files. | 🟢 Passed |

---

## Execution Phases & Artifacts

### Phase 0: Research & Number Format Pattern Mapping (`research.md`)
- Define comprehensive regex/pattern mapping for Excel `number_format` strings to the 9 standard types.
- Ensure zero regression on custom localized currency/date formats.

### Phase 1: Data Model & Quickstart Guide (`data-model.md`, `quickstart.md`)
- Document `Row1ColumnMeta`, `HierarchyNode.data_type`, and RPC data structures.
- Create automated and manual test walkthrough in `quickstart.md`.

### Phase 2: TDD Unit & Integration Tests (Red Stage)
- Update `tests/unit/test_excel_adapter.py` with tests for Row-1 column formatting detection (`read_row1_headers_and_types`).
- Update `tests/integration/test_eel_bridge.py` to verify full Row-1 type binding.

### Phase 3: Domain Implementation & Backend Bridge (Green Stage)
- Implement `read_row1_headers_and_types` in `src/hierarchy_lib/adapters/excel_adapter.py`.
- Update `import_excel_file` and `switch_active_sheet` in `src/app/eel_bridge.py`.

### Phase 4: Frontend & QA Verification
- Verify canvas badges, sidebar catalog tags, drag-and-drop inheritance, and export template persistence.
- Run full pytest test suite (57+ tests).
