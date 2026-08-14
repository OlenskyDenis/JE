# Task Breakdown: Tree Folder Collapse & Expand

**Feature**: `011-tree-folder-collapse-expand`  
**Branch**: `011-tree-folder-collapse-expand`  
**Spec**: [specs/011-tree-folder-collapse-expand/spec.md](spec.md)  
**Plan**: [specs/011-tree-folder-collapse-expand/plan.md](plan.md)  

---

## Phase 1: Setup & Foundational

**Purpose**: Verify tree node DOM structure and styling foundation

- [x] T001 [P] Verify tree node CSS hierarchy and DOM layout in `src/web/index.html` and `src/web/css/style.css`

---

## Phase 2: User Story 1 (MVP) - Interactive Folder Chevron Toggle (Priority: P1) 🎯 MVP

**Goal**: Render interactive chevrons on folders with smooth rotation and child container collapsing/expanding.

**Independent Test**: Load tree with folder and leaf nodes, click chevron next to a folder, confirm subtree hides/shows with rotating chevron, and confirm leaf nodes have matching indentation spacing without chevrons.

### Implementation
- [x] T002 [P] [US1] Update `createNodeElement` in `src/web/js/tree_renderer.js` to render `<button class="node-toggle">` on folders and `<span class="node-toggle-spacer">` on leaf nodes
- [x] T003 [P] [US1] Add CSS styles for `.node-toggle`, `.chevron-icon` rotation (`transform: rotate(-90deg)` when collapsed), `.node-toggle-spacer`, and `.tree-node.collapsed > .tree-children { display: none; }` in `src/web/css/style.css`
- [x] T004 [US1] Bind click event listener on `.node-toggle` in `src/web/js/app.js` to toggle `.collapsed` on the parent `.tree-node`

**Checkpoint**: Individual folder collapse and expand is fully functional with smooth animations.

---

## Phase 3: User Story 2 & 4 - State Preservation & Auto-Expansion on Drop (Priority: P2 / P4)

**Goal**: Preserve manual folding states across `updateUI()` re-renders and auto-expand folders when receiving a `NEST_CHILD` drop.

**Independent Test**: Collapse a folder, add a child to a different node, verify the collapsed folder remains collapsed after re-render; drag a new item onto the collapsed folder, verify it auto-expands.

### Implementation
- [x] T005 [P] [US2] Maintain `this.collapsedNodeIds = new Set()` in `src/web/js/app.js`, pass it to `TreeRenderer.renderTree`, and apply `.collapsed` class during DOM generation
- [x] T006 [US4] Auto-remove `targetId` from `this.collapsedNodeIds` on `NEST_CHILD` drops in `src/web/js/app.js` to expand the target folder upon drop

---

## Phase 4: User Story 3 - Global Toolbar Controls: Expand All & Collapse All (Priority: P3)

**Goal**: Provide 1-click global forest collapse and expansion in the workspace toolbar.

**Independent Test**: Click "Collapse All" to fold all folders across the workspace, click "Expand All" to reveal all branches.

### Implementation
- [x] T007 [P] [US3] Add `#btnExpandAll` and `#btnCollapseAll` toolbar buttons with SVG icons inside the `.panel-header` of `tree-panel` in `src/web/index.html`
- [x] T008 [US3] Implement `expandAll()` (clears `collapsedNodeIds`) and `collapseAll()` (populates `collapsedNodeIds` with all folder IDs) in `src/web/js/app.js` and bind click handlers

---

## Phase 5: System Map Sync & Regression Testing

**Purpose**: Update system map and verify full test suite

- [x] T009 [P] Update `.specify/system_map.md` with new toolbar controls and collapse state documentation
- [x] T010 Run complete test suite `python -m pytest` to confirm all 46 tests pass cleanly with 0 failures
