/**
 * Centralized Internationalization (i18n) Module
 * Handles multilingual translations (Ukrainian 'uk' and English 'en'),
 * parameter interpolation, DOM translation, and persistent language preferences.
 */

const I18N_DICTIONARIES = {
    uk: {
        // App Header & Branding
        brand_title: "Конструктор ієрархії баз даних",
        template_prefix: "Шаблон",
        template_none: "(Немає)",
        template_status_title: "Активний прив'язаний файл шаблону для швидкої синхронізації",
        btn_import_excel: "Імпорт Excel",
        btn_export_excel: "Експорт Excel",
        btn_refresh: "Оновити сесію",

        // Workspace Canvas
        workspace_title: "Робоча область конструктора ієрархії",
        workspace_sheet_label: "Аркуш:",
        workspace_no_sheet: "(Немає аркуша)",
        tooltip_expand_all: "Розгорнути всі папки",
        tooltip_collapse_all: "Згорнути всі папки",
        workspace_empty_title: "Робоча область порожня",
        workspace_empty_hint: "Імпортуйте файл Excel, перетягніть колонки з каталогу або створіть з нуля:",
        btn_create_root: "Створити кореневий вузол",

        // Sidebar Tabs & Splitter
        tab_catalog: "Каталог колонок",
        tab_paths: "Попередній перегляд",
        sidebar_resizer_tooltip: "Потягніть для зміни ширини (Подвійний клік для скидання)",
        sidebar_width_reset_toast: "Ширину бічної панелі скинуто до стандартної (340px).",

        // Catalog Tab
        catalog_browse_from: "Джерело колонок",
        catalog_no_file: "Файл Excel не завантажено",
        catalog_all_sheets: "Усі аркуші (Об'єднані)",
        catalog_help_text: "Оберіть джерело для перетягування без зміни активного дерева.",
        catalog_search_label: "Пошук колонок",
        catalog_search_placeholder: "Фільтрувати колонки в реальному часі...",
        catalog_empty_title: "Немає завантажених колонок",
        catalog_empty_hint: "Натисніть «Імпорт Excel», щоб отримати заголовки з 1-го рядка.",

        // Paths Tab (Export Preview)
        paths_empty: "Шляхи кінцевих елементів ще не згенеровано",

        // Counters
        node_count: "{count} Вузлів",
        header_count: "{count} Заголовків",
        path_count: "{count} Шляхів",

        // Tree Nodes Actions & Tooltips
        tooltip_edit_node: "Редагувати вузол",
        tooltip_add_child: "Додати дочірній вузол",
        tooltip_delete_node: "Видалити вузол",
        tooltip_drag_handle: "Потягніть для переміщення або вкладення",
        tooltip_node_title: "Подвійний клік для редагування",
        tooltip_data_type_badge: "Тип даних колонки Excel (Подвійний клік для зміни)",
        tooltip_expand_folder: "Розгорнути папку",
        tooltip_collapse_folder: "Згорнути папку",

        // Modals: Create / Edit Node
        modal_create_title: "Створити вузол",
        modal_edit_folder_title: "Редагувати папку",
        modal_edit_element_title: "Редагувати елемент",
        modal_label_name: "Назва вузла",
        modal_placeholder_name: "наприклад: Фінанси, Звіт_2026",
        modal_label_type: "Тип даних елемента",
        modal_folder_type_hint: "Типи даних застосовуються лише до кінцевих елементів.",
        modal_btn_cancel: "Скасувати",
        modal_btn_create: "Створити вузол",
        modal_btn_save: "Зберегти зміни",

        // Modals: Unsaved Changes
        unsaved_title: "Незбережені зміни",
        unsaved_btn_cancel: "Скасувати",
        unsaved_btn_discard_switch: "Відкинути і перемкнути",
        unsaved_btn_save_switch: "Зберегти і перемкнути",
        unsaved_btn_update_switch: "Оновити шаблон і перемкнути",
        unsaved_btn_discard_import: "Відкинути і імпортувати",
        unsaved_btn_save_import: "Зберегти шаблон і імпортувати",
        unsaved_btn_update_import: "Оновити шаблон і імпортувати",
        unsaved_btn_discard_refresh: "Відкинути і оновити",
        unsaved_btn_save_refresh: "Зберегти шаблон і оновити",
        unsaved_btn_update_refresh: "Оновити шаблон і оновити",
        unsaved_msg_switch_update: 'У вас є незбережені зміни на аркуші "<strong>{sheet}</strong>". Оновити шаблон "<strong>{template}</strong>" перед перемиканням на "<strong>{target}</strong>"?',
        unsaved_msg_switch_save: 'У вас є незбережені зміни на аркуші "<strong>{sheet}</strong>". Зберегти зміни у файл шаблону перед перемиканням на "<strong>{target}</strong>"?',
        unsaved_msg_import_update: 'У вас є незбережені зміни в поточній сесії. Оновити шаблон "<strong>{template}</strong>" перед імпортом нового файлу?',
        unsaved_msg_import_save: 'У вас є незбережені зміни в поточній сесії. Зберегти зміни у файл шаблону перед імпортом нового файлу?',
        unsaved_msg_refresh_update: 'У вас є незбережені зміни в поточній сесії. Оновити шаблон "<strong>{template}</strong>" перед оновленням з файлу "<strong>{file}</strong>"?',
        unsaved_msg_refresh_save: 'У вас є незбережені зміни в поточній сесії. Зберегти зміни у файл шаблону перед оновленням з файлу "<strong>{file}</strong>"?',

        // Data Types (Dropdown Options)
        type_text: "Текст (Рядок)",
        type_integer: "Ціле число (Integer)",
        type_decimal: "Дробове число (Decimal)",
        type_currency: "Валюта ($#,##0.00)",
        type_percentage: "Відсоток (%)",
        type_date: "Дата (РРРР-ММ-ДД)",
        type_time: "Час (ГГ:ХХ:СС)",
        type_datetime: "Дата і час (DateTime)",
        type_boolean: "Логічний тип (TRUE/FALSE)",

        // Dialogs & Confirmations
        confirm_delete: "Ви впевнені, що хочете видалити цей вузол та весь його вміст?",

        // Toast Messages & Errors
        toast_imported_session: "Імпортовано сесію Excel: знайдено аркушів — {count}.",
        toast_import_failed: "Не вдалося імпортувати сесію Excel.",
        toast_switched_sheet: "Активний робочий аркуш перемкнуто на «{sheet}».",
        toast_switch_failed: "Не вдалося перемкнути аркуш.",
        toast_template_updated: "Шаблон «{template}» успішно оновлено.",
        toast_template_saved: "Шаблон «{template}» збережено.",
        toast_template_exported: "Чистий шаблон експортовано до «{template}».",
        toast_template_failed: "Не вдалося експортувати шаблон.",
        toast_refreshed_session: "Оновлено сесію Excel з файлу «{file}».",
        toast_refresh_no_session: "Немає активної сесії Excel для оновлення.",
        toast_refresh_failed: "Не вдалося оновити сесію Excel.",
        toast_node_created: "Вузол «{name}» створено.",
        toast_node_updated: "Вузол «{name}» оновлено.",
        toast_node_deleted: "Вузол видалено.",
        toast_header_added: "Колонку «{name}» [{type}] додано до структури.",
        toast_name_empty: "Назва вузла не може бути порожньою.",
        toast_move_rejected: "Переміщення відхилено бекендом.",
        toast_tree_empty_export: "Дерево порожнє. Додайте вузли перед експортом.",
        toast_save_cancelled: "Збереження скасовано. Залишено поточну робочу область.",
        toast_cycle_prohibited: "Неприпустима дія: неможливо перемістити вузол у самого себе або у власний дочірній елемент."
    },
    en: {
        // App Header & Branding
        brand_title: "Database Hierarchy Creator",
        template_prefix: "Template",
        template_none: "(None)",
        template_status_title: "Active Bound Template File for 1-Click Sync",
        btn_import_excel: "Import Excel",
        btn_export_excel: "Export Excel",
        btn_refresh: "Refresh Session",

        // Workspace Canvas
        workspace_title: "Hierarchy Constructor Workspace",
        workspace_sheet_label: "Sheet:",
        workspace_no_sheet: "(No Sheet)",
        tooltip_expand_all: "Expand All Folders",
        tooltip_collapse_all: "Collapse All Folders",
        workspace_empty_title: "Workspace is empty",
        workspace_empty_hint: "Import an Excel file, drag headers from the catalog, or start from scratch:",
        btn_create_root: "Create Root Node",

        // Sidebar Tabs & Splitter
        tab_catalog: "Header Catalog",
        tab_paths: "Export Preview",
        sidebar_resizer_tooltip: "Drag to resize sidebar (Double-click to reset)",
        sidebar_width_reset_toast: "Sidebar width reset to default (340px).",

        // Catalog Tab
        catalog_browse_from: "Browse Headers From",
        catalog_no_file: "No Excel file loaded",
        catalog_all_sheets: "All Sheets (Combined)",
        catalog_help_text: "Select source to drag headers without changing the active workspace tree.",
        catalog_search_label: "Search Headers",
        catalog_search_placeholder: "Filter headers in real-time...",
        catalog_empty_title: "No headers loaded",
        catalog_empty_hint: "Click 'Import Excel' to extract Row 1 headers from any sheet.",

        // Paths Tab (Export Preview)
        paths_empty: "No leaf paths generated yet",

        // Counters
        node_count: "{count} Nodes",
        header_count: "{count} Headers",
        path_count: "{count} Paths",

        // Tree Nodes Actions & Tooltips
        tooltip_edit_node: "Edit Node",
        tooltip_add_child: "Add Child Node",
        tooltip_delete_node: "Delete Node",
        tooltip_drag_handle: "Drag to reorder or nest",
        tooltip_node_title: "Double-click to edit",
        tooltip_data_type_badge: "Excel Column Data Type (Double-click to edit)",
        tooltip_expand_folder: "Expand folder",
        tooltip_collapse_folder: "Collapse folder",

        // Modals: Create / Edit Node
        modal_create_title: "Create Node",
        modal_edit_folder_title: "Edit Folder Node",
        modal_edit_element_title: "Edit Element Node",
        modal_label_name: "Node Name",
        modal_placeholder_name: "e.g. Finance, Report_2026",
        modal_label_type: "Element Data Type",
        modal_folder_type_hint: "Data types apply to leaf data elements only.",
        modal_btn_cancel: "Cancel",
        modal_btn_create: "Create Node",
        modal_btn_save: "Save Changes",

        // Modals: Unsaved Changes
        unsaved_title: "Unsaved Changes",
        unsaved_btn_cancel: "Cancel",
        unsaved_btn_discard_switch: "Discard & Switch",
        unsaved_btn_save_switch: "Save & Switch",
        unsaved_btn_update_switch: "Update Template & Switch",
        unsaved_btn_discard_import: "Discard & Import",
        unsaved_btn_save_import: "Save Template & Import",
        unsaved_btn_update_import: "Update Template & Import",
        unsaved_btn_discard_refresh: "Discard & Refresh",
        unsaved_btn_save_refresh: "Save Template & Refresh",
        unsaved_btn_update_refresh: "Update Template & Refresh",
        unsaved_msg_switch_update: 'You have unsaved changes on sheet "<strong>{sheet}</strong>". Update template "<strong>{template}</strong>" before switching to "<strong>{target}</strong>"?',
        unsaved_msg_switch_save: 'You have unsaved changes on sheet "<strong>{sheet}</strong>". Save your changes to a template file before switching to "<strong>{target}</strong>"?',
        unsaved_msg_import_update: 'You have unsaved changes in your current session. Update template "<strong>{template}</strong>" before importing a new file?',
        unsaved_msg_import_save: 'You have unsaved changes in your current session. Save your changes to a template file before importing a new file?',
        unsaved_msg_refresh_update: 'You have unsaved changes in your current session. Update template "<strong>{template}</strong>" before refreshing from "<strong>{file}</strong>"?',
        unsaved_msg_refresh_save: 'You have unsaved changes in your current session. Save your changes to a template file before refreshing from "<strong>{file}</strong>"?',

        // Data Types (Dropdown Options)
        type_text: "Text (String)",
        type_integer: "Integer (Whole Number)",
        type_decimal: "Decimal (Float)",
        type_currency: "Currency ($#,##0.00)",
        type_percentage: "Percentage (%)",
        type_date: "Date (YYYY-MM-DD)",
        type_time: "Time (HH:MM:SS)",
        type_datetime: "DateTime (Timestamp)",
        type_boolean: "Boolean (TRUE/FALSE)",

        // Dialogs & Confirmations
        confirm_delete: "Are you sure you want to delete this node and all its contents?",

        // Toast Messages & Errors
        toast_imported_session: "Imported Excel session: {count} sheets found.",
        toast_import_failed: "Failed to import Excel session.",
        toast_switched_sheet: "Switched active workspace sheet to '{sheet}'.",
        toast_switch_failed: "Failed to switch sheet.",
        toast_template_updated: "Updated template '{template}'.",
        toast_template_saved: "Saved template '{template}'.",
        toast_template_exported: "Exported clean template to '{template}'.",
        toast_template_failed: "Failed to export template.",
        toast_refreshed_session: "Refreshed Excel session from '{file}'.",
        toast_refresh_no_session: "No active Excel session loaded to refresh.",
        toast_refresh_failed: "Failed to refresh Excel session.",
        toast_node_created: "Node '{name}' created.",
        toast_node_updated: "Node '{name}' updated.",
        toast_node_deleted: "Node deleted.",
        toast_header_added: "Added header node '{name}' [{type}] into tree structure.",
        toast_name_empty: "Node name cannot be empty.",
        toast_move_rejected: "Move rejected by backend.",
        toast_tree_empty_export: "Tree is empty. Add nodes before exporting.",
        toast_save_cancelled: "Save cancelled. Remained on active workspace.",
        toast_cycle_prohibited: "Invalid Operation: Cannot move a node into itself or its own descendant."
    }
};

const I18n = {
    currentLanguage: 'uk',
    subscribers: [],

    init() {
        const saved = localStorage.getItem('app_language');
        if (saved && (saved === 'uk' || saved === 'en')) {
            this.currentLanguage = saved;
        } else {
            this.currentLanguage = 'uk'; // Default to Ukrainian as requested
        }
        this.updateSwitcherButtons();
        this.translateDOM();
    },

    getLanguage() {
        return this.currentLanguage;
    },

    setLanguage(lang) {
        if (lang !== 'uk' && lang !== 'en') return;
        if (this.currentLanguage === lang) return;

        this.currentLanguage = lang;
        try {
            localStorage.setItem('app_language', lang);
        } catch (e) {
            console.warn("Failed to persist language preference:", e);
        }

        this.updateSwitcherButtons();
        this.translateDOM();
        this.notifySubscribers();
    },

    t(key, params = null) {
        const dict = I18N_DICTIONARIES[this.currentLanguage] || I18N_DICTIONARIES['uk'];
        let text = dict[key] || I18N_DICTIONARIES['en'][key] || key;

        if (params && typeof params === 'object') {
            Object.entries(params).forEach(([paramKey, paramVal]) => {
                text = text.replace(new RegExp(`\\{${paramKey}\\}`, 'g'), String(paramVal));
            });
        }
        return text;
    },

    onLanguageChanged(callback) {
        if (typeof callback === 'function') {
            this.subscribers.push(callback);
        }
    },

    notifySubscribers() {
        this.subscribers.forEach(cb => {
            try {
                cb(this.currentLanguage);
            } catch (err) {
                console.error("Error in language change subscriber:", err);
            }
        });
    },

    updateSwitcherButtons() {
        const btnUk = document.getElementById('langBtnUk');
        const btnEn = document.getElementById('langBtnEn');
        if (btnUk && btnEn) {
            if (this.currentLanguage === 'uk') {
                btnUk.classList.add('active');
                btnEn.classList.remove('active');
            } else {
                btnEn.classList.add('active');
                btnUk.classList.remove('active');
            }
        }
    },

    translateDOM(root = document) {
        // 1. Text elements with data-i18n
        const textElements = root.querySelectorAll('[data-i18n]');
        textElements.forEach(el => {
            const key = el.dataset.i18n;
            if (key) {
                el.textContent = this.t(key);
            }
        });

        // 2. Attribute elements with data-i18n-attr (e.g. "placeholder:key;title:key")
        const attrElements = root.querySelectorAll('[data-i18n-attr]');
        attrElements.forEach(el => {
            const raw = el.dataset.i18nAttr;
            if (!raw) return;
            const pairs = raw.split(';');
            pairs.forEach(pair => {
                const [attr, key] = pair.split(':');
                if (attr && key) {
                    el.setAttribute(attr.trim(), this.t(key.trim()));
                }
            });
        });
    }
};

// Export to window for global browser availability
window.I18n = I18n;
window.I18N_DICTIONARIES = I18N_DICTIONARIES;
