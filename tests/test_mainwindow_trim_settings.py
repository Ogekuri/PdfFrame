"""Unit tests for Trim Margins configuration handling."""

from types import SimpleNamespace
from pathlib import Path

from pdfframe import mainwindow as mainwindow_module
from pdfframe.mainwindow import MainWindow


class _FakeLineEdit:
    """Minimal line-edit stub used by trim settings tests."""

    def __init__(self, text):
        self._text = text

    def text(self):
        return self._text

    def setText(self, value):
        self._text = value


class _FakeCheckBox:
    """Minimal checkbox stub used by trim settings tests."""

    def __init__(self, checked=False):
        self._checked = checked

    def isChecked(self):
        return self._checked

    def setChecked(self, value):
        self._checked = value


class _FakeWindow:
    """MainWindow-like stub for getPadding behavior tests."""

    def __init__(self, padding_text):
        self.ui = SimpleNamespace(editPadding=_FakeLineEdit(padding_text))
        self.warnings = []

    def tr(self, text):
        return text

    def showWarning(self, title, text):
        self.warnings.append((title, text))


def test_get_padding_uses_css_style_expansion_from_configured_value():
    """Arrange/Act/Assert: configured trim padding follows CSS expansion rules."""
    fake = _FakeWindow("5,2")
    assert MainWindow.getPadding(fake) == [5.0, 2.0, 5.0, 2.0]


def test_trim_settings_controls_are_relocated_to_basic_tab():
    """Arrange/Act/Assert: runtime code moves trim settings section into Basic tab."""
    source_path = Path(__file__).resolve().parents[1] / "src" / "pdfframe" / "mainwindow.py"
    source = source_path.read_text(encoding="iso-8859-1")
    assert "self._setupTrimSettingsControls()" in source
    assert "self.ui.groupTrimMargins.setParent(self.ui.tabBasic)" in source


class _FakeQApplication:
    """QApplication stub for cursor API calls used during trim."""

    @staticmethod
    def setOverrideCursor(_cursor):
        return None

    @staticmethod
    def restoreOverrideCursor():
        return None


class _FakeViewerSinglePage:
    """Viewer stub returning a single available image page."""

    def __init__(self):
        self.currentPageIndex = 0

    def numPages(self):
        return 1

    def getImage(self, idx):
        del idx
        return object()


class _FakeSelection:
    """Selection stub exposing geometry mapping APIs."""

    def __init__(self):
        self.rect = mainwindow_module.QRectF(0, 0, 10, 10)
        self.aspectRatio = None
        self.updated = False
        self.last_top_left = None
        self.last_bottom_right = None

    def mapRectToImage(self, rect):
        del rect
        return mainwindow_module.QRectF(0, 0, 10, 10)

    def mapRectFromImage(self, rect):
        return rect

    def setBoundingRect(self, top_left, bottom_right):
        self.last_top_left = (top_left.x(), top_left.y())
        self.last_bottom_right = (bottom_right.x(), bottom_right.y())
        self.updated = True

    def selectionVisibleOnPage(self, pageIndex):
        del pageIndex
        return True


class _FakeTrimWindow:
    """MainWindow-like stub for trimMarginsSelection settings behavior."""

    def __init__(self, sensitivity="5", allowed_changes="0", padding="0",
                 use_all_pages=False):
        self.viewer = _FakeViewerSinglePage()
        self.ui = SimpleNamespace(
            editSensitivity=_FakeLineEdit(sensitivity),
            editAllowedChanges=_FakeLineEdit(allowed_changes),
            editPadding=_FakeLineEdit(padding),
            checkTrimUseAllPages=_FakeCheckBox(use_all_pages),
        )
        self.warnings = []

    def getPadding(self):
        return [0.0, 0.0, 0.0, 0.0]

    def tr(self, text):
        return text

    def showWarning(self, title, text):
        self.warnings.append((title, text))


def test_trim_margins_selection_uses_ui_threshold_values(monkeypatch):
    """Arrange/Act/Assert: trim operation reads sensitivity and allowed-change from UI."""
    fake = _FakeTrimWindow(sensitivity="7", allowed_changes="3", padding="0")
    selection = _FakeSelection()
    captured = {}

    def _fake_auto_trim(img, orect, nrect, sensitivity, allowedchanges):
        del img
        captured["sensitivity"] = sensitivity
        captured["allowedchanges"] = allowedchanges
        return orect if nrect is None else nrect

    monkeypatch.setattr(mainwindow_module, "QApplication", _FakeQApplication)
    monkeypatch.setattr(mainwindow_module, "autoTrimMargins", _fake_auto_trim)
    MainWindow.trimMarginsSelection(fake, selection)
    assert captured["sensitivity"] == 7.0
    assert captured["allowedchanges"] == 3.0
    assert selection.updated is True


def test_trim_margins_selection_invalid_thresholds_fall_back_to_defaults(monkeypatch):
    """Arrange/Act/Assert: invalid threshold values warn and default to 5/0."""
    fake = _FakeTrimWindow(sensitivity="bad", allowed_changes="oops", padding="0")
    selection = _FakeSelection()
    captured = {}

    def _fake_auto_trim(img, orect, nrect, sensitivity, allowedchanges):
        del img
        captured["sensitivity"] = sensitivity
        captured["allowedchanges"] = allowedchanges
        return orect if nrect is None else nrect

    monkeypatch.setattr(mainwindow_module, "QApplication", _FakeQApplication)
    monkeypatch.setattr(mainwindow_module, "autoTrimMargins", _fake_auto_trim)
    MainWindow.trimMarginsSelection(fake, selection)
    assert captured["sensitivity"] == 5.0
    assert captured["allowedchanges"] == 0.0
    assert len(fake.warnings) == 2


class _FakeViewerMultiPage:
    """Viewer stub returning three available image pages."""

    def __init__(self):
        self.currentPageIndex = 1

    def numPages(self):
        return 3

    def getImage(self, idx):
        del idx
        return object()


def test_trim_defaults_to_current_page_only(monkeypatch):
    """Arrange/Act/Assert: unchecked 'use all pages' trims only the current page."""
    fake = _FakeTrimWindow(use_all_pages=False)
    fake.viewer = _FakeViewerMultiPage()
    selection = _FakeSelection()
    page_indices_seen = []

    def _fake_auto_trim(img, orect, nrect, sensitivity, allowedchanges):
        del img, sensitivity, allowedchanges
        page_indices_seen.append(len(page_indices_seen))
        return orect if nrect is None else nrect

    monkeypatch.setattr(mainwindow_module, "QApplication", _FakeQApplication)
    monkeypatch.setattr(mainwindow_module, "autoTrimMargins", _fake_auto_trim)
    MainWindow.trimMarginsSelection(fake, selection)
    assert len(page_indices_seen) == 1


def test_trim_uses_all_pages_when_checkbox_checked(monkeypatch):
    """Arrange/Act/Assert: checked 'use all pages' trims across all visible pages."""
    fake = _FakeTrimWindow(use_all_pages=True)
    fake.viewer = _FakeViewerMultiPage()
    selection = _FakeSelection()
    page_indices_seen = []

    def _fake_auto_trim(img, orect, nrect, sensitivity, allowedchanges):
        del img, sensitivity, allowedchanges
        page_indices_seen.append(len(page_indices_seen))
        return orect if nrect is None else nrect

    monkeypatch.setattr(mainwindow_module, "QApplication", _FakeQApplication)
    monkeypatch.setattr(mainwindow_module, "autoTrimMargins", _fake_auto_trim)
    MainWindow.trimMarginsSelection(fake, selection)
    assert len(page_indices_seen) == 3


def test_trim_padding_expands_final_highlighted_area(monkeypatch):
    """Arrange/Act/Assert: padding expands final trim rectangle beyond trimmed box."""

    class _FakeImage:
        def width(self):
            return 20

        def height(self):
            return 20

    class _FakeViewer:
        currentPageIndex = 0

        def numPages(self):
            return 1

        def getImage(self, idx):
            del idx
            return _FakeImage()

    class _InsetSelection(_FakeSelection):
        def __init__(self):
            super().__init__()
            self.rect = mainwindow_module.QRectF(2, 2, 4, 4)

        def mapRectToImage(self, rect):
            del rect
            return mainwindow_module.QRectF(2, 2, 4, 4)

    def _fake_auto_trim(img, orect, nrect, sensitivity, allowedchanges):
        del img, sensitivity, allowedchanges
        return orect if nrect is None else nrect

    fake = _FakeTrimWindow(padding="1")
    fake.viewer = _FakeViewer()
    fake.getPadding = lambda: MainWindow.getPadding(fake)
    selection = _InsetSelection()

    monkeypatch.setattr(mainwindow_module, "QApplication", _FakeQApplication)
    monkeypatch.setattr(mainwindow_module, "autoTrimMargins", _fake_auto_trim)

    MainWindow.trimMarginsSelection(fake, selection)

    assert selection.last_top_left == (1.0, 1.0)
    assert selection.last_bottom_right == (7.0, 7.0)
