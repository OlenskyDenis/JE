# Рівень Б: Наскрізна Sequence-діаграма модального вікна незбережених змін (Unsaved Changes Full-Stack Sequence)

> **Призначення**: Повний життєвий цикл перехоплення навігації при наявності незбережених змін, збереження шаблону, відхилення або скасування.

---

```mermaid
sequenceDiagram
    autonumber
    actor User as 👤 Користувач
    participant SheetSel as 📑 #activeSheetSelector
    participant SessCtrl as 🎛️ SessionController
    participant ModalMgr as 🪟 ModalManager
    participant UnsavedModal as ⚠️ #unsavedModal
    participant RPC as ⚡ Eel Bridge (eel_bridge.py)
    participant SessMgr as 🗄️ SessionManager
    participant ExcelWriter as 📊 ExcelWriter

    %% ВИХІДНИЙ СТАН: Брудний стан сесії
    Note over User, ExcelWriter: ВИХІДНИЙ СТАН: Сесія з незбереженими змінами (isDirty = true)
    User ->> SheetSel: Спроба перемкнути аркуш з "Sheet1" на "Sheet2"
    SheetSel ->> SessCtrl: promptSwitchActiveSheet("Sheet2")
    SessCtrl ->> SessCtrl: Перевірка this.isDirty (true!)
    SessCtrl ->> SessCtrl: this.pendingAction = { type: 'switch_sheet', targetSheet: 'Sheet2' }
    SessCtrl ->> ModalMgr: ModalManager.promptUnsaved('switch_sheet')
    ModalMgr ->> UnsavedModal: Зняття класу .hidden (Modal Rendered)
    UnsavedModal -->> User: Діалог із вибором: [Зберегти та продовжити], [Відхилити], [Скасувати]

    %% ВАРІАНТ 1: Користувач обирає "Скасувати"
    alt ВАРІАНТ 1: Скасування (Cancel)
        User ->> UnsavedModal: Клік на #btnUnsavedCancel
        UnsavedModal ->> SessCtrl: cancelPendingAction()
        SessCtrl ->> SessCtrl: this.pendingAction = null
        SessCtrl ->> SheetSel: Revert значення селектора назад на "Sheet1"
        SessCtrl ->> UnsavedModal: Додавання класу .hidden
        Note over User, ExcelWriter: Дерево залишається незмінним на Sheet1, жодних RPC викликів

    %% ВАРІАНТ 2: Користувач обирає "Відхилити зміни"
    else ВАРІАНТ 2: Відхилити зміни (Discard)
        User ->> UnsavedModal: Клік на #btnUnsavedDiscard
        UnsavedModal ->> SessCtrl: executePendingAction(shouldSaveFirst = false)
        SessCtrl ->> SessCtrl: this.isDirty = false
        SessCtrl ->> RPC: eel.switch_active_sheet("Sheet2")()
        RPC ->> SessMgr: switch_active_sheet("Sheet2")
        SessMgr -->> RPC: {"success": true, "active_sheet": "Sheet2", "roots": [...]}
        RPC -->> SessCtrl: {"success": true, ...}
        SessCtrl ->> SheetSel: Значення стає "Sheet2"
        SessCtrl ->> UnsavedModal: Додавання класу .hidden

    %% ВАРІАНТ 4: Перехоплення імпорту файлу (Import Intercept)
    Note over User, ExcelWriter: СЦЕНАРІЙ 2: Перехоплення імпорту файлу при брудній сесії
    User ->> SessCtrl: Клік #btnImportExcel
    SessCtrl ->> SessCtrl: this.pendingAction = { type: 'import_file' }
    SessCtrl ->> ModalMgr: promptUnsaved('import')
    ModalMgr ->> UnsavedModal: Render ("Відкинути і імпортувати", "Зберегти шаблон і імпортувати")
    User ->> UnsavedModal: Клік #btnUnsavedDiscard
    UnsavedModal ->> ModalMgr: closeUnsavedModal()
    UnsavedModal ->> SessCtrl: executePendingAction(false)
    SessCtrl ->> SessCtrl: isDirty = false, pendingAction = null
    SessCtrl ->> RPC: eel.open_file_dialog() -> promptOpenAndImportFile()
```

