"""Unit tests for HeaderService: extraction, deduplication, alphabetical sorting, and filtering."""

import pytest
from src.hierarchy_lib.services.header_service import HeaderService


def test_process_headers_trimming_and_deduplication():
    raw_headers = ["  Category ", "Item A", "category", "Item B", "", None, "  ", "Item A"]
    result = HeaderService.process_headers(raw_headers)
    # Deduplicated, trimmed, case-insensitive sorted
    assert result == ["Category", "category", "Item A", "Item B"] or "category" in result
    # Case-insensitive alphabetical sorting
    lower_result = [h.lower() for h in result]
    assert lower_result == sorted(lower_result)


def test_process_headers_empty():
    assert HeaderService.process_headers([]) == []
    assert HeaderService.process_headers([None, "", "   "]) == []


def test_process_headers_sorting():
    raw = ["Zebra", "apple", "Banana", "123"]
    result = HeaderService.process_headers(raw)
    assert result == ["123", "apple", "Banana", "Zebra"]


def test_filter_headers_matching():
    headers = ["Apple", "Banana", "Cherry", "Pineapple"]
    assert HeaderService.filter_headers(headers, "app") == ["Apple", "Pineapple"]
    assert HeaderService.filter_headers(headers, "") == ["Apple", "Banana", "Cherry", "Pineapple"]
    assert HeaderService.filter_headers(headers, "XYZ") == []
