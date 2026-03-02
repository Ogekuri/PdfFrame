"""Unit tests for openFile page-format compatibility behavior."""

from types import SimpleNamespace

from pdfframe.mainwindow import MainWindow


class _FakeAction:
    """Action stub that records enabled state changes."""

    def __init__(self):
        self.enabled = None

    def setEnabled(self, enabled):
        self.enabled = enabled


class _FakeLineEdit:
    """Line-edit stub that records latest assigned text."""

    def __init__(self):
        self.value = None

    def setText(self, text):
        self.value = text


class _FakeCheckAction:
    """Checkable-action stub for fit-in-view state."""

    def __init__(self, checked=True):
        self._checked = checked

    def isChecked(self):
        return self._checked


class _FakeViewer:
    """Viewer stub that exposes deterministic page-size metadata."""

    def __init__(self, page_sizes):
        self._page_sizes = list(page_sizes)
        self.reset_called = False

    def load(self, _file_name):
        return None

    def isEmpty(self):
        return not self._page_sizes

    def numPages(self):
        return len(self._page_sizes)

    def pageGetSizePoints(self, index):
        return self._page_sizes[index]

    def reset(self):
        self.reset_called = True
        self._page_sizes = []


class _FakeOpenFileWindow:
    """MainWindow-like stub used to exercise openFile logic."""

    def __init__(self, page_sizes):
        self.viewer = _FakeViewer(page_sizes)
        self.fileName = ""
        self.window_file_path = None
        self.fit_values = []
        self.warnings = []
        self.update_controls_called = False
        self.update_selection_actions_called = False
        self.actionSaveMargins = _FakeAction()
        self.ui = SimpleNamespace(
            actionFitInView=_FakeCheckAction(True),
            actionPdfFrame=_FakeAction(),
            actionTrimMarginsAll=_FakeAction(),
            editFile=_FakeLineEdit(),
        )

    def tr(self, text):
        return text

    def slotFitInView(self, checked):
        self.fit_values.append(checked)

    def showWarning(self, title, text):
        self.warnings.append((title, text))

    def setWindowFilePath(self, value):
        self.window_file_path = value

    def updateControls(self):
        self.update_controls_called = True

    def _updateSelectionCreationActions(self):
        self.update_selection_actions_called = True

    _hasCompatiblePageFormat = MainWindow._hasCompatiblePageFormat


def test_openfile_keeps_loaded_state_for_uniform_page_format():
    """Arrange/Act/Assert: uniform page format keeps file loaded and actions enabled."""
    fake = _FakeOpenFileWindow([(595.0, 842.0), (595.0, 842.0), (595.0, 842.0)])

    MainWindow.openFile(fake, "/tmp/demo.pdf")

    assert fake.fileName == "/tmp/demo.pdf"
    assert fake.ui.editFile.value == "/tmp/demo-cropped.pdf"
    assert fake.window_file_path == "/tmp/demo.pdf"
    assert fake.viewer.reset_called is False
    assert fake.ui.actionPdfFrame.enabled is True
    assert fake.ui.actionTrimMarginsAll.enabled is True
    assert fake.actionSaveMargins.enabled is True
    assert fake.warnings == []
    assert fake.fit_values == [True]
    assert fake.update_controls_called is True
    assert fake.update_selection_actions_called is True


def test_openfile_resets_loaded_state_for_mixed_page_format():
    """Arrange/Act/Assert: mixed page format warns and closes the just-opened file."""
    fake = _FakeOpenFileWindow([(595.0, 842.0), (842.0, 595.0)])

    MainWindow.openFile(fake, "/tmp/demo.pdf")

    assert fake.fileName == ""
    assert fake.ui.editFile.value == ""
    assert fake.window_file_path == ""
    assert fake.viewer.reset_called is True
    assert fake.ui.actionPdfFrame.enabled is False
    assert fake.ui.actionTrimMarginsAll.enabled is False
    assert fake.actionSaveMargins.enabled is False
    assert len(fake.warnings) == 1
    assert fake.warnings[0][0] == "Incompatible page format"
    assert "different sizes or orientations" in fake.warnings[0][1]
