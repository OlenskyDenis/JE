# Рівень В: Нормативний чек-лист верифікації (i18n Verification Checklist)

> **Призначення**: Повна карта перевірки двомовності інтерфейсу, синхронності словників та перекладу бейджів з прив'язкою до тестів.

---

## Чек-лист переходів станів та перевірки контрактів

| ID | Сценарій / Фаза діаграми | Вхідний стан (Pre-condition) | Дія користувача (Trigger Action) | Очікуваний стан Frontend (DOM / UI) | Очікуваний стан Backend (RPC / State) | Покриття тестом у проекті | Статус |
|:---:|---|---|---|---|---|---|:---:|
| **CHK-I18N-01** | **Перемикання на англійську мову** | Інтерфейс українською (`#langBtnUk.active`) | Клік на `#langBtnEn` | `#langBtnEn.active`, заголовок програми стає `"Database Hierarchy Creator"`, кнопки `"Tree"`, `"Settings"` | `localStorage.getItem('je_lang') == 'en'` | `tests/e2e/test_navigation_and_i18n.py::test_bilingual_toggle_uk_and_en` | `PASS` |
| **CHK-I18N-02** | **Перемикання назад на українську мову** | Інтерфейс англійською (`#langBtnEn.active`) | Клік на `#langBtnUk` | `#langBtnUk.active`, заголовок стає `"Конструктор Ієрархій БД"`, кнопки `"Дерево"`, `"Налаштування"` | `localStorage.getItem('je_lang') == 'uk'` | `tests/e2e/test_navigation_and_i18n.py::test_bilingual_toggle_uk_and_en` | `PASS` |
| **CHK-I18N-03** | **Динамічний переклад бейджів типів даних** | Вузол з типом `Currency` на полотні | Клік на `#langBtnEn` | Текст бейджа `.type-badge` змінюється з `"Валюта"` на `"Currency"` | Без мутації дерева на бекенді | `tests/e2e/test_navigation_and_i18n.py::test_bilingual_toggle_uk_and_en` | `PASS` |
| **CHK-I18N-04** | **Переклад текстів та кнопок модальних вікон** | Обрано англійську мову | Відкриття `#settingsModal` | Заголовок `"Settings"`, кнопка `"Save"`, кнопка `"Reset to Defaults"` | Перекладено через `data-i18n` | `tests/unit/test_frontend_contracts.py::test_i18n_dictionary_parity` | `PASS` |
| **CHK-I18N-05** | **100% паритет ключів між UK та EN словниками** | Ізольоване середовище JS / Node | Порівняння всіх ключів `i18n.js` | Кількість та назви ключів у `translations.uk` та `translations.en` абсолютно ідентичні | Нуль пропущених ключів | `tests/unit/test_frontend_contracts.py::test_i18n_dictionary_parity` | `PASS` |
| **CHK-I18N-06** | **Збереження обраної мови після перезавантаження** | Вибрано мову `en` | Оновлення сторінки | Програма стартує з активною англійською мовою | Читання `localStorage` на старті | `tests/e2e/test_navigation_and_i18n.py::test_bilingual_toggle_uk_and_en` | `PASS` |
| **CHK-I18N-07** | **Автоматична валідація мови в матричному тесті** | Довільний стан | Виклик `flow_bilingual_toggle_en_uk` | Автоматична валідація перемикання та повернення мови | `MatrixFlowExecutor` | `tests/e2e/test_automated_interaction_matrix.py::test_full_state_transition_chain` | `PASS` |
