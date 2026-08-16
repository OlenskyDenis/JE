# Data Model: Excel Block Hierarchy View (Multi-Level Header Matrix Mode)

**Feature Branch**: `027-excel-block-hierarchy-view`  
**Created**: 2026-08-16  
**Status**: Completed  

---

## 1. Frontend Matrix Data Structures

### 1.1 Matrix Cell Definition (`MatrixCellDTO`)
Represents an individual header block within a specific tier row of the Excel Block Matrix.

```typescript
interface MatrixCellDTO {
    /** Associated domain HierarchyNode */
    node: HierarchyNodeDTO;
    
    /** Number of column units this block spans horizontally */
    colSpan: number;
    
    /** Number of tier rows this block spans vertically */
    rowSpan: number;
    
    /** True if this node has no children (terminal leaf element) */
    isLeaf: boolean;
    
    /** Zero-indexed vertical hierarchy tier level (0 = root) */
    level: number;
    
    /** Formatted tooltip string for hover inspection */
    tooltip: string;
}
```

### 1.2 Matrix Forest Layout Meta (`MatrixLayoutMeta`)
Container representing the complete multi-tier block grid for an active sheet.

```typescript
interface MatrixLayoutMeta {
    /** Maximum tree depth across all roots in the forest (1-indexed) */
    maxDepth: number;
    
    /** Total leaf column width across all roots */
    totalColumns: number;
    
    /** Generated Excel column coordinates (e.g. ['A', 'B', 'C', ..., 'Z', 'AA', ...]) */
    columnLabels: string[];
    
    /** Tier rows: array of length maxDepth containing lists of MatrixCellDTO */
    tierRows: MatrixCellDTO[][];
}
```

### 1.3 View Mode State (`WorkspaceViewMode`)
```typescript
type WorkspaceViewMode = 'tree' | 'matrix';

interface WorkspaceViewState {
    /** Active view mode */
    currentMode: WorkspaceViewMode;
    
    /** LocalStorage key for user preference persistence */
    storageKey: 'je_workspace_view_mode';
}
```

---

## 2. Localization Dictionary Schema Additions

The following keys are added to both `uk` and `en` dictionaries in `src/web/js/i18n.js`:

| Key | Ukrainian Translation (`uk`) | English Translation (`en`) | Purpose |
|---|---|---|---|
| `view_mode_tree` | `Дерево` | `Tree View` | Segmented button label for Tree view |
| `view_mode_matrix` | `Блоки Excel` | `Excel Blocks` | Segmented button label for Excel Block view |
| `tooltip_view_mode_tree` | `Перемкнути на деревоподібний вигляд` | `Switch to hierarchical tree view` | Tooltip for Tree toggle |
| `tooltip_view_mode_matrix` | `Перемкнути на вигляд блоків Excel` | `Switch to Excel multi-level blocks view` | Tooltip for Matrix toggle |
| `matrix_col_prefix` | `Колонка` | `Column` | Tooltip prefix for column coordinates |
| `matrix_depth_label` | `Глибина рівнів` | `Level Depth` | Tooltip stat |
| `matrix_colspan_label` | `Ширина (колонок)` | `Width (Columns)` | Tooltip stat |
| `matrix_empty_title` | `Немає даних для таблиці блоків` | `No data for block matrix` | Empty state title |
| `matrix_empty_hint` | `Імпортуйте файл Excel або створіть вузли в дереві.` | `Import an Excel file or create nodes in the tree.` | Empty state subtitle |
