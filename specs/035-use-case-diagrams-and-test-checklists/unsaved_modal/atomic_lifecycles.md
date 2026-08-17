# Рівень А: Атомарні мікро-цикли елементів (Unsaved Modal Micro-Lifecycles)

> **Призначення**: Автомати станів для модального вікна захисту від незбережених змін (`#unsavedModal`).

---

## 1. `DirtyStateTriggerLifecycle` (Життєвий цикл брудного стану сесії)

Застосовується до: `SessionController.isDirty`.

```mermaid
stateDiagram-v2
    [*] --> CleanState: SessionController.isDirty = false
    CleanState --> MutatedDirty: Any tree CRUD / Drag-Drop / Reorder
    MutatedDirty --> NavigationAttempt: User switches sheet / imports file / refreshes
    NavigationAttempt --> InterceptedPrompt: PendingAction stored & #unsavedModal opened
    InterceptedPrompt --> CleanState: User clicks "Discard" or "Save & Continue"
    InterceptedPrompt --> MutatedDirty: User clicks "Cancel" (Action aborted)
```

---

## 2. `UnsavedModalActionLifecycle` (Життєвий цикл дій діалогу)

Застосовується до кнопок: `#btnUnsavedSave`, `#btnUnsavedDiscard`, `#btnUnsavedCancel`.

```mermaid
stateDiagram-v2
    [*] --> ModalRendered: #unsavedModal visible on screen
    ModalRendered --> SavingAndContinuing: Click #btnUnsavedSave
    ModalRendered --> DiscardingAndContinuing: Click #btnUnsavedDiscard
    ModalRendered --> CancellingRevert: Click #btnUnsavedCancel
    SavingAndContinuing --> ExecutingPending: Save template first -> Run pending action
    DiscardingAndContinuing --> ExecutingPending: Reset isDirty = false -> Run pending action
    CancellingRevert --> Aborted: Reset pending action -> Revert activeSheetSelector
```

---

## 3. `PendingActionDispatcherLifecycle` (Життєвий цикл відкладеної дії)

Застосовується до: `SessionController.pendingAction`.

```mermaid
stateDiagram-v2
    [*] --> None: pendingAction = null
    None --> Enqueued: { type: 'switch_sheet' | 'import_file' | 'refresh_session' }
    Enqueued --> Executed: executePendingAction(shouldSaveFirst)
    Executed --> None: Action dispatched & reset to null
    Enqueued --> Discarded: Cancel clicked -> reverted without execution
    Discarded --> None: reset to null
```
