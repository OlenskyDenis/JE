# Data Model & UI Contracts: Direct Root Node Creation Controls

**Feature Branch**: `025-root-node-controls`  
**Spec**: [specs/025-root-node-controls/spec.md](spec.md)  
**Created**: 2026-08-14

---

## 1. UI Elements Contract

```html
<!-- Panel Header Actions Control -->
<button id="btnAddRootHeader" class="btn btn-primary btn-sm" data-i18n-attr="title:tooltip_add_root">
    <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg>
    <span data-i18n="btn_add_root_header">+ Кореневий вузол</span>
</button>

<!-- Canvas Footer Action Control -->
<div class="tree-footer-actions">
    <button id="btnAddRootCanvas" class="btn-add-root-canvas" data-i18n-attr="title:tooltip_add_root">
        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg>
        <span data-i18n="btn_add_root_canvas">Створити кореневий вузол</span>
    </button>
</div>
```

---

## 2. Eel RPC Invocation Contract

```javascript
// Adding a root node passes parentId = null
eel.add_node(
    null,           // parent_id: null creates top-level root
    nodeName,       // name: string
    true,           // is_folder: boolean
    null,           // target_id: null
    null,           // zone: null
    selectedType    // data_type: string
);
```
