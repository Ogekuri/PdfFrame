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


class _FakeCheckBox:
    """Checkbox stub returning configured checked state."""

    def __init__(self, checked):
        self._checked = checked

    def isChecked(self):
        return self._checked


class _FakeConversionWindow:
    """MainWindow-like stub focused on crop error warnings."""

    def __init__(self):
        self.fileName = "input.pdf"
        self.verbose = False
        self.debug = False
        self.ui = SimpleNamespace(
            editFile=_FakeLineEdit("output.pdf"),
            editWhichPages=_FakeLineEdit(""),
            checkDeleteAnnotsFields=_FakeCheckBox(True),
        )
        self.viewer = SimpleNamespace(numPages=lambda: 1)
        self.warnings = []

    def tr(self, text):
        return text

    def buildCropPlan(self, inputFileName, outputFileName, requestedPageIndexes=None):
        del inputFileName, outputFileName, requestedPageIndexes
        return {
            "page_indexes": [0],
            "crop_box": (10, 10, 600, 780),
            "page_width": 612,
            "page_height": 792,
            "mode": "frame",
            "delete_annots": True,
            "input_path": "input.pdf",
            "output_path": "output.pdf",
        }

    def createConversionProgressDialog(self, totalPages):
        del totalPages
        return _FakeProgressDialog()

    def showWarning(self, title, text):
        self.warnings.append((title, text))

    str2pages = MainWindow.str2pages


def test_slot_pdfframe_omits_internal_details_from_user_warning(monkeypatch):
    """Arrange/Act/Assert: user warning omits internal exception details."""

    def _raise_crop_error(*args, **kwargs):
        del args, kwargs
        raise mainwindow_module.CropError("Internal PDF processing error details")

    fake = _FakeConversionWindow()
    monkeypatch.setattr(mainwindow_module, "QApplication", _FakeQApplication)
    monkeypatch.setattr(mainwindow_module, "crop_pdf_pages", _raise_crop_error)

    MainWindow.slotPdfFrame(fake)

    assert len(fake.warnings) == 1
    _title, text = fake.warnings[0]
    assert "crop failed" in text.lower() or "Internal PDF processing error details" in text
