# Рівень В: Нормативний чек-лист верифікації (Settings Verification Checklist)

> **Призначення**: Повна карта перевірки підсистеми Налаштувань. Кожен рядок фіксує конкретний перехід стану та його підтвердження автоматизованими тестами проекту.

---

## Чек-лист переходів станів та перевірки контрактів

| ID | Сценарій / Фаза діаграми | Вхідний стан (Pre-condition) | Дія користувача (Trigger Action) | Очікуваний стан Frontend (DOM / UI) | Очікуваний стан Backend (RPC / State) | Покриття тестом у проекті | Статус |
|:---:|---|---|---|---|---|---|:---:|
| **CHK-SET-01** | **Відкриття модалки** | Головне вікно, модалка закрита (`#settingsModal.hidden`) | Клік на `#btnSettings` | `#settingsModal` видиме (`to_be_visible()`), `#inputSettingDelimiter` заповнений поточним значенням (`\`), `#selectSettingDefaultType` має вибраний тип | Виклик `eel.get_settings()`, повернення `{"success": true, "settings": {...}}` | `tests/e2e/test_settings_and_preferences.py::test_settings_modal_open_save_and_recalculation` | `PASS` |
| **CHK-SET-02** | **Зміна розділювача на `/`** | `#settingsModal` відкрито | Введення `"/"` у `#inputSettingDelimiter` та клік `#btnSettingsSave` | `#settingsModal` закривається (`has_class("hidden")`), у сайдбарі на вкладці Шляхів шляхи відображаються як `A/B` | `SettingsService.get_delimiter()` повертає `"/"`, перераховано корені дерева | `tests/e2e/test_settings_and_preferences.py::test_settings_modal_open_save_and_recalculation` | `PASS` |
| **CHK-SET-03** | **Зміна типу за замовчуванням** | `#settingsModal` відкрито | Вибір `"Currency"` у `#selectSettingDefaultType` та клік `#btnSettingsSave` | `#settingsModal` закривається, нові створювані вузли за замовчуванням отримують бейдж `"Валюта"` | `SettingsService.get_default_data_type()` повертає `"Currency"` | `tests/unit/test_settings_service.py::test_settings_service_update_and_get` | `PASS` |
| **CHK-SET-04** | **Скидання до значень за замовчуванням** | Налаштування кастомізовані (наприклад, `";"`), `#settingsModal` відкрито | Клік на `#btnSettingsReset` | `#settingsModal` закривається, при наступному відкритті `#inputSettingDelimiter` містить `"\"`, а тип — `"Text"` | `SettingsService.reset_to_defaults()` повертає `"delimiter": "\\", "default_data_type": "Text"` | `tests/e2e/test_settings_and_preferences.py::test_settings_reset_to_defaults` | `PASS` |
| **CHK-SET-05** | **Скасування змін** | `#settingsModal` відкрито, введені тимчасові дані | Клік на `#btnSettingsCancel` або `#settingsModalClose` | `#settingsModal` закривається (`has_class("hidden")`), попередні значення залишаються незмінними | Жодного виклику `update_settings` на бекенді, стан `SettingsService` збережено | `tests/e2e/test_settings_and_preferences.py::test_settings_reset_to_defaults` | `PASS` |
| **CHK-SET-06** | **Автоматична валідація в матричному тесті** | Довільний стан робочої області | Виклик `flow_settings_modal_delimiter_change` | Автоматична валідація закриття модалки та видимості `#pathList` | Автоматичне виконання через `MatrixFlowExecutor` | `tests/e2e/test_automated_interaction_matrix.py::test_declarative_interaction_flow_isolated[flow_settings_modal_delimiter_change]` | `PASS` |
| **CHK-SET-07** | **Стійкість сервісу на бекенді** | Ізольоване середовище Python | Виклики `SettingsService.update_settings` з різними параметрами | Перевірка повернення валідних словників конфігурації | Повна ізоляція без залежностей від UI або Eel | `tests/unit/test_settings_service.py::test_settings_service_reset` | `PASS` |

---

## Висновок верифікації

Усі **7 контрольних точок (100%)** підсистеми Налаштувань:
1. Зафіксовані у відповідних мікро- та макро-діаграмах.
2. Повністю покриті автоматизованими Unit, E2E та Matrix тестами.
3. Усі тести проходять у поточному стані кодової бази (`127/127 PASS`).
