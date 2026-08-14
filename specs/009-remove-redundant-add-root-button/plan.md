# Implementation Plan: Relocate Root Creation to Canvas Empty State & Streamline Workspace Header

**Branch**: `009-remove-redundant-add-root-button` | **Date**: 2026-08-14 | **Spec**: [specs/009-remove-redundant-add-root-button/spec.md](spec.md)

**Input**: Feature specification from `/specs/009-remove-redundant-add-root-button/spec.md`

---

## Summary

Streamline the Hierarchy Constructor Workspace panel header by removing the redundant `#btnAddRoot` button and relocating the root node creation action into `#treeEmptyState` via `#btnCreateRootEmpty`. This guarantees a clean, modern panel header layout while preserving a 1-click clean-slate creation pathway when launching the app without an Excel file.

---

## Technical Context

**Language/Version**: HTML5 / Vanilla JS / CSS  
**Testing**: `pytest` (Regression testing)  
**Target Platform**: Desktop (Windows / Chrome via Eel)  
**Constraints**: Zero console errors, seamless coexistence with auto-import and child node creation  

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I (SDD Scope Enforcement)**: PASSED. Spec, plan, research, and quickstart produced prior to implementation.
- **Principle II (OOP & SOLID)**: PASSED. Decouples panel header presentation from canvas empty state actions.
- **Principle VI (Global System Map & Architecture Hygiene)**: PASSED. System map in [`.specify/system_map.md`](../../.specify/system_map.md) consulted and updated.
- **Principle VII (Proactive Red Teaming & Zero-Data Stress Testing)**: PASSED. Evaluated clean-slate (zero-data / no file) scenario and integrated actionable `#btnCreateRootEmpty` to prevent user deadlock.

---

## Project Structure

### Documentation (this feature)

```text
specs/009-remove-redundant-add-root-button/
├── spec.md              # Feature specification
├── plan.md              # Implementation plan (this file)
├── research.md          # Architectural decisions & Red Teaming evaluation
├── quickstart.md        # Verification workflow
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code Architecture

```text
src/
└── web/
    ├── index.html       # Remove #btnAddRoot from .panel-header; add #btnCreateRootEmpty in #treeEmptyState
    ├── js/
    │   └── app.js       # Replace #btnAddRoot click listener with #btnCreateRootEmpty listener
    └── css/
        └── style.css    # Style button inside empty-state container
```

---

## Implementation Sequence

### Phase 1: HTML & CSS Updates
1. In `src/web/index.html`:
   - Remove `<button id="btnAddRoot">` from `<div class="panel-header">`.
   - Add `<button id="btnCreateRootEmpty" class="btn btn-primary btn-sm mt-3">` inside `<div id="treeEmptyState">`.
   - Update empty state description copy.
2. In `src/web/css/style.css`:
   - Ensure clean spacing for action buttons placed inside `.empty-state`.

### Phase 2: JavaScript Controller Refactoring
1. In `src/web/js/app.js`:
   - Replace `#btnAddRoot` event listener with `#btnCreateRootEmpty` listener calling `this.openAddModal(null, "Create Root Node")`.

### Phase 3: System Map Update & Regression Verification
1. Update `.specify/system_map.md` to reflect the updated UI components.
2. Run `python -m pytest` to verify 0 regressions.

---

## Complexity Tracking

Zero architectural complexity. Pure UI refinement delivering enhanced UX and eliminating header clutter.
