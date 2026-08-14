# Research & Architectural Decisions: Multi-Sheet Session Persistence & Template Auto-Sync

**Feature**: 016-multi-sheet-session-persistence-and-template-sync  
**Date**: 2026-08-14  

---

## Decision 1: Per-Sheet `WorkspaceForest` Dictionary (`sheet_forests`)

- **Context**: In previous versions, the backend held only a single `forest` instance that was replaced on every `switch_active_sheet`. Returning to a previous sheet wiped out all custom hierarchy nodes constructed by the user on that sheet.
- **Decision**: Introduce `sheet_forests: Dict[str, WorkspaceForest]` in `eel_bridge.py`.
- **Rationale**:
  1. **Zero Data Loss**: Each sheet retains its complete tree in memory. Switching back and forth restores the exact node tree, child hierarchies, and paths.
  2. **Minimal Memory Footprint**: Python tree node objects use negligible RAM (< 200KB for typical workbooks).
  3. **Multi-Sheet Export**: Enables extracting leaf paths from all modified sheets simultaneously when writing the template file.

---

## Decision 2: Multi-Sheet Template Clean Export (`export_multi_sheet_template`)

- **Context**: Exporting changes must support writing updated Row 1 headers across multiple sheets at once, rather than only 1 sheet at a time, while guaranteeing `max_row == 1` and zero data rows across all sheets.
- **Decision**: Implement `ExcelHierarchyAdapter.export_multi_sheet_template(file_path, sheet_leaf_paths_map, output_path)`.
- **Rationale**:
  - Replicates all original sheets in sequence.
  - Applies custom leaf paths for sheets present in `sheet_leaf_paths_map`.
  - Streams original headers for unedited sheets.
  - Writes to a clean `openpyxl.Workbook()` directly from scratch.

---

## Decision 3: Bound Template Path (`current_template_path`) & 1-Click Sync

- **Context**: Users previously had to open the native OS file save dialog every time they exported or switched dirty sheets. Once a template file is created, subsequent edits to other sheets should simply update the existing template file without file dialog friction.
- **Decision**:
  - Track `current_template_path: Optional[str]`.
  - On first save: establish `current_template_path` via OS save dialog (`Шаблон_<name>.xlsx`).
  - On subsequent dirty sheet switches: modal offers **[Update Template & Switch]** which directly writes the update via `eel.save_template_sync(current_template_path)` without opening the file dialog.
- **Rationale**: Reduces multi-sheet workflow friction from multiple file dialog clicks down to a single confirmation click.
