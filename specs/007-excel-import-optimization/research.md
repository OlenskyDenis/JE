# Research & Architectural Decisions: High-Performance Excel Header Streaming

**Feature**: 007-excel-import-optimization  
**Date**: 2026-08-14  

## Decision 1: `openpyxl.load_workbook(..., read_only=True, data_only=True)`

- **Context**: Standard openpyxl workbook loading builds full XML DOM trees for every sheet and every row in memory. For spreadsheets with 50,000+ data rows, this incurs high memory footprint (tens to hundreds of MBs) and slow load times (seconds).
- **Decision**: Use `openpyxl.load_workbook(file_path_or_stream, read_only=True, data_only=True)`.
- **Rationale**:
  - In read-only mode, openpyxl creates an event-driven XML pull parser (`xml.etree.ElementTree.iterparse`).
  - No cell objects or DOM elements are cached in memory.
  - Memory consumption is constant ($O(1)$) with respect to total workbook size and row count.

## Decision 2: `iter_rows(max_row=1, values_only=True)` Streaming Generator

- **Context**: We need to extract headers strictly from Row 1 and ensure rows 2+ are never processed or retained in memory.
- **Decision**: Call `sheet.iter_rows(max_row=1, values_only=True)`.
- **Rationale**:
  - `next(sheet.iter_rows(max_row=1, values_only=True), None)` returns a tuple of values strictly for the first row.
  - The streaming parser halts XML traversal immediately after the first row tag (`</row>`), never parsing subsequent rows into memory.

## Decision 3: Consecutive Empty Cell Counter & Early Cutoff Limit

- **Context**: In Excel, sheets with trailing formatting or empty styled cells can report large `max_column` values (up to 16,384 columns). Scanning thousands of empty cells wastes CPU cycles.
- **Decision**: Maintain a `consecutive_empty_count` tracking counter.
- **Algorithm**:
  - Initialize `consecutive_empty_count = 0` and `raw_headers = []`.
  - Iterate through elements in Row 1:
    - If cell value is valid (non-None and non-whitespace):
      - Reset `consecutive_empty_count = 0`
      - Append `val` to `raw_headers`
    - Else (None, empty string, or whitespace-only):
      - Increment `consecutive_empty_count += 1`
      - If `consecutive_empty_count >= 10`:
        - Terminate iteration immediately (`break`).
  - Pass `raw_headers` to `HeaderService.process_headers(raw_headers)`.

## Decision 4: Deterministic Stream Cleanup with `try...finally`

- **Context**: Read-only streaming workbooks hold open zip file descriptors.
- **Decision**: Always encapsulate streaming operations in a `try...finally` block calling `wb.close()`.
