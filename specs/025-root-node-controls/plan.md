# Implementation Plan: Direct Root Node Creation Controls

**Feature Branch**: `025-root-node-controls`  
**Spec**: [specs/025-root-node-controls/spec.md](spec.md)  
**Created**: 2026-08-14

---

## 1. Technical Strategy & Component Architecture

### 1.1 Header Action Button (`src/web/index.html`)
- In `.panel-header-actions`, insert an action button `#btnAddRootHeader`:
  ```html
  <button id="btnAddRootHeader" class="btn btn-primary btn-sm" data-i18n-attr="title:btn_add_root" title="Створити кореневий вузол">
      <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg>
      <span data-i18n="btn_add_root">Кореневий вузол</span>
  </button>
  ```

### 1.2 Bottom Tree Action Row (`src/web/js/tree_renderer.js`)
- In `renderTree(roots, containerEl, collapsedNodeIds)`:
  - If `roots && roots.length > 0`, render all node cards and append a clean dashed/solid quick-action button `#btnAddRootCanvas`:
    ```html
    <div class="tree-footer-actions">
        <button id="btnAddRootCanvas" class="btn btn-secondary btn-sm btn-block" data-i18n-attr="title:btn_add_root">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg>
            <span data-i18n="btn_add_root">Створити кореневий вузол</span>
        </button>
    </div>
    ```

### 1.3 Localization (`src/web/js/i18n.js`)
- Add dictionary entries:
  - `uk`: `btn_add_root: "Кореневий вузол"`, `btn_add_root_full: "Створити кореневий вузол"`
  - `en`: `btn_add_root: "Root Node"`, `btn_add_root_full: "Create Root Node"`

### 1.4 Event Wiring (`src/web/js/app.js`)
- Bind click events for `#btnAddRootHeader` and delegated / direct click for `#btnAddRootCanvas` to invoke `this.openAddModal(null, t('modal_create_title'))`.

### 1.5 Styling (`src/web/css/style.css`)
- Style `.tree-footer-actions` and `.panel-header-actions` to ensure clean spacing, proper alignment, and dark theme consistency.

---

## 2. Risk & Regression Analysis
- **Tree State Integrity**: Adding a root with `parentId = null` is already supported by the backend `eel.add_node(null, name, isFolder, null, null, type)` and `WorkspaceForest.add_root_node`.
- **Zero Regressions**: Existing drag-and-drop, expand/collapse, and child additions remain 100% operational.
