"""Unit tests for annotation-fields feature wiring."""

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


def test_annotation_fields_checkboxes_exist_with_expected_order_and_defaults():
    """Arrange/Act/Assert: preserve/show controls are ordered and unchecked by default."""
    ui_path = Path(__file__).resolve().parents[1] / "src" / "pdfframe" / "mainwindow.ui"
    root = ET.parse(ui_path).getroot()
    preserve_widget = root.find(".//widget[@name='checkPreserveFields']")
    show_widget = root.find(".//widget[@name='checkShowAnnotsFields']")
    assert preserve_widget is not None
    assert show_widget is not None
    preserve_checked = preserve_widget.find("./property[@name='checked']/bool")
    show_checked = show_widget.find("./property[@name='checked']/bool")
    preserve_text = preserve_widget.find("./property[@name='text']/string")
    show_text = show_widget.find("./property[@name='text']/string")
    assert preserve_checked is not None
    assert show_checked is not None
    assert preserve_text is not None
    assert show_text is not None
    assert preserve_checked.text == "false"
    assert show_checked.text == "false"
    assert preserve_text.text == "Preserve annotations fields"
    assert show_text.text == "Show annotations fields"
    source = ui_path.read_text(encoding="iso-8859-1")
    assert source.index('name="checkPreserveFields"') < source.index('name="checkShowAnnotsFields"')
    assert source.index('name="checkPreserveFields"') < source.index('name="groupWhichPages"')


def test_build_crop_plan_passes_annotation_fields_flags_to_command_builder(monkeypatch):
    """Arrange/Act/Assert: plan builder forwards preserve/show bools into command args."""
    captured = {}

    def _fake_command_builder(*args, **kwargs):
        del args
        captured["preserve_annots"] = kwargs["preserve_annots"]
        captured["show_annots"] = kwargs["show_annots"]
        return ["gs"]

    monkeypatch.setattr(mainwindow_module, "build_ghostscript_page_crop_command", _fake_command_builder)
    fake = SimpleNamespace(
        viewer=SimpleNamespace(numPages=lambda: 2, pageGetSizePoints=lambda idx: (1000.0, 2000.0), currentPageIndex=0),
        selectedConversionMode=lambda: "frame",
        primarySelectionCropValue=lambda page_indexes: (0.10, 0.10, 0.10, 0.10),
        ui=SimpleNamespace(
            checkPreserveFields=_FakeCheckBox(True),
            checkShowAnnotsFields=_FakeCheckBox(False),
        ),
    )
    plan = MainWindow.buildGhostscriptCropPlan(fake, "input.pdf", "out.pdf", requestedPageIndexes={0})
    assert plan["command"] == ["gs"]
    assert captured["preserve_annots"] is True
    assert captured["show_annots"] is False
