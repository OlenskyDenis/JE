# Відповідність проекту JE принципам OOP та SOLID

**Дата аналізу**: 2026-08-16  
**Scope**: весь бекенд (`src/hierarchy_lib/`, `src/app/eel_bridge.py`)  
**Оцінки**: ✅ Відповідає | ⚠️ Частково | ❌ Порушення

---

## Загальна оцінка

| Принцип | Оцінка | Коментар |
|---|---|---|
| **OOP — Encapsulation** | ✅ | Стан вузла захищений через методи |
| **OOP — Abstraction** | ⚠️ | `HierarchyComponent` є, але не використовується |
| **OOP — Inheritance** | ❌ | Оголошена але не реалізована — `HierarchyNode` не успадковує `HierarchyComponent` |
| **OOP — Polymorphism** | ⚠️ | Є через `to_dict()`, але без справжньої ієрархії типів |
| **S — SRP** | ⚠️ | `HierarchyNode` і `eel_bridge.py` мають зайві обов'язки |
| **O — OCP** | ⚠️ | Типи даних — hardcoded tuple; `eel_bridge.py` — монолітний |
| **L — LSP** | ❌ | `HierarchyNode` заявляє `HierarchyComponent` як базу в system_map, але не успадковує її |
| **I — ISP** | ⚠️ | `HierarchyComponent` нав'язує `to_dict()` всім, але не всі клієнти його потребують |
| **D — DIP** | ❌ | `HierarchyNode` напряму залежить від конкретного `SettingsService` |

---

## OOP: Детальний аналіз

### ✅ Encapsulation (Інкапсуляція)

[`HierarchyNode`](file:///e:/JE/src/hierarchy_lib/models/node.py) добре інкапсулює стан:

```python
def add_child(self, child, index=None):      # контрольований доступ
def remove_child(self, child_id):            # зміна через метод
def set_data_type(self, data_type):          # валідація при записі
def rename(self, new_name):                  # захист від пустого рядка
```

`SettingsService` теж добре інкапсульований — стан `_active_settings` зберігається як приватний атрибут класу, доступний лише через методи.

**Проблема**: `children: List[HierarchyNode]` — публічне поле. Клієнти можуть напряму робити `node.children.append(...)` в обхід `add_child()` і його валідації циклів:

```python
# eel_bridge.py L106 — читає children напряму, це безпечно
# але нічого не заважає зовнішньому коду:
node.children.append(bad_child)  # цикл не перевірено!
```

---

### ❌ Inheritance (Успадкування) — КРИТИЧНЕ ПОРУШЕННЯ

**Задеклароване у `base.py`**:
```python
class HierarchyComponent(ABC):
    @abstractmethod
    def is_container(self) -> bool: ...
    @abstractmethod
    def to_dict(self) -> Dict: ...
```

**Реалізоване у `node.py`**:
```python
class HierarchyNode:       # ← НЕ успадковує HierarchyComponent!
    def is_container(self) -> bool: ...
    def to_dict(self) -> Dict: ...
```

`HierarchyNode` реалізує той самий контракт що і `HierarchyComponent`, але **не оголошує її як базовий клас**. Це означає:
- Python не перевіряє відповідність контракту через ABC-механізм
- `isinstance(node, HierarchyComponent)` повертає `False`
- Абстракція існує лише на рівні документа, але не на рівні мови

---

### ⚠️ Abstraction (Абстракція)

[`HierarchyComponent`](file:///e:/JE/src/hierarchy_lib/models/base.py) правильно визначена як `ABC` з `@abstractmethod`. Але оскільки `HierarchyNode` не успадковує її — абстракція не працює за призначенням.

[`WorkspaceForest`](file:///e:/JE/src/hierarchy_lib/services/forest.py) не має абстрактного інтерфейсу — він є єдиною конкретною реалізацією контейнера для дерев, без можливості підміни.

---

### ⚠️ Polymorphism (Поліморфізм)

Поліморфізм частково реалізований через `to_dict()` — `WorkspaceForest.to_dict()` рекурсивно викликає `node.to_dict()` для всіх вузлів. Це правильна реалізація Composite Pattern.

Але поліморфізм **не підкріплений типовою системою** — немає спільного базового типу між `WorkspaceForest` і `HierarchyNode`, хоча обидва мають `to_dict()`.

---

## SOLID: Детальний аналіз

### ⚠️ S — Single Responsibility Principle

#### [`HierarchyNode`](file:///e:/JE/src/hierarchy_lib/models/node.py) — 4 обов'язки в одному класі:

| Обов'язок | Методи |
|---|---|
| Управління деревом (структура) | `add_child`, `remove_child`, `find_node_recursive` |
| Валідація бізнес-логіки | `validate_data_type`, `sanitize_name`, `is_ancestor_of` |
| Серіалізація в DTO | `to_dict` |
| **Обчислення шляху** з читанням зовнішнього сервісу | `get_absolute_path` → `SettingsService.get_delimiter()` |

`get_absolute_path()` порушує SRP: вузол сам читає глобальний сервіс налаштувань. Краще передавати delimiter ззовні завжди.

#### [`eel_bridge.py`](file:///e:/JE/src/app/eel_bridge.py) — монолітний модуль:

Містить **556 рядків** і виконує:
- RPC dispatching (expose/unwrap)
- Валідацію вхідних параметрів
- Бізнес-логіку (session management, multi-sheet logic)  
- DTO mapping (leaf_meta, headers_meta)
- Error handling

За SRP це має бути розбито на: `RpcController`, `SessionManager`, `SheetOrchestrator`. Але для проекту такого масштабу — прийнятний компроміс.

#### [`SettingsService`](file:///e:/JE/src/hierarchy_lib/services/settings_service.py) — ✅ чисто:

Відповідає SRP — тільки одна відповідальність: управління налаштуваннями з persistence.

---

### ⚠️ O — Open/Closed Principle

#### Типи даних — hardcoded tuple:

```python
# node.py:15 і settings_service.py:15 — одна й та ж константа в двох місцях
VALID_DATA_TYPES = ("Text", "Integer", "Decimal", "Currency", ...)
```

Щоб додати новий тип (наприклад `"JSON"`), треба **редагувати обидва класи** — порушення OCP. Немає реєстру або спільного джерела правди для типів.

#### `eel_bridge.py` — відкрита структура:

Додавання нового RPC endpoint вимагає просто нової `@eel.expose` функції — не змінює існуючих. Це ✅ відповідає OCP.

---

### ❌ L — Liskov Substitution Principle

Класичний LSP-контракт: якщо `B` успадковує `A`, то `B` може замінити `A` скрізь де використовується `A`.

**Проблема**: `HierarchyNode` **не успадковує** `HierarchyComponent`, хоча `PathGenerator.calculate_path()` приймає `HierarchyComponent` у type-hint:

```python
# path_generator.py:13
def calculate_path(component: HierarchyComponent, ...) -> str:
    return component.get_absolute_path(delimiter=delim)
```

На практиці сюди передається `HierarchyNode`. Python це дозволяє (duck typing), але:
- type-checker (mypy) видасть помилку
- LSP формально порушений — підстановка не задекларована через успадкування

**Додаткове порушення LSP** у `delete_node()`:
```python
# eel_bridge.py:140
if isinstance(node.parent, CompositeNode):  # завжди True бо CompositeNode = HierarchyNode
    node.parent.remove_child(node.id)
```

`isinstance(x, CompositeNode)` є псевдо-перевіркою — `CompositeNode` це alias для `HierarchyNode`, тому перевірка завжди `True` для будь-якого вузла. Логіка некоректна — якщо `node.parent` існує, `remove_child` треба викликати завжди.

---

### ⚠️ I — Interface Segregation Principle

[`HierarchyComponent`](file:///e:/JE/src/hierarchy_lib/models/base.py) визначає два абстрактних методи: `is_container` та `to_dict`. Це мінімальний інтерфейс — не перевантажений.

**Проблема**: `PathGenerator.calculate_path()` приймає `HierarchyComponent` і лише викликає `get_absolute_path()`. Але `get_absolute_path()` — **конкретний метод** у `HierarchyComponent`, а не абстрактний. Клієнт отримує більше, ніж потрібно — `to_dict()` і `is_container` у контракті для функції, якій потрібен лише `get_absolute_path`.

**Порушення в `i18n.js`**: `window.I18N_DICTIONARIES` та `getTypeBadgeLabel()` — публічний інтерфейс ширший за реальні потреби споживачів (ISP у JS-контексті).

---

### ❌ D — Dependency Inversion Principle

**Найсерйозніше порушення проекту**:

```python
# node.py:121 — HIGH-LEVEL MODEL залежить від CONCRETE SERVICE
def get_absolute_path(self, delimiter=None):
    delim = delimiter if delimiter is not None else SettingsService.get_delimiter()
    #                                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #                          пряма залежність від конкретного класу, не від абстракції
```

`HierarchyNode` (доменна модель, нижній рівень) напряму імпортує і викликає `SettingsService` (інфраструктурний сервіс). За DIP — має бути навпаки: `SettingsService` має залежати від абстракції, а `HierarchyNode` не повинен знати про існування сервісу.

**Правильний підхід (DIP)**:
```python
# delimiter завжди передається ззовні — модель нічого не знає про SettingsService
def get_absolute_path(self, delimiter: str = "\\") -> str:
    ...
# Хто знає про SettingsService? WorkspaceForest або eel_bridge.py
```

Аналогічно у [`WorkspaceForest`](file:///e:/JE/src/hierarchy_lib/services/forest.py):
```python
# forest.py:102 — сервісний шар теж напряму залежить від SettingsService
delim = delimiter if delimiter is not None else SettingsService.get_delimiter()
```

---

## Підсумкова таблиця

| Компонент | SRP | OCP | LSP | ISP | DIP |
|---|---|---|---|---|---|
| `HierarchyNode` | ⚠️ | ✅ | ❌ | ✅ | ❌ |
| `HierarchyComponent` | ✅ | ✅ | — | ⚠️ | ✅ |
| `WorkspaceForest` | ✅ | ✅ | ✅ | ✅ | ❌ |
| `PathGenerator` | ✅ | ✅ | ❌ | ⚠️ | ⚠️ |
| `PathParserService` | ✅ | ✅ | ✅ | ✅ | ❌ |
| `HeaderService` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `SettingsService` | ✅ | ⚠️ | ✅ | ✅ | ✅ |
| `ExcelHierarchyAdapter` | ⚠️ | ✅ | ✅ | ✅ | ✅ |
| `eel_bridge.py` | ❌ | ✅ | ✅ | ✅ | ⚠️ |

---

## Критичні рекомендації (пріоритет)

### 🔴 P1 — Виправити LSP: зробити `HierarchyNode` підкласом `HierarchyComponent`

```python
# node.py — замість:
class HierarchyNode:
# має бути:
class HierarchyNode(HierarchyComponent):
```

Або — видалити `HierarchyComponent` і використовувати `Protocol` (structural subtyping).

### 🔴 P1 — Виправити DIP: прибрати `SettingsService` з `HierarchyNode`

`get_absolute_path` та `to_dict` мають вимагати `delimiter` обов'язково, а не тягнути його з глобального сервісу.

### 🟡 P2 — Виправити баг у `delete_node()`: зайвий `isinstance(CompositeNode)`

```python
# Замість:
if isinstance(node.parent, CompositeNode):
    node.parent.remove_child(node.id)
# Має бути просто:
node.parent.remove_child(node.id)
```

### 🟡 P2 — Об'єднати `VALID_DATA_TYPES` в одне місце

Зараз дублюється в `HierarchyNode` і `SettingsService`. Винести в окремий модуль `constants.py` або `data_types.py`.

### 🟢 P3 — Захистити `children` від прямого доступу

Зробити `_children: List[HierarchyNode]` і надати read-only property `children`.
