# System Map Alignment & Redundancy Audit Checklist

**Date**: 2026-08-14  
**Governing Principles**: Constitution Principle VI (System Map First-Load & Proactive Redundancy Audit) & Principle VII (Red Teaming)  
**System Map Reference**: [`.specify/system_map.md`](../system_map.md)  
**Unified Architecture Model**: Dynamic `HierarchyNode` (State derived from `len(children) > 0`)

---

## Executive Summary of Findings

Following the unification of the tree model into the dynamic `HierarchyNode` (Feature 008) and the migration to native OS file dialogs (Feature 003), several UI form controls, event query selectors, RPC bridge parameters, and DOM elements have become **completely obsolete, redundant, or logically contradictory** to the active system architecture.

---

## Category 1: Frontend Form Inputs & Obsolete Radio Controls

### 🔴 Item 1.1: Static "Node Type" Radio Selector in Creation Modal
- **Location**: [`src/web/index.html`](file:///E:/JE/src/web/index.html#L124-L142)
- **Code Snippet**:
  ```html
  <div class="form-group">
      <label>Node Type</label>
      <div class="radio-group">
          <label class="radio-card">
              <input type="radio" name="nodeType" value="container" checked>
              <span class="radio-label">
                  <strong>Folder / Container</strong>
                  <small>Can contain sub-folders and child items</small>
              </span>
          </label>
          <label class="radio-card">
              <input type="radio" name="nodeType" value="leaf">
              <span class="radio-label">
                  <strong>Leaf Item</strong>
                  <small>Terminal data node in hierarchy</small>
              </span>
          </label>
      </div>
  </div>
  ```
- **Architectural Contradiction**:
  - The unified `HierarchyNode` model has eliminated static node typing.
  - A newly created node always starts with `0` children (`is_folder = False`).
  - As soon as a child is attached, it automatically upgrades to a folder (`is_folder = True`).
  - **Verdict**: Asking the user to choose "Folder" vs "Leaf" is 100% redundant, misleading, and contradictory to dynamic node unification.
- **Remediation**: Remove the "Node Type" radio group from `nodeModal` in `index.html`. The modal should only ask for `Node Name`.

---

## Category 2: Frontend JavaScript Logic & Dead Query Selectors

### 🔴 Item 2.1: Obsolete `nodeType` DOM Query and Value Extraction
- **Location**: [`src/web/js/app.js`](file:///E:/JE/src/web/js/app.js#L312-L316)
- **Code Snippet**:
  ```javascript
  const selectedType = document.querySelector('input[name="nodeType"]:checked').value;
  const isContainer = selectedType === 'container';
  const res = await eel.add_node(this.activeParentIdForModal, name, isContainer)();
  ```
- **Architectural Contradiction**:
  - `isContainer` is computed from the obsolete radio group and passed into RPC `add_node`.
- **Remediation**: Remove `nodeType` query selector and simplify call to `eel.add_node(this.activeParentIdForModal, name)`.

### 🟡 Item 2.2: Obsolete `isContainer: false` in Drag-and-Drop Payloads
- **Location**: [`src/web/js/drag_drop.js`](file:///E:/JE/src/web/js/drag_drop.js#L31) and [`#L71`](file:///E:/JE/src/web/js/drag_drop.js#L71)
- **Code Snippet**:
  ```javascript
  this.activeDragPayload = { isNew: true, label: headerLabel, isContainer: false };
  ```
- **Architectural Contradiction**:
  - All dropped payload items are dynamic `HierarchyNode` instances; static `isContainer` payload flags are ignored.
- **Remediation**: Clean up `isContainer` property from `activeDragPayload`.

---

## Category 3: Dead HTML Elements from Pre-Native File Dialogs

### 🔴 Item 3.1: Orphaned `<input type="file" id="excelFileInput">` Element
- **Location**: [`src/web/index.html`](file:///E:/JE/src/web/index.html#L152) and [`src/web/js/app.js`](file:///E:/JE/src/web/js/app.js#L36)
- **Code Snippet**:
  ```html
  <input type="file" id="excelFileInput" accept=".xlsx" style="display:none">
  ```
  ```javascript
  this.excelFileInput = document.getElementById('excelFileInput');
  ```
- **Architectural Contradiction**:
  - Excel file picking was migrated to native OS file dialogs via `FileDialogService` (`eel.open_file_dialog()`, Feature 003).
  - The hidden file input is never triggered, never listened to, and completely dead.
- **Remediation**: Delete `<input type="file" id="excelFileInput">` from `index.html` and delete `this.excelFileInput` reference from `app.js`.

---

## Category 4: Backend RPC Bridge & Adapter Signatures

### 🟡 Item 4.1: Unused `is_container` Argument in `eel_bridge.add_node`
- **Location**: [`src/app/eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py#L33)
- **Code Snippet**:
  ```python
  @eel.expose
  def add_node(parent_id: Optional[str] = None, name: str = "", is_container: bool = True, target_id: Optional[str] = None, zone: Optional[str] = None) -> Dict[str, Any]:
      new_node = HierarchyNode(name)
  ```
- **Architectural Contradiction**:
  - `is_container` is accepted in the signature with default `True` but is entirely ignored because `HierarchyNode(name)` dynamically calculates `is_container`.
- **Remediation**: Deprecate/default `is_container=True` or clean up parameter signature.

### 🟡 Item 4.2: Legacy Feature 001 Column A Import/Export Methods
- **Location**: [`src/app/eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py#L210-L230) & [`src/hierarchy_lib/adapters/excel_adapter.py`](file:///E:/JE/src/hierarchy_lib/adapters/excel_adapter.py#L120-L190)
- **Code Snippet**:
  - `eel_bridge.import_excel` & `eel_bridge.export_excel`
  - `ExcelHierarchyAdapter.import_from_file` & `ExcelHierarchyAdapter.export_to_file`
- **Status**: Flagged in `.specify/system_map.md` as deprecated in favor of `import_excel_file` and `export_reorganized_row1`.
- **Remediation**: Retain for legacy compatibility until scheduled for decommissioning.

---

## Requirements-Quality Action Items (Checklist)

| ID | Component | Type | Description | Priority |
|---|---|---|---|---|
| **REQ-AUDIT-01** | `src/web/index.html` | Form Cleanup | Remove `<div class="form-group"><label>Node Type</label>...</div>` radio button group from `nodeModal`. | 🔴 High |
| **REQ-AUDIT-02** | `src/web/index.html` | Dead DOM Removal | Remove orphaned `<input type="file" id="excelFileInput">`. | 🔴 High |
| **REQ-AUDIT-03** | `src/web/js/app.js` | JS Refactoring | Remove `input[name="nodeType"]` query selector from `submitAddModal()` and simplify `eel.add_node` invocation. | 🔴 High |
| **REQ-AUDIT-04** | `src/web/js/app.js` | Dead Ref Removal | Remove `this.excelFileInput = document.getElementById('excelFileInput')` from `initElements()`. | 🔴 High |
| **REQ-AUDIT-05** | `src/web/js/drag_drop.js` | Payload Hygiene | Remove unused `isContainer: false` from drag-and-drop payload dictionaries. | 🟡 Medium |
| **REQ-AUDIT-06** | `src/app/eel_bridge.py` | Signature Hygiene | Maintain `is_container: Optional[bool] = None` as optional deprecated kwarg for backward compatibility. | 🟢 Low |
| **REQ-AUDIT-07** | `.specify/system_map.md` | Map Sync | Update system map component inventory to document the simplified single-input modal. | 🟢 Low |
