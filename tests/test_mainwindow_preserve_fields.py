"""Unit tests for Preserve fields feature wiring."""

from pathlib import Path
from types import SimpleNamespace
import xml.etree.ElementTree as ET

from pdfframe import mainwindow as mainwindow_module
from pdfframe.mainwindow import MainWindow


class _FakeCheckBox:
    """Checkbox stub returning configured checked state."""

    def __init__(self, checked):
        self._checked = checked

    def isChecked(self):
        return self._checked


def test_preserve_fields_checkbox_exists_before_other_pdf_operations():
    """Arrange/Act/Assert: Preserve fields is present first and unchecked by default."""
    ui_path = Path(__file__).resolve().parents[1] / "src" / "pdfframe" / "mainwindow.ui"
    root = ET.parse(ui_path).getroot()
    widget = root.find(".//widget[@name='checkPreserveFields']")
    assert widget is not None
    checked = widget.find("./property[@name='checked']/bool")
    assert checked is not None
    assert checked.text == "false"
    source = ui_path.read_text(encoding="iso-8859-1")
    assert source.index('name="checkPreserveFields"') < source.index('name="comboRotation"')
    assert source.index('name="checkPreserveFields"') < source.index('name="checkGhostscript"')


def test_build_crop_plan_passes_preserve_fields_flag_to_command_builder(monkeypatch):
    """Arrange/Act/Assert: plan builder forwards preserve-fields bool into command args."""
    captured = {}

    def _fake_command_builder(*args, **kwargs):
        del args
        captured["preserve_annots"] = kwargs["preserve_annots"]
        return ["gs"]

    monkeypatch.setattr(mainwindow_module, "build_ghostscript_page_crop_command", _fake_command_builder)
    fake = SimpleNamespace(
        viewer=SimpleNamespace(numPages=lambda: 2, pageGetSizePoints=lambda idx: (1000.0, 2000.0), currentPageIndex=0),
        selectedConversionMode=lambda: "frame",
        primarySelectionCropValue=lambda page_indexes: (0.10, 0.10, 0.10, 0.10),
        ui=SimpleNamespace(checkPreserveFields=_FakeCheckBox(True)),
    )
    plan = MainWindow.buildGhostscriptCropPlan(fake, "input.pdf", "out.pdf", requestedPageIndexes={0})
    assert plan["command"] == ["gs"]
    assert captured["preserve_annots"] is True
