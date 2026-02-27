"""Regression test for ViewerSelections startup safety."""

from types import SimpleNamespace

from pdfframe.viewerselections import ViewerSelections


class _ViewerWithoutScene:
    """Viewer stub exposing no scene during early startup."""

    currentPageIndex = 0

    def __init__(self):
        self.mainwindow = SimpleNamespace(currentSelectionUpdated=lambda: None)

    def scene(self):
        return None


def test_current_selection_update_is_safe_without_scene():
    """Arrange/Act/Assert: startup update does not crash when scene is missing."""
    selections = ViewerSelections(_ViewerWithoutScene())
    selections.currentSelection = None
