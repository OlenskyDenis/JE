# Feature Specification: Settings Menu for Path Delimiter and Default Data Type Configuration

**Feature Branch**: `026-settings-menu-config`  
**Created**: 2026-08-16  
**Status**: Draft  
**Input**: User description: "Додай меню налаштувань. В налаштуванях можна змінювати символ розподілу, по замовчувані \\. В налаштуванях можна змінювати тип даних по замовчувані це дані тип яких явно не вказаний в ексель і стоїть загальний, по замочувані текст."

---

## Clarifications

### Session 2026-08-16
- **Q: Де саме в інтерфейсі розмістити кнопку відкриття налаштувань?**  
  → **A**: Кнопка з іконкою шестерні (`#btnSettings`) у верхній панелі інструментів (`.toolbar-actions`) поруч із перемикачем мов (`UA/EN`).
- **Q: Як реагувати на зміну символу розподілу, якщо дерево вже завантажене?**  
  → **A**: Миттєво динамічно перераховувати й оновлювати всі відображувані шляхи у дереві вузлів, бейджах шляхів та вкладці попереднього перегляду без перезавантаження файлу.
- **Q: Де зберігати налаштування користувача між перезапусками?**  
  → **A**: Подвійне збереження: у `localStorage` браузера (для швидкого відновлення клієнтського стану) та у локальному конфігураційному файлі `settings.json` на бекенді (для збереження між запусками Python).

---

## 1. Problem Statement & Objectives

### Problem
Currently, the application has hardcoded configuration values across backend services and frontend rendering:
1. **Path Delimiter**: Hardcoded to backslash (`\`) in `HierarchyNode.get_absolute_path()`, `PathParserService.parse_header_paths()`, and path badge rendering. Users cannot customize the path separator (e.g., using forward slash `/`, pipe `|`, double colon `::`, or dot `.`) when structuring their database hierarchies or exporting paths to Excel.
2. **Default Excel Data Type**: Columns in Excel with unassigned or "General" number formats (or empty formats) are hardcoded to default to `"Text"` during import. Users frequently working with numeric or date data cannot change this default baseline behavior to match their database conventions.
3. **Lack of Centralized Settings UI**: There is no accessible Settings dialog or toolbar menu for managing user preferences and workspace defaults.

### Objectives
1. Add a dedicated **Settings Menu / Modal** (`#settingsModal`) accessible from the top header toolbar via a gear icon button (`#btnSettings`).
2. Provide a setting to configure the **Path Delimiter** (default: `\`), with validation (non-empty string, 1–3 characters) and instant recalculation across the active tree canvas, path preview list, and Excel import/export services.
3. Provide a setting to configure the **Default Data Type for General/Unassigned Columns** (default: `Text`), selectable from the 9 supported Excel types (`Text`, `Integer`, `Decimal`, `Currency`, `Percentage`, `Date`, `Time`, `DateTime`, `Boolean`).
4. Persist settings across sessions via `localStorage` on the frontend and session configuration on the Python backend via Eel bridge endpoints.
5. Provide full bilingual (Ukrainian `uk` and English `en`) localization for all settings labels, tooltips, validation messages, and action buttons.

---

## 2. User Scenarios & Testing *(Prioritized)*

### User Story 1 - Configure Path Delimiter Symbol (Priority: P1)

As a database architect / user,  
I want to change the hierarchy path delimiter symbol (e.g., from `\` to `/` or `::`),  
So that absolute paths generated on node badges, the path preview tab, and exported Excel files match my target database naming convention.

**Why this priority**: Directly addresses the core user requirement to configure the path separation character.

**Independent Test**: Can be tested by opening Settings, changing the delimiter from `\` to `/`, saving, and verifying that all node path badges and the Preview Paths tab instantly reflect `/` as the separator (e.g., `Root/Folder/Item`).

**Acceptance Scenarios**:
1. **Given** the default configuration with delimiter `\`, **When** the user opens Settings, enters `/`, and clicks "Save", **Then** the active workspace tree re-evaluates all node paths with `/`, the Preview Paths tab updates, and future Excel exports use `/`.
2. **Given** a multi-level hierarchy, **When** the user imports an Excel file with header paths formatted as `A/B/C` and the active delimiter is set to `/`, **Then** `PathParserService` correctly parses the segments into parent and leaf nodes using `/`.
3. **Given** the user enters an invalid delimiter (empty string or whitespace only), **When** they attempt to save, **Then** the system prevents submission and displays a localized validation warning.

---

### User Story 2 - Configure Default Column Data Type (Priority: P2)

As an Excel data specialist,  
I want to choose the default data type for columns whose format in Excel is "General" (unspecified),  
So that imported general columns default to my preferred type (e.g., `Integer` or `Decimal`) instead of defaulting to `Text`.

**Why this priority**: Provides customized data typing control during Excel imports without manually editing dozens of individual leaf node types.

**Independent Test**: Can be tested by changing the default data type in Settings to `Integer`, importing an Excel file with General/unformatted columns, and verifying that all imported unformatted leaf nodes are assigned `Integer` type badges.

**Acceptance Scenarios**:
1. **Given** default data type is set to `Decimal`, **When** the user imports an Excel file containing columns with General/unformatted cells, **Then** those leaf nodes are automatically created with `Decimal` data type.
2. **Given** an Excel column with an explicit format (e.g., Currency `$#,##0.00` or Date `yyyy-mm-dd`), **When** the file is imported, **Then** its explicit type (`Currency` or `Date`) is preserved and is not overridden by the default data type setting.
3. **Given** the user creates a new node in the workspace without changing the type selector, **When** the modal opens, **Then** the default type selector pre-selects the configured default data type.

---

### User Story 3 - Settings UI, Reset Defaults, and Bilingual Persistence (Priority: P3)

As a user,  
I want a clean, responsive modal with "Save", "Cancel", and "Reset Defaults" buttons,  
So that I can easily configure my preferences, reset them whenever needed, and have them saved across sessions in my preferred language.

**Why this priority**: Ensures optimal UX, usability, error recovery, and seamless multilingual support.

**Independent Test**: Can be tested by switching language to Ukrainian/English, modifying settings, restarting the app or refreshing the page, and confirming that settings remain persisted.

**Acceptance Scenarios**:
1. **Given** the user clicks the gear icon (`#btnSettings`) in the header toolbar, **When** the modal opens, **Then** current active settings are pre-populated in the inputs.
2. **Given** modified settings, **When** the user clicks "Reset Defaults" (`#btnSettingsReset`), **Then** delimiter reverts to `\` and default data type reverts to `Text`.
3. **Given** the user switches the UI language between `UA` and `EN`, **When** the Settings modal is opened, **Then** all titles, labels, placeholders, option names, and buttons are rendered in the selected language.

---

## 3. Edge Cases & Handling

1. **Empty / Whitespace Delimiter**:
   - Prevent saving empty or whitespace-only delimiters. Fallback to `\` and show a warning toast: *"Символ розподілу не може бути порожнім / Delimiter cannot be empty"*.
2. **Multi-Character Delimiters (e.g., `::`, `->`, `//`)**:
   - Support delimiters up to 3 characters in length (e.g., `::` or `->` commonly used in database path notations).
3. **Delimiter Characters in Node Names**:
   - When sanitizing node names, escape or replace occurrences of the active delimiter so node names do not split improperly into unintended child segments.
4. **Switching Delimiter with Populated Canvas**:
   - Immediately trigger dynamic path recalculation on all existing nodes in active and background sheet session forests without requiring file reload or app restart.
5. **Resetting to Defaults**:
   - "Reset Defaults" restores delimiter to `\` and default data type to `Text`, updating `localStorage` and backend session configuration.

---

## 4. Requirements *(Mandatory)*

### Functional Requirements

- **FR-001**: A Settings button (`#btnSettings`) MUST be added to the `.toolbar-actions` container in `src/web/index.html` with a gear icon and localized tooltip.
- **FR-002**: A Settings Modal (`#settingsModal`) MUST be implemented containing:
  - Path delimiter input (`#inputSettingDelimiter`) with default value `\`.
  - Default data type dropdown (`#selectSettingDefaultType`) with default value `Text` containing all 9 standard Excel types.
  - Action buttons: Save (`#btnSettingsSave`), Cancel (`#btnSettingsCancel`), and Reset to Defaults (`#btnSettingsReset`).
- **FR-003**: The backend `HierarchyNode.get_absolute_path()` and `HierarchyNode.to_dict()` MUST support configurable delimiter parameter, defaulting to the active session delimiter.
- **FR-004**: `PathParserService.parse_header_paths()` MUST accept a configurable `delimiter` parameter (default: `\`) and properly split segments using the configured delimiter.
- **FR-005**: `ExcelHierarchyAdapter._map_format_to_data_type()` and `read_row1_headers_and_types()` MUST accept a configurable `default_data_type` (default: `Text`) applied when cell formatting is general/unspecified.
- **FR-006**: Eel bridge MUST expose `@eel.expose def get_settings()` and `@eel.expose def update_settings(delimiter, default_data_type)` to read and update session configuration.
- **FR-007**: When settings are updated, the frontend MUST immediately update `TreeRenderer` path badges and the `renderPaths` preview tab.
- **FR-008**: User settings MUST be persisted both in client browser `localStorage` (`je_settings_config`) and in a local backend configuration file (`settings.json`), with seamless synchronization via Eel bridge on application startup.
- **FR-009**: All UI strings in the Settings modal MUST have `data-i18n` and `data-i18n-attr` tags supporting instant bilingual translation (Ukrainian & English).
- **FR-010**: Keyboard accessibility MUST be supported (`Enter` to save in settings inputs, `Escape` to close modal).

### Key Entities

- **AppSettings**:
  - `delimiter`: `str` (default: `"\\"`, 1–3 characters)
  - `default_data_type`: `str` (default: `"Text"`, must be one of `VALID_DATA_TYPES`)

---

## 5. Success Criteria *(Mandatory)*

- **SC-001**: Users can change the path delimiter from `\` to any custom symbol (e.g. `/`, `|`, `::`), and all node paths in the tree and preview tab update in real-time.
- **SC-002**: Excel files imported with unformatted columns assign the configured `default_data_type` to all general leaf nodes.
- **SC-003**: Settings persist across app reloads and browser refreshes.
- **SC-004**: All Settings modal elements support 100% bilingual translation (UA / EN).
- **SC-005**: 100% automated pytest suite pass rate with new unit tests for configurable delimiter and default data type.

---

## 6. Assumptions & Defaults

- Supported default data types match the 9 existing Excel types (`Text`, `Integer`, `Decimal`, `Currency`, `Percentage`, `Date`, `Time`, `DateTime`, `Boolean`).
- Default delimiter is backslash (`\`).
- Settings apply globally across all sheets in the current workspace session.
