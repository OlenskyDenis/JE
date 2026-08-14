# Feature Specification: Relocate 'Add Root Node' Button to Workspace Canvas

**Feature Branch**: `004-relocate-add-root-button`  
**Created**: 2026-08-13  
**Status**: Draft  

**Input**: User description: "Relocate the 'Add Root Node' button from its current position to the 'Hierarchy Constructor Workspace' area. Position it logically at the top of the workspace canvas (above the rendering tree), styling it as a clear action button to start or extend the hierarchy."

---

## Constitution Compliance Notice
This specification strictly adheres to the project constitution:
- **SDD Scope Enforcement**: Specification document created prior to implementation.
- **OOP & SOLID Design**: UI layout changes decouple header session actions (Import/Export) from tree constructor creation actions.
- **Library-First & TDD**: DOM structure and style updates maintain contract bindings with `app.js` event handlers.
- **Self-Contained Excel & Web UI**: Styling relies exclusively on standard Vanilla CSS tokens and Semantic HTML5 elements.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Workspace-Centric 'Add Root Node' Action (Priority: P1)

As a database designer or user creating structural hierarchies, I want the "Add Root Node" action button located directly inside the "Hierarchy Constructor Workspace" panel above the canvas, so that contextually related creation actions reside right next to the tree builder.

**Why this priority**: Improves UX context alignment by placing tree node creation controls within the canvas workspace rather than global header file session controls.

**Independent Test**: Can be tested by verifying that the "Add Root Node" button is present at the top of the workspace canvas section, is no longer in the global header bar, and clicking it opens the root node creation modal window.

**Acceptance Scenarios**:

1. **Given** the main application window loaded, **When** examining the top app header, **Then** the "Add Root Node" button is no longer present in `.app-header .toolbar-actions`.
2. **Given** the "Hierarchy Constructor Workspace" panel, **When** examining the workspace canvas header/top section, **Then** the "Add Root Node" button is visible positioned logically at the top of the panel above the tree rendering container.
3. **Given** the relocated "Add Root Node" button, **When** clicked by the user, **Then** the root node creation modal opens immediately with the "Folder / Container" node type selected by default.

---

### User Story 2 - Prominent Action Button Styling & Empty Workspace Call-to-Action (Priority: P2)

As a user starting a new tree or extending an existing structure, I want the "Add Root Node" button styled as a distinct primary action button that remains clear and accessible regardless of whether the workspace is empty or populated.

**Why this priority**: Enhances visual hierarchy, ensuring users can immediately identify how to initiate or append root nodes.

**Independent Test**: Can be tested by viewing the workspace in both empty state and populated state, confirming the button remains cleanly aligned and accessible above the tree nodes.

**Acceptance Scenarios**:

1. **Given** an empty workspace, **When** the panel renders, **Then** the "Add Root Node" button appears clearly styled at the top of the canvas, complementing the empty state guidance.
2. **Given** a workspace containing existing root and leaf nodes, **When** the panel renders, **Then** the button remains anchored at the top of the workspace canvas without overlapping or obscuring tree items.

---

## Edge Cases

- **Narrow Viewport / Small Screen Heights**: The workspace panel header and canvas action controls scale responsively without clipping or wrapping inappropriately.
- **Empty State versus Populated Canvas**: The button remains consistently accessible regardless of whether `#treeEmptyState` is visible or hidden.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST remove the "Add Root Node" button (`#btnAddRoot`) from the global `.app-header` toolbar.
- **FR-002**: System MUST place the "Add Root Node" button (`#btnAddRoot`) inside the "Hierarchy Constructor Workspace" panel (`.tree-panel`), positioned at the top of the panel above `#treeContainer`.
- **FR-003**: System MUST style `#btnAddRoot` as a primary action button featuring a plus icon, clear contrast, hover feedback, and alignment matching panel typography.
- **FR-004**: System MUST maintain the existing button ID `#btnAddRoot` to preserve seamless event listener binding in `app.js`.
- **FR-005**: System MUST ensure global `.app-header` toolbar retains "Import Excel", "Export Excel", and "Refresh Workspace" cleanly formatted.

### Key Entities

- **Workspace Header Bar**: The header and action row of the Hierarchy Constructor panel containing panel title, node count badge, and creation action button.
- **Root Node Creation Trigger**: Interactive button `#btnAddRoot` initiating root node creation modal.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of user clicks on the relocated `#btnAddRoot` trigger the root creation modal without error.
- **SC-002**: Global header toolbar and workspace panel render cleanly across viewports without overflow or overlapping elements.

---

## Assumptions

- No backend python or eel bridge modifications are required for this UI relocation.
- Existing modal workflow for node creation remains unchanged.
