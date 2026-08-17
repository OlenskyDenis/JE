# Technical Research: Full-Project Comprehensive Automated Test Suite & Multi-Layer Behavioral Verification

**Feature**: 034-full-project-test-suite  
**Date**: 2026-08-17  

---

## 1. Playwright Locator Visibility & Interaction Patterns

### Decision:
Enforce `expect(page.locator(...)).to_be_visible()` and `expect(page.locator(...)).to_be_enabled()` across all E2E browser interactions. Never rely on `to_have_count()` without asserting visibility on the resulting element collection.

### Rationale:
In modern web applications, elements placed inside containers with `.hidden` or `display: none` remain part of the DOM tree. Asserting counts passes false-positive checks even if elements are completely hidden from the user. Using `to_be_visible()` guarantees true pixel-level rendering and viewport accessibility.

### Alternatives Considered:
- Checking `inner_html` or element text: Only tests string presence, not CSS display state.
- Custom JavaScript evaluate queries: Verbose and prone to missing CSS cascade nuances.

---

## 2. Multi-Sheet Session Testing Isolation

### Decision:
Reset `eel_bridge.sheet_forests`, `eel_bridge.current_active_sheet`, and `SettingsService` inside `conftest.py` before each test execution, and run tests against an ephemeral server on a dynamic port (`get_free_port()`).

### Rationale:
Guarantees zero cross-test state leakage, prevents test order dependencies, and ensures clean reproducible test runs both locally on Windows and in CI runners.

---

## 3. Pure Real-User Interaction (Zero DOM Bypasses)

### Decision:
Prohibit synthetic DOM property manipulation (e.g. `el.disabled = false` or manual class toggling via evaluate) inside tests. All UI state changes must be triggered by actual user interactions (clicking buttons, importing files, selecting dropdown options, dragging elements).

### Rationale:
Synthetic bypasses hide bugs in the application controller logic. If an element should become active, the production code must make it active when prerequisites are satisfied.
