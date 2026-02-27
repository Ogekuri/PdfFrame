"""Unit tests for Ghostscript command integration helpers."""

from pathlib import Path
import sys
from types import SimpleNamespace

import pytest

from pdfframe import pdfframecmd


def test_padding_to_crop_offsets_reorders_values():
    """Arrange/Act/Assert: GUI padding order is converted to crop-offset order."""
    result = pdfframecmd.padding_to_crop_offsets([10, 20, 30, 40])
    assert result == (40.0, 10.0, 20.0, 30.0)


def test_crop_values_to_bbox_merges_visible_crops():
    """Arrange/Act/Assert: multiple selections are merged into a single bbox."""
    crop_values = [
        (0.10, 0.20, 0.30, 0.40),
        (0.05, 0.25, 0.20, 0.35),
    ]
    bbox = pdfframecmd.crop_values_to_bbox(crop_values, page_width=1000, page_height=2000)
    assert bbox == (50.0, 700.0, 800.0, 1600.0)


def test_crop_values_to_bbox_uses_ll_and_ur_coordinates():
    """Arrange/Act/Assert: bbox coordinates map to CropBox LL/UR semantics."""
    bbox = pdfframecmd.crop_values_to_bbox(
        [(0.10, 0.20, 0.30, 0.40)],
        page_width=1000,
        page_height=2000,
    )
    assert bbox == (100.0, 800.0, 700.0, 1600.0)


def test_normalized_crop_tuple_to_bbox_uses_gui_corner_coordinates():
    """Arrange/Act/Assert: tuple conversion yields LL/UR coordinates in points."""
    bbox = pdfframecmd.normalized_crop_tuple_to_bbox(
        (0.088227258, 0.18, 0.086601307, 0.056443534),
        page_width=612,
        page_height=792,
    )
    assert bbox == pytest.approx((53.995082, 44.703279, 558.999999, 649.44))


def test_apply_crop_offsets_to_bbox_clamps_to_page_bounds():
    """Arrange/Act/Assert: offsets expand crop box and clamp to page edges."""
    bbox = (100.0, 200.0, 500.0, 700.0)
    offsets = (200.0, 400.0, 700.0, 500.0)
    result = pdfframecmd.apply_crop_offsets_to_bbox(
        bbox,
        offsets,
        page_width=1000,
        page_height=1000,
    )
    assert result == (0.0, 0.0, 1000.0, 1000.0)


def test_build_ghostscript_page_crop_command_builds_frame_mode_command():
    """Arrange/Act/Assert: frame mode keeps original media and applies clipping."""
    command = pdfframecmd.build_ghostscript_page_crop_command(
        "input.pdf",
        "page-1.pdf",
        first_page=3,
        last_page=3,
        page_width=595,
        page_height=842,
        crop_box=(10, 20, 580, 830),
        mode="frame",
    )
    assert command == [
        "gs",
        "-dSAFER",
        "-dNOPAUSE",
        "-dBATCH",
        "-sDEVICE=pdfwrite",
        "-dAutoRotatePages=/None",
        "-dFIXEDMEDIA",
        "-dModifiesPageSize=true",
        "-dPreserveAnnots=false",
        "-dFirstPage=3",
        "-dLastPage=3",
        "-dDEVICEWIDTHPOINTS=595",
        "-dDEVICEHEIGHTPOINTS=842",
        "-o",
        "page-1.pdf",
        "-c",
        "<</BeginPage{10 20 570 810 rectclip}>> setpagedevice",
        "-f",
        "input.pdf",
    ]


def test_build_ghostscript_page_crop_command_builds_crop_mode_command():
    """Arrange/Act/Assert: crop mode translates content into cropped media box."""
    command = pdfframecmd.build_ghostscript_page_crop_command(
        "input.pdf",
        "page-1.pdf",
        first_page=3,
        last_page=3,
        page_width=595,
        page_height=842,
        crop_box=(10, 20, 580, 830),
        mode="crop",
    )
    assert command == [
        "gs",
        "-dSAFER",
        "-dNOPAUSE",
        "-dBATCH",
        "-sDEVICE=pdfwrite",
        "-dAutoRotatePages=/None",
        "-dFIXEDMEDIA",
        "-dModifiesPageSize=true",
        "-dPreserveAnnots=false",
        "-dFirstPage=3",
        "-dLastPage=3",
        "-dDEVICEWIDTHPOINTS=570",
        "-dDEVICEHEIGHTPOINTS=810",
        "-o",
        "page-1.pdf",
        "-c",
        "<</BeginPage{0 0 570 810 rectclip -10 -20 translate}>> setpagedevice",
        "-f",
        "input.pdf",
    ]


def test_run_ghostscript_command_logs_shell_escaped_command(monkeypatch, capsys):
    """Arrange/Act/Assert: command execution logs exact shell-escaped command."""

    def _fake_run(*args, **kwargs):
        del args, kwargs
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(pdfframecmd.subprocess, "run", _fake_run)
    command = ["gs", "-f", "/tmp/input file.pdf"]
    pdfframecmd.run_ghostscript_command(command, log_command=True)
    expected = pdfframecmd.format_shell_command(command)
    assert f"Executing Ghostscript command: {expected}" in capsys.readouterr().err


def test_write_cropped_pages_output_keeps_only_selected_pages(tmp_path):
    """Arrange/Act/Assert: output writer emits exactly provided cropped pages."""
    from pypdf import PdfReader, PdfWriter

    def _create_single_page_pdf(path: Path, width: float):
        writer = PdfWriter()
        writer.add_blank_page(width=width, height=200)
        with path.open("wb") as output_file:
            writer.write(output_file)

    page_a = tmp_path / "page-a.pdf"
    page_b = tmp_path / "page-b.pdf"
    page_c = tmp_path / "page-c.pdf"
    _create_single_page_pdf(page_a, 101)
    _create_single_page_pdf(page_b, 202)
    _create_single_page_pdf(page_c, 303)
    output_pdf = tmp_path / "out.pdf"
    pdfframecmd.write_cropped_pages_output(
        str(output_pdf),
        [str(page_b), str(page_c)],
    )
    reader = PdfReader(str(output_pdf))
    assert len(reader.pages) == 2


def test_run_ghostscript_command_raises_with_captured_streams(monkeypatch):
    """Arrange/Act/Assert: non-zero return propagates captured output in exception."""

    def _fake_run(*args, **kwargs):
        del args, kwargs
        return SimpleNamespace(returncode=2, stdout="stdout data", stderr="stderr data")

    monkeypatch.setattr(pdfframecmd.subprocess, "run", _fake_run)
    with pytest.raises(pdfframecmd.GhostscriptCommandError) as exc:
        pdfframecmd.run_ghostscript_command(["gs", "in.pdf", "out.pdf"])
    assert exc.value.returncode == 2
    assert exc.value.stdout == "stdout data"
    assert exc.value.stderr == "stderr data"


def test_extract_ghostscript_page_number_parses_output():
    """Arrange/Act/Assert: parser extracts page number from Ghostscript lines."""
    assert pdfframecmd.extract_ghostscript_page_number("Page 192\n") == 192
    assert pdfframecmd.extract_ghostscript_page_number("Page 192") is None
    assert pdfframecmd.extract_ghostscript_page_number("not a page line") is None


def test_extract_ghostscript_page_numbers_parses_multiple_tokens():
    """Arrange/Act/Assert: parser extracts all page tokens from one chunk."""
    chunk = "Page 1\nPage 2\nPage 3\n"
    assert pdfframecmd.extract_ghostscript_page_numbers(chunk) == [1, 2, 3]


def test_extract_ghostscript_page_numbers_matches_page_line_pattern():
    """Arrange/Act/Assert: parser accepts only `^Page\\s+\\d+\\n` entries."""
    chunk = "prefix Page 1\nPage 2\nPage 3\nsuffix\n"
    assert pdfframecmd.extract_ghostscript_page_numbers(chunk) == [2, 3]


def test_build_ghostscript_page_crop_command_does_not_use_quiet_flag():
    """Arrange/Act/Assert: command does not suppress Ghostscript page progress output."""
    command = pdfframecmd.build_ghostscript_page_crop_command(
        "input.pdf",
        "page-1.pdf",
        first_page=1,
        last_page=2,
        page_width=595,
        page_height=842,
        crop_box=(10, 20, 580, 830),
        mode="frame",
    )
    assert "-q" not in command


@pytest.mark.parametrize("mode", ["frame", "crop"])
def test_build_ghostscript_page_crop_command_emits_preserve_annots_flag(mode):
    """Arrange/Act/Assert: PreserveAnnots flag mirrors preserve_annots parameter."""
    command = pdfframecmd.build_ghostscript_page_crop_command(
        "input.pdf",
        "page-1.pdf",
        first_page=1,
        last_page=1,
        page_width=595,
        page_height=842,
        crop_box=(10, 20, 580, 830),
        mode=mode,
        preserve_annots=True,
    )
    assert "-dPreserveAnnots=true" in command


def test_run_ghostscript_command_debug_output_prints_stream(monkeypatch, capsys):
    """Arrange/Act/Assert: debug mode mirrors captured output to stderr."""
    command = [
        sys.executable,
        "-c",
        "print('Page 1', flush=True); print('Page 2', flush=True)",
    ]
    pdfframecmd.run_ghostscript_command(command, debug_output=True, poll_interval=0.001)
    err = capsys.readouterr().err
    assert "Page 1" in err
    assert "Page 2" in err


def test_run_ghostscript_command_streams_output_and_pumps_events():
    """Arrange/Act/Assert: streamed lines reach callback while event pump runs."""
    command = [
        sys.executable,
        "-c",
        (
            "import time;"
            "print('Page 1', flush=True);"
            "time.sleep(0.02);"
            "print('Page 2', flush=True);"
            "time.sleep(0.02)"
        ),
    ]
    output_lines = []
    event_pump_calls = []
    result = pdfframecmd.run_ghostscript_command(
        command,
        event_pump=lambda: event_pump_calls.append(1),
        output_callback=output_lines.append,
        poll_interval=0.001,
    )
    parsed_pages = [pdfframecmd.extract_ghostscript_page_number(line) for line in output_lines]
    assert result.returncode == 0
    assert 1 in parsed_pages and 2 in parsed_pages
    assert len(event_pump_calls) > 0


def test_run_ghostscript_command_can_be_cancelled():
    """Arrange/Act/Assert: cancellation callback terminates running subprocess."""
    command = [
        sys.executable,
        "-c",
        (
            "import time;"
            "print('Page 1', flush=True);"
            "time.sleep(1.0)"
        ),
    ]
    state = {"calls": 0}

    def cancel_requested():
        state["calls"] += 1
        return state["calls"] > 2

    with pytest.raises(pdfframecmd.GhostscriptCommandCancelledError):
        pdfframecmd.run_ghostscript_command(
            command,
            event_pump=lambda: None,
            cancel_requested=cancel_requested,
            poll_interval=0.005,
        )
