# Рівень Б: Наскрізна діаграма макро-взаємодії (Settings Full-Stack Sequence)

> **Призначення**: Показує повний паралельний цикл роботи підсистеми Налаштувань (Settings) між подіями користувача, контролерами Frontend, шлюзом Eel RPC та сервісами Backend.

---

## 1. Наскрізна Sequence-діаграма повного життєвого циклу

```mermaid
sequenceDiagram
    autonumber
    actor User as 👤 Користувач
    participant HeaderBtn as 🔘 #btnSettings
    participant SetCtrl as 🎛️ SettingsController
    participant Modal as 🪟 #settingsModal
    participant Inputs as 📝 Form Inputs (Delimiter / Type)
    participant RPC as ⚡ Eel Bridge (eel_bridge.py)
    participant SetSvc as ⚙️ SettingsService
    participant TreeRend as 🌳 TreeRenderer & PathList
    participant Toast as 🍞 ToastNotification

    %% 1. Відкриття модального вікна
    Note over User, SetSvc: ФАЗА 1: Відкриття та отримання поточної конфігурації
    User ->> HeaderBtn: Клік на #btnSettings (ButtonActionLifecycle)
    HeaderBtn ->> SetCtrl: openSettingsModal()
    SetCtrl ->> RPC: eel.get_settings()()
    RPC ->> SetSvc: SettingsService.get_settings()
    SetSvc -->> RPC: {"delimiter": "\\", "default_data_type": "Text"}
    RPC -->> SetCtrl: {"success": true, "settings": {...}}
    SetCtrl ->> Inputs: Заповнення #inputSettingDelimiter та #selectSettingDefaultType
    SetCtrl ->> Modal: ModalLifecycle.Open (видалення класу .hidden)
    Modal -->> User: Модальне вікно відображається на екрані

    %% 2. Редагування та Збереження
    Note over User, SetSvc: ФАЗА 2: Модифікація та збереження налаштувань
    User ->> Inputs: Введення нового розділювача (наприклад, "/") та вибір типу "Currency"
    User ->> Modal: Клік на #btnSettingsSave (ButtonActionLifecycle)
    Modal ->> SetCtrl: saveSettings()
    SetCtrl ->> RPC: eel.update_settings(delimiter="/", default_data_type="Currency")()
    RPC ->> SetSvc: SettingsService.update_settings("/", "Currency")
    SetSvc ->> SetSvc: Збереження у JSON / пам'ять
    RPC ->> RPC: Перерахунок шляхів у active forest з новим delimiter
    RPC -->> SetCtrl: {"success": true, "settings": {...}, "roots": [...]}
    SetCtrl ->> TreeRend: Оновлення шляхів у #pathList та на полотні
    SetCtrl ->> Modal: ModalLifecycle.Close (додавання класу .hidden)
    SetCtrl ->> Toast: ToastNotificationLifecycle.Show("Налаштування збережено", "success")
    Toast -->> User: Візуальне сповіщення з'являється і зникає через 3.5с

    %% 3. Скидання до значень за замовчуванням
    Note over User, SetSvc: ФАЗА 3: Скидання до значень за замовчуванням
    User ->> HeaderBtn: Клік на #btnSettings
    HeaderBtn ->> SetCtrl: openSettingsModal()
    SetCtrl ->> Modal: ModalLifecycle.Open
    User ->> Modal: Клік на #btnSettingsReset (ButtonActionLifecycle)
    Modal ->> SetCtrl: resetSettings()
    SetCtrl ->> RPC: eel.reset_settings()()
    RPC ->> SetSvc: SettingsService.reset_to_defaults()
    SetSvc -->> RPC: {"delimiter": "\\", "default_data_type": "Text"}
    RPC -->> SetCtrl: {"success": true, "settings": {...}, "roots": [...]}
    SetCtrl ->> TreeRend: Відновлення стандартних шляхів у #pathList
    SetCtrl ->> Modal: ModalLifecycle.Close
    SetCtrl ->> Toast: ToastNotificationLifecycle.Show("Скинуто до стандартних", "info")

    %% 4. Скасування без збереження
    Note over User, SetSvc: ФАЗА 4: Скасування без збереження
    User ->> HeaderBtn: Клік на #btnSettings
    SetCtrl ->> Modal: ModalLifecycle.Open
    User ->> Inputs: Введення тимчасового тексту ";"
    User ->> Modal: Клік на #btnSettingsCancel / #settingsModalClose
    Modal ->> SetCtrl: closeSettingsModal()
    SetCtrl ->> Modal: ModalLifecycle.Close (відхилення змін, нуль RPC викликів)
    Modal -->> User: Модальне вікно закрите, налаштування не змінилися
```

---

## 2. Архітектурні компоненти та зони відповідальності

| Шар | Компонент | Роль у життєвому циклі |
|---|---|---|
| **Frontend UI** | `#btnSettings`, `#settingsModal`, `#inputSettingDelimiter`, `#selectSettingDefaultType` | DOM-елементи взаємодії, фокус та валідація |
| **Frontend Logic** | `window.SettingsController` ([`src/web/js/settings_controller.js`](file:///E:/JE/src/web/js/settings_controller.js)) | Отримання/збереження конфігурації, передача даних у `TreeRenderer` |
| **Desktop IPC** | `eel_bridge.py` ([`src/app/eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py)) | Маршрутизація RPC функцій `get_settings`, `update_settings`, `reset_settings` |
| **Backend Core** | `SettingsService` ([`src/hierarchy_lib/services/settings_service.py`](file:///E:/JE/src/hierarchy_lib/services/settings_service.py)) | Джерело правди (Single Source of Truth) для розділювача та типу за замовчуванням |
| **Tree Domain** | `WorkspaceForest`, `PathParserService` | Перерахунок текстових представлень листя при зміні розділювача |
