"""Unit tests for trim pages-range behavior."""

from types import SimpleNamespace
from pathlib import Path

from pdfframe import mainwindow as mainwindow_module
from pdfframe.mainwindow import MainWindow


class _FakeLineEdit:
    """Line-edit stub for pages-range tests."""

    def __init__(self, text):
        self._text = text
        self._enabled = True

    def text(self):
        return self._text

    def setText(self, value):
        self._text = value

    def setEnabled(self, enabled):
        self._enabled = enabled

    def isEnabled(self):
        return self._enabled


class _FakeCheckBox:
    """Checkbox stub for pages-range tests."""

    def __init__(self, checked=False):
        self._checked = checked

    def isChecked(self):
        return self._checked


class _FakeQApplication:
    """QApplication stub for cursor API calls used during trim."""

    @staticmethod
    def setOverrideCursor(_cursor):
        return None

    @staticmethod
    def restoreOverrideCursor():
        return None


class _FakeViewerMultiPage:
    """Viewer stub returning three pages and available page images."""

    def __init__(self):
        self.currentPageIndex = 1

    def numPages(self):
        return 3

    def getImage(self, idx):
        del idx
        return object()


class _FakeSelection:
    """Selection stub with visible pages and geometry APIs."""

    def __init__(self):
        self.rect = mainwindow_module.QRectF(0, 0, 10, 10)
        self.aspectRatio = None

    def mapRectToImage(self, rect):
        del rect
        return mainwindow_module.QRectF(0, 0, 10, 10)

    def mapRectFromImage(self, rect):
        return rect

    def setBoundingRect(self, top_left, bottom_right):
        del top_left, bottom_right
        return None

    def selectionVisibleOnPage(self, page_index):
        del page_index
        return True


class _FakeTrimWindow:
    """MainWindow-like stub for pages-range trim logic."""

    def __init__(self, pages_range="1-1", enabled=True):
        self.viewer = _FakeViewerMultiPage()
        self.ui = SimpleNamespace(
            editSensitivity=_FakeLineEdit("5"),
            editGrayscaleSensitivity=_FakeLineEdit("0"),
            editPadding=_FakeLineEdit("0"),
            checkTrimPagesRange=_FakeCheckBox(enabled),
            editTrimPagesRange=_FakeLineEdit(pages_range),
        )
        self.warnings = []

    def tr(self, text):
        return text

    def showWarning(self, title, text):
        self.warnings.append((title, text))

    def getPadding(self):
        return [0.0, 0.0, 0.0, 0.0]

    def _parseTrimPagesRange(self):
        return MainWindow._parseTrimPagesRange(self)


def test_trim_pages_range_parser_accepts_n_m_format():
    """Arrange/Act/Assert: parser accepts one-based inclusive N-M format."""
    fake = SimpleNamespace(ui=SimpleNamespace(editTrimPagesRange=_FakeLineEdit("2-5")))
    assert MainWindow._parseTrimPagesRange(fake) == (1, 4)


def test_trim_pages_range_parser_rejects_invalid_format_or_bounds():
    """Arrange/Act/Assert: parser rejects non N-M or descending ranges."""
    fake = SimpleNamespace(ui=SimpleNamespace(editTrimPagesRange=_FakeLineEdit("bad")))
    try:
        MainWindow._parseTrimPagesRange(fake)
        assert False, "Expected ValueError for invalid format"
    except ValueError:
        pass
    fake.ui.editTrimPagesRange.setText("5-2")
    try:
        MainWindow._parseTrimPagesRange(fake)
        assert False, "Expected ValueError for descending bounds"
    except ValueError:
        pass


def test_trim_pages_range_toggle_enables_input_and_defaults_to_1_1():
    """Arrange/Act/Assert: range input is toggle-gated and defaults to 1-1 when empty."""
    fake = SimpleNamespace(ui=SimpleNamespace(editTrimPagesRange=_FakeLineEdit("")))
    MainWindow._updateTrimPagesRangeControls(fake, False)
    assert fake.ui.editTrimPagesRange.isEnabled() is False
    assert fake.ui.editTrimPagesRange.text() == "1-1"
    MainWindow._updateTrimPagesRangeControls(fake, True)
    assert fake.ui.editTrimPagesRange.isEnabled() is True


def test_trim_pages_range_invalid_value_warns_and_falls_back(monkeypatch):
    """Arrange/Act/Assert: invalid pages range warns and trims fallback 1-1 range only."""
    fake = _FakeTrimWindow(pages_range="oops", enabled=True)
    selection = _FakeSelection()
    calls = []

    def _fake_auto_trim(img, orect, nrect, sensitivity, grayscale_sensitivity):
        del img, sensitivity, grayscale_sensitivity
        calls.append(1)
        return orect if nrect is None else nrect

    monkeypatch.setattr(mainwindow_module, "QApplication", _FakeQApplication)
    monkeypatch.setattr(mainwindow_module, "autoTrimMargins", _fake_auto_trim)
    MainWindow.trimMarginsSelection(fake, selection)
    assert len(calls) == 1
    assert fake.ui.editTrimPagesRange.text() == "1-1"
    assert fake.warnings


def test_trim_pages_range_ui_contains_label_and_separator():
    """Arrange/Act/Assert: UI defines pages-range label and horizontal separator."""
    source_path = Path(__file__).resolve().parents[1] / "src" / "pdfframe" / "mainwindow.ui"
    source = source_path.read_text(encoding="iso-8859-1")
    assert 'name="checkTrimPagesRange"' in source
    assert "Trim pages range" in source
    assert 'name="labelTrimPagesRange"' in source
    assert "Pages range:" in source
    assert 'name="lineTrimPagesRangeSeparator"' in source
