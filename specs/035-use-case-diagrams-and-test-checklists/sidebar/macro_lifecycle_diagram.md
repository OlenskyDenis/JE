# Рівень Б: Наскрізна Sequence-діаграма сайдбару (Sidebar Full-Stack Sequence)

> **Призначення**: Повний цикл роботи бічної панелі: перемикання вкладок, пошук, ресайз, згортання та зміна аркуша каталогу.

---

```mermaid
sequenceDiagram
    autonumber
    actor User as 👤 Користувач
    participant Controls as 🎛️ Sidebar Controls (Search / Tabs / Resizer)
    participant SideCtrl as 📑 SidebarController
    participant SessCtrl as 🗄️ SessionController
    participant DOM as 🖥️ Sidebar DOM
    participant DragDrop as 🎯 DragDropHandler

    %% 1. Пошук та фільтрація
    Note over User, DOM: ФАЗА 1: Живий пошук у каталозі колонок
    User ->> Controls: Введення "Price" у #sidebarSearch
    Controls ->> SideCtrl: filterAndRenderSidebar()
    SideCtrl ->> SessCtrl: Отримання currentRawHeaders для активного каталогу
    SideCtrl ->> SideCtrl: Фільтрація заголовків за підрядком "Price"
    SideCtrl ->> DOM: Рендеринг карток .sidebar-header-item
    SideCtrl ->> DOM: Оновлення #headerCountBadge (кількість знайдених)
    DOM -->> User: Відфільтровані картки готові до перетягування

    %% 2. Перетягування картки в дерево
    Note over User, DOM: ФАЗА 2: Перетягування колонки з каталогу (Drag-and-Drop)
    User ->> DOM: Dragstart на картці "Price" (.sidebar-header-item)
    DOM ->> SideCtrl: dragstart event
    SideCtrl ->> DragDrop: activeDragPayload = { isNew: true, label: "Price", dataType: "Currency" }
    User ->> DOM: Drop на вузол дерева у зону NEST_CHILD
    DragDrop ->> SessCtrl: handleDropPayload() -> RPC додавання нового вузла

    %% 3. Зміна аркуша каталогу (Cross-Sheet Catalog)
    Note over User, DOM: ФАЗА 3: Вибір іншого аркуша каталогу (без зміни дерева)
    User ->> Controls: Вибір "Warehouse_Central" у #catalogSheetSelector
    Controls ->> SessCtrl: handleCatalogSheetChange("Warehouse_Central")
    SessCtrl ->> SessCtrl: currentRawHeaders = cachedAllHeaders["Warehouse_Central"]
    SessCtrl ->> SideCtrl: filterAndRenderSidebar()
    SideCtrl ->> DOM: Оновлення списку карток на колонки складу
    Note over User, DOM: Дерево залишається на Store_East, каталог показує Warehouse_Central

    %% 4. Зміна ширини (Resizer) та згортання
    Note over User, DOM: ФАЗА 4: Зміна ширини (Drag Resizer) та згортання у смужку
    User ->> Controls: PointerDown на #sidebarResizer та перетягування
    Controls ->> SideCtrl: pointermove -> зміна style.width (наприклад, 420px)
    User ->> Controls: PointerUp -> збереження 420 у localStorage
    User ->> Controls: Клік на #btnToggleSidebarCollapse
    SideCtrl ->> DOM: Додавання .sidebar-collapsed, відображення #sidebarCollapsedStrip
    User ->> DOM: Клік на смужку #sidebarCollapsedStrip
    SideCtrl ->> DOM: Зняття .sidebar-collapsed (відновлення ширини 420px)
```
