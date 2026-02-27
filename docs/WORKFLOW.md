## Execution Units Index

- ID: `PROC:main`
  - type: `process`
  - parent_process: `-`
  - role: `Desktop PDF cropping runtime (interactive + --go batch mode)`
  - entrypoint_symbols: `pdfframe.application.main`, `MainWindow.slotPdfFrame`, `MainWindow.slotTrimMarginsAll`
  - defining_files:
    - `src/pdfframe/__main__.py`
    - `src/pdfframe/application.py`
    - `src/pdfframe/mainwindow.py`
    - `src/pdfframe/jsonconfig.py`
    - `src/pdfframe/vieweritem.py`
    - `src/pdfframe/viewerselections.py`
    - `src/pdfframe/pdfframecmd.py`
    - `src/pdfframe/__init__.py`
    - `src/pdfframe/autotrim.py`
- ID: `PROC:gha-check-branch`
  - type: `process`
  - parent_process: `-`
  - role: `GitHub Actions job that validates tag commit ancestry`
  - entrypoint_symbols: `release-uvx.yml::jobs.check-branch`
  - defining_files:
    - `.github/workflows/release-uvx.yml`
- ID: `PROC:gha-build-release`
  - type: `process`
  - parent_process: `-`
  - role: `GitHub Actions job that builds artifacts and publishes release`
  - entrypoint_symbols: `release-uvx.yml::jobs.build-release`
  - defining_files:
    - `.github/workflows/release-uvx.yml`

## Execution Units

### PROC:main

- Entrypoint(s):
  - `pdfframe.application.main(...)` [`src/pdfframe/application.py`]
  - module guard `if __name__ == "__main__": main()` [`src/pdfframe/__main__.py`]
- Lifecycle/trigger:
  - Starts when the `pdfframe` CLI or desktop launcher (`com.ogekuri.pdfframe.desktop`) invokes the Python entrypoint.
  - Initializes `QApplication`, constructs `MainWindow`, applies CLI-derived UI state, then enters Qt event loop via `app.exec()`.
  - Emits renderer-selection stderr diagnostics only when `--verbose` is present in CLI arguments.
  - Stops when window closes or `--go` schedules immediate crop+close using Qt timers.
  - Conversion action `actionPdfFrame` is exposed in the UI with label `Go!`.
  - Threads: no explicit thread creation detected under `src/`; execution remains on the main Qt thread.
- Internal Call-Trace Tree:
  - `main(...)`: parse CLI args, initialize Qt app/window, map verbose/debug runtime flags, and dispatch startup actions [`src/pdfframe/application.py`]
    - `MainWindow.__init__(...)`: wire UI actions, construct scene/viewer, and load persisted settings [`src/pdfframe/mainwindow.py`]
      - `_setupConversionModeControls(...)`: create `Frame`/`Crop` mode controls and set `Frame` as startup default [`src/pdfframe/mainwindow.py`]
      - `_setupTrimSettingsControls(...)`: relocate trim-controls group into Basic tab with all controls visible [`src/pdfframe/mainwindow.py`]
      - `_setupTrimPresetControls(...)`: create Basic-tab `Presets` section with clickable/editable rows and per-row delete buttons anchored to each row right edge [`src/pdfframe/mainwindow.py`]
      - `_setupTrimPresetAction(...)`: add toolbar `Save Margins` action adjacent to `Trim Margins` and connect preset-save slot [`src/pdfframe/mainwindow.py`]
      - `readSettings(...)`: load geometry from QSettings, load runtime `config` and `presets` from `~/.pdfframe/config.json`, and bind values to Basic-tab controls [`src/pdfframe/mainwindow.py`]
        - `JsonConfigStore.load_or_initialize(...)`: create missing JSON config and normalize existing config/preset sections [`src/pdfframe/jsonconfig.py`]
          - `default_config_document(...)`: provide default `config` values and empty `presets` list [`src/pdfframe/jsonconfig.py`]
          - `JsonConfigStore.save(...)`: persist normalized JSON config payload [`src/pdfframe/jsonconfig.py`]
      - `SelAspectRatioTypeManager.loadTypes(...)`: load selection aspect-ratio presets or defaults [`src/pdfframe/mainwindow.py`]
      - `DeviceTypeManager.loadTypes(...)`: load device presets or defaults [`src/pdfframe/mainwindow.py`]
      - `slotFitInView(...)`: apply fit mode when enabled [`src/pdfframe/mainwindow.py`]
    - `MainWindow.openFile(...)`: load initial input PDF, prime output defaults, and enable `Save Margins` when a document is available [`src/pdfframe/mainwindow.py`]
      - `AbstractViewerItem.load(...)`: reset viewer state and load document-specific backend data [`src/pdfframe/vieweritem.py`]
        - `MuPDFViewerItem.doLoad(...)`: open PDF via PyMuPDF backend [`src/pdfframe/vieweritem.py`]
        - `PopplerViewerItem.doLoad(...)`: open PDF via Poppler backend [`src/pdfframe/vieweritem.py`]
        - `AbstractViewerItem.firstPage(...)`: set current page to index `0` [`src/pdfframe/vieweritem.py`]
          - `AbstractViewerItem.setCurrentPageIndex(...)`: update geometry and visibility for the current page [`src/pdfframe/vieweritem.py`]
            - `AbstractViewerItem.getImage(...)`: lazy-load/render page image cache entry [`src/pdfframe/vieweritem.py`]
            - `ViewerSelections.updateSelectionVisibility(...)`: update page-scoped selection visibility [`src/pdfframe/viewerselections.py`]
              - `ViewerSelections.autoSetCurrentSelection(...)`: choose active selection for visible page and delegate scene-safe focus updates [`src/pdfframe/viewerselections.py`]
    - `MainWindow.slotSaveMarginsPreset(...)`: snapshot current mode/trim/crop state into a new timestamp-named preset and persist JSON [`src/pdfframe/mainwindow.py`]
      - `MainWindow._trimPresetFromCurrentSelection(...)`: collect mode, trim settings, and primary crop tuple [`src/pdfframe/mainwindow.py`]
      - `MainWindow._refreshTrimPresetList(...)`: rebuild preset rows and per-row delete controls [`src/pdfframe/mainwindow.py`]
      - `MainWindow._persistTrimPresetDocument(...)`: write current runtime config plus presets array [`src/pdfframe/mainwindow.py`]
        - `JsonConfigStore.save(...)`: persist normalized JSON config payload [`src/pdfframe/jsonconfig.py`]
    - `MainWindow.createSelectionGrid(...)`: optionally create startup grid from `--grid` [`src/pdfframe/mainwindow.py`]
      - `ViewerSelections.addSelection(...)`: create a selection item and set focus/current [`src/pdfframe/viewerselections.py`]
      - `ViewerSelectionItem.setBoundingRect(...)`: apply grid cell bounds to each selection [`src/pdfframe/viewerselections.py`]
        - `ViewerSelectionItem.adjustBoundingRect(...)`: clamp and normalize rectangle updates [`src/pdfframe/viewerselections.py`]
    - `MainWindow.slotPdfFrame(...)`: execute crop pipeline (scheduled by `--go` or invoked by UI action) [`src/pdfframe/mainwindow.py`]
      - `MainWindow.requestedUnsupportedGhostscriptOptions(...)`: return deterministic empty unsupported-option set after option removal [`src/pdfframe/mainwindow.py`]
      - `MainWindow.str2pages(...)`: parse optional `--whichpages` single-range forms (`N`, `N-`, `-N`, `N-M`) to zero-based page indices [`src/pdfframe/mainwindow.py`]
      - `MainWindow.createConversionProgressDialog(...)`: initialize modal progress window and stop button state [`src/pdfframe/mainwindow.py`]
      - `MainWindow.buildGhostscriptCropPlan(...)`: translate GUI selections to one Ghostscript command plan over the selected page range [`src/pdfframe/mainwindow.py`]
        - `MainWindow.primarySelectionCropValue(...)`: resolve first available normalized tuple from primary GUI selection [`src/pdfframe/mainwindow.py`]
        - `MainWindow.selectedConversionMode(...)`: map Mode controls to backend token (`frame` or `crop`) [`src/pdfframe/mainwindow.py`]
        - `AbstractViewerItem.cropValues(...)`: collect normalized crop regions for current page [`src/pdfframe/vieweritem.py`]
          - `ViewerSelections.cropValues(...)`: aggregate crop values from all selections [`src/pdfframe/viewerselections.py`]
            - `ViewerSelectionItem.cropValues(...)`: convert GUI corner geometry to normalized crop tuple(s) with deterministic ratio clamping [`src/pdfframe/viewerselections.py`]
              - `ViewerSelectionItem.distributeRect(...)`: split selection by device ratio when configured [`src/pdfframe/viewerselections.py`]
        - `AbstractViewerItem.pageGetSizePoints(...)`: expose page geometry for bbox conversion [`src/pdfframe/vieweritem.py`]
        - `normalized_crop_tuple_to_bbox(...)`: map one normalized GUI tuple to page-point CropBox corners (`LLx,LLy,URx,URy`) [`src/pdfframe/pdfframecmd.py`]
        - `build_ghostscript_page_crop_command(...)`: build script-style Ghostscript subprocess vector with `-dFirstPage/-dLastPage` for `frame`/`crop` modes [`src/pdfframe/pdfframecmd.py`]
      - `run_ghostscript_command(...)`: execute Ghostscript subprocess with optional shell-escaped command logging and optional captured-output console echo (enabled by verbose+debug), plus progress callback parsing, Qt event pumping, and cancellation polling [`src/pdfframe/pdfframecmd.py`]
        - `format_shell_command(...)`: render deterministic shell-escaped command diagnostics [`src/pdfframe/pdfframecmd.py`]
        - `extract_ghostscript_page_numbers(...)`: parse processed page numbers strictly from lines matching `^Page\\s+\\d+\\n` in captured output [`src/pdfframe/pdfframecmd.py`]
    - `MainWindow.slotTrimMarginsAll(...)`: trim currently visible selections on the active page [`src/pdfframe/mainwindow.py`]
      - `MainWindow.trimMarginsSelection(...)`: compute auto-trim rectangle using current page or all visible pages (per `checkTrimUseAllPages` checkbox) with color-sensitivity/grayscale-sensitivity parsed from Basic-tab trim controls, apply configured padding, and clamp the padded rectangle to page-image bounds (fallback to current selection bounds when page-image geometry is unavailable) [`src/pdfframe/mainwindow.py`]
        - `autoTrimMargins(...)`: derive trimmed rectangle from image luminance transitions and threshold parameters [`src/pdfframe/autotrim.py`]
      - `MainWindow.getPadding(...)`: parse CSS-like trim padding string into top/right/bottom/left numeric offsets [`src/pdfframe/mainwindow.py`]
- External Boundaries:
  - Qt framework event loop, signals/slots, widgets, scene rendering (`PyQt6`/`PyQt5`).
  - PDF metadata/render backends (`fitz`, `popplerqt5`) used for GUI page visualization and geometry.
  - Desktop/AppStream integration metadata (`com.ogekuri.pdfframe.desktop`, `com.ogekuri.pdfframe.metainfo.xml`) consumed by desktop environments.
  - Ghostscript executable subprocess boundary (`gs` with pdfwrite and BeginPage clipping commands).
  - User-home JSON configuration file boundary (`~/.pdfframe/config.json`) read/write through `JsonConfigStore`.
  - pypdf read/write boundary used to assemble output PDF from processed selected cropped pages.
  - OS filesystem reads/writes for input and output files.
  - OS signal integration (`signal.SIGINT` default handling).

### PROC:gha-check-branch

- Entrypoint(s):
  - `release-uvx.yml::jobs.check-branch` [` .github/workflows/release-uvx.yml`]
- Lifecycle/trigger:
  - Starts on GitHub-hosted Linux runner after tag push trigger `v<major>.<minor>.<patch>`.
  - Runs checkout + shell script that validates whether tag commit is contained in `origin/master`.
  - Stops after setting job output `is_master`.
  - Threads: no explicit thread creation detected in workflow definition.
- Internal Call-Trace Tree:
  - `check-branch(...)`: evaluate tag commit branch containment and emit `is_master` output [` .github/workflows/release-uvx.yml`]
- External Boundaries:
  - GitHub Actions runner provisioning and action execution (`actions/checkout@v4`).
  - Git CLI network/fetch interaction with remote origin.
  - GitHub Actions output channel `$GITHUB_OUTPUT`.

### PROC:gha-build-release

- Entrypoint(s):
  - `release-uvx.yml::jobs.build-release` [` .github/workflows/release-uvx.yml`]
- Lifecycle/trigger:
  - Starts only when `needs.check-branch.outputs.is_master == 'true'`.
  - Executes checkout, Python setup, uv setup, dependency install, build, provenance attestation, changelog generation, and release publication.
  - Stops after artifact upload/release creation.
  - Threads: no explicit thread creation detected in workflow definition.
- Internal Call-Trace Tree:
  - `build-release(...)`: orchestrate package build and GitHub release publication [` .github/workflows/release-uvx.yml`]
- External Boundaries:
  - GitHub Actions reusable actions (`actions/setup-python`, `astral-sh/setup-uv`, attestation/release actions).
  - Python package installation/build tooling (`uv pip`, `python -m build`).
  - GitHub release/changelog APIs via marketplace actions.

## Communication Edges

- ID: `EDGE-001`
  - source: `PROC:gha-check-branch`
  - destination: `PROC:gha-build-release`
  - direction: `check-branch -> build-release`
  - mechanism: `GitHub Actions job dependency output`
  - endpoint_channel: `needs.check-branch.outputs.is_master`
  - payload_data_shape: `string boolean token ("true" | "false")`
  - evidence:
    - `.github/workflows/release-uvx.yml`: `outputs.is_master` assigned from step `check`
    - `.github/workflows/release-uvx.yml`: `if: needs.check-branch.outputs.is_master == 'true'`

- ID: `EDGE-002`
  - source: `PROC:main`
  - destination: `PROC:main`
  - direction: `Qt event producer -> slot consumer (intra-process)`
  - mechanism: `Qt signal/slot dispatch inside main event loop`
  - endpoint_channel: `QAction.triggered / QWidget signals bound in MainWindow.__init__`
  - payload_data_shape: `Qt signal payloads (e.g., bool checked, text edits, trigger with no args)`
  - evidence:
    - `src/pdfframe/mainwindow.py`: multiple `.triggered.connect(...)`, `.toggled.connect(...)`, `.textEdited.connect(...)` bindings
