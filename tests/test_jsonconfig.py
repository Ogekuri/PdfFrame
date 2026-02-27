"""Unit tests for JSON configuration bootstrap and persistence."""

import json

from pdfframe.jsonconfig import DEFAULT_CONFIG_VALUES, JsonConfigStore


def test_json_config_bootstrap_creates_defaults_when_missing(tmp_path):
    """Arrange/Act/Assert: missing config file is created with default sections."""
    config_path = tmp_path / ".pdfframe" / "config.json"
    store = JsonConfigStore(config_path)
    document = store.load_or_initialize()

    assert config_path.exists()
    assert document["config"] == DEFAULT_CONFIG_VALUES
    assert document["presets"] == []


def test_json_config_preserves_persisted_values_and_fills_missing_defaults(tmp_path):
    """Arrange/Act/Assert: persisted config keys override hardcoded defaults."""
    config_path = tmp_path / ".pdfframe" / "config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        json.dumps(
            {
                "config": {"PDF/Mode": "crop", "Trim/Sensitivity": "9"},
                "presets": [{"name": "Preset A", "crop": [0.1, 0.2, 0.3, 0.4]}],
            }
        ),
        encoding="utf-8",
    )
    store = JsonConfigStore(config_path)
    document = store.load_or_initialize()

    assert document["config"]["PDF/Mode"] == "crop"
    assert document["config"]["Trim/Sensitivity"] == "9"
    assert document["config"]["Trim/Padding"] == DEFAULT_CONFIG_VALUES["Trim/Padding"]
    assert document["presets"][0]["name"] == "Preset A"
