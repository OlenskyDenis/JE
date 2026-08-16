# Requirements Traceability & Checklist: Playwright E2E Suite

**Feature Branch**: `031-playwright-e2e-testing`  
**Created**: 2026-08-16  
**Status**: Ready for Planning  

---

## 1. Traceability Matrix

| Requirement ID | Description | Spec Reference | Target Test Module |
|---|---|---|---|
| **FR-001** | Install & configure `playwright` / `pytest-playwright` | [`spec.md`](../spec.md#L94) | `requirements.txt`, `pytest.ini` |
| **FR-002** | Implement ephemeral live Eel server & Chromium browser fixture | [`spec.md`](../spec.md#L95) | `tests/e2e/conftest.py` |
| **FR-003** | Navigation, header toolbar & bilingual i18n E2E tests | [`spec.md`](../spec.md#L100) | `tests/e2e/test_navigation_and_i18n.py` |
| **FR-004** | Hierarchy Tree CRUD, chevrons, and modals E2E tests | [`spec.md`](../spec.md#L104) | `tests/e2e/test_tree_crud_and_modals.py` |
| **FR-005** | Drag-and-drop gestures across 3 zones & cycle detection E2E tests | [`spec.md`](../spec.md#L109) | `tests/e2e/test_drag_and_drop.py` |
| **FR-006** | Excel matrix mode & unique level grouping with hover sync E2E tests | [`spec.md`](../spec.md#L114) | `tests/e2e/test_excel_matrix_and_unique_levels.py` |
| **FR-007** | Sidebar catalog search, tab switching & resizer E2E tests | [`spec.md`](../spec.md#L119) | `tests/e2e/test_sidebar_and_resizer.py` |
| **FR-008** | Settings modal, delimiter propagation & disk persistence E2E tests | [`spec.md`](../spec.md#L124) | `tests/e2e/test_settings_and_persistence.py` |
| **FR-009** | Deterministic headless execution in CI and local pytest runner | [`spec.md`](../spec.md#L129) | `pytest.ini` |

---

## 2. User Story Coverage Matrix

| User Story | Priority | Target E2E Module | Status |
|---|---|---|---|
| **US1** | P1 | `tests/e2e/test_navigation_and_i18n.py` | 📝 Specified |
| **US2** | P1 | `tests/e2e/test_tree_crud_and_modals.py` | 📝 Specified |
| **US3** | P1 | `tests/e2e/test_drag_and_drop.py` | 📝 Specified |
| **US4** | P2 | `tests/e2e/test_excel_matrix_and_unique_levels.py` | 📝 Specified |
| **US5** | P2 | `tests/e2e/test_settings_and_persistence.py` | 📝 Specified |
| **US6** | P2 | `tests/e2e/test_sidebar_and_resizer.py` | 📝 Specified |
