# Data Model: Unique Level Hierarchy View (Feature 028)

**Feature Branch**: `028-unique-level-hierarchy-view`  
**Created**: 2026-08-16  
**Status**: Completed  

---

## 1. Frontend Data Structures

### 1.1 Unique Level Header Item (`UniqueLevelItemDTO`)
Represents an individual deduplicated header term at a specific depth level.

```typescript
interface UniqueLevelItemDTO {
    /** Display name of the header */
    name: string;
    
    /** Lowercase normalized key for case-insensitive matching */
    normalized: string;
    
    /** Number of times this header occurs on this specific level */
    count: number;
    
    /** Array of all absolute paths for occurrences of this header */
    paths: string[];
    
    /** Assigned data types for occurrences of this header */
    dataTypes: string[];
    
    /** Sorted array of 0-based depth level indexes where this name appears */
    matchingLevels: number[];
    
    /** True if matchingLevels.length > 1 (exists on other levels) */
    isCrossLevelMatch: boolean;
    
    /** Formatted tooltip detailing counts, levels, and paths */
    tooltip: string;
}
```

### 1.2 Unique Level Row Meta (`UniqueLevelRowMeta`)
Represents a single depth level row containing all deduplicated items for that level.

```typescript
interface UniqueLevelRowMeta {
    /** Zero-based depth level (0 = Roots) */
    level: number;
    
    /** Localized title (e.g. "Рівень 0 (Корені)" or "Рівень 1") */
    title: string;
    
    /** Total unique header items on this level */
    uniqueCount: number;
    
    /** Count of items on this level that have cross-level duplicates */
    crossMatchCount: number;
    
    /** List of deduplicated header items */
    items: UniqueLevelItemDTO[];
}
```

---

## 2. Localization Dictionary Schema Additions

The following keys are added to both `uk` and `en` dictionaries in `src/web/js/i18n.js`:

| Key | Ukrainian Translation (`uk`) | English Translation (`en`) | Purpose |
|---|---|---|---|
| `view_mode_unique_levels` | `Унікальні за рівнями` | `Unique by Levels` | Segmented switcher button label |
| `tooltip_view_mode_unique_levels` | `Перемкнути на пошаровий перегляд унікальних заголовків` | `Switch to level-by-level unique headers view` | View switcher button tooltip |
| `level_roots_title` | `Рівень 0 (Корені)` | `Level 0 (Roots)` | Title for Tier 0 |
| `level_tier_title` | `Рівень {level}` | `Level {level}` | Title for Tier 1..N |
| `level_unique_stat` | `{count} унікальних` | `{count} unique` | Level unique items counter |
| `level_match_stat` | `{count} міжрівневих збігів` | `{count} cross-level matches` | Level cross-match counter |
| `chip_match_badge` | `Збіг: Рівні {levels}` | `Match: Levels {levels}` | Cross-level match chip tag |
| `unique_levels_empty_title` | `Немає даних для аналізу рівнів` | `No data for level analysis` | Empty state title |
| `unique_levels_empty_hint` | `Імпортуйте файл Excel або створіть вузли в дереві.` | `Import an Excel file or create nodes in the tree.` | Empty state hint |
