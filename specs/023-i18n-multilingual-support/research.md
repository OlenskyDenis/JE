# Technical Research: Localization Dictionary Schema & Architecture

**Feature Branch**: `023-i18n-multilingual-support`  
**Spec**: [specs/023-i18n-multilingual-support/spec.md](spec.md)  
**Created**: 2026-08-14

---

## 1. Complete Translation Dictionary Schema

Below is the complete key-value catalog mapped across Ukrainian (`uk`) and English (`en`):

```json
{
  "brand_title": {
    "en": "Database Hierarchy Creator",
    "uk": "Конструктор ієрархії баз даних"
  },
  "template_prefix": {
    "en": "Template",
    "uk": "Шаблон"
  },
  "template_none": {
    "en": "(None)",
    "uk": "(Немає)"
  },
  "template_status_title": {
    "en": "Active Bound Template File for 1-Click Sync",
    "uk": "Активний прив'язаний файл шаблону для швидкої синхронізації"
  },
  "btn_import_excel": {
    "en": "Import Excel",
    "uk": "Імпорт Excel"
  },
  "btn_export_excel": {
    "en": "Export Excel",
    "uk": "Експорт Excel"
  },
  "btn_refresh": {
    "en": "Refresh Session",
    "uk": "Оновити сесію"
  },
  "workspace_title": {
    "en": "Hierarchy Constructor Workspace",
    "uk": "Робоча область конструктора ієрархії"
  },
  "workspace_sheet_label": {
    "en": "Sheet:",
    "uk": "Аркуш:"
  },
  "workspace_no_sheet": {
    "en": "(No Sheet)",
    "uk": "(Немає аркуша)"
  },
  "tooltip_expand_all": {
    "en": "Expand All Folders",
    "uk": "Розгорнути всі папки"
  },
  "tooltip_collapse_all": {
    "en": "Collapse All Folders",
    "uk": "Згорнути всі папки"
  },
  "workspace_empty_title": {
    "en": "Workspace is empty",
    "uk": "Робоча область порожня"
  },
  "workspace_empty_hint": {
    "en": "Import an Excel file, drag headers from the catalog, or start from scratch:",
    "uk": "Імпортуйте файл Excel, перетягніть колонки з каталогу або створіть з нуля:"
  },
  "btn_create_root": {
    "en": "Create Root Node",
    "uk": "Створити кореневий вузол"
  },
  "tab_catalog": {
    "en": "Header Catalog",
    "uk": "Каталог колонок"
  },
  "tab_paths": {
    "en": "Export Preview",
    "uk": "Попередній перегляд"
  },
  "sidebar_resizer_tooltip": {
    "en": "Drag to resize sidebar (Double-click to reset)",
    "uk": "Потягніть для зміни ширини (Подвійний клік для скидання)"
  },
  "catalog_browse_from": {
    "en": "Browse Headers From",
    "uk": "Джерело колонок"
  },
  "catalog_no_file": {
    "en": "No Excel file loaded",
    "uk": "Файл Excel не завантажено"
  },
  "catalog_all_sheets": {
    "en": "All Sheets (Combined)",
    "uk": "Усі аркуші (Об'єднані)"
  },
  "catalog_help_text": {
    "en": "Select source to drag headers without changing the active workspace tree.",
    "uk": "Оберіть джерело для перетягування без зміни активного дерева."
  },
  "catalog_search_label": {
    "en": "Search Headers",
    "uk": "Пошук колонок"
  },
  "catalog_search_placeholder": {
    "en": "Filter headers in real-time...",
    "uk": "Фільтрувати колонки в реальному часі..."
  },
  "catalog_empty_title": {
    "en": "No headers loaded",
    "uk": "Немає завантажених колонок"
  },
  "catalog_empty_hint": {
    "en": "Click 'Import Excel' to extract Row 1 headers from any sheet.",
    "uk": "Натисніть «Імпорт Excel», щоб отримати заголовки з 1-го рядка."
  },
  "paths_empty": {
    "en": "No leaf paths generated yet",
    "uk": "Шляхи кінцевих елементів ще не згенеровано"
  },
  "modal_create_title": {
    "en": "Create Node",
    "uk": "Створити вузол"
  },
  "modal_edit_folder_title": {
    "en": "Edit Folder Node",
    "uk": "Редагувати папку"
  },
  "modal_edit_element_title": {
    "en": "Edit Element Node",
    "uk": "Редагувати елемент"
  },
  "modal_label_name": {
    "en": "Node Name",
    "uk": "Назва вузла"
  },
  "modal_placeholder_name": {
    "en": "e.g. Finance, Report_2026",
    "uk": "наприклад: Фінанси, Звіт_2026"
  },
  "modal_label_type": {
    "en": "Element Data Type",
    "uk": "Тип даних елемента"
  },
  "modal_folder_type_hint": {
    "en": "Data types apply to leaf data elements only.",
    "uk": "Типи даних застосовуються лише до кінцевих елементів."
  },
  "modal_btn_cancel": {
    "en": "Cancel",
    "uk": "Скасувати"
  },
  "modal_btn_create": {
    "en": "Create Node",
    "uk": "Створити вузол"
  },
  "modal_btn_save": {
    "en": "Save Changes",
    "uk": "Зберегти зміни"
  },
  "unsaved_title": {
    "en": "Unsaved Changes",
    "uk": "Незбережені зміни"
  },
  "unsaved_btn_cancel": {
    "en": "Cancel",
    "uk": "Скасувати"
  },
  "unsaved_btn_discard_switch": {
    "en": "Discard & Switch",
    "uk": "Відкинути і перемкнути"
  },
  "unsaved_btn_save_switch": {
    "en": "Save & Switch",
    "uk": "Зберегти і перемкнути"
  },
  "unsaved_btn_update_switch": {
    "en": "Update Template & Switch",
    "uk": "Оновити шаблон і перемкнути"
  },
  "unsaved_btn_discard_import": {
    "en": "Discard & Import",
    "uk": "Відкинути і імпортувати"
  },
  "unsaved_btn_save_import": {
    "en": "Save Template & Import",
    "uk": "Зберегти шаблон і імпортувати"
  },
  "unsaved_btn_update_import": {
    "en": "Update Template & Import",
    "uk": "Оновити шаблон і імпортувати"
  },
  "unsaved_btn_discard_refresh": {
    "en": "Discard & Refresh",
    "uk": "Відкинути і оновити"
  },
  "unsaved_btn_save_refresh": {
    "en": "Save Template & Refresh",
    "uk": "Зберегти шаблон і оновити"
  },
  "unsaved_btn_update_refresh": {
    "en": "Update Template & Refresh",
    "uk": "Оновити шаблон і оновити"
  },
  "type_text": {
    "en": "Text (String)",
    "uk": "Текст (Рядок)"
  },
  "type_integer": {
    "en": "Integer (Whole Number)",
    "uk": "Ціле число (Integer)"
  },
  "type_decimal": {
    "en": "Decimal (Float)",
    "uk": "Дробове число (Decimal)"
  },
  "type_currency": {
    "en": "Currency ($#,##0.00)",
    "uk": "Валюта ($#,##0.00)"
  },
  "type_percentage": {
    "en": "Percentage (%)",
    "uk": "Відсоток (%)"
  },
  "type_date": {
    "en": "Date (YYYY-MM-DD)",
    "uk": "Дата (РРРР-ММ-ДД)"
  },
  "type_time": {
    "en": "Time (HH:MM:SS)",
    "uk": "Час (ГГ:ХХ:СС)"
  },
  "type_datetime": {
    "en": "DateTime (Timestamp)",
    "uk": "Дата і час (DateTime)"
  },
  "type_boolean": {
    "en": "Boolean (TRUE/FALSE)",
    "uk": "Логічний тип (TRUE/FALSE)"
  },
  "node_count": {
    "en": "{count} Nodes",
    "uk": "{count} Вузлів"
  },
  "header_count": {
    "en": "{count} Headers",
    "uk": "{count} Заголовків"
  },
  "path_count": {
    "en": "{count} Paths",
    "uk": "{count} Шляхів"
  },
  "tooltip_edit_node": {
    "en": "Edit Node",
    "uk": "Редагувати вузол"
  },
  "tooltip_add_child": {
    "en": "Add Child Node",
    "uk": "Додати дочірній вузол"
  },
  "tooltip_delete_node": {
    "en": "Delete Node",
    "uk": "Видалити вузол"
  },
  "tooltip_drag_handle": {
    "en": "Drag to reorder or nest",
    "uk": "Потягніть для переміщення або вкладення"
  },
  "tooltip_node_title": {
    "en": "Double-click to edit",
    "uk": "Подвійний клік для редагування"
  },
  "tooltip_data_type_badge": {
    "en": "Excel Column Data Type (Double-click to edit)",
    "uk": "Тип даних колонки Excel (Подвійний клік для зміни)"
  },
  "tooltip_expand_folder": {
    "en": "Expand folder",
    "uk": "Розгорнути папку"
  },
  "tooltip_collapse_folder": {
    "en": "Collapse folder",
    "uk": "Згорнути папку"
  },
  "confirm_delete": {
    "en": "Are you sure you want to delete this node and all its contents?",
    "uk": "Ви впевнені, що хочете видалити цей вузол та весь його вміст?"
  }
}
```
