# Feature Specification: Database Hierarchy Creator with Excel Integration

**Feature Branch**: `001-database-hierarchy-creator`  
**Created**: 2026-08-13  
**Last Clarified**: 2026-08-13  
**Status**: Draft  

**Input**: User description: "Build a database hierarchy creator compatible with Excel. Feature details: 1) Drag-and-drop constructor UI to build nested tree structures with infinite levels of nesting. 2) Path generator: for each leaf node, calculate and output its absolute path starting from the root, separated by backslashes (e.g., Root\Folder\Subfolder\Item). 3) Excel integration: allow importing Excel files to build hierarchies, and exporting the final tree structure with generated path strings back to Excel."

---

## Constitution Compliance Notice
This specification strictly adheres to the project constitution:
- **SDD Scope Enforcement**: No source code is generated during this phase.
- **OOP & SOLID Design**: Core models follow Composite pattern interfaces and SOLID principles.
- **Library-First & TDD**: Path calculation and hierarchy parsing are specified as a standalone core library.
- **Self-Contained Excel**: Excel processing must run without requiring Microsoft Excel installation or COM dependencies.

---

## Clarifications & Decision Log

1. **Excel Sheet Import Protocol**:
   - **Decision**: Only the first line (Row 1 / Cell A1) of each sheet in an imported Excel file is parsed as a hierarchy path string.
   - **Behavior**: The string may or may not contain backslashes (`\`). If backslashes exist (e.g., `Root\Folder\Subfolder\Item`), the importer breaks down the string into parent-child nodes to build the Composite tree. If no backslash is present, it is instantiated as a top-level root node.

2. **Excel Export Formatting**:
   - **Decision**: When exporting the tree hierarchy to Excel, elements of each path are written with **one path segment per cell, and strictly one segment per row** down the sheet column.

3. **Workspace Hierarchy Architecture**:
   - **Decision**: The system supports **Multi-Root Forest** structures. The workspace constructor UI and core library allow multiple top-level root nodes operating independently on the same canvas.

4. **Drag-and-Drop Zone Hit-Testing Rules**:
   - **Decision**: Tree target nodes use a **Three-Zone Hit Target**:
     - Top 25% height: Drop as sibling immediately *above* target node.
     - Bottom 25% height: Drop as sibling immediately *below* target node.
     - Center 50% height: Drop as child *nested inside* target node.

5. **Invalid Drag Feedback & Rejection Rules**:
   - **Decision**: Drag operations that attempt to drop a node onto itself or into any of its own descendant nodes (preventing cycles) MUST be intercepted in real-time.
   - **Behavior**: Hovering over an invalid drop target displays a red "prohibited" cursor and disables drop highlight; dropping on an invalid target smoothly snaps the node back to its original position and emits a warning toast notification.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Core Hierarchy Modeling & Path Generator Library (Priority: P1)

As a system architect or developer, I want a standalone hierarchy management library that models nodes using the Composite design pattern, supports multiple top-level root nodes (forest hierarchy), and calculates backslash-delimited absolute paths for leaf nodes (e.g., `Root\Folder\Subfolder\Item`) across infinite nesting levels.

**Why this priority**: Core domain logic and primary constitution constraint (Library-First approach). All visual drag-and-drop interfaces and Excel import/export pipelines depend on this foundational component.

**Independent Test**: Can be fully tested via standalone unit test suites that instantiate `CompositeNode` and `LeafNode` objects, perform nesting/reparenting operations, and verify generated path strings without any UI rendering or Excel file dependencies.

**Acceptance Scenarios**:
1. **Given** a root node `Root`, container `Folder`, and leaf node `Item`, **When** `Item` is added under `Folder` and `Folder` under `Root`, **Then** the computed absolute path for `Item` MUST be `Root\Folder\Item`.
2. **Given** an existing deep tree structure, **When** a container node is moved to a different parent node, **Then** all descendant leaf nodes MUST automatically reflect the new absolute path prefix upon recalculation.
3. **Given** a workspace with multiple independent top-level root nodes (`RootA` and `RootB`), **When** path generation is executed, **Then** paths for nodes under `RootA` start with `RootA` and nodes under `RootB` start with `RootB`.

---

### User Story 2 - Self-Contained Single-Line Excel Import & Export (Priority: P2)

As a data analyst or database administrator, I want to import Excel workbooks where Row 1 of each sheet defines a hierarchy path string, and export finalized hierarchies back to Excel with one path segment per cell per row, operating completely independently of Microsoft Excel desktop software.

**Why this priority**: Enables bulk data onboarding and integration with existing enterprise spreadsheets.

**Independent Test**: Can be independently tested by passing sample `.xlsx` binary buffers/files to the `ExcelHierarchyAdapter`, verifying that valid Composite node trees are instantiated on import from sheet Row 1 path strings, and asserting that generated `.xlsx` exports contain one path segment per cell/row.

**Acceptance Scenarios**:
1. **Given** an Excel file where Row 1 / Cell A1 of each sheet contains a backslash path string (e.g., `Root\Folder\Item`), **When** imported, **Then** the system MUST parse the path string and build the corresponding Composite node tree structure in memory.
2. **Given** a constructed node hierarchy, **When** exported to Excel, **Then** the adapter MUST generate an `.xlsx` file structuring each path with one element per cell, and strictly one element per row.
3. **Given** an environment without Microsoft Excel or COM interop installed, **When** import or export is executed, **Then** the processing MUST succeed seamlessly using self-contained spreadsheet libraries.

---

### User Story 3 - Interactive Three-Zone Drag-and-Drop Tree Constructor UI (Priority: P3)

As an end user, I want a visual drag-and-drop interface with three-zone hit testing (top/bottom for sibling reordering, center for child nesting) and instant validation feedback to build and modify tree hierarchies.

**Why this priority**: Provides the visual interaction layer for end users once core hierarchy modeling and file persistence contracts are fully established.

**Independent Test**: Can be independently tested using browser component tests that simulate drag events (dragStart, dragOver, drop) across top, center, and bottom target zones, verifying DOM position changes, snap-back behavior, and path badge updates.

**Acceptance Scenarios**:
1. **Given** a dragged node dropped on the center 50% of node `A`, **When** dropped, **Then** the dragged node MUST become a child of node `A` and its path preview MUST update.
2. **Given** a dragged node dropped on the top 25% of node `A`, **When** dropped, **Then** the dragged node MUST be positioned as a sibling immediately above node `A`.
3. **Given** a drag operation over an invalid target (itself or descendant), **When** hovered, **Then** the UI MUST render a prohibited cursor, and upon release, snap back to origin and display a warning toast message.

---

## Edge Cases

- **Special Characters in Node Names**: Node names with raw backslashes must be escaped or sanitized so path delimiter parsing remains unambiguous.
- **Single-Segment Sheet Paths**: Rows containing strings without backslashes (e.g. "TopFolder") instantiate top-level root nodes without parent linkages.
- **Circular Dependencies & Ancestor Dragging**: Dragging a parent into its descendant or onto itself MUST be rejected during `dragOver` validation.
- **Boundary Drop Target Calculations**: Nodes with very small vertical height (e.g. <20px) must scale hit-testing zones proportionately to prevent misclicks.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST implement tree nodes using the Object-Oriented Composite Design Pattern (`HierarchyNode`, `CompositeNode`, `LeafNode`).
- **FR-002**: The system MUST support infinite levels of hierarchy nesting without arbitrary depth limits.
- **FR-003**: The system MUST compute the absolute path for every node starting from its top-level root node down to the target node, joining segment names with backslashes (`\`).
- **FR-004**: The system MUST automatically update all descendant absolute path calculations whenever a parent node is moved, renamed, or deleted.
- **FR-005**: The system MUST support Excel file (`.xlsx`) import by reading Row 1 / Cell A1 of each sheet as a path string.
- **FR-006**: The system MUST support Excel file (`.xlsx`) export by outputting path elements with one element per cell, and strictly one element per row.
- **FR-007**: Excel processing MUST be entirely self-contained without requiring Microsoft Excel software or COM dependencies.
- **FR-008**: The system MUST support Multi-Root Forest structures allowing multiple independent top-level root nodes.
- **FR-009**: The system MUST implement a Three-Zone Hit-Testing drag-and-drop constructor UI (top/bottom 25% for sibling reorder, center 50% for child nesting).
- **FR-010**: The system MUST enforce real-time drag validation: displaying a prohibited cursor over invalid drop targets (self/descendants), snapping back on release, and showing a toast notification.

---

## Key Entities

- **HierarchyComponent (Interface/Abstract Class)**: Abstract contract for hierarchy items (`Id`, `Name`, `Parent`, `GetAbsolutePath()`).
- **CompositeNode (Class)**: Container node holding child `HierarchyComponent` objects.
- **LeafNode (Class)**: Terminal data node.
- **PathGenerator (Service)**: Algorithm for traversing parent links and building backslash-delimited paths.
- **ExcelHierarchyAdapter (Service)**: Adapter converting between single-line sheet paths, vertical segment cell rows, and Composite node trees.
- **DragDropValidator (Service/Component)**: Validates drag drop targets (preventing cycle creation and self-parenting) and calculates 3-zone hit targets.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Absolute path calculations for a hierarchy of 10,000 nodes complete in less than 300 milliseconds.
- **SC-002**: 100% of Excel import and export operations execute successfully in environments with zero Microsoft Excel software installed.
- **SC-003**: Drag-and-drop zone detection and path recalculation execute within 50 milliseconds (real-time responsiveness).
- **SC-004**: 100% of invalid drag operations (self-parenting, descendant nesting) are intercepted and rejected before DOM/state mutations occur.
- **SC-005**: Core hierarchy modeling, Composite pattern implementations, and path generation libraries achieve 100% unit test coverage prior to UI integration.

---

## Assumptions

- Backslash (`\`) is the standard, mandatory delimiter for absolute node paths.
- Excel files follow standard `.xlsx` OpenXML formats.
- HTML5 Drag and Drop API or standard pointer event libraries are supported by the client browser.
