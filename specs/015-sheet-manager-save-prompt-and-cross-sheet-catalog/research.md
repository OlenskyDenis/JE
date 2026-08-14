# Research & Architectural Decisions: Intuitive Sheet Management, Unsaved Changes Protection & Cross-Sheet Header Catalog

**Feature**: 015-sheet-manager-save-prompt-and-cross-sheet-catalog  
**Date**: 2026-08-14  

---

## Decision 1: Dual-Selector Architecture (Active Workspace vs Catalog Source)

- **Context**: In previous versions, changing the single `Sheet Manager` dropdown immediately destroyed the canvas tree and rebuilt it for the new sheet. This prevented users from borrowing headers from Sheet B while editing Sheet A, and caused accidental loss of work.
- **Decision**: Decouple sheet selection into two dedicated controls:
  1. `#activeSheetSelector`: Determines which sheet's hierarchy is loaded into the canvas. Protected by dirty state checking and confirmation dialogs.
  2. `#catalogSheetSelector`: Determines which sheet's headers are displayed in the sidebar catalog. Changing this control updates only `#sidebarHeaderList` and never alters the canvas tree.
- **Rationale**: Completely eliminates cognitive ambiguity and empowers users to construct cross-sheet composite database hierarchies with zero friction.

---

## Decision 2: Dirty State Machine & Interception Flow

- **Context**: Users must never lose unexported work when switching the active editing sheet.
- **Decision**:
  - Maintain `isDirty: boolean` on `App`.
  - Set `isDirty = true` on any tree mutation (`add_node`, `move_node`, `delete_node`).
  - Reset `isDirty = false` on file import, sheet discard, or successful export.
  - When `#activeSheetSelector` changes:
    - If `isDirty == true`, open `#unsavedModal` and record `pendingSwitchSheetName`. Revert dropdown display to `currentSheetName` until decision.
    - If `Cancel`, dismiss modal.
    - If `Discard & Switch`, reset `isDirty = false` and invoke `handleSwitchSheet(pendingSwitchSheetName)`.
    - If `Save & Switch`, trigger `save_file_dialog` + `export_reorganized_row1`; if successful, reset `isDirty = false` and invoke `handleSwitchSheet(pendingSwitchSheetName)`.
- **Rationale**: Industry standard unsaved changes lifecycle ensuring 100% data loss prevention.

---

## Decision 3: Cached Multi-Sheet Headers for Zero-Latency Catalog Browsing

- **Context**: Switching the catalog source to browse headers from another sheet should feel instantaneous.
- **Decision**:
  - When `eel.import_excel_file(path)` runs, return `all_headers: { sheetName: [...] }` in the RPC response.
  - Cache `all_headers` in `App.cachedAllHeaders`.
  - When `#catalogSheetSelector` changes, filter and render from `cachedAllHeaders` in < 1ms without unnecessary RPC calls. Provide `eel.get_sheet_headers(sheetName)` as fallback.
- **Rationale**: Instantaneous 60fps catalog browsing and search filtering across all sheets.
