# Task Breakdown: Relocate Root Creation to Canvas Empty State & Streamline Workspace Header

**Feature**: `009-remove-redundant-add-root-button`  
**Branch**: `009-remove-redundant-add-root-button`  
**Spec**: [specs/009-remove-redundant-add-root-button/spec.md](spec.md)  
**Plan**: [specs/009-remove-redundant-add-root-button/plan.md](plan.md)  

---

## Phase 1: Setup & Foundational

**Purpose**: Verify UI layout and DOM selectors

- [x] T001 [P] Verify DOM selectors and event bindings in `src/web/index.html` and `src/web/js/app.js`

---

## Phase 2: User Story 1 & 2 - Streamlined Workspace Header & Empty-State Root Creation (Priority: P1 / P2) 🎯 MVP

**Goal**: Remove redundant `#btnAddRoot` from panel header and add `#btnCreateRootEmpty` inside `#treeEmptyState`, binding it to the creation modal.

**Independent Test**: Load app without an Excel file, verify panel header contains only title and badge (no button), and click "Create Root Node" button in empty state to create first root node.

### Implementation
- [x] T002 [P] [US1] Remove `<button id="btnAddRoot">` from `.panel-header` in `src/web/index.html`
- [x] T003 [P] [US2] Add `<button id="btnCreateRootEmpty" class="btn btn-primary btn-sm">` and updated prompt copy inside `#treeEmptyState` in `src/web/index.html`
- [x] T004 [US1/US2] Replace `#btnAddRoot` event listener with `#btnCreateRootEmpty` click event listener in `src/web/js/app.js`

**Checkpoint**: User Stories 1 and 2 are complete. Clean header toolbar with actionable empty state onboarding.

---

## Phase 3: User Story 3 - System Map Update & Regression Verification (Priority: P3)

**Goal**: Synchronize system map and confirm 100% test pass rate.

### Tasks
- [x] T005 [P] [US3] Update `.specify/system_map.md` with updated UI button inventory
- [x] T006 Run complete test suite `python -m pytest` to confirm all 46 tests pass cleanly with 0 failures
