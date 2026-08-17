"""Declarative Component & State Interaction Manifest for JE Test Constructor."""

from pathlib import Path

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures" / "excel_samples"

# Declarative interaction flows defining actions, target elements, and strict post-conditions
INTERACTION_FLOWS = {
    "flow_empty_workspace": {
        "description": "Initial clean workspace state on startup",
        "action": {"type": "navigate"},
        "expected": {
            "#treeEmptyState": {"visible": True},
            "#btnCreateRootEmpty": {"visible": True, "enabled": True},
            "#activeSheetSelector": {"visible": True, "disabled": True},
            "#catalogSheetSelector": {"visible": True, "disabled": True},
            "#sidebarSearch": {"visible": True, "disabled": True},
            "#sidebarEmptyState": {"visible": True},
            "#sidebarHeaderList": {"has_class": "hidden"},
            "#templateStatusBadge": {"visible": True, "text_contains": "(Немає)"},
        },
    },
    "flow_import_multisheet_excel": {
        "description": "Importing a multi-sheet Excel workbook and verifying global cascade",
        "action": {
            "type": "import_file",
            "file_path": str(FIXTURES_DIR / "multisheet_retail.xlsx"),
        },
        "expected": {
            "#activeSheetSelector": {"visible": True, "enabled": True, "min_options": 3},
            "#catalogSheetSelector": {"visible": True, "enabled": True, "min_options": 3},
            "#sidebarSearch": {"visible": True, "enabled": True},
            "#sidebarHeaderList": {"visible": True, "has_not_class": "hidden"},
            "#sidebarEmptyState": {"has_class": "hidden"},
            ".sidebar-header-item": {"visible": True, "min_count": 1},
            "#templateStatusBadge": {"visible": True},
            "#treeView": {"visible": True},
        },
    },
    "flow_template_badge_sync": {
        "description": "Binding template path updates template badge with Synced status",
        "action": {
            "type": "custom",
            "steps": [
                {"action": "evaluate", "script": "SessionController.updateTemplateBadge('C:/Exports/Шаблон_Retail.xlsx')"}
            ],
        },
        "expected": {
            "#templateStatusBadge": {"visible": True, "text_contains": "Шаблон_Retail.xlsx"},
        },
    },
    "flow_switch_active_sheet": {
        "description": "Switching active tree sheet in multi-sheet session",
        "action": {"type": "select_option", "selector": "#activeSheetSelector", "value": "Store_West"},
        "expected": {
            "#activeSheetSelector": {"value": "Store_West"},
            "#treeView": {"visible": True},
            "#treeEmptyState": {"visible": False},
        },
    },
    "flow_switch_catalog_sheet_independent": {
        "description": "Switching catalog sheet updates header list without altering active tree sheet",
        "action": {"type": "select_option", "selector": "#catalogSheetSelector", "value": "Warehouse_Central"},
        "expected": {
            "#catalogSheetSelector": {"value": "Warehouse_Central"},
            "#sidebarHeaderList": {"visible": True, "has_not_class": "hidden"},
            ".sidebar-header-item": {"visible": True},
        },
    },
    "flow_sidebar_search_filter": {
        "description": "Filtering sidebar headers by query and restoring",
        "action": {"type": "fill_input", "selector": "#sidebarSearch", "value": "e"},
        "expected": {
            "#sidebarSearch": {"value": "e"},
            ".sidebar-header-item": {"visible": True},
        },
    },
    "flow_switch_to_matrix_view": {
        "description": "Switching to Excel Blocks Matrix view",
        "action": {"type": "click", "selector": "#btnViewMatrix"},
        "expected": {
            "#btnViewMatrix": {"has_class": "active"},
            "#excelBlockView": {"visible": True, "has_not_class": "hidden"},
            "#treeView": {"has_class": "hidden"},
            "#uniqueLevelView": {"has_class": "hidden"},
            ".excel-matrix-table": {"visible": True},
        },
    },
    "flow_switch_to_unique_levels_view": {
        "description": "Switching to Unique Levels view with leaf grouping",
        "action": {"type": "click", "selector": "#btnViewUniqueLevels"},
        "expected": {
            "#btnViewUniqueLevels": {"has_class": "active"},
            "#uniqueLevelView": {"visible": True, "has_not_class": "hidden"},
            "#treeView": {"has_class": "hidden"},
            "#excelBlockView": {"has_class": "hidden"},
            ".unique-levels-wrapper": {"visible": True},
        },
    },
    "flow_switch_back_to_tree_view": {
        "description": "Switching back to Tree Canvas view",
        "action": {"type": "click", "selector": "#btnViewTree"},
        "expected": {
            "#btnViewTree": {"has_class": "active"},
            "#treeView": {"visible": True, "has_not_class": "hidden"},
            "#excelBlockView": {"has_class": "hidden"},
            "#uniqueLevelView": {"has_class": "hidden"},
        },
    },
    "flow_sidebar_tab_paths": {
        "description": "Switching sidebar tab to Leaf Paths preview",
        "action": {"type": "select_option", "selector": "#sidebarTabSelector", "value": "paths"},
        "expected": {
            "#tabContentPaths": {"visible": True, "has_not_class": "hidden"},
            "#tabContentCatalog": {"has_class": "hidden"},
            "#pathCountBadge": {"visible": True, "has_not_class": "hidden"},
            "#headerCountBadge": {"has_class": "hidden"},
        },
    },
    "flow_settings_modal_delimiter_change": {
        "description": "Opening settings modal, changing delimiter to '.', saving and checking paths",
        "action": {
            "type": "custom",
            "steps": [
                {"action": "click", "selector": "#btnSettings"},
                {"action": "fill", "selector": "#inputSettingDelimiter", "value": "."},
                {"action": "click", "selector": "#btnSettingsSave"},
                {"action": "select", "selector": "#sidebarTabSelector", "value": "paths"},
            ],
        },
        "expected": {
            "#settingsModal": {"has_class": "hidden"},
            "#pathList": {"visible": True},
        },
    },
    "flow_sidebar_collapse_and_expand": {
        "description": "Collapsing sidebar to vertical strip and expanding back",
        "action": {
            "type": "custom",
            "steps": [
                {"action": "click", "selector": "#btnToggleSidebarCollapse"},
                {"action": "click", "selector": "#btnExpandSidebarStrip"},
            ],
        },
        "expected": {
            "#unifiedSidebar": {"has_not_class": "sidebar-collapsed"},
        },
    },
    "flow_bilingual_toggle_en_uk": {
        "description": "Switching language to English and restoring Ukrainian",
        "action": {
            "type": "custom",
            "steps": [
                {"action": "click", "selector": "#langBtnEn"},
                {"action": "click", "selector": "#langBtnUk"},
            ],
        },
        "expected": {
            "#langBtnUk": {"has_class": "active"},
            ".brand h1": {"visible": True, "text_contains": "Конструктор"},
        },
    },
}
