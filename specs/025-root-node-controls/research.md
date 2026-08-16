# Research & Decisions: Root Node Creation Controls

**Feature Branch**: `025-root-node-controls`  
**Spec**: [specs/025-root-node-controls/spec.md](spec.md)  
**Created**: 2026-08-14

---

## 1. UI Control Placement & Behavior

| Control Element | Location | Visibility | Action Triggered |
|---|---|---|---|
| `#btnAddRootHeader` | `.panel-header-actions` | Always visible | `App.openAddModal(null, t('modal_create_title'))` |
| `#btnAddRootCanvas` | Bottom of `#treeView` | Visible when `roots.length > 0` | `App.openAddModal(null, t('modal_create_title'))` |
| `#btnCreateRootEmpty` | `#treeEmptyState` | Visible when `roots.length === 0` | `App.openAddModal(null, t('modal_create_title'))` |

---

## 2. Localization Keys

| Key | Ukrainian (`uk`) | English (`en`) |
|---|---|---|
| `btn_add_root_header` | `"+ Кореневий вузол"` | `"+ Root Node"` |
| `btn_add_root_canvas` | `"Створити кореневий вузол"` | `"Create Root Node"` |
| `tooltip_add_root` | `"Додати новий кореневий вузол"` | `"Add new root node"` |
