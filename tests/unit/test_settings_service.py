"""Unit tests for SettingsService."""

import json

import pytest

from src.hierarchy_lib.services.settings_service import SettingsService


@pytest.fixture
def temp_config_path(tmp_path):
    """Provides a temporary config file path."""
    return str(tmp_path / "settings.json")


def test_default_settings_when_no_file(temp_config_path):
    SettingsService.reset_to_defaults(config_path=temp_config_path)
    settings = SettingsService.load_settings(config_path=temp_config_path)
    assert settings["delimiter"] == "\\"
    assert settings["default_data_type"] == "Text"


def test_update_settings_valid(temp_config_path):
    SettingsService.reset_to_defaults(config_path=temp_config_path)
    updated = SettingsService.update_settings(delimiter="/", default_data_type="Decimal", config_path=temp_config_path)
    assert updated["delimiter"] == "/"
    assert updated["default_data_type"] == "Decimal"

    # Verify persisted to disk
    with open(temp_config_path, "r", encoding="utf-8") as f:
        disk_data = json.load(f)
    assert disk_data["delimiter"] == "/"
    assert disk_data["default_data_type"] == "Decimal"


def test_update_settings_custom_multi_char_delimiter(temp_config_path):
    SettingsService.reset_to_defaults(config_path=temp_config_path)
    updated = SettingsService.update_settings(delimiter="::", config_path=temp_config_path)
    assert updated["delimiter"] == "::"


def test_validate_delimiter_rejection():
    with pytest.raises(ValueError, match="Delimiter cannot be empty"):
        SettingsService.validate_delimiter("")

    with pytest.raises(ValueError, match="Delimiter cannot be empty"):
        SettingsService.validate_delimiter("   ")

    with pytest.raises(ValueError, match="cannot exceed 3 characters"):
        SettingsService.validate_delimiter("////")


def test_validate_default_data_type_rejection():
    with pytest.raises(ValueError, match="Invalid data type"):
        SettingsService.validate_default_data_type("InvalidTypeXYZ")


def test_reset_to_defaults(temp_config_path):
    SettingsService.update_settings(delimiter="|", default_data_type="Integer", config_path=temp_config_path)
    reset = SettingsService.reset_to_defaults(config_path=temp_config_path)
    assert reset["delimiter"] == "\\"
    assert reset["default_data_type"] == "Text"
