"""Unit tests for HeaderService: extraction, deduplication, insertion-order preservation, and filtering."""

import pytest
from src.hierarchy_lib.services.header_service import HeaderService


def test_process_headers_trimming_and_stable_deduplication():
    """Trims whitespace and deduplicates while strictly preserving original first-seen insertion order."""
    raw_headers = ["  Category ", "Item A", "Item B", "", None, "  ", "Item A", "Category"]
    result = HeaderService.process_headers(raw_headers)
    assert result == ["Category", "Item A", "Item B"]


def test_process_headers_empty():
    assert HeaderService.process_headers([]) == []
    assert HeaderService.process_headers([None, "", "   "]) == []


def test_process_headers_preserves_original_column_sequence():
    """Headers must strictly preserve original left-to-right Excel column sequence without alphabetical sorting."""
    raw = ["Zebra", "apple", "Banana", "123", "Beta"]
    result = HeaderService.process_headers(raw)
    assert result == ["Zebra", "apple", "Banana", "123", "Beta"]


def test_filter_headers_matching():
    headers = ["Apple", "Banana", "Cherry", "Pineapple"]
    assert HeaderService.filter_headers(headers, "app") == ["Apple", "Pineapple"]
    assert HeaderService.filter_headers(headers, "") == ["Apple", "Banana", "Cherry", "Pineapple"]
    assert HeaderService.filter_headers(headers, "XYZ") == []
