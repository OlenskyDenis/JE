# Implementation Plan: Multi-Sheet Session Persistence & Template Auto-Sync

**Branch**: `016-multi-sheet-session-persistence-and-template-sync` | **Date**: 2026-08-14 | **Spec**: [specs/016-multi-sheet-session-persistence-and-template-sync/spec.md](spec.md)

**Input**: Feature specification from `/specs/016-multi-sheet-session-persistence-and-template-sync/spec.md`

---

## Summary

Implement full multi-sheet session hierarchy persistence in backend memory (`sheet_forests: Dict[str, WorkspaceForest]`), ensuring that custom tree modifications on any sheet are 100% preserved when navigating across sheets. Implement bound template file synchronization (`current_template_path`), enabling 1-click template updates during sheet switching without reopening the OS file picker, and exporting all modified sheets simultaneously in a clean multi-sheet template workbook (`max_row == 1` across all sheets).

---

## Technical Context

**Language/Version**: Python 3.14 (Core Domain & RPC), Vanilla JavaScript / HTML5 / CSS3 (Frontend)  
**Testing**: `pytest` test suite (`tests/unit/test_excel_adapter.py`, `tests/integration/test_eel_bridge.py`)  
**Target Platform**: Desktop GUI (Windows / Chromium via Eel)  
**Constraints**: 0% node loss when switching between sheets, 100% clean template export with `max_row == 1`, 1-click template synchronization.

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I (SDD Scope Enforcement)**: PASSED. Spec and Plan authored prior to code changes.
- **Principle II (OOP & Clean State Architecture)**: PASSED. `ExcelHierarchyAdapter.export_multi_sheet_template` cleanly abstracts multi-sheet workbook generation, and `sheet_forests` isolates per-sheet state.
- **Principle IV (Library-First & TDD)**: PASSED. Unit tests in `test_excel_adapter.py` and integration tests in `test_eel_bridge.py` scheduled first.
- **Principle VI (System Map First-Load & Proactive Redundancy Audit)**: PASSED. Consulted [`.specify/system_map.md`](../../.specify/system_map.md).
- **Principle VII (Proactive Red Teaming & Zero-Data Stress Testing)**: PASSED. Validated multi-sheet switching, template file overwriting, and missing template recovery.

---

## Project Structure

### Documentation (this feature)

```text
specs/016-multi-sheet-session-persistence-and-template-sync/
├── spec.md              # Feature specification
├── plan.md              # Implementation plan (this file)
├── research.md          # Architectural decisions & multi-sheet state machine
├── quickstart.md        # Verification guide
└── checklists/
    └── requirements.md  # Quality & compliance checklist
```

### Source Code Architecture

```text
src/
├── app/
│   └── eel_bridge.py        # sheet_forests dictionary, current_template_path, save_template_sync RPC
├── hierarchy_lib/
│   └── adapters/
│       └── excel_adapter.py # export_multi_sheet_template (multi-sheet leaf paths export)
└── web/
    ├── index.html           # #templateStatusBadge, dynamic unsaved modal messages
    ├── css/
    │   └── style.css        # .badge-template styling
    └── js/
        └── app.js           # 1-click template sync, template status updates, multi-sheet restoration
```

---

## Implementation Sequence

### Phase 1: Core Domain Adapter Refactoring (`src/hierarchy_lib/adapters/excel_adapter.py`)
1. Add `ExcelHierarchyAdapter.export_multi_sheet_template(file_path_or_stream, sheet_leaf_paths_map, output_path)`:
   - Constructs fresh `openpyxl.Workbook()`.
   - Iterates through all workbook sheets.
   - For sheets in `sheet_leaf_paths_map`: writes custom leaf paths in Row 1.
   - For other sheets: streams original Row 1 headers.
   - Saves clean workbook with `max_row == 1` across all sheets.
2. Refactor `export_horizontal_row1_leaf_paths` to call `export_multi_sheet_template`.

### Phase 2: Backend RPC & Multi-Sheet State (`src/app/eel_bridge.py`)
1. Implement `sheet_forests: Dict[str, WorkspaceForest]` in `src/app/eel_bridge.py`.
2. In `import_excel_file`: initialize separate `WorkspaceForest` for each sheet, reset `current_template_path = None`.
3. In `switch_active_sheet`: switch active `forest` reference without losing previous sheet modifications, returning active roots and `template_path`.
4. Add `@eel.expose def save_template_sync(output_path: Optional[str] = None)`:
   - Calculates leaf paths across all `sheet_forests`.
   - Exports multi-sheet template via `export_multi_sheet_template`.
   - Updates `current_template_path`.

### Phase 3: Frontend UI & Template Auto-Sync (`src/web/`)
1. In `src/web/index.html`: Add `#templateStatusBadge` in header toolbar.
2. In `src/web/css/style.css`: Add `.badge-template` styling.
3. In `src/web/js/app.js`:
   - Bind `this.currentTemplatePath`.
   - Update `#templateStatusBadge` text.
   - When `isDirty` and switching sheets:
     - If `currentTemplatePath` is set: configure modal for 1-click `[Update Template & Switch]`, calling `eel.save_template_sync(currentTemplatePath)` directly.
     - If no template bound: open save dialog, call `eel.save_template_sync(chosenPath)`.

### Phase 4: System Map Sync & Quality Assurance
1. Update unit tests (`test_excel_adapter.py`) and integration tests (`test_eel_bridge.py`).
2. Update [`.specify/system_map.md`](../../.specify/system_map.md).
3. Run `python -m pytest` and manual verification per `quickstart.md`.

---

## Complexity Tracking

| Dimension | Risk / Effort | Mitigation |
|---|---|---|
| Multi-Sheet State Memory | Negligible | In-memory trees are extremely lightweight (< 1MB for 50 sheets) |
| Multi-Sheet Clean Export | Low | Reuses proven from-scratch openpyxl construction from Feature 014 |
| Save Dialog Bypass | Low | Direct RPC call with bound `current_template_path` |
