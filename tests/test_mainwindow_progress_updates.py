"""Unit tests for progress updates driven by PyMuPDF crop callbacks."""

from types import SimpleNamespace

from pdfframe import mainwindow as mainwindow_module
from pdfframe.mainwindow import MainWindow


class _FakeLineEdit:
    """Minimal line-edit stub used by progress-update tests."""

    def __init__(self, value):
        self._value = value

    def text(self):
        return self._value


class _FakeCheckBox:
    """Checkbox stub returning configured checked state."""

    def __init__(self, checked):
        self._checked = checked

    def isChecked(self):
        return self._checked


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
            checkDeleteAnnotsFields=_FakeCheckBox(True),
        )
        self.viewer = SimpleNamespace(numPages=lambda: 100)
        self._page_indexes = page_indexes
        self.progress_dialog = None
        self.warnings = []

    def tr(self, text):
        return text

    def buildCropPlan(self, inputFileName, outputFileName, requestedPageIndexes=None):
        del inputFileName, outputFileName, requestedPageIndexes
        return {
            "page_indexes": self._page_indexes,
            "crop_box": (10, 10, 600, 780),
            "page_width": 612,
            "page_height": 792,
            "mode": "frame",
            "delete_annots": True,
            "input_path": "input.pdf",
            "output_path": "output.pdf",
        }

    def createConversionProgressDialog(self, totalPages):
        self.progress_dialog = _FakeProgressDialog(totalPages)
        return self.progress_dialog

    def showWarning(self, title, text):
        self.warnings.append((title, text))

    str2pages = MainWindow.str2pages


def test_slot_pdfframe_updates_progress_from_callback(monkeypatch):
    """Arrange/Act/Assert: per-page callback drives monotonic progress updates."""

    def _fake_crop_pdf_pages(*args, **kwargs):
        progress_callback = kwargs["progress_callback"]
        progress_callback(5, 1, 3)
        progress_callback(6, 2, 3)
        progress_callback(7, 3, 3)

    fake = _FakeProgressWindow(page_indexes=[4, 5, 6])
    monkeypatch.setattr(mainwindow_module, "QApplication", _FakeQApplication)
    monkeypatch.setattr(mainwindow_module, "crop_pdf_pages", _fake_crop_pdf_pages)

    MainWindow.slotPdfFrame(fake)

    assert fake.warnings == []
    assert fake.progress_dialog is not None
    assert fake.progress_dialog.values[:3] == [1, 2, 3]


def test_slot_pdfframe_enables_log_and_debug_with_verbose_and_debug(monkeypatch):
    """Arrange/Act/Assert: combined flags pass log/debug toggles downstream."""
    captured = {}

    def _fake_crop_pdf_pages(*args, **kwargs):
        captured["log_params"] = kwargs.get("log_params")
        captured["debug_output"] = kwargs.get("debug_output")
        kwargs["progress_callback"](5, 1, 1)

    fake = _FakeProgressWindow(page_indexes=[4])
    fake.verbose = True
    fake.debug = True
    monkeypatch.setattr(mainwindow_module, "QApplication", _FakeQApplication)
    monkeypatch.setattr(mainwindow_module, "crop_pdf_pages", _fake_crop_pdf_pages)

    MainWindow.slotPdfFrame(fake)

    assert captured["log_params"] is True
    assert captured["debug_output"] is True
