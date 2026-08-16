# State & Lifecycle: Multi-Sheet Sessions & Data Flow

**Path**: `.specify/system_map/state_and_lifecycle.md`  
**Architectural Layer**: State & Session Management  
**Scope**: In-memory session synchronization across Python and JavaScript

---

## 1. Backend Global State Variables (`src/app/eel_bridge.py`)

The backend maintains active session state in global variables:

```python
forest: WorkspaceForest                  # Active workspace forest currently displayed in UI
sheet_forests: Dict[str, WorkspaceForest] # Multi-sheet session map: { "Sheet1": forest1, "Sheet2": forest2 }
current_active_sheet: Optional[str]      # Name of the active sheet
current_file_path: Optional[str]         # Absolute path to the loaded source Excel file
current_template_path: Optional[str]     # Absolute path to the bound exported template file
```

### Backend State Transitions:
1. **File Import (`import_excel_file`)**:
   * Reads all sheets from disk.
   * Parses Row 1 headers into separate `WorkspaceForest` instances in `sheet_forests`.
   * Sets `current_active_sheet = sheets[0]`, `forest = sheet_forests[sheets[0]]`, `current_template_path = None`.
2. **Sheet Switch (`switch_active_sheet`)**:
   * Preserves current modifications in `sheet_forests[current_active_sheet]`.
   * Switches `forest` pointer to target `sheet_forests[target_sheet]`.
   * Returns restored tree roots and headers.
3. **Session Refresh (`refresh_excel_session`)**:
   * Re-reads disk file, retains `current_active_sheet` selection if still present in workbook.
4. **Template Export (`save_template_sync`)**:
   * Simultaneously exports all modified trees from `sheet_forests` into target workbook.
   * Binds `current_template_path = target_path`.

---

## 2. Frontend Session State (`src/web/js/app.js`)

The frontend manages browser-side session state and user interactions:

| State Variable | Type | Purpose | Persistence |
|---|---|---|---|
| `App.isDirty` | `boolean` | Flags unsaved tree modifications since last file load or template save. | Runtime in-memory |
| `App.currentSheetName` | `string` | Currently selected sheet name in UI. | Runtime in-memory |
| `App.currentFilePath` | `string` | Active loaded source file path. | Runtime in-memory |
| `App.currentTemplatePath` | `string` | Bound template path shown in `#templateStatusBadge`. | Runtime in-memory |
| `App.collapsedNodeIds` | `Set<string>` | IDs of collapsed folder nodes in tree view. | Runtime in-memory |
| `App.activeViewMode` | `'tree' \| 'matrix' \| 'unique'` | Active workspace view mode. | `localStorage.getItem('je_workspace_view_mode')` |
| `I18n.currentLanguage` | `'uk' \| 'en'` | Active user language. | `localStorage.getItem('app_language')` |
| `App.pendingAction` | `Function \| null` | Deferred action intercepted by `#unsavedModal`. | Runtime in-memory |
