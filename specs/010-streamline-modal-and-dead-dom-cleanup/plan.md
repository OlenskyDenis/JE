# Implementation Plan: Streamline Creation Modal & Dead DOM Cleanup

**Branch**: `010-streamline-modal-and-dead-dom-cleanup` | **Date**: 2026-08-14 | **Spec**: [specs/010-streamline-modal-and-dead-dom-cleanup/spec.md](spec.md)

**Input**: Feature specification from `/specs/010-streamline-modal-and-dead-dom-cleanup/spec.md`

---

## Summary

Streamline the node creation modal by removing the redundant "Node Type" (Folder/Leaf) radio button group, delete the orphaned `#excelFileInput` DOM element and unused controller references, and clean up drag-and-drop payload flags to achieve 100% alignment with the unified dynamic `HierarchyNode` architecture.

---

## Technical Context

**Language/Version**: HTML5 / Vanilla JS / CSS  
**Testing**: `pytest` (Regression suite)  
**Target Platform**: Desktop (Windows / Chrome via Eel)  
**Constraints**: Zero console errors, seamless modal submission, preservation of all 46 existing tests  

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I (SDD Scope Enforcement)**: PASSED. Spec, plan, research, and quickstart produced prior to implementation.
- **Principle II (OOP & SOLID)**: PASSED. Eliminates static typing artifacts from presentation layers to reflect the unified dynamic domain model.
- **Principle VI (System Map First-Load & Proactive Redundancy Audit)**: PASSED. Directly executes the findings from [`.specify/memory/system_map_audit.md`](../../.specify/memory/system_map_audit.md).
- **Principle VII (Proactive Red Teaming & Zero-Data Stress Testing)**: PASSED. Verified that single-field modal streamlines clean-slate workflows with zero deadlocks.

---

## Project Structure

### Documentation (this feature)

```text
specs/010-streamline-modal-and-dead-dom-cleanup/
├── spec.md              # Feature specification
├── plan.md              # Implementation plan (this file)
├── research.md          # Architectural decisions & audit reconciliation
├── quickstart.md        # Verification workflow
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code Architecture

```text
src/
└── web/
    ├── index.html       # Remove .radio-group (Node Type) from #nodeModal; remove #excelFileInput
    ├── js/
    │   ├── app.js       # Remove this.excelFileInput; simplify submitAddModal() to call eel.add_node
    │   └── drag_drop.js # Clean up isContainer: false from drag payloads
    └── css/
        └── style.css    # Clean up obsolete .radio-group styling if needed
```

---

## Implementation Sequence

### Phase 1: HTML Cleanup (`src/web/index.html`)
1. In `src/web/index.html`:
   - Remove `<div class="form-group"><label>Node Type</label>...</div>` from `#nodeModal`.
   - Remove `<input type="file" id="excelFileInput" accept=".xlsx" style="display:none">`.

### Phase 2: JavaScript Refactoring (`src/web/js/`)
1. In `src/web/js/app.js`:
   - Remove `this.excelFileInput = document.getElementById('excelFileInput');` from `initElements()`.
   - In `submitAddModal()`, remove `document.querySelector('input[name="nodeType"]:checked')` and call `eel.add_node(this.activeParentIdForModal, name)`.
2. In `src/web/js/drag_drop.js`:
   - Remove `isContainer: false` from payload initializers in `bindSidebarItem` and `getDragPayload`.

### Phase 3: System Map Sync & Regression Validation
1. Update `.specify/system_map.md` to document the streamlined modal and cleaned DOM.
2. Run `python -m pytest` to confirm 100% test pass rate across all 46 tests.

---

## Complexity Tracking

Zero architectural complexity. Pure code and DOM hygiene delivering optimal UX and technical debt reduction.
