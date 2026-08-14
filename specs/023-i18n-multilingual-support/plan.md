# Implementation Plan: Multilingual Localization System (Ukrainian & English)

**Feature Branch**: `023-i18n-multilingual-support`  
**Spec**: [specs/023-i18n-multilingual-support/spec.md](spec.md)  
**Created**: 2026-08-14  
**Status**: In Progress

---

## Technical Context & Architecture Overview

### Problem Statement
All user-facing interface copy, tooltips, placeholders, modals, toasts, and dynamic tree action hints are currently hardcoded in English. The application needs a standalone, zero-dependency localization engine with comprehensive Ukrainian (`uk`) and English (`en`) dictionary assets, persistent language preference, and instant runtime language toggling without page reloading or loss of workspace hierarchy state.

### Target Architecture & Strategy
1. **Centralized Localization Asset & Engine (`src/web/js/i18n.js`)**:
   - Self-contained vanilla JS module defining `I18N_DICTIONARIES` with full key parity between `uk` (Ukrainian) and `en` (English).
   - Global `I18n` singleton managing `currentLanguage`, `t(key, params)` interpolation, `setLanguage(lang)` persistence in `localStorage`, and `translateDOM()`.
2. **Declarative & Dynamic DOM Translation (`src/web/index.html`, `src/web/js/app.js`, `src/web/js/tree_renderer.js`)**:
   - Static elements annotated with `data-i18n="<key>"` and `data-i18n-attr="title:<key>;placeholder:<key>"`.
   - Dynamic renderers (`TreeRenderer.renderTree`, `TreeRenderer.renderPaths`, `app.js` toasts/modals/counters) call `I18n.t()` with active locale parameters.
3. **Toolbar Language Switcher Widget**:
   - Segmented toggle control `[ UA | EN ]` positioned in `.toolbar-actions` of `.app-header`.
   - Toggling immediately executes `I18n.setLanguage(lang)`, translating static DOM and re-rendering active tree views in-place without triggering network reload.
4. **Data Model Integrity**:
   - Internal node properties (such as canonical `data_type` values `"Text"`, `"Currency"`, `"Date"`, etc.) remain language-agnostic for openpyxl export and Excel interoperability, while display labels and dropdowns render localized names.

---

## Constitution & Principle Gates Checklist

| Constitution Principle | Evaluation | Status |
|---|---|---|
| **I. Spec-Driven Development (SDD)** | Spec and plan finalized prior to implementation; no untracked code edits. | 🟢 Passed |
| **II. OOP & SOLID Principles** | `I18n` module follows SRP for string resolution and localization lifecycle. | 🟢 Passed |
| **III. Gang of Four Design Patterns** | Observer/Subscriber pattern for language change events notifying UI renderers. | 🟢 Passed |
| **IV. Library-First & TDD** | Existing test suite and new Python integration/unit tests maintained at 100% pass rate. | 🟢 Passed |
| **V. Self-Contained Frontend Assets** | Vanilla JavaScript without external translation libraries or heavy dependencies. | 🟢 Passed |
| **VI. System Map & Architecture Hygiene** | Synchronized with [`.specify/system_map.md`](../../.specify/system_map.md). | 🟢 Passed |
| **VII. Red Teaming & Zero-Data Stress Testing** | Validated with empty states, missing keys fallback, and active modal language switches. | 🟢 Passed |

---

## Execution Phases & Artifacts

### Phase 0: Research & Dictionary Schema (`research.md`)
- Define full key catalog and translation mappings between `uk` and `en`.

### Phase 1: Data Model & Contracts (`data-model.md`, `quickstart.md`)
- Document `I18n` API contract, dictionary structure, and DOM translation schema.
- Detail automated and manual verification steps in `quickstart.md`.

### Phase 2: Core Localization Engine (`src/web/js/i18n.js`)
- Implement `I18n` module with `uk` and `en` dictionaries, `t()` token interpolation, `localStorage` persistence, and `translateDOM()`.

### Phase 3: HTML Layout & Toolbar Switcher (`src/web/index.html`, `src/web/css/style.css`)
- Embed `i18n.js` in `index.html`.
- Add `[ UA | EN ]` segmented toggle in `.toolbar-actions`.
- Annotate static HTML elements with `data-i18n` and `data-i18n-attr`.
- Style `.lang-switcher` and `.lang-btn` in `style.css`.

### Phase 4: Dynamic UI & Renderer Integration (`src/web/js/app.js`, `src/web/js/tree_renderer.js`, `src/web/js/drag_drop.js`)
- Update `TreeRenderer` to use `I18n.t()` for chevrons, drag handles, action tooltips, type badges, and empty states.
- Update `app.js` to use `I18n.t()` for all toasts, modals, confirmation dialogs, counter badges, dropdown options, and dual sheet selector combined headers.
- Update `drag_drop.js` to use localized toast callbacks.

### Phase 5: Verification & System Map Synchronization
- Update `.specify/system_map.md`.
- Run full pytest test suite (62+ tests).
