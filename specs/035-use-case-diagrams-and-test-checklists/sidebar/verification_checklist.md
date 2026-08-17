# Рівень В: Нормативний чек-лист верифікації (Sidebar Verification Checklist)

> **Призначення**: Повна карта перевірки вкладок, пошуку, згортання та зміни розміру сайдбару з прив'язкою до тестів.

---

## Чек-лист переходів станів та перевірки контрактів

| ID | Сценарій / Фаза діаграми | Вхідний стан (Pre-condition) | Дія користувача (Trigger Action) | Очікуваний стан Frontend (DOM / UI) | Очікуваний стан Backend (RPC / State) | Покриття тестом у проекті | Статус |
|:---:|---|---|---|---|---|---|:---:|
| **CHK-SIDE-01** | **Перемикання на вкладку Шляхів** | Вкладка «Каталог» активна | Вибір `"paths"` у `#sidebarTabSelector` | `#tabContentCatalog.hidden`, `#tabContentPaths` видиме, `#pathCountBadge` показує кількість шляхів | Синхронізація з `forest.get_all_leaf_paths()` | `tests/e2e/test_sidebar_tabs_and_resizer.py::test_sidebar_tab_switching_catalog_and_paths` | `PASS` |
| **CHK-SIDE-02** | **Фільтрація пошуком у каталозі** | Завантажено заголовки | Введення `"Price"` у `#sidebarSearch` | Відображаються лише картки, що містять `"Price"`, лічильник `#headerCountBadge` зменшується | Фільтрація на рівні клієнта | `tests/e2e/test_sidebar_tabs_and_resizer.py::test_sidebar_search_filter_and_empty_state` | `PASS` |
| **CHK-SIDE-03** | **Пошук без збігів (Empty State)** | Будь-який каталог | Введення `"XYZ_UNKNOWN_QUERY"` | `#sidebarHeaderList.hidden`, відображається `#sidebarEmptyState` ("Нічого не знайдено") | Без помилок | `tests/e2e/test_sidebar_tabs_and_resizer.py::test_sidebar_search_filter_and_empty_state` | `PASS` |
| **CHK-SIDE-04** | **Згортання сайдбару у смужку** | Сайдбар розгорнутий | Клік на `#btnToggleSidebarCollapse` | `#unifiedSidebar` отримує `.sidebar-collapsed`, `#sidebarCollapsedStrip` стає видимим | Стан збережено у `localStorage` | `tests/e2e/test_sidebar_tabs_and_resizer.py::test_sidebar_collapse_and_expand_strip` | `PASS` |
| **CHK-SIDE-05** | **Розгортання зі смужки** | Сайдбар згорнутий | Клік на `#btnExpandSidebarStrip` | Клас `.sidebar-collapsed` видалено, повний сайдбар видимий | Відновлення попередньої ширини | `tests/e2e/test_sidebar_tabs_and_resizer.py::test_sidebar_collapse_and_expand_strip` | `PASS` |
| **CHK-SIDE-06** | **Ресайзер ширини (Drag)** | Сайдбар відкритий | Drag спліттера `#sidebarResizer` | Ширина `#unifiedSidebar` динамічно змінюється (обмежена [220px, 600px]) | Запис ширини у `localStorage` | `tests/e2e/test_sidebar_tabs_and_resizer.py::test_sidebar_resizer_drag_and_double_click_reset` | `PASS` |
| **CHK-SIDE-07** | **Скидання ширини (Double-Click)** | Змінена ширина (наприклад, 450px) | Double-click на `#sidebarResizer` | Ширина миттєво стає `340px` | `localStorage.getItem('je_sidebar_width') == '340'` | `tests/e2e/test_sidebar_tabs_and_resizer.py::test_sidebar_resizer_drag_and_double_click_reset` | `PASS` |
| **CHK-SIDE-08** | **Зміна листа каталогу** | Багатолистова книга | Вибір іншого листа у `#catalogSheetSelector` | Оновлюються заголовки в сайдбарі, дерево залишається незмінним | `SessionController.catalogSheetName` оновлено | `tests/e2e/test_automated_interaction_matrix.py::test_declarative_interaction_flow_isolated[flow_switch_catalog_sheet_independent]` | `PASS` |
