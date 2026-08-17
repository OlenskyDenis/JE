---
name: eel-desktop-bridge
description: >
  Architecture, IPC patterns, lifecycle quirks, and test strategies for the Python-Eel-JS desktop bridge in JE.
  Use when adding or modifying backend RPC endpoints, JavaScript Eel calls, desktop window management, or Playwright E2E browser automation.
---

# Eel Desktop Bridge & IPC Architecture Guide

> **Purpose:** Authoritative reference for the Python-Eel backend, WebSocket IPC, JavaScript client bindings, desktop lifecycle quirks, and Playwright test automation in the JE application.

---

## 1. Architecture Overview

JE is built as a lightweight hybrid desktop application:
* **Backend:** Python (`src/app/main.py`, `src/app/eel_bridge.py`) running Python business logic and services (`src/hierarchy_lib/`).
* **Frontend:** Vanilla HTML5 / CSS3 / ES6 JavaScript (`src/web/`) served via Eel's internal Bottle/gevent WebSocket server.
* **IPC Transport:** WebSocket-based RPC provided by the Eel library (`/eel.js`).

```mermaid
graph LR
    subgraph Frontend ["Frontend (src/web/)"]
        HTML["index.html"]
        JS["app.js / renderers"]
        EelClient["/eel.js (WebSocket client)"]
    end

    subgraph Backend ["Backend (src/app/)"]
        EelServer["Eel WebSocket Server"]
        Bridge["eel_bridge.py (@eel.expose)"]
        Services["src/hierarchy_lib/"]
    end

    JS -->|await eel.fn()()| EelClient
    EelClient <== WebSocket RPC ==> EelServer
    EelServer --> Bridge
    Bridge --> Services
```

---

## 2. Backend RPC Endpoints (`src/app/eel_bridge.py`)

### Exposing Python Functions
Decorate exposed functions with `@eel.expose`:

```python
import eel
from typing import Dict, Any, Optional

@eel.expose
def add_node(parent_id: Optional[str] = None, name: str = "", is_container: bool = True, ...) -> Dict[str, Any]:
    try:
        # 1. Validate inputs & fetch settings
        delim = SettingsService.get_delimiter()
        # 2. Execute business logic via Domain Services
        new_node = HierarchyNode(name)
        forest.add_root(new_node)
        # 3. Return structured Result DTO
        return {
            "success": True,
            "node": new_node.to_dict(delimiter=delim),
            "roots": forest.to_dict(delimiter=delim)["roots"]
        }
    except Exception as e:
        # Always return error object rather than raising uncaught exception over IPC
        return {"success": False, "error": str(e)}
```

### Invariants & Rules for Bridge Functions:
1. **Never raise uncaught exceptions:** Catch exceptions and return `{"success": False, "error": str(e)}`.
2. **Deterministic Return Format:** Always include `"success": True | False` as the primary status flag.
3. **State Management:** Mutate active session state (`forest`, `sheet_forests`, `current_active_sheet`) only within bridge handlers or dedicated session managers.
4. **Pure Python Fallback:** Maintain `os.environ.setdefault("PURE_PYTHON", "1")` at entry points to prevent gevent DLL conflicts on Windows.

---

## 3. Frontend Client Invocations (`src/web/js/`)

### Double Invocation Syntax `()()`
Eel wraps exposed Python functions in a factory that returns a Promise:

```javascript
// Correct syntax for async/await:
try {
    const res = await eel.open_file_dialog()();
    if (res && res.success) {
        console.log("Selected file:", res.file_path);
    } else if (res && res.error) {
        showToast(res.error, "error");
    }
} catch (err) {
    console.error("Eel IPC call failed:", err);
}
```

### Safe Fallback & Guarding
Always guard Eel calls against undefined `window.eel` in environments where Eel runtime might be loading or running in detached mock mode:

```javascript
if (typeof eel !== 'undefined' && typeof eel.get_settings === 'function') {
    const res = await eel.get_settings()();
    if (res && res.success) {
        this.settings = res.settings;
    }
}
```

---

## 4. Desktop Lifecycle & Windows Quirks

### 1. Dynamic / Ephemeral Ports (`port=0`)
To prevent "Port already in use" errors when launching multiple instances or during rapid restarts:
* In production/development (`src/app/main.py`):
  ```python
  eel.start("index.html", size=(1200, 800), port=0)
  ```
* `port=0` instructs the OS to allocate an available ephemeral port dynamically.

### 2. Auto-Shutdown on Disconnect
By default, Eel terminates the Python process when the browser window/tab closes.
* In automated testing, disable auto-shutdown to keep the server alive during test fixtures:
  ```python
  eel._detect_shutdown = lambda *args, **kwargs: None
  ```

### 3. Native File Dialogs (`FileDialogService`)
* File pickers (`open_file_dialog`, `save_file_dialog`) run in Python using native OS dialogs (e.g. Tkinter/win32) via `dialog_service.py`.
* Dialogs execute synchronously on the backend thread while frontend awaits the JSON result containing `{ "file_path": "...", "success": True }`.

---

## 5. Playwright E2E Test Strategy (`tests/e2e/`)

### Test Server Lifecycle (`conftest.py`)
1. **Find Free Port:** `get_free_port()` finds an available local TCP socket.
2. **Start Daemon Thread:** Starts `eel.start('index.html', mode=False, port=port, block=False)` in a background thread.
3. **Poll Until Listening:** `wait_for_server(port, timeout=6.0)` verifies connection readiness.
4. **Session-Scoped Fixture:** Yields `http://127.0.0.1:{port}/index.html` to Playwright `page` fixtures.

### Headless Page Interaction Pattern
```python
def test_add_root_node_e2e(page: Page, eel_server_url: str):
    page.goto(eel_server_url)
    page.wait_for_selector("#tree-content")
    
    # Click Add Root button
    page.click("#btn-add-root")
    page.wait_for_selector("#node-modal:not(.hidden)")
    
    # Fill form and submit
    page.fill("#modal-node-name", "Finance")
    page.click("#modal-btn-confirm")
    
    # Verify DOM update rendered from backend state
    page.wait_for_selector(".node-card")
    expect(page.locator(".node-card .node-title")).to_have_text("Finance")
```

---

## 6. Verification Checklist for Bridge Changes

- [ ] New Python function decorated with `@eel.expose`.
- [ ] Returns dict with `"success": True` or `"success": False, "error": "..."`.
- [ ] In JS, called with `await eel.function_name(...)()`.
- [ ] Unit/Integration test in `tests/integration/test_eel_bridge.py` covers success and error paths.
- [ ] E2E test in `tests/e2e/` verifies real UI interaction and DOM updates.
