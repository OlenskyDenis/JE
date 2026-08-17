# Рівень Б: Наскрізна Sequence-діаграма модального вікна вузла (Node Modal Full-Stack Sequence)

> **Призначення**: Повний життєвий цикл створення кореневого вузла, додавання нащадка, перейменування та валідації між Frontend та Backend.

---

```mermaid
sequenceDiagram
    autonumber
    actor User as 👤 Користувач
    participant TreeUI as 🌳 TreeCanvas / Header
    participant ModalMgr as 🪟 ModalManager
    participant Modal as 📝 #nodeModal
    participant RPC as ⚡ Eel Bridge (eel_bridge.py)
    participant NodeCtrl as 🎯 NodeController
    participant Forest as 🌲 WorkspaceForest
    participant TreeRend as 🖼️ TreeRenderer

    %% СЦЕНАРІЙ 1: Створення кореневого вузла
    Note over User, Forest: СЦЕНАРІЙ 1: Створення кореневого вузла (Root Node)
    User ->> TreeUI: Клік на #btnAddRootHeader або #btnCreateRootEmpty
    TreeUI ->> ModalMgr: promptAddRoot()
    ModalMgr ->> Modal: ModalContainerLifecycle.Open("Створити вузол", empty name)
    Modal -->> User: Вікно відкрито, фокус на #inputNodeName
    User ->> Modal: Введення "Departments" та вибір типу "Text"
    User ->> Modal: Клік на #btnModalSubmit
    Modal ->> ModalMgr: submit() -> валідація non-empty
    ModalMgr ->> RPC: eel.add_node(name="Departments", data_type="Text")()
    RPC ->> NodeCtrl: NodeController.add_node(forest, name="Departments")
    NodeCtrl ->> Forest: forest.add_node(HierarchyNode("Departments"))
    Forest -->> NodeCtrl: updated roots
    NodeCtrl -->> RPC: {"success": true, "roots": [...]}
    RPC -->> ModalMgr: {"success": true, "roots": [...]}
    ModalMgr ->> TreeRend: App.updateUI(roots)
    TreeRend ->> TreeUI: Рендеринг картки кореневого вузла
    ModalMgr ->> Modal: ModalContainerLifecycle.Close (class .hidden)

    %% СЦЕНАРІЙ 2: Додавання дочірнього вузла (Child Nesting)
    Note over User, Forest: СЦЕНАРІЙ 2: Додавання дочірнього вузла
    User ->> TreeUI: Клік на кнопку [+] на картці "Departments"
    TreeUI ->> ModalMgr: promptAddChild("dep_id_123")
    ModalMgr ->> Modal: Open("Створити дочірній вузол")
    User ->> Modal: Введення "HR" + тип "Text" + Submit
    ModalMgr ->> RPC: eel.add_node(parent_id="dep_id_123", name="HR")()
    RPC ->> NodeCtrl: NodeController.add_node(parent_id="dep_id_123", name="HR")
    NodeCtrl ->> Forest: parent.add_child(HierarchyNode("HR"))
    Forest -->> NodeCtrl: updated forest
    NodeCtrl -->> RPC: {"success": true, "roots": [...]}
    RPC -->> ModalMgr: updateUI(roots)
    ModalMgr ->> TreeRend: Рендеринг (Departments стає папкою з шевроном, HR — нащадком)

    %% СЦЕНАРІЙ 3: Перейменування та зміна типу даних
    Note over User, Forest: СЦЕНАРІЙ 3: Перейменування вузла та оновлення типу
    User ->> TreeUI: Подвійний клік на вузол або кнопка ✏️ (.rename-node)
    TreeUI ->> ModalMgr: promptRename("node_id_456")
    ModalMgr ->> Modal: Open("Редагувати вузол", prefill "Price", type "Decimal")
    User ->> Modal: Зміна імені на "TotalAmount", тип на "Currency" + Submit
    ModalMgr ->> RPC: eel.update_node(node_id="node_id_456", name="TotalAmount", data_type="Currency")()
    RPC ->> NodeCtrl: NodeController.update_node(...)
    NodeCtrl ->> Forest: node.name = "TotalAmount", node.data_type = "Currency"
    RPC -->> ModalMgr: {"success": true, "roots": [...]}
    ModalMgr ->> TreeRend: updateUI(roots)
    TreeRend ->> TreeUI: Оновлена назва картки та бейдж "Валюта"
```
