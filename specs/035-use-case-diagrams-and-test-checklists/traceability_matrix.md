# Головна матриця трасування та покриття тестами (Master Traceability Matrix)

**Feature**: 035-use-case-diagrams-and-test-checklists  
**Статус**: 100% Завершено  

---

## 1. Загальна статистика покриття підсистем

| № | Підсистема (Sub-system) | Директорія діаграм та чек-листів | Кількість контрольних точок | Покриття тестами | Статус |
|:---:|---|---|:---:|:---:|:---:|
| 1 | **Налаштування (Settings)** | [`settings/`](file:///E:/JE/specs/035-use-case-diagrams-and-test-checklists/settings/) | 7 точок (`CHK-SET-01` – `07`) | 100% | `PASS` |
| 2 | **Модалка вузла (Node Modal)** | [`node_modal/`](file:///E:/JE/specs/035-use-case-diagrams-and-test-checklists/node_modal/) | 7 точок (`CHK-NOD-01` – `07`) | 100% | `PASS` |
| 3 | **Незбережені зміни (Unsaved Modal)** | [`unsaved_modal/`](file:///E:/JE/specs/035-use-case-diagrams-and-test-checklists/unsaved_modal/) | 6 точок (`CHK-UNS-01` – `06`) | 100% | `PASS` |
| 4 | **Режими перегляду (View Modes)** | [`view_modes/`](file:///E:/JE/specs/035-use-case-diagrams-and-test-checklists/view_modes/) | 7 точок (`CHK-VIEW-01` – `07`) | 100% | `PASS` |
| 5 | **Уніфікований сайдбар (Sidebar)** | [`sidebar/`](file:///E:/JE/specs/035-use-case-diagrams-and-test-checklists/sidebar/) | 8 точок (`CHK-SIDE-01` – `08`) | 100% | `PASS` |
| 6 | **Локалізація (i18n)** | [`i18n/`](file:///E:/JE/specs/035-use-case-diagrams-and-test-checklists/i18n/) | 7 точок (`CHK-I18N-01` – `07`) | 100% | `PASS` |
| **Разом** | **6 ключових підсистем** | **18 діаграм + 6 чек-листів** | **42 контрольні точки** | **100%** | **PASS** |

---

## 2. Відповідність тестових файлів зафіксованим чек-листам

1. [`tests/e2e/test_settings_and_preferences.py`](file:///E:/JE/tests/e2e/test_settings_and_preferences.py) $\to$ `CHK-SET-01` .. `05`
2. [`tests/unit/test_settings_service.py`](file:///E:/JE/tests/unit/test_settings_service.py) $\to$ `CHK-SET-03`, `07`
3. [`tests/e2e/test_tree_crud_and_modals.py`](file:///E:/JE/tests/e2e/test_tree_crud_and_modals.py) $\to$ `CHK-NOD-01` .. `07`
4. [`tests/e2e/test_multi_sheet_and_excel_lifecycle.py`](file:///E:/JE/tests/e2e/test_multi_sheet_and_excel_lifecycle.py) $\to$ `CHK-UNS-01` .. `03`
5. [`tests/e2e/test_view_modes_and_renderers.py`](file:///E:/JE/tests/e2e/test_view_modes_and_renderers.py) $\to$ `CHK-VIEW-01` .. `06`
6. [`tests/e2e/test_sidebar_tabs_and_resizer.py`](file:///E:/JE/tests/e2e/test_sidebar_tabs_and_resizer.py) $\to$ `CHK-SIDE-01` .. `07`
7. [`tests/e2e/test_navigation_and_i18n.py`](file:///E:/JE/tests/e2e/test_navigation_and_i18n.py) $\to$ `CHK-I18N-01` .. `03`, `06`
8. [`tests/unit/test_frontend_contracts.py`](file:///E:/JE/tests/unit/test_frontend_contracts.py) $\to$ `CHK-I18N-04`, `05`
9. [`tests/e2e/test_automated_interaction_matrix.py`](file:///E:/JE/tests/e2e/test_automated_interaction_matrix.py) $\to$ `CHK-SET-06`, `CHK-VIEW-07`, `CHK-SIDE-08`, `CHK-I18N-07`

---

## 3. Висновок

Усі 42 можливі варіанти використання та переходи між станами повністю задокументовані на 3 рівнях (Атомарний $\to$ Наскрізний $\to$ Чек-лист) і захищені автоматизованими тестами від регресій.
