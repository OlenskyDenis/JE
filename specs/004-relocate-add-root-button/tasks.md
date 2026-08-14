# Task Breakdown: Relocate 'Add Root Node' Button to Workspace Canvas

**Feature**: `004-relocate-add-root-button`  
**Branch**: `004-relocate-add-root-button`  
**Spec**: [specs/004-relocate-add-root-button/spec.md](spec.md)  
**Plan**: [specs/004-relocate-add-root-button/plan.md](plan.md)  

---

## Phase 1: Setup & DOM Relocate (HTML Structure)

**Purpose**: Move `#btnAddRoot` button to workspace canvas header

- [x] T001 [P] Relocate `#btnAddRoot` button element from `.app-header .toolbar-actions` to `.tree-panel .panel-header` in `src/web/index.html`

---

## Phase 2: Canvas Action Styling (CSS Layout)

**Purpose**: Style and position the relocated button cleanly at the top of the workspace canvas

- [x] T002 Update `.panel-header` CSS in `src/web/css/style.css` to align panel header title, node badge, and action button `#btnAddRoot` flexibly
- [x] T003 Ensure button `#btnAddRoot` uses primary button styling (`.btn-primary`), clear contrast, hover effects, and responsive spacing

---

## Phase 3: Verification & Regression Tests

**Purpose**: Confirm modal invocation and verify backend test suite

- [x] T004 Verify `app.js` event listener initialization for `#btnAddRoot` functions properly
- [x] T005 Run pytest regression suite (`python -m pytest`) to ensure all integration and unit tests pass cleanly

---

## Dependencies & Execution Order

1. **Phase 1 (HTML Relocate)**: Blocks Phase 2 styling.
2. **Phase 2 (CSS Styling)**: Ensures visual hierarchy.
3. **Phase 3 (Verification)**: Confirms complete compliance.
