# Feature Specification: Direct Root Node Creation Controls

**Feature Branch**: `025-root-node-controls`  
**Created**: 2026-08-14  
**Status**: Draft  
**Input**: User directive: "Додай інтрумент для додавання в робочу область елемнти, коли робоча область пуста користувач може додати один елемент але потім він не може в корні створити ще кілька напряму"

---

## Clarifications

### Session 2026-08-14
- Q: Де саме ви бажаєте розмістити кнопку для додавання нового кореневого вузла? → A: Both in panel header (`+ Кореневий вузол` / `+ Root Node`) and at the bottom of the tree canvas.

---

## 1. Problem Statement & Objectives

### Problem
When the Hierarchy Constructor Workspace contains one or more nodes, the `#treeEmptyState` container is hidden, leaving the user with no direct button or tool to create additional root-level (top-level) nodes on the canvas. Currently, users can only add child nodes to existing nodes, but cannot add sibling root trees without importing or using drag-and-drop.

### Objectives
1. Add an explicit **"Add Root Node"** (`#btnAddRootNode`) button in the workspace panel header actions (`.panel-header-actions`) that is always accessible regardless of whether the workspace is empty or populated.
2. Add a persistent **"Add Root Node"** bottom action row / button at the bottom of the tree canvas container when populated for quick 1-click root creation.
3. Ensure full localization (Ukrainian and English) with keyboard accessibility (`Enter`/`Escape` in modal) and instant DOM synchronization.

---

## 2. User Scenarios & Workflows

### Scenario 1: Creating multiple root nodes on a populated canvas
- **Given** the user already has 1 or more root nodes in the workspace.
- **When** the user clicks the "+ Root Node" button in the workspace panel header or at the bottom of the canvas.
- **Then** the "Create Node" modal opens with `parentId = null`.
- **When** the user enters a name and selects a data type, then clicks "Create Node".
- **Then** the new root node is created and appended to the workspace forest roots.

---

## 3. Functional Requirements

- **FR-001**: An accessible button `#btnAddRootNode` MUST be added to `.panel-header-actions` in `src/web/index.html`.
- **FR-002**: Clicking `#btnAddRootNode` MUST trigger `App.openAddModal(null, I18n.t('modal_create_title'))`.
- **FR-003**: An interactive footer action button `#btnAddRootCanvas` MUST be rendered at the bottom of the tree container when `roots.length > 0`.
- **FR-004**: All new buttons MUST have `data-i18n` and `data-i18n-attr` tags supporting instant bilingual translation between Ukrainian and English.
- **FR-005**: All existing keyboard shortcuts and drag-and-drop operations MUST remain unaffected.

---

## 4. Success Criteria

- **SC-001**: Users can create second, third, and subsequent root-level nodes directly without needing to empty the workspace.
- **SC-002**: Root creation button is accessible from both the workspace panel header and canvas footer.
- **SC-003**: 100% test pass rate in automated pytest suite.
