# Feature Specification: Relocate Root Creation to Canvas Empty State & Streamline Workspace Header

**Feature Branch**: `009-remove-redundant-add-root-button`  
**Created**: 2026-08-14  
**Status**: Draft  

**Input**: User requirement: "Option 1: Remove 'Add Root Node' button from the Hierarchy Constructor Workspace header toolbar to keep it clean. Relocate the root creation action directly into the canvas Empty State placeholder with a prominent 'Create Root Node' button, enabling seamless creation from scratch without an Excel file while auto-import works when a file is loaded."

---

## Constitution Compliance Notice
This specification strictly adheres to the project constitution:
- **Principle I (SDD Scope Enforcement)**: No source code is modified or generated during this specification phase.
- **Principle II (OOP & SOLID)**: Clean UI refactoring separating panel header display concerns from canvas empty-state action triggers.
- **Principle VI (Global System Map & Architecture Hygiene)**: System map in [`.specify/system_map.md`](../system_map.md) consulted. Streamlines the Hierarchy Constructor Workspace panel header, eliminates header clutter, and integrates intuitive empty-state onboarding.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Streamlined Workspace Header Toolbar (Priority: P1)

As a user navigating the application, I want the Hierarchy Constructor Workspace header to display a clean, uncluttered layout containing only the title and active node count badge, so that the interface feels focused and modern.

**Why this priority**: Cleans up redundant toolbar controls on the panel header.

**Independent Test**: Can be tested by opening the app and observing that the panel header for "Hierarchy Constructor Workspace" contains only the title and `0 Nodes` badge, without any header buttons.

**Acceptance Scenarios**:

1. **Given** the application loaded, **When** viewing the "Hierarchy Constructor Workspace" panel header, **Then** the `#btnAddRoot` button is no longer present in the header toolbar.
2. **Given** the panel header, **When** nodes are added or removed, **Then** the `nodeCountBadge` displays the node count cleanly next to the title.

---

### User Story 2 - Empty-State Call-to-Action for Clean-Slate Workflows (Priority: P2)

As a database architect starting a new project without an existing Excel file, I want to see a clear call-to-action button inside the empty canvas ("+ Create Root Node") so that I can easily create my first root node from scratch.

**Why this priority**: Prevents UX lockouts when opening the application with no file loaded.

**Independent Test**: Can be tested by opening the application without loading an Excel file, clicking the "Create Root Node" button in the empty canvas placeholder, entering a name in the modal, and verifying that the first root node appears on canvas and the empty state hides.

**Acceptance Scenarios**:

1. **Given** an empty workspace canvas, **When** viewing the empty state graphic, **Then** a prominent button `#btnCreateRootEmpty` ("+ Create Root Node") is visible and clickable.
2. **Given** the empty state button clicked, **When** the user enters a root node name and clicks Submit, **Then** the modal closes, the root node is rendered in the tree canvas, and the empty state is hidden.
3. **Given** a canvas with at least 1 node, **When** the user wants to expand the tree, **Then** they use the `+ Add Child` action button on existing nodes or drag from the catalog.

---

### User Story 3 - Automatic Tree Generation on Excel Import (Priority: P3)

As a user importing an existing Excel file, I want the canvas to automatically generate the full hierarchical tree on file load, completely bypassing and hiding the empty state.

**Why this priority**: Ensures zero-click automatic hierarchy generation remains the primary flow for Excel users.

**Independent Test**: Can be tested by clicking "Import Excel" and selecting a file with `Root\Folder\Leaf` headers, confirming the empty state disappears and the tree renders immediately.

**Acceptance Scenarios**:

1. **Given** the empty workspace, **When** the user imports an Excel file via "Import Excel", **Then** the empty state is immediately hidden, and the parsed tree is displayed.

---

### Edge Cases

- **Deleting All Nodes**: If the user deletes all nodes from the tree canvas, the canvas re-enters the empty state, revealing the "+ Create Root Node" button again.
- **Switching to an Empty Sheet**: If the user switches to an Excel sheet with 0 headers, the canvas enters the empty state with the "+ Create Root Node" button accessible.
- **Modal Validation**: Submitting an empty string or whitespace-only name in the creation modal defaults to `"Unnamed Node"` or prompts validation.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST remove the `<button id="btnAddRoot">` from the `.panel-header` of the tree panel in `src/web/index.html`.
- **FR-002**: System MUST add a call-to-action button `<button id="btnCreateRootEmpty" class="btn btn-primary">` inside the `#treeEmptyState` container in `src/web/index.html`.
- **FR-003**: System MUST bind a click event listener to `#btnCreateRootEmpty` in `src/web/js/app.js` that opens the modal dialog to create a root node (`openAddModal(null, "Create Root Node")`).
- **FR-004**: System MUST ensure that creating a root node from the empty state immediately renders the root node and hides the empty state placeholder.
- **FR-005**: System MUST maintain full functionality of `+ Add Child` buttons on all rendered nodes and sidebar drag-and-drop.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Clean panel header layout with 0 extraneous action buttons in the panel header toolbar.
- **SC-002**: 100% of clean-slate sessions (no Excel file) can successfully create root nodes and build subtrees in under 3 clicks.
- **SC-003**: 0 console errors or broken event listeners when initializing or interacting with the canvas.
- **SC-004**: 100% test pass rate across unit and integration tests.

---

## Assumptions

- Root nodes can also be created by dragging sidebar catalog items directly onto the canvas.
- The modal dialog handles both root node creation and child node creation with appropriate modal title and placeholder text.
