"""Unit tests for single-selection-only behavior."""

from pathlib import Path


def test_viewerselections_add_selection_blocks_second_area_creation():
    """Arrange/Act/Assert: addSelection returns existing area when one already exists."""
    source_path = Path(__file__).resolve().parents[1] / "src" / "pdfframe" / "viewerselections.py"
    source = source_path.read_text(encoding="iso-8859-1")
    assert "if self._selections:" in source
    assert "s = self._selections[0]" in source
    assert "return s" in source


def test_mouse_drag_creation_is_blocked_when_area_exists():
    """Arrange/Act/Assert: scene mouse-press path does not create a second selection."""
    source_path = Path(__file__).resolve().parents[1] / "src" / "pdfframe" / "viewerselections.py"
    source = source_path.read_text(encoding="iso-8859-1")
    assert "if self._selections:" in source
    assert "self.currentSelection = self._selections[0]" in source
    assert "self.currentSelection = self.addSelection(rect)" in source


def test_centered_selection_index_rendering_is_removed():
    """Arrange/Act/Assert: selection paint no longer renders centered ordinal number."""
    source_path = Path(__file__).resolve().parents[1] / "src" / "pdfframe" / "viewerselections.py"
    source = source_path.read_text(encoding="iso-8859-1")
    assert "painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(self.orderIndex))" not in source


def test_mainwindow_grid_creation_and_actions_enforce_single_area_mode():
    """Arrange/Act/Assert: MainWindow enforces single area in grid creation and action enablement."""
    source_path = Path(__file__).resolve().parents[1] / "src" / "pdfframe" / "mainwindow.py"
    source = source_path.read_text(encoding="iso-8859-1")
    assert "len(self.selections.items) == 0" in source
    assert "Only one trim/selection area is supported." in source
    assert "if cols * rows != 1:" in source
    assert "cols = 1" in source
    assert "rows = 1" in source
