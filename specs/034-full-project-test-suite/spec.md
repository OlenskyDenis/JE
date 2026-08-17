# Feature Specification: Full-Project Comprehensive Automated Test Suite & Multi-Layer Behavioral Verification

**Feature Branch**: `034-full-project-test-suite`

**Created**: 2026-08-17

**Status**: Draft

**Input**: User description: "Створення повноціних автоматичних тестів які будуть покривати кожен свою частину функціоналу. Потрібно повністю покрити весь проект тестами для перевірки роботи інтерфейсу, всі наявні функції, весь функціонал. Так як зараз ще є баги, ми зразу перевіримо ефективність цих тестів."

---

## 💡 Clarifications

### Session 2026-08-17
- **Q**: Яку стратегію організації тестових наборів обрати для повного покриття проєкту?
  **A**: Модульна структура тестових наборів: окремі спеціалізовані файли під кожен функціональний домен (`test_tree_crud_and_modals.py`, `test_view_modes_and_renderers.py`, `test_multi_sheet_and_excel_lifecycle.py`, `test_drag_and_drop.py`, `test_settings_and_preferences.py`, `test_sidebar_tabs_and_resizer.py`, `test_navigation_and_i18n.py`) із суворою перевіркою реальної видимості `to_be_visible()` та доступності контролів `to_be_enabled()` без штучних DOM-модифікацій у коді тестів.

---

## 🗑️ Retirement & Cleanup Matrix *(mandatory for changes replacing existing logic)*

| Component / Endpoint / File | Action (Delete / Refactor / Migrate) | Replacement (Canonical New Approach) | Obsolete Tests to Remove / Update |
|---|---|---|---|
| Fragile / Shallow assertions in legacy E2E tests (`to_have_count` without visibility checks) | Refactor / Replace | Strict assertions enforcing `expect(el).to_be_visible()`, `expect(el).to_be_enabled()` | `tests/e2e/test_*.py` |
| Manual DOM manipulation bypasses inside test cases (e.g. `el.disabled = false`) | Delete | Real user-driven production state activation | `tests/e2e/test_sidebar_tabs_and_resizer.py` |

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Comprehensive Core Tree & View Mode E2E Test Matrix (Priority: P1) 🎯 MVP

As a user and QA engineer, I want exhaustive automated tests covering all 3 interactive workspace views (Tree Canvas, Excel Matrix View, Unique Levels View) including node creation, editing, deletion, folding, and cross-level highlights, so that visual hierarchy integrity is guaranteed across all viewing modes.

**Why this priority**: Workspace visualization is the core product value. Tree navigation and switching between Matrix and Unique Levels must be 100% bug-free.

**Independent Test**: Execute `pytest tests/e2e/test_view_modes_and_renderers.py` and `pytest tests/e2e/test_tree_crud_and_modals.py`; verify that all tree operations, matrix cells, unique level chips, and hover synchronization pass with concrete visibility assertions.

**Acceptance Scenarios**:
1. **Given** an empty workspace, **When** clicking `#btnCreateRootEmpty` or `#btnAddRootHeader`, **Then** the creation modal opens, validates non-empty names, and renders the new root card in Tree view.
2. **Given** an existing node card, **When** clicking `.action-btn.rename-node`, **Then** the edit modal opens with pre-filled name and type, and saving updates the title immediately in the DOM.
3. **Given** a parent node with children, **When** clicking `.node-toggle`, **Then** child branches fold/unfold with correct chevron icon rotation, and `#btnExpandAll` / `#btnCollapseAll` affect all branches globally.
4. **Given** a multi-level hierarchy, **When** switching to Matrix View (`#btnViewMatrix`), **Then** a coordinate table with column coordinates ($A, B, C\dots$) and hierarchical block cells renders visibly.
5. **Given** duplicate node names across different hierarchy levels, **When** switching to Unique Levels View (`#btnViewUniqueLevels`), **Then** chips group cross-level occurrences, show count badges, and hovering a duplicate chip highlights all matching chips simultaneously (`.highlight-match-sync`).

---

### User Story 2 - Multi-Sheet Workbook Lifecycle, File Dialogs & Template Sync E2E Suite (Priority: P1)

As an Excel data engineer, I want automated E2E tests covering the complete Excel workbook lifecycle: importing `.xlsx` files, switching active workspace sheets, catalog sheets, live template synchronization, and dirty state protection, so that data loss is completely impossible.

**Why this priority**: Multi-sheet workbook management and template synchronization are critical business invariants. Accidental data loss during sheet switching or file loading must be strictly prevented.

**Independent Test**: Execute `pytest tests/e2e/test_multi_sheet_and_excel_lifecycle.py`; verify that multi-sheet workbooks load correctly, sheet selectors update, dirty state prompts appear on unsaved edits, and template export creates valid headers-only files.

**Acceptance Scenarios**:
1. **Given** a multi-sheet Excel file (`multisheet_retail.xlsx`), **When** imported via `handleImportExcelFile`, **Then** `#activeSheetSelector` and `#catalogSheetSelector` populate with all sheet names and enable automatically.
2. **Given** modifications in the active sheet (dirty state), **When** user attempts to switch `#activeSheetSelector` or import another file, **Then** `#unsavedModal` pops up with "Save & Continue", "Discard", and "Cancel" options.
3. **Given** `#unsavedModal`, **When** user clicks "Cancel", **Then** the selector reverts to the original sheet without losing state; when clicking "Discard", the switch proceeds immediately.
4. **Given** configured hierarchies across multiple sheets, **When** `#btnExportExcel` is clicked, **Then** a clean Excel template is generated containing only Row 1 headers without any data rows ($Row \ge 2$).

---

### User Story 3 - Drag-and-Drop, Zone Placement & Cycle Validation E2E Matrix (Priority: P2)

As an interactive designer, I want automated browser tests for all three drop zones (`BEFORE_SIBLING`, `AFTER_SIBLING`, `NEST_CHILD`), catalog-to-canvas dragging, and cycle prevention guards, so that structural tree mutations are intuitive, reliable, and mathematically sound.

**Why this priority**: Drag-and-drop is the primary interaction mechanism for building hierarchies. Dropping parent nodes into descendants must be rejected instantly.

**Independent Test**: Execute `pytest tests/e2e/test_drag_and_drop.py`; verify that moving headers from the sidebar catalog inserts new nodes at the target zone, intra-tree reordering updates leaf paths, and illegal cycle drops display warning toasts.

**Acceptance Scenarios**:
1. **Given** a header item in `#sidebarHeaderList`, **When** dragged and dropped onto a target tree node, **Then** a new node is created under the specified zone with the header's name and data type.
2. **Given** existing nodes $A$ and $B$, **When** node $A$ is dragged before or after node $B$, **Then** sibling order updates and dynamic leaf paths re-render.
3. **Given** parent node $P$ and child node $C$, **When** attempting to drag $P$ into $C$ (`NEST_CHILD`), **Then** the operation is rejected, a warning toast appears, and the tree structure remains intact.

---

### User Story 4 - Data Types System & Leaf Promotion/Demotion E2E Suite (Priority: P2)

As a database schema architect, I want automated verification of all 9 data types (`Text`, `Integer`, `Decimal`, `Currency`, `Percentage`, `Date`, `Time`, `DateTime`, `Boolean`), format auto-detection, and leaf container promotion/demotion behavior, so that exported Excel templates maintain 100% type formatting fidelity.

**Why this priority**: Strict typing ensures compatibility with downstream database ingestion pipelines.

**Independent Test**: Execute `pytest tests/unit/test_data_types.py` and `pytest tests/e2e/test_settings_and_preferences.py`; verify that data type badges render with distinct color tokens, formatting maps to valid Excel number formats, and leaf promotion suppresses types on folder nodes.

**Acceptance Scenarios**:
1. **Given** each of the 9 standard data types, **When** assigned to a leaf node, **Then** the node displays the corresponding type badge (`.node-type-badge[data-type="..."]`) with translated labels in both Ukrainian and English.
2. **Given** a leaf node with type `Currency`, **When** a child node is added to it, **Then** the node is promoted to a folder container and its type badge is hidden from view mode rendering.
3. **Given** a folder node, **When** all its children are deleted, **Then** it reverts to a leaf node with its default or configured data type restored.

---

### User Story 5 - Sidebar, Settings & Full Bilingual (UA/EN) i18n Verification Suite (Priority: P3)

As an international user, I want comprehensive E2E tests for the resizable unified sidebar, settings configuration (custom delimiter, default data type), and bilingual UI switching, so that every label, button, badge, tooltip, and toast notification has 100% translation coverage without untranslated raw keys.

**Why this priority**: Ensures polished accessibility and flawless bilingual experience for both Ukrainian and international users.

**Independent Test**: Execute `pytest tests/e2e/test_navigation_and_i18n.py` and `pytest tests/e2e/test_sidebar_tabs_and_resizer.py`; verify that switching between UA and EN updates all DOM elements dynamically, settings persist across reloads, and sidebar drag-resizing works smoothly.

**Acceptance Scenarios**:
1. **Given** the application UI, **When** clicking `#langBtnEn` and `#langBtnUk`, **Then** 100% of headers, buttons, tabs, empty states, and modal labels switch languages instantly without reloading the page.
2. **Given** `#settingsModal`, **When** user customizes the path delimiter (e.g. `.` or `/`) and default data type, **Then** the new delimiter immediately reflects in the leaf paths list (`#pathList`).
3. **Given** `#unifiedSidebar`, **When** user drags `#sidebarResizer` or double-clicks to reset, **Then** the sidebar width adjusts smoothly and persists in `localStorage`.

---

### User Story 6 - Automated Architecture Contracts & Line-Count Linters (Priority: P3)

As a lead architect, I want automated AST linters and contract tests enforcing Constitution Principle VIII ($\le 200$ lines per file), downward-only dependency flow, pure domain models, and zero dead code, so that code hygiene cannot degrade in future iterations.

**Why this priority**: Guarantees modular architectural boundaries and prevents monolithic creep.

**Independent Test**: Execute `pytest tests/unit/test_architecture_contracts.py` and `python scripts/check_all.py --quick`; verify that 100% of source files strictly satisfy line count and architectural purity rules.

**Acceptance Scenarios**:
1. **Given** all `.py` and `.js` files in `src/`, **When** `test_file_line_count_thresholds()` executes, **Then** all non-exempt files have $\le 200$ lines of code.
2. **Given** `src/hierarchy_lib/models/`, **When** inspected, **Then** models have zero imports from UI, Eel, or external service layers.

---

## Edge Cases & Red Teaming (Zero-Data & Error States)

- **Zero-Data State**: Application launch with no Excel workbook loaded — all view modes, modals, and sidebar empty states render cleanly with zero JavaScript console exceptions.
- **Corrupted / Blank Excel File**: Loading an empty `.xlsx` file or a file with no headers displays a clear, localized error toast without crashing the Python backend.
- **Rapid View Mode Dispatches**: Fast toggling between Tree, Matrix, and Unique Level views does not cause ghost DOM element accumulation or duplicate event listeners.
- **Strict Visual Visibility**: Every E2E test asserts that elements are visible on screen (`to_be_visible()`) and enabled (`to_be_enabled()`), eliminating false-positive passes caused by hidden DOM elements.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Test suite MUST provide dedicated, comprehensive E2E test modules for each core functional domain under `tests/e2e/`.
- **FR-002**: All Playwright E2E tests MUST assert visual visibility (`to_be_visible()`) and accessibility rather than mere DOM existence (`to_have_count()`).
- **FR-003**: Test cases MUST NEVER synthetically mutate element properties (e.g. `el.disabled = false`) and MUST validate real user flows.
- **FR-004**: Test suite MUST cover all 3 view modes (Tree Canvas, Excel Matrix View, Unique Levels View) and their specific interactions.
- **FR-005**: Test suite MUST cover multi-sheet workbook sessions, active/catalog sheet separation, unsaved changes modal prompts, and template export.
- **FR-006**: Test suite MUST cover the complete 9 data types system, auto-detection, number format mapping, and leaf promotion/demotion.
- **FR-007**: Test suite MUST verify bilingual translation parity (`uk` and `en`) across all UI surfaces, tooltips, dialogs, badges, and toasts.
- **FR-008**: Test suite MUST verify sidebar tab switching, search filtering, collapsible vertical strip, and drag-to-resize persistence.
- **FR-009**: Test suite MUST verify custom settings (delimiter and default data type) propagation to path parsing and node creation.
- **FR-010**: Automated architecture linter MUST verify Constitution Principle VIII ($\le 200$ lines per file) across all non-exempt files.

---

### Key Entities

- **E2ETestSuite (`tests/e2e/`)**: Playwright browser automation suite covering all interactive UI journeys.
- **IntegrationTestSuite (`tests/integration/`)**: Backend-to-frontend RPC bridge and multi-sheet session validation.
- **UnitTestSuite (`tests/unit/`)**: Domain models, Excel reader/writer, path parser, settings service, and architecture contract linters.
- **QualityGateRunner (`scripts/check_all.py`)**: Unified pre-flight and full-flight test verification orchestrator.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% test pass rate across all unit, integration, and E2E browser tests (110+ tests) via `python scripts/check_all.py --full` in $< 35$ seconds.
- **SC-002**: 100% of non-exempt Python and JavaScript files in `src/` strictly satisfy the $\le 200$ lines of code threshold.
- **SC-003**: Zero console errors (`Page Errors: 0`, `Console Errors: 0`) observed during full E2E execution in visual Chromium.
- **SC-004**: 100% bilingual i18n coverage verified with zero missing translation keys in Ukrainian and English.
- **SC-005**: Zero synthetic DOM bypasses present in test fixtures or test cases.

---

## Assumptions

- Headless Chromium via Playwright is the standard E2E test browser runner.
- The existing ephemeral Eel port fixture in `tests/e2e/conftest.py` provides backend session isolation per test.
