# -*- coding: iso-8859-1 -*-

"""
@file pdfframecmd.py
@brief PyMuPDF-based PDF crop/frame utilities for pdfframe.
@details Provides crop-box geometry helpers and iterative page processing
through the PyMuPDF `fitz` API with per-page progress reporting,
cancellation support, annotation deletion, and bookmark preservation.

Copyright (C) 2010-2025 Ogekuri
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

import importlib
import sys

import fitz


class CropError(RuntimeError):
    """
    @brief Represents a failed PDF crop operation.
    @details Encapsulates error context so caller code can emit deterministic
    diagnostics for GUI and terminal paths.
    @param message {str} Human-readable error description.
    @return {None} Constructs exception payload.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class CropCancelledError(RuntimeError):
    """
    @brief Represents user-requested cancellation of crop processing.
    @details Raised when the cancel callback returns True between page iterations.
    @return {None} Constructs exception payload.
    """

    def __init__(self):
        super().__init__("PDF crop cancelled by user")


def _format_scalar(value):
    """
    @brief Converts numeric values to stable scalar strings.
    @details Emits integer-like values without decimal suffix and non-integers with compact decimal representation for deterministic logging output.
    @param value {float|int} Numeric value to format.
    @return {str} Stable scalar representation.
    """

    numeric = float(value)
    if numeric.is_integer():
        return str(int(numeric))
    return f"{numeric:.6f}".rstrip("0").rstrip(".")


def _redact_outside_selection(page, selection_rect, page_rect):
    """
    @brief Physically removes page content outside the selection boundary.
    @details Adds redaction annotations (fill=False) for four rectangular
    strips (top, bottom, left, right) around the selection boundary, then
    applies redactions to permanently remove text, images, and line art
    from those areas without drawing fill rectangles over the redacted
    regions. Content inside the selection is preserved unchanged.
    Uses PyMuPDF redaction API with PDF_REDACT_IMAGE_REMOVE and
    PDF_REDACT_LINE_ART_REMOVE_IF_TOUCHED to ensure no hidden artifacts remain.
    @param page {fitz.Page} PyMuPDF page object to redact.
    @param selection_rect {fitz.Rect} Selection boundary in PyMuPDF
    coordinates (top-left origin).
    @param page_rect {fitz.Rect} Full page boundary (MediaBox) in PyMuPDF
    coordinates.
    @return {None} Modifies page content stream in place; removed content
    is irrecoverable.
    """

    has_redactions = False
    if selection_rect.y0 > page_rect.y0:
        page.add_redact_annot(
            fitz.Rect(page_rect.x0, page_rect.y0,
                      page_rect.x1, selection_rect.y0),
            fill=False)
        has_redactions = True
    if selection_rect.y1 < page_rect.y1:
        page.add_redact_annot(
            fitz.Rect(page_rect.x0, selection_rect.y1,
                      page_rect.x1, page_rect.y1),
            fill=False)
        has_redactions = True
    if selection_rect.x0 > page_rect.x0:
        page.add_redact_annot(
            fitz.Rect(page_rect.x0, selection_rect.y0,
                      selection_rect.x0, selection_rect.y1),
            fill=False)
        has_redactions = True
    if selection_rect.x1 < page_rect.x1:
        page.add_redact_annot(
            fitz.Rect(selection_rect.x1, selection_rect.y0,
                      page_rect.x1, selection_rect.y1),
            fill=False)
        has_redactions = True
    if has_redactions:
        page.apply_redactions(
            images=fitz.PDF_REDACT_IMAGE_REMOVE,
            graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_TOUCHED,
        )


def padding_to_crop_offsets(padding):
    """
    @brief Reorders GUI padding vector to crop-offset order.
    @details Converts GUI tuple [top, right, bottom, left] to crop-offset tuple [left, top, right, bottom] for deterministic crop-box expansion.
    @param padding {list[float]|tuple[float,float,float,float]} GUI padding vector with exactly four components.
    @return {tuple[float,float,float,float]} Crop-offset tuple ordered as left, top, right, bottom.
    @throws {ValueError} If padding vector does not contain exactly four values.
    """

    if len(padding) != 4:
        raise ValueError("Padding vector must have exactly four values.")
    top, right, bottom, left = [float(v) for v in padding]
    return left, top, right, bottom


def crop_values_to_bbox(crop_values, page_width, page_height):
    """
    @brief Converts normalized selection crop values to absolute page-space crop box.
    @details Merges all visible normalized crops into one union box by first converting each GUI-derived normalized crop tuple to CropBox LL/UR page-space coordinates and then taking bounding extents in left,bottom,right,top order.
    @param crop_values {list[tuple[float,float,float,float]]} Normalized crop tuples (left, top, right, bottom).
    @param page_width {float} Page width in points.
    @param page_height {float} Page height in points.
    @return {tuple[float,float,float,float]|None} Crop box tuple or None when no crop values exist.
    @throws {ValueError} If page dimensions are non-positive.
    """

    if not crop_values:
        return None
    width = float(page_width)
    height = float(page_height)
    if width <= 0 or height <= 0:
        raise ValueError("Page dimensions must be positive for bbox conversion.")

    converted_boxes = [
        normalized_crop_tuple_to_bbox(crop_value, width, height)
        for crop_value in crop_values
    ]
    llx = min(box[0] for box in converted_boxes)
    lly = min(box[1] for box in converted_boxes)
    urx = max(box[2] for box in converted_boxes)
    ury = max(box[3] for box in converted_boxes)
    if urx <= llx or ury <= lly:
        raise ValueError("Calculated crop box is empty after margin conversion.")
    return llx, lly, urx, ury


def normalized_crop_tuple_to_bbox(crop_value, page_width, page_height):
    """
    @brief Converts one normalized GUI crop tuple into page-point CropBox coordinates.
    @details Maps normalized GUI tuple `(left, top, right_margin, bottom_margin)` to CropBox corners `(LLx, LLy, URx, URy)` in page-point space with lower-left PDF origin.
    @param crop_value {tuple[float,float,float,float]} Normalized GUI crop tuple.
    @param page_width {float} Page width in points.
    @param page_height {float} Page height in points.
    @return {tuple[float,float,float,float]} CropBox coordinates in left,bottom,right,top order.
    @throws {ValueError} If resulting CropBox is empty.
    """

    left, top, right_margin, bottom_margin = [float(value) for value in crop_value]
    width = float(page_width)
    height = float(page_height)
    llx = left * width
    lly = bottom_margin * height
    urx = (1.0 - right_margin) * width
    ury = (1.0 - top) * height
    if urx <= llx or ury <= lly:
        raise ValueError("Calculated crop box is empty after tuple conversion.")
    return llx, lly, urx, ury


def apply_crop_offsets_to_bbox(bbox, offsets, page_width, page_height):
    """
    @brief Applies GUI crop offsets to an absolute crop box.
    @details Expands or shrinks the crop box by offsets in left,top,right,bottom order and clamps the resulting box to page bounds.
    @param bbox {tuple[float,float,float,float]} Input crop box in left,bottom,right,top order.
    @param offsets {tuple[float,float,float,float]} Crop offsets in left,top,right,bottom order.
    @param page_width {float} Page width in points.
    @param page_height {float} Page height in points.
    @return {tuple[float,float,float,float]} Adjusted crop box in left,bottom,right,top order.
    @throws {ValueError} If resulting crop box is empty after clamping.
    """

    left, bottom, right, top = [float(v) for v in bbox]
    pad_left, pad_top, pad_right, pad_bottom = [float(v) for v in offsets]
    width = float(page_width)
    height = float(page_height)

    adjusted_left = max(0.0, left - pad_left)
    adjusted_bottom = max(0.0, bottom - pad_bottom)
    adjusted_right = min(width, right + pad_right)
    adjusted_top = min(height, top + pad_top)
    if adjusted_right <= adjusted_left or adjusted_top <= adjusted_bottom:
        raise ValueError("Calculated crop box is empty after applying offsets.")
    return adjusted_left, adjusted_bottom, adjusted_right, adjusted_top


def write_cropped_pages_output(output_file_name, cropped_page_paths):
    """
    @brief Writes output PDF using only selected cropped page files.
    @details Loads one-page cropped PDF files in provided order and writes a new
    output PDF that contains exactly those pages.
    @param output_file_name {str} Destination PDF file path.
    @param cropped_page_paths {list[str]} Ordered one-page cropped PDF paths
    selected for export.
    @return {None} Writes assembled output PDF to filesystem.
    @throws {ValueError} If no cropped pages are provided.
    """

    if not cropped_page_paths:
        raise ValueError("At least one cropped page path is required.")
    pypdf_module = importlib.import_module("pypdf")
    PdfReader = pypdf_module.PdfReader
    PdfWriter = pypdf_module.PdfWriter
    writer = PdfWriter()
    for cropped_path in cropped_page_paths:
        reader = PdfReader(cropped_path)
        writer.add_page(reader.pages[0])
    with open(output_file_name, "wb") as output_file:
        writer.write(output_file)


def crop_pdf_pages(
    input_path,
    output_path,
    page_indexes,
    crop_box,
    page_width,
    page_height,
    mode="frame",
    delete_annots=True,
    progress_callback=None,
    cancel_requested=None,
    event_pump=None,
    log_params=False,
    debug_output=False,
):
    """
    @brief Crops/frames PDF pages using PyMuPDF fitz API with physical
    content removal.
    @details Opens the source PDF, selects only requested pages, physically
    removes all content outside the selection boundary via PyMuPDF redaction
    API (no hidden artifacts remain), then applies mode-specific page sizing:
    crop mode resizes to selection bounds, frame mode preserves original
    page dimensions. Optionally deletes all annotations/widgets, preserves
    bookmarks/TOC, and saves the output with garbage collection.
    @param input_path {str} Source PDF file path.
    @param output_path {str} Destination PDF file path.
    @param page_indexes {list[int]} Zero-based page indexes to include.
    @param crop_box {tuple[float,float,float,float]} PDF-coordinate crop box
    as (left, bottom, right, top) where origin is bottom-left.
    @param page_width {float} Original page width in points.
    @param page_height {float} Original page height in points.
    @param mode {str} `"frame"` keeps original page size with CropBox clip;
    `"crop"` physically resizes page to crop area.
    @param delete_annots {bool} When True removes all `/Annots` entries
    using native PyMuPDF annotation/widget API.
    @param progress_callback {callable|None} Called as
    `progress_callback(original_page_number_1based, processed_count, total)`
    after each page is processed.
    @param cancel_requested {callable|None} Returns True to cancel between
    page iterations.
    @param event_pump {callable|None} Pumps UI events between pages.
    @param log_params {bool} Prints crop parameters to stderr before
    processing.
    @param debug_output {bool} Prints per-page processing info to stderr.
    @return {None} Writes cropped PDF to output_path.
    @throws {CropError} If PyMuPDF open/save/crop operations fail.
    @throws {CropCancelledError} If cancel_requested returns True.
    @throws {ValueError} If crop dimensions are non-positive or mode invalid.
    """

    left, bottom, right, top = [float(v) for v in crop_box]
    crop_width = right - left
    crop_height = top - bottom
    if crop_width <= 0 or crop_height <= 0:
        raise ValueError("Calculated crop size must be positive.")
    if mode not in {"frame", "crop"}:
        raise ValueError("Mode must be either `frame` or `crop`.")

    if log_params:
        sys.stderr.write(
            f"PyMuPDF crop: mode={mode}, pages={len(page_indexes)}, "
            f"crop_box=({_format_scalar(left)}, {_format_scalar(bottom)}, "
            f"{_format_scalar(right)}, {_format_scalar(top)}), "
            f"delete_annots={delete_annots}\n"
        )

    try:
        doc = fitz.open(input_path)
    except Exception as exc:
        raise CropError(f"Failed to open PDF: {exc}") from exc

    try:
        toc = doc.get_toc(simple=False)

        doc.select(page_indexes)
        total = len(doc)

        # Convert PDF bbox (bottom-left origin) to PyMuPDF Rect (top-left origin)
        # set_cropbox internally flips y using current mediabox
        pymupdf_crop_rect = fitz.Rect(
            left, page_height - top, right, page_height - bottom
        )

        for idx in range(total):
            if cancel_requested and cancel_requested():
                raise CropCancelledError()

            if event_pump:
                event_pump()

            page = doc[idx]

            # Physically remove content outside selection via redaction
            _redact_outside_selection(page, pymupdf_crop_rect, page.mediabox)

            if mode == "crop":
                # Physically resize page to selection bounds
                page.set_cropbox(pymupdf_crop_rect)
                xref = page.xref
                doc.xref_set_key(
                    xref, "MediaBox",
                    f"[{left} {bottom} {right} {top}]",
                )
            else:
                # Frame mode: keep original page size, content already removed
                page.set_cropbox(page.mediabox)

            if delete_annots:
                for annot in list(page.annots()):
                    page.delete_annot(annot)
                for widget in list(page.widgets()):
                    page.delete_widget(widget)
                doc.xref_set_key(page.xref, "Annots", "null")

            original_page_number = page_indexes[idx] + 1
            if progress_callback:
                progress_callback(original_page_number, idx + 1, total)

            if debug_output:
                sys.stderr.write(f"Processed page {original_page_number}\n")

        if event_pump:
            event_pump()
        if cancel_requested and cancel_requested():
            raise CropCancelledError()

        doc.set_toc(toc)
        doc.save(output_path, garbage=4, deflate=True)
    except (CropCancelledError, ValueError):
        raise
    except Exception as exc:
        raise CropError(f"PDF crop failed: {exc}") from exc
    finally:
        doc.close()
