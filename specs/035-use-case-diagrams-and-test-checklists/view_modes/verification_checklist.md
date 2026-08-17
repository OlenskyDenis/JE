# Рівень В: Нормативний чек-лист верифікації (View Modes Verification Checklist)

> **Призначення**: Повна карта перевірки перемикання 3 режимів перегляду, таблиць координат та підсвічування дублікатів з прив'язкою до тестів.

---

## Чек-лист переходів станів та перевірки контрактів

| ID | Сценарій / Фаза діаграми | Вхідний стан (Pre-condition) | Дія користувача (Trigger Action) | Очікуваний стан Frontend (DOM / UI) | Очікуваний стан Backend (RPC / State) | Покриття тестом у проекті | Статус |
|:---:|---|---|---|---|---|---|:---:|
| **CHK-VIEW-01** | **Перемикання на Блоки Excel** | Активне Дерево (`#treeView.visible`) | Клік на `#btnViewMatrix` | `#btnViewMatrix.active`, `#treeView.hidden`, `#excelBlockView` видиме (`to_be_visible()`) | Дерево не мутує, генерується матриця | `tests/e2e/test_view_modes_and_renderers.py::test_view_mode_switching_between_tree_matrix_and_unique_levels` | `PASS` |
| **CHK-VIEW-02** | **Координати колонок та об'єднання осередків** | Режим Блоків Excel | Рендеринг структури | Наявні заголовки координат $A, B\dots$, батьки мають атрибут `colspan` по кількості дітей | Відповідає структурі `openpyxl` | `tests/e2e/test_view_modes_and_renderers.py::test_excel_block_matrix_rendering_and_coordinates` | `PASS` |
| **CHK-VIEW-03** | **Перемикання на Унікальні за рівнями** | Будь-який режим | Клік на `#btnViewUniqueLevels` | `#btnViewUniqueLevels.active`, `#uniqueLevelView` видиме (`to_be_visible()`), наявні рядки рівнів `.level-row-container` | `UniqueLevelExtractor` виділив унікальні вузли | `tests/e2e/test_view_modes_and_renderers.py::test_view_mode_switching_between_tree_matrix_and_unique_levels` | `PASS` |
| **CHK-VIEW-04** | **Розділення на листки та гілки (Leaf-first)** | Режим Унікальних за рівнями | Рендеринг рівня з листками і гілками | Зліва група листків `.level-group-leaves`, справа група гілок `.level-group-branches`, між ними розділювач | Листки виділені за відсутністю `children` | `tests/e2e/test_view_modes_and_renderers.py::test_unique_level_view_leaf_and_branch_partitioning` | `PASS` |
| **CHK-VIEW-05** | **Синхронне підсвічування дублікатів (Hover Match)** | Унікальні рівні з дублями | Наведення на чіп з повторюваною назвою | Усі чіпи з такою назвою на всіх рівнях одночасно отримують клас `.highlight-match-sync` | DOM event-driven синхронізація | `tests/e2e/test_view_modes_and_renderers.py::test_unique_level_duplicate_highlight_sync` | `PASS` |
| **CHK-VIEW-06** | **Повернення до класичного Дерева** | Режим Блоків або Унікальних | Клік на `#btnViewTree` | `#btnViewTree.active`, `#excelBlockView.hidden`, `#uniqueLevelView.hidden`, `#treeView` видиме | Інтерактивне полотно відновлено | `tests/e2e/test_view_modes_and_renderers.py::test_view_mode_switching_between_tree_matrix_and_unique_levels` | `PASS` |
| **CHK-VIEW-07** | **Автоматична валідація переходів у матриці** | Довільний стан | Виклик `flow_switch_to_matrix_view` та `flow_switch_to_unique_levels_view` | Перевірка відсутності взаємних накладень та коректності класів | `MatrixFlowExecutor` | `tests/e2e/test_automated_interaction_matrix.py::test_full_state_transition_chain` | `PASS` |
