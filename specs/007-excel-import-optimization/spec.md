# Feature Specification: High-Performance Read-Only Excel Header Streaming & Safety Limit

**Feature Branch**: `007-excel-import-optimization`  
**Created**: 2026-08-14  
**Status**: Draft  

**Input**: User description: "Optimize Excel import performance and memory usage. 1) Only load and parse Row 1 (the headers) of each sheet. All subsequent rows (Row 2+) must be completely ignored and never read into memory. 2) Open workbooks strictly in read-only streaming mode (openpyxl read_only=True) to prevent memory allocation for large sheets. 3) Implement a safety limit for column parsing in Row 1: if the parser encounters 10 consecutive empty header cells, it must immediately stop scanning and treat it as the end of the headers for that sheet."

---

## Constitution Compliance Notice
This specification strictly adheres to the project constitution:
- **SDD Scope Enforcement**: No source code is modified or generated during this specification phase.
- **OOP & SOLID Design**: Streaming extraction and safety cutoff logic are encapsulated within `ExcelHierarchyAdapter` adhering to Single Responsibility and Open/Closed principles.
- **Library-First & TDD**: Streaming header extraction and cutoff limits are defined as standalone core library features with dedicated unit and performance tests.
- **Self-Contained Excel**: File operations use `openpyxl` streaming mode (`read_only=True`) without external dependencies or COM bridges.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Read-Only Streaming Extraction of Row 1 (Priority: P1)

As a data engineer importing large Excel workbooks (e.g. 100,000+ data rows), I want the system to open files in read-only streaming mode and exclusively inspect Row 1, so that importing headers is near-instantaneous and consumes negligible memory.

**Why this priority**: Core optimization delivering massive speedups and preventing out-of-memory errors on large spreadsheets.

**Independent Test**: Can be tested by loading an Excel file with 50,000 data rows in Rows 2–50,000. Header reading must complete in <100ms with negligible RAM consumption, and no Row 2+ data must ever be read into memory.

**Acceptance Scenarios**:

1. **Given** an `.xlsx` file with large data volumes in Rows 2+, **When** the file is opened for header extraction or sheet switching, **Then** `openpyxl` opens the workbook with `read_only=True, data_only=True`.
2. **Given** the streaming reader attached to a worksheet, **When** headers are extracted, **Then** the reader exclusively evaluates `min_row=1, max_row=1` and closes the stream immediately after Row 1 extraction.
3. **Given** Row 2+ containing invalid formatting or huge payloads, **When** Row 1 is parsed, **Then** the lower rows are completely ignored and do not trigger parsing errors or memory spikes.

---

### User Story 2 - 10-Consecutive-Empty-Header Safety Cutoff (Priority: P2)

As a database architect loading sparse or wide sheets, I want header scanning in Row 1 to terminate immediately when encountering 10 consecutive empty cells, so that infinite or excessive blank column iterations (up to Excel's 16,384 column limit) are prevented.

**Why this priority**: Guards against runaway column scanning in sheets where default styles or formatting extend across thousands of empty trailing columns.

**Independent Test**: Can be tested by importing a sheet with 5 valid headers, followed by 10 empty cells, followed by arbitrary distant cells. The reader must stop scanning after the 10th consecutive empty cell and return only the first 5 headers.

**Acceptance Scenarios**:

1. **Given** a sheet where Row 1 has headers in columns 1–3, columns 4–13 are empty (10 consecutive empty cells), and column 14 has text, **When** Row 1 is scanned, **Then** the scanner stops scanning at column 13 and returns headers from columns 1–3.
2. **Given** a sheet where Row 1 has 1–9 consecutive empty cells between valid headers (e.g., Col 1 valid, Cols 2–3 empty, Col 4 valid), **When** scanned, **Then** the scanner continues scanning past the small gap and captures Col 4.
3. **Given** an entirely empty Row 1, **When** scanned, **Then** the scanner terminates after 10 empty cells (or end of row, whichever is smaller) and returns an empty list `[]`.

---

### User Story 3 - Sheet Switching & Memory Reclaim (Priority: P3)

As a user navigating multi-sheet workbooks, I want switching between sheets to stream each sheet's headers on-demand and close all file handles properly, ensuring no memory leaks or locked file handles.

**Why this priority**: Guarantees responsive UI navigation across workbooks with dozens of large sheets without accumulating memory.

**Independent Test**: Can be tested by rapidly switching between 10 different sheets in a large workbook, verifying that each sheet streams Row 1 in <50ms and memory remains flat.

**Acceptance Scenarios**:

1. **Given** a multi-sheet workbook session, **When** switching sheets via `switch_active_sheet`, **Then** the workbook is opened in read-only streaming mode, Row 1 of the target sheet is parsed with the 10-empty cutoff, and the workbook stream is closed (`wb.close()`).
2. **Given** file stream operations, **When** an exception occurs or reading completes, **Then** all underlying file resources and zip handles are guaranteed to be closed via context managers or try/finally blocks.

---

### Edge Cases

- **Trailing Formatted Empty Cells**: Sheets formatted with trailing border colors across 16,384 columns terminate scanning after 10 consecutive empty cells rather than processing all 16k columns.
- **Whitespace-Only Header Cells**: Cells containing spaces, tabs, or non-breaking whitespace are treated as empty cells for the consecutive empty counter.
- **Single-Column Sheets**: Sheets with only 1 column terminate naturally at end of row.
- **Gaps of Less Than 10 Empty Cells**: An intentional gap of 1–9 empty columns between header blocks does not trigger premature cutoff.
- **First 10 Cells Empty**: If the first 10 columns are empty, scanning aborts immediately and the sheet is treated as having no headers.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST open `.xlsx` workbooks strictly in read-only streaming mode (`openpyxl.load_workbook(..., read_only=True, data_only=True)`) during header extraction and sheet inspection.
- **FR-002**: System MUST restrict cell reading strictly to Row 1 (`min_row=1, max_row=1`), ignoring all data in Rows 2+ without reading them into memory.
- **FR-003**: System MUST maintain a consecutive empty cell counter while streaming Row 1 columns:
  - If a cell value is non-empty (non-None, non-whitespace string), the counter resets to 0.
  - If a cell value is None, empty string, or whitespace-only, the counter increments by 1.
- **FR-004**: System MUST terminate scanning Row 1 immediately upon reaching 10 consecutive empty cells (`consecutive_empty_count >= 10`).
- **FR-005**: System MUST properly close read-only workbooks (`wb.close()`) in all execution paths, including errors or early loop terminations.
- **FR-006**: System MUST pass the extracted raw header list to `HeaderService.process_headers` for standard trimming, deduplication, and sorting.

### Key Entities

- **Streaming Header Scanner**: Logic responsible for single-row streaming iteration with consecutive empty cell threshold tracking.
- **Consecutive Empty Threshold**: Constant set to `10`, representing the maximum allowable gap of empty header cells before terminating row scan.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Row 1 header extraction executes in under 50 milliseconds for sheets with 100,000 data rows in Rows 2+.
- **SC-002**: Memory consumption remains under 20MB delta regardless of file size or row count during import and sheet switching.
- **SC-003**: 100% of sheet scans terminate within 10 cells after the last valid header if trailing formatted empty columns exist.
- **SC-004**: 0 file descriptor / handle leaks across multiple import and sheet switching cycles.

---

## Assumptions

- Read-only streaming mode with `openpyxl` supports standard `.xlsx` files generated by Excel, LibreOffice, and data export tools.
- Export operations (`export_horizontal_row1_leaf_paths`) continue to open workbooks in write mode as needed to persist new headers while preserving Row 2+ and existing sheets.
- Header fields reside exclusively in Row 1.
