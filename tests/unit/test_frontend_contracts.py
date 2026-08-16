import re
from pathlib import Path
import pytest

WEB_DIR = Path(__file__).resolve().parent.parent.parent / "src" / "web"
JS_DIR = WEB_DIR / "js"
HTML_FILE = WEB_DIR / "index.html"


def _extract_i18n_keys():
    """Helper to extract all dictionary keys for 'uk' and 'en' from i18n.js."""
    i18n_file = JS_DIR / "i18n.js"
    content = i18n_file.read_text(encoding="utf-8")

    # Isolate I18N_DICTIONARIES block before const I18n
    dict_block = content
    if "const I18n" in content:
        dict_block = content.split("const I18n")[0]

    # Split by dictionary declarations
    uk_part = ""
    en_part = ""

    if "uk:" in dict_block and "en:" in dict_block:
        parts = dict_block.split("en:")
        uk_part = parts[0]
        en_part = parts[1]

    uk_keys = set(re.findall(r'^\s*([a-zA-Z0-9_]+)\s*:', uk_part, re.MULTILINE))
    uk_keys.discard("uk")
    uk_keys.discard("I18N_DICTIONARIES")

    en_keys = set(re.findall(r'^\s*([a-zA-Z0-9_]+)\s*:', en_part, re.MULTILINE))
    en_keys.discard("en")

    return uk_keys, en_keys


class TestFrontendContracts:
    """Automated integrity and contract tests for Frontend JavaScript, HTML, and I18n."""

    def test_all_script_tags_exist(self):
        """Verify that all script tags in index.html reference existing files on disk."""
        assert HTML_FILE.exists(), f"index.html not found at {HTML_FILE}"
        html_content = HTML_FILE.read_text(encoding="utf-8")

        script_srcs = re.findall(r'<script\s+[^>]*src=["\']([^"\']+)["\']', html_content)
        assert len(script_srcs) > 0, "No script tags found in index.html"

        for src in script_srcs:
            # Skip external scripts or eel dynamic injection (/eel.js, eel.js)
            if src.startswith("http") or src.startswith("//") or src.endswith("eel.js"):
                continue
            target_path = WEB_DIR / src
            assert target_path.exists(), f"Script referenced in index.html does not exist: {src} -> {target_path}"

    def test_i18n_methods_integrity(self):
        """Verify that any I18n.<method>() called across all JS files exists in i18n.js."""
        i18n_file = JS_DIR / "i18n.js"
        assert i18n_file.exists(), f"i18n.js not found at {i18n_file}"
        i18n_content = i18n_file.read_text(encoding="utf-8")

        # Extract method names defined inside const I18n = { ... }
        declared_methods = set(re.findall(r'^\s*([a-zA-Z0-9_]+)\s*\([^)]*\)\s*\{', i18n_content, re.MULTILINE))
        declared_methods.update(re.findall(r'([a-zA-Z0-9_]+)\s*:\s*function', i18n_content))

        assert "t" in declared_methods
        assert "getTypeLabel" in declared_methods

        # Check all JS files for I18n.<methodName>(
        js_files = list(JS_DIR.glob("*.js"))
        for js_file in js_files:
            content = js_file.read_text(encoding="utf-8")
            calls = re.findall(r'\bI18n\.([a-zA-Z0-9_]+)\s*\(', content)
            for call in calls:
                assert call in declared_methods, (
                    f"Undefined I18n method '{call}' called in {js_file.name}. "
                    f"Declared methods in i18n.js: {sorted(list(declared_methods))}"
                )

    def test_dom_ids_exist_in_html(self):
        """Verify that any document.getElementById('...') in JS files exists in index.html."""
        html_content = HTML_FILE.read_text(encoding="utf-8")
        html_ids = set(re.findall(r'\bid=["\']([^"\']+)["\']', html_content))

        js_files = list(JS_DIR.glob("*.js"))
        for js_file in js_files:
            content = js_file.read_text(encoding="utf-8")
            referenced_ids = re.findall(r'getElementById\(["\']([^"\']+)["\']\)', content)
            for rid in referenced_ids:
                assert rid in html_ids, (
                    f"DOM ID '{rid}' referenced via document.getElementById in {js_file.name} "
                    f"was not found in index.html."
                )

    def test_i18n_dictionaries_parity(self):
        """Verify that Ukrainian ('uk') and English ('en') dictionaries have identical key sets."""
        uk_keys, en_keys = _extract_i18n_keys()

        assert len(uk_keys) > 20, "Failed to extract Ukrainian keys"
        assert len(en_keys) > 20, "Failed to extract English keys"

        missing_in_en = uk_keys - en_keys
        missing_in_uk = en_keys - uk_keys

        assert not missing_in_en, f"Keys present in 'uk' but missing in 'en': {missing_in_en}"
        assert not missing_in_uk, f"Keys present in 'en' but missing in 'uk': {missing_in_uk}"

    def test_html_data_i18n_attributes_valid(self):
        """Verify that all data-i18n and data-i18n-attr tags in index.html exist in i18n dictionaries."""
        uk_keys, en_keys = _extract_i18n_keys()
        html_content = HTML_FILE.read_text(encoding="utf-8")

        # Check data-i18n="my_key"
        data_i18n_keys = re.findall(r'data-i18n=["\']([^"\']+)["\']', html_content)
        for key in data_i18n_keys:
            assert key in uk_keys, f"data-i18n key '{key}' in index.html is not defined in i18n.js"

        # Check data-i18n-attr="title:my_key" or "placeholder:my_key"
        data_i18n_attr_entries = re.findall(r'data-i18n-attr=["\']([^"\']+)["\']', html_content)
        for entry in data_i18n_attr_entries:
            for pair in entry.split(";"):
                if ":" in pair:
                    _, key = pair.split(":", 1)
                    key = key.strip()
                    assert key in uk_keys, f"data-i18n-attr key '{key}' in index.html is not defined in i18n.js"

    def test_unique_level_renderer_contract(self):
        """Verify that unique_level_renderer.js implements required API methods and partitions leaves."""
        js_file = JS_DIR / "unique_level_renderer.js"
        assert js_file.exists(), f"unique_level_renderer.js not found at {js_file}"
        content = js_file.read_text(encoding="utf-8")

        assert "extractUniqueLevels(roots)" in content
        assert "renderUniqueLevels(roots, containerEl)" in content
        assert "level-group-leaves" in content
        assert "level-group-branches" in content
        assert "level-group-separator" in content
        assert "level_subgroup_leaves" in content
        assert "level_subgroup_branches" in content

