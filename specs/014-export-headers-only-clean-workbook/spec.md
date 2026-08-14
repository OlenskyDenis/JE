# Feature Specification: Full-Workbook Header Template Export via Clean Workbook Construction (`Шаблон_...xlsx`)

**Feature Branch**: `014-export-headers-only-clean-workbook`  
**Created**: 2026-08-14  
**Status**: Draft (Clarified with Resource-Saving Architecture)  

**Input**: User directive: "When exporting, do not delete data from the original file; create a new file entirely from scratch to conserve system resources. Preserve all sheets and original sheet names, with default filename prefixed with 'Шаблон_'."

---

## Constitution Compliance Notice
This specification strictly adheres to the project constitution:
- **Principle I (SDD Scope Enforcement)**: Only specification documentation is authored during this phase. No application source code is modified.
- **Principle II (OOP & Clean Resource-Efficient Design)**: `ExcelHierarchyAdapter` avoids heavy full-file parsing and in-place row deletions. Instead, it streams Row 1 headers from source sheets and constructs a fresh, lightweight `openpyxl.Workbook()` containing strictly sheet schemas and Row 1 headers.
- **Principle VI (System Map First-Load & Proactive Redundancy Audit)**: System map in [`.specify/system_map.md`](../../.specify/system_map.md) consulted. Traces `src/web/js/app.js` (`handleExportReorganizedRow1`) -> `src/app/eel_bridge.py` (`export_reorganized_row1`, `save_file_dialog`) -> `src/hierarchy_lib/adapters/excel_adapter.py` (`export_horizontal_row1_leaf_paths`, `read_row1_headers`).
- **Principle VII (Red Teaming & Zero-Data Stress Testing)**: Validates export against gigabyte-scale source files with 100,000+ data rows, verifying that export consumes near-zero memory and executes in milliseconds because data rows are never loaded or parsed.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Resource-Efficient Clean Template Workbook Construction (Priority: P1) 🎯 MVP

As a user working with large Excel workbooks (hundreds of megabytes or thousands of rows), I want the export process to create a brand new `.xlsx` workbook from scratch using lightweight Row 1 header streaming, so that the export finishes instantly without consuming memory or running heavy row-deletion operations, while preserving all original sheet names and structure.

**Why this priority**: Core clarified architectural requirement maximizing speed and conserving system resources.

**Independent Test**:
1. Create a 3-sheet Excel workbook `Data_Warehouse.xlsx` containing sheets `["Sales", "Inventory", "Analytics"]` with 10,000 data rows in each sheet.
2. Import the file, select `Sales`, reorganize headers into a hierarchy tree.
3. Click "Export Excel".
4. Verify that the export process:
   - Completes in < 100ms with negligible memory consumption.
   - Creates a new `.xlsx` file containing all 3 sheets: `Sales`, `Inventory`, `Analytics`.
   - `Sales` sheet contains newly reorganized leaf paths in Row 1 (`max_row == 1`).
   - `Inventory` and `Analytics` sheets contain their original Row 1 headers (`max_row == 1`).
   - All sheets contain exactly 0 data rows.

**Acceptance Scenarios**:

1. **Given** an imported multi-sheet Excel file, **When** exporting, **Then** `ExcelHierarchyAdapter` extracts sheet names and streams only Row 1 headers without loading data rows into memory.
2. **Given** the extracted sheet metadata, **When** generating the export, **Then** a brand new `openpyxl.Workbook()` is instantiated from scratch with all original sheet names created in exact original order.
3. **Given** the target active sheet being reorganized, **When** written to the new workbook, **Then** Row 1 is populated with the reorganized `leaf_paths`.
4. **Given** all other sheets from the original file, **When** written to the new workbook, **Then** their original Row 1 headers are populated into Row 1.
5. **Given** the final exported workbook, **When** inspected, **Then** every worksheet has `max_row == 1` and contains zero legacy data cells.

---

### User Story 2 - Default Export Filename with `Шаблон_` Prefix (Priority: P2)

As a user clicking "Export Excel", I want the native OS save dialog to suggest a default filename formatted as `Шаблон_<original_filename>.xlsx`, so that the template nature of the exported file is clear and the original source file is protected from accidental overwriting.

**Why this priority**: Directly requested user convention for template file naming.

**Independent Test**: Import `Enterprise_Metrics_2026.xlsx`, click "Export Excel", and verify the OS save dialog proposes `Шаблон_Enterprise_Metrics_2026.xlsx`.

**Acceptance Scenarios**:

1. **Given** an active session with imported file `Warehouse_Inventory.xlsx`, **When** clicking `btnExportExcel`, **Then** the native save dialog prompt proposes `Шаблон_Warehouse_Inventory.xlsx`.
2. **Given** an active session created from scratch (no file imported), **When** clicking `btnExportExcel`, **Then** the fallback default name `Шаблон_reorganized_headers_export.xlsx` is proposed.
3. **Given** a user choosing a save path in a non-existent folder, **When** saving, **Then** directories are created automatically and the file is saved.

---

## Edge Cases

- **Sheets with Empty Row 1**: If an unedited sheet in the source file had no headers in Row 1, a clean empty worksheet with that sheet's name is created in the template workbook.
- **Single-Sheet Source File**: A single-sheet file produces a single-sheet new workbook with the original sheet name and only Row 1 headers.
- **Scratch Session (No Source File)**: When exporting a tree built from scratch, a new workbook with a single sheet named after the active sheet (e.g. `Sheet1`) is created with the leaf paths in Row 1.
- **Overwriting Same Path**: If the user explicitly selects the original file as the destination, the file is safely replaced with the clean header-only workbook.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `ExcelHierarchyAdapter.export_horizontal_row1_leaf_paths` MUST construct a new `openpyxl.Workbook()` instance from scratch rather than modifying or deleting rows from an existing loaded file.
- **FR-002**: If a source file path is provided, `ExcelHierarchyAdapter` MUST retrieve all sheet names and stream their Row 1 headers using read-only streaming (`read_row1_headers`).
- **FR-003**: The new workbook MUST create worksheets matching all original sheet names in their exact original sequence.
- **FR-004**: In the new workbook, for the target `sheet_name`, Row 1 MUST be populated with the reorganized `leaf_paths` across columns (`A1, B1, C1...`).
- **FR-005**: In the new workbook, for all other sheets, Row 1 MUST be populated with their original streamed headers across columns (`A1, B1, C1...`).
- **FR-006**: Every worksheet in the newly created workbook MUST contain strictly `max_row <= 1` with 0 rows of data.
- **FR-007**: `App.handleExportReorganizedRow1` in `src/web/js/app.js` and `eel_bridge.py` MUST suggest a default save filename formatted as `Шаблон_<original_basename>.xlsx` (fallback: `Шаблон_reorganized_headers_export.xlsx`).
- **FR-008**: All test suites (`tests/unit/test_excel_adapter.py`, `tests/unit/test_excel_export.py`, `tests/integration/test_eel_bridge.py`) MUST be updated to verify clean workbook instantiation, multi-sheet retention, and `Шаблон_` filename formatting.
- **FR-009**: System map in [`.specify/system_map.md`](../../.specify/system_map.md) MUST be updated to document clean template workbook generation from scratch.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Zero data rows exist anywhere in the exported workbook (`max_row <= 1` across all sheets).
- **SC-002**: 100% of sheet names and sheet sequences from the original file are preserved in the newly constructed workbook.
- **SC-003**: Export performance remains $O(H)$ where $H$ is the total count of headers, completing in < 100ms regardless of how many thousands of data rows were in the original file.
- **SC-004**: 100% of automated tests pass cleanly (`python -m pytest`).

---

## Assumptions

- Read-only streaming via `read_row1_headers` is used to extract headers from non-active sheets without parsing data rows.
- The `Шаблон_` prefix is standard UTF-8 text.
