# Feature Specification: Unique Level Hierarchy View (Level-by-Level Unique Headers & Cross-Level Match Highlighting)

**Feature Branch**: `028-unique-level-hierarchy-view`  
**Created**: 2026-08-16  
**Status**: Clarified  
**Input**: User description: "Додай до Режим перегляду / View Mode в Hierarchy Constructor Workspace, ще один варінт відображення даних, це порвнева структура унікальних елментів заголовків, на кожному рівні лише унікальні заголовки. Підсвічуй повне співпадіння між рівнями"

---

## Clarifications

### Session 2026-08-16
- **Q: Як розташувати рівні ієрархії у вікні перегляду?**  
  → **A**: Горизонтальні рядки рівнів один під одним (Рівень 0 / Корені зверху, Рівень 1 нижче, Рівень 2 ще нижче...), всередині кожного рядка — горизонтальний перелік унікальних чіпів/карток заголовків.
- **Q: Як підсвічувати елементи, які повторюються на різних рівнях?**  
  → **A**: Акцентний бейдж збігу (наприклад, `[Збіг: Рівень 0, 1]`) + інтерактивне спільне підсвічування всіх копій цього заголовка на всіх рівнях одночасно при наведенні курсору (hover sync).
- **Q: Чи враховувати регістр літер при пошуку повних співпадінь між рівнями?**  
  → **A**: Нечутливий до регістру (Case-insensitive: "Код" та "код" вважаються однаковими).
- **Q: Як обробляти редагування в режимі «Унікальні за рівнями», якщо назва зустрічається кілька разів (наприклад ×2, ×3)?**  
  → **A**: Відкривати редагування представницького вузла та оновлювати всі однакові входження на цьому рівні при зміні назви/типу.
- **Q: Чи додавати візуальну підказку для редагування подвійним кліком у спливаючі підказки та курсор?**  
  → **A**: Показувати курсор pointer на клікабельних елементах та додати підказку «(Подвійний клік для редагування)» / «(Double-click to edit)» у спливаючий tooltip.
- **Q: Яке сповіщення (Toast) показувати після успішного масового збереження?**  
  → **A**: Точний інформативний тост: `«Оновлено {count} вузл(ів) «{name}» на цьому рівні»` / `«Updated {count} node(s) "{name}" on this level»`.
- **Q: Як візуально оформити повідомлення про масове редагування в модальному вікні?**  
  → **A**: Акуратний інфо-блок (`.modal-batch-notice` / Alert box з іконкою) над полем введення в модальному вікні.

---

## 1. Problem Statement & Objectives

### Problem
In complex data models and multi-sheet reporting templates, hierarchies often contain repetitive header terms across different depths (e.g., identical names like "Сума", "ID", "Код", "Дата", or "Загальні" appearing at Level 0, Level 1, and Level 2). Currently, users can inspect hierarchies either as an indented parent-child tree (`#treeView`) or as multi-column merged Excel blocks (`#excelBlockView`), but neither mode provides a consolidated cross-level vocabulary and duplicate analysis view.

Users need a dedicated **Unique Level Structure View** to:
1. View a clear tier-by-tier breakdown (Level 0, Level 1, Level 2, ...) showing only deduplicated, unique header names present at each depth level.
2. Immediately spot exact name duplicates/collisions that occur across different levels via distinct visual highlighting (e.g. cross-level match badges, color tags, or occurrence indicators).
3. Inspect how header names are distributed across depth layers and navigate seamlessly between all 3 view modes (`Дерево` / `Блоки Excel` / `Унікальні за рівнями`).

### Objectives
1. Expand the **View Mode Switcher** in the workspace header into a 3-way segmented control:
   - **`Tree View`** (`#btnViewTree`)
   - **`Excel Blocks`** (`#btnViewMatrix`)
   - **`Unique Levels`** (`#btnViewUniqueLevels` / "Унікальні за рівнями")
2. Implement a dedicated **Unique Level Renderer** (`#uniqueLevelView`) that:
   - Extracts all nodes from the active `WorkspaceForest` grouped by their depth level ($0, 1, \dots, D-1$).
   - Computes deduplicated unique header names for each level along with frequency counts and occurrences.
   - Identifies header names that exist across **multiple levels** (cross-level matches) and highlights them with distinct matching colors/badges.
   - Provides rich tooltips showing full paths and parent contexts for each unique header card.
3. Ensure real-time synchronization between active sheet switches, tree edits (add/rename/delete/reorder), delimiter settings, and view toggling.
4. Support full bilingual (`uk` and `en`) localization for all new buttons, headers, tooltips, and badges.

---

## 2. User Scenarios & Testing *(Prioritized)*

### User Story 1 - 3-Way Workspace View Switching (Priority: P1)

As a database architect / data analyst,  
I want to toggle between Tree View, Excel Blocks View, and Unique Level View,  
So that I can analyze my hierarchy from structural, tabular, and vocabulary perspectives.

**Acceptance Scenarios**:
1. **Given** the workspace header toolbar, **When** inspecting `#viewModeSwitcher`, **Then** it presents 3 options: `Дерево` / `Блоки Excel` / `Унікальні за рівнями` (`Tree View` / `Excel Blocks` / `Unique Levels`).
2. **Given** the user clicks `Унікальні за рівнями`, **Then** the canvas smoothly transitions to the Unique Level View (`#uniqueLevelView`), and the user's choice is saved in `localStorage` (`je_workspace_view_mode = 'unique_levels'`).
3. **Given** the user switches back to `Дерево` or `Блоки Excel`, **Then** the canvas restores the selected view with 0 data loss.

---

### User Story 2 - Deduplicated Level-by-Level Breakdown & Cross-Level Highlighting (Priority: P1)

As an auditor of reporting hierarchies,  
I want to see all unique headers partitioned by level with highlighted cross-level duplicates,  
So that I can identify repeated naming patterns, taxonomy redundancies, and ambiguous column names.

**Acceptance Scenarios**:
1. **Given** a hierarchy containing `Finance \ Revenue`, `Sales \ Revenue`, and `Operations \ Costs`, **When** rendered in Unique Level View:
   - **Level 0 (Roots)** displays: `Finance`, `Sales`, `Operations` (3 unique cards).
   - **Level 1 (Children)** displays: `Revenue` (2 occurrences), `Costs` (1 occurrence) (2 unique cards).
2. **Given** a hierarchy where the term `ID` or `Date` appears at both Level 0 (`Root \ ID`) and Level 1 (`Root \ Sub \ ID`), **When** rendered in Unique Level View, **Then** all cards with exact matching names across different levels are highlighted with a distinct matching tag/border (e.g. `[Cross-Level Match: L0, L1]`).
3. **Given** hovering over a unique header card, **Then** a tooltip displays the count of occurrences and the list of absolute paths where this name appears.

---

### User Story 3 - Real-Time Synchronization & Multilingual Localization (Priority: P2)

As a multilingual user,  
I want the Unique Level View to update instantly when editing the tree, switching sheets, or changing the language,  
So that all vocabulary metrics and highlights stay accurate.

**Acceptance Scenarios**:
1. **Given** an active session with multiple sheets, **When** switching sheets via `#activeSheetSelector`, **Then** the Unique Level View instantly recalculates and re-renders the levels for the new sheet.
2. **Given** the language switcher is toggled between `UA` and `EN`, **Then** all level titles (`Рівень 0 (Корені)` / `Level 0 (Roots)`), match badges, and tooltips update in the selected language.

---

### User Story 4 - Double-Click Editing in Excel Blocks & Unique Level Views (Priority: P2) (Quick Fix)

As a user inspecting a hierarchy in Excel Blocks or Unique Levels mode,  
I want to double-click on any cell or header chip to open the Node Edit modal,  
So that I can quickly rename nodes or change their data types without needing to switch back to Tree View.

**Acceptance Scenarios**:
1. **Given** the workspace is in `Excel Blocks View` (`#excelBlockView`), **When** the user double-clicks on any block cell (`.matrix-cell`), **Then** the Node Edit modal opens pre-populated with the node's current name and data type, allowing renaming and type editing.
2. **Given** the workspace is in `Unique Level View` (`#uniqueLevelView`), **When** the user double-clicks on any unique header chip (`.level-header-chip`), **Then** the Node Edit modal opens for that header element, allowing quick renaming or type updates.
3. **Given** the user saves changes in the Node Edit modal, **Then** all 3 views (`Tree View`, `Excel Blocks`, and `Unique Levels`) immediately refresh with the updated node name and data type.

---

## 3. Requirements

### Functional Requirements (FR)

- **FR-001**: The `#viewModeSwitcher` in workspace header MUST support 3 view modes: `tree`, `matrix`, and `unique_levels`.
- **FR-002**: In `Unique Level View` (`#uniqueLevelView`), the layout MUST display stacked horizontal level rows (Level 0 on top, Level 1 below, Level 2 below, etc.), where each row contains a horizontal flow of unique header chips/cards.
- **FR-003**: On each level row, header names MUST be deduplicated so that each distinct name appears exactly once per level.
- **FR-004**: Each unique header chip/card MUST show:
  - Header name.
  - Frequency badge showing occurrence count if > 1 (e.g. `×2`, `×3`).
  - Cross-level match badge if the exact same header name (case-insensitive) also appears on at least one other depth level (e.g. `[Збіг: Рівень 0, 1]`).
- **FR-005**: Cross-level matching MUST be case-insensitive, and hovering over any matching card MUST interactively highlight all matching instances across all other levels simultaneously.
- **FR-006**: Hovering over a unique header card MUST show a rich tooltip detailing occurrence count, level breakdown, and all absolute paths where this header occurs.
- **FR-007**: When nodes are added, edited, deleted, or reordered, `#uniqueLevelView` MUST re-render in real-time alongside Tree and Matrix views.
- **FR-008**: All UI labels, badges, level headers, and tooltips MUST be registered in both `uk` and `en` dictionaries in `src/web/js/i18n.js`.
- **FR-009**: Selected view mode MUST be persisted in `localStorage` (`je_workspace_view_mode`).
- **FR-010**: Double-clicking on any `.matrix-cell` in Excel Blocks View (`#excelBlockView`) MUST trigger the Node Edit modal (`openEditModal`) for that node.
- **FR-011**: Double-clicking on any `.level-header-chip` in Unique Level View (`#uniqueLevelView`) MUST trigger the Node Edit modal (`openEditModal`) for that header node.
- **FR-012**: When opening the Node Edit modal from Unique Level View (`#uniqueLevelView`):
  - The modal MUST display an informative batch notice (`#modalBatchNotice`) stating the count of items that will be edited simultaneously on that level (e.g., `Буде змінено всі {count} вузли з назвою «{name}» на цьому рівні.` / `All {count} nodes named "{name}" on this level will be updated simultaneously.`).
  - Submitting the modal MUST update all node instances on that level in a unified operation and immediately refresh all 3 workspace views.

---

## 4. Success Criteria

1. **Exact Vocabulary Deduplication**: Each level displays 100% deduplicated unique names.
2. **Instant Cross-Level Duplicate Discovery**: Headers repeated across different depth levels are highlighted immediately with zero lag.
3. **Double-Click Edit Universality**: Double-clicking elements in Tree View, Excel Blocks View, and Unique Level View seamlessly opens the edit modal across all 3 view modes.
4. **Responsive Multi-Tier Layout**: Clean dark theme cards with horizontal scrolling for deep hierarchies.
5. **100% Bilingual**: Complete Ukrainian and English localization.
6. **Full Test Suite Integrity**: All automated pytest tests (including frontend contract tests) pass with 0 regressions.
