# Research & Decisions: Data Type Badge and Tooltip Localization

**Feature Branch**: `024-fix-data-type`  
**Spec**: [specs/024-fix-data-type/spec.md](spec.md)  
**Created**: 2026-08-14

---

## 1. Badge Localized Text Parity Mapping

| Canonical Domain String | Ukrainian Badge Display (`uk`) | English Badge Display (`en`) |
|---|---|---|
| `"Text"` | `"Текст (Рядок)"` | `"Text (String)"` |
| `"Integer"` | `"Ціле число"` | `"Integer (Whole Number)"` |
| `"Decimal"` | `"Дробове число"` | `"Decimal (Float)"` |
| `"Currency"` | `"Валюта"` | `"Currency ($#,##0.00)"` |
| `"Percentage"` | `"Відсоток"` | `"Percentage (%)"` |
| `"Date"` | `"Дата"` | `"Date (YYYY-MM-DD)"` |
| `"Time"` | `"Час"` | `"Time (HH:MM:SS)"` |
| `"DateTime"` | `"Дата і час"` | `"DateTime (Timestamp)"` |
| `"Boolean"` | `"Логічний тип"` | `"Boolean (TRUE/FALSE)"` |

---

## 2. Tooltip Localization Parity

| Tooltip Key | Ukrainian Tooltip | English Tooltip |
|---|---|---|
| `tooltip_data_type_badge` | `"Тип даних колонки Excel (Подвійний клік для зміни)"` | `"Excel Column Data Type (Double-click to edit)"` |
