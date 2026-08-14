# Research & Architectural Decisions: Creation Modal Streamlining & Dead DOM Cleanup

**Feature**: 010-streamline-modal-and-dead-dom-cleanup  
**Date**: 2026-08-14  

## Decision 1: Single-Field Node Creation Modal (`#nodeModal`)

- **Context**: The System Map Alignment Audit identified that `#nodeModal` contained a `<div class="form-group"><label>Node Type</label>...</div>` radio group allowing users to choose "Folder" vs "Leaf". Because `HierarchyNode` dynamically determines container vs leaf status based on `len(children) > 0`, this static selection is completely ignored by the backend and misleads users.
- **Decision**:
  - Delete the entire "Node Type" radio group from `src/web/index.html`.
  - Maintain only the `Node Name` input field, title, close button, and submit/cancel buttons.
- **Rationale**: Reduces user friction to a 1-step interaction (Type name -> Press Enter), while completely aligning the UI with the dynamic domain model.

## Decision 2: Purging Dead DOM File Input (`#excelFileInput`)

- **Context**: Before native OS file dialogs were introduced in Feature 003 (`FileDialogService` via `eel.open_file_dialog()`), a hidden `<input type="file" id="excelFileInput">` was present in `index.html` and queried into `this.excelFileInput` in `app.js`.
- **Decision**:
  - Remove `<input type="file" id="excelFileInput">` from `src/web/index.html`.
  - Remove `this.excelFileInput = document.getElementById('excelFileInput');` from `src/web/js/app.js`.
- **Rationale**: Eliminates dead DOM nodes and unneeded controller properties.

## Decision 3: Controller & Drag-Drop Payload Simplification

- **Context**: `submitAddModal()` in `app.js` extracted `selectedType` and passed `isContainer` to Eel RPC. In `drag_drop.js`, sidebar drag payloads set `isContainer: false`.
- **Decision**:
  - In `app.js`, `submitAddModal()` now directly calls `eel.add_node(this.activeParentIdForModal, name)()`.
  - In `drag_drop.js`, remove `isContainer: false` from payload initializers.
- **Rationale**: Code cleanliness, zero redundant property allocations, and zero risk of null-reference exceptions on query selectors.

## Decision 4: System Map Synchronization

- **Context**: Constitution Principle VI mandates updating `.specify/system_map.md`.
- **Decision**: Update `.specify/system_map.md` component inventory to reflect the single-input creation modal.
