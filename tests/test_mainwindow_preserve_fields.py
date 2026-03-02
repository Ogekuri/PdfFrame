"""Unit tests for Delete annotations fields feature wiring."""

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


def test_annotation_fields_checkbox_exists_with_expected_defaults():
    """Arrange/Act/Assert: delete-annots control is present and checked by default."""
    ui_path = Path(__file__).resolve().parents[1] / "src" / "pdfframe" / "mainwindow.ui"
    root = ET.parse(ui_path).getroot()
    delete_widget = root.find(".//widget[@name='checkDeleteAnnotsFields']")
    assert delete_widget is not None
    checked = delete_widget.find("./property[@name='checked']/bool")
    text = delete_widget.find("./property[@name='text']/string")
    assert checked is not None
    assert text is not None
    assert checked.text == "true"
    assert text.text == "Delete annotations fields"
    source = ui_path.read_text(encoding="iso-8859-1")
    assert source.index('name="checkDeleteAnnotsFields"') < source.index('name="groupWhichPages"')


def test_build_crop_plan_passes_delete_annots_flag(monkeypatch):
    """Arrange/Act/Assert: plan builder includes delete_annots from checkbox state."""
    fake = SimpleNamespace(
        viewer=SimpleNamespace(numPages=lambda: 2, pageGetSizePoints=lambda idx: (1000.0, 2000.0), currentPageIndex=0),
        selectedConversionMode=lambda: "frame",
        primarySelectionCropValue=lambda page_indexes: (0.10, 0.10, 0.10, 0.10),
        ui=SimpleNamespace(
            checkDeleteAnnotsFields=_FakeCheckBox(True),
        ),
    )
    plan = MainWindow.buildCropPlan(fake, "input.pdf", "out.pdf", requestedPageIndexes={0})
    assert plan is not None
    assert plan["delete_annots"] is True


def test_build_crop_plan_delete_annots_false_when_unchecked(monkeypatch):
    """Arrange/Act/Assert: unchecked delete-annots checkbox sets flag to False."""
    fake = SimpleNamespace(
        viewer=SimpleNamespace(numPages=lambda: 2, pageGetSizePoints=lambda idx: (1000.0, 2000.0), currentPageIndex=0),
        selectedConversionMode=lambda: "crop",
        primarySelectionCropValue=lambda page_indexes: (0.10, 0.10, 0.10, 0.10),
        ui=SimpleNamespace(
            checkDeleteAnnotsFields=_FakeCheckBox(False),
        ),
    )
    plan = MainWindow.buildCropPlan(fake, "input.pdf", "out.pdf", requestedPageIndexes={0})
    assert plan is not None
    assert plan["delete_annots"] is False
