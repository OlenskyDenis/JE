# Task Breakdown: Dynamic HierarchyNode Unification

**Feature**: `008-dynamic-node-unification`  
**Branch**: `008-dynamic-node-unification`  
**Spec**: [specs/008-dynamic-node-unification/spec.md](spec.md)  
**Plan**: [specs/008-dynamic-node-unification/plan.md](plan.md)  

---

## Phase 1: Setup & Foundational

**Purpose**: Test scaffolding for dynamic HierarchyNode model

- [x] T001 [P] Create `tests/unit/test_composite.py` test cases for `HierarchyNode` dynamic state transitions

---

## Phase 2: User Story 1 - Dynamic Node State Transitions (Priority: P1) 🎯 MVP

**Goal**: Unify `CompositeNode` and `LeafNode` into a single `HierarchyNode` with dynamic `is_folder` and `is_container` properties evaluated from `len(children) > 0`.

**Independent Test**: Create a `HierarchyNode`, verify `is_folder == False` when 0 children, add a child to verify `is_folder == True`, remove child to verify `is_folder == False`.

### Tests (TDD)
- [x] T002 [P] [US1] Write unit tests in `tests/unit/test_composite.py` for:
  - Dynamic `is_folder` / `is_container` boolean evaluation
  - Adding child dynamically upgrades node to folder
  - Removing last child dynamically downgrades node to leaf
  - Cycle prevention check (`is_ancestor_of`)

### Implementation
- [x] T003 [US1] Implement `HierarchyNode` class in `src/hierarchy_lib/models/node.py` and alias/bridge in `src/hierarchy_lib/models/composite.py` and `leaf.py`
- [x] T004 [US1] Update `WorkspaceForest` in `src/hierarchy_lib/services/forest.py` to use `HierarchyNode` and dynamically evaluate leaf paths for nodes with `len(children) == 0`

**Checkpoint**: Core domain model is unified with dynamic state transitions.

---

## Phase 3: User Story 2 - Universal Child Addition & Drag-Drop Nesting (Priority: P2)

**Goal**: Allow adding children and dropping items via `NEST_CHILD` on ANY node, instantly upgrading the target to a folder.

**Independent Test**: Drag a sidebar header onto a leaf node (0 children) with `NEST_CHILD`, verifying it succeeds without error and the leaf becomes a folder containing the child.

### Tests & Implementation
- [x] T005 [P] [US2] Update unit tests in `tests/unit/test_forest_zone_addition.py` to verify `NEST_CHILD` onto leaf nodes
- [x] T006 [US2] Update `add_node` in `src/app/eel_bridge.py` and `PathParserService` in `src/hierarchy_lib/services/path_parser.py` to use unified `HierarchyNode`
- [x] T007 [US2] Update `src/web/js/tree_renderer.js` and `src/web/js/drag_drop.js` to render folder vs leaf icon based on `node.children.length > 0`, and provide universal `+ Add Child` button and `NEST_CHILD` drop zone on all nodes

---

## Phase 4: User Story 3 - Dynamic Leaf Path Generation & Export Fidelity (Priority: P3)

**Goal**: Confirm dynamic leaf paths correctly identify all terminal endpoints with 0 children and export cleanly to Excel.

### Tests & Verification
- [x] T008 [P] [US3] Verify dynamic leaf path collection in `tests/unit/test_path_generator.py` and `tests/unit/test_excel_adapter.py`

---

## Phase 5: Polish & Regression Testing

**Purpose**: Execute full regression test suite

- [x] T009 [P] Update integration tests in `tests/integration/test_eel_bridge.py` for dynamic node operations
- [x] T010 Run complete test suite `python -m pytest` to confirm all unit and integration tests pass cleanly with 0 errors
