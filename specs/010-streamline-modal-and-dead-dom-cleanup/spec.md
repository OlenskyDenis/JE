# Feature Specification: Streamline Creation Modal & Dead DOM Cleanup

**Feature Branch**: `010-streamline-modal-and-dead-dom-cleanup`  
**Created**: 2026-08-14  
**Status**: Draft  

**Input**: User directive: "Streamline the node creation modal by removing the redundant 'Node Type' (Folder/Leaf) radio button group, eliminate the dead 'excelFileInput' DOM element and unused references, and align modal submission logic with the unified dynamic HierarchyNode architecture."

---

## Constitution Compliance Notice
This specification strictly adheres to the project constitution:
- **Principle I (SDD Scope Enforcement)**: No source code is created, edited, or deleted during this specification phase.
- **Principle II (OOP & SOLID)**: Aligns presentation layer forms directly with the unified dynamic domain model, eliminating obsolete static typing artifacts.
- **Principle VI (System Map First-Load & Proactive Redundancy Audit)**: Grounded in the audit findings documented in [`.specify/memory/system_map_audit.md`](../../.specify/memory/system_map_audit.md) and [`.specify/system_map.md`](../../.specify/system_map.md).
- **Principle VII (Red Teaming & Zero-Data Stress Testing)**: Verified that removing the static type radio group creates zero deadlocks in zero-data or clean-slate workflows; reducing modal interaction from 2 fields to 1 field (`Node Name`) reduces cognitive load and user friction.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Frictionless Single-Input Node Creation (Priority: P1) 🎯 MVP

As a database architect creating root nodes or adding children to existing structures, I want the creation modal to prompt only for the "Node Name", so that I can quickly create nodes without making obsolete and confusing "Folder vs Leaf" static type selections.

**Why this priority**: Directly resolves the primary UI contradiction identified in the System Map Alignment Audit.

**Independent Test**: Open the application, trigger the modal via "Create Root Node" or "+ Add Child" on any node, confirm the modal contains only the "Node Name" text field and action buttons, enter a name, and submit.

**Acceptance Scenarios**:

1. **Given** the creation modal (`#nodeModal`) opened, **When** inspecting its contents, **Then** the static "Node Type" radio button group is completely absent.
2. **Given** the user enters a node name (e.g. `Customers`) and submits, **When** the node is created, **Then** it is instantiated as a dynamic `HierarchyNode` and rendered on canvas with zero client or backend errors.
3. **Given** the modal submitted without a name or with whitespace only, **When** validation executes, **Then** a warning toast ("Node name cannot be empty.") appears and the modal remains open.

---

### User Story 2 - Elimination of Dead DOM Elements and References (Priority: P2)

As a frontend maintainer, I want all obsolete DOM elements (`#excelFileInput`) and dead query selectors to be cleanly purged from the codebase, so that the DOM structure and controller remain lean and free of technical debt.

**Why this priority**: Eliminates orphaned HTML and unneeded controller properties left over from pre-native dialog iterations.

**Independent Test**: Inspect the DOM in the browser/Eel console, verifying `#excelFileInput` is not present in the DOM tree, and `app.js` contains no unneeded query selectors for `nodeType` or `excelFileInput`.

**Acceptance Scenarios**:

1. **Given** `src/web/index.html`, **When** inspected, **Then** the hidden `<input type="file" id="excelFileInput">` is removed.
2. **Given** `src/web/js/app.js`, **When** initialized, **Then** `this.excelFileInput` is not queried or stored.
3. **Given** `submitAddModal()` in `src/web/js/app.js`, **When** executed, **Then** it directly calls `eel.add_node(this.activeParentIdForModal, name)` without evaluating `nodeType`.

---

### User Story 3 - Drag-Drop Payload Hygiene (Priority: P3)

As a system architect, I want drag-and-drop payloads to omit obsolete static flags (`isContainer: false`), maintaining clean consistency with the unified dynamic model.

**Why this priority**: Enforces payload hygiene across drag sources.

**Independent Test**: Drag a header from the sidebar catalog to canvas, verifying the drag payload contains `{ isNew: true, label: headerLabel }` without static container flags.

**Acceptance Scenarios**:

1. **Given** a sidebar catalog item dragged, **When** inspecting the drag payload, **Then** only `isNew` and `label` are populated.

---

## Edge Cases

- **Special Characters in Node Name**: Inputting names with backslashes (`\`) is automatically sanitized by `HierarchyNode.sanitize_name` to forward slashes (`/`), preserving hierarchical path delimiters.
- **Empty / Whitespace Input**: Submitting blank or whitespace names continues to display a warning toast and prevents empty node creation.
- **Keyboard Navigation**: Pressing `Enter` in the `inputNodeName` field submits the modal cleanly; pressing `Escape` closes the modal.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST remove the `<div class="form-group"><label>Node Type</label>...</div>` radio group from `#nodeModal` in `src/web/index.html`.
- **FR-002**: System MUST remove `<input type="file" id="excelFileInput">` from `src/web/index.html`.
- **FR-003**: System MUST remove `this.excelFileInput` from `src/web/js/app.js`.
- **FR-004**: System MUST refactor `submitAddModal()` in `src/web/js/app.js` to eliminate `input[name="nodeType"]` query selection and invoke `eel.add_node(this.activeParentIdForModal, name)`.
- **FR-005**: System MUST clean up `isContainer` property from drag-and-drop payload builders in `src/web/js/drag_drop.js`.
- **FR-006**: System MUST update `.specify/system_map.md` to document the streamlined single-input creation modal.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 0 redundant form fields or static type selectors in `#nodeModal`.
- **SC-002**: 0 dead DOM nodes or orphaned event selectors in `src/web/`.
- **SC-003**: 100% of existing automated tests pass with 0 regressions (`python -m pytest`).
- **SC-004**: Modal creation flow completed in 1 input step (Type Name -> Enter).

---

## Assumptions

- Dynamic node upgrade/downgrade behavior (`len(children) > 0`) is fully handled by `HierarchyNode` and `WorkspaceForest`.
- Native file dialogs via `FileDialogService` completely replace all HTML file inputs.
