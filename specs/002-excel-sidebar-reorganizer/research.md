# Research & Architectural Decisions: Excel Header Reorganization

**Feature**: `002-excel-sidebar-reorganizer`  
**Date**: 2026-08-13  
**Status**: Complete  

---

## Technical Context & Research Summary

### 1. Row 1 Header Extraction via `openpyxl`
- **Decision**: Read exclusively Row 1 (`max_row=1`) across sheets using `openpyxl` in `read_only=True` mode or standard workbook inspection.
- **Rationale**: `max_row=1` ensures extremely fast header parsing without loading cell values from large data sets below Row 1.
- **Alternatives Considered**:
  - `pandas`: Rejected because pandas adds heavy dependencies (`numpy`, `pandas`) and defaults to reading entire datasets into DataFrames.
  - `xlrd`: Rejected because it does not natively support modern `.xlsx` format.

---

### 2. Multi-Sheet Session Management
- **Decision**: Maintain a lightweight Python session object (`WorkbookHeaderSession`) that holds the workbook path, sheet names, and a cached map of sheet names to unique sorted headers.
- **Rationale**: Fast in-memory switching between sheets (<10ms) without re-parsing the Excel file on every UI click.
- **Alternatives Considered**:
  - Re-reading the `.xlsx` file from disk on every sheet dropdown change: Rejected due to unnecessary disk I/O latency.

---

### 3. Non-Destructive Drag-and-Drop UI Pattern
- **Decision**: HTML5 Drag and Drop API where sidebar items act as drag sources (`draggable="true"`), transferring text payload `header_label` to drop zones in the tree editor without modifying or removing the sidebar DOM element.
- **Rationale**: Native HTML5 drag-and-drop provides lightweight, responsive UI interaction without external UI framework overhead (Vanilla JS/CSS compliant with project design system).
- **Alternatives Considered**:
  - Destructive drop (move item): Violates requirement 4 (headers must remain reusable).
  - External JS libraries (jQuery UI, Dragula): Rejected to keep the frontend zero-dependency, fast, and maintainable.

---

### 4. Horizontal Row-1 Export & Sheet Integrity
- **Decision**: Use `openpyxl` in read-write mode to load the original workbook, target the selected sheet, overwrite Row 1 cells horizontally (A1, B1, C1...) with leaf backslash path strings (`Root\Folder\Item`), and save the workbook without altering lower rows or other worksheets.
- **Rationale**: Strictly meets Constitution Principle V (Self-contained, no MS Excel dependency) and preserves unedited sheets and lower-row data.
- **Alternatives Considered**:
  - Creating a brand-new workbook on export: Rejected because unedited sheets in multi-sheet workbooks would be lost.
