# Test Suite Contracts & Invariants

**Feature**: 034-full-project-test-suite  
**Date**: 2026-08-17  

---

## 1. Playwright E2E Test Invariants

1. **Visibility Contract**:
   Every element asserted to exist after a user action MUST use `expect(locator).to_be_visible()`.
2. **Enabled Contract**:
   Every interactive input, button, or select element MUST use `expect(locator).to_be_enabled()`.
3. **No Synthetic Mutation Contract**:
   Tests MUST NOT invoke `el.disabled = false`, `el.classList.remove('hidden')`, or synthetic property mutators via `page.evaluate()` to make a test pass.
4. **Isolated State Contract**:
   Tests MUST NOT assume pre-existing state from earlier tests. All state must be created through explicit actions or isolated fixtures.

---

## 2. Unit & Integration Test Invariants

1. **Pure Domain Contract**:
   Tests under `tests/unit/` must never depend on a running web server, Eel, or network sockets.
2. **Deterministic Fixture Contract**:
   All Excel tests must use standard fixtures from `tests/fixtures/excel_samples/`.
3. **Principle VIII Invariant**:
   `test_file_line_count_thresholds()` in `test_architecture_contracts.py` must assert that every non-exempt source file has $\le 200$ lines.
