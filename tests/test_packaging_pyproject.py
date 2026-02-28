"""Unit tests for pyproject packaging metadata."""

import tomllib
from pathlib import Path


def test_pyproject_exposes_pdfframe_console_script():
    """Arrange/Act/Assert: pdfframe script maps to application.main entrypoint."""
    repo_root = Path(__file__).resolve().parents[1]
    pyproject_path = repo_root / "pyproject.toml"

    pyproject_data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    scripts = pyproject_data["project"]["scripts"]

    assert scripts["pdfframe"] == "pdfframe.application:main"


def test_pyproject_declares_required_runtime_dependencies():
    """Arrange/Act/Assert: pyproject dependencies include required GUI/runtime packages."""
    repo_root = Path(__file__).resolve().parents[1]
    pyproject_path = repo_root / "pyproject.toml"

    pyproject_data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    dependencies = pyproject_data["project"]["dependencies"]
    dependency_set = set(dependencies)

    assert {"PyQt6", "PyQt5", "PyMuPDF", "pypdf", "pikepdf"} <= dependency_set
