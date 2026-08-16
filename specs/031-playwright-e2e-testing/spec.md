# Feature Specification: Full Project Playwright E2E Automated Testing Suite

**Feature Branch**: `031-playwright-e2e-testing`  
**Created**: 2026-08-16  
**Status**: Clarified  
**Input**: User description: "Додати Playwright E2E автоматизовані тести. Покрий тестами весь існуючий функціонал проекту"

---

## Clarifications

### Session 2026-08-16
- **Q: Чи покриють ці тести весь існуючий функціонал і чи будуть вони оновлюватися та розширюватися для нових фіч?**  
  → **A**: **ТАК, на 100%**. Тести покривають усі 6 існуючих модулів (Хедер, Дерево CRUD, Drag-and-Drop, Блоки Excel, Унікальні за рівнями, Сайдбар і Налаштування). Усі наступні специфікації та редизайни будуть автоматично валідуватися цими тестами, а нові фічі будуть отримувати нові E2E тест-кейси.
- **Q: Як ви бажаєте налаштувати щоденний запуск тестів у консолі?**  
  → **A**: Запускати всі тести разом (`pytest` виконує і юніт-тести бекенду, і браузерні Playwright E2E-тести за одну команду).
- **Q: Який режим запуску браузера у Playwright для вас зручніший за замовчуванням?**  
  → **A**: Візуальний режим (Headed) — під час виконання тестів відкривається реальне вікно браузера, де наочно видно рух мишки, відкриття модалок, кліки та перетягування елементів (з можливістю перемикання у headless за потреби).

---

## 🗑️ Retirement & Cleanup Matrix *(mandatory for changes replacing existing logic)*

| Component / Endpoint / File | Action (Delete / Refactor / Migrate) | Replacement (Canonical New Approach) | Obsolete Tests to Remove / Update |
|---|---|---|---|
| Fragile static regex assertions in `tests/unit/test_frontend_contracts.py` | Refactor / Supplement | Full Playwright E2E Test Suite in `tests/e2e/` | Retain unit contracts as fast smoke tests; supplement with comprehensive E2E browser tests |

---

## 1. Problem Statement & Objectives

### Problem
1. **Testing Gap**: The current test suite (78 tests) exclusively verifies Python backend data structures, in-memory tree nodes, and static string regexes.
2. **Zero Browser Verification**: There are currently 0 tests verifying real DOM rendering, CSS visibility, physical mouse clicks, keyboard navigation, modal overlays, drag-and-drop hitboxes, and real-time UI updates in a live browser engine.
3. **Regression Blindspot**: As demonstrated during UI redesigns, major visual regressions and unclickable buttons went undetected because existing tests do not execute JavaScript or interact with the rendered page.

### Objectives
Build a **100% comprehensive End-to-End (E2E) Browser Test Suite** using **Playwright for Python** (`pytest-playwright`), covering every interactive user flow, button, modal, drag-and-drop gesture, and view mode:
1. **E2E Infrastructure**: Establish an automated Eel live test server fixture (`tests/e2e/conftest.py`) that starts an isolated backend on an ephemeral port, opens visual/headed Chromium, and tears down cleanly after test sessions.
2. **Navigation & Localization E2E**: Test language toggle (`UA` $\leftrightarrow$ `EN`), brand header, and dynamic translation of all UI labels, tooltips, and badges.
3. **Tree CRUD & Modals E2E**: Test creating root nodes, adding child nodes, editing names, changing data types, folder collapse/expand chevrons, and deletion confirmations.
4. **Drag-and-Drop E2E**: Test dragging columns from the Header Catalog into the Tree, and reordering nodes across all 3 zones (`BEFORE_SIBLING`, `AFTER_SIBLING`, `NEST_CHILD`).
5. **Multi-View Modes E2E**: Test switching between **Дерево (Tree)**, **Блоки Excel (Matrix)**, and **Унікальні за рівнями (Unique Levels)**, verifying coordinate headers, tier grouping, leaf-first partitioning, paragraph separators, and synchronized hover highlights.
6. **Sidebar & Resizer E2E**: Test catalog search filtering, sheet selector, path list preview, draggable splitter resizing, and collapse/expand strip transitions.
7. **Settings & Persistence E2E**: Test changing path delimiter (`\`, `/`), default data types, resetting to defaults, disk persistence in `settings.json`, and toast alert feedback.

---

## 2. User Scenarios & Testing *(Prioritized)*

### User Story 1 - Header Toolbar, Navigation & Bilingual Localization E2E (Priority: P1)

As a QA engineer or automated CI pipeline,  
I want automated browser tests to click the language switcher, header buttons, and sheet selectors,  
So that I can verify that all labels, buttons, and session actions execute without JavaScript errors.

**Independent Test**:
- Run `pytest tests/e2e/test_navigation_and_i18n.py`. Verify that language toggles between UA and EN update all DOM text, header titles, and placeholders in real time.

**Acceptance Scenarios**:
1. **Given** the app is open in Chromium, **When** clicking `#langBtnEn`, **Then** the active button switches to EN, and `#workspaceTitle` updates to "Hierarchy Constructor Workspace".
2. **Given** the language is EN, **When** clicking `#langBtnUk`, **Then** the active button switches to UA, and `#workspaceTitle` updates to "Робоча область конструктора ієрархії".
3. **Given** clicking `#btnRefresh`, **Then** a workspace refresh RPC is executed and a confirmation toast appears.

---

### User Story 2 - Tree Hierarchy CRUD & Folder Micro-Interactions E2E (Priority: P1) 🎯 MVP

As a user organizing a data hierarchy,  
I want automated E2E tests to verify creating, editing, collapsing, and deleting nodes,  
So that no button on tree node cards or modals can ever become unclickable.

**Acceptance Scenarios**:
1. **Given** an empty workspace, **When** clicking `#btnCreateRootEmpty`, **Then** `#nodeModal` opens with `#inputNodeName` focused.
2. **Given** entering "Finance" and submitting `#btnModalSubmit`, **Then** a new root node card `.tree-node` with title "Finance" appears in `#treeView`.
3. **Given** clicking `.action-btn.add-child` on "Finance" and entering "Q1", **Then** "Q1" appears inside `.tree-children` of "Finance", and "Finance" transforms into a folder with a rotating chevron `.node-toggle`.
4. **Given** clicking `.node-toggle`, **Then** `.tree-node` gains `.collapsed`, `.tree-children` is hidden, and clicking again expands it.
5. **Given** double-clicking on a leaf node's title or `.node-type-badge`, **Then** `#nodeModal` opens in edit mode, and updating the name and data type persists to the UI.
6. **Given** clicking `.action-btn.delete`, **Then** confirming the dialog removes the node from the tree.

---

### User Story 3 - Drag-and-Drop Gestures & Zone Highlighting E2E (Priority: P1)

As a user structuring spreadsheets,  
I want automated browser tests to drag items from the sidebar and reorder nodes in the tree,  
So that drop zones, indicators, and data type inheritance work flawlessly under real mouse events.

**Acceptance Scenarios**:
1. **Given** headers loaded in `#sidebarHeaderList`, **When** dragging a header card to a root node, **Then** `.drop-zone-inside` / `.drop-zone-after` highlights activate.
2. **Given** dropping on `.drop-zone-inside`, **Then** the header is nested as a child node in the tree and inherits the active default data type.
3. **Given** dragging a node onto its own descendant, **Then** cycle prevention rejects the drop with `.drop-prohibited` and a warning toast.

---

### User Story 4 - Multi-View Modes (Excel Blocks & Unique Levels) E2E (Priority: P2)

As a database analyst,  
I want automated tests to switch between Tree, Excel Blocks, and Unique Level views,  
So that matrix coordinate tables, tier backgrounds, leaf-first partitioning, and sync highlights render correctly.

**Acceptance Scenarios**:
1. **Given** a multi-level hierarchy loaded, **When** clicking `#btnViewMatrix`, **Then** `#treeView` is hidden, `#excelBlockView` is visible, and the coordinate header row (`Row 1`) renders columns.
2. **Given** clicking `#btnViewUniqueLevels`, **Then** `#uniqueLevelView` renders stacked level containers (`Tier 1`, `Tier 2`), with the leaf sub-group first, visual separator divider, and branch sub-group second.
3. **Given** hovering over a chip in Unique Levels, **Then** matching identical chips across other levels gain `.highlight-match-sync`.

---

### User Story 5 - Settings Modal, Persistence & Delimiter Propagation E2E (Priority: P2)

As a user configuring custom path delimiters,  
I want automated browser tests to open the Settings modal, change settings, and verify file persistence,  
So that `settings.json` is always synchronized and propagates to all paths.

**Acceptance Scenarios**:
1. **Given** clicking `#btnSettings`, **When** `#settingsModal` opens, **Then** `#inputSettingDelimiter` and `#selectSettingDefaultType` display active settings.
2. **Given** entering delimiter `/` and default type `Integer`, **When** clicking `#btnSettingsSave`, **Then** `#settingsModal` closes, a success toast appears, `settings.json` is updated on disk, and all paths in `#pathList` update to use `/`.
3. **Given** restarting or refreshing the browser, **When** reloading, **Then** the saved settings `/` and `Integer` are read directly from `settings.json` and remain active.

---

## 3. Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Install and configure `playwright` / `pytest-playwright` and Chromium in the Python environment.
- **FR-002**: Implement `tests/e2e/conftest.py` with:
  - Ephemeral port live server fixture running the Eel/Bottle web application.
  - Headed/visual Playwright browser context fixture with screenshot capture on failure.
- **FR-003**: Implement `tests/e2e/test_navigation_and_i18n.py`:
  - Language toggle (`UA` / `EN`) and title/button translation verification.
  - Template status badge rendering.
- **FR-004**: Implement `tests/e2e/test_tree_crud_and_modals.py`:
  - Root node creation (`#btnCreateRootEmpty`, `#btnAddRootHeader`, `#btnAddRootCanvas`).
  - Child node nesting, folder chevron rotation, and expand/collapse all toolbar buttons (`#btnExpandAll`, `#btnCollapseAll`).
  - Edit modal invocation via rename button and double-click.
  - Delete node flow with confirmation dialog.
- **FR-005**: Implement `tests/e2e/test_drag_and_drop.py`:
  - Dragging from Header Catalog (`.sidebar-header-item`) to tree canvas.
  - Tree node reordering across all 3 zones (`BEFORE_SIBLING`, `AFTER_SIBLING`, `NEST_CHILD`).
  - Cycle detection feedback (`.drop-prohibited`).
- **FR-006**: Implement `tests/e2e/test_excel_matrix_and_unique_levels.py`:
  - View mode switching (`#btnViewTree`, `#btnViewMatrix`, `#btnViewUniqueLevels`).
  - Matrix table structure, coordinate headers, and cell edit double-clicks.
  - Unique level rows, leaf sub-group first, paragraph divider, branch sub-group second, and hover sync.
- **FR-007**: Implement `tests/e2e/test_sidebar_and_resizer.py`:
  - Tab switching between Header Catalog and Export Preview.
  - Real-time catalog search filtering.
  - Sidebar resizer handle dragging and collapse/expand toggle strip.
- **FR-008**: Implement `tests/e2e/test_settings_and_persistence.py`:
  - Settings modal open/close, delimiter validation, and default data type change.
  - Disk persistence verification against `settings.json`.
  - Reset to defaults flow (`#btnSettingsReset`).
- **FR-009**: All E2E tests MUST run deterministically in `pytest` alongside backend unit tests.

---

## 4. Success Criteria *(mandatory)*

### Measurable Outcomes
- **SC-001**: 100% of all user-facing interactive elements (buttons, inputs, dropdowns, modals, drag items, tabs) covered by automated Playwright E2E tests.
- **SC-002**: 0 console errors or unhandled JavaScript exceptions across all E2E test runs.
- **SC-003**: 100% pass rate across the entire test suite (Unit + Integration + Contracts + E2E).
- **SC-004**: Deterministic execution time with clean server teardown and isolated temporary test fixtures.
