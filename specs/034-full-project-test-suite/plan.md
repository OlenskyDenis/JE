# Implementation Plan: Full-Project Comprehensive Automated Test Suite & Multi-Layer Behavioral Verification

**Branch**: `034-full-project-test-suite` | **Date**: 2026-08-17 | **Spec**: [specs/034-full-project-test-suite/spec.md](spec.md)

**Input**: Feature specification from `/specs/034-full-project-test-suite/spec.md`

---

## 1. Summary of Requirements & Technical Decisions

- **Goal**: Establish 100% test coverage across all functional layers (E2E Browser Playwright, RPC Integration, Backend Services/Models, Frontend Contracts, and Architecture Contracts) with zero blind spots, ensuring real visibility (`to_be_visible()`) and active states (`to_be_enabled()`) without synthetic test DOM mutations.
- **Scope**:
  1. `tests/e2e/test_tree_crud_and_modals.py`: Root creation, leaf add/edit, delete node, name validation, toggle branch folding, collapse/expand all.
  2. `tests/e2e/test_view_modes_and_renderers.py`: Tree canvas, Excel Matrix view coordinate rendering, Unique Levels view leaf-first grouping, duplicate matching highlight synchronization.
  3. `tests/e2e/test_multi_sheet_and_excel_lifecycle.py`: Import `.xlsx`, session forest switching, template badge sync, unsaved changes modal cancel/discard/save, clean headers-only template export.
  4. `tests/e2e/test_drag_and_drop.py`: Catalog header drag to tree (3 zones), intra-tree sibling reordering, cycle detection rejection toast.
  5. `tests/e2e/test_settings_and_preferences.py`: Delimiter change (`/`, `.`, `-`), default data type change, reset to defaults, setting persistence in localStorage & backend.
  6. `tests/e2e/test_sidebar_tabs_and_resizer.py`: Tab selector (catalog vs paths), live search filtering, collapse vertical strip, resizer drag & reset, catalog sheet dropdown.
  7. `tests/e2e/test_navigation_and_i18n.py`: Full bilingual translation parity (UA/EN), toast visual styles and dismissal.
  8. `tests/unit/` & `tests/integration/`: Model invariants, path parsing, streaming Excel reader/writer, settings service, Eel bridge RPC dispatcher, and Principle VIII line-count linter.

---

## 2. Technical Context & Constitution Check

### Architectural Boundaries:
- **Playwright Test Runner**: Uses Python `pytest-playwright` with session-scoped Chromium browser and ephemeral Eel server on `127.0.0.1:<random_port>`.
- **Eel State Isolation**: Each test runs with clean backend session state reset in `conftest.py` fixture.
- **Principle VIII Guardrail**: All source files must remain $\le 200$ lines. Test files are modularized by domain.

### Constitution Compliance Matrix:
| Constitution Principle | Status | Evaluation |
|---|---|---|
| **Principle I (FIRST Test Invariant)** | **Compliant** | All tests are Fast ($< 35s$ full run), Independent, Repeatable, Self-validating, Timely. |
| **Principle II (Downward-Only Dependencies)** | **Compliant** | `tests/unit` $\to$ `src/hierarchy_lib`, `tests/integration` $\to$ `src/app`, `tests/e2e` $\to$ visual browser. |
| **Principle III (Pure Models)** | **Compliant** | Domain models tested independently with zero UI/Eel imports. |
| **Principle VII (Comprehensive Verification)** | **Compliant** | Pre-flight and post-flight quality gates enforced via `check_all.py`. |
| **Principle VIII (Line-Count Modularity)** | **Compliant** | Automated linter verifies $\le 200$ lines on all source files. |

---

## 3. Implementation Phases & Directory Map

```
tests/
├── e2e/
│   ├── conftest.py
│   ├── test_tree_crud_and_modals.py
│   ├── test_view_modes_and_renderers.py
│   ├── test_multi_sheet_and_excel_lifecycle.py
│   ├── test_drag_and_drop.py
│   ├── test_settings_and_preferences.py
│   ├── test_sidebar_tabs_and_resizer.py
│   └── test_navigation_and_i18n.py
├── integration/
│   └── test_eel_bridge.py
├── unit/
│   ├── test_architecture_contracts.py
│   ├── test_composite.py
│   ├── test_data_types.py
│   ├── test_dialog_service.py
│   ├── test_excel_adapter.py
│   ├── test_excel_fixtures.py
│   ├── test_forest_zone_addition.py
│   ├── test_frontend_contracts.py
│   ├── test_header_service.py
│   ├── test_path_parser.py
│   └── test_settings_service.py
└── fixtures/
    ├── generate_fixtures.py
    └── excel_samples/
```

### Planned Phases:
- **Phase 0**: Research test patterns, edge cases, and Playwright locator visibility best practices (`research.md`).
- **Phase 1**: Define test data models, contracts, and validation instructions (`data-model.md`, `contracts/test_suite_contracts.md`, `quickstart.md`).
- **Phase 2 (US1 - MVP)**: Full interactive Tree CRUD & 3 View Mode E2E test suite.
- **Phase 3 (US2)**: Multi-sheet workbook lifecycle, dirty state & template export E2E suite.
- **Phase 4 (US3)**: Drag-and-drop 3-zone placement & cycle validation E2E suite.
- **Phase 5 (US4)**: Data types formatting, promotion/demotion & settings E2E suite.
- **Phase 6 (US5 & US6)**: Sidebar, full i18n bilingual testing, and automated architecture linters.
- **Phase 7**: Quality gate execution (`check_all.py --full`) and quickstart validation.
