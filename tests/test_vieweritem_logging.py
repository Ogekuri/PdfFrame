"""Unit tests for renderer-selection logging behavior."""

from pathlib import Path


def test_renderer_selection_messages_are_gated_by_verbose_flag():
    """Arrange/Act/Assert: backend selection messages print only with --verbose."""
    source_path = Path(__file__).resolve().parents[1] / "src" / "pdfframe" / "vieweritem.py"
    source = source_path.read_text(encoding="iso-8859-1")
    assert source.count("if '--verbose' in sys.argv:") >= 2
    assert 'print("Using PyMuPDF for rendering.", file=sys.stderr)' in source
    assert 'print("Using PopplerQt for rendering.", file=sys.stderr)' in source
