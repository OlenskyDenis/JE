# Task Breakdown: Streamline Creation Modal & Dead DOM Cleanup

**Feature**: `010-streamline-modal-and-dead-dom-cleanup`  
**Branch**: `010-streamline-modal-and-dead-dom-cleanup`  
**Spec**: [specs/010-streamline-modal-and-dead-dom-cleanup/spec.md](spec.md)  
**Plan**: [specs/010-streamline-modal-and-dead-dom-cleanup/plan.md](plan.md)  

---

## Phase 1: Setup & Foundational

**Purpose**: Audit and verify targeted DOM elements and selectors

- [x] T001 [P] Audit all occurrences of `nodeType`, `excelFileInput`, and `isContainer` in `src/web/`

---

## Phase 2: User Story 1 (MVP) - Streamlined Single-Field Modal (Priority: P1) 🎯 MVP

**Goal**: Remove static `Node Type` radio group from `#nodeModal` and simplify modal submission in `app.js` to prompt only for `Node Name`.

**Independent Test**: Click "Create Root Node" or "+ Add Child" on any node, verify modal contains only "Node Name" field, submit name, and verify dynamic `HierarchyNode` is created without errors.

### Implementation
- [x] T002 [P] [US1] Remove `<div class="form-group"><label>Node Type</label>...</div>` radio button group from `#nodeModal` in `src/web/index.html`
- [x] T003 [US1] Refactor `submitAddModal()` in `src/web/js/app.js` to remove `input[name="nodeType"]` query selector and invoke `eel.add_node(this.activeParentIdForModal, name)`

**Checkpoint**: Modal creation flow is streamlined to a 1-step dialog with zero static type selectors.

---

## Phase 3: User Story 2 & 3 - Dead DOM Removal & Payload Hygiene (Priority: P2 / P3)

**Goal**: Eliminate orphaned `#excelFileInput` HTML and controller references, and clean up drag-and-drop payload dictionaries.

**Independent Test**: Inspect DOM in browser to confirm `#excelFileInput` is absent, and verify dragging sidebar headers onto canvas creates nodes cleanly.

### Implementation
- [x] T004 [P] [US2] Remove `<input type="file" id="excelFileInput">` from `src/web/index.html` and delete `this.excelFileInput` from `initElements()` in `src/web/js/app.js`
- [x] T005 [P] [US3] Remove `isContainer: false` from drag payload initializers in `src/web/js/drag_drop.js`

---

## Phase 4: System Map Sync & Regression Testing

**Purpose**: Update system map and verify full test suite

- [x] T006 [P] Update `.specify/system_map.md` to reflect streamlined modal and clean DOM inventory
- [x] T007 Run complete test suite `python -m pytest` to confirm all 46 tests pass cleanly with 0 failures
