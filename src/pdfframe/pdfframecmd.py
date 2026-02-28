# -*- coding: iso-8859-1 -*-

"""
Ghostscript command integration utilities for pdfframe.

Copyright (C) 2010-2025 Ogekuri
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

import importlib
import queue
import re
import shlex
import subprocess
import sys
import threading
import time


class GhostscriptCommandError(RuntimeError):
    """
    @brief Represents a failed Ghostscript subprocess execution.
    @details Encapsulates command vector, return code, and captured streams so caller code can emit deterministic diagnostics for GUI and terminal paths.
    @param command {list[str]} Executed command vector passed to subprocess.
    @param returncode {int} Process exit code returned by subprocess.
    @param stdout {str} Captured standard output text.
    @param stderr {str} Captured standard error text.
    @return {None} Constructs exception payload and error message.
    """

    def __init__(self, command, returncode, stdout, stderr):
        self.command = command
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        super().__init__(f"ghostscript exited with status {returncode}")


class GhostscriptCommandCancelledError(RuntimeError):
    """
    @brief Represents user-requested cancellation of Ghostscript execution.
    @details Encapsulates executed command and partial output captured before termination so caller code can report deterministic cancellation diagnostics.
    @param command {list[str]} Executed command vector passed to subprocess.
    @param stdout {str} Partial captured standard output text.
    @return {None} Constructs exception payload and error message.
    """

    def __init__(self, command, stdout):
        self.command = command
        self.stdout = stdout
        super().__init__("ghostscript execution cancelled")


def _format_scalar(value):
    """
    @brief Converts numeric values to stable CLI scalar strings.
    @details Emits integer-like values without decimal suffix and non-integers with compact decimal representation to keep generated command arguments deterministic for tests.
    @param value {float|int} Numeric value to format.
    @return {str} Stable scalar representation for CLI arguments.
    """

    numeric = float(value)
    if numeric.is_integer():
        return str(int(numeric))
    return f"{numeric:.6f}".rstrip("0").rstrip(".")


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


def build_ghostscript_page_crop_command(input_path, output_path, first_page,
    last_page,
    page_width, page_height, crop_box, mode="frame", preserve_annots=False,
    show_annots=False, command_name="gs"):
    """
    @brief Builds Ghostscript command vector for cropping a page range.
    @details Assembles script-style pdfwrite command with BeginPage clipping for selected pages, using either physical crop (`crop`) or original-size clipped output (`frame`).
    @param input_path {str} Source PDF path.
    @param output_path {str} Destination output PDF path.
    @param first_page {int} One-based first page index to process.
    @param last_page {int} One-based last page index to process.
    @param page_width {float} Target media width in points.
    @param page_height {float} Target media height in points.
    @param crop_box {tuple[float,float,float,float]} Crop box in left,bottom,right,top order.
    @param mode {str} Conversion mode (`frame` or `crop`).
    @param preserve_annots {bool} When True, passes `-dPreserveAnnots=true`; otherwise `-dPreserveAnnots=false`.
    @param show_annots {bool} When True, passes `-dShowAnnots=true`; otherwise `-dShowAnnots=false`.
    @param command_name {str} Executable name for Ghostscript binary.
    @return {list[str]} Complete subprocess command vector.
    @throws {ValueError} If mode is not supported or crop size is invalid.
    """

    left, bottom, right, top = [float(v) for v in crop_box]
    crop_width = right - left
    crop_height = top - bottom
    if crop_width <= 0 or crop_height <= 0:
        raise ValueError("Calculated crop size must be positive.")
    if int(first_page) <= 0 or int(last_page) <= 0 or int(first_page) > int(last_page):
        raise ValueError("Page range must satisfy 1 <= first_page <= last_page.")
    if mode not in {"frame", "crop"}:
        raise ValueError("Mode must be either `frame` or `crop`.")
    left_value = _format_scalar(left)
    bottom_value = _format_scalar(bottom)
    crop_width_value = _format_scalar(crop_width)
    crop_height_value = _format_scalar(crop_height)
    page_width_value = _format_scalar(page_width)
    page_height_value = _format_scalar(page_height)
    if mode == "crop":
        device_width_value = crop_width_value
        device_height_value = crop_height_value
        begin_page = (
            f"<</BeginPage{{0 0 {crop_width_value} {crop_height_value} rectclip "
            f"-{left_value} -{bottom_value} translate}}>> setpagedevice"
        )
    else:
        device_width_value = page_width_value
        device_height_value = page_height_value
        begin_page = (
            f"<</BeginPage{{{left_value} {bottom_value} {crop_width_value} "
            f"{crop_height_value} rectclip}}>> setpagedevice"
        )
    return [
        command_name,
        "-dSAFER",
        "-dNOPAUSE",
        "-dBATCH",
        "-sDEVICE=pdfwrite",
        "-dAutoRotatePages=/None",
        "-dFIXEDMEDIA",
        "-dModifiesPageSize=true",
        f"-dPreserveAnnots={'true' if preserve_annots else 'false'}",
        f"-dShowAnnots={'true' if show_annots else 'false'}",
        f"-dFirstPage={int(first_page)}",
        f"-dLastPage={int(last_page)}",
        f"-dDEVICEWIDTHPOINTS={device_width_value}",
        f"-dDEVICEHEIGHTPOINTS={device_height_value}",
        "-o",
        output_path,
        "-c",
        begin_page,
        "-f",
        input_path,
    ]


def extract_ghostscript_page_numbers(line):
    """
    @brief Extracts all processed page indices from Ghostscript output text.
    @details Parses each output line that matches `^Page\\s+\\d+\\n` in the provided chunk and returns one-based page numbers in encounter order.
    @param line {str} One output line or chunk produced by Ghostscript.
    @return {list[int]} Processed page numbers found in the chunk.
    """

    normalized = line.replace("\r", "\n")
    return [int(match.group(1)) for match in re.finditer(r"(?m)^Page\s+(\d+)\n", normalized)]


def extract_ghostscript_page_number(line):
    """
    @brief Extracts processed page index from Ghostscript output lines.
    @details Parses `Page N` line format emitted by Ghostscript and returns one-based page number when a match is present.
    @param line {str} One output line produced by Ghostscript.
    @return {int|None} Processed page number or None when line does not contain page progress information.
    """

    page_numbers = extract_ghostscript_page_numbers(line)
    if not page_numbers:
        return None
    return page_numbers[-1]


def format_shell_command(command):
    """
    @brief Formats command vectors into deterministic shell-escaped strings.
    @details Serializes subprocess command vectors with POSIX shell escaping to provide exact reproducible command diagnostics.
    @param command {list[str]} Subprocess command vector.
    @return {str} Shell-escaped command string preserving argument boundaries.
    """

    return shlex.join([str(value) for value in command])


def write_cropped_pages_output(output_file_name, cropped_page_paths):
    """
    @brief Writes output PDF using only selected cropped page files.
    @details Loads one-page cropped PDF files in provided order and writes a new output PDF that contains exactly those pages.
    @param output_file_name {str} Destination PDF file path.
    @param cropped_page_paths {list[str]} Ordered one-page cropped PDF paths selected for export.
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


def run_ghostscript_command(command, event_pump=None, poll_interval=0.05,
    output_callback=None, cancel_requested=None, log_command=False, debug_output=False):
    """
    @brief Executes Ghostscript and captures subprocess output streams.
    @details Runs subprocess in text mode, captures output for deterministic diagnostics, optionally streams output lines through a callback, optionally pumps UI events while process is running, and supports user-requested cancellation.
    @param command {list[str]} Complete subprocess command vector.
    @param event_pump {callable|None} Optional callback invoked repeatedly while subprocess execution is in progress.
    @param poll_interval {float} Seconds to wait between event-pump cycles when callback mode is enabled.
    @param output_callback {callable|None} Optional callback receiving each streamed output line.
    @param cancel_requested {callable|None} Optional callback returning True when subprocess should be cancelled.
    @param log_command {bool} When True, prints the shell-escaped command line before execution.
    @param debug_output {bool} When True, prints captured Ghostscript output to stderr while preserving capture behavior.
    @return {subprocess.CompletedProcess[str]} Successful subprocess result with captured streams.
    @throws {GhostscriptCommandError} If Ghostscript exits with non-zero status.
    @throws {GhostscriptCommandCancelledError} If cancellation callback requests process termination.
    """

    if log_command:
        sys.stderr.write(f"Executing Ghostscript command: {format_shell_command(command)}\n")
    stream_mode = event_pump is not None or output_callback is not None or cancel_requested is not None
    if not stream_mode:
        result = subprocess.run(command, check=False, text=True, capture_output=True)
        if debug_output and result.stdout:
            sys.stderr.write(result.stdout)
    else:
        process = subprocess.Popen(command, text=True, bufsize=1,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output_queue = queue.Queue()

        def reader():
            stream = process.stdout
            if stream is None:
                return
            for line in iter(stream.readline, ""):
                output_queue.put(line)
            stream.close()

        reader_thread = threading.Thread(target=reader, daemon=True)
        reader_thread.start()
        captured_lines = []
        was_cancelled = False
        while True:
            if event_pump is not None:
                event_pump()
            while not output_queue.empty():
                line = output_queue.get_nowait()
                captured_lines.append(line)
                if debug_output:
                    sys.stderr.write(line)
                if output_callback is not None:
                    output_callback(line)
            if (cancel_requested is not None and not was_cancelled and process.poll() is None
                    and cancel_requested()):
                was_cancelled = True
                process.terminate()
            if process.poll() is not None and output_queue.empty() and not reader_thread.is_alive():
                break
            if poll_interval > 0:
                time.sleep(poll_interval)
        reader_thread.join(timeout=1.0)
        if process.poll() is None:
            process.kill()
        returncode = process.wait()
        stdout = "".join(captured_lines)
        result = subprocess.CompletedProcess(command, returncode, stdout=stdout, stderr="")
        if was_cancelled:
            raise GhostscriptCommandCancelledError(command, stdout)
    if result.returncode != 0:
        raise GhostscriptCommandError(command, result.returncode, result.stdout, result.stderr)
    return result
