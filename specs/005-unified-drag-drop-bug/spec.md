# Feature Specification: Unified Drag-and-Drop Interaction Handler

**Feature Branch**: `005-unified-drag-drop-bug`

**Created**: 2026-08-13

**Status**: Approved

**Input**: Violation of SOLID/DRY principles in drag-and-drop interaction. The sibling positioning mechanism (above/below/inside logic) works perfectly for internal node reordering inside 'Hierarchy Constructor Workspace' but fails when dragging new headers from 'Excel Header Catalog'. The system has duplicate or inconsistent event handlers. Refactor the drag-and-drop controllers to use a single, unified interaction handler. Ensure that drops from 'Excel Header Catalog' reuse the exact same visual highlighting, Y-coordinate calculation, and sibling-versus-child insertion logic as internal workspace nodes, passing only a new node payload instead of an existing node ID.

## User Scenarios & Testing

### User Story 1 - Unified Sibling and Child Drag-and-Drop Positioning for Header Catalog Items (Priority: P1)

As a user organizing Excel headers into a tree hierarchy, I want to drag headers from the Excel Header Catalog and drop them directly above, below, or inside any target node in the Hierarchy Constructor Workspace so that I can construct complex hierarchies with precise relative positioning in a single drag action.

**Why this priority**: Currently, dragging catalog headers ignores the calculated target zone and always appends nodes as children (or fails on leaf nodes). Fixing this delivers a reliable, intuitive drag-and-drop experience.

**Independent Test**: Drag a header from the sidebar catalog to the top 25% of an existing node; verify it drops as a sibling *before* that node. Drag another header to the bottom 25%; verify it drops as a sibling *after* that node.

**Acceptance Scenarios**:

1. **Given** an existing tree node, **When** dragging a header from the Excel Header Catalog over the top 25% of the target node content, **Then** visual highlight `drop-zone-before` is displayed, and upon drop, the new header node is inserted immediately before the target node as a sibling.
2. **Given** an existing tree node, **When** dragging a header from the Excel Header Catalog over the bottom 25% of the target node content, **Then** visual highlight `drop-zone-after` is displayed, and upon drop, the new header node is inserted immediately after the target node as a sibling.
3. **Given** an existing container node, **When** dragging a header from the Excel Header Catalog over the middle 50% of the target node content, **Then** visual highlight `drop-zone-inside` is displayed, and upon drop, the new header node is nested as a child of the container node.
4. **Given** a leaf node, **When** dragging a header from the Excel Header Catalog over the middle of the leaf node, **Then** the target zone defaults to sibling insertion (before or after based on relative Y) rather than invalid child nesting.

---

### User Story 2 - Unified Drag State and Lifecycle Controller (Priority: P2)

As a developer and system maintainer, I want a single, DRY `DragDropHandler` lifecycle controller that uses a unified drag payload format for both internal node moves and catalog additions, so that event handling, hit testing, CSS highlighting, and RPC invocations follow consistent SOLID patterns.

**Why this priority**: Eliminates duplicate event handling and branching bugs, reducing technical debt and preventing feature regressions.

**Independent Test**: Perform internal node reordering and catalog header drops in succession; verify both use the same hit-testing calculations, CSS visual states, dragend cleanup, and backend node insertion rules.

**Acceptance Scenarios**:

1. **Given** any drag operation (internal node or sidebar header), **When** dragging over workspace targets, **Then** hit-testing uses the exact same Y-coordinate relative position calculation and CSS class toggles (`drop-zone-before`, `drop-zone-after`, `drop-zone-inside`, `drop-prohibited`).
2. **Given** a drop operation, **When** dropping a new node payload (`{ isNew: true, label: "..." }`) or existing node payload (`{ isNew: false, id: "..." }`), **Then** the unified drop handler processes the payload and target position `(targetId, zone)` consistently.

---

## Functional Requirements

- **FR-001**: `DragDropHandler` MUST use a single, unified payload structure for active drag operations: `{ isNew: boolean, id?: string, label?: string, isContainer?: boolean }`.
- **FR-002**: Y-coordinate hit testing and 3-zone calculation (`BEFORE_SIBLING`, `AFTER_SIBLING`, `NEST_CHILD`) MUST be identical for both internal node reordering and Excel header catalog drag operations.
- **FR-003**: Dropping a header from the Excel Header Catalog over a target node MUST respect the active drop zone (`BEFORE_SIBLING`, `AFTER_SIBLING`, `NEST_CHILD`) and insert the new node in the corresponding position.
- **FR-004**: Dropping a header from the Excel Header Catalog onto an empty workspace container MUST add the header as a top-level root node.
- **FR-005**: Backend `WorkspaceForest` and Eel RPC bridge `add_node` MUST support zone positioning (`target_id`, `zone`) when inserting new nodes.
- **FR-006**: Drag end cleanup MUST clear active drag payload state, drop highlights, and body prohibition classes for all drag operations.

## Key Entities

- **DragPayload**: Structure representing dragged item context:
  - `isNew`: boolean flag (true for catalog items, false for workspace nodes)
  - `id`: optional string (ID of existing workspace node)
  - `label`: optional string (text label of new header catalog item)
  - `isContainer`: optional boolean (default false for catalog leaf items)
- **TargetZone**: Enum or string representing position relative to target node: `'BEFORE_SIBLING'`, `'AFTER_SIBLING'`, `'NEST_CHILD'`.

## Success Criteria

- **SC-001**: 100% of header drops from Excel Header Catalog respect the calculated drop zone (`BEFORE_SIBLING`, `AFTER_SIBLING`, `NEST_CHILD`).
- **SC-002**: Elimination of separate `draggedNodeId` / `draggedSidebarHeader` split state variables in favor of unified `activeDragPayload`.
- **SC-003**: 100% passing python pytest test suite covering node addition with zone positioning.
