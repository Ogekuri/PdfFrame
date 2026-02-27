---
title: "PdfFrame Requirements"
description: Software requirements specification
version: "0.2.1"
date: "2026-02-27"
author: "req-change"
scope:
  paths:
    - "src/pdfframe/**/*.py"
    - "src/pdfframe/mainwindow.ui"
   - "requirements.txt"
   - "pdfframe.sh"
    - "com.ogekuri.pdfframe.desktop"
    - "com.ogekuri.pdfframe.metainfo.xml"
    - "com.ogekuri.pdfframe.svg"
    - ".github/workflows/release-uvx.yml"
    - "tests.sh"
  excludes:
    - ".venv/**"
    - ".git/**"
visibility: "draft"
tags: ["markdown", "requirements", "pdfframe"]
---

# PdfFrame Requirements

## 1. Introduction

### 1.1 Document Rules
This SRS is English-only and uses RFC 2119 keywords (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY) with stable requirement IDs and atomic single-sentence requirements optimized for machine parsing.

### 1.2 Project Scope
PdfFrame implements PDF page-region cropping through a Qt GUI with optional command-line preconfiguration and batch execution, computes crop arguments from GUI state, and performs final cropping through external Ghostscript command execution.

### 1.3 Project File/Folder Structure
```text
.
├── .github/
│   └── workflows/
│       ├── .place-holder
│       └── release-uvx.yml
├── docs/
│   ├── .place-holder
│   └── REQUIREMENTS.md
├── src/
│   ├── .place-holder
│   └── pdfframe/
│       ├── __init__.py
│       ├── __main__.py
│       ├── application.py
│       ├── autotrim.py
│       ├── config.py
│       ├── mainwindow.py
│       ├── mainwindow.ui
│       ├── mainwindowui_qt5.py
│       ├── mainwindowui_qt6.py
│       ├── pdfframeper.py
│       ├── qt.py
│       ├── vieweritem.py
│       ├── viewerselections.py
│       └── version.py
├── tests/
│   └── .place-holder
├── com.ogekuri.pdfframe.desktop
├── com.ogekuri.pdfframe.metainfo.xml
├── com.ogekuri.pdfframe.svg
└── tests.sh
```

### 1.4 Components and Libraries (Evidence-Based)
| Component/Library | Evidence |
| --- | --- |
| Qt bindings (PyQt6/PyQt5) | `src/pdfframe/config.py` imports `PyQt6` then `PyQt5`; `src/pdfframe/qt.py` conditionally imports Qt modules. |
| Rendering backends (PyMuPDF/PopplerQt5) | `src/pdfframe/vieweritem.py` imports `fitz` and optionally `popplerqt5.Poppler`. |
| External crop engine (Ghostscript) | `src/pdfframe/mainwindow.py` builds and executes `gs` command lines that apply page crop boxes. |
| GUI metadata/render backends | `src/pdfframe/vieweritem.py` imports `fitz` and optionally `popplerqt5.Poppler` for page rendering and geometry used by GUI. |
| Desktop/AppStream branding | `com.ogekuri.pdfframe.desktop` and `com.ogekuri.pdfframe.metainfo.xml` use `pdfframe` executable/name and `com.ogekuri.pdfframe` IDs; `com.ogekuri.pdfframe.svg` provides matching icon asset. |
| Release automation | `.github/workflows/release-uvx.yml` defines `check-branch` and `build-release` jobs. |

## 2. Project Requirements

### 2.1 Project Functions
- **PRJ-001**: MUST provide an interactive Qt GUI that loads a PDF, displays pages, allows selection editing, writes a cropped output PDF, and shows conversion progress with user-initiated cancellation.
- **PRJ-002**: MUST expose a CLI entrypoint with program name `pdfframe`, optional input-file and output-file arguments, and desktop integration metadata rooted at application ID `com.ogekuri.pdfframe`.
- **PRJ-003**: MUST map CLI options to GUI state before execution, including selection construction controls, optional `--whichpages` page filtering, crop-parameter controls used to derive Ghostscript crop arguments, and runtime logging flags.
- **PRJ-004**: MUST support non-interactive mode `--go` that schedules cropping and closes the window immediately after startup.
- **PRJ-005**: MUST support automatic initial selection grid creation from `--grid` and optional automatic margin trimming from `--trim`.

### 2.2 Project Constraints
- **CTN-001**: MUST select PyQt6 by default and fall back to PyQt5 when `--use-qt5` is passed or PyQt6 import fails.
- **CTN-002**: MUST raise RuntimeError when neither PyQt6 nor PyQt5 can be imported.
- **CTN-003**: MUST execute final cropping through external `gs` command using Ghostscript-compatible CLI flags and MUST NOT execute output cropping through `pdfframe`.
- **CTN-004**: MUST raise a user-visible error when `gs` executable is unavailable or returns a non-zero exit status.
- **CTN-005**: MUST use PyMuPDF or PopplerQt only for rendering/geometry metadata needed by GUI selection handling.
- **CTN-006**: MUST pass `-dNOPAUSE`, `-dBATCH`, `-dFIXEDMEDIA`, `-dDEVICEWIDTHPOINTS`, `-dDEVICEHEIGHTPOINTS`, and `-dPDFFitPage` in every Ghostscript crop invocation.
- **CTN-007**: MUST treat rotation and include-pages-without-selections as unsupported by the Ghostscript backend and MUST surface explicit warnings when they are requested.
- **CTN-008**: MUST execute release builds only for semantic-version tags whose commit is contained in `origin/master`.
- **CTN-009**: MUST keep GUI behavior and interaction model intact while replacing only the crop execution backend.

Explicit performance optimization identified: lazy page-image caching in `AbstractViewerItem.getImage`.

## 3. Requirements

### 3.1 Design and Implementation
- **DES-001**: MUST implement `MainWindow` as an orchestration layer connecting UI events to `ViewerItem`, `ViewerSelections`, Ghostscript command construction, and `autoTrimMargins`.
- **DES-002**: MUST model selections as `ViewerSelectionItem` graphics items with drag, resize handles, focus management, and page-visibility rules.
- **DES-003**: MUST enforce selection bounds within the displayed page rectangle, minimum size constraints, and optional fixed aspect ratio during resizing.
- **DES-004**: MUST compute crop values as normalized `(left, top, right, bottom)` fractions relative to the page rectangle.
- **DES-005**: MAY split a selection into multiple overlapping rectangles using configured device aspect ratio before crop-value generation.
- **DES-006**: MUST cache rendered page images lazily by page index and reuse cached images until viewer reset.
- **DES-007**: MUST execute cropping by translating GUI selections into Ghostscript arguments, invoking a single `gs` subprocess per conversion request, and capturing streamed conversion output to extract processed page numbers for UI progress updates.
- **DES-008**: MUST route warnings to `QMessageBox` when the window is visible and to `stderr` when the window is hidden.
- **DES-009**: MUST capture and parse Ghostscript output streams (including chunks containing multiple `Page N` tokens) to drive progress updates and MUST NOT display captured stream payload in user-visible failure messages.

### 3.2 Functions
- **REQ-001**: MUST parse `--whichpages` as exactly one range expression in one of these forms: `N`, `N-`, `-N`, or `N-M`, converting it into zero-based page indices.
- **REQ-002**: MUST create selection grids from `CxR` format or a single integer resolved by current page orientation.
- **REQ-003**: MUST apply GUI selections to all processed pages without selection-mode variants or exception-page overrides.
- **REQ-004**: MUST auto-trim selection edges when grayscale changes remain within configured color-sensitivity and grayscale-sensitivity thresholds in the dedicated Basic-tab trim settings section.
- **REQ-005**: MUST default trim page scope to current page only and MAY optionally use all visible pages when user enables the "Use all pages" trim setting exposed in the Basic-tab trim settings section.
- **REQ-006**: MUST expose conversion mode selector with `Frame` and `Crop` options and default to `Frame` at application startup.
- **REQ-007**: MUST show warnings and use safe defaults when grid or trim-settings values (padding, grayscale sensitivity, color sensitivity) are invalid.
- **REQ-008**: MUST process only pages selected by `--whichpages` (or all pages when empty), compute crop parameters from the primary GUI selection only, and execute one Ghostscript command configured with `-dFirstPage` and `-dLastPage` for the selected range.
- **REQ-009**: MUST remove GUI controls for include-pages-without-selections and selection-application modes so these options cannot affect conversion behavior.
- **REQ-010**: MUST invoke Ghostscript with script-style BeginPage clipping commands, using `crop` mode for translated physical cropping and `frame` mode for original-page clipping without scaling.
- **REQ-011**: MUST set default output filename to `<input>-cropped.pdf` after successful file load and disable crop actions when loading fails.
- **REQ-012**: MUST show selection-context menu actions for selection clicks and page-context actions for background clicks.
- **REQ-013**: MUST support Shift+Arrow keyboard movement for pixel-level adjustment of the current selection.
- **REQ-014**: MUST reapply fit-in-view on resize and splitter movement when fit mode is enabled.
- **REQ-015**: MUST open a progress window during conversion, capture Ghostscript output from the single conversion command, extract processed page numbers from page-output lines (including multiple page tokens in one captured chunk), and update a progress bar from `0` to total pages selected for processing.
- **REQ-016**: MUST provide launcher script `pdfframe.sh` that executes the GUI application from project root using the project virtual environment.
- **REQ-017**: MUST expose a stop button in the conversion progress window that allows users to cancel the active Ghostscript process before completion.
- **REQ-018**: MUST support at least five-digit page numbers in GUI current-page, max-page, and page-range input controls without visual truncation.
- **REQ-019**: MUST print the exact Ghostscript command line before conversion execution using deterministic shell-escaped formatting when both `--verbose` and `--debug` are enabled.
- **REQ-020**: MUST remove the Advanced tab and expose trim configuration parameters in a dedicated section at the bottom of the Basic tab.
- **REQ-021**: MUST label the main conversion trigger button as `Go!`.
- **REQ-022**: MUST expose CLI flags `--verbose` and `--debug`; `--verbose` enables Python-side console progress/status output including renderer-selection diagnostics, and `--verbose --debug` additionally prints Ghostscript command and captured Ghostscript output while preserving progress capture.
- **REQ-023**: MUST use `~/.pdfframe/config.json` as persistent configuration storage with top-level objects `config` and `presets`.
- **REQ-024**: MUST create `~/.pdfframe/config.json` with default hardcoded parameter values under `config` when the file is missing at startup.
- **REQ-025**: MUST load `config` values from `~/.pdfframe/config.json` at startup and prioritize them over hardcoded defaults when keys are present.
- **REQ-026**: MUST expose a `Presets` section under Basic-tab trim settings listing crop presets, where selecting a preset applies its saved crop/frame margins to the current crop controls.
- **REQ-027**: MUST expose a `Save Margins` button adjacent to `Trim Margins` that saves current crop/frame margins as a new preset named by default with `%Y/%m/%d %H:%M:%S`.
- **REQ-028**: MUST support preset deletion via a `-` control anchored at the right edge of each preset-list row and preset rename via double-click inline editing, persisting the modified preset name.
- **REQ-029**: MUST persist the full `presets` array to `~/.pdfframe/config.json` after preset add, rename, update, or delete operations.
- **REQ-030**: MUST label the trim threshold field as `Grayscale sensitivity` and provide tooltip/help text that defines it as tolerated grayscale transitions used by margin auto-trimming.

## 4. Test Requirements

Unit tests are implemented under `tests/` and executed through `tests.sh`.

- **TST-001**: MUST execute repository tests through `tests.sh`, creating `.venv` and installing `requirements.txt` when the virtual environment is missing.
- **TST-002**: MUST run `pytest` with `PYTHONPATH` prefixed by `src` and default target `tests` when no arguments are provided.
- **TST-003**: MUST include unit tests that validate Ghostscript script-style command argument construction for `frame` and `crop` modes from GUI-derived crop data.
- **TST-004**: MUST include unit tests that validate failure diagnostics omit captured subprocess payload from user-visible warnings when Ghostscript execution fails and that captured page-output lines (including multiple page tokens in one chunk) drive progress updates from parsed processed page numbers.
- **TST-005**: MUST include unit tests that validate large page-index support, allowed single-range `--whichpages` formats, and primary-selection-only crop planning for one-command range conversion.
- **TST-006**: MUST include unit tests that validate Ghostscript command logging/output toggles (`--verbose`, `--debug`), Ghostscript range command argument assembly, and desktop integration branding identifiers (`pdfframe` / `com.ogekuri.pdfframe`).
- **TST-007**: MUST include unit tests that validate startup config bootstrap at `~/.pdfframe/config.json`, including missing-file creation with `config` defaults and startup override precedence for persisted `config` keys.
- **TST-008**: MUST include unit tests that validate preset list CRUD interactions (save/apply/rename/delete), right-edge alignment behavior of per-row delete controls, and persistence of the `presets` array in `~/.pdfframe/config.json`.
- **TST-009**: MUST include unit tests that validate `Grayscale sensitivity` nomenclature across trim UI labels/tooltips/help text and runtime persistence keys used by trim settings and presets.

## 5. Evidence Matrix

| ID | Evidence (file + symbol + excerpt) |
| --- | --- |
| PRJ-001 | `src/pdfframe/mainwindow.py::slotPdfFrame` creates and updates a progress dialog while `run_ghostscript_command(...)` executes conversion. |
| PRJ-002 | `src/pdfframe/application.py::main` — `ArgumentParser(prog='pdfframe')`, `parser.add_argument('file', nargs='?')`, `parser.add_argument('-o', '--output', ...)`; `com.ogekuri.pdfframe.desktop` and `com.ogekuri.pdfframe.metainfo.xml` use `pdfframe` and `com.ogekuri.pdfframe`. |
| PRJ-003 | `src/pdfframe/application.py::main` — CLI values set UI fields (`editWhichPages`, mode, output), startup actions, and runtime logging flags (`window.verbose`, `window.debug`). |
| PRJ-004 | `src/pdfframe/application.py::main` — `if args.go: QTimer.singleShot(0, window.slotPdfFrame); QTimer.singleShot(0, window.close)`. |
| PRJ-005 | `src/pdfframe/application.py::main` — `if args.grid: window.createSelectionGrid(args.grid)` and `if args.trim: window.slotTrimMarginsAll()`. |
| CTN-001 | `src/pdfframe/config.py` — checks `--use-qt5`, tries `from PyQt6 import QtCore`, then falls back to `from PyQt5 import QtCore`. |
| CTN-002 | `src/pdfframe/config.py` — `except ImportError: raise RuntimeError("Please install PyQt6 (or PyQt5) first.")`. |
| CTN-003 | `src/pdfframe/mainwindow.py::slotPdfFrame` and `src/pdfframe/pdfframecmd.py` — output crop execution occurs through `gs` subprocess commands; no `pdfframe` execution path remains. |
| CTN-004 | `src/pdfframe/mainwindow.py::slotPdfFrame` — checks `which('gs')` and warns when executable is missing; command-error path handles non-zero exits. |
| CTN-005 | `src/pdfframe/vieweritem.py` — PyQt6 branch requires `fitz`; PyQt5 branch tries `fitz` then `popplerqt5`; raises RuntimeError when unavailable. |
| CTN-006 | `src/pdfframe/pdfframecmd.py::build_ghostscript_page_crop_command` — command vector includes fixed-media Ghostscript crop flags. |
| CTN-007 | `src/pdfframe/mainwindow.py::requestedUnsupportedGhostscriptOptions` and `slotPdfFrame` — rotation and include-pages-without-selections trigger explicit warning and abort. |
| CTN-008 | `.github/workflows/release-uvx.yml::check-branch/build-release` — `if: needs.check-branch.outputs.is_master == 'true'` with semantic tag trigger. |
| CTN-009 | `src/pdfframe/mainwindow.py` keeps selection/edit/trim GUI flows unchanged while replacing only crop execution path inside `slotPdfFrame`. |
| DES-001 | `src/pdfframe/mainwindow.py::MainWindow` imports/uses `ViewerItem`, `ViewerSelections`, Ghostscript command helpers, and `autoTrimMargins`. |
| DES-002 | `src/pdfframe/viewerselections.py::ViewerSelectionItem` and handle classes define selection item behavior, focus, and drag/resize controls. |
| DES-003 | `src/pdfframe/viewerselections.py::adjustBoundingRect` — clamps to parent rect, enforces minimum width/height, and applies `aspectRatio` logic. |
| DES-004 | `src/pdfframe/viewerselections.py::cropValues` — computes normalized crop fractions from selection and parent rectangles. |
| DES-005 | `src/pdfframe/viewerselections.py::distributeRect` — splits selection into multiple aspect-ratio pieces with overlap calculation. |
| DES-006 | `src/pdfframe/vieweritem.py::getImage` — `if self._images[idx] is None: self._images[idx] = self.cacheImage(idx)`. |
| DES-007 | `src/pdfframe/mainwindow.py::buildGhostscriptCropPlan/slotPdfFrame` plus `src/pdfframe/pdfframecmd.py::run_ghostscript_command` — constructs one command with selected range bounds, captures streamed output lines, parses processed page numbers, and executes subprocess-based crop flow. |
| DES-008 | `src/pdfframe/mainwindow.py::showWarning` — visible window uses `QMessageBox.warning`, hidden window writes warning text to `stderr`. |
| DES-009 | `src/pdfframe/pdfframecmd.py::run_ghostscript_command` streams/captures subprocess output and `src/pdfframe/mainwindow.py::slotPdfFrame` parses page numbers (including multiple tokens per chunk) for progress while keeping captured payload out of user-visible warnings. |
| REQ-001 | `src/pdfframe/mainwindow.py::str2pages` — accepts only one range token (`N`, `N-`, `-N`, `N-M`) and returns zero-based indices. |
| REQ-002 | `src/pdfframe/mainwindow.py::createSelectionGrid` — parses `grid.split('x')`, supports single value orientation-dependent rows/cols. |
| REQ-003 | `src/pdfframe/viewerselections.py::selectionVisibleOnPage` applies selections uniformly to all processed pages without mode-dependent branching. |
| REQ-004 | `src/pdfframe/mainwindow.py::trimMarginsSelection` reads color/grayscale sensitivity thresholds from Basic-tab controls and `src/pdfframe/autotrim.py::autoTrimMargins` applies them to edge trimming. |
| REQ-005 | `src/pdfframe/mainwindow.py::trimMarginsSelection` defaults to current page and conditionally uses all visible pages via `checkTrimUseAllPages` checkbox. |
| REQ-006 | `src/pdfframe/mainwindow.py` creates `Mode` radio controls with default `Frame` and `Crop` alternate mode. |
| REQ-007 | `src/pdfframe/mainwindow.py::createSelectionGrid/getPadding/trimMarginsSelection` — invalid grid or trim-settings values (`padding`, `grayscale sensitivity`, `color sensitivity`) trigger `showWarning(...)` and fallback defaults. |
| REQ-008 | `src/pdfframe/mainwindow.py::buildGhostscriptCropPlan` processes only requested pages, derives geometry from the primary selection tuple, and emits one command using `-dFirstPage/-dLastPage`. |
| REQ-009 | `src/pdfframe/mainwindow.py` removes include-without-selections and selection-mode controls from conversion flow. |
| REQ-010 | `src/pdfframe/pdfframecmd.py::build_ghostscript_page_crop_command` emits script-style BeginPage clipping commands for `frame` and `crop` modes with matching page bounds. |
| REQ-011 | `src/pdfframe/mainwindow.py::openFile` — sets `"%s-cropped.pdf"` output name on success and toggles `actionPdfFrame`/`actionTrimMarginsAll` by viewer emptiness. |
| REQ-012 | `src/pdfframe/mainwindow.py::slotContextMenu` — adds selection actions (`Delete`, `Trim Margins`) only for selection context; otherwise adds `Trim Margins All`. |
| REQ-013 | `src/pdfframe/viewerselections.py::ViewerSelectionItem.keyPressEvent` — Shift+Arrow calls `moveBoundingRect` with one-pixel deltas. |
| REQ-014 | `src/pdfframe/mainwindow.py::slotSplitterMoved/resizeEvent/slotFitInView` reapply fit behavior when fit mode is checked. |
| REQ-015 | `src/pdfframe/mainwindow.py::slotPdfFrame` captures single-command output and uses parsed processed page numbers from `src/pdfframe/pdfframecmd.py::extract_ghostscript_page_numbers` to advance progress. |
| REQ-016 | `pdfframe.sh` creates/uses project virtual environment and starts GUI with `PYTHONPATH=<repo>/src ... -m pdfframe`. |
| REQ-017 | `src/pdfframe/mainwindow.py::slotPdfFrame` checks progress dialog cancel state and triggers command cancellation path in `run_ghostscript_command`. |
| REQ-018 | `src/pdfframe/mainwindow.ui`, `src/pdfframe/mainwindowui_qt5.py`, and `src/pdfframe/mainwindowui_qt6.py` define widened page-number controls for values beyond four digits. |
| REQ-019 | `src/pdfframe/mainwindow.py::slotPdfFrame` passes verbose/debug flags to `src/pdfframe/pdfframecmd.py::run_ghostscript_command(log_command=..., debug_output=...)`, which conditionally emits shell-escaped command lines. |
| REQ-020 | `src/pdfframe/mainwindow.py` relocates trim settings to the Basic tab and removes the Advanced tab from the interactive workflow. |
| REQ-021 | `src/pdfframe/mainwindow.py` and `src/pdfframe/mainwindow.ui` define the conversion trigger label as `Go!`. |
| REQ-022 | `src/pdfframe/application.py::main` defines `--verbose`/`--debug`; `src/pdfframe/vieweritem.py` gates renderer-selection diagnostics by `--verbose`; `src/pdfframe/mainwindow.py::slotPdfFrame` and `src/pdfframe/pdfframecmd.py::run_ghostscript_command` enforce verbose/debug Ghostscript logging behavior. |
| REQ-023 | `src/pdfframe/jsonconfig.py::default_config_path/default_config_document/JsonConfigStore._normalize_document` and `src/pdfframe/mainwindow.py::MainWindow.__init__` define and consume JSON storage at `~/.pdfframe/config.json` with `config` and `presets`. |
| REQ-024 | `src/pdfframe/jsonconfig.py::JsonConfigStore.load_or_initialize` creates missing `~/.pdfframe/config.json` using `default_config_document()` values. |
| REQ-025 | `src/pdfframe/mainwindow.py::readSettings` loads `config` values via `JsonConfigStore.load_or_initialize` and applies them to runtime controls instead of hardcoded defaults. |
| REQ-026 | `src/pdfframe/mainwindow.py::_setupTrimPresetControls/slotTrimPresetClicked/_applyTrimPreset` adds `Presets` section under trim settings and applies selected preset values to crop controls/selection. |
| REQ-027 | `src/pdfframe/mainwindow.py::_setupTrimPresetAction/slotSaveMarginsPreset/_defaultTrimPresetName` adds `Save Margins` button adjacent to trim action and creates timestamp-named presets `%Y/%m/%d %H:%M:%S`. |
| REQ-028 | `src/pdfframe/mainwindow.py::_refreshTrimPresetList/slotDeleteTrimPreset/slotTrimPresetDoubleClicked/slotTrimPresetChanged` implements per-entry `-` deletion anchored at row right edge and double-click rename with persisted names. |
| REQ-029 | `src/pdfframe/mainwindow.py::_persistTrimPresetDocument` plus calls in `slotSaveMarginsPreset`, `slotTrimPresetChanged`, `slotDeleteTrimPreset`, and `writeSettings` persist updated `presets` arrays to JSON config. |
| REQ-030 | `src/pdfframe/mainwindow.ui`, `src/pdfframe/mainwindowui_qt5.py`, and `src/pdfframe/mainwindowui_qt6.py` label trim threshold as `Grayscale sensitivity` and define tooltip/help semantics for tolerated grayscale transitions. |
| TST-001 | `tests.sh` — creates `.venv` when missing and installs `requirements.txt` before invoking pytest. |
| TST-002 | `tests.sh` — default `set -- tests` and runs `PYTHONPATH="${SCRIPT_PATH}/src:${PYTHONPATH}" ${VENVDIR}/bin/python3 -m 'pytest' "$@"`. |
| TST-003 | `tests/test_pdfframecmd.py` validates script-style Ghostscript command generation for `frame` and `crop` modes. |
| TST-004 | `tests/test_mainwindow_conversion_errors.py`, `tests/test_pdfframecmd.py`, and `tests/test_mainwindow_progress_updates.py` validate warning payload redaction and captured page-output callbacks (including multi-token chunks) that drive progress updates from parsed page numbers. |
| TST-005 | `tests/test_mainwindow_whichpages.py` verifies accepted/rejected `--whichpages` single-range formats, primary-selection-only planning, and large page-index range behavior. |
| TST-006 | `tests/test_pdfframecmd.py` and `tests/test_mainwindow_progress_updates.py` validate command/output logging toggles and Ghostscript range-argument command assembly; `tests/test_desktop_metadata_branding.py` validates desktop/AppStream branding identifiers. |
| TST-007 | `tests/test_jsonconfig.py` validates JSON bootstrap default creation and persisted-config override precedence with default-key backfill. |
| TST-008 | `tests/test_mainwindow_presets.py` validates preset snapshot/apply/rename/delete/save behavior, right-edge delete-control row layout, and persistence trigger paths. |
| TST-009 | `tests/test_mainwindow_trim_settings.py` and `tests/test_mainwindow_presets.py` validate `grayscale_sensitivity` runtime/preset keys; `tests/test_mainwindow_trim_nomenclature.py` validates renamed UI labels/tooltips/help semantics. |

## 6. Test Coverage Summary

Repository unit tests currently target the Ghostscript command backend helper module (`tests/test_pdfframecmd.py`), while GUI interaction behavior remains covered by runtime/manual verification paths.
