# Feature Specification: Leaf-First Partitioning, Paragraph Separation & Visual Ergonomics in Unique Level View

**Feature Branch**: `030-unique-levels-leaf-grouping`  
**Created**: 2026-08-16  
**Status**: Clarified  
**Input**: User description: "Додай для Unique by Levels щоб елменти які не мають вкладеностей були спочатку в кожному рівні і їх розіляв абзац з іншими елементами" + "Правка в цій же спеццікації, візульно сильно давить на очі, потрібно зробити більш легшою гамою кольорів, для орінтира візьми Excel Blocks та Tree View"

---

## Clarifications

### Session 2026-08-16 (Visual Ergonomics & Color Harmony)
- **Q: Яка кольорова гама має бути використана для карток та контейнерів рівнів?**  
  → **A**: Легка, спокійна та стримана гама, що повністю гармонує з `Excel Blocks` та `Tree View`:
  - Рівневі панелі (`.level-row-container`) використовують м'який фон панелей `var(--bg-panel)` (`#1e293b`) або темний спокійний сланець, замість важкого контрастного `#334155`.
  - Чіпи (`.level-header-chip`) мають спокійний темний фон (`#0f172a` / `#131d2e`) з тонкими нейтральними рамками `rgba(255, 255, 255, 0.08)`.
  - Усуваються агресивні товсті кольорові смуги зліва на чіпах (`border-left`), які створювали зоровий шум і перевтому очей.
  - Підгрупи мають мінімалістичні витончені заголовки та спокійні пастельні/нейтральні пілюлі (м'який нейтральний сланець для кінцевих елементів, делікатний крижаний блакитний для категорій).
  - Абзацний роздільник (`.level-group-separator`) — ледь помітна делікатна лінія з м'якими відступами, що дає очам відпочити між секціями.

---

## 🗑️ Retirement & Cleanup Matrix *(mandatory for changes replacing existing logic)*

| Component / Endpoint / File | Action (Delete / Refactor / Migrate) | Replacement (Canonical New Approach) | Obsolete Tests to Remove / Update |
|---|---|---|---|
| Single undivided `.level-chips-container` in `UniqueLevelRenderer` | Refactor | Partitioned dual-group rendering (`.level-group-leaves` and `.level-group-branches` separated by `.level-group-paragraph-separator`) | None |
| High-contrast `#334155` level rows & heavy saturated chip borders | Refactor | Soft, low-strain palette harmonized with Excel Blocks (`#1e293b`) & Tree View | None |

---

## 1. Problem Statement & Objectives

### Problem
In the **Unique Level Hierarchy View** (`#uniqueLevelView` / `Unique by Levels`), all unique header chips for a given depth level were previously rendered in a single flat list with heavy visual contrast (`#334155` backgrounds, saturated thick left borders on every chip, and intense badges). This caused two main issues:
1. **Lack of Structure**: Users could not easily differentiate terminal data fields (leaves without children) from structural category groupings (branches with children).
2. **Visual Strain**: The heavy contrast and cluttered colored accents strained users' eyes during prolonged hierarchy analysis.

### Objectives
1. **Leaf-First Ordering**: Within every level row (Tier 0, Tier 1, Tier 2, etc.), elements without nested children (`hasChildren === false` / `isLeaf === true`) must be positioned **first**.
2. **Visual Paragraph Separation ("Абзац")**: A subtle, elegant visual break / paragraph gap / sub-section separator must clearly divide the leaf elements from branch elements with nested children.
3. **Ergonomic, Low-Strain Color Palette**:
   - Align visual surfaces, backgrounds, borders, and typography with `Excel Blocks` and `Tree View`.
   - Soft `#1e293b` panel backgrounds with subtle `1px` borders.
   - Clean, lightweight chips with restrained accents (no aggressive colored left-bars).
   - Minimalist muted sub-headers and subtle pill counters.
4. **Adaptive Group Rendering**:
   - When a level contains both leaf and branch elements: render Leaf section first, paragraph separator, and Branch section second.
   - When a level contains only leaves or only branches: render only the relevant section cleanly without empty containers or dangling dividers.
5. **Full Feature & Interaction Parity**:
   - Maintain frequency badges (`×2`, `×3`), cross-level match badges (`[Збіг: Рівні X, Y]`), synchronized hover highlighting (`highlight-match-sync`), and double-click batch editing (`openEditModal`) across all groups.
6. **Multilingual Localization**:
   - Complete Ukrainian (`uk`) and English (`en`) localization for all sub-group labels and counters.

---

## 2. User Scenarios & Testing *(Prioritized)*

### User Story 1 - Leaf-First Partitioning & Ergonomic Visual Separation (Priority: P1)

As a database designer or hierarchy auditor,  
I want terminal leaf elements (without nested children) to appear first in each level row, separated by an understated paragraph break from branch elements, in a calm, eye-friendly color palette,  
So that I can comfortably inspect and analyze hierarchy levels without eye strain.

**Why this priority**: Directly satisfies both the functional partitioning requirement and the visual comfort requirement.

**Independent Test**:
- Load any multi-level hierarchy containing both leaf and non-leaf nodes on the same level. Verify that leaf items appear first, the paragraph separator is clean and subtle, and the color palette is soft and harmonized with Excel Blocks and Tree View.

**Acceptance Scenarios**:
1. **Given** a hierarchy where Level 0 has both leaf roots and branch roots, **When** viewing in `Unique by Levels` mode, **Then** leaf items appear first, followed by a subtle paragraph separator, followed by branch items.
2. **Given** the overall appearance of `#uniqueLevelView`, **When** compared with `Excel Blocks` and `Tree View`, **Then** the surfaces use consistent `--bg-panel` (`#1e293b`), soft neutral typography, and calm borders without harsh colored bars.
3. **Given** a level containing *only* leaf elements, **When** rendered, **Then** only the Leaf section is displayed with 0 empty paragraph dividers.
4. **Given** a level containing *only* branch elements, **When** rendered, **Then** only the Branch section is displayed cleanly.

---

### User Story 2 - Interactive Feature Parity & Hover Synchronization (Priority: P1)

As a user exploring duplicated vocabulary and editing nodes in Unique Level View,  
I want cross-level duplicate badges, hover synchronization, and double-click editing to work consistently across both leaf and branch sections,  
So that partitioning does not compromise any existing features.

**Acceptance Scenarios**:
1. **Given** a header term that appears in both Leaf and Branch groups across different levels, **When** hovering over either chip, **Then** both chips smoothly activate the synchronized highlight style (`highlight-match-sync`).
2. **Given** any chip in either the Leaf or Branch group, **When** double-clicked, **Then** the Node Edit modal opens with batch update support.
3. **Given** saving an edit, **Then** all 3 workspace views (`Дерево`, `Блоки Excel`, `Унікальні за рівнями`) immediately update.

---

### User Story 3 - Multilingual Localization (Priority: P2)

As a multilingual user,  
I want sub-group labels, counters, and tooltips to be clearly displayed in Ukrainian or English.

**Acceptance Scenarios**:
1. **Given** Ukrainian language (`uk`), **When** viewing partitioned levels, **Then** sub-section labels display in Ukrainian (e.g. `Кінцеві елементи (без вкладеностей)` / `Категорії (з вкладеностями)`).
2. **Given** English language (`en`), **When** viewing partitioned levels, **Then** labels switch to English (e.g. `Terminal elements (no children)` / `Categories (with children)`).

---

## 3. Requirements

### Functional Requirements

- **FR-001**: `UniqueLevelRenderer.extractUniqueLevels` MUST evaluate each unique header term on a depth level to determine if it is a leaf element (`isLeaf: true` / no child nodes) or a branch element (`isLeaf: false` / has child nodes).
- **FR-002**: For each level, `extractUniqueLevels` MUST partition items into `leafItems` and `branchItems` sorted alphabetically.
- **FR-003**: In `UniqueLevelRenderer.renderUniqueLevels`, `leafItems` MUST be rendered before `branchItems` in each level row.
- **FR-004**: When both `leafItems` and `branchItems` exist on a level, a visual paragraph separator (`.level-group-separator`) MUST separate the two groups.
- **FR-005**: If `leafItems` is empty, only the branch group is rendered. If `branchItems` is empty, only the leaf group is rendered without empty containers or dangling dividers.
- **FR-006**: Sub-groups MUST display subtle, minimalist headers (`.level-subgroup-header`) with small pill counters.
- **FR-007**: Every chip in both groups MUST preserve all attributes, badges, tooltips, synchronized hover highlights, and double-click edit handlers.
- **FR-008**: All new text strings, sub-group labels, and tooltips MUST be registered in both `uk` and `en` dictionaries in `src/web/js/i18n.js`.
- **FR-009**: Styles in `src/web/css/style.css` MUST use a soft, low-strain dark theme palette matching `Excel Blocks` and `Tree View`:
  - Panel background: `var(--bg-panel)` (`#1e293b`) with `1px solid rgba(255, 255, 255, 0.07)`.
  - Chip background: `#0f172a` / `#131d2e` with clean border `1px solid rgba(255, 255, 255, 0.08)`.
  - No harsh thick colored left bars on individual chips.
  - Paragraph separator: fine `1px` subtle divider `rgba(255, 255, 255, 0.05)` with comfortable vertical spacing.

---

## 4. Success Criteria

- **SC-001**: 100% of levels with mixed elements display leaf items first, followed by a subtle paragraph separation and branch items.
- **SC-002**: Visual palette seamlessly harmonizes with Excel Blocks and Tree View, eliminating high-contrast eye fatigue.
- **SC-003**: 0 dangling dividers or empty placeholders on single-type levels.
- **SC-004**: 100% test pass rate across all unit, integration, and frontend contract tests.
