# Рівень А: Атомарні мікро-цикли елементів (View Modes Micro-Lifecycles)

> **Призначення**: Автомати станів для перемикача режимів перегляду та компонентів рендерингу.

---

## 1. `ViewModeButtonGroupLifecycle` (Життєвий цикл кнопок перемикання режимів)

Застосовується до: `#btnViewTree`, `#btnViewMatrix`, `#btnViewUniqueLevels`.

```mermaid
stateDiagram-v2
    [*] --> TreeActive: Initial State (#btnViewTree.active)
    TreeActive --> MatrixActive: Click #btnViewMatrix -> remove .active from Tree, add .active to Matrix
    MatrixActive --> UniqueLevelsActive: Click #btnViewUniqueLevels -> remove .active from Matrix, add .active to UniqueLevels
    UniqueLevelsActive --> TreeActive: Click #btnViewTree -> remove .active from UniqueLevels, add .active to Tree
```

---

## 2. `MatrixCoordTableLifecycle` (Життєвий цикл таблиці блоків Excel)

Застосовується до: `#excelBlockView`, `.excel-matrix-table`.

```mermaid
stateDiagram-v2
    [*] --> Hidden: class "excel-block-view hidden"
    Hidden --> ActiveRendering: ViewModeManager.switchMode('matrix')
    ActiveRendering --> CoordinatesBuilt: Generate Row 1 Excel Columns (A, B, C, D...)
    CoordinatesBuilt --> CellsSpanned: Group parent nodes with colspan across children
    CellsSpanned --> TypeTagsAttached: Add .matrix-cell-type-tag to leaf elements
    TypeTagsAttached --> VisibleOnScreen: class removed "hidden" -> table visible
```

---

## 3. `UniqueLevelChipGroupLifecycle` (Життєвий цикл пошарових чіпів)

Застосовується до: `#uniqueLevelView`, `.level-row-container`.

```mermaid
stateDiagram-v2
    [*] --> Hidden: class "unique-level-view hidden"
    Hidden --> ActiveExtraction: UniqueLevelExtractor.extractUniqueLevels(roots)
    ActiveExtraction --> PartitioningGroups: Partition leaves first (left) & branches second (right)
    PartitioningGroups --> ChipsRendered: Render .level-header-chip with count badges
    ChipsRendered --> VisibleOnScreen: class removed "hidden" -> wrapper visible
```

---

## 4. `DuplicateSyncHighlightLifecycle` (Життєвий цикл синхронного підсвічування дублікатів)

Застосовується до: `.level-header-chip` з однаковими назвами.

```mermaid
stateDiagram-v2
    [*] --> NormalChip: Regular display with border & badge
    NormalChip --> PointerOver: pointerenter / hover on duplicate chip
    PointerOver --> QueryCrossMatches: Find all chips with same data-term / nodeName
    QueryCrossMatches --> SynchronouslyHighlighted: Add class .highlight-match-sync to all matches
    SynchronouslyHighlighted --> PointerOut: pointerleave / mouseout
    PointerOut --> NormalChip: Remove class .highlight-match-sync from all matches
```
