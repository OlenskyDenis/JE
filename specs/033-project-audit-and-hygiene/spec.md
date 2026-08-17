# Feature Specification: Project Audit, Hygiene Enforcement & Modular Architecture Refactor

**Feature Branch**: `033-project-audit-and-hygiene`

**Created**: 2026-08-17

**Status**: Draft

**Input**: User description: "Проведення аудиту проекту. Основна ціль виявлення файлів які не задіяні, фантомний код, проблемні питання. Перевірка логіки і відповідності до правил, скілів, конституції."

---

## 💡 Clarifications

### Session 2026-08-17

- **Q**: Який патерн зв'язку між підмодулями слід використати для декомпозиції моноліту `app.js`?
  **A**: Фасадний контролер `App` з прямою делегацією підмодулів через глобальний простір імен (`window.ModalManager`, `window.SidebarController`, `window.ViewModeManager`) без сторонніх бандлерів (збереження нативного Vanilla JS та нульових збиральних залежностей).

---

## 🗑️ Retirement & Cleanup Matrix *(mandatory for changes replacing existing logic)*

| Component / Endpoint / File | Action (Delete / Refactor / Migrate) | Replacement (Canonical New Approach) | Obsolete Tests to Remove / Update |
|---|---|---|---|
| Dead CSS Selectors in `src/web/css/style.css` (`.badge-sheet`, `.matrix-tier-*`, `.radio-*`, `.sidebar-tab-btn`, `.toast-*`) | Delete | Pruned CSS; active classes only | N/A (Style cleanup) |
| Duplicate `_apply_types` & header loops in `eel_bridge.py` (`import_excel_file`, `refresh_excel_session`, `switch_active_sheet`) | Refactor / Extract | Reusable session helper service `SessionManagerService` | `test_eel_bridge.py` (Assert via unified helper) |
| Monolithic `src/web/js/app.js` (>1 300 lines) | Modular Refactor (Decompose) | Sub-controllers: `App` (core bus), `ModalManager`, `SidebarController`, `ViewModeManager` (all $\le 200$ lines) | `test_frontend_contracts.py` (Update script tags test) |
| Monolithic `src/web/js/unique_level_renderer.js` (>320 lines) | Modular Refactor (Decompose) | Split into `unique_level_extractor.js` (algorithm) and `unique_level_renderer.js` (DOM rendering) ($\le 200$ lines) | `test_frontend_contracts.py` (Add new script tag validation) |
| Monolithic `src/app/eel_bridge.py` (>430 lines) | Modular Refactor (Decompose) | Split into `session_manager.py` / `node_controller.py` + streamlined `eel_bridge.py` ($\le 200$ lines) | `test_architecture_contracts.py` (Add line-count guardrail test) |
| Monolithic `src/hierarchy_lib/adapters/excel_adapter.py` (>225 lines) | Modular Refactor (Decompose) | Split into `excel_reader.py` / `excel_writer.py` under adapters ($\le 200$ lines) | `test_excel_adapter.py` (Keep public API intact) |

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Project Audit & Dead Artifact / Phantom Code Purge (Priority: P1) 🎯 MVP

As a system architect and developer, I want all dead CSS classes, duplicate logic blocks, and orphan code identified and safely eliminated across the repository, so that the project contains zero phantom code, zero unused styles, and 100% clear logic.

**Why this priority**: Eliminating dead artifacts and duplicated logic immediately improves code clarity, prevents maintenance regressions, and establishes an auditable baseline for future development.

**Independent Test**: Perform automated search and AST inspection across all source files; verify that all 13 dead CSS rules are pruned from `style.css`, duplicate type mapping loops in `eel_bridge.py` are extracted into a single reusable helper, and all 84 existing tests continue to pass with 100% success rate.

**Acceptance Scenarios**:

1. **Given** `src/web/css/style.css`, **When** scanned for unused legacy selectors (`.badge-sheet`, `.matrix-tier-0..3`, `.radio-card`, `.radio-group`, `.radio-label`, `.sidebar-tab-btn`, `.toast-error..warning`), **Then** all 13 dead rules are removed without any visual regression on any UI component.
2. **Given** backend Excel import/refresh/switch operations in `eel_bridge.py`, **When** inspected, **Then** the duplicate `_apply_types` recursive closure and header-type pairing routines are extracted into a single DRY helper function.
3. **Given** the entire repository, **When** project quality check `python scripts/check_all.py --quick` is executed, **Then** all syntax, JS integrity, Ruff linting, and Pytest test suites pass with 0 errors and 0 warnings.

---

### User Story 2 - Frontend Monolith Decomposition & Modularity Compliance (Priority: P2)

As a frontend developer, I want the monolithic `app.js` (1,324 lines) and `unique_level_renderer.js` (329 lines) decomposed into focused, single-responsibility ES modules strictly under the 200-line limit (Constitution Principle VIII), so that each module has a single reason to change and is easy to read, test, and maintain.

**Why this priority**: Monolithic files violate Principle VIII and SRP, making it difficult to locate logic, increasing merge conflict risks, and obscuring event flow.

**Independent Test**: Load the desktop GUI and run Playwright E2E suite (`python scripts/check_all.py --e2e`); verify that all UI operations (tree navigation, modals, tab switching, resizing, all 3 view modes, data types, i18n switching) behave identically with decomposed modules.

**Acceptance Scenarios**:

1. **Given** `src/web/js/app.js`, **When** decomposed, **Then** modal logic is encapsulated in `modal_manager.js`, sidebar interactions in `sidebar_controller.js`, and view-mode rendering coordination in `view_mode_manager.js`, with each module remaining $\le 200$ lines.
2. **Given** `src/web/js/unique_level_renderer.js`, **When** decomposed, **Then** level extraction and leaf partitioning logic is encapsulated in `unique_level_extractor.js`, and DOM rendering in `unique_level_renderer.js`, with each file $\le 200$ lines.
3. **Given** `src/web/index.html`, **When** loaded in a browser or test runner, **Then** all decomposed scripts are properly loaded with dependency ordering and zero global namespace collisions.
4. **Given** `tests/unit/test_frontend_contracts.py`, **When** executed, **Then** all new script tags, DOM ID references, and I18n bindings are verified and pass without error.

---

### User Story 3 - Backend Architecture & Adapter Modularity Refactor (Priority: P2)

As a backend engineer, I want `src/app/eel_bridge.py` (431 lines) and `src/hierarchy_lib/adapters/excel_adapter.py` (227 lines) decomposed into modular components strictly under 200 lines (Constitution Principle VIII) while adhering to Downward-Only Dependency Flow (Principle II), so that backend services maintain high cohesion and test isolation.

**Why this priority**: `eel_bridge.py` currently acts as a catch-all session container and RPC dispatcher, while `excel_adapter.py` mixes reading, format detection, and writing logic.

**Independent Test**: Execute `pytest tests/unit tests/integration`; verify that all Excel parsing, multi-sheet template export, node mutations, and RPC endpoints operate seamlessly with zero test regressions.

**Acceptance Scenarios**:

1. **Given** `src/app/eel_bridge.py`, **When** decomposed, **Then** multi-sheet session container management is extracted into `session_manager.py`, node CRUD helpers into `node_controller.py`, and `eel_bridge.py` remains a clean, compact RPC router ($\le 200$ lines).
2. **Given** `src/hierarchy_lib/adapters/excel_adapter.py`, **When** decomposed, **Then** streaming row 1 reading and format mapping are isolated from workbook export construction while preserving the public adapter facade `ExcelHierarchyAdapter` ($\le 200$ lines).
3. **Given** `src/hierarchy_lib/models/`, **When** inspected, **Then** domain models remain 100% pure abstractions with zero imports of services, adapters, or configuration managers.

---

### User Story 4 - Automated Architecture Linter & System Map Parity (Priority: P3)

As a quality assurance architect, I want an automated AST architecture linter that enforces the 200-line modularity threshold across all Python and JavaScript files, and full synchronization of `.specify/system_map/` documentation with the 84+ test baseline.

**Why this priority**: Guarantees that future code contributions cannot silently re-introduce monolithic files or violate constitutional guardrails.

**Independent Test**: Run `pytest tests/unit/test_architecture_contracts.py`; verify that a new test `test_file_line_count_thresholds()` checks all non-exempt source files ($\le 200$ lines) and that system map files accurately state current component sizes and test counts.

**Acceptance Scenarios**:

1. **Given** `tests/unit/test_architecture_contracts.py`, **When** executed, **Then** it iterates over all `.py` and `.js` source files (excluding documented exemptions: `i18n.js`, `style.css`, `index.html`) and asserts that each file has $\le 200$ lines of code.
2. **Given** `.specify/system_map.md` and `.specify/system_map/*.md`, **When** reviewed, **Then** all modular system maps reflect the new modular components, active 84+ test suite count, and current file mappings.

---

## Edge Cases & Red Teaming (Zero-Data & Error States)

- **Zero-Data / Clean Slate Initialization**: What happens when the app starts with no Excel file loaded? Modal managers and view mode renderers must cleanly handle empty state (`forest.root_nodes == []`) without `null` reference errors.
- **Rapid View Mode Switching**: Switching between Tree, Matrix, and Unique Level views rapidly must not cause memory leaks or duplicate event listener accumulation in decomposed sub-controllers.
- **Exempt File Verification**: Static localization dictionary `i18n.js` (bilingual translation strings) and declarative stylesheet `style.css` are explicitly exempt from the 200-line threshold pursuant to Constitution Principle VIII.
- **Backwards Compatibility of Public Facades**: Public interfaces (`ExcelHierarchyAdapter`, `App`, Eel RPC endpoints) must maintain 100% signature compatibility so that existing test suites and fixtures require zero breaking changes.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST audit and remove all 13 dead/unused CSS class selectors from `src/web/css/style.css`.
- **FR-002**: System MUST extract duplicate header-parsing and type-mapping routines in `eel_bridge.py` into a reusable helper function or service.
- **FR-003**: System MUST refactor `src/web/js/app.js` into focused modules (`modal_manager.js`, `sidebar_controller.js`, `view_mode_manager.js`, `app.js`) using facade delegation via window namespace without external bundlers, each containing $\le 200$ lines of code.
- **FR-004**: System MUST refactor `src/web/js/unique_level_renderer.js` into `unique_level_extractor.js` and `unique_level_renderer.js`, each containing $\le 200$ lines of code.
- **FR-005**: System MUST refactor `src/app/eel_bridge.py` into focused sub-modules (`session_manager.py`, `node_controller.py`, `eel_bridge.py`), each containing $\le 200$ lines of code.
- **FR-006**: System MUST refactor `src/hierarchy_lib/adapters/excel_adapter.py` to keep module size $\le 200$ lines while preserving complete `ExcelHierarchyAdapter` functionality.
- **FR-007**: System MUST update `src/web/index.html` to load all decomposed JavaScript files in correct dependency order.
- **FR-008**: System MUST update `tests/unit/test_frontend_contracts.py` to validate the existence and integrity of all decomposed frontend scripts.
- **FR-009**: System MUST add an automated test in `tests/unit/test_architecture_contracts.py` enforcing the 200-line modularity threshold for all non-exempt source files.
- **FR-010**: System MUST update `.specify/system_map.md` and relevant modular maps in `.specify/system_map/` to reflect decomposed components and active test suite metrics (84+ tests).

---

### Key Entities

- **SessionManager (`session_manager.py`)**: Manages multi-sheet session forests, active sheet tracking, and session file path state.
- **ModalManager (`modal_manager.js`)**: Encapsulates node add/edit modals, unsaved changes confirmation dialogs, and settings modal lifecycle.
- **SidebarController (`sidebar_controller.js`)**: Encapsulates sidebar tabs, search filter, responsive drag-resizing, and collapsed strip toggle.
- **ViewModeManager (`view_mode_manager.js`)**: Coordinates active view mode selection (Tree, Matrix, Unique Levels) and dispatches canvas rendering.
- **UniqueLevelExtractor (`unique_level_extractor.js`)**: Pure algorithmic module extracting depth levels, duplicate detection, and leaf-first partitioning.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of non-exempt Python and JavaScript source files in `src/` strictly satisfy the $\le 200$ lines of code threshold (Constitution Principle VIII).
- **SC-002**: 100% pass rate across all 84+ unit and integration tests (`python scripts/check_all.py --quick`) in $< 3.0$ seconds.
- **SC-003**: 100% pass rate across all Playwright E2E browser tests (`python scripts/check_all.py --full`) with zero regressions.
- **SC-004**: Zero dead CSS class selectors detected in `src/web/css/style.css`.
- **SC-005**: 100% synchronization of `.specify/system_map.md` and `.specify/system_map/*.md` with active codebase structure.

---

## Assumptions

- Python 3.10+ runtime with `openpyxl`, `eel`, `pytest`, and `ruff`.
- Web UI executes within Chromium/Eel desktop environment.
- Files exempt from the 200-line threshold: `src/web/js/i18n.js` (static bilingual dictionary), `src/web/css/style.css` (central stylesheet), and `src/web/index.html` (declarative markup), as defined by Constitution Principle VIII.
- Refactoring preserves 100% public API compatibility for all Eel RPC endpoints and domain classes.
