"""Automated Model-Based Interaction Matrix Test Suite for JE Component Topology."""

import pytest
from playwright.sync_api import Page

from tests.matrix.contracts_manifest import INTERACTION_FLOWS
from tests.matrix.executor import MatrixFlowExecutor


@pytest.mark.e2e
@pytest.mark.parametrize("flow_key", list(INTERACTION_FLOWS.keys()))
def test_declarative_interaction_flow_isolated(page: Page, flow_key: str):
    """Executes each declarative interaction flow in isolation, verifying global state invariants."""
    executor = MatrixFlowExecutor(page)

    # For downstream flows that depend on an imported session, auto-bootstrap import first
    dependent_flows = [
        "flow_template_badge_sync",
        "flow_switch_active_sheet",
        "flow_switch_catalog_sheet_independent",
        "flow_sidebar_search_filter",
        "flow_switch_to_matrix_view",
        "flow_switch_to_unique_levels_view",
        "flow_switch_back_to_tree_view",
        "flow_sidebar_tab_paths",
        "flow_settings_modal_delimiter_change",
    ]

    if flow_key in dependent_flows:
        executor.execute_flow("flow_import_multisheet_excel", INTERACTION_FLOWS["flow_import_multisheet_excel"])

    # Execute the target flow and validate its full-system contract
    flow_def = INTERACTION_FLOWS[flow_key]
    executor.execute_flow(flow_key, flow_def)


@pytest.mark.e2e
def test_full_state_transition_chain(page: Page):
    """Executes a complete end-to-end chained sequence through all flows without page reload."""
    executor = MatrixFlowExecutor(page)

    chain_sequence = [
        "flow_empty_workspace",
        "flow_import_multisheet_excel",
        "flow_template_badge_sync",
        "flow_switch_active_sheet",
        "flow_switch_catalog_sheet_independent",
        "flow_sidebar_search_filter",
        "flow_switch_to_matrix_view",
        "flow_switch_to_unique_levels_view",
        "flow_switch_back_to_tree_view",
        "flow_sidebar_tab_paths",
        "flow_settings_modal_delimiter_change",
        "flow_sidebar_collapse_and_expand",
        "flow_bilingual_toggle_en_uk",
    ]

    for step_key in chain_sequence:
        executor.execute_flow(step_key, INTERACTION_FLOWS[step_key])

