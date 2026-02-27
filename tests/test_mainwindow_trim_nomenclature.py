"""Unit tests for trim grayscale-sensitivity nomenclature."""

from pathlib import Path


def test_trim_ui_uses_grayscale_sensitivity_label_tooltip_and_help_text():
    """Arrange/Act/Assert: generated UI text uses the renamed trim nomenclature."""
    ui_qt6_path = Path(__file__).resolve().parents[1] / "src" / "pdfframe" / "mainwindowui_qt6.py"
    ui_qt6 = ui_qt6_path.read_text(encoding="iso-8859-1")
    assert 'self.labelGrayscaleSensitivity.setText(_translate("MainWindow", "Grayscale sensitivity:"))' in ui_qt6
    assert "Maximum number of grayscale transitions tolerated on each inspected line while auto-trimming margins." in ui_qt6
    assert "Grayscale sensitivity controls how many grayscale transitions are accepted while trimming." in ui_qt6


def test_trim_runtime_persistence_keys_use_grayscale_sensitivity():
    """Arrange/Act/Assert: runtime config and presets use renamed grayscale keys."""
    source_root = Path(__file__).resolve().parents[1] / "src" / "pdfframe"
    mainwindow_source = (source_root / "mainwindow.py").read_text(encoding="iso-8859-1")
    jsonconfig_source = (source_root / "jsonconfig.py").read_text(encoding="iso-8859-1")
    assert '"Trim/GrayscaleSensitivity"' in mainwindow_source
    assert '"grayscale_sensitivity"' in mainwindow_source
    assert '"Trim/GrayscaleSensitivity"' in jsonconfig_source
