# Implementation Plan: Intuitive Sheet Management, Unsaved Changes Protection & Cross-Sheet Header Catalog

**Branch**: `015-sheet-manager-save-prompt-and-cross-sheet-catalog` | **Date**: 2026-08-14 | **Spec**: [specs/015-sheet-manager-save-prompt-and-cross-sheet-catalog/spec.md](spec.md)

**Input**: Feature specification from `/specs/015-sheet-manager-save-prompt-and-cross-sheet-catalog/spec.md`

---

## Summary

Dramatically improve the first-time user experience and eliminate data loss by decoupling **Active Workspace Sheet Editing** from **Catalog Header Browsing**. Implement modified/dirty state tracking (`isDirty`) with an interactive **Unsaved Changes confirmation modal** (`Save & Switch`, `Discard & Switch`, `Cancel`). Add an **Active Sheet Indicator Badge** on the canvas header, provide an independent **Browse Headers From** catalog selector supporting individual or combined sheet headers without canvas resets, and clearly label Tab 2 as **Export Preview (Row 1 Paths)**.

---

## Technical Context

**Language/Version**: Python 3.14 (Backend RPC), Vanilla JavaScript / HTML5 / CSS3 (Frontend UI)  
**Testing**: `pytest` test suite (`tests/unit/*`, `tests/integration/test_eel_bridge.py`)  
**Target Platform**: Desktop GUI (Windows / Chromium via Eel)  
**Constraints**: 100% data loss prevention on sheet navigation, zero breaking changes to existing tree drag-and-drop or Excel export pipelines.

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I (SDD Scope Enforcement)**: PASSED. Spec and Plan completed prior to implementation.
- **Principle II (OOP & Clean UI State Decoupling)**: PASSED. Active workspace sheet state and catalog browsing source are cleanly isolated in `app.js`.
- **Principle VI (System Map First-Load & Proactive Redundancy Audit)**: PASSED. Consulted [`.specify/system_map.md`](../../.specify/system_map.md); preserved all existing RPC endpoints and DOM element contracts.
- **Principle VII (Proactive Red Teaming & Zero-Data Stress Testing)**: PASSED. Handled dirty state transitions, modal cancellation, scratch sessions, cross-sheet dragging, and error recovery.

---

## Project Structure

### Documentation (this feature)

```text
specs/015-sheet-manager-save-prompt-and-cross-sheet-catalog/
├── spec.md              # Feature specification (FTUX & Dual-Mode Sheet Management)
├── plan.md              # Implementation plan (this file)
├── research.md          # Architectural decisions & state machine design
├── quickstart.md        # Manual and automated verification guide
└── checklists/
    └── requirements.md  # Quality & compliance checklist
```

### Source Code Architecture

```text
src/
├── app/
│   └── eel_bridge.py        # Expose get_sheet_headers RPC & return all_headers on import
├── hierarchy_lib/
│   └── adapters/
│       └── excel_adapter.py # Unchanged (read_row1_headers already provides streaming)
└── web/
    ├── index.html           # Active Sheet Badge, #unsavedModal, separated sheet controls
    ├── css/
    │   └── style.css        # Styles for #activeSheetBadge, #unsavedModal, helper copy
    └── js/
        ├── app.js           # isDirty state machine, unsaved modal handlers, dual selectors
        └── tree_renderer.js # Unchanged
```

---

## Implementation Sequence

### Phase 1: Backend RPC Updates (`src/app/eel_bridge.py`)
1. In `src/app/eel_bridge.py`:
   - Update `import_excel_file` to extract and return `all_headers: { sheet_name: [...] }` across all workbook sheets.
   - Add `@eel.expose def get_sheet_headers(sheet_name: str)` to fetch headers for any sheet on demand.

### Phase 2: Markup & Modal Structure (`src/web/index.html`)
1. In `src/web/index.html`:
   - Add `<span class="badge-sheet" id="activeSheetBadge">Active Sheet: (None)</span>` to the workspace header.
   - In the sidebar, separate sheet controls:
     - `#activeSheetSelector`: For switching the active canvas workspace sheet.
     - `#catalogSheetSelector`: For selecting the header catalog source sheet (includes `All Sheets (Combined)`).
   - Relabel Tab 2 button `#tabBtnPaths` to `Export Preview` with subtitle/tooltip `Row 1 Output Preview`.
   - Add `#unsavedModal` markup with Cancel, Discard & Switch, and Save & Switch action buttons.

### Phase 3: CSS Styling (`src/web/css/style.css`)
1. In `src/web/css/style.css`:
   - Style `.badge-sheet` (accent border, subtle background, prominent contrast).
   - Style helper text `.form-help-text` for intuitive first-time user guidance.
   - Ensure `#unsavedModal` uses modal card and danger-highlighted discard buttons.

### Phase 4: JavaScript State Machine & Event Interceptors (`src/web/js/app.js`)
1. In `src/web/js/app.js`:
   - Add `isDirty`, `currentSheetName`, `catalogSheetName`, `pendingSwitchSheetName`, and `cachedAllHeaders` to `App` state.
   - Set `isDirty = true` on node additions, moves, and deletions; reset to `false` on import, save, or discard.
   - Intercept `#activeSheetSelector` change: if `isDirty`, show `#unsavedModal`; else switch immediately.
   - Wire `#unsavedModal` buttons: Cancel (revert dropdown), Discard & Switch (load new sheet), Save & Switch (export then load new sheet).
   - Wire `#catalogSheetSelector` change: filter and display headers from selected sheet (or all sheets) without resetting the canvas.
   - Update `#activeSheetBadge` text on active sheet updates.

### Phase 5: System Map Sync & Quality Assurance
1. Update [`.specify/system_map.md`](../../.specify/system_map.md).
2. Run full test suite `python -m pytest` to confirm 100% test pass rate.
3. Validate end-to-end manual FTUX workflow per `quickstart.md`.

---

## Complexity Tracking

| Dimension | Risk / Effort | Mitigation |
|---|---|---|
| Dirty State Tracking | Low | Hooked into existing node mutations (`handleAddHeaderNode`, `submitAddModal`, `handleMoveNode`, `handleDeleteNode`) |
| Cross-Sheet Header Fetching | Low | Streaming via existing `read_row1_headers` |
| Save Dialog Interception | Low | Uses existing `save_file_dialog` & `export_reorganized_row1` |
