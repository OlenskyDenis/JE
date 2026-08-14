# Research & Architectural Decisions: Full-Workbook Header Template Export via Clean Workbook Construction

**Feature**: 014-export-headers-only-clean-workbook  
**Date**: 2026-08-14  

---

## Decision 1: Fresh `openpyxl.Workbook()` Construction vs In-Memory Row Deletion

- **Context**: Previous implementations loaded the source file using `openpyxl.load_workbook(file_path_or_stream)` and modified Row 1, preserving all subsequent rows (Row 2+). To export headers only, one could either (A) load the entire file and call `sheet.delete_rows(2, sheet.max_row)` across all sheets, or (B) create a brand new `openpyxl.Workbook()` from scratch, populate only Row 1 for each sheet, and save it.
- **Decision**: Adopt **Option B (Fresh Workbook Construction)**.
- **Rationale**:
  1. **Performance**: Option A requires loading millions of cells into memory and shifting/deleting XML rows in memory, which is slow and memory-intensive ($O(Rows \times Cols)$). Option B streams only Row 1 headers ($O(Cols)$), creating a tiny, lightweight template in < 50ms.
  2. **Zero Data Leak Guarantee**: Creating a new file guarantees that no hidden rows, legacy cell values, formulas, comments, or pivot caches from the original data are leaked.
  3. **Multi-Sheet Support**: All original sheet names are preserved in exact sequence, with target sheet receiving reorganized leaf paths and other sheets receiving their original streamed Row 1 headers.

---

## Decision 2: Streaming Header Extraction for Unedited Sheets

- **Context**: For unedited sheets in the source file, we need to populate their original Row 1 headers in the new workbook.
- **Decision**: Utilize `ExcelHierarchyAdapter.read_row1_headers(file_path_or_stream, sheet_name)`.
- **Rationale**: `read_row1_headers` operates with `read_only=True`, `max_row=1`, and consecutive empty cutoffs, reading only the header row without loading data rows into memory.

---

## Decision 3: Default Filename Formatting with `Шаблон_`

- **Context**: Users need clear visual distinction between original data files and generated templates, and protection from accidental source file overwrites.
- **Decision**:
  - In `eel_bridge.py` and `app.js`, format default save dialog filename as `Шаблон_<original_basename>.xlsx`.
  - Fallback for scratch sessions without an imported file: `Шаблон_reorganized_headers_export.xlsx`.
- **Rationale**: Standard desktop convention providing immediate clarity on the template nature of the exported workbook.
