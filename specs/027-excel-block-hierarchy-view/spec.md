# Feature Specification: Excel Block Hierarchy View (Multi-Level Header Matrix Mode)

**Feature Branch**: `027-excel-block-hierarchy-view`  
**Created**: 2026-08-16  
**Status**: Clarified  
**Input**: User description: "Додай ще один варінт відображення інформації як ще однин із фарінтів відображення Hierarchy Constructor Workspace. Другий варфнт повинен показувати структуру в людиночитному вигляді, максимально просто аналог як в ексель, візувльно воно повино розтавити всі елмети вкладенсті в блоки в ексель, так щоб якщо блок має кілька владеностей він був з верху а його вкладності з низу, блок який вище він займає стілкьи само місця скілкьи і та кількість блоків яка в нього вкладена."

---

## Clarifications

### Session 2026-08-16
- **Q: Яку інтерактивність повинні мати блоки в новому режимі «Блоки Excel»?**  
  → **A**: Інформаційний режим перегляду структури (Read-only) для швидкого аналізу колонок з можливістю перемикання на дерево для перетягування/редагування.
- **Q: Де саме розмістити перемикач режимів перегляду («Дерево» / «Блоки Excel»)?**  
  → **A**: У шапці робочої області (панелі Canvas) поруч із вибором аркуша та лічильником вузлів.
- **Q: Як вирівнювати кінцеві елементи, якщо різні гілки дерева мають різну глибину вкладеності?**  
  → **A**: За замовчуванням кінцеві елементи меншої глибини розтягуються вертикально (`rowspan`), заповнюючи висоту до нижнього рядка (як у багаторівневих заголовках Excel), створюючи ідеально вирівняну сітку.
- **Q: Який візуальний стиль відображення блоків у режимі «Блоки Excel»?**  
  → **A**: Стиль електронної таблиці (Spreadsheet Style) — чіткі межі комірок, заливка шарів, класичні лінії сітки як в Excel.
- **Q: Яку інформацію відображати всередині кожного блоку?**  
  → **A**: Чистий мінімалістичний вигляд: всередині блоку показується назва вузла (та компактний індикатор типу), а при наведенні курсору (hover tooltip) — повний детальний опис (назва, повний шлях, тип даних, кількість нащадків/колонок).
- **Q: Чи додавати над блоками рядок з індексами колонок Excel (A, B, C...)?**  
  → **A**: Так, додати верхній рядок з літерними індексами колонок (A, B, C, D... як в Excel) над блоками для точної координатної прив'язки.
- **Q: Як поводитися з шириною колонок?**  
  → **A**: Повний адаптивний розмір — колонки мають мінімальну ширину (наприклад `140px`) з автоматичним розширенням за вмістом та можливістю плавного горизонтального скролу для великих таблиць.
- **Q: Яким способом перемикати режими перегляду та як зберігати стан?**  
  → **A**: Перемикання здійснюється кліком мишкою по кнопках сегментованого перемикача у шапці робочої області; обраний режим (`tree` або `matrix`) зберігається у `localStorage` (`je_workspace_view_mode`) та відновлюється при перезапуску додатку.
- **Q: Який візуальний вигляд та елементи керування повинна мати згорнута бічна панель?**  
  → **A**: Тонка вертикальна смуга (~24-28px) з кнопкою-стрілкою по центру та можливістю кліку для розгортання; кнопки згортання/розгортання доступні в шапці вкладок сайдбару та на смузі спліттера.

---

## 1. Problem Statement & Objectives

### Problem
Currently, the **Hierarchy Constructor Workspace** only offers a single vertical indented tree view (`#treeView`). While the tree view is effective for drag-and-drop reorganization and expanding/collapsing folders, users who design complex tabular database exports or Excel reporting templates often struggle to visualize how the parent-child hierarchy translates into multi-level Excel column headers (e.g., merged super-headers spanning multiple sub-columns).

Users need an alternative, human-readable, Excel-like visual block representation directly within the workspace where:
1. Hierarchy levels are rendered as horizontal block layers (parents on top, children directly underneath).
2. Parent blocks automatically span horizontally across the exact number of column units (leaf blocks) nested below them (`colspan`), mimicking Excel merged header cells.
3. Users can seamlessly switch between the **Tree View** and the **Excel Block Matrix View** without losing workspace state.

### Objectives
1. Add a **View Mode Switcher** (segmented toggle: `Tree View` / `Excel Blocks View`) to the Hierarchy Constructor Workspace toolbar.
2. Implement a dedicated **Excel Block Matrix Renderer** (`#excelBlockView`) that translates the multi-root `WorkspaceForest` into a structured, responsive HTML table/CSS grid matrix:
   - **Parent Nodes**: Placed in upper tier rows, spanning horizontally (`colspan`) across the total count of their nested leaf descendants.
   - **Child / Leaf Nodes**: Placed in subsequent tier rows directly under their respective parent blocks, with individual column width.
   - **Vertical Span (`rowspan`)**: Leaf nodes reaching terminal levels span down to the bottom tier for consistent grid alignment.
   - **Visual Styling**: Excel-like cell borders, distinct header tier shading, typography, node name labels, and leaf element data type badges.
3. Ensure seamless real-time synchronization between active sheet switches, tree modifications (add/rename/delete/reorder), delimiter settings, and view toggling.
4. Support full bilingual (Ukrainian `uk` and English `en`) localization for all view switcher controls, tooltips, and empty states.

---

## 2. User Scenarios & Testing *(Prioritized)*

### User Story 1 - Toggle Between Tree View and Excel Block Matrix View (Priority: P1)

As a database architect / data analyst,  
I want to toggle between the classic Tree View and an Excel Block Matrix View in the workspace,  
So that I can inspect my hierarchy structure both as an operational tree and as an Excel-style multi-level column header matrix.

**Why this priority**: Core navigation mechanism enabling the dual-view workspace experience.

**Independent Test**: Can be tested by clicking the view switcher buttons in the workspace header and verifying that the active canvas switches between `#treeView` and `#excelBlockView` smoothly.

**Acceptance Scenarios**:
1. **Given** a loaded hierarchy, **When** the user clicks the "Excel Blocks" view mode toggle, **Then** `#treeView` is hidden and `#excelBlockView` is rendered with the active hierarchy.
2. **Given** the user is in "Excel Blocks" view, **When** they click "Tree View", **Then** `#excelBlockView` is hidden and `#treeView` is displayed.
3. **Given** the workspace is empty, **When** switching to "Excel Blocks" view, **Then** a friendly localized empty state is displayed with a call-to-action to import a file or create root nodes.

---

### User Story 2 - Excel Block Layout with Proportional Parent Colspan (Priority: P1)

As a report designer,  
I want parent blocks to appear above their nested children and occupy the exact width of all their sub-blocks combined,  
So that I can immediately see the hierarchical grouping and column span just like merged cells in Microsoft Excel.

**Why this priority**: Fundamental functional requirement specified by the user.

**Independent Test**: Can be tested with a multi-level structure (e.g., `Finance\Q1\Revenue`, `Finance\Q1\Expenses`, `Finance\Q2\Revenue`) and verifying that `Finance` spans 3 columns, `Q1` spans 2 columns, `Q2` spans 1 column, and each terminal leaf occupies 1 column.

**Acceptance Scenarios**:
1. **Given** a parent node with 3 leaf descendants across 2 sub-folders, **When** rendered in Excel Block View, **Then** the top-level parent block spans 3 columns (`colspan = 3`), its child folders span their respective leaf counts (e.g. 2 and 1), and leaf nodes are rendered in the bottom row.
2. **Given** a single standalone root leaf (no children) alongside multi-level trees, **When** rendered in Excel Block View, **Then** the standalone leaf block spans 1 column and extends full height (`rowspan = maxDepth`).
3. **Given** any leaf block in the matrix, **Then** it displays both the node name and its assigned data type badge (e.g. `Currency`, `Date`, `Text`).

---

### User Story 3 - Real-Time Workspace Synchronization & Multilingual Localization (Priority: P2)

As a multilingual user,  
I want the Excel Block View to stay synchronized when switching sheets, editing nodes, or changing language preferences,  
So that all view modes remain consistent and accurately localized in Ukrainian and English.

**Why this priority**: Ensures seamless integration with existing multi-sheet sessions, undo/edit workflows, and i18n support.

**Acceptance Scenarios**:
1. **Given** an active session with multiple sheets, **When** switching sheets via `#activeSheetSelector`, **Then** the Excel Block View instantly re-renders the newly active sheet's hierarchy.
2. **Given** the language switcher is toggled between `UA` and `EN`, **Then** all view mode button labels, tooltips, data type badges, and empty state text instantly update in the selected language.
3. **Given** the view preference is changed, **Then** the selected view mode (`tree` or `matrix`) is remembered in `localStorage` across page refreshes.

---

### User Story 4 - Collapsible Right Sidebar Panel (Priority: P2)

As a power user designing wide Excel matrices or complex tree hierarchies,  
I want to quickly collapse the right sidebar panel (`#unifiedSidebar`) into a slim vertical line/strip and expand it back on demand,  
So that I can maximize horizontal and vertical workspace canvas space for visual inspection.

**Acceptance Scenarios**:
1. **Given** the unified sidebar is expanded, **When** clicking the collapse toggle button (`#btnToggleSidebarCollapse` or dedicated icon on splitter), **Then** `#unifiedSidebar` shrinks to a minimal vertical line/strip (`collapsed` state) and the workspace canvas expands to fill the entire remaining screen width.
2. **Given** the sidebar is collapsed, **When** clicking the expand toggle button on the collapsed bar, **Then** `#unifiedSidebar` smoothly expands back to its previous user-resized or default width.
3. **Given** the sidebar collapsed state is changed, **Then** the preference is stored in `localStorage` (`je_sidebar_collapsed`) and restored across app reloads.

---

## 3. Requirements

### Functional Requirements (FR)

- **FR-001**: The workspace header MUST include a segmented View Mode Switcher control (`#viewModeSwitcher`) with two options: `Tree View` (`#btnViewTree`) and `Excel Blocks View` (`#btnViewMatrix`).
- **FR-002**: The default view mode MUST be `Tree View`, but the active view mode preference MUST be persisted in `localStorage` (`je_workspace_view_mode`).
- **FR-003**: In `Excel Blocks View`, the canvas MUST calculate the maximum depth of the active forest and generate a multi-tier block matrix layout:
  - Each tree level corresponds to a tier row (Tier 0 for roots, Tier 1 for level-1 children, etc.).
  - A node with `N` leaf descendants MUST span `N` columns horizontally (`colspan = N`).
  - A leaf node at level `L` in a tree with max depth `D` MUST span `(D - L)` rows vertically (`rowspan = max(1, D - L)`).
- **FR-004**: Each block in the Excel Matrix MUST display:
  - Clean, minimal block content: node title / name with clean typography and Excel-like cell boundaries.
  - An optional compact icon / type tag indicator.
  - A rich tooltip / title on hover detailing: node name, full absolute path (using active delimiter), data type (for leaf elements), and number of nested columns / children.
- **FR-005**: The Excel Matrix container MUST provide responsive horizontal and vertical scrolling (`overflow: auto`) with sticky header rows or distinct grid lines so large structures with dozens of columns remain legible and accessible.
- **FR-006**: When nodes are added, edited, deleted, or reordered, both the Tree View and Excel Block View MUST receive the updated `roots` state and update in real-time.
- **FR-007**: All UI text for the view mode switcher, block badges, tooltips, and empty states MUST be registered in both `uk` and `en` dictionaries in `src/web/js/i18n.js`.
- **FR-008**: The right sidebar (`#unifiedSidebar`) MUST support quick collapsing and expanding:
  - When collapsed (`.sidebar-collapsed`), the sidebar narrows to a compact vertical bar (~28px) with a dedicated expand button, allowing the main canvas panel to expand.
  - When expanded, the sidebar returns to its previous width.
  - State is persisted in `localStorage` (`je_sidebar_collapsed`).
- **FR-009**: The sidebar tab header (`.sidebar-tab-header`) MUST combine the catalog and paths tabs into a compact dropdown selector (`#sidebarTabSelector`):
  - Contains options for "Каталог колонок" (`catalog`) and "Попередній перегляд" (`paths`), persisting active tab selection.
  - Displays the active counter badge dynamically alongside the selector.
  - The collapse button (`#btnToggleSidebarCollapse`) MUST have `flex-shrink: 0` and remain fully visible and clickable at all times, even when the sidebar is manually resized down to its minimum width.

---

## 4. Success Criteria

1. **Visual Match with Excel Multi-Level Headers**: Hierarchies render as stacked block cells where parent width = sum of child widths, matching Excel merged cell hierarchy conventions.
2. **Zero Loss of State on Toggle**: Switching between Tree View and Excel Block View preserves all active sheet selections, unsaved edits, and template bindings.
3. **Responsive & Performant**: Complex hierarchies (50+ columns, 5+ levels deep) render in under 50ms without UI freezing.
4. **Fluid Sidebar Collapse**: Toggling sidebar collapse instantly grants full width to canvas and restores effortlessly.
5. **100% Bilingual**: Both view modes and sidebar collapse controls support Ukrainian and English localization seamlessly.
6. **Full Test Suite Integrity**: All automated pytest unit and integration tests continue to pass with 0 regressions.
