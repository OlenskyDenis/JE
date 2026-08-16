# Feature Specification: Data Type Badge and Tooltip Localization

**Feature Branch**: `024-fix-data-type`  
**Created**: 2026-08-14  
**Status**: Draft  
**Input**: User directive: "Швидкий фікс, не перекладє span Excel Column Data Type (Double-click to edit)"

---

## Clarifications

### Session 2026-08-14
- Q: Який стиль відображення назв типів даних у бейджах (span .node-type-badge) ви бажаєте використовувати в українській локалізації? → A: Extended Ukrainian terms: `Текст (Рядок)`, `Ціле число`, `Дробове число`, `Валюта`, `Відсоток`, `Дата`, `Час`, `Дата і час`, `Логічний тип`.

---

## 1. Problem Statement & Objectives

### Problem
The Excel column data type badges (`.node-type-badge` and `.header-type-tag`) across the tree canvas, sidebar catalog, and export preview list were not fully localizing their display names (e.g. `"Text"`, `"Integer"`, `"Date"`) and tooltip attributes (`"Excel Column Data Type (Double-click to edit)"` / `"Тип даних колонки Excel (Подвійний клік для зміни)"`) dynamically across language switches.

### Objectives
1. Add short localized badge display names (`type_badge_*`) to `uk` and `en` dictionaries in `src/web/js/i18n.js`.
2. Add `I18n.getTypeLabel(dataType)` helper to translate canonical data types to active UI language without modifying the underlying domain string stored in `node.data_type`.
3. Ensure all instances of `.node-type-badge` (in `TreeRenderer.renderTree` and `TreeRenderer.renderPaths`) and `.header-type-tag` (in `App.filterAndRenderSidebar`) render with the localized tooltip `tooltip_data_type_badge` and localized type label.

---

## 2. Functional Requirements

- **FR-001**: `I18n` dictionary MUST contain `type_badge_text`, `type_badge_integer`, `type_badge_decimal`, `type_badge_currency`, `type_badge_percentage`, `type_badge_date`, `type_badge_time`, `type_badge_datetime`, and `type_badge_boolean` in both Ukrainian and English.
- **FR-002**: `I18n.getTypeLabel(type)` helper MUST return the localized label for the active language, while falling back to the canonical string.
- **FR-003**: `TreeRenderer.createNodeElement` MUST apply `title="${t('tooltip_data_type_badge')}"` and render `I18n.getTypeLabel(node.data_type)` inside `<span class="node-type-badge">`.
- **FR-004**: `TreeRenderer.renderPaths` MUST apply `title="${t('tooltip_data_type_badge')}"` and render `I18n.getTypeLabel(item.type)` inside `<span class="node-type-badge">`.
- **FR-005**: `App.filterAndRenderSidebar` MUST apply `title="${t('tooltip_data_type_badge')}"` and render `I18n.getTypeLabel(item.type)` inside `<span class="header-type-tag">`.
- **FR-006**: The underlying `data-type` DOM attribute and the node data model `data_type` value MUST remain the canonical English identifier (`"Text"`, `"Currency"`, etc.) for CSS styling and Excel template export compatibility.

---

## 3. Success Criteria

- **SC-001**: Hovering over any data type badge in Ukrainian mode displays `"Тип даних колонки Excel (Подвійний клік для зміни)"`.
- **SC-002**: Hovering over any data type badge in English mode displays `"Excel Column Data Type (Double-click to edit)"`.
- **SC-003**: Data type badge text updates to Ukrainian (`"Текст"`, `"Валюта"`, `"Дата"`, тощо) in `uk` mode and English (`"Text"`, `"Currency"`, `"Date"`, etc.) in `en` mode upon instant language switch.
- **SC-004**: 100% pass rate in automated pytest test suite.
