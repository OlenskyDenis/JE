# Tasks: Project Audit, Hygiene Enforcement & Modular Architecture Refactor

**Branch**: `033-project-audit-and-hygiene` | **Date**: 2026-08-17 | **Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and quality baseline verification

- [X] T001 Initialize feature branch verification and ensure pre-commit hook is active via `python scripts/check_all.py --quick`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Confirm clean test suite baseline before any modifications

- [X] T002 Execute full test suite baseline check via `python -m pytest tests/unit tests/integration` to verify 84 tests pass with 0 warnings

---

## Phase 3: User Story 1 - Project Audit & Dead Code/CSS Purge (Priority: P1) 🎯 MVP

**Goal**: Identify and eliminate all 13 dead CSS selectors from `src/web/css/style.css`, clean up duplicate code patterns, and verify visual integrity.

**Independent Test**: Run `python scripts/check_all.py --quick` and inspect `style.css` to verify 13 dead selectors are deleted without styling regressions.

### Implementation for User Story 1

- [X] T003 [P] [US1] Remove 13 dead/unused CSS selectors (`.badge-sheet`, `.matrix-tier-0..3`, `.radio-card`, `.radio-group`, `.radio-label`, `.sidebar-tab-btn`, `.toast-error..warning`) from `src/web/css/style.css`
- [X] T004 [US1] Run fast quality gate check via `python scripts/check_all.py --quick` to verify style hygiene and zero test regressions

**Checkpoint**: Dead CSS pruned; zero UI styling regressions.

---

## Phase 4: User Story 2 - Frontend Monolith Decomposition & Modularity Compliance (Priority: P2)

**Goal**: Decompose `app.js` (1,324 lines) and `unique_level_renderer.js` (329 lines) into focused sub-modules $\le 200$ lines using window namespace facade delegation.

**Independent Test**: Verify all JS modules are $\le 200$ lines, run `node --check` on all JS files, and execute `python -m pytest tests/unit/test_frontend_contracts.py`.

### Implementation for User Story 2

- [X] T005 [P] [US2] Extract pure level calculation and leaf-first partitioning algorithm into `src/web/js/unique_level_extractor.js` ($\le 200$ lines)
- [X] T006 [US2] Refactor `src/web/js/unique_level_renderer.js` to focus strictly on DOM generation, badges, and inline editing events ($\le 200$ lines)
- [X] T007 [P] [US2] Extract add/edit/batch node modals, unsaved changes prompt, and settings modal lifecycle into `src/web/js/modal_manager.js` ($\le 200$ lines)
- [X] T008 [P] [US2] Extract sidebar tabs, search filter, responsive resizer, and collapse strip into `src/web/js/sidebar_controller.js` ($\le 200$ lines)
- [X] T009 [P] [US2] Extract view mode coordination (`tree`, `excelBlock`, `uniqueLevel`) and canvas double-click routing into `src/web/js/view_mode_manager.js` ($\le 200$ lines)
- [X] T010 [US2] Refactor `src/web/js/app.js` into a compact orchestrator and Eel event dispatcher ($\le 200$ lines)
- [X] T011 [US2] Update `src/web/index.html` with script tags for `unique_level_extractor.js`, `modal_manager.js`, `sidebar_controller.js`, `view_mode_manager.js` in correct load order
- [X] T012 [US2] Update `tests/unit/test_frontend_contracts.py` to validate script tags, DOM bindings, and I18n calls for all new frontend modules

**Checkpoint**: Frontend modules decomposed; all files $\le 200$ lines; frontend contracts pass.

---

## Phase 5: User Story 3 - Backend Architecture & Adapter Modularity Refactor (Priority: P2)

**Goal**: Decompose `eel_bridge.py` (431 lines) and `excel_adapter.py` (227 lines) into focused modules $\le 200$ lines while eliminating duplicate type mapping loops.

**Independent Test**: Run `python -m pytest tests/unit tests/integration` to verify Excel reading/writing, session forest management, and RPC responses.

### Implementation for User Story 3

- [X] T013 [P] [US3] Extract streaming row 1 header reading and format mapping heuristics into `src/hierarchy_lib/adapters/excel_reader.py` ($\le 200$ lines)
- [X] T014 [P] [US3] Extract clean multi-sheet template export workbook construction into `src/hierarchy_lib/adapters/excel_writer.py` ($\le 200$ lines)
- [X] T015 [US3] Refactor `src/hierarchy_lib/adapters/excel_adapter.py` into a thin public facade `ExcelHierarchyAdapter` ($\le 50$ lines)
- [X] T016 [P] [US3] Extract multi-sheet session forests, active sheet tracking, and unified DRY header parsing / type applying into `src/app/session_manager.py` ($\le 200$ lines)
- [X] T017 [P] [US3] Extract node CRUD operations and zone additions on active forest into `src/app/node_controller.py` ($\le 200$ lines)
- [X] T018 [US3] Refactor `src/app/eel_bridge.py` into a clean `@eel.expose` router delegating to `SessionManager`, `NodeController`, `SettingsService`, and `FileDialogService` ($\le 200$ lines)
- [X] T019 [US3] Execute unit and integration tests via `python -m pytest tests/unit tests/integration` to verify backend modularity contracts

**Checkpoint**: Backend modules decomposed; all files $\le 200$ lines; zero duplicate parsing loops; tests pass 100%.

---

## Phase 6: User Story 4 - Automated Architecture Linter & System Map Parity (Priority: P3)

**Goal**: Add automated 200-line threshold checks to `test_architecture_contracts.py` and update `.specify/system_map/` to 86+ tests.

**Independent Test**: Run `python -m pytest tests/unit/test_architecture_contracts.py` and verify all checks pass.

### Implementation for User Story 4

- [X] T020 [US4] Add `test_file_line_count_thresholds()` to `tests/unit/test_architecture_contracts.py` enforcing $\le 200$ lines for all non-exempt `.py` and `.js` files
- [X] T021 [P] [US4] Update `.specify/system_map.md` and modular maps in `.specify/system_map/` to reflect new components and 86+ test metrics
- [X] T022 [P] [US4] Update `docs/KNOWLEDGE.md` with the decomposed modular component map and line-count guardrail reference

**Checkpoint**: Automated linter actively enforces 200-line modularity threshold; system maps fully synchronized.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Full regression testing and quickstart validation

- [X] T023 [P] Run complete fast quality gate check via `python scripts/check_all.py --quick`
- [X] T024 [P] Run full Playwright E2E browser test suite via `python scripts/check_all.py --full`
- [X] T025 Execute `specs/033-project-audit-and-hygiene/quickstart.md` validation scenarios and verify zero test warnings or lint errors

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - verifies baseline.
- **User Story 1 (Phase 3 - MVP)**: Dead CSS purge - independent.
- **User Story 2 (Phase 4)**: Frontend decomposition - depends on Phase 2.
- **User Story 3 (Phase 5)**: Backend decomposition - depends on Phase 2 (can run in parallel with US2).
- **User Story 4 (Phase 6)**: Architecture linter & system maps - depends on US2 and US3 completion.
- **Polish (Phase 7)**: Final full regression suite across all stories.

### Parallel Opportunities

- Within US2: `T005`, `T007`, `T008`, `T009` can be developed in parallel before merging into `T010`/`T011`.
- Within US3: `T013`, `T014`, `T016`, `T017` can be developed in parallel.
- US2 (Frontend) and US3 (Backend) can proceed in parallel once Phase 2 completes.
- Within Polish: `T023`, `T024` can run sequentially or in parallel test environments.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational baseline
3. Complete Phase 3: User Story 1 (CSS hygiene & dead code purge)
4. **STOP and VALIDATE**: Verify zero visual regressions with `check_all.py --quick`

### Incremental Delivery

1. Setup + Foundational $\to$ Baseline verified
2. User Story 1 $\to$ CSS and dead code purged (MVP!)
3. User Story 2 $\to$ Frontend monolith decomposed into modular controllers ($\le 200$ lines)
4. User Story 3 $\to$ Backend adapter & RPC bridge decomposed into modular services ($\le 200$ lines)
5. User Story 4 $\to$ Architecture contracts linter + System maps updated
6. Polish $\to$ 100% full quality gate passing (109 tests)
