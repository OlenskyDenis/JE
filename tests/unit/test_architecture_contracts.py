"""Automated architectural boundary, DIP compliance, and dead code prevention tests."""

import ast
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SRC_DIR = REPO_ROOT / "src"
MODELS_DIR = SRC_DIR / "hierarchy_lib" / "models"
SERVICES_DIR = SRC_DIR / "hierarchy_lib" / "services"
ADAPTERS_DIR = SRC_DIR / "hierarchy_lib" / "adapters"
APP_DIR = SRC_DIR / "app"
TESTS_DIR = REPO_ROOT / "tests"


class TestArchitectureContracts:
    """Automated enforcement of Constitution Principle II (DIP & YAGNI) and Principle VI."""

    def test_domain_models_do_not_import_services_or_adapters(self):
        """
        DIP Enforcement: Pure domain models in src/hierarchy_lib/models/ MUST NOT
        import from services, adapters, or app infrastructure.
        """
        forbidden_prefixes = (
            "src.hierarchy_lib.services",
            "src.hierarchy_lib.adapters",
            "src.app",
        )

        for py_file in MODELS_DIR.glob("*.py"):
            if py_file.name.startswith("__"):
                continue
            tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        for forbidden in forbidden_prefixes:
                            assert not alias.name.startswith(forbidden), (
                                f"DIP Violation: Model file {py_file.name} imports from forbidden module '{alias.name}'"
                            )
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        for forbidden in forbidden_prefixes:
                            assert not node.module.startswith(forbidden), (
                                f"DIP Violation: Model file {py_file.name} imports from forbidden module '{node.module}'"
                            )

    def test_retired_files_do_not_exist(self):
        """
        Strict YAGNI: Ensure that retired ghost/alias files remain deleted.
        """
        retired_files = [
            MODELS_DIR / "base.py",
            MODELS_DIR / "composite.py",
            MODELS_DIR / "leaf.py",
            SERVICES_DIR / "path_generator.py",
            TESTS_DIR / "unit" / "test_excel_export.py",
            TESTS_DIR / "unit" / "test_excel_import.py",
            TESTS_DIR / "unit" / "test_path_generator.py",
        ]
        for f in retired_files:
            assert not f.exists(), f"Retired file {f.relative_to(REPO_ROOT)} was found on disk!"

    def test_no_retired_rpc_endpoints_in_eel_bridge(self):
        """
        RPC Hygiene: Ensure that deleted Feature 001 and legacy single-field RPCs are not present.
        """
        eel_bridge_file = APP_DIR / "eel_bridge.py"
        assert eel_bridge_file.exists()
        content = eel_bridge_file.read_text(encoding="utf-8")
        tree = ast.parse(content, filename=str(eel_bridge_file))

        function_names = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}

        retired_rpcs = {
            "import_excel",
            "export_excel",
            "rename_node",
            "update_node_type",
            "get_sheet_headers",
            "get_workspace_tree",
            "export_reorganized_row1",
        }

        found_retired = function_names.intersection(retired_rpcs)
        assert not found_retired, f"Retired RPC functions still present in eel_bridge.py: {found_retired}"

    def test_system_map_modular_router_integrity(self):
        """
        Modular System Map Integrity: Ensure master router and all MVC modular maps exist and are non-empty.
        """
        specify_dir = REPO_ROOT / ".specify"
        master_router = specify_dir / "system_map.md"
        assert master_router.exists(), "Master router .specify/system_map.md missing"

        system_map_dir = specify_dir / "system_map"
        assert system_map_dir.exists() and system_map_dir.is_dir(), "Modular directory .specify/system_map missing"

        expected_modules = [
            "domain_and_models.md",
            "views_and_ui.md",
            "controllers_and_rpc.md",
            "dtos_and_contracts.md",
            "infrastructure_and_adapters.md",
            "state_and_lifecycle.md",
            "tests_and_quality.md",
        ]

        for mod_name in expected_modules:
            mod_file = system_map_dir / mod_name
            assert mod_file.exists(), f"Modular system map file '{mod_name}' is missing"
            assert mod_file.stat().st_size > 100, f"Modular system map file '{mod_name}' is empty or too short"
