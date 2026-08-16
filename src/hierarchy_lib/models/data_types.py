"""Centralized standard Excel column data types and validation logic."""

from typing import Tuple

VALID_DATA_TYPES: Tuple[str, ...] = (
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


def validate_data_type(data_type: str) -> str:
    """Validates and returns normalized canonical standard Excel data type string."""
    if not data_type or not str(data_type).strip():
        return "Text"
    clean = str(data_type).strip()
    for valid in VALID_DATA_TYPES:
        if clean.lower() == valid.lower():
            return valid
    raise ValueError(f"Invalid data type '{data_type}'. Expected one of: {', '.join(VALID_DATA_TYPES)}")
