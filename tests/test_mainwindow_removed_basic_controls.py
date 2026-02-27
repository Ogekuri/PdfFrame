"""Unit tests for removed Basic-tab conversion controls."""

from pathlib import Path
import xml.etree.ElementTree as ET

from pdfframe.jsonconfig import DEFAULT_CONFIG_VALUES
from pdfframe.mainwindow import MainWindow


def test_removed_basic_controls_are_absent_from_ui_xml():
    """Arrange/Act/Assert: removed conversion controls are no longer declared in UI."""
    ui_path = Path(__file__).resolve().parents[1] / "src" / "pdfframe" / "mainwindow.ui"
    root = ET.parse(ui_path).getroot()
    assert root.find(".//widget[@name='comboRotation']") is None
    assert root.find(".//widget[@name='checkGhostscript']") is None
    assert root.find(".//widget[@name='checkIncludePagesWithoutSelections']") is None


def test_removed_runtime_option_gate_and_optimize_config_key():
    """Arrange/Act/Assert: runtime no longer exposes removed options gate or optimize key."""
    assert not hasattr(MainWindow, "requestedUnsupportedGhostscriptOptions")
    assert "PDF/Optimize" not in DEFAULT_CONFIG_VALUES


def test_help_text_does_not_reference_removed_basic_controls():
    """Arrange/Act/Assert: Help tab text omits references to removed Basic controls."""
    ui_path = Path(__file__).resolve().parents[1] / "src" / "pdfframe" / "mainwindow.ui"
    source = ui_path.read_text(encoding="iso-8859-1")
    assert "Use Ghostscript to optimize" not in source
    assert "Include pages without selections" not in source
    assert "don't rotate" not in source
    assert "create individual selections for each page" not in source
