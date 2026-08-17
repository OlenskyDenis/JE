# Рівень В: Нормативний чек-лист верифікації (Node Modal Verification Checklist)

> **Призначення**: Повна карта перевірки модального вікна створення/редагування вузла з прив'язкою до тестів.

---

## Чек-лист переходів станів та перевірки контрактів

| ID | Сценарій / Фаза діаграми | Вхідний стан (Pre-condition) | Дія користувача (Trigger Action) | Очікуваний стан Frontend (DOM / UI) | Очікуваний стан Backend (RPC / State) | Покриття тестом у проекті | Статус |
|:---:|---|---|---|---|---|---|:---:|
| **CHK-NOD-01** | **Створення кореня з порожнього стану** | Порожнє полотно (`#treeEmptyState.visible`) | Клік на `#btnCreateRootEmpty` | Відкривається `#nodeModal`, поле назви порожнє | Готовність форми, виклики ще не виконувались | `tests/e2e/test_tree_crud_and_modals.py::test_create_root_node_and_modal_validation` | `PASS` |
| **CHK-NOD-02** | **Валідація порожньої назви** | Відкрито `#nodeModal` | Клік `#btnModalSubmit` з порожнім полем | Форма блокує відправку, поле підсвічується / тост помилки | Жодного RPC виклику не відправлено | `tests/e2e/test_tree_crud_and_modals.py::test_create_root_node_and_modal_validation` | `PASS` |
| **CHK-NOD-03** | **Успішне створення кореня** | `#nodeModal` відкрито | Введення `"Root_A"` + Submit | `#nodeModal` закривається, з'являється картка `.tree-node` з текстом `"Root_A"`, лічильник `#nodeCountBadge` = 1 | `eel.add_node()` повертає `{"success": true}`, у `forest.root_nodes` додано вузол | `tests/e2e/test_tree_crud_and_modals.py::test_create_root_node_and_modal_validation` | `PASS` |
| **CHK-NOD-04** | **Додавання дочірнього вузла (Nesting)** | Існує кореневий вузол `"Sales"` | Клік на кнопку `[+]` (`.add-child`) на картці `"Sales"` | Відкривається `#nodeModal` з заголовком "Створити дочірній вузол" | `parent_id` зафіксовано у `ModalManager` | `tests/e2e/test_tree_crud_and_modals.py::test_add_child_nesting_and_folder_chevrons` | `PASS` |
| **CHK-NOD-05** | **Перетворення на папку та шеврон** | Додано нащадок `"Q1"` у `"Sales"` | Підтвердження створення нащадка | Батько `"Sales"` отримує іконку папки `.folder` та кнопку-шеврон `.node-toggle` | `node.is_container = True` у `WorkspaceForest` | `tests/e2e/test_tree_crud_and_modals.py::test_add_child_nesting_and_folder_chevrons` | `PASS` |
| **CHK-NOD-06** | **Редагування назви та типу даних** | Існує листок `"Price"` (тип `Decimal`) | Клік на `.rename-node` | Відкривається `#nodeModal` з передзаповненими полями `"Price"` та `Decimal` | Отримано дані вузла | `tests/e2e/test_tree_crud_and_modals.py::test_edit_node_modal_and_type_update` | `PASS` |
| **CHK-NOD-07** | **Збереження перейменування** | Введено `"Total_Amount"` + тип `Currency` | Клік `#btnModalSubmit` | Картка оновлюється: назва `"Total_Amount"`, бейдж типу `"Валюта"` | `eel.update_node()` повертає успіх, стан вузла оновлено | `tests/e2e/test_tree_crud_and_modals.py::test_edit_node_modal_and_type_update` | `PASS` |
