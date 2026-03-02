# Files Structure
```
.
└── src
    └── pdfframe
        ├── __init__.py
        ├── __main__.py
        ├── application.py
        ├── autotrim.py
        ├── config.py
        ├── jsonconfig.py
        ├── mainwindow.py
        ├── mainwindowui_qt5.py
        ├── mainwindowui_qt6.py
        ├── pdfframecmd.py
        ├── pdfframeper.py
        ├── qt.py
        ├── version.py
        ├── vieweritem.py
        └── viewerselections.py
```

# __init__.py | Python | 0L | 0 symbols | 0 imports | 0 comments
> Path: `src/pdfframe/__init__.py`


---

# __main__.py | Python | 4L | 0 symbols | 1 imports | 0 comments
> Path: `src/pdfframe/__main__.py`

## Imports
```
from pdfframe.application import main
```


---

# application.py | Python | 95L | 1 symbols | 7 imports | 7 comments
> Path: `src/pdfframe/application.py`
- @brief CLI entrypoint for pdfframe GUI and one-shot conversion.
- @details Parses command-line arguments, applies startup options on MainWindow, and launches Qt event loop.
Copyright (C) 2010-2025 Ogekuri.
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

## Imports
```
import sys
from pdfframe.version import __version__
from argparse import ArgumentParser, RawTextHelpFormatter
from pdfframe.qt import QApplication
from pdfframe.mainwindow import MainWindow
import signal
from pdfframe.qt import QTimer
```

## Definitions

### fn `def main()` (L20-95)

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`main`|fn|pub|20-95|def main()|


---

# autotrim.py | Python | 73L | 3 symbols | 1 imports | 7 comments
> Path: `src/pdfframe/autotrim.py`
- @brief Margin auto-trimming helpers for selection rectangles.
- @details Performs grayscale transition scanning to shrink candidate rectangles while preserving content bounds.
Copyright (C) 2010-2020 ogekuri.
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

## Imports
```
from pdfframe.qt import *
```

## Definitions

### fn `def autoTrimMargins(img, r, minr, sensitivity, grayscale_sensitivity)` (L19-73)
- @brief Auto-trims margins of a rectangle using grayscale-transition thresholds.
- @details Scans rectangle border lines and trims sides while per-line grayscale transitions remain within configured sensitivity and grayscale-sensitivity.
- @param img {QImage} Page image used for grayscale sampling.
- @param r {QRect} Candidate rectangle to trim.
- @param minr {QRect|None} Optional minimum rectangle that limits trimming.
- @param sensitivity {float} Minimum pixel delta counted as a transition.
- @param grayscale_sensitivity {float} Maximum accepted transition count per scan line.
- @return {QRect} Trimmed rectangle clamped to image bounds.

### fn `def pixAt(x, y)` (L32-34)
- @brief Auto-trims margins of a rectangle using grayscale-transition thresholds.
- @details Scans rectangle border lines and trims sides while per-line grayscale
transitions remain within configured sensitivity and grayscale-sensitivity.
- @param img {QImage} Page image used for grayscale sampling.
- @param r {QRect} Candidate rectangle to trim.
- @param minr {QRect|None} Optional minimum rectangle that limits trimming.
- @param sensitivity {float} Minimum pixel delta counted as a transition.
- @param grayscale_sensitivity {float} Maximum accepted transition count per scan line.
- @return {QRect} Trimmed rectangle clamped to image bounds.

### fn `def isTrimmable(L)` (L35-47)

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`autoTrimMargins`|fn|pub|19-73|def autoTrimMargins(img, r, minr, sensitivity, grayscale_...|
|`pixAt`|fn|pub|32-34|def pixAt(x, y)|
|`isTrimmable`|fn|pub|35-47|def isTrimmable(L)|


---

# config.py | Python | 17L | 2 symbols | 2 imports | 2 comments
> Path: `src/pdfframe/config.py`
- @brief Runtime backend-selection flags for pdfframe.
- @details Detects which Qt binding is available and exposes the `PYQT6` switch consumed by UI modules.

## Imports
```
import importlib.util
import sys
```

## Definitions

- var `PYQT6 = False` (L11)
- var `PYQT6 = True` (L14)
## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`PYQT6`|var|pub|11||
|`PYQT6`|var|pub|14||


---

# jsonconfig.py | Python | 113L | 8 symbols | 3 imports | 9 comments
> Path: `src/pdfframe/jsonconfig.py`

## Imports
```
import json
from copy import deepcopy
from pathlib import Path
```

## Definitions

- var `DEFAULT_CONFIG_VALUES = {` (L12)
### fn `def default_config_path()` (L23-31)
- @brief Returns canonical user JSON configuration path.
- @details Resolves `~/.pdfframe/config.json` using current user home directory.
- @return {pathlib.Path} Expanded configuration file path.

### fn `def default_config_document()` (L32-40)
- @brief Returns default JSON configuration document.
- @details Includes top-level `config` object seeded from `DEFAULT_CONFIG_VALUES` and empty `presets` array.
- @return {dict[str,object]} Default config document payload.

### class `class JsonConfigStore` (L41-113)
- @brief Provides normalized JSON config read/write operations.
- @details Enforces top-level `config` and `presets` sections and guarantees default keys for config values.
- fn `def __init__(self, path=None)` `priv` (L47-54)
  - @brief Provides normalized JSON config read/write operations.
  - @brief Initializes JSON config store.
  - @details Enforces top-level `config` and `presets` sections and guarantees default keys for config values.
  - @details Uses explicit path when provided; otherwise defaults to `~/.pdfframe/config.json`.
  - @param path {str|pathlib.Path|None} Optional configuration path override.
- fn `def _normalize_document(self, document)` `priv` (L55-79)
  - @brief Normalizes JSON config document shape.
  - @details Validates root object and top-level section types, merges missing default config keys, and guarantees list type for presets.
  - @param document {dict[str,object]} Raw decoded JSON payload.
  - @return {dict[str,object]} Normalized document.
  - @throws {ValueError} If root or required sections have incompatible types.
- fn `def load_or_initialize(self)` (L80-99)
  - @brief Loads JSON configuration and creates defaults when missing.
  - @details Creates `~/.pdfframe/config.json` when absent, normalizes loaded documents, and writes back normalization deltas.
  - @return {dict[str,object]} Normalized configuration document.
  - @throws {OSError} If filesystem operations fail.
  - @throws {ValueError} If existing JSON document has invalid structure.
  - @throws {json.JSONDecodeError} If existing JSON file is syntactically invalid.
- fn `def save(self, document)` (L100-113)
  - @brief Writes normalized JSON configuration to disk.
  - @details Validates/normalizes payload, ensures parent directory exists, and serializes with deterministic indentation.
  - @param document {dict[str,object]} Document payload to persist.
  - @return {None} Performs filesystem writes.
  - @throws {OSError} If write operation fails.
  - @throws {ValueError} If payload has invalid structure.

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`DEFAULT_CONFIG_VALUES`|var|pub|12||
|`default_config_path`|fn|pub|23-31|def default_config_path()|
|`default_config_document`|fn|pub|32-40|def default_config_document()|
|`JsonConfigStore`|class|pub|41-113|class JsonConfigStore|
|`JsonConfigStore.__init__`|fn|priv|47-54|def __init__(self, path=None)|
|`JsonConfigStore._normalize_document`|fn|priv|55-79|def _normalize_document(self, document)|
|`JsonConfigStore.load_or_initialize`|fn|pub|80-99|def load_or_initialize(self)|
|`JsonConfigStore.save`|fn|pub|100-113|def save(self, document)|


---

# mainwindow.py | Python | 1390L | 89 symbols | 14 imports | 69 comments
> Path: `src/pdfframe/mainwindow.py`
- @brief Main Qt window and interactive workflow for pdfframe.
- @details Hosts viewer interactions, selection editing, settings persistence, and conversion orchestration.
Copyright (C) 2010-2025 Ogekuri.
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

## Imports
```
import sys
import re
from datetime import datetime
from pathlib import Path
from os.path import splitext
from pdfframe.qt import *
from pdfframe.config import PYQT6
from pdfframe.jsonconfig import DEFAULT_CONFIG_VALUES, JsonConfigStore
from pdfframe.mainwindowui_qt6 import Ui_MainWindow
from pdfframe.mainwindowui_qt5 import Ui_MainWindow
from pdfframe.viewerselections import ViewerSelections, aspectRatioFromStr
from pdfframe.vieweritem import ViewerItem
from pdfframe.pdfframecmd import (
from pdfframe.autotrim import autoTrimMargins
```

## Definitions

### class `class AspectRatioType` (L42-47)
- fn `def __init__(self, name, width, height)` `priv` (L43-47)

### class `class AspectRatioTypeManager` (L48-100)
- fn `def __init__(self)` `priv` (L50-53)
- fn `def __iter__(self)` `priv` (L54-56)
- fn `def addType(self, name, width, height)` (L57-59)
- fn `def getType(self, index)` (L60-64)
- fn `def addDefaults(self)` (L65-67)
- fn `def settingsCaption(self)` (L68-70)
- fn `def saveTypes(self, settings)` (L71-87)
- fn `def loadTypes(self, settings)` (L88-100)

### class `class SelAspectRatioTypeManager(AspectRatioTypeManager)` : AspectRatioTypeManager (L101-114)
- fn `def settingsCaption(self)` (L103-105)
- fn `def addDefaults(self)` (L106-114)

### class `class DeviceTypeManager(AspectRatioTypeManager)` : AspectRatioTypeManager (L115-127)
- fn `def settingsCaption(self)` (L117-119)
- fn `def addDefaults(self)` (L120-127)

### class `class MainWindow(QMainWindow)` : QMainWindow (L128-327)
- fn `def __init__(self)` `priv` (L132-246)
- fn `def viewer(self)` (L248-250)
- fn `def selections(self)` (L252-254)
- fn `def _toolbarIconFromAsset(self, filename, fallbackTheme)` `priv` (L255-267)
  - @brief Resolves toolbar icon from bundled asset with fallback theme icon.
  - @details Loads icon from `src/pdfframe/icons/<filename>` when available; otherwise returns `QIcon.fromTheme(<fallbackTheme>)`.
  - @param filename {str} Bundled icon filename.
  - @param fallbackTheme {str} Freedesktop theme-icon token.
  - @return {QIcon} Toolbar icon object.
- fn `def _setupConversionModeControls(self)` `priv` (L268-285)
  - @brief Adds conversion mode controls to the basic tab.
  - @details Creates `Mode` group with `Frame` and `Crop` radio buttons, defaults to `Frame`, and inserts it into the basic-tab layout.
  - @return {None} Applies UI side effects.
- fn `def _setupTrimSettingsControls(self)` `priv` (L286-296)
  - @brief Relocates trim configuration controls into the Basic tab.
  - @details Reuses the existing trim-settings group from the advanced UI definition, moves it to the bottom of the basic layout with all controls visible.
  - @return {None} Applies UI side effects.

### fn `def _setupTrimPresetControls(self)` `priv` (L297-333)
- @brief Adds dedicated Basic-tab trim preset controls.
- @details Creates a standalone `Presets` group placed immediately after `Trim settings`, configures stretch/fixed columns so preset names fill row width up to the right-edge remove button, and wires apply/rename/delete flows.
- @return {None} Applies UI side effects.

### fn `def _setupTrimPresetAction(self)` `priv` (L334-355)
- @brief Adds the `Save Margins` toolbar action next to trim action.
- @details Inserts a dedicated action directly to the right of `Trim Margins`, applies the dedicated `Save Margins` icon, then moves `Go!` to the far-right position immediately after `Save Margins`, and keeps preset-save action disabled until a PDF is loaded.
- @return {None} Applies UI side effects.

### fn `def _trimPresetEditableFlag(self)` `priv` (L356-360)

### fn `def _trimPresetRole(self)` `priv` (L361-365)

### fn `def _defaultTrimPresetName(self)` `priv` (L366-373)
- @brief Returns default trim preset name.
- @details Generates timestamp name in `%Y/%m/%d %H:%M:%S` format.
- @return {str} Default preset display label.

### fn `def _toBool(self, value)` `priv` (L374-384)
- @brief Normalizes persisted boolean-like values.
- @details Accepts bools and common string tokens produced by historical settings writers.
- @param value {object} Input value from settings/config source.
- @return {bool} Parsed boolean result.

### fn `def _updateTrimPagesRangeControls(self, enabled)` `priv` (L385-395)
- @brief Updates `Pages range` control enabled state.
- @details Enables range input only when trim-range mode is active and ensures default text `1-1` when empty.
- @param enabled {bool} State propagated from trim-range toggle.
- @return {None} Applies UI side effects.

### fn `def _parseTrimPagesRange(self)` `priv` (L396-412)
- @brief Parses and validates the trim pages range expression.
- @details Accepts only `N-M` one-based inclusive format, validates positive ordered bounds, and converts to zero-based bounds.
- @return {tuple[int,int]} `(start_index, end_index)` inclusive zero-based page bounds.
- @throws {ValueError} If the range is missing or syntactically/semantically invalid.

### fn `def _collectRuntimeConfigValues(self)` `priv` (L413-428)
- @brief Collects runtime config values mapped to JSON `config` keys.
- @details Converts current UI control state into serializable values for `~/.pdfframe/config.json`.
- @return {dict[str,object]} Persistable runtime config key/value mapping.

### fn `def _deleteAnnotsEnabled(self)` `priv` (L429-443)
- @brief Returns Delete annotations fields option state.
- @details Reads `checkDeleteAnnotsFields` when available and normalizes truthy values for compatibility with test stubs.
- @return {bool} True when annotations must be deleted from output PDF.

### fn `def _trimPresetFromCurrentSelection(self)` `priv` (L444-463)
- @brief Creates a trim preset payload from current UI state.
- @details Captures mode and trim parameters plus the primary current-page crop tuple when available.
- @return {dict[str,object]} New preset payload ready for persistence.

### fn `def _refreshTrimPresetList(self)` `priv` (L464-492)
- @brief Rebuilds trim preset tree rows from in-memory presets.
- @details Clears the list, creates editable name rows, and attaches one remove button per row mapped to preset index inside a right-aligned cell container.
- @return {None} Applies UI side effects.

### fn `def _persistTrimPresetDocument(self)` `priv` (L493-510)
- @brief Persists runtime config and preset list to JSON config file.
- @details Writes both `config` values and `presets` array through JsonConfigStore, surfacing warning on I/O failures.
- @return {None} Writes `~/.pdfframe/config.json`.

### fn `def _applyCropPreset(self, crop_values)` `priv` (L511-542)
- @brief Applies normalized crop tuple to current selection.
- @details Maps `[left,top,right,bottom]` normalized margins to viewer coordinates and updates (or creates) the current selection.
- @param crop_values {list[float]} Normalized crop tuple values.
- @return {None} Mutates current selection geometry.

### fn `def _applyTrimPreset(self, index)` `priv` (L543-568)
- @brief Applies one stored preset to current runtime controls.
- @details Restores mode and trim values, then applies saved crop tuple when present.
- @param index {int} Preset list index.
- @return {None} Applies UI and selection updates.

### fn `def slotTrimPresetClicked(self, item, column)` (L569-581)
- @brief Applies a preset when the preset name cell is clicked.
- @details Ignores delete-button column and list rebuild events.
- @param item {QTreeWidgetItem} Clicked row item.
- @param column {int} Clicked column index.
- @return {None} Applies preset side effects.

### fn `def slotTrimPresetDoubleClicked(self, item, column)` (L582-592)
- @brief Starts inline rename for preset names.
- @details Enables user-driven preset rename on double-click of first column.
- @param item {QTreeWidgetItem} Double-clicked row item.
- @param column {int} Double-clicked column index.
- @return {None} Opens in-place editor.

### fn `def slotTrimPresetChanged(self, item, column)` (L593-616)
- @brief Persists preset rename changes from inline editing.
- @details Normalizes empty labels to timestamp defaults and rewrites JSON config after updates.
- @param item {QTreeWidgetItem} Changed row item.
- @param column {int} Changed column index.
- @return {None} Persists preset list updates.

### fn `def slotDeleteTrimPreset(self)` (L617-635)
- @brief Deletes one preset from remove-button click.
- @details Resolves row index from sender button metadata, updates in-memory list, refreshes UI, and persists JSON state.
- @return {None} Applies preset delete side effects.

### fn `def slotSaveMarginsPreset(self)` (L636-647)
- @brief Saves current crop/trim state as a new preset.
- @details Captures active control values, appends new preset with timestamp default name, refreshes list, and persists JSON state.
- @return {None} Applies preset creation side effects.

### fn `def selectedConversionMode(self)` (L648-655)
- @brief Returns selected conversion mode for PDF crop execution.
- @details Maps GUI mode controls to backend mode tokens expected by crop processing.
- @return {str} Conversion mode token (`frame` or `crop`).

### fn `def currentSelectionUpdated(self)` (L656-672)

### fn `def _updateSelectionCreationActions(self)` `priv` (L673-682)
- @brief Updates enablement of selection-creation actions.
- @details Allows creating a selection only when the viewer has a document and no selection exists; keeps creation actions disabled once one selection area is present.
- @return {None} Applies action-enable side effects.

### fn `def readSettings(self)` (L683-731)
- @brief Reads persisted runtime settings from QSettings and JSON config.
- @details Restores window geometry from QSettings, loads trim/runtime defaults from `~/.pdfframe/config.json`, and refreshes preset UI entries.
- @return {None} Applies UI state restoration side effects.

### fn `def writeSettings(self)` (L732-756)
- @brief Persists runtime settings to legacy and JSON backends.
- @details Writes window/session metadata to QSettings and writes trim/runtime config plus presets to `~/.pdfframe/config.json`.
- @return {None} Persists runtime state.

### fn `def _hasCompatiblePageFormat(self)` `priv` (L757-778)
- @brief Validates homogeneous page format against page 1.
- @details Compares each page from index 1 onward with page-1 width/height values and orientation (portrait/landscape) using point units from `pageGetSizePoints`.
- @return {bool} True when every page is compatible with page 1; otherwise False.

### fn `def openFile(self, fileName)` (L779-810)

### fn `def slotOpenFile(self)` (L811-816)

### fn `def slotSelectFile(self)` (L817-826)

### fn `def showWarning(self, title, text)` (L827-834)

### fn `def str2pages(self, s)` (L835-852)

### fn `def primarySelectionCropValue(self, page_indexes)` (L853-866)
- @brief Gets primary selection crop tuple for conversion planning.
- @details Resolves first available normalized crop tuple from current page first, then requested pages, and returns only the primary tuple used for all output pages.
- @param page_indexes {list[int]} Ordered page indexes selected for processing.
- @return {tuple[float,float,float,float]|None} Primary normalized crop tuple or None when no selections are available.

### fn `def buildCropPlan(self, inputFileName, outputFileName, requestedPageIndexes=None)` (L867-903)
- @brief Builds PyMuPDF crop plan from GUI-derived parameters.
- @details Iterates only requested pages (or all pages when omitted), derives geometry from the primary GUI selection tuple, computes crop bbox from page-size metadata, and returns a plan dict with crop parameters for PyMuPDF page processing.
- @param inputFileName {str} Source PDF path.
- @param outputFileName {str} Destination cropped PDF path.
- @param requestedPageIndexes {set[int]|None} Optional zero-based page-index filter derived from `--whichpages`.
- @return {dict[str,object]|None} Crop plan containing page indexes, crop box, page dimensions, mode, and delete_annots flag.

### fn `def createConversionProgressDialog(self, totalPages)` (L904-926)
- @brief Creates modal conversion progress dialog for crop execution.
- @details Configures progress dialog with deterministic page range and cancellable stop action used during long-running conversion command execution.
- @param totalPages {int} Number of selected pages to process.
- @return {QProgressDialog} Configured progress dialog instance.

### fn `def slotPdfFrame(self)` (L927-1028)
- @brief Executes PDF crop action using PyMuPDF crop backend.
- @details Builds a crop plan from GUI state and processes pages iteratively through PyMuPDF fitz API with per-page progress callback.
- @return {None} Triggers output PDF generation side effect.

### fn `def on_page_progress(original_page_number, processed_count, total)` (L971-987)
- @brief Executes PDF crop action using PyMuPDF crop backend.
- @brief Per-page progress callback for PyMuPDF crop processing.
- @details Builds a crop plan from GUI state and processes pages
iteratively through PyMuPDF fitz API with per-page progress callback.
- @details Updates dialog value and label for each processed page.
- @param original_page_number {int} One-based original page number.
- @param processed_count {int} Number of pages processed so far.
- @param total {int} Total pages to process.
- @return {None} Triggers output PDF generation side effect.
- @return {None} Applies progress side effects.

### fn `def slotZoomIn(self)` (L1029-1032)

### fn `def slotZoomOut(self)` (L1033-1036)

### fn `def slotFitInView(self, checked)` (L1037-1041)

### fn `def slotSplitterMoved(self, pos, idx)` (L1042-1044)

### fn `def slotPreviousPage(self)` (L1045-1048)

### fn `def slotNextPage(self)` (L1049-1052)

### fn `def slotFirstPage(self)` (L1053-1056)

### fn `def slotLastPage(self)` (L1057-1060)

### fn `def slotCurrentPageEdited(self, text)` (L1061-1068)

### fn `def updateControls(self)` (L1069-1077)

### fn `def slotSelectionMode(self, checked)` (L1078-1081)

### fn `def slotSelExceptionsChanged(self)` (L1082-1084)

### fn `def slotSelExceptionsEdited(self, text)` (L1085-1089)

### fn `def slotSelAspectRatioChanged(self)` (L1090-1098)

### fn `def slotSelAspectRatioTypeChanged(self, index)` (L1099-1118)

### fn `def distributeAspectRatioChanged(self, aspectRatio)` (L1119-1121)

### fn `def slotDistributeAspectRatioChanged(self)` (L1122-1124)

### fn `def slotDeviceTypeChanged(self, index)` (L1125-1131)

### fn `def slotContextMenu(self, pos)` (L1132-1152)

### fn `def slotDeleteSelection(self)` (L1153-1156)

### fn `def slotNewSelection(self)` (L1157-1159)

### fn `def slotNewSelectionGrid(self)` (L1160-1178)
- @brief Requests one new trim/selection area from user grid input.
- @details Prompts only when no selection area exists; in single-selection mode the request is rejected while an area is already present.
- @return {None} Applies selection-creation side effects.

### fn `def createSelectionGrid(self, grid)` (L1179-1235)
- @brief Creates the initial trim/selection area from grid input.
- @details Parses `grid` input, enforces single-selection mode by reducing multi-cell requests to one area, and prevents creation when an area already exists.
- @param grid {str} Grid expression entered by CLI or UI.
- @return {None} Applies selection-creation side effects.

### fn `def getPadding(self)` (L1236-1263)
- @brief Returns trim padding in CSS-expanded order.
- @details Reads trim padding text from the dedicated Basic-tab controls and expands one-to-four comma-separated values to `[top,right,bottom,left]`.
- @return {list[float]} Padding tuple in top,right,bottom,left order.

### fn `def slotTrimMarginsAll(self)` (L1264-1276)

### fn `def slotTrimMargins(self)` (L1277-1281)

### fn `def trimMarginsSelection(self, sel)` (L1282-1385)
- @brief Computes auto-trim rectangle for a selection using configured thresholds.
- @details Reads color-sensitivity and grayscale-sensitivity values from Basic-tab controls, selects page scope using current page by default or a validated `Pages range` slice of visible pages when range mode is enabled, and applies auto-trim with padding and aspect-ratio adjustments.
- @param sel {ViewerSelectionItem} Selection item to trim.
- @return {None} Mutates selection bounding rectangle.

### fn `def resizeEvent(self, event)` (L1386-1388)

### fn `def closeEvent(self, event)` (L1389-1390)

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`AspectRatioType`|class|pub|42-47|class AspectRatioType|
|`AspectRatioType.__init__`|fn|priv|43-47|def __init__(self, name, width, height)|
|`AspectRatioTypeManager`|class|pub|48-100|class AspectRatioTypeManager|
|`AspectRatioTypeManager.__init__`|fn|priv|50-53|def __init__(self)|
|`AspectRatioTypeManager.__iter__`|fn|priv|54-56|def __iter__(self)|
|`AspectRatioTypeManager.addType`|fn|pub|57-59|def addType(self, name, width, height)|
|`AspectRatioTypeManager.getType`|fn|pub|60-64|def getType(self, index)|
|`AspectRatioTypeManager.addDefaults`|fn|pub|65-67|def addDefaults(self)|
|`AspectRatioTypeManager.settingsCaption`|fn|pub|68-70|def settingsCaption(self)|
|`AspectRatioTypeManager.saveTypes`|fn|pub|71-87|def saveTypes(self, settings)|
|`AspectRatioTypeManager.loadTypes`|fn|pub|88-100|def loadTypes(self, settings)|
|`SelAspectRatioTypeManager`|class|pub|101-114|class SelAspectRatioTypeManager(AspectRatioTypeManager)|
|`SelAspectRatioTypeManager.settingsCaption`|fn|pub|103-105|def settingsCaption(self)|
|`SelAspectRatioTypeManager.addDefaults`|fn|pub|106-114|def addDefaults(self)|
|`DeviceTypeManager`|class|pub|115-127|class DeviceTypeManager(AspectRatioTypeManager)|
|`DeviceTypeManager.settingsCaption`|fn|pub|117-119|def settingsCaption(self)|
|`DeviceTypeManager.addDefaults`|fn|pub|120-127|def addDefaults(self)|
|`MainWindow`|class|pub|128-327|class MainWindow(QMainWindow)|
|`MainWindow.__init__`|fn|priv|132-246|def __init__(self)|
|`MainWindow.viewer`|fn|pub|248-250|def viewer(self)|
|`MainWindow.selections`|fn|pub|252-254|def selections(self)|
|`MainWindow._toolbarIconFromAsset`|fn|priv|255-267|def _toolbarIconFromAsset(self, filename, fallbackTheme)|
|`MainWindow._setupConversionModeControls`|fn|priv|268-285|def _setupConversionModeControls(self)|
|`MainWindow._setupTrimSettingsControls`|fn|priv|286-296|def _setupTrimSettingsControls(self)|
|`_setupTrimPresetControls`|fn|priv|297-333|def _setupTrimPresetControls(self)|
|`_setupTrimPresetAction`|fn|priv|334-355|def _setupTrimPresetAction(self)|
|`_trimPresetEditableFlag`|fn|priv|356-360|def _trimPresetEditableFlag(self)|
|`_trimPresetRole`|fn|priv|361-365|def _trimPresetRole(self)|
|`_defaultTrimPresetName`|fn|priv|366-373|def _defaultTrimPresetName(self)|
|`_toBool`|fn|priv|374-384|def _toBool(self, value)|
|`_updateTrimPagesRangeControls`|fn|priv|385-395|def _updateTrimPagesRangeControls(self, enabled)|
|`_parseTrimPagesRange`|fn|priv|396-412|def _parseTrimPagesRange(self)|
|`_collectRuntimeConfigValues`|fn|priv|413-428|def _collectRuntimeConfigValues(self)|
|`_deleteAnnotsEnabled`|fn|priv|429-443|def _deleteAnnotsEnabled(self)|
|`_trimPresetFromCurrentSelection`|fn|priv|444-463|def _trimPresetFromCurrentSelection(self)|
|`_refreshTrimPresetList`|fn|priv|464-492|def _refreshTrimPresetList(self)|
|`_persistTrimPresetDocument`|fn|priv|493-510|def _persistTrimPresetDocument(self)|
|`_applyCropPreset`|fn|priv|511-542|def _applyCropPreset(self, crop_values)|
|`_applyTrimPreset`|fn|priv|543-568|def _applyTrimPreset(self, index)|
|`slotTrimPresetClicked`|fn|pub|569-581|def slotTrimPresetClicked(self, item, column)|
|`slotTrimPresetDoubleClicked`|fn|pub|582-592|def slotTrimPresetDoubleClicked(self, item, column)|
|`slotTrimPresetChanged`|fn|pub|593-616|def slotTrimPresetChanged(self, item, column)|
|`slotDeleteTrimPreset`|fn|pub|617-635|def slotDeleteTrimPreset(self)|
|`slotSaveMarginsPreset`|fn|pub|636-647|def slotSaveMarginsPreset(self)|
|`selectedConversionMode`|fn|pub|648-655|def selectedConversionMode(self)|
|`currentSelectionUpdated`|fn|pub|656-672|def currentSelectionUpdated(self)|
|`_updateSelectionCreationActions`|fn|priv|673-682|def _updateSelectionCreationActions(self)|
|`readSettings`|fn|pub|683-731|def readSettings(self)|
|`writeSettings`|fn|pub|732-756|def writeSettings(self)|
|`_hasCompatiblePageFormat`|fn|priv|757-778|def _hasCompatiblePageFormat(self)|
|`openFile`|fn|pub|779-810|def openFile(self, fileName)|
|`slotOpenFile`|fn|pub|811-816|def slotOpenFile(self)|
|`slotSelectFile`|fn|pub|817-826|def slotSelectFile(self)|
|`showWarning`|fn|pub|827-834|def showWarning(self, title, text)|
|`str2pages`|fn|pub|835-852|def str2pages(self, s)|
|`primarySelectionCropValue`|fn|pub|853-866|def primarySelectionCropValue(self, page_indexes)|
|`buildCropPlan`|fn|pub|867-903|def buildCropPlan(self, inputFileName, outputFileName, re...|
|`createConversionProgressDialog`|fn|pub|904-926|def createConversionProgressDialog(self, totalPages)|
|`slotPdfFrame`|fn|pub|927-1028|def slotPdfFrame(self)|
|`on_page_progress`|fn|pub|971-987|def on_page_progress(original_page_number, processed_coun...|
|`slotZoomIn`|fn|pub|1029-1032|def slotZoomIn(self)|
|`slotZoomOut`|fn|pub|1033-1036|def slotZoomOut(self)|
|`slotFitInView`|fn|pub|1037-1041|def slotFitInView(self, checked)|
|`slotSplitterMoved`|fn|pub|1042-1044|def slotSplitterMoved(self, pos, idx)|
|`slotPreviousPage`|fn|pub|1045-1048|def slotPreviousPage(self)|
|`slotNextPage`|fn|pub|1049-1052|def slotNextPage(self)|
|`slotFirstPage`|fn|pub|1053-1056|def slotFirstPage(self)|
|`slotLastPage`|fn|pub|1057-1060|def slotLastPage(self)|
|`slotCurrentPageEdited`|fn|pub|1061-1068|def slotCurrentPageEdited(self, text)|
|`updateControls`|fn|pub|1069-1077|def updateControls(self)|
|`slotSelectionMode`|fn|pub|1078-1081|def slotSelectionMode(self, checked)|
|`slotSelExceptionsChanged`|fn|pub|1082-1084|def slotSelExceptionsChanged(self)|
|`slotSelExceptionsEdited`|fn|pub|1085-1089|def slotSelExceptionsEdited(self, text)|
|`slotSelAspectRatioChanged`|fn|pub|1090-1098|def slotSelAspectRatioChanged(self)|
|`slotSelAspectRatioTypeChanged`|fn|pub|1099-1118|def slotSelAspectRatioTypeChanged(self, index)|
|`distributeAspectRatioChanged`|fn|pub|1119-1121|def distributeAspectRatioChanged(self, aspectRatio)|
|`slotDistributeAspectRatioChanged`|fn|pub|1122-1124|def slotDistributeAspectRatioChanged(self)|
|`slotDeviceTypeChanged`|fn|pub|1125-1131|def slotDeviceTypeChanged(self, index)|
|`slotContextMenu`|fn|pub|1132-1152|def slotContextMenu(self, pos)|
|`slotDeleteSelection`|fn|pub|1153-1156|def slotDeleteSelection(self)|
|`slotNewSelection`|fn|pub|1157-1159|def slotNewSelection(self)|
|`slotNewSelectionGrid`|fn|pub|1160-1178|def slotNewSelectionGrid(self)|
|`createSelectionGrid`|fn|pub|1179-1235|def createSelectionGrid(self, grid)|
|`getPadding`|fn|pub|1236-1263|def getPadding(self)|
|`slotTrimMarginsAll`|fn|pub|1264-1276|def slotTrimMarginsAll(self)|
|`slotTrimMargins`|fn|pub|1277-1281|def slotTrimMargins(self)|
|`trimMarginsSelection`|fn|pub|1282-1385|def trimMarginsSelection(self, sel)|
|`resizeEvent`|fn|pub|1386-1388|def resizeEvent(self, event)|
|`closeEvent`|fn|pub|1389-1390|def closeEvent(self, event)|


---

# mainwindowui_qt5.py | Python | 479L | 3 symbols | 1 imports | 12 comments
> Path: `src/pdfframe/mainwindowui_qt5.py`
- @brief PyQt5-generated UI bindings for `MainWindow`.
- @details Source generated from `mainwindow.ui`; manual edits are restricted to static-analysis metadata.

## Imports
```
from PyQt5 import QtCore, QtWidgets
```

## Definitions

### class `class Ui_MainWindow(object)` : object (L21-220)
- @brief Contains generated widget wiring for the main application window.

### fn `def setupUi(self, MainWindow)` (L26-225)
- @brief Contains generated widget wiring for the main application window.
- @brief Creates widgets, layouts, and signal connections for `MainWindow`.
- @param MainWindow {QtWidgets.QMainWindow} Target window instance.
- @return {None} Applies generated UI graph.

### fn `def retranslateUi(self, MainWindow)` (L388-402)
- @brief Applies translatable UI strings to generated widgets.
- @param MainWindow {QtWidgets.QMainWindow} Target window instance.
- @return {None} Updates texts/tooltips/actions.

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`Ui_MainWindow`|class|pub|21-220|class Ui_MainWindow(object)|
|`setupUi`|fn|pub|26-225|def setupUi(self, MainWindow)|
|`retranslateUi`|fn|pub|388-402|def retranslateUi(self, MainWindow)|


---

# mainwindowui_qt6.py | Python | 477L | 3 symbols | 1 imports | 12 comments
> Path: `src/pdfframe/mainwindowui_qt6.py`
- @brief PyQt6-generated UI bindings for `MainWindow`.
- @details Source generated from `mainwindow.ui`; manual edits are restricted to static-analysis metadata.

## Imports
```
from PyQt6 import QtCore, QtGui, QtWidgets
```

## Definitions

### class `class Ui_MainWindow(object)` : object (L19-218)
- @brief Contains generated widget wiring for the main application window.

### fn `def setupUi(self, MainWindow)` (L24-223)
- @brief Contains generated widget wiring for the main application window.
- @brief Creates widgets, layouts, and signal connections for `MainWindow`.
- @param MainWindow {QtWidgets.QMainWindow} Target window instance.
- @return {None} Applies generated UI graph.

### fn `def retranslateUi(self, MainWindow)` (L386-400)
- @brief Applies translatable UI strings to generated widgets.
- @param MainWindow {QtWidgets.QMainWindow} Target window instance.
- @return {None} Updates texts/tooltips/actions.

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`Ui_MainWindow`|class|pub|19-218|class Ui_MainWindow(object)|
|`setupUi`|fn|pub|24-223|def setupUi(self, MainWindow)|
|`retranslateUi`|fn|pub|386-400|def retranslateUi(self, MainWindow)|


---

# pdfframecmd.py | Python | 348L | 12 symbols | 3 imports | 17 comments
> Path: `src/pdfframe/pdfframecmd.py`
- @brief PyMuPDF-based PDF crop/frame utilities for pdfframe.
- @details Provides crop-box geometry helpers and iterative page processing
through the PyMuPDF `fitz` API with per-page progress reporting,
cancellation support, annotation deletion, and bookmark preservation.
Copyright (C) 2010-2025 Ogekuri
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

## Imports
```
import importlib
import sys
import fitz
```

## Definitions

### class `class CropError(RuntimeError)` : RuntimeError (L23-36)
- @brief Represents a failed PDF crop operation.
- @details Encapsulates error context so caller code can emit deterministic diagnostics for GUI and terminal paths.
- @param message {str} Human-readable error description.
- @return {None} Constructs exception payload.
- fn `def __init__(self, message)` `priv` (L32-36)
  - @brief Represents a failed PDF crop operation.
  - @details Encapsulates error context so caller code can emit deterministic
diagnostics for GUI and terminal paths.
  - @param message {str} Human-readable error description.
  - @return {None} Constructs exception payload.

### class `class CropCancelledError(RuntimeError)` : RuntimeError (L37-47)
- @brief Represents user-requested cancellation of crop processing.
- @details Raised when the cancel callback returns True between page iterations.
- @return {None} Constructs exception payload.
- fn `def __init__(self)` `priv` (L44-47)
  - @brief Represents user-requested cancellation of crop processing.
  - @details Raised when the cancel callback returns True between page iterations.
  - @return {None} Constructs exception payload.

### fn `def _format_scalar(value)` `priv` (L48-61)
- @brief Converts numeric values to stable scalar strings.
- @details Emits integer-like values without decimal suffix and non-integers with compact decimal representation for deterministic logging output.
- @param value {float|int} Numeric value to format.
- @return {str} Stable scalar representation.

### fn `def _blank_outside_selection(page, selection_rect, page_rect)` `priv` (L62-98)
- @brief Draws white fill rectangles over page areas outside a selection.
- @details Covers four rectangular strips (top, bottom, left, right) around the selection boundary with opaque white fill to blank content outside the selection on an original-size page. Used by frame mode to keep page dimensions unchanged while restricting visible content.
- @param page {fitz.Page} PyMuPDF page object to draw on.
- @param selection_rect {fitz.Rect} Selection boundary in PyMuPDF coordinates.
- @param page_rect {fitz.Rect} Full page boundary (MediaBox) in PyMuPDF coordinates.
- @return {None} Modifies page content stream in place.

### fn `def padding_to_crop_offsets(padding)` (L99-113)
- @brief Reorders GUI padding vector to crop-offset order.
- @details Converts GUI tuple [top, right, bottom, left] to crop-offset tuple [left, top, right, bottom] for deterministic crop-box expansion.
- @param padding {list[float]|tuple[float,float,float,float]} GUI padding vector with exactly four components.
- @return {tuple[float,float,float,float]} Crop-offset tuple ordered as left, top, right, bottom.
- @throws {ValueError} If padding vector does not contain exactly four values.

### fn `def crop_values_to_bbox(crop_values, page_width, page_height)` (L114-144)
- @brief Converts normalized selection crop values to absolute page-space crop box.
- @details Merges all visible normalized crops into one union box by first converting each GUI-derived normalized crop tuple to CropBox LL/UR page-space coordinates and then taking bounding extents in left,bottom,right,top order.
- @param crop_values {list[tuple[float,float,float,float]]} Normalized crop tuples (left, top, right, bottom).
- @param page_width {float} Page width in points.
- @param page_height {float} Page height in points.
- @return {tuple[float,float,float,float]|None} Crop box tuple or None when no crop values exist.
- @throws {ValueError} If page dimensions are non-positive.

### fn `def normalized_crop_tuple_to_bbox(crop_value, page_width, page_height)` (L145-167)
- @brief Converts one normalized GUI crop tuple into page-point CropBox coordinates.
- @details Maps normalized GUI tuple `(left, top, right_margin, bottom_margin)` to CropBox corners `(LLx, LLy, URx, URy)` in page-point space with lower-left PDF origin.
- @param crop_value {tuple[float,float,float,float]} Normalized GUI crop tuple.
- @param page_width {float} Page width in points.
- @param page_height {float} Page height in points.
- @return {tuple[float,float,float,float]} CropBox coordinates in left,bottom,right,top order.
- @throws {ValueError} If resulting CropBox is empty.

### fn `def apply_crop_offsets_to_bbox(bbox, offsets, page_width, page_height)` (L168-193)
- @brief Applies GUI crop offsets to an absolute crop box.
- @details Expands or shrinks the crop box by offsets in left,top,right,bottom order and clamps the resulting box to page bounds.
- @param bbox {tuple[float,float,float,float]} Input crop box in left,bottom,right,top order.
- @param offsets {tuple[float,float,float,float]} Crop offsets in left,top,right,bottom order.
- @param page_width {float} Page width in points.
- @param page_height {float} Page height in points.
- @return {tuple[float,float,float,float]} Adjusted crop box in left,bottom,right,top order.
- @throws {ValueError} If resulting crop box is empty after clamping.

### fn `def write_cropped_pages_output(output_file_name, cropped_page_paths)` (L194-218)
- @brief Writes output PDF using only selected cropped page files.
- @details Loads one-page cropped PDF files in provided order and writes a new output PDF that contains exactly those pages.
- @param output_file_name {str} Destination PDF file path.
- @param cropped_page_paths {list[str]} Ordered one-page cropped PDF paths selected for export.
- @return {None} Writes assembled output PDF to filesystem.
- @throws {ValueError} If no cropped pages are provided.

### fn `def crop_pdf_pages(` (L219-232)

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`CropError`|class|pub|23-36|class CropError(RuntimeError)|
|`CropError.__init__`|fn|priv|32-36|def __init__(self, message)|
|`CropCancelledError`|class|pub|37-47|class CropCancelledError(RuntimeError)|
|`CropCancelledError.__init__`|fn|priv|44-47|def __init__(self)|
|`_format_scalar`|fn|priv|48-61|def _format_scalar(value)|
|`_blank_outside_selection`|fn|priv|62-98|def _blank_outside_selection(page, selection_rect, page_r...|
|`padding_to_crop_offsets`|fn|pub|99-113|def padding_to_crop_offsets(padding)|
|`crop_values_to_bbox`|fn|pub|114-144|def crop_values_to_bbox(crop_values, page_width, page_hei...|
|`normalized_crop_tuple_to_bbox`|fn|pub|145-167|def normalized_crop_tuple_to_bbox(crop_value, page_width,...|
|`apply_crop_offsets_to_bbox`|fn|pub|168-193|def apply_crop_offsets_to_bbox(bbox, offsets, page_width,...|
|`write_cropped_pages_output`|fn|pub|194-218|def write_cropped_pages_output(output_file_name, cropped_...|
|`crop_pdf_pages`|fn|pub|219-232|def crop_pdf_pages(|


---

# pdfframeper.py | Python | 322L | 61 symbols | 9 imports | 43 comments
> Path: `src/pdfframe/pdfframeper.py`
- @brief PDF backend adapters for loading and writing cropped documents.
- @details Provides wrapper classes over pypdf, PyPDF2, PyMuPDF, and pikepdf for unified crop operations.
Copyright (C) 2010-2025 Ogekuri.
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

## Imports
```
import copy
import sys
from pdfframe.config import PYQT6
import fitz
from pikepdf import Pdf
from pypdf import PdfReader, PdfWriter
import PyPDF2
from PyPDF2 import PdfFileReader as PdfReader, PdfFileWriter as PdfWriter
from PyPDF2 import PdfReader, PdfWriter
```

## Definitions

### class `class PdfEncryptedError(Exception)` : Exception (L21-24)

### class `class AbstractPdfFile` (L25-32)
- fn `def loadFromStream(self, stream)` (L28-29)
- fn `def loadFromFile(self, filename)` (L30-32)

### class `class PyPdfFile(AbstractPdfFile)` : AbstractPdfFile (L33-47)
- fn `def __init__(self)` `priv` (L35-36)
- fn `def loadFromStream(self, stream)` (L37-44)
- fn `def getPage(self, nr)` (L45-47)

### class `class PyPdfOldFile(PyPdfFile)` : PyPdfFile (L48-61)
- fn `def loadFromStream(self, stream)` (L51-58)
- fn `def getPage(self, nr)` (L59-61)

### class `class PyMuPdfFile(AbstractPdfFile)` : AbstractPdfFile (L62-72)
- fn `def __init__(self)` `priv` (L64-65)
- fn `def loadFromStream(self, stream)` (L66-69)
- fn `def getPage(self, nr)` (L70-72)

### class `class PikePdfFile(AbstractPdfFile)` : AbstractPdfFile (L73-84)
- fn `def __init__(self)` `priv` (L75-76)
- fn `def loadFromStream(self, stream)` (L77-80)
- fn `def getPage(self, nr)` (L81-84)

### class `class AbstractPdfFrameper` (L85-98)
- fn `def writeToStream(self, stream)` (L88-89)
- fn `def writeToFile(self, filename)` (L90-93)
- fn `def addPageCropped(self, pdffile, pagenumber, croplist, rotate=0)` (L94-95)
- fn `def copyDocumentRoot(self, pdffile)` (L96-98)

### class `class SemiAbstractPdfFrameper(AbstractPdfFrameper)` : AbstractPdfFrameper (L99-119)
- fn `def addPageCropped(self, pdffile, pagenumber, croplist, alwaysinclude, rotate=0)` (L102-112)
- fn `def doAddPage(self, page, rotate)` (L113-114)
- fn `def pageGetCropBox(self, page)` (L115-116)
- fn `def pageSetCropBox(self, page, box)` (L117-119)

### class `class PyPdfFrameper(SemiAbstractPdfFrameper)` : SemiAbstractPdfFrameper (L120-151)
- fn `def __init__(self)` `priv` (L122-123)
- fn `def writeToStream(self, stream)` (L124-132)
- fn `def doAddPage(self, page, rotate)` (L133-136)
- fn `def pageGetCropBox(self, page)` (L137-140)
- fn `def pageSetCropBox(self, page, box)` (L141-145)
- fn `def copyDocumentRoot(self, pdffile)` (L146-151)

### class `class PyPdfOldCropper(PyPdfFrameper)` : PyPdfFrameper (L152-172)
- fn `def doAddPage(self, page, rotate)` (L154-157)
- fn `def pageGetCropBox(self, page)` (L158-161)
- fn `def pageSetCropBox(self, page, box)` (L162-166)
- fn `def copyDocumentRoot(self, pdffile)` (L167-172)

### class `class PyMuPdfFrameper(SemiAbstractPdfFrameper)` : SemiAbstractPdfFrameper (L173-213)
- fn `def __init__(self)` `priv` (L175-176)
- fn `def writeToStream(self, stream)` (L177-178)
- fn `def addPageCropped(self, pdffile, pagenumber, croplist, alwaysinclude, rotate=0)` (L179-196)
- fn `def addPage()` (L180-183)
- fn `def pageGetCropBox(self, page)` (L197-198)
- fn `def pageSetCropBox(self, page, box)` (L199-209)
- fn `def copyDocumentRoot(self, pdffile)` (L210-213)

### class `class PikePdfFrameper(SemiAbstractPdfFrameper)` : SemiAbstractPdfFrameper (L214-237)
- fn `def __init__(self)` `priv` (L216-217)
- fn `def writeToStream(self, stream)` (L218-219)
- fn `def doAddPage(self, page, rotate)` (L220-223)
- fn `def pageGetCropBox(self, page)` (L224-229)
- fn `def pageSetCropBox(self, page, box)` (L230-233)
- fn `def copyDocumentRoot(self, pdffile)` (L234-237)

### fn `def computeCropBoxCoords(box, crop, pdf_coords=True)` (L238-249)

### fn `def import_pymupdf()` (L253-260)

### fn `def import_pikepdf()` (L261-266)

### fn `def import_pypdf()` (L267-272)

### fn `def import_pypdf2()` (L273-287)

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`PdfEncryptedError`|class|pub|21-24|class PdfEncryptedError(Exception)|
|`AbstractPdfFile`|class|pub|25-32|class AbstractPdfFile|
|`AbstractPdfFile.loadFromStream`|fn|pub|28-29|def loadFromStream(self, stream)|
|`AbstractPdfFile.loadFromFile`|fn|pub|30-32|def loadFromFile(self, filename)|
|`PyPdfFile`|class|pub|33-47|class PyPdfFile(AbstractPdfFile)|
|`PyPdfFile.__init__`|fn|priv|35-36|def __init__(self)|
|`PyPdfFile.loadFromStream`|fn|pub|37-44|def loadFromStream(self, stream)|
|`PyPdfFile.getPage`|fn|pub|45-47|def getPage(self, nr)|
|`PyPdfOldFile`|class|pub|48-61|class PyPdfOldFile(PyPdfFile)|
|`PyPdfOldFile.loadFromStream`|fn|pub|51-58|def loadFromStream(self, stream)|
|`PyPdfOldFile.getPage`|fn|pub|59-61|def getPage(self, nr)|
|`PyMuPdfFile`|class|pub|62-72|class PyMuPdfFile(AbstractPdfFile)|
|`PyMuPdfFile.__init__`|fn|priv|64-65|def __init__(self)|
|`PyMuPdfFile.loadFromStream`|fn|pub|66-69|def loadFromStream(self, stream)|
|`PyMuPdfFile.getPage`|fn|pub|70-72|def getPage(self, nr)|
|`PikePdfFile`|class|pub|73-84|class PikePdfFile(AbstractPdfFile)|
|`PikePdfFile.__init__`|fn|priv|75-76|def __init__(self)|
|`PikePdfFile.loadFromStream`|fn|pub|77-80|def loadFromStream(self, stream)|
|`PikePdfFile.getPage`|fn|pub|81-84|def getPage(self, nr)|
|`AbstractPdfFrameper`|class|pub|85-98|class AbstractPdfFrameper|
|`AbstractPdfFrameper.writeToStream`|fn|pub|88-89|def writeToStream(self, stream)|
|`AbstractPdfFrameper.writeToFile`|fn|pub|90-93|def writeToFile(self, filename)|
|`AbstractPdfFrameper.addPageCropped`|fn|pub|94-95|def addPageCropped(self, pdffile, pagenumber, croplist, r...|
|`AbstractPdfFrameper.copyDocumentRoot`|fn|pub|96-98|def copyDocumentRoot(self, pdffile)|
|`SemiAbstractPdfFrameper`|class|pub|99-119|class SemiAbstractPdfFrameper(AbstractPdfFrameper)|
|`SemiAbstractPdfFrameper.addPageCropped`|fn|pub|102-112|def addPageCropped(self, pdffile, pagenumber, croplist, a...|
|`SemiAbstractPdfFrameper.doAddPage`|fn|pub|113-114|def doAddPage(self, page, rotate)|
|`SemiAbstractPdfFrameper.pageGetCropBox`|fn|pub|115-116|def pageGetCropBox(self, page)|
|`SemiAbstractPdfFrameper.pageSetCropBox`|fn|pub|117-119|def pageSetCropBox(self, page, box)|
|`PyPdfFrameper`|class|pub|120-151|class PyPdfFrameper(SemiAbstractPdfFrameper)|
|`PyPdfFrameper.__init__`|fn|priv|122-123|def __init__(self)|
|`PyPdfFrameper.writeToStream`|fn|pub|124-132|def writeToStream(self, stream)|
|`PyPdfFrameper.doAddPage`|fn|pub|133-136|def doAddPage(self, page, rotate)|
|`PyPdfFrameper.pageGetCropBox`|fn|pub|137-140|def pageGetCropBox(self, page)|
|`PyPdfFrameper.pageSetCropBox`|fn|pub|141-145|def pageSetCropBox(self, page, box)|
|`PyPdfFrameper.copyDocumentRoot`|fn|pub|146-151|def copyDocumentRoot(self, pdffile)|
|`PyPdfOldCropper`|class|pub|152-172|class PyPdfOldCropper(PyPdfFrameper)|
|`PyPdfOldCropper.doAddPage`|fn|pub|154-157|def doAddPage(self, page, rotate)|
|`PyPdfOldCropper.pageGetCropBox`|fn|pub|158-161|def pageGetCropBox(self, page)|
|`PyPdfOldCropper.pageSetCropBox`|fn|pub|162-166|def pageSetCropBox(self, page, box)|
|`PyPdfOldCropper.copyDocumentRoot`|fn|pub|167-172|def copyDocumentRoot(self, pdffile)|
|`PyMuPdfFrameper`|class|pub|173-213|class PyMuPdfFrameper(SemiAbstractPdfFrameper)|
|`PyMuPdfFrameper.__init__`|fn|priv|175-176|def __init__(self)|
|`PyMuPdfFrameper.writeToStream`|fn|pub|177-178|def writeToStream(self, stream)|
|`PyMuPdfFrameper.addPageCropped`|fn|pub|179-196|def addPageCropped(self, pdffile, pagenumber, croplist, a...|
|`PyMuPdfFrameper.addPage`|fn|pub|180-183|def addPage()|
|`PyMuPdfFrameper.pageGetCropBox`|fn|pub|197-198|def pageGetCropBox(self, page)|
|`PyMuPdfFrameper.pageSetCropBox`|fn|pub|199-209|def pageSetCropBox(self, page, box)|
|`PyMuPdfFrameper.copyDocumentRoot`|fn|pub|210-213|def copyDocumentRoot(self, pdffile)|
|`PikePdfFrameper`|class|pub|214-237|class PikePdfFrameper(SemiAbstractPdfFrameper)|
|`PikePdfFrameper.__init__`|fn|priv|216-217|def __init__(self)|
|`PikePdfFrameper.writeToStream`|fn|pub|218-219|def writeToStream(self, stream)|
|`PikePdfFrameper.doAddPage`|fn|pub|220-223|def doAddPage(self, page, rotate)|
|`PikePdfFrameper.pageGetCropBox`|fn|pub|224-229|def pageGetCropBox(self, page)|
|`PikePdfFrameper.pageSetCropBox`|fn|pub|230-233|def pageSetCropBox(self, page, box)|
|`PikePdfFrameper.copyDocumentRoot`|fn|pub|234-237|def copyDocumentRoot(self, pdffile)|
|`computeCropBoxCoords`|fn|pub|238-249|def computeCropBoxCoords(box, crop, pdf_coords=True)|
|`import_pymupdf`|fn|pub|253-260|def import_pymupdf()|
|`import_pikepdf`|fn|pub|261-266|def import_pikepdf()|
|`import_pypdf`|fn|pub|267-272|def import_pypdf()|
|`import_pypdf2`|fn|pub|273-287|def import_pypdf2()|


---

# qt.py | Python | 18L | 0 symbols | 7 imports | 3 comments
> Path: `src/pdfframe/qt.py`
- @brief Unified Qt symbol export layer for PyQt6/PyQt5 compatibility.
- @details Re-exports QtCore/QtGui/QtWidgets symbols based on runtime backend selection.

## Imports
```
from pdfframe.config import PYQT6
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
```


---

# version.py | Python | 1L | 0 symbols | 0 imports | 0 comments
> Path: `src/pdfframe/version.py`


---

# vieweritem.py | Python | 300L | 43 symbols | 7 imports | 26 comments
> Path: `src/pdfframe/vieweritem.py`
- @brief Viewer backends and rendering abstractions for PDF page display.
- @details Implements Qt graphics-item viewer classes for Poppler and PyMuPDF rendering backends.
Copyright (C) 2010-2025 Ogekuri.
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

## Imports
```
import sys
from pdfframe.config import PYQT6
from pdfframe.qt import *
from pdfframe.viewerselections import ViewerSelections
import fitz
import fitz
from popplerqt5 import Poppler
```

## Definitions

### class `class AbstractViewerItem(QGraphicsItem)` : QGraphicsItem (L24-161)
- fn `def __init__(self, mainwindow)` `priv` (L27-32)
- fn `def reset(self)` (L33-39)
- fn `def boundingRect(self)` (L40-42)
- fn `def isPortrait(self)` (L43-45)
- fn `def paint(self, painter, option, widget)` (L46-52)
- fn `def mapRectToImage(self, r)` (L53-55)
- fn `def mapRectFromImage(self, r)` (L56-58)
- fn `def getCurrentPageIndex(self)` (L59-61)
- fn `def setCurrentPageIndex(self, idx)` (L62-81)
- fn `def previousPage(self)` (L84-86)
- fn `def nextPage(self)` (L87-89)
- fn `def firstPage(self)` (L90-92)
- fn `def lastPage(self)` (L93-95)
- fn `def getImage(self, idx)` (L96-102)
- fn `def mousePressEvent(self, event)` (L103-105)
- fn `def mouseMoveEvent(self, event)` (L106-108)
- fn `def mouseReleaseEvent(self, event)` (L109-111)
- fn `def load(self, filename)` (L112-117)
- fn `def doLoad(self, filename)` (L120-122)
- fn `def numPages(self)` (L123-125)
- fn `def isEmpty(self)` (L126-128)
- fn `def cacheImage(self, idx)` (L129-131)
- fn `def pageGetRotation(self, idx)` (L132-134)
- fn `def pageGetSizePoints(self, idx)` (L135-146)
  - @brief Returns page size for bbox conversion when backend metadata is unavailable.
  - @details Uses rendered image dimensions as fallback point-like units for callers that require non-zero geometry values.
  - @param idx {int} Zero-based page index.
  - @return {tuple[float,float]} Width and height pair.
- fn `def cropValues(self, idx)` (L147-161)
- fn `def adjustForOrientation(cv)` (L148-156)

### class `class PopplerViewerItem(AbstractViewerItem)` : AbstractViewerItem (L162-210)
- fn `def reset(self)` (L164-167)
- fn `def doLoad(self, filename)` (L168-173)
- fn `def numPages(self)` (L174-179)
- fn `def cacheImage(self, idx)` (L180-184)
- fn `def pageGetRotation(self, idx)` (L185-196)
- fn `def pageGetSizePoints(self, idx)` (L197-210)
  - @brief Returns Poppler page size in point units.
  - @details Queries Poppler page metadata and exposes width/height values used by command-backend crop-box generation logic.
  - @param idx {int} Zero-based page index.
  - @return {tuple[float,float]} Width and height pair in points.

### class `class MuPDFViewerItem(AbstractViewerItem)` : AbstractViewerItem (L211-255)
- fn `def reset(self)` (L213-216)
- fn `def doLoad(self, filename)` (L217-222)
- fn `def numPages(self)` (L223-228)
- fn `def cacheImage(self, idx)` (L229-239)
- fn `def pageGetRotation(self, idx)` (L240-243)
- fn `def pageGetSizePoints(self, idx)` (L244-255)
  - @brief Returns MuPDF media-box dimensions in point units.
  - @details Reads page media-box coordinates and provides width/height for deterministic bbox conversion in command-based cropping.
  - @param idx {int} Zero-based page index.
  - @return {tuple[float,float]} Width and height pair in points.

- var `POPPLERQT = 1` (L257)
- var `PYMUPDF = 2` (L258)
## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`AbstractViewerItem`|class|pub|24-161|class AbstractViewerItem(QGraphicsItem)|
|`AbstractViewerItem.__init__`|fn|priv|27-32|def __init__(self, mainwindow)|
|`AbstractViewerItem.reset`|fn|pub|33-39|def reset(self)|
|`AbstractViewerItem.boundingRect`|fn|pub|40-42|def boundingRect(self)|
|`AbstractViewerItem.isPortrait`|fn|pub|43-45|def isPortrait(self)|
|`AbstractViewerItem.paint`|fn|pub|46-52|def paint(self, painter, option, widget)|
|`AbstractViewerItem.mapRectToImage`|fn|pub|53-55|def mapRectToImage(self, r)|
|`AbstractViewerItem.mapRectFromImage`|fn|pub|56-58|def mapRectFromImage(self, r)|
|`AbstractViewerItem.getCurrentPageIndex`|fn|pub|59-61|def getCurrentPageIndex(self)|
|`AbstractViewerItem.setCurrentPageIndex`|fn|pub|62-81|def setCurrentPageIndex(self, idx)|
|`AbstractViewerItem.previousPage`|fn|pub|84-86|def previousPage(self)|
|`AbstractViewerItem.nextPage`|fn|pub|87-89|def nextPage(self)|
|`AbstractViewerItem.firstPage`|fn|pub|90-92|def firstPage(self)|
|`AbstractViewerItem.lastPage`|fn|pub|93-95|def lastPage(self)|
|`AbstractViewerItem.getImage`|fn|pub|96-102|def getImage(self, idx)|
|`AbstractViewerItem.mousePressEvent`|fn|pub|103-105|def mousePressEvent(self, event)|
|`AbstractViewerItem.mouseMoveEvent`|fn|pub|106-108|def mouseMoveEvent(self, event)|
|`AbstractViewerItem.mouseReleaseEvent`|fn|pub|109-111|def mouseReleaseEvent(self, event)|
|`AbstractViewerItem.load`|fn|pub|112-117|def load(self, filename)|
|`AbstractViewerItem.doLoad`|fn|pub|120-122|def doLoad(self, filename)|
|`AbstractViewerItem.numPages`|fn|pub|123-125|def numPages(self)|
|`AbstractViewerItem.isEmpty`|fn|pub|126-128|def isEmpty(self)|
|`AbstractViewerItem.cacheImage`|fn|pub|129-131|def cacheImage(self, idx)|
|`AbstractViewerItem.pageGetRotation`|fn|pub|132-134|def pageGetRotation(self, idx)|
|`AbstractViewerItem.pageGetSizePoints`|fn|pub|135-146|def pageGetSizePoints(self, idx)|
|`AbstractViewerItem.cropValues`|fn|pub|147-161|def cropValues(self, idx)|
|`AbstractViewerItem.adjustForOrientation`|fn|pub|148-156|def adjustForOrientation(cv)|
|`PopplerViewerItem`|class|pub|162-210|class PopplerViewerItem(AbstractViewerItem)|
|`PopplerViewerItem.reset`|fn|pub|164-167|def reset(self)|
|`PopplerViewerItem.doLoad`|fn|pub|168-173|def doLoad(self, filename)|
|`PopplerViewerItem.numPages`|fn|pub|174-179|def numPages(self)|
|`PopplerViewerItem.cacheImage`|fn|pub|180-184|def cacheImage(self, idx)|
|`PopplerViewerItem.pageGetRotation`|fn|pub|185-196|def pageGetRotation(self, idx)|
|`PopplerViewerItem.pageGetSizePoints`|fn|pub|197-210|def pageGetSizePoints(self, idx)|
|`MuPDFViewerItem`|class|pub|211-255|class MuPDFViewerItem(AbstractViewerItem)|
|`MuPDFViewerItem.reset`|fn|pub|213-216|def reset(self)|
|`MuPDFViewerItem.doLoad`|fn|pub|217-222|def doLoad(self, filename)|
|`MuPDFViewerItem.numPages`|fn|pub|223-228|def numPages(self)|
|`MuPDFViewerItem.cacheImage`|fn|pub|229-239|def cacheImage(self, idx)|
|`MuPDFViewerItem.pageGetRotation`|fn|pub|240-243|def pageGetRotation(self, idx)|
|`MuPDFViewerItem.pageGetSizePoints`|fn|pub|244-255|def pageGetSizePoints(self, idx)|
|`POPPLERQT`|var|pub|257||
|`PYMUPDF`|var|pub|258||


---

# viewerselections.py | Python | 667L | 71 symbols | 2 imports | 42 comments
> Path: `src/pdfframe/viewerselections.py`
- @brief Interactive selection items and gestures used by viewer backends.
- @details Defines selection geometry, resize handles, and mouse-driven edit behavior in scene coordinates.
Copyright (C) 2010-2020 ogekuri.
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

## Imports
```
from math import ceil
from pdfframe.qt import *
```

## Definitions

### class `class ViewerSelections(object)` : object (L21-170)
- fn `def __init__(self, viewer)` `priv` (L29-37)
- fn `def items(self)` (L39-46)
- fn `def addSelection(self, rect=None)` (L47-62)
  - @brief Creates the selection area when absent.
  - @details Enforces single-selection mode by returning the existing area when one is already present.
  - @param rect {QRectF|None} Optional initial rectangle for first creation.
  - @return {ViewerSelectionItem} Current selection area.
- fn `def deleteSelection(self, s)` (L63-69)
- fn `def deleteSelections(self)` (L70-73)
- fn `def getCurrentSelection(self)` (L74-76)
- fn `def setCurrentSelection(self, currentSelection)` (L77-88)
- fn `def autoSetCurrentSelection(self)` (L91-104)
- fn `def currentSelectionUpdated(self)` (L105-107)
- fn `def getDistributeAspectRatio(self)` (L108-110)
- fn `def setDistributeAspectRatio(self, distributeAspectRatio)` (L111-114)
- fn `def getSelectionMode(self)` (L117-119)
- fn `def setSelectionMode(self, mode)` (L120-123)
- fn `def getSelectionExceptions(self)` (L126-128)
- fn `def setSelectionExceptions(self, exceptions)` (L129-132)
- fn `def updateSelectionVisibility(self)` (L135-140)
- fn `def cropValues(self, idx)` (L141-144)
- fn `def mousePressEvent(self, event)` (L145-161)
  - @brief Starts scene-level selection creation gesture.
  - @details Creates a first selection on left click only when no selection exists; otherwise keeps the existing area current.
  - @param event {QGraphicsSceneMouseEvent} Mouse event object.
  - @return {None} Applies selection creation side effects.
- fn `def mouseMoveEvent(self, event)` (L162-166)
- fn `def mouseReleaseEvent(self, event)` (L167-170)

### class `class ViewerSelectionItem(QGraphicsItem)` : QGraphicsItem (L171-370)
- fn `def __init__(self, parent, rect=None)` `priv` (L177-203)
- fn `def selection(self)` (L205-208)
- fn `def viewer(self)` (L210-212)
- fn `def selections(self)` (L214-217)
- fn `def isCurrent(self)` (L218-220)
- fn `def setAsCurrent(self)` (L221-224)
- fn `def orderIndex(self)` (L226-234)
- fn `def aspectRatio(self)` (L236-238)
- fn `def getAspectRatioData(self)` (L239-241)
- fn `def setAspectRatioData(self, data)` (L242-255)
- fn `def distributeAspectRatio(self)` (L260-263)
- fn `def selectionVisibleOnPage(self, pageIndex)` (L264-269)
- fn `def boundingRect(self)` (L270-272)
- fn `def setBoundingRect(self, pt1, pt2)` (L273-282)
- fn `def adjustBoundingRect(self, dx1=0, dy1=0, dx2=0, dy2=0)` (L283-354)
- fn `def moveBoundingRect(self, dx, dy)` (L355-369)

### fn `def distributeRect(self)` (L370-382)

### fn `def cropValues(self)` (L383-399)

### fn `def clamp(v)` (L385-386)

### fn `def cV(r)` (L387-397)

### fn `def mapRectToImage(self, r)` (L400-403)

### fn `def mapRectFromImage(self, r)` (L404-407)

### fn `def paint(self, painter, option, widget)` (L408-439)

### fn `def drawLine(pt1, pt2)` (L419-424)

### fn `def mousePressEvent(self, event)` (L440-451)

### fn `def mouseMoveEvent(self, event)` (L452-470)

### fn `def mouseReleaseEvent(self, event)` (L471-474)

### fn `def keyPressEvent(self, event)` (L475-494)

### class `class SelectionHandleItem(QGraphicsItem)` : QGraphicsItem (L495-595)
- fn `def __init__(self, parent, role)` `priv` (L502-517)
- fn `def selection(self)` (L519-521)
- fn `def handleColor(self)` (L523-527)
- fn `def boundingRect(self)` (L528-547)
- fn `def paint(self, painter, option, widget)` (L548-567)
- fn `def mousePressEvent(self, event)` (L568-573)
- fn `def mouseMoveEvent(self, event)` (L574-591)
- fn `def mouseReleaseEvent(self, event)` (L592-595)

### class `class SelectionCornerHandleItem(QGraphicsItem)` : QGraphicsItem (L596-655)
- fn `def __init__(self, parent, lr, tb)` `priv` (L597-607)
- fn `def selection(self)` (L609-611)
- fn `def handleColor(self)` (L613-617)
- fn `def corner(self, rect)` (L618-621)
- fn `def direction(self, pt)` (L622-627)
- fn `def boundingRect(self)` (L628-633)
- fn `def paint(self, painter, option, widget)` (L634-639)
- fn `def mousePressEvent(self, event)` (L640-645)
- fn `def mouseMoveEvent(self, event)` (L646-651)
- fn `def mouseReleaseEvent(self, event)` (L652-655)

### fn `def aspectRatioFromStr(s)` (L656-667)

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`ViewerSelections`|class|pub|21-170|class ViewerSelections(object)|
|`ViewerSelections.__init__`|fn|priv|29-37|def __init__(self, viewer)|
|`ViewerSelections.items`|fn|pub|39-46|def items(self)|
|`ViewerSelections.addSelection`|fn|pub|47-62|def addSelection(self, rect=None)|
|`ViewerSelections.deleteSelection`|fn|pub|63-69|def deleteSelection(self, s)|
|`ViewerSelections.deleteSelections`|fn|pub|70-73|def deleteSelections(self)|
|`ViewerSelections.getCurrentSelection`|fn|pub|74-76|def getCurrentSelection(self)|
|`ViewerSelections.setCurrentSelection`|fn|pub|77-88|def setCurrentSelection(self, currentSelection)|
|`ViewerSelections.autoSetCurrentSelection`|fn|pub|91-104|def autoSetCurrentSelection(self)|
|`ViewerSelections.currentSelectionUpdated`|fn|pub|105-107|def currentSelectionUpdated(self)|
|`ViewerSelections.getDistributeAspectRatio`|fn|pub|108-110|def getDistributeAspectRatio(self)|
|`ViewerSelections.setDistributeAspectRatio`|fn|pub|111-114|def setDistributeAspectRatio(self, distributeAspectRatio)|
|`ViewerSelections.getSelectionMode`|fn|pub|117-119|def getSelectionMode(self)|
|`ViewerSelections.setSelectionMode`|fn|pub|120-123|def setSelectionMode(self, mode)|
|`ViewerSelections.getSelectionExceptions`|fn|pub|126-128|def getSelectionExceptions(self)|
|`ViewerSelections.setSelectionExceptions`|fn|pub|129-132|def setSelectionExceptions(self, exceptions)|
|`ViewerSelections.updateSelectionVisibility`|fn|pub|135-140|def updateSelectionVisibility(self)|
|`ViewerSelections.cropValues`|fn|pub|141-144|def cropValues(self, idx)|
|`ViewerSelections.mousePressEvent`|fn|pub|145-161|def mousePressEvent(self, event)|
|`ViewerSelections.mouseMoveEvent`|fn|pub|162-166|def mouseMoveEvent(self, event)|
|`ViewerSelections.mouseReleaseEvent`|fn|pub|167-170|def mouseReleaseEvent(self, event)|
|`ViewerSelectionItem`|class|pub|171-370|class ViewerSelectionItem(QGraphicsItem)|
|`ViewerSelectionItem.__init__`|fn|priv|177-203|def __init__(self, parent, rect=None)|
|`ViewerSelectionItem.selection`|fn|pub|205-208|def selection(self)|
|`ViewerSelectionItem.viewer`|fn|pub|210-212|def viewer(self)|
|`ViewerSelectionItem.selections`|fn|pub|214-217|def selections(self)|
|`ViewerSelectionItem.isCurrent`|fn|pub|218-220|def isCurrent(self)|
|`ViewerSelectionItem.setAsCurrent`|fn|pub|221-224|def setAsCurrent(self)|
|`ViewerSelectionItem.orderIndex`|fn|pub|226-234|def orderIndex(self)|
|`ViewerSelectionItem.aspectRatio`|fn|pub|236-238|def aspectRatio(self)|
|`ViewerSelectionItem.getAspectRatioData`|fn|pub|239-241|def getAspectRatioData(self)|
|`ViewerSelectionItem.setAspectRatioData`|fn|pub|242-255|def setAspectRatioData(self, data)|
|`ViewerSelectionItem.distributeAspectRatio`|fn|pub|260-263|def distributeAspectRatio(self)|
|`ViewerSelectionItem.selectionVisibleOnPage`|fn|pub|264-269|def selectionVisibleOnPage(self, pageIndex)|
|`ViewerSelectionItem.boundingRect`|fn|pub|270-272|def boundingRect(self)|
|`ViewerSelectionItem.setBoundingRect`|fn|pub|273-282|def setBoundingRect(self, pt1, pt2)|
|`ViewerSelectionItem.adjustBoundingRect`|fn|pub|283-354|def adjustBoundingRect(self, dx1=0, dy1=0, dx2=0, dy2=0)|
|`ViewerSelectionItem.moveBoundingRect`|fn|pub|355-369|def moveBoundingRect(self, dx, dy)|
|`distributeRect`|fn|pub|370-382|def distributeRect(self)|
|`cropValues`|fn|pub|383-399|def cropValues(self)|
|`clamp`|fn|pub|385-386|def clamp(v)|
|`cV`|fn|pub|387-397|def cV(r)|
|`mapRectToImage`|fn|pub|400-403|def mapRectToImage(self, r)|
|`mapRectFromImage`|fn|pub|404-407|def mapRectFromImage(self, r)|
|`paint`|fn|pub|408-439|def paint(self, painter, option, widget)|
|`drawLine`|fn|pub|419-424|def drawLine(pt1, pt2)|
|`mousePressEvent`|fn|pub|440-451|def mousePressEvent(self, event)|
|`mouseMoveEvent`|fn|pub|452-470|def mouseMoveEvent(self, event)|
|`mouseReleaseEvent`|fn|pub|471-474|def mouseReleaseEvent(self, event)|
|`keyPressEvent`|fn|pub|475-494|def keyPressEvent(self, event)|
|`SelectionHandleItem`|class|pub|495-595|class SelectionHandleItem(QGraphicsItem)|
|`SelectionHandleItem.__init__`|fn|priv|502-517|def __init__(self, parent, role)|
|`SelectionHandleItem.selection`|fn|pub|519-521|def selection(self)|
|`SelectionHandleItem.handleColor`|fn|pub|523-527|def handleColor(self)|
|`SelectionHandleItem.boundingRect`|fn|pub|528-547|def boundingRect(self)|
|`SelectionHandleItem.paint`|fn|pub|548-567|def paint(self, painter, option, widget)|
|`SelectionHandleItem.mousePressEvent`|fn|pub|568-573|def mousePressEvent(self, event)|
|`SelectionHandleItem.mouseMoveEvent`|fn|pub|574-591|def mouseMoveEvent(self, event)|
|`SelectionHandleItem.mouseReleaseEvent`|fn|pub|592-595|def mouseReleaseEvent(self, event)|
|`SelectionCornerHandleItem`|class|pub|596-655|class SelectionCornerHandleItem(QGraphicsItem)|
|`SelectionCornerHandleItem.__init__`|fn|priv|597-607|def __init__(self, parent, lr, tb)|
|`SelectionCornerHandleItem.selection`|fn|pub|609-611|def selection(self)|
|`SelectionCornerHandleItem.handleColor`|fn|pub|613-617|def handleColor(self)|
|`SelectionCornerHandleItem.corner`|fn|pub|618-621|def corner(self, rect)|
|`SelectionCornerHandleItem.direction`|fn|pub|622-627|def direction(self, pt)|
|`SelectionCornerHandleItem.boundingRect`|fn|pub|628-633|def boundingRect(self)|
|`SelectionCornerHandleItem.paint`|fn|pub|634-639|def paint(self, painter, option, widget)|
|`SelectionCornerHandleItem.mousePressEvent`|fn|pub|640-645|def mousePressEvent(self, event)|
|`SelectionCornerHandleItem.mouseMoveEvent`|fn|pub|646-651|def mouseMoveEvent(self, event)|
|`SelectionCornerHandleItem.mouseReleaseEvent`|fn|pub|652-655|def mouseReleaseEvent(self, event)|
|`aspectRatioFromStr`|fn|pub|656-667|def aspectRatioFromStr(s)|

