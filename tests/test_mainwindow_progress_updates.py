"""Unit tests for progress updates driven by captured Ghostscript output."""

from types import SimpleNamespace

from pdfframe import mainwindow as mainwindow_module
from pdfframe.mainwindow import MainWindow


class _FakeLineEdit:
    """Minimal line-edit stub used by progress-update tests."""

    def __init__(self, value):
        self._value = value

    def text(self):
        return self._value


class _FakeProgressDialog:
    """Progress-dialog stub that records value updates."""

    def __init__(self, total_pages):
        self._max = total_pages
        self.values = []

    def setValue(self, value):
        self.values.append(value)

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
    """QApplication stub for progress-update tests."""

    @staticmethod
    def setOverrideCursor(_cursor):
        return None

    @staticmethod
    def restoreOverrideCursor():
        return None

    @staticmethod
    def processEvents():
        return None


class _FakeProgressWindow:
    """MainWindow-like stub focused on progress-update behavior."""

    def __init__(self, page_indexes):
        self.fileName = "input.pdf"
        self.verbose = False
        self.debug = False
        self.ui = SimpleNamespace(
            editFile=_FakeLineEdit("output.pdf"),
            editWhichPages=_FakeLineEdit(""),
        )
        self.viewer = SimpleNamespace(numPages=lambda: 100)
        self._page_indexes = page_indexes
        self.progress_dialog = None
        self.warnings = []

    def tr(self, text):
        return text

    def requestedUnsupportedGhostscriptOptions(self):
        return []

    def buildGhostscriptCropPlan(self, inputFileName, outputFileName, requestedPageIndexes=None):
        del inputFileName, outputFileName, requestedPageIndexes
        return {"page_indexes": self._page_indexes, "command": ["gs", "-f", "input.pdf"]}

    def createConversionProgressDialog(self, totalPages):
        self.progress_dialog = _FakeProgressDialog(totalPages)
        return self.progress_dialog

    def showWarning(self, title, text):
        self.warnings.append((title, text))

    str2pages = MainWindow.str2pages


def test_slot_pdfframe_updates_progress_from_absolute_page_numbers(monkeypatch):
    """Arrange/Act/Assert: captured output page numbers drive monotonic progress."""

    def _fake_run_ghostscript_command(*args, **kwargs):
        del args
        output_callback = kwargs["output_callback"]
        output_callback("Page 5\n")
        output_callback("Page 6\n")
        output_callback("Page 7\n")

    fake = _FakeProgressWindow(page_indexes=[4, 5, 6])
    monkeypatch.setattr(mainwindow_module, "which", lambda _name: "/usr/bin/gs")
    monkeypatch.setattr(mainwindow_module, "QApplication", _FakeQApplication)
    monkeypatch.setattr(mainwindow_module, "run_ghostscript_command", _fake_run_ghostscript_command)

    MainWindow.slotPdfFrame(fake)

    assert fake.warnings == []
    assert fake.progress_dialog is not None
    assert fake.progress_dialog.values[:3] == [1, 2, 3]


def test_slot_pdfframe_updates_progress_from_relative_page_numbers(monkeypatch):
    """Arrange/Act/Assert: relative page-output numbers map to selected-page progress."""

    def _fake_run_ghostscript_command(*args, **kwargs):
        del args
        output_callback = kwargs["output_callback"]
        output_callback("Page 1\n")
        output_callback("Page 2\n")
        output_callback("Page 3\n")

    fake = _FakeProgressWindow(page_indexes=[4, 5, 6])
    monkeypatch.setattr(mainwindow_module, "which", lambda _name: "/usr/bin/gs")
    monkeypatch.setattr(mainwindow_module, "QApplication", _FakeQApplication)
    monkeypatch.setattr(mainwindow_module, "run_ghostscript_command", _fake_run_ghostscript_command)

    MainWindow.slotPdfFrame(fake)

    assert fake.warnings == []
    assert fake.progress_dialog is not None
    assert fake.progress_dialog.values[:3] == [1, 2, 3]


def test_slot_pdfframe_parses_multiple_page_numbers_from_one_output_chunk(monkeypatch):
    """Arrange/Act/Assert: one chunk containing multiple page tokens updates progress."""

    def _fake_run_ghostscript_command(*args, **kwargs):
        del args
        output_callback = kwargs["output_callback"]
        output_callback("Page 1\rPage 2\rPage 3")

    fake = _FakeProgressWindow(page_indexes=[4, 5, 6])
    monkeypatch.setattr(mainwindow_module, "which", lambda _name: "/usr/bin/gs")
    monkeypatch.setattr(mainwindow_module, "QApplication", _FakeQApplication)
    monkeypatch.setattr(mainwindow_module, "run_ghostscript_command", _fake_run_ghostscript_command)

    MainWindow.slotPdfFrame(fake)

    assert fake.warnings == []
    assert fake.progress_dialog is not None
    assert fake.progress_dialog.values[:3] == [1, 2, 3]


def test_slot_pdfframe_enables_command_and_shell_debug_output_with_verbose_and_debug(monkeypatch):
    """Arrange/Act/Assert: combined flags pass command/output debug toggles downstream."""
    captured = {}

    def _fake_run_ghostscript_command(*args, **kwargs):
        del args
        captured["log_command"] = kwargs.get("log_command")
        captured["debug_output"] = kwargs.get("debug_output")
        kwargs["output_callback"]("Page 5\n")

    fake = _FakeProgressWindow(page_indexes=[4])
    fake.verbose = True
    fake.debug = True
    monkeypatch.setattr(mainwindow_module, "which", lambda _name: "/usr/bin/gs")
    monkeypatch.setattr(mainwindow_module, "QApplication", _FakeQApplication)
    monkeypatch.setattr(mainwindow_module, "run_ghostscript_command", _fake_run_ghostscript_command)

    MainWindow.slotPdfFrame(fake)

    assert captured["log_command"] is True
    assert captured["debug_output"] is True
