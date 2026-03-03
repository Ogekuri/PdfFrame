# useReq/req (0.4.0)

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/license-GPL--3.0-491?style=flat-square" alt="License: GPL-3.0">
  <img src="https://img.shields.io/badge/platform-Linux-6A7EC2?style=flat-square&logo=terminal&logoColor=white" alt="Platforms">
  <img src="https://img.shields.io/badge/docs-live-b31b1b" alt="Docs">
<img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv">
</p>

<p align="center">
<strong>The <u>PdfFrame</u> crops PDF files with PyMuPDF.</strong><br>
PdfFrame is a desktop tool to crop or frame PDF pages with visual selection, margin trimming, and reusable margin presets.
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> |
  <a href="#feature-highlights">Feature Highlights</a> |
  <a href="#acknowledgments">Acknowledgments</a>
</p>

<p align="center">
<br>
🚧 <strong>DRAFT:</strong>Preliminary Version 📝 - Work in Progress 🏗️ 🚧<br>
⚠️ <strong>IMPORTANT NOTICE</strong>: Created with <a href="https://github.com/ogekuri/useReq"><strong>useReq/req</strong></a> 🤖✨ ⚠️<br>
<br>
<p>


## Feature Highlights
- Toolbar actions `Trim Margins`, `Save Margins`, and `Go!` use dedicated bundled icons for consistent appearance.
- `Save Margins` is placed next to `Trim Margins`, and `Go!` is placed at the far right of the toolbar.
- `Extra operations on the final PDF` includes `Delete annotations fields` (enabled by default).
- Conversion `Mode` supports `Frame` (keep original page size) and `Crop` (shrink page size to the selected area).
- Only one trim/selection area is supported at a time; grid values above one area are reduced to one area.
- `Trim settings` and `Presets` are available in the Basic tab, and `Save Margins` stores reusable presets.

## Screenshot

[![PdfFrame](https://raw.githubusercontent.com/Ogekuri/PdfFrame/refs/heads/master/images/screenshot.png)](https://raw.githubusercontent.com/Ogekuri/PdfFrame/refs/heads/master/images/screenshot.png)


## Quick Start

1. Open a PDF file.
2. Use `Trim Margins` to auto-trim the current page/selected range.
3. Select `Mode`:
   - `Frame`: keep the original page size and crop visible content.
   - `Crop`: resize each output page to the selected area.
4. (Optional) In `Extra operations on the final PDF`, uncheck `Delete annotations fields` if you want to keep annotations/widgets.
5. Use `Save Margins` to store the current crop/frame setup as a preset.
6. Click `Go!` to generate the output PDF.

## CLI usage

```bash
pdfframe [file] [options]
```

### Core options
- `-o, --output`: output PDF path.
- `--whichpages`: one page range to process (`N`, `N-`, `-N`, `N-M`).
- `--mode {frame,crop}`: conversion mode.
- `--grid`: initial selection grid; only one selection area is kept.
- `--initialpage`: page opened initially (1-based).
- `--go`: run conversion immediately without opening the GUI window.

### Logging and compatibility options
- `--verbose`: enable console progress output.
- `--debug`: enable extra crop debug output (effective with `--verbose`).
- `--use-qt5`: force PyQt5 (default is PyQt6 when available).
- `--use-pymupdf`: use PyMuPDF rendering (default).
- `--use-poppler`: use Poppler rendering (PyQt5 only).
- `--use-pikepdf`, `--use-pypdf`, `--use-pypdf2`: legacy compatibility flags (no crop backend effect).

## Configuration file

PdfFrame stores runtime options and trim presets in `~/.pdfframe/config.json`.
The file is auto-created on first run and normalized to this shape:

```json
{
  "config": {
    "PDF/DeleteAnnots": true,
    "PDF/Mode": "frame",
    "Trim/Padding": "0",
    "Trim/GrayscaleSensitivity": "0",
    "Trim/Sensitivity": "5",
    "Trim/PagesRangeEnabled": false,
    "Trim/PagesRange": "1-1"
  },
  "presets": []
}
```

## Install with Astral uv

#### Install
```bash
uv tool install pdfframe --force --from git+https://github.com/Ogekuri/PdfFrame.git
```

#### Uninstall
```bash
uv tool uninstall pdfframe
```

## Live execution with uvx

Run PdfFrame directly from the current repository checkout without prior installation:

```bash
uvx --from git+https://github.com/Ogekuri/PdfFrame.git pdfframe
```

You can pass CLI options as usual, for example:

```bash
uvx --from git+https://github.com/Ogekuri/PdfFrame.git pdfframe input.pdf -o output.pdf --go
```


## Acknowledgments

- Thanks to Prof. Armin Straub for developing [Krop](https://arminstraub.com/software/krop).
