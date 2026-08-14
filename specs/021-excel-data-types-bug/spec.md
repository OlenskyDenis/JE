# Feature Specification: Pure Row-1 Streaming Excel Column Data Type Inference

**Feature Branch**: `021-excel-data-types-bug`  
**Created**: 2026-08-14  
**Status**: Approved  
**Input**: User directive: "Ні, не так, не потрібно брати два рядка, це порушую вимоги що ми користуюємось лише першим рядком. Мені потрібно щоб ти брав значення типу колонки, в екселі я можу виставити тип колонки ось по цьому принципу."

---

## Clarifications

### Session 2026-08-14
- Q: How should the column data types be determined during Excel import without loading data rows? → A: In strict accordance with the project constitution (Row 1 Only Streaming, `max_row=1`), the parser MUST NOT read Row 2 or any data rows. Instead, it directly inspects the column-level formatting metadata (`ws.column_dimensions[col_letter].number_format`), the header cell formatting (`cell.number_format`), and cell type flags (`cell.data_type`) on Row 1 to dynamically infer the configured Excel column type.

---

## Problem Assessment & Root Cause Analysis

### Background & Observed Defect
In Excel, users configure data formats for entire columns (e.g. by selecting a column and setting format to Date, Currency, Number, Percentage, etc.). During import, column elements in the Hierarchy Constructor Workspace and Sidebar Catalog defaulted to `Text` (string) because the system attempted a separate multi-row data scan instead of reading the column formatting metadata configured in Excel directly on Row 1.

### Root Cause
1. **Separation of Header Reading & Type Scanning**: Header reading was isolated in `read_row1_headers` without capturing the cell's `number_format` and `column_dimensions.number_format`.
2. **Unnecessary Multi-Row Scanning**: A secondary pass attempted to sample data cells, which violated the $O(1)$ Row-1-only streaming principle and failed on templates or sheets where formatting was set on the column structure rather than populated data cells.

### Target Solution
Consolidate Excel header ingestion and type inference into a **single, ultra-fast Row-1-only streaming pass (`max_row=1`)**:
- For each column in Row 1:
  - Extract the column header name (`cell.value`).
  - Read the column's configured number format from `ws.column_dimensions[col_letter].number_format` and `cell.number_format`.
  - Read `cell.data_type`.
  - Dynamically map the Excel number format string to one of the 9 standard types (`Date`, `DateTime`, `Time`, `Currency`, `Percentage`, `Integer`, `Decimal`, `Boolean`, `Text`).
- **Strict Constraint**: Zero data rows read (`max_row=1`). Memory usage is $O(1)$, and file import remains instantaneous even for multi-gigabyte workbooks.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Row-1 Column Format Ingestion on File Import (Priority: P1) 🎯 MVP

As a database hierarchy architect importing Excel workbooks, I want the system to infer each column's data type directly from its Excel column/header formatting in Row 1, so that leaf elements immediately reflect their configured types (e.g. `HireDate` as `Date`, `Salary` as `Currency`, `Age` as `Integer`) without reading any data rows.

**Why this priority**: Directly satisfies the user requirement and preserves Constitution Principle I (Row 1 Only Streaming) and Principle IV (Performance).

**Independent Test**: Create an Excel workbook where Column A is formatted as Currency (`"$"#,##0.00`), Column B as Date (`yyyy-mm-dd`), Column C as Integer (`0`), and Column D as Text (`@`). Import into workspace; verify leaf nodes immediately receive badges `[Currency]`, `[Date]`, `[Integer]`, and `[Text]` with zero data rows read.

**Acceptance Scenarios**:
1. **Given** an Excel sheet where Column A has header `"Revenue"` and column/cell format `'"$"#,##0.00'`, **When** imported via `import_excel_file`, **Then** the leaf node and sidebar catalog item for `"Revenue"` are assigned `data_type="Currency"`.
2. **Given** an Excel sheet where Column B has header `"StartDate"` and format `'yyyy-mm-dd'` (or standard Excel date format IDs), **When** imported, **Then** the leaf node is assigned `data_type="Date"`.
3. **Given** an Excel sheet where Column C has format `'0.00%'`, **When** imported, **Then** the leaf node is assigned `data_type="Percentage"`.
4. **Given** an Excel sheet where Column D has format `'0'` or `'#,##0'`, **When** imported, **Then** the leaf node is assigned `data_type="Integer"`.
5. **Given** an Excel sheet where Column E has format `'0.00'`, **When** imported, **Then** the leaf node is assigned `data_type="Decimal"`.
6. **Given** an Excel sheet with default general or text format (`'@'`, `'General'`), **When** imported, **Then** the leaf node is assigned `data_type="Text"`.

---

### User Story 2 - Zero-Data-Row Streaming Performance (Priority: P2)

As a user importing massive enterprise Excel workbooks (hundreds of thousands of rows), I want the parser to strictly stream only Row 1 (`max_row=1`), guaranteeing zero memory bloat and sub-second load times.

**Why this priority**: Preserves responsiveness and satisfies Constitution Principle IV (Performance & Responsiveness).

**Independent Test**: Load a 100MB workbook with 1,000,000 rows. Verify file ingestion finishes in under 500ms using minimal memory.

**Acceptance Scenarios**:
1. **Given** an Excel sheet with 1,000,000 data rows in rows 2..1,000,000, **When** imported, **Then** `openpyxl` streaming generator executes strictly with `max_row=1`, reading 0 rows past Row 1.

---

### User Story 3 - Preserved Type Fidelity in Sidebar Catalog & Drag-and-Drop (Priority: P3)

As a user dragging headers from the Excel Header Catalog into the canvas, I want catalog items to display and retain the column data types inferred from Row 1, so that newly added tree nodes receive their correct types automatically.

**Why this priority**: Delivers end-to-end type consistency across all hierarchy editing operations.

**Independent Test**: Drag a header with format `Currency` from the catalog into the tree; verify the created node has `data_type="Currency"`.

**Acceptance Scenarios**:
1. **Given** a header item in the catalog with inferred type `Date`, **When** dragged into the tree canvas, **Then** the newly instantiated node is assigned `data_type="Date"`.

---

## Edge Cases

- **Custom / Localized Date Formats**: Formats containing `yy`, `yyyy`, `dd`, `mm`, `d-mmm-yy`, `dd.mm.yyyy` safely resolve to `Date` or `DateTime`.
- **Custom Currency Formats**: Formats containing `$`, `€`, `£`, `грн`, `₽`, `¥`, `руб`, `¤` safely resolve to `Currency`.
- **General / Unspecified Format**: If `number_format` is `General` or None, defaults cleanly to `Text`.
- **Consecutive Empty Headers**: Trailing empty columns after 10 consecutive blanks in Row 1 are safely truncated per the existing standard cutoff.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `ExcelHierarchyAdapter` MUST implement a unified single-pass Row-1 streaming reader (`max_row=1`) that extracts header names, column dimensions `number_format`, cell `number_format`, and `cell.data_type`.
- **FR-002**: The parser MUST map Excel column number format strings to the 9 standard Excel data types: `Date`, `DateTime`, `Time`, `Currency`, `Percentage`, `Integer`, `Decimal`, `Boolean`, and `Text`.
- **FR-003**: The parser MUST NOT read Row 2 or any subsequent data rows (`max_row=1`).
- **FR-004**: `import_excel_file` and `switch_active_sheet` in `eel_bridge.py` MUST use the Row-1 reader to initialize `sheet_forests` and `all_headers_meta` with inferred data types.
- **FR-005**: All parsed leaf nodes in `WorkspaceForest` MUST have their `data_type` set from the Row 1 column format upon initial import.
- **FR-006**: The Excel Header Catalog in the sidebar MUST display and bind the inferred data type for every header item.
- **FR-007**: Dragging and dropping a catalog item into the tree canvas MUST instantiate the new node with the item's inferred data type.
- **FR-008**: Exporting templates (`save_template_sync` / `export_reorganized_row1`) MUST persist the leaf element data types as openpyxl `number_format` strings into Row 1 across all sheets.

### Key Entities

- **Row1ColumnMeta**: Encapsulates column metadata derived strictly from Row 1:
  - `name` (string): Header name from Row 1
  - `type` (string): Standard Excel data type inferred from column/cell number format
  - `column_index` (integer): 1-based column position in the worksheet
- **HierarchyNode**: Dynamic composite node encapsulating `name`, `children`, and `data_type`.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of standard Excel column formats (Date, Time, Currency, Percentage, Integer, Decimal, Text) configured in Excel are correctly detected on Row 1 import.
- **SC-002**: Workbook import reads strictly 1 row (`max_row=1`) per sheet, executing in < 500ms.
- **SC-003**: 100% pass rate across the full pytest automated test suite (57+ unit and integration tests).
- **SC-004**: Zero data rows read from Row 2+ across all sheets.
