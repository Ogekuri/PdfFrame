## Execution Units Index

- ID: `PROC:main`
  - type: `process`
  - parent_process: `-`
  - role: `Desktop PDF crop runtime (interactive UI and --go batch trigger)`
  - entrypoint_symbols: `pdfframe.application.main`, `pdfframe.__main__.main`
  - defining_files:
    - `src/pdfframe/__main__.py`
    - `src/pdfframe/application.py`
    - `src/pdfframe/mainwindow.py`
    - `src/pdfframe/pdfframecmd.py`
    - `src/pdfframe/vieweritem.py`
    - `src/pdfframe/viewerselections.py`
    - `src/pdfframe/jsonconfig.py`
    - `src/pdfframe/autotrim.py`
- ID: `PROC:gha-check-branch`
  - type: `process`
  - parent_process: `-`
  - role: `GitHub Actions job that verifies tagged commit ancestry on origin/master`
  - entrypoint_symbols: `release-uvx.yml::jobs.check-branch`
  - defining_files:
    - `.github/workflows/release-uvx.yml`
- ID: `PROC:gha-build-release`
  - type: `process`
  - parent_process: `-`
  - role: `GitHub Actions job that builds distributions, attests provenance, and publishes release assets`
  - entrypoint_symbols: `release-uvx.yml::jobs.build-release`
  - defining_files:
    - `.github/workflows/release-uvx.yml`

## Execution Units

### PROC:main

- Entrypoint(s):
  - `pdfframe.application.main(...)` [`src/pdfframe/application.py`]
  - module guard `if __name__ == "__main__": main()` [`src/pdfframe/__main__.py`]
- Lifecycle/trigger:
  - Starts when `pdfframe` entrypoint is invoked.
  - Initializes `QApplication`, constructs `MainWindow`, applies CLI-derived startup state, then blocks in `app.exec()`.
  - In `--go` mode, schedules `window.slotPdfFrame` and `window.close` through `QTimer.singleShot(0, ...)`.
  - During conversion, iterates pages synchronously through PyMuPDF `fitz` API inside `crop_pdf_pages(...)`, pumping Qt events between pages via `event_pump` callback.
  - No explicit threads detected (single-threaded synchronous crop processing).
  - Stops when Qt event loop exits.
- Internal Call-Trace Tree:
  - `main(...)`: parse CLI options, configure runtime flags, construct UI, dispatch startup actions, and enter Qt loop [`src/pdfframe/application.py`]
    - `MainWindow.__init__(...)`: connect UI actions/signals, instantiate viewer scene, load persisted config [`src/pdfframe/mainwindow.py`]
      - `_setupConversionModeControls(...)`: initialize frame/crop mode controls [`src/pdfframe/mainwindow.py`]
      - `_setupTrimSettingsControls(...)`: bind trim-controls section and enablement logic [`src/pdfframe/mainwindow.py`]
      - `_setupTrimPresetControls(...)`: initialize preset list controls [`src/pdfframe/mainwindow.py`]
      - `_setupTrimPresetAction(...)`: wire Save Margins toolbar action ordering and handler [`src/pdfframe/mainwindow.py`]
      - `readSettings(...)`: load QSettings and JSON-backed runtime config [`src/pdfframe/mainwindow.py`]
        - `JsonConfigStore.load_or_initialize(...)`: load/create normalized `~/.pdfframe/config.json` document [`src/pdfframe/jsonconfig.py`]
          - `default_config_document(...)`: return default `{config, presets}` structure [`src/pdfframe/jsonconfig.py`]
          - `JsonConfigStore.save(...)`: persist normalized JSON configuration [`src/pdfframe/jsonconfig.py`]
    - `MainWindow.openFile(...)`: open source PDF, validate homogeneous page format, initialize output path, and enable/disable conversion actions [`src/pdfframe/mainwindow.py`]
      - `AbstractViewerItem.load(...)`: load viewer backend and reset caches/state [`src/pdfframe/vieweritem.py`]
        - `MuPDFViewerItem.doLoad(...)`: open document through PyMuPDF backend [`src/pdfframe/vieweritem.py`]
        - `PopplerViewerItem.doLoad(...)`: open document through Poppler backend [`src/pdfframe/vieweritem.py`]
      - `MainWindow._hasCompatiblePageFormat(...)`: compare page-1 dimensions/orientation with all later pages [`src/pdfframe/mainwindow.py`]
      - `MainWindow.showWarning(...)`: display modal incompatibility warning before clearing loaded state [`src/pdfframe/mainwindow.py`]
    - `MainWindow.slotPdfFrame(...)`: build crop plan, open progress dialog, execute PyMuPDF crop, and handle error/cancel paths [`src/pdfframe/mainwindow.py`]
      - `MainWindow.str2pages(...)`: parse single-range `--whichpages` formats [`src/pdfframe/mainwindow.py`]
      - `MainWindow.buildCropPlan(...)`: derive crop parameters for selected range and propagate Delete annotations field toggle [`src/pdfframe/mainwindow.py`]
        - `MainWindow.primarySelectionCropValue(...)`: resolve primary normalized crop tuple [`src/pdfframe/mainwindow.py`]
          - `AbstractViewerItem.cropValues(...)`: fetch normalized crop tuples for page index [`src/pdfframe/vieweritem.py`]
            - `ViewerSelections.cropValues(...)`: aggregate single-selection crop tuples [`src/pdfframe/viewerselections.py`]
              - `ViewerSelectionItem.cropValues(...)`: compute normalized tuple from graphics bounds [`src/pdfframe/viewerselections.py`]
        - `MainWindow.selectedConversionMode(...)`: map UI state to `frame|crop` token [`src/pdfframe/mainwindow.py`]
        - `AbstractViewerItem.pageGetSizePoints(...)`: return source page dimensions in points [`src/pdfframe/vieweritem.py`]
        - `normalized_crop_tuple_to_bbox(...)`: convert normalized tuple to PDF bbox points [`src/pdfframe/pdfframecmd.py`]
      - `MainWindow.createConversionProgressDialog(...)`: construct modal progress UI with cancellation [`src/pdfframe/mainwindow.py`]
      - `crop_pdf_pages(...)`: iterate pages through PyMuPDF fitz API, physically remove content outside selection via redaction, apply frame-mode CropBox or crop-mode CropBox/MediaBox, delete annotations via API and xref cleanup, report per-page progress via callback, pump UI events before save [`src/pdfframe/pdfframecmd.py`]
        - `_redact_outside_selection(...)`: add redaction annotations for page areas outside selection boundary and apply redactions to physically remove text, images, and line art [`src/pdfframe/pdfframecmd.py`]
    - `MainWindow.slotTrimMarginsAll(...)`: auto-trim current selection [`src/pdfframe/mainwindow.py`]
      - `MainWindow.trimMarginsSelection(...)`: compute trim rectangle using thresholds/range/padding [`src/pdfframe/mainwindow.py`]
        - `autoTrimMargins(...)`: detect content bounds from image data [`src/pdfframe/autotrim.py`]
- External Boundaries:
  - Qt framework event loop, widgets, and signal/slot runtime (`PyQt6`/`PyQt5`).
  - PyMuPDF `fitz` API for page manipulation, annotation deletion, and PDF save.
  - OS filesystem I/O for input PDFs, output PDFs, and user config path (`~/.pdfframe/config.json`).
  - Rendering backends (`fitz`, `popplerqt5`) for page rasterization/geometry.
  - OS signal handling (`signal.SIGINT`).

### PROC:gha-check-branch

- Entrypoint(s):
  - `release-uvx.yml::jobs.check-branch` [`.github/workflows/release-uvx.yml`]
- Lifecycle/trigger:
  - Starts on tag push matching `v<major>.<minor>.<patch>`.
  - Executes checkout, fetches `origin/master`, checks if `${GITHUB_SHA}` is contained in remote master.
  - Writes `is_master=true|false` to `$GITHUB_OUTPUT` and exits.
  - Threads: no explicit threads detected in workflow definition.
- Internal Call-Trace Tree:
  - `check-branch(...)`: run shell script to compute `is_master` output [`.github/workflows/release-uvx.yml`]
- External Boundaries:
  - GitHub Actions runner and marketplace actions.
  - Git CLI/network access to origin.
  - GitHub Actions output channel `$GITHUB_OUTPUT`.

### PROC:gha-build-release

- Entrypoint(s):
  - `release-uvx.yml::jobs.build-release` [`.github/workflows/release-uvx.yml`]
- Lifecycle/trigger:
  - Starts only when `needs.check-branch.outputs.is_master == 'true'`.
  - Runs checkout, Python/uv setup, dependency install, build, attestation, changelog build, and release publish.
  - Stops after artifacts are uploaded/release step completes.
  - Threads: no explicit threads detected in workflow definition.
- Internal Call-Trace Tree:
  - `build-release(...)`: orchestrate release build and publication steps [`.github/workflows/release-uvx.yml`]
- External Boundaries:
  - GitHub Actions reusable actions and hosted runner services.
  - Python build tooling (`uv`, `python -m build`).
  - GitHub Releases/Attestations APIs.

## Communication Edges

- ID: `EDGE-001`
  - source: `PROC:gha-check-branch`
  - destination: `PROC:gha-build-release`
  - direction: `PROC:gha-check-branch -> PROC:gha-build-release`
  - mechanism: `GitHub Actions job output dependency`
  - endpoint_channel: `needs.check-branch.outputs.is_master`
  - payload_data_shape: `string enum {"true","false"}`
  - evidence:
    - `.github/workflows/release-uvx.yml`: `outputs.is_master` mapped from step `check`
    - `.github/workflows/release-uvx.yml`: `if: needs.check-branch.outputs.is_master == 'true'`

- ID: `EDGE-002`
  - source: `PROC:main`
  - destination: `PROC:main`
  - direction: `Qt event producer -> Qt slot consumer (intra-process)`
  - mechanism: `Qt signal/slot dispatch`
  - endpoint_channel: `QAction.triggered / QWidget edited/toggled signals`
  - payload_data_shape: `Qt signal payloads (bool, str, no-arg trigger)`
  - evidence:
    - `src/pdfframe/mainwindow.py`: multiple `.triggered.connect(...)`, `.toggled.connect(...)`, `.textEdited.connect(...)`

- ID: `EDGE-003`
  - source: `PROC:main`
  - destination: `PROC:main`
  - direction: `MainWindow.slotPdfFrame -> crop_pdf_pages (intra-process synchronous call)`
  - mechanism: `direct function call with callback-based progress`
  - endpoint_channel: `progress_callback(page_number, processed_count, total)`, `cancel_requested()`, `event_pump()`
  - payload_data_shape: `callback signatures: Callable[[int, int, int], None], Callable[[], bool], Callable[[], None]`
  - evidence:
    - `src/pdfframe/mainwindow.py`: `crop_pdf_pages(...)` called with progress_callback, cancel_requested, event_pump lambdas
    - `src/pdfframe/pdfframecmd.py`: `crop_pdf_pages(...)` invokes `progress_callback(...)` per page, checks `cancel_requested()`, calls `event_pump()`
