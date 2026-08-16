# Tasks: Data Type Badge and Tooltip Localization

**Feature Branch**: `024-fix-data-type`  
**Spec**: [specs/024-fix-data-type/spec.md](spec.md)  
**Plan**: [specs/024-fix-data-type/plan.md](plan.md)  
**Created**: 2026-08-14

---

## Phase 1: Foundational (Dictionary & Engine Helper)

- [x] T001 [P] Update `src/web/js/i18n.js` with `type_badge_*` dictionary entries in `uk` and `en` (using chosen extended Ukrainian terms) and add `I18n.getTypeLabel(type)` method

---

## Phase 2: Implementation & DOM Integration

- [x] T002 [P] Update `src/web/js/tree_renderer.js` to render localized badge text via `I18n.getTypeLabel()` and apply `title="${t('tooltip_data_type_badge')}"` in `createNodeElement` and `renderPaths`
- [x] T003 [P] Update `src/web/js/app.js` to render localized header type tags via `I18n.getTypeLabel()` and apply `title="${t('tooltip_data_type_badge')}"` in `filterAndRenderSidebar`

---

## Phase 3: Verification & Test Suite

- [x] T004 Run automated test suite (`python -m pytest`) to ensure 100% pass rate
