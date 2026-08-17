---
name: testing-standards
description: >
  Detailed testing standards, patterns, and verification guidelines.
  Use when writing, reviewing, or discussing tests for any part of the codebase.
---

# Testing Standards, Patterns & Verification

> **Policy:** Testing must validate actual system behavior without introducing brittle, speculative test scaffolding. Tests are first-class production code.

## Core Directives

* **FIRST Principles:** Ensure all tests are Fast, Independent, Repeatable in any environment, Self-validating (pass/fail without manual inspection), and Timely.
* **AAA Structure (Arrange-Act-Assert):** Structure every test clearly into three distinct phases: prepare input state, trigger the action, and verify expected outcomes.
* **Test Behavior, Not Implementation:** Assert on public interfaces, observable outputs, and state changes. Never test private methods or internal execution details that break during safe refactoring.
* **YAGNI in Testing:** Write tests only for existing features and identified edge cases. Avoid generating sprawling test suites for hypothetical inputs or unused parameters.
* **Deterministic & Flake-Free:** Eliminate dependencies on real-time clocks, random seeds, fixed sleep delays, or live network calls. Use deterministic mocks, fake timers, and isolated fixtures.
* **Failure Clarity:** Write descriptive test names and assertion failure messages that pinpoint the root cause immediately without debugging.
* **Visual Visibility over DOM Presence (UI/E2E):** In Playwright/browser tests, never rely solely on `to_have_count(N)`. Assert actual visibility via `expect(locator).to_be_visible()` to catch hidden/`display: none` container bugs.
* **Zero Synthetic Test Bypasses:** Never manually mutate element properties inside tests (e.g. `el.disabled = false`). Test real production activation flows.

## Test Structure Template

```
describe('[Unit/Feature under test]', () => {
  it('[should + expected behavior + given condition]', () => {
    // Arrange — prepare state, inputs, mocks
    // Act     — invoke the unit
    // Assert  — verify observable outcome
  });
});
```

## What to Test

| ✅ Test | ❌ Do Not Test |
|---|---|
| Public API contracts | Private methods |
| State transitions | Internal implementation details |
| Error paths & edge cases | Getters/setters with no logic |
| Integration boundaries | Framework internals |

## Mocking Guidelines

* Mock **only** external dependencies (network, DB, filesystem, clock).
* Never mock the unit under test itself.
* Prefer fakes and in-memory implementations over complex mock frameworks when possible.

---

## JE Test Execution Recipes (Windows PowerShell)

### 1. Fast Backend Suite (Unit + Integration)
Run all backend model, service, adapter, and Eel bridge tests:
```powershell
python -m pytest tests/unit tests/integration -v
```

### 2. Playwright E2E Test Suite (Frontend + RPC)
Run all full-stack browser E2E test modules headlessly:
```powershell
python -m pytest tests/e2e/ -v
```

Run an individual E2E test module with a visible browser for debugging:
```powershell
python -m pytest tests/e2e/test_navigation_and_i18n.py --headed -v
```

### 3. Complete Test Suite
Run the entire testing pyramid (unit, integration, and e2e):
```powershell
python -m pytest
```

