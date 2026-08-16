# Аналіз невикористовуваного коду — проект JE

## Python Backend

### 🔴 Повністю невикористовувані

| Елемент | Файл | Причина |
|---|---|---|
| `HierarchyComponent` (клас) | [`base.py`](file:///e:/JE/src/hierarchy_lib/models/base.py) | Абстрактний базовий клас GoF Composite Pattern — повністю замінений `HierarchyNode`. Ніхто його не успадковує. Єдиний споживач — `PathGenerator`, але й він передає `HierarchyComponent` лише у type-hint, а реально передаються `HierarchyNode`. |
| `PathGenerator` (клас) | [`path_generator.py`](file:///e:/JE/src/hierarchy_lib/services/path_generator.py) | Ніде не імпортується у production-коді (`eel_bridge.py`, адаптери, сервіси). Використовується тільки у тестах `test_path_generator.py` та `test_excel_adapter.py`. Функціонал дублює `WorkspaceForest.get_all_leaf_paths()` та `HierarchyNode.get_absolute_path()`. |
| `from collections import Counter` | [`excel_adapter.py`](file:///e:/JE/src/hierarchy_lib/adapters/excel_adapter.py#L5) | Імпортований, але `Counter(...)` ніде не викликається у файлі. Мертвий імпорт. |
| `export_horizontal_row1_leaf_paths()` | [`excel_adapter.py`](file:///e:/JE/src/hierarchy_lib/adapters/excel_adapter.py#L245) | Позначений як "Backwards-compatible wrapper". Викликається лише у тесті `test_excel_adapter.py`. Жоден production-код (`eel_bridge.py`) його не використовує — `save_template_sync()` викликає `export_multi_sheet_template()` напряму. |
| `infer_column_types()` | [`excel_adapter.py`](file:///e:/JE/src/hierarchy_lib/adapters/excel_adapter.py#L141) | Простий wrapper над `read_row1_headers_and_types()`. Ніде не викликається у production-коді. Лише один тест `test_infer_column_types_from_excel_cells` у `test_excel_adapter.py`. |
| `get_sheet_headers()` | [`eel_bridge.py`](file:///e:/JE/src/app/eel_bridge.py#L413) | `@eel.expose` endpoint. Ніде не викликається у `app.js` (підтверджено пошуком). Тільки в одному інтеграційному тесті. |
| `import_excel()` | [`eel_bridge.py`](file:///e:/JE/src/app/eel_bridge.py#L224) | Старий `@eel.expose` endpoint для Feature 001. Замінений повнішою `import_excel_file()`. Не викликається у `app.js`. Лише в одному інтеграційному тесті. |
| `export_excel()` | [`eel_bridge.py`](file:///e:/JE/src/app/eel_bridge.py#L244) | Старий `@eel.expose` endpoint. Не викликається у `app.js` (підтверджено пошуком). Лише в інтеграційному тесті. |
| `update_node_type()` | [`eel_bridge.py`](file:///e:/JE/src/app/eel_bridge.py#L177) | `@eel.expose` endpoint. `app.js` завжди використовує загальніший `update_node()`, який оновлює і ім'я і тип одночасно. `update_node_type` лише в тесті. |

---

### 🟡 Частково або умовно невикористовувані

| Елемент | Файл | Причина |
|---|---|---|
| `LeafNode` (alias) | [`leaf.py`](file:///e:/JE/src/hierarchy_lib/models/leaf.py) | Просто `= HierarchyNode`. Імпортується у `eel_bridge.py` (рядок 12) і `excel_adapter.py` (рядок 8), але обидва файли завжди створюють `HierarchyNode(...)` напряму. Сам alias `LeafNode(...)` викликається тільки в `import_from_file()` — який сам фактично застарів. |
| `CompositeNode` (alias) | [`composite.py`](file:///e:/JE/src/hierarchy_lib/models/composite.py) | Аналогічно. `= HierarchyNode`. Використовується в `delete_node()` для `isinstance()` перевірки та в `import_from_file()`. Перевірка `isinstance(node.parent, CompositeNode)` надлишкова — будь-який вузол може бути і папкою і листом. |
| `get_workspace_tree()` | [`eel_bridge.py`](file:///e:/JE/src/app/eel_bridge.py#L71) | `@eel.expose` endpoint. Не знайдено викликів у `app.js` (пошук не дав результатів). `app.js` отримує `roots` як частину відповідей від інших RPC-функцій, а не через окремий виклик цього endpoint. |
| `export_reorganized_row1()` | [`eel_bridge.py`](file:///e:/JE/src/app/eel_bridge.py#L514) | Викликається у `app.js` (рядок 1044), але є дублюванням: функція всередині просто делегує у `save_template_sync()`, ігноруючи вхідні `sheet_name` і `leaf_paths` параметри. |
| `HeaderService.filter_headers()` | [`header_service.py`](file:///e:/JE/src/hierarchy_lib/services/header_service.py#L31) | Не викликається у production-коді. Пошук у sidebar-фільтрації в `app.js` реалізований через нативний JS-фільтр на клієнті, без виклику цієї серверної функції. |
| `is_container` property | [`node.py`](file:///e:/JE/src/hierarchy_lib/models/node.py#L47) | Позначений як "Backwards-compatible alias for `is_folder`". Дублює `is_folder`. Обидва поля включені у `to_dict()`. JS-код в `app.js` і рендерери не використовують `is_container` з payload; `tree_renderer.js` читає `node.children.length`. |

---

## JavaScript Frontend

| Елемент | Файл | Причина |
|---|---|---|
| `getTypeBadgeLabel()` | [`i18n.js`](file:///e:/JE/src/web/js/i18n.js#L408) | Метод `I18n.getTypeBadgeLabel()` — повний дублікат `getTypeLabel()`. Жоден JS-файл не викликає `getTypeBadgeLabel()`, всі рендерери використовують `I18n.getTypeLabel()`. |
| `window.I18N_DICTIONARIES` | [`i18n.js`](file:///e:/JE/src/web/js/i18n.js#L470) | Експортується в глобальну область, але не використовується жодним іншим JS-файлом. Словники вже доступні через `I18n.t()`. |

---

## Підсумок за категоріями

| Категорія | Кількість |
|---|---|
| 🔴 Повністю невикористовувані | 9 |
| 🟡 Умовно зайві / дублікати | 7 |
| **Всього** | **16** |
