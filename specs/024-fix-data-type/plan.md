# Implementation Plan: Data Type Badge and Tooltip Localization

**Feature Branch**: `024-fix-data-type`  
**Spec**: [specs/024-fix-data-type/spec.md](spec.md)  
**Created**: 2026-08-14

---

## 1. Technical Architecture & Strategy

### 1.1 `I18n` Engine Enhancements (`src/web/js/i18n.js`)
- Add dictionary entries in `uk`:
  ```javascript
  type_badge_text: "Текст (Рядок)",
  type_badge_integer: "Ціле число",
  type_badge_decimal: "Дробове число",
  type_badge_currency: "Валюта",
  type_badge_percentage: "Відсоток",
  type_badge_date: "Дата",
  type_badge_time: "Час",
  type_badge_datetime: "Дата і час",
  type_badge_boolean: "Логічний тип",
  ```
- Add dictionary entries in `en`:
  ```javascript
  type_badge_text: "Text (String)",
  type_badge_integer: "Integer (Whole Number)",
  type_badge_decimal: "Decimal (Float)",
  type_badge_currency: "Currency ($#,##0.00)",
  type_badge_percentage: "Percentage (%)",
  type_badge_date: "Date (YYYY-MM-DD)",
  type_badge_time: "Time (HH:MM:SS)",
  type_badge_datetime: "DateTime (Timestamp)",
  type_badge_boolean: "Boolean (TRUE/FALSE)",
  ```
- Add helper method on `I18n`:
  ```javascript
  getTypeLabel(type) {
      if (!type) return 'Text';
      const key = 'type_badge_' + String(type).toLowerCase();
      const translated = this.t(key);
      return (translated !== key) ? translated : String(type);
  }
  ```

### 1.2 Tree Node Badges (`src/web/js/tree_renderer.js`)
- In `createNodeElement`:
  ```javascript
  const typeBadgeHtml = !isFolder
      ? `<span class="node-type-badge" data-type="${this.escapeHtml(node.data_type || 'Text')}" title="${t('tooltip_data_type_badge')}">${this.escapeHtml(window.I18n ? I18n.getTypeLabel(node.data_type) : (node.data_type || 'Text'))}</span>`
      : '';
  ```
- In `renderPaths`:
  ```javascript
  <span class="node-type-badge" data-type="${this.escapeHtml(item.type)}" title="${t('tooltip_data_type_badge')}">${this.escapeHtml(window.I18n ? I18n.getTypeLabel(item.type) : item.type)}</span>
  ```

### 1.3 Sidebar Header Type Tags (`src/web/js/app.js`)
- In `filterAndRenderSidebar`:
  ```javascript
  const typeTagHtml = `<span class="header-type-tag" title="${t('tooltip_data_type_badge')}">${this.escapeHtml(window.I18n ? I18n.getTypeLabel(item.type) : (item.type || 'Text'))}</span>`;
  ```

---

## 2. Risk & Impact Analysis
- **Domain Data Model Invariance**: The string stored in `node.data_type` remains canonical English (`"Text"`, `"Currency"`, etc.). `data-type` CSS attributes remain unchanged, preserving styling.
- **Performance**: Direct in-memory lookup in `I18n.getTypeLabel`, zero DOM flicker or delay.
