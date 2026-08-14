# Feature Specification: Hierarchy Tree Folder Collapse & Expand

**Feature Branch**: `011-tree-folder-collapse-expand`  
**Created**: 2026-08-14  
**Status**: Draft  

**Input**: User directive: "Implement collapse and expand (fold/unfold) functionality for folder-type elements in the Hierarchy Constructor Workspace, with interactive chevron toggles, preserved collapse state across re-renders, auto-expansion on NEST_CHILD drops, and global Expand All / Collapse All controls in the workspace toolbar."

---

## Constitution Compliance Notice
This specification strictly adheres to the project constitution:
- **Principle I (SDD Scope Enforcement)**: No source code is created, edited, or deleted during this specification phase.
- **Principle II (OOP & SOLID)**: Clean encapsulation of tree view UI state in the frontend rendering engine without mutating backend domain models or path generation.
- **Principle VI (System Map First-Load & Proactive Redundancy Audit)**: System map in [`.specify/system_map.md`](../../.specify/system_map.md) consulted; builds directly on top of `tree_renderer.js`, `app.js`, and `drag_drop.js`.
- **Principle VII (Red Teaming & Zero-Data Stress Testing)**: Verified that folding/unfolding is purely visual and does not alter backend tree hierarchy, leaf path calculation, or export fidelity; empty workspaces display the empty state cleanly without broken chevron listeners.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Interactive Folder Chevron Toggle (Priority: P1) 🎯 MVP

As a database architect managing complex multi-level hierarchies, I want to click an interactive chevron toggle next to any folder to collapse or expand its child elements, so that I can reduce visual clutter and focus on specific subtrees.

**Why this priority**: Core interaction feature for large tree visualization.

**Independent Test**: Load or build a tree with nested nodes (`Root -> Folder -> Leaf`), click the chevron next to `Root`, verify its child subtree collapses (`display: none` / folded state) and the chevron rotates, then click again to expand.

**Acceptance Scenarios**:

1. **Given** a folder node with $\ge 1$ children rendered on canvas, **When** inspecting the node, **Then** an interactive chevron icon is displayed to the left of the folder icon.
2. **Given** a leaf node with 0 children, **When** rendered, **Then** an empty spacer of identical width is rendered instead of a chevron, keeping vertical hierarchy indentation aligned.
3. **Given** an expanded folder, **When** the user clicks its chevron, **Then** the child container (`.tree-children`) collapses with a smooth transition, and the chevron rotates to indicate collapsed state.
4. **Given** a collapsed folder, **When** the user clicks its chevron, **Then** the child container expands and reveals its children.

---

### User Story 2 - Collapse State Preservation Across Workspace Re-renders (Priority: P2)

As a user modifying nodes, adding children, or dragging items, I want my manual folder collapse states to be preserved when the workspace re-renders, so that my customized tree view layout does not reset after every action.

**Why this priority**: Prevents UX frustration caused by full tree re-renders resetting user fold states.

**Independent Test**: Collapse a folder, add a child to a different node or delete a sibling, and verify the collapsed folder remains collapsed after UI refresh.

**Acceptance Scenarios**:

1. **Given** a folder collapsed by the user, **When** an Eel RPC operation triggers `updateUI(roots)` (e.g. adding a node, deleting a node, or reordering), **Then** the folder remains in its collapsed state upon re-render.
2. **Given** a new Excel file loaded or active sheet switched, **When** the workspace initializes, **Then** all nodes default to fully expanded.

---

### User Story 3 - Global Toolbar Controls: Expand All & Collapse All (Priority: P3)

As a user working with large sheets containing dozens of categories, I want quick "Expand All" and "Collapse All" buttons in the workspace header, so that I can instantly toggle the entire forest visibility in one click.

**Why this priority**: High-value accelerator for large multi-root trees.

**Independent Test**: Click "Collapse All" to fold all folders across all root trees, then click "Expand All" to reveal all nodes.

**Acceptance Scenarios**:

1. **Given** the workspace panel header, **When** viewing the controls, **Then** two compact icon/text buttons (`Expand All` and `Collapse All`) are accessible next to the node count badge.
2. **Given** multiple expanded folders, **When** "Collapse All" is clicked, **Then** all folders collapse simultaneously.
3. **Given** collapsed folders, **When** "Expand All" is clicked, **Then** all folders expand simultaneously.

---

### User Story 4 - Auto-Expansion on Drag-and-Drop Nesting (Priority: P4)

As a user dragging a payload into a collapsed folder (`NEST_CHILD`), I want the folder to automatically expand upon dropping, so that I receive immediate visual confirmation that the item was successfully nested.

**Why this priority**: Guarantees visual feedback during drag-and-drop operations.

**Independent Test**: Collapse a folder, drag a sidebar header item onto the folder center (`NEST_CHILD`), and confirm the folder auto-expands showing the new child.

**Acceptance Scenarios**:

1. **Given** a collapsed folder, **When** a user drops a node onto it with `NEST_CHILD` zone, **Then** the folder automatically expands to display its updated children.

---

## Edge Cases

- **Dynamically Upgraded Leaf**: When a leaf node with 0 children receives its first child, it automatically becomes a folder and renders an expanded chevron toggle.
- **Dynamically Downgraded Folder**: When a folder's last child is deleted or moved away, it downgrades to a leaf with 0 children, and its chevron toggle is replaced by an alignment spacer.
- **Empty Canvas**: When no nodes are present, "Expand All" / "Collapse All" buttons gracefully do nothing without errors.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST render an interactive chevron toggle button (`<span class="node-toggle">`) for any node where `children.length > 0` in `src/web/js/tree_renderer.js`.
- **FR-002**: System MUST render a placeholder spacing element (`<span class="node-toggle spacer">`) for nodes with 0 children to preserve visual hierarchy indentation.
- **FR-003**: System MUST toggle the `.collapsed` class on `.tree-node` and show/hide `.tree-children` when the chevron is clicked.
- **FR-004**: System MUST maintain a persistent `Set` of collapsed node IDs (`collapsedNodeIds`) in the frontend state across `updateUI()` re-renders.
- **FR-005**: System MUST add `#btnExpandAll` and `#btnCollapseAll` buttons to the Hierarchy Constructor Workspace panel header in `src/web/index.html`.
- **FR-006**: System MUST implement `expandAll()` and `collapseAll()` controller methods in `src/web/js/app.js`.
- **FR-007**: System MUST automatically remove target node ID from `collapsedNodeIds` when a `NEST_CHILD` drop occurs on that node in `src/web/js/drag_drop.js` / `app.js`.
- **FR-008**: System MUST style the chevron with smooth rotation animation and responsive hover states in `src/web/css/style.css`.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 1-click collapse and expansion of any folder subtree with smooth chevron rotation.
- **SC-002**: 100% preservation of manual folder collapse states across dynamic tree updates (node additions, deletions, renames).
- **SC-003**: 0 backend regressions — all 46 existing unit and integration tests continue to pass.
- **SC-004**: Instant (<50ms) full-tree folding and unfolding via Expand All / Collapse All buttons.

---

## Assumptions

- Folding/unfolding is a purely client-side visual state that does not affect backend data persistence or Row 1 export paths.
- Leaf path calculation in the middle panel continues to show all absolute leaf paths regardless of whether their parent folders are visually collapsed or expanded on canvas.
