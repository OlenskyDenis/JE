# Рівень А: Атомарні мікро-цикли елементів (Node Modal Micro-Lifecycles)

> **Призначення**: Автомати станів для окремих елементів модального вікна створення/редагування вузла (`#nodeModal`).

---

## 1. `ModalContainerLifecycle` (Життєвий цикл контейнера модалки)

Застосовується до: `#nodeModal`.

```mermaid
stateDiagram-v2
    [*] --> ClosedHidden: class "modal-overlay hidden"
    ClosedHidden --> OpeningCreateRoot: ModalManager.promptAddRoot()
    ClosedHidden --> OpeningAddChild: ModalManager.promptAddChild(parentId)
    ClosedHidden --> OpeningRename: ModalManager.promptRename(nodeId)
    OpeningCreateRoot --> OpenVisible: Title "Створити вузол", Type select visible
    OpeningAddChild --> OpenVisible: Title "Створити дочірній вузол", Type select visible
    OpeningRename --> OpenVisible: Title "Редагувати вузол", Name pre-filled
    OpenVisible --> Validating: User types name
    Validating --> Submitting: Click "#btnModalSubmit"
    Validating --> Dismissing: Click "#btnModalCancel" / "#modalClose"
    Submitting --> ClosedHidden: Success (RPC done) + add "hidden"
    Dismissing --> ClosedHidden: Add "hidden" without changes
```

---

## 2. `NameInputValidationLifecycle` (Життєвий цикл валідації назви)

Застосовується до: `#inputNodeName`.

```mermaid
stateDiagram-v2
    [*] --> EmptyOrPrefilled: Input mounted
    EmptyOrPrefilled --> Focused: Auto-focus on modal open
    Focused --> Typing: User inputs character string
    Typing --> Validating: Trim whitespace
    Validating --> EmptyError: If string is empty ("") -> Border red / Toast error
    Validating --> ValidName: If non-empty -> Ready for submit
    EmptyError --> Typing: User enters valid character
    ValidName --> Submitted: Enter key / Submit button click
```

---

## 3. `TypeSelectLifecycle` (Життєвий цикл вибору типу даних)

Застосовується до: `#selectNodeType`.

```mermaid
stateDiagram-v2
    [*] --> InitialType: Pre-selected with node's current type or default type
    InitialType --> HiddenForFolders: If parent node is a container with children
    InitialType --> VisibleForLeaves: If leaf node
    VisibleForLeaves --> OptionSelected: User selects from 9 data types
    OptionSelected --> Dispatched: Captured in payload on submit
```

---

## 4. `SubmitButtonLifecycle` (Життєвий цикл кнопки збереження)

Застосовується до: `#btnModalSubmit`.

```mermaid
stateDiagram-v2
    [*] --> Ready: Enabled button
    Ready --> Clicked: User clicks / presses Enter
    Clicked --> DispatchingRPC: Calls NodeController via eel_bridge
    DispatchingRPC --> SuccessDone: Tree updated + Modal closed
    DispatchingRPC --> ErrorShown: Backend returns {"success": false} -> Toast error
```
