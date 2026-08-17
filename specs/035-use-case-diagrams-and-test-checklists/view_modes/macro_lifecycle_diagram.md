# Рівень Б: Наскрізна Sequence-діаграма режимів перегляду (View Modes Full-Stack Sequence)

> **Призначення**: Повний цикл перемикання між Деревом, Блоками Excel та Унікальними рівнями із синхронізацією підсвічування.

---

```mermaid
sequenceDiagram
    autonumber
    actor User as 👤 Користувач
    participant ViewBtns as 🎛️ #viewModeSwitcher
    participant ViewMgr as 🧭 ViewModeManager
    participant TreeRend as 🌳 TreeRenderer
    participant MatrixRend as 📊 ExcelBlockRenderer
    participant UniqueRend as 🏷️ UniqueLevelRenderer
    participant Extractor as 🔍 UniqueLevelExtractor
    participant DOM as 🖥️ Workspace Canvas

    %% 1. Перемикання на Блоки Excel (Matrix)
    Note over User, DOM: ФАЗА 1: Перемикання на режим «Блоки Excel» (Matrix View)
    User ->> ViewBtns: Клік на #btnViewMatrix
    ViewBtns ->> ViewMgr: switchMode('matrix')
    ViewMgr ->> DOM: Приховування #treeView та #uniqueLevelView (.hidden)
    ViewMgr ->> DOM: Відображення #excelBlockView (зняття .hidden)
    ViewMgr ->> MatrixRend: renderExcelBlockView(roots)
    MatrixRend ->> MatrixRend: Побудова координат колонок (A, B, C, D...)
    MatrixRend ->> MatrixRend: Обчислення colspan для батьківських папок
    MatrixRend ->> DOM: Рендеринг .excel-matrix-table
    DOM -->> User: Таблиця блоків Excel відображається на екрані

    %% 2. Перемикання на Унікальні за рівнями
    Note over User, DOM: ФАЗА 2: Перемикання на режим «Унікальні за рівнями» (Unique Levels)
    User ->> ViewBtns: Клік на #btnViewUniqueLevels
    ViewBtns ->> ViewMgr: switchMode('unique_levels')
    ViewMgr ->> DOM: Приховування #treeView та #excelBlockView (.hidden)
    ViewMgr ->> DOM: Відображення #uniqueLevelView (зняття .hidden)
    ViewMgr ->> Extractor: extractUniqueLevels(roots)
    Extractor ->> Extractor: Групування по рівнях: листки (ліворуч) + гілки (праворуч)
    Extractor -->> UniqueRend: Structured levels data
    UniqueRend ->> DOM: Рендеринг .unique-levels-wrapper та чіпів
    DOM -->> User: Пошарові чіпи відображаються з лічильниками повторів

    %% 3. Наведення на дублікат (Синхронне підсвічування)
    Note over User, DOM: ФАЗА 3: Наведення курсору на дублікат (Duplicate Matching Sync)
    User ->> DOM: Наведення курсору на чіп "Common" на Рівні 1
    DOM ->> UniqueRend: pointerenter event
    UniqueRend ->> DOM: Пошук усіх .level-header-chip[data-term="common"]
    UniqueRend ->> DOM: Додавання класу .highlight-match-sync до всіх збігів (Рівень 1 і 2)
    DOM -->> User: Усі однакові чіпи підсвічуються синхронно яскравим кольором
    User ->> DOM: Відведення курсору (pointerleave)
    UniqueRend ->> DOM: Зняття класу .highlight-match-sync

    %% 4. Повернення до Дерева
    Note over User, DOM: ФАЗА 4: Повернення до класичного «Дерева»
    User ->> ViewBtns: Клік на #btnViewTree
    ViewBtns ->> ViewMgr: switchMode('tree')
    ViewMgr ->> DOM: Приховування #excelBlockView та #uniqueLevelView (.hidden)
    ViewMgr ->> DOM: Відображення #treeView (зняття .hidden)
    ViewMgr ->> TreeRend: renderTree(roots)
    DOM -->> User: Класичне інтерактивне дерево знову активне
```
