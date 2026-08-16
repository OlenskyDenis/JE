# Tasks: Direct Root Node Creation Controls

**Feature Branch**: `025-root-node-controls`  
**Spec**: [specs/025-root-node-controls/spec.md](spec.md)  
**Plan**: [specs/025-root-node-controls/plan.md](plan.md)  
**Created**: 2026-08-14

---

## Phase 1: Foundational (Localization Keys)

- [x] T001 [P] Add `btn_add_root_header`, `btn_add_root_canvas`, and `tooltip_add_root` to `uk` and `en` dictionaries in `src/web/js/i18n.js`

---

## Phase 2: User Story 1 - Header & Canvas Root Creation Tools (Priority: P1) 🎯 MVP

- [x] T002 [P] [US1] Add `#btnAddRootHeader` in `.panel-header-actions` in `src/web/index.html` with `data-i18n` and `data-i18n-attr`
- [x] T003 [P] [US1] Update `src/web/js/tree_renderer.js` to render `#btnAddRootCanvas` inside `.tree-footer-actions` at the bottom of `#treeView` when `roots.length > 0`
- [x] T004 [P] [US1] Add styles for `.tree-footer-actions` and `.btn-add-root-canvas` in `src/web/css/style.css` matching the dark design system
- [x] T005 [US1] Wire click listeners for `#btnAddRootHeader` and delegated click for `#btnAddRootCanvas` in `src/web/js/app.js` to call `openAddModal(null, t('modal_create_title'))`

---

## Phase 3: Polish & Verification

- [x] T006 Update `.specify/system_map.md` and run automated pytest test suite (`python -m pytest`)
