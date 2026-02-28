# useReq/req (0.3.0)

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/license-GPL--3.0-491?style=flat-square" alt="License: GPL-3.0">
  <img src="https://img.shields.io/badge/platform-Linux-6A7EC2?style=flat-square&logo=terminal&logoColor=white" alt="Platforms">
  <img src="https://img.shields.io/badge/docs-live-b31b1b" alt="Docs">
<img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv">
</p>

<p align="center">
<strong>The <u>PdfFrame</u> crop pdf files with ghostscript.</strong><br>
PdfFrame is a desktop tool to crop or frame PDF pages with Ghostscript, including visual selection, margin trimming, and reusable margin presets.
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
- `Extra operations on the final PDF` includes `Preserve annotations fields` and `Show annotations fields`, both disabled by default.

## Screenshot

[![PdfFrame](https://raw.githubusercontent.com/Ogekuri/PdfFrame/refs/heads/master/images/screenshot.png)](https://raw.githubusercontent.com/Ogekuri/PdfFrame/refs/heads/master/images/screenshot.png)


## Quick Start

1. Open a PDF file.
2. Use `Trim Margins` to auto-trim the current page/selected range.
3. Use `Save Margins` to store the current crop/frame setup as a preset.
4. (Optional) In `Extra operations on the final PDF`, enable `Preserve annotations fields` and/or `Show annotations fields`.
5. Click `Go!` to generate the output PDF.

## Install with Astral uv

1. Install uv (Linux/macOS):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
2. Install PdfFrame as a local tool from this repository:
   ```bash
   uv tool install .
   ```
3. Run the installed command:
   ```bash
   pdfframe
   ```

## Live execution with uvx

Run PdfFrame directly from the current repository checkout without prior installation:

```bash
uvx --from . pdfframe
```

You can pass CLI options as usual, for example:

```bash
uvx --from . pdfframe input.pdf -o output.pdf --go
```


## Acknowledgments

- Thanks to Prof. Armin Straub for developing [Krop](https://arminstraub.com/software/krop).
