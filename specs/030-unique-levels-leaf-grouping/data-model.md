# Data Model: Leaf-First Partitioning & Paragraph Separation (Feature 030)

**Feature Branch**: `030-unique-levels-leaf-grouping`  
**Created**: 2026-08-16  
**Status**: Draft  

---

## 1. Frontend Data Structures

### 1.1 Unique Level Header Item (`UniqueLevelItemDTO`)
Represents an individual deduplicated header term at a specific depth level.

```typescript
interface UniqueLevelItemDTO {
    /** Primary node ID (for DOM reference and editing) */
    nodeId: string;
    
    /** All node IDs with this name on this level */
    nodeIds: string[];
    
    /** Display name of the header */
    name: string;
    
    /** Lowercase normalized key for case-insensitive matching */
    normalized: string;
    
    /** Primary data type (e.g., 'Text', 'Numeric', 'Date') */
    dataType: string;
    
    /** True if any occurrence of this term has child nodes */
    isFolder: boolean;
    
    /** True if no occurrence of this term has child nodes (leaf element) */
    isLeaf: boolean;
    
    /** Number of times this header occurs on this specific level */
    count: number;
    
    /** Array of all absolute paths for occurrences of this header */
    paths: string[];
    
    /** All unique data types assigned to occurrences of this header */
    dataTypes: string[];
    
    /** Sorted array of depth level indexes where this name appears */
    matchingLevels: number[];
    
    /** True if matchingLevels.length > 1 (exists on multiple levels) */
    isCrossMatch: boolean;
    
    /** Formatted tooltip detailing counts, types, paths, and edit instructions */
    tooltip: string;
}
```

### 1.2 Unique Level Row Meta (`UniqueLevelRowMeta`)
Represents a single depth level row containing partitioned unique items.

```typescript
interface UniqueLevelRowMeta {
    /** Zero-based depth level (0 = Roots) */
    level: number;
    
    /** Localized title (e.g. "Рівень 0 (Корені)" or "Рівень 1") */
    title: string;
    
    /** Total unique header items on this level */
    uniqueCount: number;
    
    /** Number of unique leaf items (without children) */
    leafCount: number;
    
    /** Number of unique branch items (with children) */
    branchCount: number;
    
    /** Count of items on this level that have cross-level duplicates */
    crossMatchCount: number;
    
    /** Sorted list of leaf items (without nested children) */
    leafItems: UniqueLevelItemDTO[];
    
    /** Sorted list of branch items (with nested children) */
    branchItems: UniqueLevelItemDTO[];
    
    /** Complete list of items on this level */
    items: UniqueLevelItemDTO[];
}
```

---

## 2. Localization Dictionary Schema Additions

The following keys will be registered in both `uk` and `en` dictionaries in `src/web/js/i18n.js`:

| Key | Ukrainian Translation (`uk`) | English Translation (`en`) | Purpose |
|---|---|---|---|
| `level_subgroup_leaves` | `Кінцеві елементи (без вкладеностей)` | `Terminal elements (no children)` | Header/label for leaf group |
| `level_subgroup_branches` | `Категорії (з вкладеностями)` | `Categories (with children)` | Header/label for branch group |
| `level_subgroup_leaves_badge` | `Кінцеві: {count}` | `Leaves: {count}` | Badge summary for leaves |
| `level_subgroup_branches_badge` | `Категорії: {count}` | `Branches: {count}` | Badge summary for categories |
| `chip_leaf_tag` | `Кінцевий` | `Leaf` | Tooltip or badge tag for leaf items |
| `chip_branch_tag` | `Категорія` | `Category` | Tooltip or badge tag for branch items |
