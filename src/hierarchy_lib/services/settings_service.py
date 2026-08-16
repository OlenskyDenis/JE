"""SettingsService for managing application preferences and persistence in settings.json."""

import json
import os
from typing import Dict, Any, Optional, Tuple
from src.hierarchy_lib.models.data_types import VALID_DATA_TYPES, validate_data_type


class SettingsService:
    """Service managing application settings, persistence, and validation."""

    DEFAULT_DELIMITER = "\\"
    DEFAULT_DATA_TYPE = "Text"
    MAX_DELIMITER_LENGTH = 3

    VALID_DATA_TYPES: Tuple[str, ...] = VALID_DATA_TYPES

    DEFAULT_SETTINGS: Dict[str, str] = {
        "delimiter": DEFAULT_DELIMITER,
        "default_data_type": DEFAULT_DATA_TYPE
    }

    _active_settings: Dict[str, str] = dict(DEFAULT_SETTINGS)

    @classmethod
    def get_config_path(cls, custom_path: Optional[str] = None) -> str:
        """Resolves absolute path to settings.json."""
        if custom_path:
            return os.path.abspath(custom_path)
        # Default to repo root directory (two levels up from this file)
        repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        return os.path.join(repo_root, "settings.json")

    @classmethod
    def validate_delimiter(cls, delimiter: Optional[str]) -> str:
        """Validates path delimiter (must be non-empty, 1-3 characters)."""
        if delimiter is None:
            return cls.DEFAULT_DELIMITER
        delim_str = str(delimiter).strip()
        if not delim_str:
            raise ValueError("Delimiter cannot be empty or whitespace only.")
        if len(delim_str) > cls.MAX_DELIMITER_LENGTH:
            raise ValueError(f"Delimiter length cannot exceed {cls.MAX_DELIMITER_LENGTH} characters.")
        return delim_str

    @classmethod
    def validate_default_data_type(cls, data_type: Optional[str]) -> str:
        """Validates default data type against VALID_DATA_TYPES."""
        if not data_type or not str(data_type).strip():
            return cls.DEFAULT_DATA_TYPE
        return validate_data_type(data_type)

    @classmethod
    def load_settings(cls, config_path: Optional[str] = None) -> Dict[str, str]:
        """Loads settings from settings.json file or falls back to defaults."""
        path = cls.get_config_path(config_path)
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                delimiter = cls.validate_delimiter(data.get("delimiter", cls.DEFAULT_DELIMITER))
                default_data_type = cls.validate_default_data_type(data.get("default_data_type", cls.DEFAULT_DATA_TYPE))
                cls._active_settings = {
                    "delimiter": delimiter,
                    "default_data_type": default_data_type
                }
            except Exception:
                # In case of corrupted file, fallback safely to defaults
                cls._active_settings = dict(cls.DEFAULT_SETTINGS)
        else:
            cls._active_settings = dict(cls.DEFAULT_SETTINGS)

        return dict(cls._active_settings)

    @classmethod
    def get_settings(cls, config_path: Optional[str] = None) -> Dict[str, str]:
        """Returns current active settings dictionary."""
        if not cls._active_settings:
            return cls.load_settings(config_path)
        return dict(cls._active_settings)

    @classmethod
    def get_delimiter(cls) -> str:
        """Returns active path delimiter."""
        return cls._active_settings.get("delimiter", cls.DEFAULT_DELIMITER)

    @classmethod
    def get_default_data_type(cls) -> str:
        """Returns active default data type for unassigned/General columns."""
        return cls._active_settings.get("default_data_type", cls.DEFAULT_DATA_TYPE)

    @classmethod
    def save_settings(cls, settings: Dict[str, str], config_path: Optional[str] = None) -> None:
        """Persists settings dictionary to settings.json atomically."""
        path = cls.get_config_path(config_path)
        dir_name = os.path.dirname(path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        temp_path = f"{path}.tmp"
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        if os.path.exists(path):
            os.replace(temp_path, path)
        else:
            os.rename(temp_path, path)

    @classmethod
    def update_settings(
        cls,
        delimiter: Optional[str] = None,
        default_data_type: Optional[str] = None,
        config_path: Optional[str] = None
    ) -> Dict[str, str]:
        """Validates, updates, and persists settings."""
        valid_delimiter = cls.validate_delimiter(delimiter) if delimiter is not None else cls.get_delimiter()
        valid_type = cls.validate_default_data_type(default_data_type) if default_data_type is not None else cls.get_default_data_type()

        new_settings = {
            "delimiter": valid_delimiter,
            "default_data_type": valid_type
        }
        cls._active_settings = new_settings
        cls.save_settings(new_settings, config_path)
        return dict(cls._active_settings)

    @classmethod
    def reset_to_defaults(cls, config_path: Optional[str] = None) -> Dict[str, str]:
        """Resets settings to defaults and saves to disk."""
        cls._active_settings = dict(cls.DEFAULT_SETTINGS)
        cls.save_settings(cls._active_settings, config_path)
        return dict(cls._active_settings)
