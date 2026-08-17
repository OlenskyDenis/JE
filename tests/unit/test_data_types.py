"""Unit tests for centralized standard Excel data types and validation logic."""

import pytest

from src.hierarchy_lib.models.data_types import VALID_DATA_TYPES, validate_data_type


def test_valid_data_types_content():
    """Verify that all 9 standard Excel data types are present in canonical order."""
    expected = (
        "Text",
        "Integer",
        "Decimal",
        "Currency",
        "Percentage",
        "Date",
        "Time",
        "DateTime",
        "Boolean",
    )
    assert VALID_DATA_TYPES == expected


def test_validate_data_type_valid_inputs():
    """Verify that valid inputs are properly normalized and returned."""
    assert validate_data_type("Text") == "Text"
    assert validate_data_type("text") == "Text"
    assert validate_data_type("  INTEGER  ") == "Integer"
    assert validate_data_type("decimal") == "Decimal"
    assert validate_data_type("currency") == "Currency"
    assert validate_data_type("percentage") == "Percentage"
    assert validate_data_type("date") == "Date"
    assert validate_data_type("time") == "Time"
    assert validate_data_type("datetime") == "DateTime"
    assert validate_data_type("boolean") == "Boolean"


def test_validate_data_type_empty_fallback():
    """Verify that None, empty string, or whitespace-only strings fallback to 'Text'."""
    assert validate_data_type("") == "Text"
    assert validate_data_type("   ") == "Text"
    assert validate_data_type(None) == "Text"


def test_validate_data_type_invalid_rejection():
    """Verify that unsupported data types raise ValueError."""
    with pytest.raises(ValueError, match="Invalid data type 'InvalidType'"):
        validate_data_type("InvalidType")
