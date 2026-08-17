# Рівень А: Атомарні мікро-цикли елементів (Settings Micro-Lifecycles)

> **Призначення**: Кожен окремий елемент інтерфейсу розглядається як самостійний, замкнений автомат станів зі своїм повним життєвим циклом роботи.

---

## 1. `ButtonActionLifecycle` (Життєвий цикл кнопок дій)

Застосовується до: `#btnSettings`, `#btnSettingsSave`, `#btnSettingsReset`, `#btnSettingsCancel`.

```mermaid
stateDiagram-v2
    [*] --> Idle: DOM Mount (Enabled)
    Idle --> Hovered: pointerenter / mouseover
    Hovered --> Idle: pointerleave / mouseout
    Hovered --> ActivePressed: pointerdown / click
    ActivePressed --> Processing: Trigger Event Dispatch
    Processing --> Idle: Action Complete (Success/Cancel)
    Processing --> Disabled: If Async Wait / Pending
    Disabled --> Idle: Response Received
```

- **Стани**:
  - `Idle`: Кнопка видима, готова до взаємодії (`to_be_enabled()`).
  - `Hovered`: Активується підсвічування фону/тіні (CSS `:hover`).
  - `ActivePressed`: Натиснутий стан (CSS `:active`).
  - `Processing`: Виклик асоційованого обробника події в `SettingsController`.

---

## 2. `ModalLifecycle` (Життєвий цикл модального вікна)

Застосовується до: `#settingsModal`.

```mermaid
stateDiagram-v2
    [*] --> ClosedHidden: Initial DOM (class "hidden")
    ClosedHidden --> Opening: Trigger from SettingsController.openSettingsModal()
    Opening --> FetchingConfig: Call eel.get_settings()
    FetchingConfig --> OpenRendered: Populate Form Inputs & remove "hidden" class
    OpenRendered --> ValidatingInput: User edits Delimiter / Type
    ValidatingInput --> Submitting: Click "#btnSettingsSave"
    ValidatingInput --> Resetting: Click "#btnSettingsReset"
    ValidatingInput --> Dismissing: Click "#btnSettingsCancel" / "#settingsModalClose"
    Submitting --> ClosedHidden: Save Success & add "hidden" class
    Resetting --> ClosedHidden: Reset Success & add "hidden" class
    Dismissing --> ClosedHidden: Revert changes & add "hidden" class
```

- **Стани**:
  - `ClosedHidden`: Модалка має клас `modal-overlay hidden` і невидима (`not_to_be_visible()`).
  - `OpenRendered`: Клас `hidden` знято, модалка видима (`to_be_visible()`), фокус на першому полі вводу.

---

## 3. `InputControlLifecycle` (Життєвий цикл текстового поля розділювача)

Застосовується до: `#inputSettingDelimiter`.

```mermaid
stateDiagram-v2
    [*] --> EmptyOrBound: Initial Value ("\")
    EmptyOrBound --> Focused: focus / click
    Focused --> Editing: User inputs custom character (e.g. "/", ".", "-")
    Editing --> Validating: Trim & length check (max 5 chars)
    Validating --> ValidReady: Non-empty valid string
    Validating --> FallbackDefault: If empty, defaults to "\" on save
    ValidReady --> Blurred: blur / enter
    FallbackDefault --> Blurred: blur / enter
    Blurred --> SavedState: Persisted via SettingsService
```

---

## 4. `SelectDropdownLifecycle` (Життєвий цикл селектора типу за замовчуванням)

Застосовується до: `#selectSettingDefaultType`.

```mermaid
stateDiagram-v2
    [*] --> Populated: 9 Data Types rendered as <option>
    Populated --> CurrentSelected: Set active value (e.g. "Text" or "Currency")
    CurrentSelected --> OptionChanging: User changes option in dropdown
    OptionChanging --> Dispatched: Change event captures new data type
    Dispatched --> Persisted: Passed to eel.update_settings()
```

---

## 5. `ToastNotificationLifecycle` (Життєвий цикл спливаючого сповіщення)

Застосовується до зворотного зв'язку збереження/скидання налаштувань.

```mermaid
stateDiagram-v2
    [*] --> Triggered: App.showToast(message, type)
    Triggered --> Rendered: Create .toast.toast-success element
    Rendered --> VisibleOnScreen: Append to #toastContainer (computed border & bg)
    VisibleOnScreen --> AutoDismissTimer: setTimeout (3500ms)
    AutoDismissTimer --> FadeOut: Animate opacity to 0
    FadeOut --> Detached: element.remove() from DOM
    Detached --> [*]
```
