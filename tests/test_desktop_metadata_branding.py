"""Unit tests for desktop/AppStream branding metadata."""

from pathlib import Path


def test_desktop_and_metainfo_use_pdfframe_branding():
    """Arrange/Act/Assert: desktop integration files use pdfframe identifiers."""
    repo_root = Path(__file__).resolve().parents[1]
    desktop_path = repo_root / "com.ogekuri.pdfframe.desktop"
    metainfo_path = repo_root / "com.ogekuri.pdfframe.metainfo.xml"

    desktop = desktop_path.read_text(encoding="utf-8")
    metainfo = metainfo_path.read_text(encoding="utf-8")

    assert "Name=PdfFrame" in desktop
    assert "TryExec=pdfframe" in desktop
    assert "Exec=pdfframe %F" in desktop
    assert "Icon=com.ogekuri.pdfframe" in desktop

    assert "<id>com.ogekuri.pdfframe</id>" in metainfo
    assert "<launchable type=\"desktop-id\">com.ogekuri.pdfframe.desktop</launchable>" in metainfo
    assert "<name>PdfFrame</name>" in metainfo
    assert "pdfcrop" not in metainfo


def test_gitignore_whitelists_pdfframe_desktop_artifacts():
    """Arrange/Act/Assert: root desktop metadata files are explicitly unignored."""
    repo_root = Path(__file__).resolve().parents[1]
    gitignore = (repo_root / ".gitignore").read_text(encoding="utf-8")

    assert "!com.ogekuri.pdfframe.desktop" in gitignore
    assert "!com.ogekuri.pdfframe.metainfo.xml" in gitignore
    assert "!com.ogekuri.pdfframe.svg" in gitignore
