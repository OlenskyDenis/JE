# Quickstart: Data Type Badge and Tooltip Verification

**Feature Branch**: `024-fix-data-type`  
**Created**: 2026-08-14

---

## 1. Automated Test Suite

```powershell
python -m pytest
```

---

## 2. Manual UI Verification Steps

1. Launch application:
   ```powershell
   python -m src.app.main
   ```
2. In Ukrainian mode (`UA`), verify any leaf node badge displays Ukrainian text (e.g. `"Текст (Рядок)"`, `"Валюта"`).
3. Hover over the badge and verify the tooltip displays:
   `"Тип даних колонки Excel (Подвійний клік для зміни)"`.
4. Switch to English (`EN`) and verify the badge text updates to `"Text (String)"`, `"Currency ($#,##0.00)"` and tooltip updates to `"Excel Column Data Type (Double-click to edit)"`.
