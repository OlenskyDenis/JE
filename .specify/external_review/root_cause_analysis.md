# Аналіз причин виникнення мертвого коду — крізь призму правил і специфікацій

## Де шукати відповідь

Всі 16 знайдених елементів мають структурні причини, які **прямо зафіксовані** в:
- `constitution.md` (Принципи I–VII)
- `system_map.md` (Секції 2.2–3)
- `system_map_audit.md` (Categories 1–4)
- Специфікаціях Features 001, 008, 020, 023

---

## 🔑 Причина #1: Правило "Backwards Compatibility Before Cleanup"

**Де прописано**: [`system_map.md` §3](file:///e:/JE/.specify/system_map.md#L137) — «Architecture Hygiene & Deprecation Audit»:
> *"import_excel(file_path) and export_excel(file_path)... They are superseded... Recommendation: Deprecate and retire **when legacy compatibility is no longer required**."*

**Що накопилось через це правило:**

| Елемент | Чому не видалено |
|---|---|
| `import_excel()` у [`eel_bridge.py`](file:///e:/JE/src/app/eel_bridge.py#L224) | system_map прямо каже "retain for legacy compatibility" — видалення заплановане, але умова "коли більше не потрібно" ніколи не настала |
| `export_excel()` у [`eel_bridge.py`](file:///e:/JE/src/app/eel_bridge.py#L244) | Те саме — system_map позначив як `🟡 Deprecated` але без конкретного milestone |
| `export_horizontal_row1_leaf_paths()` у [`excel_adapter.py`](file:///e:/JE/src/hierarchy_lib/adapters/excel_adapter.py#L245) | Написано як "Backwards-compatible wrapper" у задачі T006 (Feature 020, tasks.md) — wrapper залишили, але ніколи не запланували cleanup-таск |
| `CompositeNode` / `LeafNode` aliases | system_map §3 пункт 2: *"Retained for backwards compatibility"* — прямо дозволено залишити |

**Коренева причина**: Конституція (Принцип I — SDD Scope Enforcement) забороняє видаляти код під час фаз `specify`/`plan`/`tasks`. Cleanup отримав статус "низький пріоритет" у system_map, але окремої задачі з конкретним milestone так і не з'явилось.

---

## 🔑 Причина #2: Feature 008 — Unification без повного retire старого

**Де прописано**: [`specs/008-dynamic-node-unification/tasks.md`](file:///e:/JE/specs/008-dynamic-node-unification/tasks.md), Task T003:
> *"Implement HierarchyNode and **alias/bridge** in composite.py and leaf.py"*

**Що накопичилось:**

| Елемент | Механізм |
|---|---|
| `HierarchyComponent` (base.py) | Spec 008 FR-001 казав «unify into a single DynamicNode/CompositeNode/HierarchyComponent» — тобто сама специфікація вагалась між трьома назвами. Реалізований `HierarchyNode` як нова одиниця, але `base.py` лишили, бо spec не містив явного завдання "DELETE base.py" |
| `is_container` property | Task T002 та Spec 008 FR-003 вимагали зберегти `is_container` поряд з `is_folder` для сумісності схеми `to_dict()` (Assumption: *"consistent JSON schemas (id, name, is_container, absolute_path)"*). Але жоден наступний spec не перевіряв чи JS реально читає `is_container` |
| `PathGenerator` клас | Task T008 (Feature 008) вимагав «Verify dynamic leaf path collection in test_path_generator.py» — тест написали, але `PathGenerator` як production-dependency ніколи не wired в `eel_bridge.py`. System_map §2.1 позначає його `🟢 Active Core`, хоча це неправда |

**Коренева причина**: Spec 008 правильно описав логіку уніфікації, але **tasks.md не містив завдань на видалення старих абстракцій** — лише на створення нових. Відповідно до Конституції Принцип I, агент не може самостійно видаляти код без явного cleanup-task.

---

## 🔑 Причина #3: Feature 020 — Два endpoint'и замість одного (update_node vs update_node_type)

**Де прописано**: [`specs/020-leaf-element-data-types/tasks.md`](file:///e:/JE/specs/020-leaf-element-data-types/tasks.md), Task T006:
> *"expose **update_node / update_node_type**"* — дві функції в одному рядку через `/`

**Що накопичилось:**

| Елемент | Механізм |
|---|---|
| `update_node_type()` | Task T006 прямо вимагав **обидва** endpoint'и. Але у Task T010 (app.js wiring) зробили лише `update_node()` для загального збереження. `update_node_type()` осів як непотрібний публічний API |
| `infer_column_types()` | Task T003 вимагав «unit tests for **infer_column_types**» — функцію написали під тест, але в production-flow її замінив `read_row1_headers_and_types()`. Cleanup не з'явився бо task не містив фрази "після цього видалити" |

**Коренева причина**: Spec не розмежував чітко "яку функцію викликатиме JS, яку — тест". Обидва методи потрапили в production без verification по принципу «задокументовано — значить активно».

---

## 🔑 Причина #4: System Map не синхронізований зі станом коду (Порушення Принципу VI)

**Де прописано**: [`constitution.md`](file:///e:/JE/.specify/memory/constitution.md#L58), Принцип VI:
> *"Whenever any software component... is created, modified, or **retired**, system_map.md must be updated immediately."*

**Фактичний стан system_map:**

| Позначка в system_map | Реальний стан |
|---|---|
| `PathGenerator` — `🟢 Active Core` | Не викликається жодним production-кодом |
| `get_workspace_tree()` — `🟢 Active RPC` | Не викликається у app.js |
| `get_sheet_headers()` — `🟢 Active RPC` | Не викликається у app.js |
| `update_node_type()` — `🟢 Active RPC` | Не викликається у app.js |
| `HierarchyComponent` (base.py) — `🟢 Active Base` | Ніхто не успадковує |
| `HeaderService.filter_headers()` | Відсутня в system_map взагалі |

**Коренева причина**: Принцип VI вимагає синхронізації, але жодна фаза не мала явного **"audit system_map for stale Active labels"** чекліста. Агент оновлює system_map при *створенні*, але не завжди при *витісненні* старого компонента новим.

---

## 🔑 Причина #5: Feature 023 (i18n) — надлишок у самому I18n модулі

**Де прописано**: [`specs/023-i18n-multilingual-support/tasks.md`](file:///e:/JE/specs/023-i18n-multilingual-support/tasks.md), Task T002:
> *"Create i18n.js with complete uk and en translation dictionaries, I18n.t(), localStorage persistence, language change subscriber mechanism, and translateDOM()"*

**Що накопичилось:**

| Елемент | Механізм |
|---|---|
| `getTypeBadgeLabel()` | Task T002 не деталізував API surface модуля. Розробник додав `getTypeBadgeLabel` як «зручний alias» поряд з `getTypeLabel`, але spec не вказав "лише один метод для badge labels". Ніякий task не перевіряв "чи використовується кожен публічний метод" |
| `window.I18N_DICTIONARIES` | FR-002 вимагав «centralized localization module» — виставлення в `window` здавалося безпечним, але жоден task не перевіряв "чи хтось реально читає цей global" |

**Коренева причина**: Spec 023 FR-002 і SC-001 перевіряли **повноту перекладів**, але не **мінімальність публічного API** модуля. Принцип ISP (Interface Segregation) з конституції порушено на рівні планування, бо tasks не містили кроку "audit public API surface of i18n.js".

---

## 🔑 Причина #6: Принцип IV (TDD) провокує "zombie tests"

**Де прописано**: [`constitution.md`](file:///e:/JE/.specify/memory/constitution.md#L41), Принцип IV:
> *"Unit tests must be written first and confirmed failing before writing the corresponding production logic."*

**Наслідок**: TDD-цикл за конституцією вимагає **тести → код**. Але коли production-код еволюціонував (Feature 002 замінив Feature 001, Feature 020 додав `update_node`), тести до старих функцій залишились і «легалізували» існування цих функцій:

- `test_excel_export.py` / `test_excel_import.py` → підтримують `import_from_file` / `export_to_file` живими
- `test_path_generator.py` → підтримує `PathGenerator` живим
- `test_excel_adapter.py::test_infer_column_types` → підтримує `infer_column_types` живим

**Коренева причина**: TDD-правило захищає виробничий код від видалення через "але є тест". Жоден spec не містив завдань виду "видали тест і відповідний метод який він тестує".

---

## Підсумкова матриця: хто за що відповідає

| Мертвий елемент | Feature | Принцип конституції | Прогалина в процесі |
|---|---|---|---|
| `HierarchyComponent` | 008 | II (SOLID/LSP) | tasks.md не мав "DELETE base.py" |
| `PathGenerator` | 001→008 | VI (System Map sync) | system_map не оновлено після витіснення |
| `Counter` import | 020/014 | II (SRP) | Не було lint/import-check задачі |
| `export_horizontal_row1_leaf_paths` | 014→016 | I (SDD cleanup phase) | Backward compat без expiry date |
| `infer_column_types` | 020 | IV (TDD) | Тест легалізував мертву функцію |
| `import_excel` / `export_excel` | 001→002 | I (SDD) | system_map дав "retain" без deadline |
| `get_workspace_tree` | 001→002 | VI (System Map sync) | system_map помилково помічений Active |
| `get_sheet_headers` | 002 | VI (System Map sync) | system_map помилково помічений Active |
| `update_node_type` | 020 | I (SDD) | Spec задав обидва API без розмежування хто викликає |
| `LeafNode` / `CompositeNode` | 008 | III (Composite GoF) | tasks.md сказав "alias/bridge" — не "remove" |
| `is_container` | 008 | II (SOLID/ISP) | Spec assumption вимагав для JSON schema |
| `HeaderService.filter_headers` | 002 | VI (System Map sync) | Відсутня в system_map взагалі |
| `getTypeBadgeLabel` | 023 | II (ISP) | tasks.md не задав "мінімальний API" |
| `window.I18N_DICTIONARIES` | 023 | II (ISP) | FR не перевіряв споживачів глобала |

---

## Висновок

Проблема не в якості окремих специфікацій — вони детальні та добре структуровані. Проблема в **системному пропуску**: у жодному spec/tasks не визначено фазу **"Retirement Verification"** яка б відповідала на питання:

> *"Після того як нова реалізація завершена — перевірити, що старі компоненти більше не мають активних споживачів, і якщо так — видалити їх та їх тести, та оновити system_map з `🟢 Active` на `🔴 Retired`."*

Конституція описує це через Принцип VI як "Proactive Redundancy Audit" — але **лише на фазі specify**. На фазі implement і після неї такого gate немає.
