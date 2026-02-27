"""Unit tests for trim preset behavior in MainWindow."""

from types import SimpleNamespace
from pathlib import Path

from pdfframe.mainwindow import MainWindow


class _FakeLineEdit:
    """Line-edit stub with text getter/setter."""

    def __init__(self, value):
        self._value = value

    def text(self):
        return self._value

    def setText(self, value):
        self._value = value


class _FakeCheckBox:
    """Checkbox stub with checked getter/setter."""

    def __init__(self, checked=False):
        self._checked = checked

    def isChecked(self):
        return self._checked

    def setChecked(self, checked):
        self._checked = checked


class _FakeRadioButton(_FakeCheckBox):
    """Radio-button stub reusing checkbox behavior."""


class _FakeViewer:
    """Viewer stub exposing cropValues and empty-state API."""

    def __init__(self, crop_values, empty=False):
        self.currentPageIndex = 0
        self._crop_values = crop_values
        self._empty = empty

    def cropValues(self, idx):
        del idx
        return self._crop_values

    def isEmpty(self):
        return self._empty


def _build_fake_window():
    fake = SimpleNamespace()
    fake.ui = SimpleNamespace(
        editPadding=_FakeLineEdit("1,2,3,4"),
        editGrayscaleSensitivity=_FakeLineEdit("3"),
        editSensitivity=_FakeLineEdit("7"),
        checkTrimUseAllPages=_FakeCheckBox(True),
    )
    fake.viewer = _FakeViewer([(0.1, 0.2, 0.3, 0.4)])
    fake.selectedConversionMode = lambda: "crop"
    fake._defaultTrimPresetName = lambda: "2026/01/01 01:02:03"
    return fake


def test_trim_preset_snapshot_captures_current_controls_and_crop():
    """Arrange/Act/Assert: preset snapshot stores current mode/trim/crop values."""
    fake = _build_fake_window()
    preset = MainWindow._trimPresetFromCurrentSelection(fake)
    assert preset["mode"] == "crop"
    assert preset["padding"] == "1,2,3,4"
    assert preset["grayscale_sensitivity"] == "3"
    assert preset["sensitivity"] == "7"
    assert preset["use_all_pages"] is True
    assert preset["crop"] == [0.1, 0.2, 0.3, 0.4]


def test_apply_trim_preset_updates_runtime_controls_and_crop():
    """Arrange/Act/Assert: applying preset updates mode, trim controls, and crop data."""
    fake = _build_fake_window()
    fake.radioModeFrame = _FakeRadioButton()
    fake.radioModeCrop = _FakeRadioButton()
    fake.trimPresets = [
        {
            "name": "Preset A",
            "mode": "frame",
            "padding": "5",
            "grayscale_sensitivity": "1",
            "sensitivity": "9",
            "use_all_pages": False,
            "crop": [0.2, 0.1, 0.2, 0.1],
        }
    ]
    captured = {}
    fake._applyCropPreset = lambda crop: captured.setdefault("crop", crop)
    fake._toBool = lambda value: MainWindow._toBool(fake, value)
    MainWindow._applyTrimPreset(fake, 0)
    assert fake.radioModeFrame.isChecked() is True
    assert fake.radioModeCrop.isChecked() is False
    assert fake.ui.editPadding.text() == "5"
    assert fake.ui.editGrayscaleSensitivity.text() == "1"
    assert fake.ui.editSensitivity.text() == "9"
    assert fake.ui.checkTrimUseAllPages.isChecked() is False
    assert captured["crop"] == [0.2, 0.1, 0.2, 0.1]


def test_rename_preset_persists_with_default_name_when_empty():
    """Arrange/Act/Assert: empty inline rename is replaced with timestamp default."""
    fake = SimpleNamespace()
    fake._updatingTrimPresetList = False
    fake.trimPresets = [{"name": "Old"}]
    fake._defaultTrimPresetName = lambda: "2026/01/01 01:02:03"
    fake.persisted = False
    fake._persistTrimPresetDocument = lambda: setattr(fake, "persisted", True)
    fake.treeTrimPresets = SimpleNamespace(indexOfTopLevelItem=lambda item: 0)
    item = SimpleNamespace(
        text=lambda column: "",
        setText=lambda column, value: setattr(item, "value", value),
    )
    MainWindow.slotTrimPresetChanged(fake, item, 0)
    assert fake.trimPresets[0]["name"] == "2026/01/01 01:02:03"
    assert item.value == "2026/01/01 01:02:03"
    assert fake.persisted is True


def test_delete_preset_removes_row_and_persists():
    """Arrange/Act/Assert: row delete button removes matching preset index."""
    button = SimpleNamespace(property=lambda name: 1 if name == "preset_index" else None)
    fake = SimpleNamespace()
    fake.trimPresets = [{"name": "A"}, {"name": "B"}]
    fake.sender = lambda: button
    fake.refreshed = False
    fake.persisted = False
    fake._refreshTrimPresetList = lambda: setattr(fake, "refreshed", True)
    fake._persistTrimPresetDocument = lambda: setattr(fake, "persisted", True)
    MainWindow.slotDeleteTrimPreset(fake)
    assert [preset["name"] for preset in fake.trimPresets] == ["A"]
    assert fake.refreshed is True
    assert fake.persisted is True


def test_save_margins_appends_new_preset_and_persists():
    """Arrange/Act/Assert: save action appends new preset and writes config."""
    fake = SimpleNamespace()
    fake.viewer = _FakeViewer([], empty=False)
    fake.trimPresets = []
    fake._trimPresetFromCurrentSelection = lambda: {"name": "Preset New"}
    fake.refreshed = False
    fake.persisted = False
    fake._refreshTrimPresetList = lambda: setattr(fake, "refreshed", True)
    fake._persistTrimPresetDocument = lambda: setattr(fake, "persisted", True)
    MainWindow.slotSaveMarginsPreset(fake)
    assert fake.trimPresets == [{"name": "Preset New"}]
    assert fake.refreshed is True
    assert fake.persisted is True


def test_preset_delete_button_is_right_aligned_in_row_container():
    """Arrange/Act/Assert: delete button is placed in a right-aligned row widget."""
    source_path = Path(__file__).resolve().parents[1] / "src" / "pdfframe" / "mainwindow.py"
    source = source_path.read_text(encoding="iso-8859-1")
    assert "row_layout = QHBoxLayout(row_widget)" in source
    assert "row_layout.addStretch(1)" in source
    assert "self.treeTrimPresets.setItemWidget(item, 1, row_widget)" in source
