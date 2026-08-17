# Рівень В: Нормативний чек-лист верифікації (Unsaved Modal Verification Checklist)

> **Призначення**: Повна карта перевірки перехоплення незбережених змін та захисту даних з прив'язкою до тестів.

---

## Чек-лист переходів станів та перевірки контрактів

| ID | Сценарій / Фаза діаграми | Вхідний стан (Pre-condition) | Дія користувача (Trigger Action) | Очікуваний стан Frontend (DOM / UI) | Очікуваний стан Backend (RPC / State) | Покриття тестом у проекті | Статус |
|:---:|---|---|---|---|---|---|:---:|
| **CHK-UNS-01** | **Перехоплення зміни аркуша при незбережених змінах** | `SessionController.isDirty = true`, активний `"Sheet1"` | Вибір `"Sheet2"` у `#activeSheetSelector` | Відкривається `#unsavedModal` (`to_be_visible()`), селектор тимчасово зупинено | `pendingAction` зафіксовано у пам'яті фронтенду | `tests/e2e/test_multi_sheet_and_excel_lifecycle.py::test_unsaved_changes_modal_cancel_and_discard` | `PASS` |
| **CHK-UNS-02** | **Скасування перемикання (Cancel)** | `#unsavedModal` відкрито | Клік на `#btnUnsavedCancel` | `#unsavedModal` закривається (`has_class("hidden")`), `#activeSheetSelector` повертається на `"Sheet1"` | Жодного виклику `switch_active_sheet` не відбулося, `isDirty` залишається `true` | `tests/e2e/test_multi_sheet_and_excel_lifecycle.py::test_unsaved_changes_modal_cancel_and_discard` | `PASS` |
| **CHK-UNS-03** | **Відхилення змін (Discard)** | `#unsavedModal` відкрито | Клік на `#btnUnsavedDiscard` | `#unsavedModal` закривається, `#activeSheetSelector` стає `"Sheet2"`, відображається дерево `"Sheet2"` | `eel.switch_active_sheet("Sheet2")` виконано, `isDirty` стає `false` | `tests/e2e/test_multi_sheet_and_excel_lifecycle.py::test_unsaved_changes_modal_cancel_and_discard` | `PASS` |
| **CHK-UNS-04** | **Збереження та продовження (Save & Continue)** | `#unsavedModal` відкрито, шаблон прив'язано | Клік на `#btnUnsavedSave` | `#unsavedModal` закривається, `#templateStatusBadge` оновлюється на `(Synced)`, дерево перемикається | Виклик `save_template_sync()` $\to$ виклик `switch_active_sheet()` | `tests/unit/test_excel_adapter.py::test_export_template_multi_sheet` | `PASS` |
| **CHK-UNS-05** | **Перехоплення імпорту нового файлу та відхилення** | `isDirty = true` | Клік `#btnImportExcel` та `#btnUnsavedDiscard` | Відкривається `#unsavedModal`, після відхилення запускається імпорт | `promptOpenAndImportFile` виконано, `isDirty` скинуто | `tests/e2e/test_multi_sheet_and_excel_lifecycle.py::test_unsaved_changes_modal_cancel_and_discard` | `PASS` |
| **CHK-UNS-06** | **Перехоплення кнопки оновлення сесії** | `isDirty = true` | Клік `#btnRefresh` | Відкривається `#unsavedModal` | Оновлення з диска заблоковано до вирішення змін | `tests/e2e/test_navigation_and_i18n.py::test_refresh_workspace_button` | `PASS` |
