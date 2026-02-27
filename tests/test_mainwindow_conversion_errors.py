"""Unit tests for conversion error handling in MainWindow.slotPdfFrame."""

from types import SimpleNamespace

from pdfframe import mainwindow as mainwindow_module
from pdfframe.mainwindow import MainWindow


class _FakeLineEdit:
    """Minimal line-edit stub used by conversion tests."""

    def __init__(self, value):
        self._value = value

    def text(self):
        return self._value


class _FakeProgressDialog:
    """Progress-dialog stub used by conversion tests."""

    def __init__(self):
        self._max = 1

    def setValue(self, _value):
        return None

    def maximum(self):
        return self._max

    def setLabelText(self, _text):
        return None

    def show(self):
        return None

    def close(self):
        return None

    def wasCanceled(self):
        return False


class _FakeQApplication:
    """QApplication stub for conversion tests."""

    @staticmethod
    def setOverrideCursor(_cursor):
        return None

    @staticmethod
    def restoreOverrideCursor():
        return None

    @staticmethod
    def processEvents():
        return None


class _FakeConversionWindow:
    """MainWindow-like stub focused on Ghostscript error warnings."""

    def __init__(self):
        self.fileName = "input.pdf"
        self.verbose = False
        self.debug = False
        self.ui = SimpleNamespace(
            editFile=_FakeLineEdit("output.pdf"),
            editWhichPages=_FakeLineEdit(""),
        )
        self.viewer = SimpleNamespace(numPages=lambda: 1)
        self.warnings = []

    def tr(self, text):
        return text

    def requestedUnsupportedGhostscriptOptions(self):
        return []

    def buildGhostscriptCropPlan(self, inputFileName, outputFileName, requestedPageIndexes=None):
        del inputFileName, outputFileName, requestedPageIndexes
        return {"page_indexes": [0], "command": ["gs", "-f", "input.pdf"]}

    def createConversionProgressDialog(self, totalPages):
        del totalPages
        return _FakeProgressDialog()

    def showWarning(self, title, text):
        self.warnings.append((title, text))

    str2pages = MainWindow.str2pages


def test_slot_pdfframe_omits_captured_output_from_user_warning(monkeypatch):
    """Arrange/Act/Assert: user warning omits captured stdout/stderr payload."""

    def _raise_command_error(*args, **kwargs):
        del args, kwargs
        raise mainwindow_module.GhostscriptCommandError(
            ["gs", "-f", "input.pdf"], 2, "captured stdout", "captured stderr")

    fake = _FakeConversionWindow()
    monkeypatch.setattr(mainwindow_module, "which", lambda _name: "/usr/bin/gs")
    monkeypatch.setattr(mainwindow_module, "QApplication", _FakeQApplication)
    monkeypatch.setattr(mainwindow_module, "run_ghostscript_command", _raise_command_error)

    MainWindow.slotPdfFrame(fake)

    assert len(fake.warnings) == 1
    _title, text = fake.warnings[0]
    assert "Command failed:\ngs -f input.pdf" in text
    assert "captured stdout" not in text
    assert "captured stderr" not in text
