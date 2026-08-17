"""Generic Test Flow Executor & Invariant Validator for Matrix Test Engine."""

import re

from playwright.sync_api import Page, expect


class MatrixFlowExecutor:
    """Executes declarative interaction flows and verifies full-system state invariants."""

    def __init__(self, page: Page):
        self.page = page

    def execute_flow(self, flow_key: str, flow_def: dict):
        """Executes a single declarative flow and validates all expected element states."""
        action = flow_def.get("action", {})
        action_type = action.get("type")

        # 1. Trigger the Action
        if action_type == "navigate":
            pass  # Page is already at base URL
        elif action_type == "click":
            self.page.click(action["selector"])
        elif action_type == "fill_input":
            self.page.fill(action["selector"], action["value"])
        elif action_type == "select_option":
            self.page.select_option(action["selector"], action["value"])
        elif action_type == "import_file":
            file_path = action["file_path"].replace("\\", "/")
            self.page.evaluate(f"async () => {{ await window.SessionController.handleImportExcelFile('{file_path}'); }}")
            self.page.wait_for_selector(".sidebar-header-item, .tree-node", timeout=5000)
        elif action_type == "custom":
            for step in action.get("steps", []):
                s_action = step.get("action")
                if s_action == "click":
                    self.page.click(step["selector"])
                elif s_action == "fill":
                    self.page.fill(step["selector"], step["value"])
                elif s_action == "select":
                    self.page.select_option(step["selector"], step["value"])
                elif s_action == "evaluate":
                    self.page.evaluate(step["script"])

        # 2. Validate All Declared Element Invariants
        expected_states = flow_def.get("expected", {})
        for selector, rules in expected_states.items():
            self._validate_element_rules(flow_key, selector, rules)

    def _validate_element_rules(self, flow_key: str, selector: str, rules: dict):
        """Validates all specified assertion rules against a target locator."""
        loc = self.page.locator(selector)

        # Rule: visible (True / False)
        if "visible" in rules:
            if rules["visible"]:
                target = loc.first if rules.get("min_count", 0) > 0 or loc.count() > 1 else loc
                expect(target).to_be_visible(
                    timeout=3000
                )
            else:
                expect(loc).not_to_be_visible(timeout=3000)

        # Rule: enabled / disabled
        if "enabled" in rules:
            if rules["enabled"]:
                expect(loc).to_be_enabled(timeout=3000)
            else:
                expect(loc).to_be_disabled(timeout=3000)

        if "disabled" in rules:
            if rules["disabled"]:
                expect(loc).to_be_disabled(timeout=3000)
            else:
                expect(loc).to_be_enabled(timeout=3000)

        # Rule: has_class / has_not_class
        if "has_class" in rules:
            expect(loc).to_have_class(re.compile(rf"\b{rules['has_class']}\b"), timeout=3000)

        if "has_not_class" in rules:
            expect(loc).not_to_have_class(re.compile(rf"\b{rules['has_not_class']}\b"), timeout=3000)

        # Rule: text_contains
        if "text_contains" in rules:
            expect(loc).to_contain_text(rules["text_contains"], timeout=3000)

        # Rule: value
        if "value" in rules:
            expect(loc).to_have_value(rules["value"], timeout=3000)

        # Rule: min_count
        if "min_count" in rules:
            assert loc.count() >= rules["min_count"], (
                f"[{flow_key}] Expected locator '{selector}' to have at least {rules['min_count']} items, "
                f"but found {loc.count()}."
            )

        # Rule: min_options
        if "min_options" in rules:
            options_count = loc.locator("option").count()
            assert options_count >= rules["min_options"], (
                f"[{flow_key}] Expected select '{selector}' to have at least {rules['min_options']} options, "
                f"but found {options_count}."
            )
