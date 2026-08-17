

# Code Style & Project Conventions

> **Mandatory Policy:** Follow existing project conventions. Consistency within the codebase trumps personal preference.

## Python (Backend)

* **Naming:** `snake_case` for functions, methods, variables, and module files. `PascalCase` for classes. `UPPER_SNAKE_CASE` for module-level constants.
* **Type Hints:** Use `typing` annotations on all function signatures (`def foo(name: str) -> Dict[str, Any]:`). Use `Optional[T]` for nullable parameters.
* **Docstrings:** One-line `"""..."""` docstrings for all public classes and methods. Use imperative mood ("Returns…", "Adds…", "Validates…").
* **Imports:** Standard library → third-party → project modules (`src.*`). One import per line.
* **Module Files:** Each module file should have a top-level docstring describing its purpose.

## JavaScript (Frontend)

* **Pattern:** Singleton object-literal modules (`const App = { ... }`, `const DragDropHandler = { ... }`). No class-based or ES module patterns.
* **Naming:** `camelCase` for variables, functions, and object properties. `PascalCase` for module singletons (`App`, `I18n`, `TreeRenderer`).
* **DOM Access:** Cache DOM references in `bindDOM()` method. Use `document.getElementById()` for element access.
* **Eel Calls:** All `eel.*` calls are `async/await`. Always check `result.success` before processing.
* **File Scope:** Target ≤200 lines per logical concern. Split renderers into separate files (`tree_renderer.js`, `excel_block_renderer.js`).

## Eel Bridge Contract

* **Exposed functions:** Use `@eel.expose` decorator. Function name = JS callable name (`eel.add_node(...)` from JS).
* **Return format:** Always return `Dict[str, Any]` with `"success": True/False`. On failure, include `"error": str`. On success, include operation-specific data + `"roots"` for tree state sync.
* **No raw exceptions to frontend:** Wrap all bridge methods in `try/except Exception`, return error dict.

## Language Policy

* **Code identifiers:** English only (variable names, function names, classes, parameters).
* **Docstrings & code comments:** English.
* **UI-facing strings:** Managed via `i18n.js`. Never hardcode Ukrainian text in JS logic — use translation keys.
* **Spec documents & README:** Ukrainian.
* **Git commits:** English, prefixed with spec number or conventional type (see `Git.md`).
