# Feature Specification: Dynamic Node Unification (Eliminate Static Folder/Leaf Typing)

**Feature Branch**: `008-dynamic-node-unification`  
**Created**: 2026-08-14  
**Status**: Draft  

**Input**: User description: "Unify Leaf and Folder elements into a single Dynamic Node class on both frontend and backend. Eliminate static Folder/Leaf typing. A node must dynamically determine its state: if it has 1 or more children, it is treated as a folder (catalog); if it has 0 children, it is treated as a leaf. Adding a child must automatically upgrade a node to a folder, and removing its last child must automatically downgrade it to a leaf."

---

## Constitution Compliance Notice
This specification strictly adheres to the project constitution:
- **SDD Scope Enforcement**: No source code is modified or generated during this specification phase.
- **OOP & SOLID Design**: Unification replaces separate subclass hierarchies with a single, highly cohesive `DynamicNode` model satisfying the GoF Composite Pattern dynamically.
- **Library-First & TDD**: Dynamic state transitions (upgrade/downgrade) and path calculations are defined as standalone core library behaviors tested with comprehensive unit test suites.
- **Self-Contained Excel**: File operations and leaf path round-trips continue to operate seamlessly with `openpyxl`.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Dynamic Node State Transitions (Priority: P1)

As a database hierarchy architect, I want every node to dynamically behave as a leaf when it has 0 children and as a folder when it has $\ge 1$ children, so that I never have to manually convert or differentiate between static folder and leaf node types.

**Why this priority**: Core foundation of the unification architecture. Removes rigid static typing and simplifies the mental model for tree construction.

**Independent Test**: Can be tested by creating a node with 0 children (verifying its state is leaf), adding a child to it (verifying its state immediately switches to folder/container), and removing the child (verifying its state immediately reverts to leaf).

**Acceptance Scenarios**:

1. **Given** a new node created with 0 children, **When** its state is evaluated, **Then** `is_container` is `False`, and it is treated and styled as a leaf node.
2. **Given** an existing leaf node (0 children), **When** a child node is added under it, **Then** its `is_container` property automatically becomes `True`, and it renders with folder icon and child container.
3. **Given** a folder node with exactly 1 child, **When** that child node is deleted or moved elsewhere, **Then** the parent node's `is_container` property automatically reverts to `False`, and it renders as a leaf node.

---

### User Story 2 - Universal Child Addition & Drag-Drop Nesting (Priority: P2)

As a user interacting with the workspace canvas, I want to be able to add child nodes or drag-drop items into ANY existing node (not just pre-defined folders), so that tree hierarchy building is frictionless.

**Why this priority**: Removes artificial drag-and-drop and UI action restrictions, allowing any node on canvas to receive children.

**Independent Test**: Can be tested by dragging an item from the sidebar or another tree branch and dropping it via `NEST_CHILD` onto a leaf node (0 children). The drop must succeed, upgrading the target leaf into a parent folder containing the dropped item.

**Acceptance Scenarios**:

1. **Given** any node displayed on the workspace canvas, **When** looking at its action controls, **Then** an `Add Child` button is visible and actionable for all nodes.
2. **Given** a leaf node on canvas, **When** the user drags a header or existing node onto its `NEST_CHILD` drop zone, **Then** the drop is accepted, the target node transitions to a folder, and the dropped node becomes its child.
3. **Given** any nesting operation, **When** validated, **Then** cycle prevention rules prevent adding or moving an ancestor node into its own descendant.

---

### User Story 3 - Dynamic Leaf Path Generation & Export Fidelity (Priority: P3)

As a data manager, I want the system to dynamically calculate leaf paths from all nodes currently possessing 0 children, ensuring 100% round-trip export fidelity to Excel.

**Why this priority**: Guarantees that export operations always output the terminal endpoints of the active hierarchy without relying on obsolete static flags.

**Independent Test**: Can be tested by building a multi-level hierarchy, verifying the Path Inspector lists only nodes with 0 children, and exporting to Excel to verify Row 1 contains all active leaf paths.

**Acceptance Scenarios**:

1. **Given** a hierarchy where Node A contains Node B, and Node B contains 0 children, **When** paths are calculated, **Then** `A\B` is returned as a leaf path, while `A` is not (since `A` has children).
2. **Given** a leaf node `A\B` which subsequently receives child `C`, **When** paths are recalculated, **Then** `A\B\C` becomes the leaf path, and `A\B` is no longer a terminal leaf.
3. **Given** the dynamic tree, **When** exported to Excel, **Then** all terminal leaf paths are written across Row 1 horizontally.

---

### Edge Cases

- **Root Nodes with 0 Children**: A top-level root node with 0 children is treated as a terminal leaf node (and exported as `RootName` in leaf paths).
- **Moving a Node's Only Child to Another Node**: When the single child of Parent 1 is dragged and nested under Parent 2, Parent 1 immediately reverts to a leaf, and Parent 2 becomes a folder (if it wasn't already).
- **Self & Descendant Cycle Validation**: Attempting to drag or add a parent node inside itself or any of its descendants must be rejected with a descriptive rejection toast.
- **Deep Nesting Hierarchy**: Deep chains ($N$ levels) where only the $N$-th level has 0 children correctly treat levels $1 \dots N-1$ as folders and level $N$ as the sole leaf.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST unify node modeling into a single `DynamicNode` class (or unified `CompositeNode` / `HierarchyComponent`) where a node's container status is dynamically determined by `len(children) > 0`.
- **FR-002**: System MUST eliminate static distinction between `LeafNode` and `CompositeNode` classes across backend and frontend models.
- **FR-003**: System MUST automatically evaluate `is_container = True` if `len(children) >= 1` and `is_container = False` if `len(children) == 0`.
- **FR-004**: System MUST allow adding child nodes to ANY node in the workspace forest without requiring pre-conversion or type re-instantiation.
- **FR-005**: System MUST allow `NEST_CHILD` drag-and-drop operations onto any valid target node, upgrading target to a folder upon drop.
- **FR-006**: System MUST automatically revert a node's visual rendering and container state to a leaf when its last child is removed or moved out.
- **FR-007**: System MUST calculate leaf paths for export and UI display dynamically as any node currently possessing 0 children (`len(children) == 0`).
- **FR-008**: System MUST maintain cycle validation preventing a node from being added or moved into itself or its own descendants.

### Key Entities

- **DynamicNode**: Unified component representing any node in the hierarchy. Contains `id: str`, `name: str`, `parent: Optional[DynamicNode]`, and `children: List[DynamicNode]`.
- **Dynamic State**: Evaluated property (`is_container: bool` = `len(children) > 0`).

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of nodes with $\ge 1$ children evaluate to `is_container: True` and render with folder visuals; 100% of nodes with 0 children evaluate to `is_container: False` and render with leaf visuals.
- **SC-002**: 0 type conversion errors or `LeafNode cannot nest children` exceptions when nesting items into any node.
- **SC-003**: Removing the last child from a folder transitions it to a leaf in < 16ms (within 1 frame render).
- **SC-004**: 100% test pass rate across all unit and integration test suites after unification refactor.

---

## Assumptions

- Python backend and JS frontend serialize and deserialize nodes using consistent JSON schemas (`id`, `name`, `is_container`, `absolute_path`, `children`).
- Path separator remains the backslash character `\`.
