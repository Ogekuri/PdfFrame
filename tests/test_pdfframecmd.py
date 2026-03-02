"""Unit tests for PyMuPDF crop/frame backend helpers."""

from pathlib import Path
import sys
from types import SimpleNamespace

import fitz
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


def _create_test_pdf(path, num_pages=3, width=612, height=792, with_annots=False,
                     with_toc=False):
    """Creates a test PDF with optional annotations and bookmarks."""
    doc = fitz.open()
    for i in range(num_pages):
        page = doc.new_page(width=width, height=height)
        if with_annots:
            annot = page.add_text_annot((72, 72), f"Test annotation page {i+1}")
            del annot
    if with_toc:
        toc = [[1, f"Chapter {i+1}", i+1] for i in range(num_pages)]
        doc.set_toc(toc)
    doc.save(str(path))
    doc.close()


def test_crop_pdf_pages_frame_mode_preserves_original_page_size(tmp_path):
    """Arrange/Act/Assert: frame mode keeps original page dimensions."""
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    _create_test_pdf(input_pdf, num_pages=1, width=612, height=792)
    pdfframecmd.crop_pdf_pages(
        str(input_pdf), str(output_pdf),
        page_indexes=[0],
        crop_box=(100, 200, 500, 700),
        page_width=612, page_height=792,
        mode="frame", delete_annots=False,
    )
    doc = fitz.open(str(output_pdf))
    page = doc[0]
    mediabox = page.mediabox
    cropbox = page.cropbox
    assert mediabox.width == pytest.approx(612, abs=1)
    assert mediabox.height == pytest.approx(792, abs=1)
    assert cropbox.width == pytest.approx(612, abs=1)
    assert cropbox.height == pytest.approx(792, abs=1)
    doc.close()


def test_crop_pdf_pages_crop_mode_sets_mediabox(tmp_path):
    """Arrange/Act/Assert: crop mode physically resizes page via MediaBox."""
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    _create_test_pdf(input_pdf, num_pages=1, width=612, height=792)
    pdfframecmd.crop_pdf_pages(
        str(input_pdf), str(output_pdf),
        page_indexes=[0],
        crop_box=(100, 200, 500, 700),
        page_width=612, page_height=792,
        mode="crop", delete_annots=False,
    )
    doc = fitz.open(str(output_pdf))
    page = doc[0]
    mediabox = page.mediabox
    assert mediabox.width == pytest.approx(400, abs=1)
    assert mediabox.height == pytest.approx(500, abs=1)
    doc.close()


def test_crop_pdf_pages_deletes_annotations_when_enabled(tmp_path):
    """Arrange/Act/Assert: delete_annots removes all /Annots entries."""
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    _create_test_pdf(input_pdf, num_pages=2, with_annots=True)
    pdfframecmd.crop_pdf_pages(
        str(input_pdf), str(output_pdf),
        page_indexes=[0, 1],
        crop_box=(10, 10, 600, 780),
        page_width=612, page_height=792,
        mode="frame", delete_annots=True,
    )
    doc = fitz.open(str(output_pdf))
    for page in doc:
        assert len(list(page.annots())) == 0
    doc.close()


def test_crop_pdf_pages_preserves_annotations_when_disabled(tmp_path):
    """Arrange/Act/Assert: delete_annots=False keeps annotations in output."""
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    _create_test_pdf(input_pdf, num_pages=1, with_annots=True)
    pdfframecmd.crop_pdf_pages(
        str(input_pdf), str(output_pdf),
        page_indexes=[0],
        crop_box=(10, 10, 600, 780),
        page_width=612, page_height=792,
        mode="frame", delete_annots=False,
    )
    doc = fitz.open(str(output_pdf))
    assert len(list(doc[0].annots())) > 0
    doc.close()


def test_crop_pdf_pages_preserves_bookmarks(tmp_path):
    """Arrange/Act/Assert: output PDF preserves TOC/bookmarks from input."""
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    _create_test_pdf(input_pdf, num_pages=3, with_toc=True)
    pdfframecmd.crop_pdf_pages(
        str(input_pdf), str(output_pdf),
        page_indexes=[0, 1, 2],
        crop_box=(10, 10, 600, 780),
        page_width=612, page_height=792,
        mode="frame", delete_annots=False,
    )
    doc = fitz.open(str(output_pdf))
    toc = doc.get_toc()
    assert len(toc) == 3
    assert toc[0][1] == "Chapter 1"
    doc.close()


def test_crop_pdf_pages_selects_only_requested_pages(tmp_path):
    """Arrange/Act/Assert: output contains only specified page indexes."""
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    _create_test_pdf(input_pdf, num_pages=5)
    pdfframecmd.crop_pdf_pages(
        str(input_pdf), str(output_pdf),
        page_indexes=[1, 3],
        crop_box=(10, 10, 600, 780),
        page_width=612, page_height=792,
        mode="frame", delete_annots=False,
    )
    doc = fitz.open(str(output_pdf))
    assert len(doc) == 2
    doc.close()


def test_crop_pdf_pages_progress_callback_invoked_per_page(tmp_path):
    """Arrange/Act/Assert: progress callback receives per-page updates."""
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    _create_test_pdf(input_pdf, num_pages=3)
    progress_calls = []
    pdfframecmd.crop_pdf_pages(
        str(input_pdf), str(output_pdf),
        page_indexes=[0, 1, 2],
        crop_box=(10, 10, 600, 780),
        page_width=612, page_height=792,
        mode="frame", delete_annots=False,
        progress_callback=lambda pn, pc, t: progress_calls.append((pn, pc, t)),
    )
    assert len(progress_calls) == 3
    assert progress_calls[0] == (1, 1, 3)
    assert progress_calls[1] == (2, 2, 3)
    assert progress_calls[2] == (3, 3, 3)


def test_crop_pdf_pages_cancel_raises_cancelled_error(tmp_path):
    """Arrange/Act/Assert: cancel callback triggers CropCancelledError."""
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    _create_test_pdf(input_pdf, num_pages=3)
    with pytest.raises(pdfframecmd.CropCancelledError):
        pdfframecmd.crop_pdf_pages(
            str(input_pdf), str(output_pdf),
            page_indexes=[0, 1, 2],
            crop_box=(10, 10, 600, 780),
            page_width=612, page_height=792,
            mode="frame", delete_annots=False,
            cancel_requested=lambda: True,
        )


def test_crop_pdf_pages_invalid_crop_raises_value_error(tmp_path):
    """Arrange/Act/Assert: non-positive crop dimensions raise ValueError."""
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    _create_test_pdf(input_pdf, num_pages=1)
    with pytest.raises(ValueError, match="positive"):
        pdfframecmd.crop_pdf_pages(
            str(input_pdf), str(output_pdf),
            page_indexes=[0],
            crop_box=(500, 200, 100, 700),
            page_width=612, page_height=792,
            mode="frame",
        )


def test_crop_pdf_pages_invalid_mode_raises_value_error(tmp_path):
    """Arrange/Act/Assert: unsupported mode raises ValueError."""
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    _create_test_pdf(input_pdf, num_pages=1)
    with pytest.raises(ValueError, match="frame.*crop"):
        pdfframecmd.crop_pdf_pages(
            str(input_pdf), str(output_pdf),
            page_indexes=[0],
            crop_box=(10, 10, 600, 780),
            page_width=612, page_height=792,
            mode="invalid",
        )


def test_crop_pdf_pages_logs_parameters_to_stderr(tmp_path, capsys):
    """Arrange/Act/Assert: log_params prints crop parameters to stderr."""
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    _create_test_pdf(input_pdf, num_pages=1)
    pdfframecmd.crop_pdf_pages(
        str(input_pdf), str(output_pdf),
        page_indexes=[0],
        crop_box=(10, 10, 600, 780),
        page_width=612, page_height=792,
        mode="frame", delete_annots=True,
        log_params=True,
    )
    err = capsys.readouterr().err
    assert "PyMuPDF crop" in err
    assert "mode=frame" in err


def test_crop_pdf_pages_debug_output_prints_page_info(tmp_path, capsys):
    """Arrange/Act/Assert: debug_output prints per-page info to stderr."""
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    _create_test_pdf(input_pdf, num_pages=2)
    pdfframecmd.crop_pdf_pages(
        str(input_pdf), str(output_pdf),
        page_indexes=[0, 1],
        crop_box=(10, 10, 600, 780),
        page_width=612, page_height=792,
        mode="frame", delete_annots=False,
        debug_output=True,
    )
    err = capsys.readouterr().err
    assert "Processed page 1" in err
    assert "Processed page 2" in err


def test_crop_pdf_pages_open_failure_raises_crop_error(tmp_path):
    """Arrange/Act/Assert: non-existent input raises CropError."""
    with pytest.raises(pdfframecmd.CropError, match="open PDF"):
        pdfframecmd.crop_pdf_pages(
            str(tmp_path / "nonexistent.pdf"),
            str(tmp_path / "output.pdf"),
            page_indexes=[0],
            crop_box=(10, 10, 600, 780),
            page_width=612, page_height=792,
        )


@pytest.mark.parametrize("mode", ["frame", "crop"])
def test_crop_pdf_pages_both_modes_with_delete_annots(tmp_path, mode):
    """Arrange/Act/Assert: annotation deletion works in both frame and crop modes."""
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    _create_test_pdf(input_pdf, num_pages=1, with_annots=True)
    pdfframecmd.crop_pdf_pages(
        str(input_pdf), str(output_pdf),
        page_indexes=[0],
        crop_box=(10, 10, 600, 780),
        page_width=612, page_height=792,
        mode=mode, delete_annots=True,
    )
    doc = fitz.open(str(output_pdf))
    assert len(list(doc[0].annots())) == 0
    doc.close()


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


def test_crop_pdf_pages_frame_mode_blanks_outside_selection(tmp_path):
    """Arrange/Act/Assert: frame mode draws white fill outside selection area."""
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    doc = fitz.open()
    page = doc.new_page(width=612, height=792)
    page.draw_rect(fitz.Rect(0, 0, 612, 792), fill=(0, 0, 0))
    doc.save(str(input_pdf))
    doc.close()
    pdfframecmd.crop_pdf_pages(
        str(input_pdf), str(output_pdf),
        page_indexes=[0],
        crop_box=(100, 200, 500, 700),
        page_width=612, page_height=792,
        mode="frame", delete_annots=False,
    )
    doc = fitz.open(str(output_pdf))
    page = doc[0]
    pix = page.get_pixmap()
    corner_sample = pix.pixel(5, 5)
    assert corner_sample[0] == 255 and corner_sample[1] == 255
    doc.close()


def test_crop_pdf_pages_deletes_all_annotation_types(tmp_path):
    """Arrange/Act/Assert: delete_annots removes annotations including links."""
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    doc = fitz.open()
    page = doc.new_page(width=612, height=792)
    page.add_text_annot((72, 72), "Text annot")
    page.insert_link({
        "kind": fitz.LINK_URI,
        "from": fitz.Rect(100, 100, 200, 200),
        "uri": "https://example.com",
    })
    doc.save(str(input_pdf))
    doc.close()
    pdfframecmd.crop_pdf_pages(
        str(input_pdf), str(output_pdf),
        page_indexes=[0],
        crop_box=(10, 10, 600, 780),
        page_width=612, page_height=792,
        mode="frame", delete_annots=True,
    )
    doc = fitz.open(str(output_pdf))
    page = doc[0]
    assert len(list(page.annots())) == 0
    assert len(page.get_links()) == 0
    xref_str = doc.xref_object(page.xref)
    assert "/Annots null" in xref_str
    doc.close()


def test_crop_pdf_pages_event_pump_called_before_save(tmp_path):
    """Arrange/Act/Assert: event_pump is called once more than page count."""
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    _create_test_pdf(input_pdf, num_pages=2)
    pump_count = [0]
    pdfframecmd.crop_pdf_pages(
        str(input_pdf), str(output_pdf),
        page_indexes=[0, 1],
        crop_box=(10, 10, 600, 780),
        page_width=612, page_height=792,
        mode="frame", delete_annots=False,
        event_pump=lambda: pump_count.__setitem__(0, pump_count[0] + 1),
    )
    assert pump_count[0] == 3


def test_crop_pdf_pages_frame_mode_physically_removes_text(tmp_path):
    """Arrange/Act/Assert: frame mode removes text outside selection from content stream."""
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    doc = fitz.open()
    page = doc.new_page(width=612, height=792)
    page.insert_text((50, 50), "OUTSIDE_TEXT", fontsize=12)
    page.insert_text((300, 400), "INSIDE_TEXT", fontsize=12)
    doc.save(str(input_pdf))
    doc.close()
    pdfframecmd.crop_pdf_pages(
        str(input_pdf), str(output_pdf),
        page_indexes=[0],
        crop_box=(200, 200, 500, 600),
        page_width=612, page_height=792,
        mode="frame", delete_annots=False,
    )
    doc = fitz.open(str(output_pdf))
    text = doc[0].get_text()
    assert "OUTSIDE_TEXT" not in text
    assert "INSIDE_TEXT" in text
    doc.close()


def test_crop_pdf_pages_crop_mode_physically_removes_text(tmp_path):
    """Arrange/Act/Assert: crop mode removes text outside selection from content stream."""
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    doc = fitz.open()
    page = doc.new_page(width=612, height=792)
    page.insert_text((50, 50), "HIDDEN_ARTIFACT", fontsize=12)
    page.insert_text((300, 400), "KEPT_CONTENT", fontsize=12)
    doc.save(str(input_pdf))
    doc.close()
    pdfframecmd.crop_pdf_pages(
        str(input_pdf), str(output_pdf),
        page_indexes=[0],
        crop_box=(200, 200, 500, 600),
        page_width=612, page_height=792,
        mode="crop", delete_annots=False,
    )
    doc = fitz.open(str(output_pdf))
    text = doc[0].get_text()
    assert "HIDDEN_ARTIFACT" not in text
    assert "KEPT_CONTENT" in text
    doc.close()
