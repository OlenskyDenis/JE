# Research & Architectural Decisions: Empty-State Root Node Creation & Header Cleanup

**Feature**: 009-remove-redundant-add-root-button  
**Date**: 2026-08-14  

## Decision 1: Relocation of Root Creation to Canvas Empty State (`#treeEmptyState`)

- **Context**: The user initially requested completely removing the "Add Root Node" button due to automated Excel import. Red Teaming analysis (Constitution Principle VII) revealed that complete removal would create a UX deadlock when the application is launched without an Excel file loaded (clean-slate workflow).
- **Decision**:
  - Remove `<button id="btnAddRoot">` from the panel header `.panel-header` to eliminate toolbar clutter.
  - Insert a prominent call-to-action button `<button id="btnCreateRootEmpty" class="btn btn-primary">` directly inside `#treeEmptyState`.
- **Rationale**:
  - Keeps the panel header minimal and focused on title and node count badge.
  - Guarantees zero-data / clean-slate users have a frictionless 1-click pathway to start building a tree from scratch without an Excel file.
  - When an Excel file is loaded or nodes exist, `#treeEmptyState` is hidden (`display: none`), so the button never clutters an active workspace canvas.

## Decision 2: Event Listener & Controller Refactoring (`app.js`)

- **Context**: `document.getElementById('btnAddRoot')` in `app.js` needs to be replaced to avoid runtime null-reference errors.
- **Decision**:
  - Remove event listener for `#btnAddRoot`.
  - Add event listener for `#btnCreateRootEmpty` calling `this.openAddModal(null, "Create Root Node")`.
  - Retain `openAddModal`, `closeModal`, and `submitAddModal` methods for both empty-state root creation and on-node `+ Add Child` actions.

## Decision 3: System Map Update (`.specify/system_map.md`)

- **Context**: Constitution Principle VI mandates keeping the global system map in sync.
- **Decision**: Update `.specify/system_map.md` to reflect the removal of `#btnAddRoot` from the panel header and the addition of `#btnCreateRootEmpty` within the canvas empty state.
