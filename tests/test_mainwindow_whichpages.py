"""Unit tests for --whichpages support in Ghostscript crop flow."""

from pathlib import Path
from types import SimpleNamespace
import xml.etree.ElementTree as ET

import pytest

from pdfframe.mainwindow import MainWindow


class _FakeViewer:
    """Minimal viewer stub providing geometry and selection data for tests."""

    currentPageIndex = 0

    def numPages(self):
        return 3

    def cropValues(self, page_index):
        if page_index in (0, 1):
            return [(0.10, 0.10, 0.10, 0.10)]
        return []

    def pageGetSizePoints(self, page_index):
        del page_index
        return 1000.0, 2000.0


class _LargePageViewer:
    """Viewer stub for large-doc page-index filtering tests."""

    currentPageIndex = 0

    def numPages(self):
        return 14000

    def cropValues(self, page_index):
        if page_index == 13999:
            return [(0.10, 0.10, 0.10, 0.10)]
        return []

    def pageGetSizePoints(self, page_index):
        del page_index
        return 1000.0, 2000.0


def test_requested_unsupported_options_does_not_include_whichpages():
    """Arrange/Act/Assert: conversion flow exposes no unsupported option flags."""
    fake = SimpleNamespace()
    result = MainWindow.requestedUnsupportedGhostscriptOptions(fake)
    assert result == []


def test_build_ghostscript_crop_plan_filters_requested_pages():
    """Arrange/Act/Assert: single plan keeps requested first/last page bounds."""
    fake = SimpleNamespace(
        viewer=_FakeViewer(),
        selectedConversionMode=lambda: "frame",
        primarySelectionCropValue=lambda page_indexes: (0.10, 0.10, 0.10, 0.10),
    )
    plan = MainWindow.buildGhostscriptCropPlan(
        fake,
        "input.pdf",
        "out.pdf",
        requestedPageIndexes={1},
    )
    assert plan["page_indexes"] == [1]
    assert "-dFirstPage=2" in plan["command"]
    assert "-dLastPage=2" in plan["command"]


def test_build_ghostscript_crop_plan_supports_five_digit_page_indexes():
    """Arrange/Act/Assert: requested page ranges can include five-digit indexes."""
    fake = SimpleNamespace(
        viewer=_LargePageViewer(),
        selectedConversionMode=lambda: "frame",
        primarySelectionCropValue=lambda page_indexes: (0.10, 0.10, 0.10, 0.10),
    )
    plan = MainWindow.buildGhostscriptCropPlan(
        fake,
        "input.pdf",
        "out.pdf",
        requestedPageIndexes={13999},
    )
    assert plan["page_indexes"] == [13999]
    assert "-dFirstPage=14000" in plan["command"]
    assert "-dLastPage=14000" in plan["command"]


def test_build_ghostscript_crop_plan_uses_single_command_for_selected_range():
    """Arrange/Act/Assert: one command covers full selected range using primary selection."""
    fake = SimpleNamespace(
        viewer=_FakeViewer(),
        selectedConversionMode=lambda: "crop",
        primarySelectionCropValue=lambda page_indexes: (0.10, 0.10, 0.10, 0.10),
    )
    plan = MainWindow.buildGhostscriptCropPlan(
        fake,
        "input.pdf",
        "out.pdf",
        requestedPageIndexes={0, 1},
    )
    assert plan["page_indexes"] == [0, 1]
    assert "-dFirstPage=1" in plan["command"]
    assert "-dLastPage=2" in plan["command"]
    assert "<</BeginPage{0 0 800 1600 rectclip -100 -200 translate}>> setpagedevice" in plan["command"]


def test_str2pages_accepts_supported_single_range_forms():
    """Arrange/Act/Assert: parser accepts N, N-, -N, and N-M forms."""
    fake = SimpleNamespace(viewer=SimpleNamespace(numPages=lambda: 10))
    assert MainWindow.str2pages(fake, "3") == [2]
    assert MainWindow.str2pages(fake, "3-") == list(range(2, 10))
    assert MainWindow.str2pages(fake, "-3") == [0, 1, 2]
    assert MainWindow.str2pages(fake, "3-5") == [2, 3, 4]


def test_str2pages_rejects_unsupported_formats():
    """Arrange/Act/Assert: parser rejects comma lists and invalid ranges."""
    fake = SimpleNamespace(viewer=SimpleNamespace(numPages=lambda: 10))
    with pytest.raises(ValueError):
        MainWindow.str2pages(fake, "1-3,5")
    with pytest.raises(ValueError):
        MainWindow.str2pages(fake, "current")
    with pytest.raises(ValueError):
        MainWindow.str2pages(fake, "7-3")


def test_page_number_controls_allow_five_digit_display():
    """Arrange/Act/Assert: UI page-number controls are wider than four-digit slots."""
    ui_path = Path(__file__).resolve().parents[1] / "src" / "pdfframe" / "mainwindow.ui"
    root = ET.parse(ui_path).getroot()
    for widget_name in ("editCurrentPage", "editMaxPage"):
        widget = root.find(f".//widget[@name='{widget_name}']")
        assert widget is not None
        min_width = int(widget.find("./property[@name='minimumSize']/size/width").text)
        max_width = int(widget.find("./property[@name='maximumSize']/size/width").text)
        assert min_width >= 72
        assert max_width >= 72
def test_mode_selector_defaults_to_frame_in_runtime_code():
    """Arrange/Act/Assert: runtime initialization keeps Frame as default mode."""
    source_path = Path(__file__).resolve().parents[1] / "src" / "pdfframe" / "mainwindow.py"
    source = source_path.read_text(encoding="iso-8859-1")
    assert "self.radioModeFrame.setChecked(True)" in source
    assert 'mode = settings.value("PDF/Mode", "frame")' in source
    assert 'self.radioModeFrame.setChecked(mode != "crop")' in source


def test_conversion_trigger_label_is_go():
    """Arrange/Act/Assert: UI action label for conversion trigger is Go!."""
    ui_path = Path(__file__).resolve().parents[1] / "src" / "pdfframe" / "mainwindow.ui"
    root = ET.parse(ui_path).getroot()
    action = root.find(".//action[@name='actionPdfFrame']")
    assert action is not None
    text = action.find("./property[@name='text']/string")
    assert text is not None
    assert text.text == "Go!"
