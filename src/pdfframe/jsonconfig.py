# -*- coding: iso-8859-1 -*-

"""
JSON-backed user configuration storage for pdfframe.
"""

import json
from copy import deepcopy
from pathlib import Path


DEFAULT_CONFIG_VALUES = {
    "PDF/PreserveFields": False,
    "PDF/Mode": "frame",
    "Trim/Padding": "0",
    "Trim/GrayscaleSensitivity": "0",
    "Trim/Sensitivity": "5",
    "Trim/PagesRangeEnabled": False,
    "Trim/PagesRange": "1-1",
}


def default_config_path():
    """
    @brief Returns canonical user JSON configuration path.
    @details Resolves `~/.pdfframe/config.json` using current user home directory.
    @return {pathlib.Path} Expanded configuration file path.
    """
    return Path.home() / ".pdfframe" / "config.json"


def default_config_document():
    """
    @brief Returns default JSON configuration document.
    @details Includes top-level `config` object seeded from `DEFAULT_CONFIG_VALUES` and empty `presets` array.
    @return {dict[str,object]} Default config document payload.
    """
    return {"config": deepcopy(DEFAULT_CONFIG_VALUES), "presets": []}


class JsonConfigStore:
    """
    @brief Provides normalized JSON config read/write operations.
    @details Enforces top-level `config` and `presets` sections and guarantees default keys for config values.
    """

    def __init__(self, path=None):
        """
        @brief Initializes JSON config store.
        @details Uses explicit path when provided; otherwise defaults to `~/.pdfframe/config.json`.
        @param path {str|pathlib.Path|None} Optional configuration path override.
        """
        self.path = Path(path).expanduser() if path is not None else default_config_path()

    def _normalize_document(self, document):
        """
        @brief Normalizes JSON config document shape.
        @details Validates root object and top-level section types, merges missing default config keys, and guarantees list type for presets.
        @param document {dict[str,object]} Raw decoded JSON payload.
        @return {dict[str,object]} Normalized document.
        @throws {ValueError} If root or required sections have incompatible types.
        """
        if not isinstance(document, dict):
            raise ValueError("JSON config root must be an object.")
        raw_config = document.get("config", {})
        if raw_config is None:
            raw_config = {}
        if not isinstance(raw_config, dict):
            raise ValueError("JSON config `config` section must be an object.")
        raw_presets = document.get("presets", [])
        if raw_presets is None:
            raw_presets = []
        if not isinstance(raw_presets, list):
            raise ValueError("JSON config `presets` section must be an array.")

        config_values = deepcopy(DEFAULT_CONFIG_VALUES)
        config_values.update(raw_config)
        return {"config": config_values, "presets": list(raw_presets)}

    def load_or_initialize(self):
        """
        @brief Loads JSON configuration and creates defaults when missing.
        @details Creates `~/.pdfframe/config.json` when absent, normalizes loaded documents, and writes back normalization deltas.
        @return {dict[str,object]} Normalized configuration document.
        @throws {OSError} If filesystem operations fail.
        @throws {ValueError} If existing JSON document has invalid structure.
        @throws {json.JSONDecodeError} If existing JSON file is syntactically invalid.
        """
        if not self.path.exists():
            document = default_config_document()
            self.save(document)
            return document
        with self.path.open("r", encoding="utf-8") as handle:
            decoded = json.load(handle)
        normalized = self._normalize_document(decoded)
        if normalized != decoded:
            self.save(normalized)
        return normalized

    def save(self, document):
        """
        @brief Writes normalized JSON configuration to disk.
        @details Validates/normalizes payload, ensures parent directory exists, and serializes with deterministic indentation.
        @param document {dict[str,object]} Document payload to persist.
        @return {None} Performs filesystem writes.
        @throws {OSError} If write operation fails.
        @throws {ValueError} If payload has invalid structure.
        """
        normalized = self._normalize_document(document)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(normalized, handle, indent=2, ensure_ascii=True)
            handle.write("\n")
