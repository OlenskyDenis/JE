# Feature Specification: Multilingual Localization System (Ukrainian & English)

**Feature Branch**: `023-i18n-multilingual-support`  
**Created**: 2026-08-14  
**Status**: Draft  
**Input**: User directive: "Додай можливість перемикатись між мовами, Українська та Англійська, весь текст і опис перекладється, зробисистему та файл залежностей де будуть зберагатись переклади елементів інтерфейсу"

---

## Clarifications

### Session 2026-08-14
- Q: What should be the default language on first launch, and which switcher style do you prefer? → A: Ukrainian (`uk`) as default with quick toggle button `[ UA | EN ]` in top toolbar.

---

## Problem Statement & Context

The application currently has hardcoded English UI strings across HTML layouts, JavaScript controllers, dynamic tree renderers, modal dialogs, and toast notifications. Ukrainian-speaking users and international teams require full bilingual support (Ukrainian `uk` and English `en`) with seamless runtime switching, persistent language preferences, and a clean, modular translation dictionary architecture.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Instant Runtime Language Switching (Priority: P1) 🎯 MVP

As a user of the Database Hierarchy Creator, I want to switch the application language between Ukrainian and English at any time using a language selector in the top toolbar, so that all interface text, toolbar actions, sidebar labels, tab names, empty states, and descriptions immediately update without reloading the page or losing current workspace edits.

**Why this priority**: Core user journey providing accessibility and localization for Ukrainian and English users.

**Independent Test**:
1. Open the application (default language loaded).
2. Click the language switcher in the toolbar to toggle between `UA` and `EN`.
3. Verify that all visible labels (Brand, Toolbar buttons, Workspace title, Sheet selector, Sidebar tabs, Catalog search placeholder, Empty states, Modal labels) switch to the selected language instantly.
4. Verify current in-memory workspace tree and unsaved edits are 100% preserved during the switch.

**Acceptance Scenarios**:
1. **Given** the app is in English (`en`), **When** the user selects Ukrainian (`uk`), **Then** all static and dynamic UI elements display correct Ukrainian translations.
2. **Given** the app is in Ukrainian (`uk`), **When** the user selects English (`en`), **Then** all UI elements display correct English translations.
3. **Given** an active workspace session with an imported file and modified nodes, **When** switching languages, **Then** all node names and hierarchy structures remain intact while all system UI labels, tooltips, and badges translate.

---

### User Story 2 - Comprehensive Translation Dictionary & System (Priority: P2)

As a developer and maintainer, I want all user-facing translation strings to be organized in a centralized, structured localization asset file (`src/web/js/i18n.js` / dictionary registry), so that adding new strings or modifying existing translations is maintainable and decoupled from UI logic.

**Why this priority**: Architectural hygiene, maintainability, and extensibility for new strings and languages.

**Independent Test**:
- Inspect translation dictionary file; verify 100% key parity between `uk` and `en` catalogs.
- Call translation lookup `I18n.t(key, params)` for parameterized strings (e.g. counter badges, modal messages); verify correct placeholder substitution.

**Acceptance Scenarios**:
1. **Given** the localization system `I18n`, **When** `I18n.t("key")` is invoked, **Then** it returns the corresponding translation for the active language with a fallback to English if a key is missing.
2. **Given** parameterized keys (e.g. `node_count`, `unsaved_switch_msg`), **When** parameters are supplied, **Then** placeholders like `{count}`, `{sheet}`, `{template}` are interpolated accurately.

---

### User Story 3 - Dynamic Tooltips, Modals, Toasts & Confirmation Localization (Priority: P3)

As a user interacting with tree nodes, modals, and notifications, I want all tooltips, modal dialogs, toast messages, data type dropdown options, and delete confirmations to appear in my selected language.

**Why this priority**: Eliminates residual untranslated English strings and guarantees complete immersion.

**Independent Test**:
1. Switch to Ukrainian (`uk`).
2. Hover over buttons (e.g., Expand All, Collapse All, Edit Node, Delete Node); verify tooltips are in Ukrainian.
3. Open Node Edit modal; verify modal title, field labels, data type dropdown options, and help text are in Ukrainian.
4. Trigger an action (e.g., import file, add node, refresh, delete node); verify toast messages and confirmation dialogs appear in Ukrainian.

**Acceptance Scenarios**:
1. **Given** active language is `uk`, **When** deleting a node, **Then** the confirmation prompt displays `"Ви впевнені, що хочете видалити цей вузол та весь його вміст?"`.
2. **Given** active language is `uk`, **When** viewing the data type selector in the node modal, **Then** options display localized labels (e.g. `"Текст (Рядок)"`, `"Ціле число"`, `"Валюта ($#,##0.00)"`, `"Дата (РРРР-ММ-ДД)"`).
3. **Given** active language is `uk`, **When** hovering over the drag handle or action buttons, **Then** title attributes display Ukrainian tooltips.

---

### User Story 4 - Language Preference Persistence (Priority: P4)

As a user who reopens the desktop application, I want my selected language preference to be remembered across app launches and page refreshes, so that I don't have to re-select my language every time.

**Why this priority**: Seamless user experience and convenience.

**Independent Test**:
1. Select Ukrainian (`uk`).
2. Refresh or restart the application.
3. Verify the application loads directly in Ukrainian.

**Acceptance Scenarios**:
1. **Given** a saved preference in `localStorage.getItem('app_language')`, **When** the application boots, **Then** it initializes with the stored language (defaulting to Ukrainian `uk` or browser preference if unset).
2. **Given** the user toggles language, **When** new language is chosen, **Then** `localStorage` is updated immediately.

---

## Edge Cases

- **Missing translation key**: Fallback to English key value without breaking layout or showing `undefined`.
- **Dynamic pluralization / counters**: Handles Ukrainian plural forms or clear unified counter formats (e.g. `"12 Вузлів"` / `"12 Nodes"`).
- **Active modal open during language switch**: Dynamically re-translates open modal titles and buttons.
- **Data type preservation**: Switching languages does NOT alter the underlying node `data_type` string value sent to/from the backend (`"Text"`, `"Currency"`, etc.), only localized display labels.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Application MUST include a centralized localization module [`src/web/js/i18n.js`](file:///E:/JE/src/web/js/i18n.js) containing comprehensive translation dictionaries for Ukrainian (`uk`) and English (`en`).
- **FR-002**: Application MUST provide a language switcher UI in the top header toolbar allowing one-click toggling between Ukrainian (`UA`) and English (`EN`).
- **FR-003**: The localization system MUST translate all static DOM elements via declarative `data-i18n` and `data-i18n-attr` (for `title`, `placeholder`) attributes upon language switch.
- **FR-004**: The dynamic tree renderer (`TreeRenderer`), application controller (`app.js`), and drag-and-drop handler (`drag_drop.js`) MUST use `I18n.t()` for all dynamically generated text, tooltips, counters, and badges.
- **FR-005**: All modals (Create/Edit Node Modal, Unsaved Changes Modal) MUST dynamically translate all titles, messages, button labels, dropdown options, and help text.
- **FR-006**: All toast notifications and confirmation dialogs MUST display localized messages in the active language.
- **FR-007**: Selected language MUST be persisted in `localStorage` under `app_language` and restored on application startup.
- **FR-008**: Switching languages MUST preserve all current workspace tree nodes, active sheet selection, and unsaved state without page reloads or backend state loss.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of visible UI elements, tooltips, placeholders, modal dialogs, and toast messages are translated in both Ukrainian (`uk`) and English (`en`).
- **SC-002**: Language switching occurs instantaneously (< 50ms) with zero DOM flickering and zero lost canvas modifications.
- **SC-003**: Zero hardcoded user-facing English strings remaining in JavaScript alert/confirm/toast/renderer routines.
- **SC-004**: 100% pass rate across automated unit and integration tests.

---

## Assumptions

- The backend data model continues using canonical English identifiers for node `data_type` (`"Text"`, `"Currency"`, `"Date"`, etc.) and sheet names to maintain Excel and schema interoperability; translation applies to the user-facing presentation layer.
- Ukrainian (`uk`) and English (`en`) are the initial supported languages, with architecture designed for easy addition of future locales.
