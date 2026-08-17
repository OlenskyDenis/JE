# Рівень А: Атомарні мікро-цикли елементів (Sidebar Micro-Lifecycles)

> **Призначення**: Автомати станів для вкладок, пошуку, смужки згортання, ресайзера та вибору листа каталогу.

---

## 1. `TabSelectorLifecycle` (Життєвий цикл селектора вкладок)

Застосовується до: `#sidebarTabSelector`, `#tabContentCatalog`, `#tabContentPaths`.

```mermaid
stateDiagram-v2
    [*] --> CatalogTabActive: Default ("catalog")
    CatalogTabActive --> SwitchingToPaths: Select option "paths"
    SwitchingToPaths --> PathsTabActive: #tabContentCatalog.hidden, #tabContentPaths visible, #pathCountBadge visible
    PathsTabActive --> SwitchingToCatalog: Select option "catalog"
    SwitchingToCatalog --> CatalogTabActive: #tabContentPaths.hidden, #tabContentCatalog visible, #headerCountBadge visible
```

---

## 2. `SearchFilterLifecycle` (Життєвий цикл живого пошуку)

Застосовується до: `#sidebarSearch`, `#sidebarHeaderList`, `#sidebarEmptyState`.

```mermaid
stateDiagram-v2
    [*] --> IdleEmptySearch: Search value = "" -> all headers rendered in list
    IdleEmptySearch --> TypingQuery: User inputs query string (e.g. "Price")
    TypingQuery --> Filtering: Compare headers substring (case-insensitive)
    Filtering --> MatchingItems: If filtered.length > 0 -> render .sidebar-header-item, #sidebarEmptyState.hidden
    Filtering --> ZeroMatches: If filtered.length === 0 -> #sidebarHeaderList.hidden, #sidebarEmptyState visible
    ZeroMatches --> TypingQuery: Backspace / clear input
    MatchingItems --> IdleEmptySearch: Search input cleared
```

---

## 3. `CollapseStripLifecycle` (Життєвий цикл згортання у смужку)

Застосовується до: `#btnToggleSidebarCollapse`, `#sidebarCollapsedStrip`, `#btnExpandSidebarStrip`.

```mermaid
stateDiagram-v2
    [*] --> Expanded: Full sidebar visible (width 340px)
    Expanded --> Collapsing: Click #btnToggleSidebarCollapse
    Collapsing --> CollapsedStrip: #unifiedSidebar gets class .sidebar-collapsed, #sidebarCollapsedStrip visible
    CollapsedStrip --> ExpandingViaBtn: Click #btnExpandSidebarStrip
    CollapsedStrip --> ExpandingViaStripBody: Click #sidebarCollapsedStrip body
    ExpandingViaBtn --> Expanded: Remove .sidebar-collapsed class
    ExpandingViaStripBody --> Expanded: Remove .sidebar-collapsed class
```

---

## 4. `ResizerSplitterLifecycle` (Життєвий цикл ресайзера ширини)

Застосовується до: `#sidebarResizer`.

```mermaid
stateDiagram-v2
    [*] --> DefaultWidth: Width 340px (or from localStorage)
    DefaultWidth --> DragStarting: pointerdown on #sidebarResizer
    DragStarting --> Dragging: pointermove -> clamp width between 220px and 600px
    Dragging --> DragEnded: pointerup -> save width to localStorage
    DefaultWidth --> Resetting: dblclick on #sidebarResizer -> reset width to 340px
    Resetting --> DefaultWidth: localStorage set to '340'
```
