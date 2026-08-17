# JE — Specification Registry (Каталог Специфікацій)

Цей каталог містить повний перелік усіх специфікацій проєкту **JE (Database Hierarchy Creator)**, створених та імплементованих у рамках процесу розробки за стандартом `.specify`.

---

## Реєстр Специфікацій

| # | Специфікація | Назва / Опис | Статус |
|---|---|---|---|
| **001** | [`001-database-hierarchy-creator`](file:///e:/JE/specs/001-database-hierarchy-creator) | Базова архітектура створення ієрархії баз даних, канвас та експорт в Excel | `Completed` |
| **002** | [`002-excel-sidebar-reorganizer`](file:///e:/JE/specs/002-excel-sidebar-reorganizer) | Сайдбар для реорганізації заголовків Excel та структури БД | `Completed` |
| **003** | [`003-native-file-dialogs`](file:///e:/JE/specs/003-native-file-dialogs) | Нативні системні діалогові вікна вибору файлів через Tkinter bridge | `Completed` |
| **004** | [`004-relocate-add-root-button`](file:///e:/JE/specs/004-relocate-add-root-button) | Перенесення кнопки створення кореневого вузла на робочу область | `Completed` |
| **005** | [`005-unified-drag-drop-bug`](file:///e:/JE/specs/005-unified-drag-drop-bug) | Уніфікований обробник Drag-and-Drop взаємодій між контейнерами | `Completed` |
| **006** | [`006-excel-hierarchical-import`](file:///e:/JE/specs/006-excel-hierarchical-import) | Автоматичний ієрархічний імпорт заголовків Excel та побудова дерева | `Completed` |
| **007** | [`007-excel-import-optimization`](file:///e:/JE/specs/007-excel-import-optimization) | Високопродуктивне потокове читання Excel (`read_only=True`) з лімітом безпеки | `Completed` |
| **008** | [`008-dynamic-node-unification`](file:///e:/JE/specs/008-dynamic-node-unification) | Динамічна уніфікація вузлів (усунення статичного поділу folder/leaf) | `Completed` |
| **009** | [`009-remove-redundant-add-root-button`](file:///e:/JE/specs/009-remove-redundant-add-root-button) | Спрощення хедера робочої області та створення кореня через Empty State | `Completed` |
| **010** | [`010-streamline-modal-and-dead-dom-cleanup`](file:///e:/JE/specs/010-streamline-modal-and-dead-dom-cleanup) | Оптимізація модальних вікон та очищення мертвого DOM-коду | `Completed` |
| **011** | [`011-tree-folder-collapse-expand`](file:///e:/JE/specs/011-tree-folder-collapse-expand) | Згортання та розгортання гілок ієрархічного дерева з візуальними стрілками | `Completed` |
| **012** | [`012-preserve-excel-column-order`](file:///e:/JE/specs/012-preserve-excel-column-order) | Збереження оригінального порядку колонок Excel при побудові дерева | `Completed` |
| **013** | [`013-unified-sidebar-tabs-resize`](file:///e:/JE/specs/013-unified-sidebar-tabs-resize) | Вкладки в сайдбарі та можливість зміни ширини (drag-resize) | `Completed` |
| **014** | [`014-export-headers-only-clean-workbook`](file:///e:/JE/specs/014-export-headers-only-clean-workbook) | Чистий експорт шаблону книги Excel із префіксом `h_...xlsx` | `Completed` |
| **015** | [`015-sheet-manager-save-prompt-and-cross-sheet-catalog`](file:///e:/JE/specs/015-sheet-manager-save-prompt-and-cross-sheet-catalog) | Керування аркушами, між-аркушевий каталог та захист незбережених змін | `Completed` |
| **016** | [`016-multi-sheet-session-persistence-and-template-sync`](file:///e:/JE/specs/016-multi-sheet-session-persistence-and-template-sync) | Збереження сесії багатьох аркушів та автосинхронізація шаблону | `Completed` |
| **017** | [`017-move-active-sheet-selector-to-canvas-workspace`](file:///e:/JE/specs/017-move-active-sheet-selector-to-canvas-workspace) | Перенесення перемикача активного аркуша на робочу область | `Completed` |
| **018** | [`018-unsaved-changes-prompt-on-new-file-import`](file:///e:/JE/specs/018-unsaved-changes-prompt-on-new-file-import) | Діалог попередження про незбережені зміни при імпорті нового файлу | `Completed` |
| **019** | [`019-node-renaming-in-workspace`](file:///e:/JE/specs/019-node-renaming-in-workspace) | Перейменування вузлів на полотні через модальне вікно та інлайн-валідація | `Completed` |
| **020** | [`020-leaf-element-data-types`](file:///e:/JE/specs/020-leaf-element-data-types) | Інспекція та редагування типів даних (`string`, `number`, `date`, `boolean`) | `Completed` |
| **021** | [`021-excel-data-types-bug`](file:///e:/JE/specs/021-excel-data-types-bug) | Автоматичне виведення типів даних колонок за першим рядком Excel | `Completed` |
| **022** | [`022-refresh-imported-excel-session`](file:///e:/JE/specs/022-refresh-imported-excel-session) | Оновлення та повторне зчитування активної Excel-сесії | `Completed` |
| **023** | [`023-i18n-multilingual-support`](file:///e:/JE/specs/023-i18n-multilingual-support) | Повна багатомовна локалізація інтерфейсу (Українська та Англійська) | `Completed` |
| **024** | [`024-fix-data-type`](file:///e:/JE/specs/024-fix-data-type) | Локалізація бейджів та підказок типів даних вузлів | `Completed` |
| **025** | [`025-root-node-controls`](file:///e:/JE/specs/025-root-node-controls) | Елементи швидкого створення кореневих вузлів на полотні | `Completed` |
| **026** | [`026-settings-menu-config`](file:///e:/JE/specs/026-settings-menu-config) | Меню налаштувань (розділювач шляхів та тип даних за замовчуванням) | `Completed` |
| **027** | [`027-excel-block-hierarchy-view`](file:///e:/JE/specs/027-excel-block-hierarchy-view) | Режим табличного блокового перегляду ієрархії (Excel Block View) | `Completed` |
| **028** | [`028-unique-level-hierarchy-view`](file:///e:/JE/specs/028-unique-level-hierarchy-view) | Режим порівневого перегляду унікальних елементів та підсвічування дублікатів | `Completed` |
| **029** | [`029-codebase-cleanup-and-solid-refactor`](file:///e:/JE/specs/029-codebase-cleanup-and-solid-refactor) | Очищення кодової бази та рефакторинг згідно з принципами SOLID | `Completed` |
| **030** | [`030-unique-levels-leaf-grouping`](file:///e:/JE/specs/030-unique-levels-leaf-grouping) | Групування листя (leaf-first), абзаци та ергономіка унікальних рівнів | `Completed` |
| **031** | [`031-playwright-e2e-testing`](file:///e:/JE/specs/031-playwright-e2e-testing) | Покриття функціоналу автоматизованими E2E Playwright тестами | `Completed` |
| **032** | [`032-test-fixtures-and-quality-automation`](file:///e:/JE/specs/032-test-fixtures-and-quality-automation) | Еталонний набір тестових Excel-фікстур, база знань проєкту та Pre-Commit автоматизація | `Completed` |
| **033** | [`033-project-audit-and-hygiene`](file:///e:/JE/specs/033-project-audit-and-hygiene) | Аудит проєкту, виявлення мертвого коду/CSS, декомпозиція монолітів $\le 200$ рядків | `Completed` |
| **034** | [`034-full-project-test-suite`](file:///e:/JE/specs/034-full-project-test-suite) | Повне наскрізне покриття функціоналу автоматизованими тестами | `Completed` |
| **035** | [`035-use-case-diagrams-and-test-checklists`](file:///e:/JE/specs/035-use-case-diagrams-and-test-checklists) | Діаграми життєвого циклу (Frontend + Backend) та чек-листи верифікації | `In Progress` |


---

## Структура Папки Специфікації

Кожна папка специфікації організована за структурою:
* `spec.md` — бізнес-вимоги, сценарії користувача, acceptance criteria.
* `plan.md` — детальний технічний план реалізації, змінені компоненти та фази.
* `research.md` — дослідження поточного стану системи, аналіз альтернатив.
* `data-model.md` — моделі даних та DTO контракти (за наявності).
* `tasks.md` — декомпозиція та чеклист задач.
* `quickstart.md` / `contracts/` — інструкції з валідації та контракти інтерфейсів.
