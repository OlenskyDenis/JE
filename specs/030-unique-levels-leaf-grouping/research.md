# Research & Technical Analysis: Leaf-First Partitioning & Paragraph Separation (Feature 030)

**Feature Branch**: `030-unique-levels-leaf-grouping`  
**Created**: 2026-08-16  
**Status**: Ready  

---

## 1. Domain Analysis & UI Layout Considerations

### Leaf vs Branch Node Definition
In tree and forest data structures:
- A **Leaf Node** has no child elements (`!node.children || node.children.length === 0`). In database schemas and financial templates, leaves represent actual data fields, values, or metrics.
- A **Branch Node** (category / folder node) has one or more child elements (`node.children.length > 0`). These serve purely structural / grouping purposes.

### Deduplication at Depth Level
When collapsing the forest into unique terms for level $L$:
- If an entry has multiple occurrences on level $L$, we check if any occurrence contains child nodes:
  `const isFolder = occurrences.some(node => node.children && node.children.length > 0);`
  `const isLeaf = !isFolder;`
- This ensures that if a term is used structurally anywhere on this level, it is treated as a structural/branch element; otherwise, it is a pure data leaf.

---

## 2. Visual Separation ("Абзац") Options

### Option A: Dual-Section Flow with Paragraph Divider (Recommended)
- **Leaves Sub-Group**:
  - Container `.level-subgroup.level-subgroup-leaves`
  - Subtle sub-header with icon/badge (e.g. `Кінцеві елементи` / `Leaf elements`)
  - Horizontal flex-wrap chip container
- **Paragraph Divider**:
  - Distinctive paragraph break `.level-group-separator` with vertical spacing and a subtle horizontal line.
- **Branches Sub-Group**:
  - Container `.level-subgroup.level-subgroup-branches`
  - Subtle sub-header with icon/badge (e.g. `Категорії (з вкладеностями)` / `Branches / Categories`)
  - Horizontal flex-wrap chip container

**Benefits**:
- Intuitive and frictionless: clean scannability.
- No clutter if only leaves or only branches exist on that tier.
- Preserves all double-click and hover synchronization bindings via event delegation.

---

## 3. Localization Strategy

Add to `src/web/js/i18n.js`:
```javascript
// uk
level_subgroup_leaves: "Кінцеві елементи (без вкладеностей)",
level_subgroup_branches: "Категорії (з вкладеностями)",
level_subgroup_leaves_badge: "{count} без вкладеностей",
level_subgroup_branches_badge: "{count} з вкладеностями",

// en
level_subgroup_leaves: "Terminal elements (no children)",
level_subgroup_branches: "Categories (with children)",
level_subgroup_leaves_badge: "{count} leaf items",
level_subgroup_branches_badge: "{count} with children",
```
