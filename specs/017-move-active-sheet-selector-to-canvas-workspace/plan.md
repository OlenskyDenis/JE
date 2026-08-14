# Implementation Plan: Move Active Workspace Sheet Selector to Canvas Workspace

**Branch**: `017-move-active-sheet-selector-to-canvas-workspace` | **Date**: 2026-08-14 | **Spec**: [specs/017-move-active-sheet-selector-to-canvas-workspace/spec.md](spec.md)

**Input**: Feature specification from `/specs/017-move-active-sheet-selector-to-canvas-workspace/spec.md`

---

## Summary

Move the interactive **Active Workspace Sheet** dropdown selector (`#activeSheetSelector`) directly into the **Hierarchy Constructor Workspace** panel header (`.tree-panel .panel-header`) on the left canvas. Clean up the Unified Sidebar Tab 1 by removing the redundant active sheet selector, leaving only `Browse Headers From:` (`#catalogSheetSelector`), search filter, and header cards.

---

## Technical Context

**Language/Version**: HTML5, Vanilla CSS3, Vanilla JavaScript ES6+  
**Testing**: `pytest` automated test suite (`python -m pytest`)  
**Target Platform**: Desktop GUI (Windows / Chromium via Eel)  
**Constraints**: 0 regression in `isDirty` state tracking, unsaved changes modal prompts, template synchronization, and header drag-and-drop.

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I (SDD Scope Enforcement)**: PASSED. Spec and Plan authored prior to code changes.
- **Principle II (OOP & Clean State Architecture)**: PASSED. Clear separation between workspace editing target (left canvas) and header discovery source (right sidebar).
- **Principle VI (System Map First-Load & Proactive Redundancy Audit)**: PASSED. Consulted [`.specify/system_map.md`](../../.specify/system_map.md).
- **Principle VII (Proactive Red Teaming & Zero-Data Stress Testing)**: PASSED. Verified responsive layout, disabled placeholder state before file import, and dirty state switching.

---

## Project Structure

### Documentation (this feature)

```text
specs/017-move-active-sheet-selector-to-canvas-workspace/
├── spec.md              # Feature specification
├── plan.md              # Implementation plan (this file)
├── research.md          # Layout design & DOM restructuring decisions
├── quickstart.md        # Verification guide
└── checklists/
    └── requirements.md  # Quality & compliance checklist
```

### Source Code Architecture

```text
src/
└── web/
    ├── index.html       # Embeds #activeSheetSelector in .panel-header; cleans #tabContentCatalog
    ├── css/style.css    # .workspace-sheet-picker, .workspace-sheet-label, .workspace-sheet-select
    └── js/app.js        # Retains #activeSheetSelector bindings, removes obsolete activeSheetBadge references
```

---

## Implementation Sequence

### Phase 1: DOM & Markup Restructuring (`src/web/index.html`)
1. In `src/web/index.html`:
   - In `.tree-panel .panel-header .panel-title-group`: Replace `#activeSheetBadge` with `.workspace-sheet-picker` containing `<select id="activeSheetSelector">`.
   - In `#tabContentCatalog`: Remove the redundant Active Workspace Sheet `.form-group`.

### Phase 2: Design System & Styling (`src/web/css/style.css`)
1. Add `.workspace-sheet-picker`, `.workspace-sheet-label`, and `.workspace-sheet-select` styling with dark theme accents, compact padding, and responsive text truncation.

### Phase 3: Controller Updates (`src/web/js/app.js`)
1. Remove obsolete DOM references to `this.activeSheetBadge`.
2. Verify all `activeSheetSelector` change listeners, options population, and dirty modal triggers work seamlessly.

### Phase 4: System Map Sync & Quality Assurance
1. Update [`.specify/system_map.md`](../../.specify/system_map.md).
2. Run full pytest suite `python -m pytest` (48/48 tests).
3. Execute end-to-end manual verification per `quickstart.md`.

---

## Complexity Tracking

| Dimension | Risk / Effort | Mitigation |
|---|---|---|
| DOM Reorganization | Negligible | Preserves `id="activeSheetSelector"` attribute |
| UI Overflow on Narrow Canvas | Low | Max-width constraint and text truncation on select element |
