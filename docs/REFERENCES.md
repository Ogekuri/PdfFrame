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
- Brief: CLI entrypoint for pdfframe GUI and one-shot conversion.
- Details: Parses command-line arguments, applies startup options on MainWindow, and launches Qt event loop.
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
- Brief: Margin auto-trimming helpers for selection rectangles.
- Details: Performs grayscale transition scanning to shrink candidate rectangles while preserving content bounds.
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
- Brief: Auto-trims margins of a rectangle using grayscale-transition thresholds.
- Details: Scans rectangle border lines and trims sides while per-line grayscale transitions remain within configured sensitivity and grayscale-sensitivity.
- Param: img {QImage} Page image used for grayscale sampling.
- Param: r {QRect} Candidate rectangle to trim.
- Param: minr {QRect|None} Optional minimum rectangle that limits trimming.
- Param: sensitivity {float} Minimum pixel delta counted as a transition.
- Param: grayscale_sensitivity {float} Maximum accepted transition count per scan line.
- Return: {QRect} Trimmed rectangle clamped to image bounds.

### fn `def pixAt(x, y)` (L32-34)
- Brief: Auto-trims margins of a rectangle using grayscale-transition thresholds.
- Details: Scans rectangle border lines and trims sides while per-line grayscale
transitions remain within configured sensitivity and grayscale-sensitivity.
- Param: img {QImage} Page image used for grayscale sampling.
- Param: r {QRect} Candidate rectangle to trim.
- Param: minr {QRect|None} Optional minimum rectangle that limits trimming.
- Param: sensitivity {float} Minimum pixel delta counted as a transition.
- Param: grayscale_sensitivity {float} Maximum accepted transition count per scan line.
- Return: {QRect} Trimmed rectangle clamped to image bounds.

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
- Brief: Runtime backend-selection flags for pdfframe.
- Details: Detects which Qt binding is available and exposes the `PYQT6` switch consumed by UI modules.

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
- Brief: Returns canonical user JSON configuration path.
- Details: Resolves `~/.pdfframe/config.json` using current user home directory.
- Return: {pathlib.Path} Expanded configuration file path.

### fn `def default_config_document()` (L32-40)
- Brief: Returns default JSON configuration document.
- Details: Includes top-level `config` object seeded from `DEFAULT_CONFIG_VALUES` and empty `presets` array.
- Return: {dict[str,object]} Default config document payload.

### class `class JsonConfigStore` (L41-113)
- Brief: Provides normalized JSON config read/write operations.
- Details: Enforces top-level `config` and `presets` sections and guarantees default keys for config values.
- fn `def __init__(self, path=None)` `priv` (L47-54)
  - Brief: Provides normalized JSON config read/write operations.
  - Brief: Initializes JSON config store.
  - Details: Enforces top-level `config` and `presets` sections and guarantees default keys for config values.
  - Details: Uses explicit path when provided; otherwise defaults to `~/.pdfframe/config.json`.
  - Param: path {str|pathlib.Path|None} Optional configuration path override.
- fn `def _normalize_document(self, document)` `priv` (L55-79)
  - Brief: Normalizes JSON config document shape.
  - Details: Validates root object and top-level section types, merges missing default config keys, and guarantees list type for presets.
  - Param: document {dict[str,object]} Raw decoded JSON payload.
  - Return: {dict[str,object]} Normalized document.
  - Throws: {ValueError} If root or required sections have incompatible types.
- fn `def load_or_initialize(self)` (L80-99)
  - Brief: Loads JSON configuration and creates defaults when missing.
  - Details: Creates `~/.pdfframe/config.json` when absent, normalizes loaded documents, and writes back normalization deltas.
  - Return: {dict[str,object]} Normalized configuration document.
  - Throws: {OSError} If filesystem operations fail.
  - Throws: {ValueError} If existing JSON document has invalid structure.
  - Throws: {json.JSONDecodeError} If existing JSON file is syntactically invalid.
- fn `def save(self, document)` (L100-113)
  - Brief: Writes normalized JSON configuration to disk.
  - Details: Validates/normalizes payload, ensures parent directory exists, and serializes with deterministic indentation.
  - Param: document {dict[str,object]} Document payload to persist.
  - Return: {None} Performs filesystem writes.
  - Throws: {OSError} If write operation fails.
  - Throws: {ValueError} If payload has invalid structure.

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

# mainwindow.py | Python | 1379L | 89 symbols | 15 imports | 69 comments
> Path: `src/pdfframe/mainwindow.py`
- Brief: Main Qt window and interactive workflow for pdfframe.
- Details: Hosts viewer interactions, selection editing, settings persistence, and conversion orchestration.
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
from shutil import which
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

### class `class AspectRatioType` (L45-50)
- fn `def __init__(self, name, width, height)` `priv` (L46-50)

### class `class AspectRatioTypeManager` (L51-103)
- fn `def __init__(self)` `priv` (L53-56)
- fn `def __iter__(self)` `priv` (L57-59)
- fn `def addType(self, name, width, height)` (L60-62)
- fn `def getType(self, index)` (L63-67)
- fn `def addDefaults(self)` (L68-70)
- fn `def settingsCaption(self)` (L71-73)
- fn `def saveTypes(self, settings)` (L74-90)
- fn `def loadTypes(self, settings)` (L91-103)

### class `class SelAspectRatioTypeManager(AspectRatioTypeManager)` : AspectRatioTypeManager (L104-117)
- fn `def settingsCaption(self)` (L106-108)
- fn `def addDefaults(self)` (L109-117)

### class `class DeviceTypeManager(AspectRatioTypeManager)` : AspectRatioTypeManager (L118-130)
- fn `def settingsCaption(self)` (L120-122)
- fn `def addDefaults(self)` (L123-130)

### class `class MainWindow(QMainWindow)` : QMainWindow (L131-330)
- fn `def __init__(self)` `priv` (L135-249)
- fn `def viewer(self)` (L251-253)
- fn `def selections(self)` (L255-257)
- fn `def _toolbarIconFromAsset(self, filename, fallbackTheme)` `priv` (L258-270)
  - Brief: Resolves toolbar icon from bundled asset with fallback theme icon.
  - Details: Loads icon from `src/pdfframe/icons/<filename>` when available; otherwise returns `QIcon.fromTheme(<fallbackTheme>)`.
  - Param: filename {str} Bundled icon filename.
  - Param: fallbackTheme {str} Freedesktop theme-icon token.
  - Return: {QIcon} Toolbar icon object.
- fn `def _setupConversionModeControls(self)` `priv` (L271-288)
  - Brief: Adds conversion mode controls to the basic tab.
  - Details: Creates `Mode` group with `Frame` and `Crop` radio buttons, defaults to `Frame`, and inserts it into the basic-tab layout.
  - Return: {None} Applies UI side effects.
- fn `def _setupTrimSettingsControls(self)` `priv` (L289-299)
  - Brief: Relocates trim configuration controls into the Basic tab.
  - Details: Reuses the existing trim-settings group from the advanced UI definition, moves it to the bottom of the basic layout with all controls visible.
  - Return: {None} Applies UI side effects.

### fn `def _setupTrimPresetControls(self)` `priv` (L300-336)
- Brief: Adds dedicated Basic-tab trim preset controls.
- Details: Creates a standalone `Presets` group placed immediately after `Trim settings`, configures stretch/fixed columns so preset names fill row width up to the right-edge remove button, and wires apply/rename/delete flows.
- Return: {None} Applies UI side effects.

### fn `def _setupTrimPresetAction(self)` `priv` (L337-358)
- Brief: Adds the `Save Margins` toolbar action next to trim action.
- Details: Inserts a dedicated action directly to the right of `Trim Margins`, applies the dedicated `Save Margins` icon, then moves `Go!` to the far-right position immediately after `Save Margins`, and keeps preset-save action disabled until a PDF is loaded.
- Return: {None} Applies UI side effects.

### fn `def _trimPresetEditableFlag(self)` `priv` (L359-363)

### fn `def _trimPresetRole(self)` `priv` (L364-368)

### fn `def _defaultTrimPresetName(self)` `priv` (L369-376)
- Brief: Returns default trim preset name.
- Details: Generates timestamp name in `%Y/%m/%d %H:%M:%S` format.
- Return: {str} Default preset display label.

### fn `def _toBool(self, value)` `priv` (L377-387)
- Brief: Normalizes persisted boolean-like values.
- Details: Accepts bools and common string tokens produced by historical settings writers.
- Param: value {object} Input value from settings/config source.
- Return: {bool} Parsed boolean result.

### fn `def _updateTrimPagesRangeControls(self, enabled)` `priv` (L388-398)
- Brief: Updates `Pages range` control enabled state.
- Details: Enables range input only when trim-range mode is active and ensures default text `1-1` when empty.
- Param: enabled {bool} State propagated from trim-range toggle.
- Return: {None} Applies UI side effects.

### fn `def _parseTrimPagesRange(self)` `priv` (L399-415)
- Brief: Parses and validates the trim pages range expression.
- Details: Accepts only `N-M` one-based inclusive format, validates positive ordered bounds, and converts to zero-based bounds.
- Return: {tuple[int,int]} `(start_index, end_index)` inclusive zero-based page bounds.
- Throws: {ValueError} If the range is missing or syntactically/semantically invalid.

### fn `def _collectRuntimeConfigValues(self)` `priv` (L416-431)
- Brief: Collects runtime config values mapped to JSON `config` keys.
- Details: Converts current UI control state into serializable values for `~/.pdfframe/config.json`.
- Return: {dict[str,object]} Persistable runtime config key/value mapping.

### fn `def _preserveFieldsEnabled(self)` `priv` (L432-445)
- Brief: Returns Preserve fields option state.
- Details: Reads `checkPreserveFields` when available and normalizes truthy values for compatibility with test stubs.
- Return: {bool} True when `-dPreserveAnnots=true` must be emitted.

### fn `def _trimPresetFromCurrentSelection(self)` `priv` (L446-465)
- Brief: Creates a trim preset payload from current UI state.
- Details: Captures mode and trim parameters plus the primary current-page crop tuple when available.
- Return: {dict[str,object]} New preset payload ready for persistence.

### fn `def _refreshTrimPresetList(self)` `priv` (L466-494)
- Brief: Rebuilds trim preset tree rows from in-memory presets.
- Details: Clears the list, creates editable name rows, and attaches one remove button per row mapped to preset index inside a right-aligned cell container.
- Return: {None} Applies UI side effects.

### fn `def _persistTrimPresetDocument(self)` `priv` (L495-512)
- Brief: Persists runtime config and preset list to JSON config file.
- Details: Writes both `config` values and `presets` array through JsonConfigStore, surfacing warning on I/O failures.
- Return: {None} Writes `~/.pdfframe/config.json`.

### fn `def _applyCropPreset(self, crop_values)` `priv` (L513-544)
- Brief: Applies normalized crop tuple to current selection.
- Details: Maps `[left,top,right,bottom]` normalized margins to viewer coordinates and updates (or creates) the current selection.
- Param: crop_values {list[float]} Normalized crop tuple values.
- Return: {None} Mutates current selection geometry.

### fn `def _applyTrimPreset(self, index)` `priv` (L545-570)
- Brief: Applies one stored preset to current runtime controls.
- Details: Restores mode and trim values, then applies saved crop tuple when present.
- Param: index {int} Preset list index.
- Return: {None} Applies UI and selection updates.

### fn `def slotTrimPresetClicked(self, item, column)` (L571-583)
- Brief: Applies a preset when the preset name cell is clicked.
- Details: Ignores delete-button column and list rebuild events.
- Param: item {QTreeWidgetItem} Clicked row item.
- Param: column {int} Clicked column index.
- Return: {None} Applies preset side effects.

### fn `def slotTrimPresetDoubleClicked(self, item, column)` (L584-594)
- Brief: Starts inline rename for preset names.
- Details: Enables user-driven preset rename on double-click of first column.
- Param: item {QTreeWidgetItem} Double-clicked row item.
- Param: column {int} Double-clicked column index.
- Return: {None} Opens in-place editor.

### fn `def slotTrimPresetChanged(self, item, column)` (L595-618)
- Brief: Persists preset rename changes from inline editing.
- Details: Normalizes empty labels to timestamp defaults and rewrites JSON config after updates.
- Param: item {QTreeWidgetItem} Changed row item.
- Param: column {int} Changed column index.
- Return: {None} Persists preset list updates.

### fn `def slotDeleteTrimPreset(self)` (L619-637)
- Brief: Deletes one preset from remove-button click.
- Details: Resolves row index from sender button metadata, updates in-memory list, refreshes UI, and persists JSON state.
- Return: {None} Applies preset delete side effects.

### fn `def slotSaveMarginsPreset(self)` (L638-649)
- Brief: Saves current crop/trim state as a new preset.
- Details: Captures active control values, appends new preset with timestamp default name, refreshes list, and persists JSON state.
- Return: {None} Applies preset creation side effects.

### fn `def selectedConversionMode(self)` (L650-657)
- Brief: Returns selected conversion mode for Ghostscript execution.
- Details: Maps GUI mode controls to backend mode tokens expected by command generation.
- Return: {str} Conversion mode token (`frame` or `crop`).

### fn `def currentSelectionUpdated(self)` (L658-674)

### fn `def _updateSelectionCreationActions(self)` `priv` (L675-684)
- Brief: Updates enablement of selection-creation actions.
- Details: Allows creating a selection only when the viewer has a document and no selection exists; keeps creation actions disabled once one selection area is present.
- Return: {None} Applies action-enable side effects.

### fn `def readSettings(self)` (L685-733)
- Brief: Reads persisted runtime settings from QSettings and JSON config.
- Details: Restores window geometry from QSettings, loads trim/runtime defaults from `~/.pdfframe/config.json`, and refreshes preset UI entries.
- Return: {None} Applies UI state restoration side effects.

### fn `def writeSettings(self)` (L734-758)
- Brief: Persists runtime settings to legacy and JSON backends.
- Details: Writes window/session metadata to QSettings and writes trim/runtime config plus presets to `~/.pdfframe/config.json`.
- Return: {None} Persists runtime state.

### fn `def openFile(self, fileName)` (L759-779)

### fn `def slotOpenFile(self)` (L780-785)

### fn `def slotSelectFile(self)` (L786-795)

### fn `def showWarning(self, title, text)` (L796-803)

### fn `def str2pages(self, s)` (L804-821)

### fn `def primarySelectionCropValue(self, page_indexes)` (L822-835)
- Brief: Gets primary selection crop tuple for conversion planning.
- Details: Resolves first available normalized crop tuple from current page first, then requested pages, and returns only the primary tuple used for all output pages.
- Param: page_indexes {list[int]} Ordered page indexes selected for processing.
- Return: {tuple[float,float,float,float]|None} Primary normalized crop tuple or None when no selections are available.

### fn `def buildGhostscriptCropPlan(self, inputFileName, outputFileName, requestedPageIndexes=None)` (L836-871)
- Brief: Builds single Ghostscript crop plan from GUI-derived parameters.
- Details: Iterates only requested pages (or all pages when omitted), derives geometry from the primary GUI selection tuple, computes crop bbox from page-size metadata, and emits one Ghostscript command for the full selected range using `-dFirstPage/-dLastPage` plus preserve-fields flag state.
- Param: inputFileName {str} Source PDF path.
- Param: outputFileName {str} Destination cropped PDF path.
- Param: requestedPageIndexes {set[int]|None} Optional zero-based page-index filter derived from `--whichpages`.
- Return: {dict[str,object]|None} Crop plan containing selected page indexes and one Ghostscript command vector.

### fn `def createConversionProgressDialog(self, totalPages)` (L872-894)
- Brief: Creates modal conversion progress dialog for crop execution.
- Details: Configures progress dialog with deterministic page range and cancellable stop action used during long-running conversion command execution.
- Param: totalPages {int} Number of selected pages to process.
- Return: {QProgressDialog} Configured progress dialog instance.

### fn `def slotPdfFrame(self)` (L895-1017)
- Brief: Executes PDF crop action using Ghostscript command backend.
- Details: Verifies Ghostscript availability, builds one Ghostscript crop command from GUI state, and streams command output to update conversion progress across the selected page range.
- Return: {None} Triggers output PDF generation side effect.

### fn `def mark_page_processed(page_number)` (L949-967)
- Brief: Executes PDF crop action using Ghostscript command backend.
- Brief: Marks one selected page as processed for progress updates.
- Details: Verifies Ghostscript availability, builds one Ghostscript crop command from GUI state, and streams command output to update conversion progress across the selected page range.
- Details: Updates dialog value and label only once per page number to keep deterministic monotonic progress during streamed subprocess output handling.
- Param: page_number {int} One-based page number reported by Ghostscript.
- Return: {None} Triggers output PDF generation side effect.
- Return: {None} Applies progress side effects.

### fn `def on_output_line(line)` (L968-982)
- Brief: Processes streamed Ghostscript output lines during conversion.
- Details: Uses parsed Ghostscript page numbers from captured output to advance conversion progress without forwarding captured command output to user-visible UI messages.
- Param: line {str} Single output line emitted by Ghostscript.
- Return: {None} Applies progress side effects.

### fn `def slotZoomIn(self)` (L1018-1021)

### fn `def slotZoomOut(self)` (L1022-1025)

### fn `def slotFitInView(self, checked)` (L1026-1030)

### fn `def slotSplitterMoved(self, pos, idx)` (L1031-1033)

### fn `def slotPreviousPage(self)` (L1034-1037)

### fn `def slotNextPage(self)` (L1038-1041)

### fn `def slotFirstPage(self)` (L1042-1045)

### fn `def slotLastPage(self)` (L1046-1049)

### fn `def slotCurrentPageEdited(self, text)` (L1050-1057)

### fn `def updateControls(self)` (L1058-1066)

### fn `def slotSelectionMode(self, checked)` (L1067-1070)

### fn `def slotSelExceptionsChanged(self)` (L1071-1073)

### fn `def slotSelExceptionsEdited(self, text)` (L1074-1078)

### fn `def slotSelAspectRatioChanged(self)` (L1079-1087)

### fn `def slotSelAspectRatioTypeChanged(self, index)` (L1088-1107)

### fn `def distributeAspectRatioChanged(self, aspectRatio)` (L1108-1110)

### fn `def slotDistributeAspectRatioChanged(self)` (L1111-1113)

### fn `def slotDeviceTypeChanged(self, index)` (L1114-1120)

### fn `def slotContextMenu(self, pos)` (L1121-1141)

### fn `def slotDeleteSelection(self)` (L1142-1145)

### fn `def slotNewSelection(self)` (L1146-1148)

### fn `def slotNewSelectionGrid(self)` (L1149-1167)
- Brief: Requests one new trim/selection area from user grid input.
- Details: Prompts only when no selection area exists; in single-selection mode the request is rejected while an area is already present.
- Return: {None} Applies selection-creation side effects.

### fn `def createSelectionGrid(self, grid)` (L1168-1224)
- Brief: Creates the initial trim/selection area from grid input.
- Details: Parses `grid` input, enforces single-selection mode by reducing multi-cell requests to one area, and prevents creation when an area already exists.
- Param: grid {str} Grid expression entered by CLI or UI.
- Return: {None} Applies selection-creation side effects.

### fn `def getPadding(self)` (L1225-1252)
- Brief: Returns trim padding in CSS-expanded order.
- Details: Reads trim padding text from the dedicated Basic-tab controls and expands one-to-four comma-separated values to `[top,right,bottom,left]`.
- Return: {list[float]} Padding tuple in top,right,bottom,left order.

### fn `def slotTrimMarginsAll(self)` (L1253-1265)

### fn `def slotTrimMargins(self)` (L1266-1270)

### fn `def trimMarginsSelection(self, sel)` (L1271-1374)
- Brief: Computes auto-trim rectangle for a selection using configured thresholds.
- Details: Reads color-sensitivity and grayscale-sensitivity values from Basic-tab controls, selects page scope using current page by default or a validated `Pages range` slice of visible pages when range mode is enabled, and applies auto-trim with padding and aspect-ratio adjustments.
- Param: sel {ViewerSelectionItem} Selection item to trim.
- Return: {None} Mutates selection bounding rectangle.

### fn `def resizeEvent(self, event)` (L1375-1377)

### fn `def closeEvent(self, event)` (L1378-1379)

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`AspectRatioType`|class|pub|45-50|class AspectRatioType|
|`AspectRatioType.__init__`|fn|priv|46-50|def __init__(self, name, width, height)|
|`AspectRatioTypeManager`|class|pub|51-103|class AspectRatioTypeManager|
|`AspectRatioTypeManager.__init__`|fn|priv|53-56|def __init__(self)|
|`AspectRatioTypeManager.__iter__`|fn|priv|57-59|def __iter__(self)|
|`AspectRatioTypeManager.addType`|fn|pub|60-62|def addType(self, name, width, height)|
|`AspectRatioTypeManager.getType`|fn|pub|63-67|def getType(self, index)|
|`AspectRatioTypeManager.addDefaults`|fn|pub|68-70|def addDefaults(self)|
|`AspectRatioTypeManager.settingsCaption`|fn|pub|71-73|def settingsCaption(self)|
|`AspectRatioTypeManager.saveTypes`|fn|pub|74-90|def saveTypes(self, settings)|
|`AspectRatioTypeManager.loadTypes`|fn|pub|91-103|def loadTypes(self, settings)|
|`SelAspectRatioTypeManager`|class|pub|104-117|class SelAspectRatioTypeManager(AspectRatioTypeManager)|
|`SelAspectRatioTypeManager.settingsCaption`|fn|pub|106-108|def settingsCaption(self)|
|`SelAspectRatioTypeManager.addDefaults`|fn|pub|109-117|def addDefaults(self)|
|`DeviceTypeManager`|class|pub|118-130|class DeviceTypeManager(AspectRatioTypeManager)|
|`DeviceTypeManager.settingsCaption`|fn|pub|120-122|def settingsCaption(self)|
|`DeviceTypeManager.addDefaults`|fn|pub|123-130|def addDefaults(self)|
|`MainWindow`|class|pub|131-330|class MainWindow(QMainWindow)|
|`MainWindow.__init__`|fn|priv|135-249|def __init__(self)|
|`MainWindow.viewer`|fn|pub|251-253|def viewer(self)|
|`MainWindow.selections`|fn|pub|255-257|def selections(self)|
|`MainWindow._toolbarIconFromAsset`|fn|priv|258-270|def _toolbarIconFromAsset(self, filename, fallbackTheme)|
|`MainWindow._setupConversionModeControls`|fn|priv|271-288|def _setupConversionModeControls(self)|
|`MainWindow._setupTrimSettingsControls`|fn|priv|289-299|def _setupTrimSettingsControls(self)|
|`_setupTrimPresetControls`|fn|priv|300-336|def _setupTrimPresetControls(self)|
|`_setupTrimPresetAction`|fn|priv|337-358|def _setupTrimPresetAction(self)|
|`_trimPresetEditableFlag`|fn|priv|359-363|def _trimPresetEditableFlag(self)|
|`_trimPresetRole`|fn|priv|364-368|def _trimPresetRole(self)|
|`_defaultTrimPresetName`|fn|priv|369-376|def _defaultTrimPresetName(self)|
|`_toBool`|fn|priv|377-387|def _toBool(self, value)|
|`_updateTrimPagesRangeControls`|fn|priv|388-398|def _updateTrimPagesRangeControls(self, enabled)|
|`_parseTrimPagesRange`|fn|priv|399-415|def _parseTrimPagesRange(self)|
|`_collectRuntimeConfigValues`|fn|priv|416-431|def _collectRuntimeConfigValues(self)|
|`_preserveFieldsEnabled`|fn|priv|432-445|def _preserveFieldsEnabled(self)|
|`_trimPresetFromCurrentSelection`|fn|priv|446-465|def _trimPresetFromCurrentSelection(self)|
|`_refreshTrimPresetList`|fn|priv|466-494|def _refreshTrimPresetList(self)|
|`_persistTrimPresetDocument`|fn|priv|495-512|def _persistTrimPresetDocument(self)|
|`_applyCropPreset`|fn|priv|513-544|def _applyCropPreset(self, crop_values)|
|`_applyTrimPreset`|fn|priv|545-570|def _applyTrimPreset(self, index)|
|`slotTrimPresetClicked`|fn|pub|571-583|def slotTrimPresetClicked(self, item, column)|
|`slotTrimPresetDoubleClicked`|fn|pub|584-594|def slotTrimPresetDoubleClicked(self, item, column)|
|`slotTrimPresetChanged`|fn|pub|595-618|def slotTrimPresetChanged(self, item, column)|
|`slotDeleteTrimPreset`|fn|pub|619-637|def slotDeleteTrimPreset(self)|
|`slotSaveMarginsPreset`|fn|pub|638-649|def slotSaveMarginsPreset(self)|
|`selectedConversionMode`|fn|pub|650-657|def selectedConversionMode(self)|
|`currentSelectionUpdated`|fn|pub|658-674|def currentSelectionUpdated(self)|
|`_updateSelectionCreationActions`|fn|priv|675-684|def _updateSelectionCreationActions(self)|
|`readSettings`|fn|pub|685-733|def readSettings(self)|
|`writeSettings`|fn|pub|734-758|def writeSettings(self)|
|`openFile`|fn|pub|759-779|def openFile(self, fileName)|
|`slotOpenFile`|fn|pub|780-785|def slotOpenFile(self)|
|`slotSelectFile`|fn|pub|786-795|def slotSelectFile(self)|
|`showWarning`|fn|pub|796-803|def showWarning(self, title, text)|
|`str2pages`|fn|pub|804-821|def str2pages(self, s)|
|`primarySelectionCropValue`|fn|pub|822-835|def primarySelectionCropValue(self, page_indexes)|
|`buildGhostscriptCropPlan`|fn|pub|836-871|def buildGhostscriptCropPlan(self, inputFileName, outputF...|
|`createConversionProgressDialog`|fn|pub|872-894|def createConversionProgressDialog(self, totalPages)|
|`slotPdfFrame`|fn|pub|895-1017|def slotPdfFrame(self)|
|`mark_page_processed`|fn|pub|949-967|def mark_page_processed(page_number)|
|`on_output_line`|fn|pub|968-982|def on_output_line(line)|
|`slotZoomIn`|fn|pub|1018-1021|def slotZoomIn(self)|
|`slotZoomOut`|fn|pub|1022-1025|def slotZoomOut(self)|
|`slotFitInView`|fn|pub|1026-1030|def slotFitInView(self, checked)|
|`slotSplitterMoved`|fn|pub|1031-1033|def slotSplitterMoved(self, pos, idx)|
|`slotPreviousPage`|fn|pub|1034-1037|def slotPreviousPage(self)|
|`slotNextPage`|fn|pub|1038-1041|def slotNextPage(self)|
|`slotFirstPage`|fn|pub|1042-1045|def slotFirstPage(self)|
|`slotLastPage`|fn|pub|1046-1049|def slotLastPage(self)|
|`slotCurrentPageEdited`|fn|pub|1050-1057|def slotCurrentPageEdited(self, text)|
|`updateControls`|fn|pub|1058-1066|def updateControls(self)|
|`slotSelectionMode`|fn|pub|1067-1070|def slotSelectionMode(self, checked)|
|`slotSelExceptionsChanged`|fn|pub|1071-1073|def slotSelExceptionsChanged(self)|
|`slotSelExceptionsEdited`|fn|pub|1074-1078|def slotSelExceptionsEdited(self, text)|
|`slotSelAspectRatioChanged`|fn|pub|1079-1087|def slotSelAspectRatioChanged(self)|
|`slotSelAspectRatioTypeChanged`|fn|pub|1088-1107|def slotSelAspectRatioTypeChanged(self, index)|
|`distributeAspectRatioChanged`|fn|pub|1108-1110|def distributeAspectRatioChanged(self, aspectRatio)|
|`slotDistributeAspectRatioChanged`|fn|pub|1111-1113|def slotDistributeAspectRatioChanged(self)|
|`slotDeviceTypeChanged`|fn|pub|1114-1120|def slotDeviceTypeChanged(self, index)|
|`slotContextMenu`|fn|pub|1121-1141|def slotContextMenu(self, pos)|
|`slotDeleteSelection`|fn|pub|1142-1145|def slotDeleteSelection(self)|
|`slotNewSelection`|fn|pub|1146-1148|def slotNewSelection(self)|
|`slotNewSelectionGrid`|fn|pub|1149-1167|def slotNewSelectionGrid(self)|
|`createSelectionGrid`|fn|pub|1168-1224|def createSelectionGrid(self, grid)|
|`getPadding`|fn|pub|1225-1252|def getPadding(self)|
|`slotTrimMarginsAll`|fn|pub|1253-1265|def slotTrimMarginsAll(self)|
|`slotTrimMargins`|fn|pub|1266-1270|def slotTrimMargins(self)|
|`trimMarginsSelection`|fn|pub|1271-1374|def trimMarginsSelection(self, sel)|
|`resizeEvent`|fn|pub|1375-1377|def resizeEvent(self, event)|
|`closeEvent`|fn|pub|1378-1379|def closeEvent(self, event)|


---

# mainwindowui_qt5.py | Python | 479L | 3 symbols | 1 imports | 12 comments
> Path: `src/pdfframe/mainwindowui_qt5.py`
- Brief: PyQt5-generated UI bindings for `MainWindow`.
- Details: Source generated from `mainwindow.ui`; manual edits are restricted to static-analysis metadata.

## Imports
```
from PyQt5 import QtCore, QtWidgets
```

## Definitions

### class `class Ui_MainWindow(object)` : object (L21-220)
- Brief: Contains generated widget wiring for the main application window.

### fn `def setupUi(self, MainWindow)` (L26-225)
- Brief: Contains generated widget wiring for the main application window.
- Brief: Creates widgets, layouts, and signal connections for `MainWindow`.
- Param: MainWindow {QtWidgets.QMainWindow} Target window instance.
- Return: {None} Applies generated UI graph.

### fn `def retranslateUi(self, MainWindow)` (L388-402)
- Brief: Applies translatable UI strings to generated widgets.
- Param: MainWindow {QtWidgets.QMainWindow} Target window instance.
- Return: {None} Updates texts/tooltips/actions.

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`Ui_MainWindow`|class|pub|21-220|class Ui_MainWindow(object)|
|`setupUi`|fn|pub|26-225|def setupUi(self, MainWindow)|
|`retranslateUi`|fn|pub|388-402|def retranslateUi(self, MainWindow)|


---

# mainwindowui_qt6.py | Python | 477L | 3 symbols | 1 imports | 12 comments
> Path: `src/pdfframe/mainwindowui_qt6.py`
- Brief: PyQt6-generated UI bindings for `MainWindow`.
- Details: Source generated from `mainwindow.ui`; manual edits are restricted to static-analysis metadata.

## Imports
```
from PyQt6 import QtCore, QtGui, QtWidgets
```

## Definitions

### class `class Ui_MainWindow(object)` : object (L19-218)
- Brief: Contains generated widget wiring for the main application window.

### fn `def setupUi(self, MainWindow)` (L24-223)
- Brief: Contains generated widget wiring for the main application window.
- Brief: Creates widgets, layouts, and signal connections for `MainWindow`.
- Param: MainWindow {QtWidgets.QMainWindow} Target window instance.
- Return: {None} Applies generated UI graph.

### fn `def retranslateUi(self, MainWindow)` (L386-400)
- Brief: Applies translatable UI strings to generated widgets.
- Param: MainWindow {QtWidgets.QMainWindow} Target window instance.
- Return: {None} Updates texts/tooltips/actions.

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`Ui_MainWindow`|class|pub|19-218|class Ui_MainWindow(object)|
|`setupUi`|fn|pub|24-223|def setupUi(self, MainWindow)|
|`retranslateUi`|fn|pub|386-400|def retranslateUi(self, MainWindow)|


---

# pdfframecmd.py | Python | 368L | 16 symbols | 8 imports | 15 comments
> Path: `src/pdfframe/pdfframecmd.py`

## Imports
```
import importlib
import queue
import re
import shlex
import subprocess
import sys
import threading
import time
```

## Definitions

### class `class GhostscriptCommandError(RuntimeError)` : RuntimeError (L23-41)
- Brief: Represents a failed Ghostscript subprocess execution.
- Details: Encapsulates command vector, return code, and captured streams so caller code can emit deterministic diagnostics for GUI and terminal paths.
- Param: command {list[str]} Executed command vector passed to subprocess.
- Param: returncode {int} Process exit code returned by subprocess.
- Param: stdout {str} Captured standard output text.
- Param: stderr {str} Captured standard error text.
- Return: {None} Constructs exception payload and error message.
- fn `def __init__(self, command, returncode, stdout, stderr)` `priv` (L34-41)
  - Brief: Represents a failed Ghostscript subprocess execution.
  - Details: Encapsulates command vector, return code, and captured streams so caller code can emit deterministic diagnostics for GUI and terminal paths.
  - Param: command {list[str]} Executed command vector passed to subprocess.
  - Param: returncode {int} Process exit code returned by subprocess.
  - Param: stdout {str} Captured standard output text.
  - Param: stderr {str} Captured standard error text.
  - Return: {None} Constructs exception payload and error message.

### class `class GhostscriptCommandCancelledError(RuntimeError)` : RuntimeError (L42-56)
- Brief: Represents user-requested cancellation of Ghostscript execution.
- Details: Encapsulates executed command and partial output captured before termination so caller code can report deterministic cancellation diagnostics.
- Param: command {list[str]} Executed command vector passed to subprocess.
- Param: stdout {str} Partial captured standard output text.
- Return: {None} Constructs exception payload and error message.
- fn `def __init__(self, command, stdout)` `priv` (L51-56)
  - Brief: Represents user-requested cancellation of Ghostscript execution.
  - Details: Encapsulates executed command and partial output captured before termination so caller code can report deterministic cancellation diagnostics.
  - Param: command {list[str]} Executed command vector passed to subprocess.
  - Param: stdout {str} Partial captured standard output text.
  - Return: {None} Constructs exception payload and error message.

### fn `def _format_scalar(value)` `priv` (L57-70)
- Brief: Converts numeric values to stable CLI scalar strings.
- Details: Emits integer-like values without decimal suffix and non-integers with compact decimal representation to keep generated command arguments deterministic for tests.
- Param: value {float|int} Numeric value to format.
- Return: {str} Stable scalar representation for CLI arguments.

### fn `def padding_to_crop_offsets(padding)` (L71-85)
- Brief: Reorders GUI padding vector to crop-offset order.
- Details: Converts GUI tuple [top, right, bottom, left] to crop-offset tuple [left, top, right, bottom] for deterministic crop-box expansion.
- Param: padding {list[float]|tuple[float,float,float,float]} GUI padding vector with exactly four components.
- Return: {tuple[float,float,float,float]} Crop-offset tuple ordered as left, top, right, bottom.
- Throws: {ValueError} If padding vector does not contain exactly four values.

### fn `def crop_values_to_bbox(crop_values, page_width, page_height)` (L86-116)
- Brief: Converts normalized selection crop values to absolute page-space crop box.
- Details: Merges all visible normalized crops into one union box by first converting each GUI-derived normalized crop tuple to CropBox LL/UR page-space coordinates and then taking bounding extents in left,bottom,right,top order.
- Param: crop_values {list[tuple[float,float,float,float]]} Normalized crop tuples (left, top, right, bottom).
- Param: page_width {float} Page width in points.
- Param: page_height {float} Page height in points.
- Return: {tuple[float,float,float,float]|None} Crop box tuple or None when no crop values exist.
- Throws: {ValueError} If page dimensions are non-positive.

### fn `def normalized_crop_tuple_to_bbox(crop_value, page_width, page_height)` (L117-139)
- Brief: Converts one normalized GUI crop tuple into page-point CropBox coordinates.
- Details: Maps normalized GUI tuple `(left, top, right_margin, bottom_margin)` to CropBox corners `(LLx, LLy, URx, URy)` in page-point space with lower-left PDF origin.
- Param: crop_value {tuple[float,float,float,float]} Normalized GUI crop tuple.
- Param: page_width {float} Page width in points.
- Param: page_height {float} Page height in points.
- Return: {tuple[float,float,float,float]} CropBox coordinates in left,bottom,right,top order.
- Throws: {ValueError} If resulting CropBox is empty.

### fn `def apply_crop_offsets_to_bbox(bbox, offsets, page_width, page_height)` (L140-165)
- Brief: Applies GUI crop offsets to an absolute crop box.
- Details: Expands or shrinks the crop box by offsets in left,top,right,bottom order and clamps the resulting box to page bounds.
- Param: bbox {tuple[float,float,float,float]} Input crop box in left,bottom,right,top order.
- Param: offsets {tuple[float,float,float,float]} Crop offsets in left,top,right,bottom order.
- Param: page_width {float} Page width in points.
- Param: page_height {float} Page height in points.
- Return: {tuple[float,float,float,float]} Adjusted crop box in left,bottom,right,top order.
- Throws: {ValueError} If resulting crop box is empty after clamping.

### fn `def build_ghostscript_page_crop_command(input_path, output_path, first_page,` (L166-238)

### fn `def extract_ghostscript_page_numbers(line)` (L239-250)
- Brief: Extracts all processed page indices from Ghostscript output text.
- Details: Parses each output line that matches `^Page\\s+\\d+\\n` in the provided chunk and returns one-based page numbers in encounter order.
- Param: line {str} One output line or chunk produced by Ghostscript.
- Return: {list[int]} Processed page numbers found in the chunk.

### fn `def extract_ghostscript_page_number(line)` (L251-264)
- Brief: Extracts processed page index from Ghostscript output lines.
- Details: Parses `Page N` line format emitted by Ghostscript and returns one-based page number when a match is present.
- Param: line {str} One output line produced by Ghostscript.
- Return: {int|None} Processed page number or None when line does not contain page progress information.

### fn `def format_shell_command(command)` (L265-275)
- Brief: Formats command vectors into deterministic shell-escaped strings.
- Details: Serializes subprocess command vectors with POSIX shell escaping to provide exact reproducible command diagnostics.
- Param: command {list[str]} Subprocess command vector.
- Return: {str} Shell-escaped command string preserving argument boundaries.

### fn `def write_cropped_pages_output(output_file_name, cropped_page_paths)` (L276-298)
- Brief: Writes output PDF using only selected cropped page files.
- Details: Loads one-page cropped PDF files in provided order and writes a new output PDF that contains exactly those pages.
- Param: output_file_name {str} Destination PDF file path.
- Param: cropped_page_paths {list[str]} Ordered one-page cropped PDF paths selected for export.
- Return: {None} Writes assembled output PDF to filesystem.
- Throws: {ValueError} If no cropped pages are provided.

### fn `def run_ghostscript_command(command, event_pump=None, poll_interval=0.05,` (L299-368)
- Brief: Executes Ghostscript and captures subprocess output streams.
- Details: Runs subprocess in text mode, captures output for deterministic diagnostics, optionally streams output lines through a callback, optionally pumps UI events while process is running, and supports user-requested cancellation.
- Param: command {list[str]} Complete subprocess command vector.
- Param: event_pump {callable|None} Optional callback invoked repeatedly while subprocess execution is in progress.
- Param: poll_interval {float} Seconds to wait between event-pump cycles when callback mode is enabled.
- Param: output_callback {callable|None} Optional callback receiving each streamed output line.
- Param: cancel_requested {callable|None} Optional callback returning True when subprocess should be cancelled.
- Param: log_command {bool} When True, prints the shell-escaped command line before execution.
- Param: debug_output {bool} When True, prints captured Ghostscript output to stderr while preserving capture behavior.
- Return: {subprocess.CompletedProcess[str]} Successful subprocess result with captured streams.
- Throws: {GhostscriptCommandError} If Ghostscript exits with non-zero status.
- Throws: {GhostscriptCommandCancelledError} If cancellation callback requests process termination.

### fn `def reader()` (L328-335)
- Brief: Executes Ghostscript and captures subprocess output streams.
- Details: Runs subprocess in text mode, captures output for deterministic diagnostics, optionally streams output lines through a callback, optionally pumps UI events while process is running, and supports user-requested cancellation.
- Param: command {list[str]} Complete subprocess command vector.
- Param: event_pump {callable|None} Optional callback invoked repeatedly while subprocess execution is in progress.
- Param: poll_interval {float} Seconds to wait between event-pump cycles when callback mode is enabled.
- Param: output_callback {callable|None} Optional callback receiving each streamed output line.
- Param: cancel_requested {callable|None} Optional callback returning True when subprocess should be cancelled.
- Param: log_command {bool} When True, prints the shell-escaped command line before execution.
- Param: debug_output {bool} When True, prints captured Ghostscript output to stderr while preserving capture behavior.
- Return: {subprocess.CompletedProcess[str]} Successful subprocess result with captured streams.
- Throws: {GhostscriptCommandError} If Ghostscript exits with non-zero status.
- Throws: {GhostscriptCommandCancelledError} If cancellation callback requests process termination.

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`GhostscriptCommandError`|class|pub|23-41|class GhostscriptCommandError(RuntimeError)|
|`GhostscriptCommandError.__init__`|fn|priv|34-41|def __init__(self, command, returncode, stdout, stderr)|
|`GhostscriptCommandCancelledError`|class|pub|42-56|class GhostscriptCommandCancelledError(RuntimeError)|
|`GhostscriptCommandCancelledError.__init__`|fn|priv|51-56|def __init__(self, command, stdout)|
|`_format_scalar`|fn|priv|57-70|def _format_scalar(value)|
|`padding_to_crop_offsets`|fn|pub|71-85|def padding_to_crop_offsets(padding)|
|`crop_values_to_bbox`|fn|pub|86-116|def crop_values_to_bbox(crop_values, page_width, page_hei...|
|`normalized_crop_tuple_to_bbox`|fn|pub|117-139|def normalized_crop_tuple_to_bbox(crop_value, page_width,...|
|`apply_crop_offsets_to_bbox`|fn|pub|140-165|def apply_crop_offsets_to_bbox(bbox, offsets, page_width,...|
|`build_ghostscript_page_crop_command`|fn|pub|166-238|def build_ghostscript_page_crop_command(input_path, outpu...|
|`extract_ghostscript_page_numbers`|fn|pub|239-250|def extract_ghostscript_page_numbers(line)|
|`extract_ghostscript_page_number`|fn|pub|251-264|def extract_ghostscript_page_number(line)|
|`format_shell_command`|fn|pub|265-275|def format_shell_command(command)|
|`write_cropped_pages_output`|fn|pub|276-298|def write_cropped_pages_output(output_file_name, cropped_...|
|`run_ghostscript_command`|fn|pub|299-368|def run_ghostscript_command(command, event_pump=None, pol...|
|`reader`|fn|pub|328-335|def reader()|


---

# pdfframeper.py | Python | 327L | 62 symbols | 10 imports | 43 comments
> Path: `src/pdfframe/pdfframeper.py`
- Brief: PDF backend adapters for loading and writing cropped documents.
- Details: Provides wrapper classes over pypdf, PyPDF2, PyMuPDF, and pikepdf for unified crop operations.
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
import subprocess
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

### fn `def computeCropBoxCoords(box, crop, pdf_coords=True)` (L238-248)

### fn `def optimizePdfGhostscript(oldfilename, newfilename)` (L249-254)

### fn `def import_pymupdf()` (L258-265)

### fn `def import_pikepdf()` (L266-271)

### fn `def import_pypdf()` (L272-277)

### fn `def import_pypdf2()` (L278-292)

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
|`computeCropBoxCoords`|fn|pub|238-248|def computeCropBoxCoords(box, crop, pdf_coords=True)|
|`optimizePdfGhostscript`|fn|pub|249-254|def optimizePdfGhostscript(oldfilename, newfilename)|
|`import_pymupdf`|fn|pub|258-265|def import_pymupdf()|
|`import_pikepdf`|fn|pub|266-271|def import_pikepdf()|
|`import_pypdf`|fn|pub|272-277|def import_pypdf()|
|`import_pypdf2`|fn|pub|278-292|def import_pypdf2()|


---

# qt.py | Python | 18L | 0 symbols | 7 imports | 3 comments
> Path: `src/pdfframe/qt.py`
- Brief: Unified Qt symbol export layer for PyQt6/PyQt5 compatibility.
- Details: Re-exports QtCore/QtGui/QtWidgets symbols based on runtime backend selection.

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
- Brief: Viewer backends and rendering abstractions for PDF page display.
- Details: Implements Qt graphics-item viewer classes for Poppler and PyMuPDF rendering backends.
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
  - Brief: Returns page size for bbox conversion when backend metadata is unavailable.
  - Details: Uses rendered image dimensions as fallback point-like units for callers that require non-zero geometry values.
  - Param: idx {int} Zero-based page index.
  - Return: {tuple[float,float]} Width and height pair.
- fn `def cropValues(self, idx)` (L147-161)
- fn `def adjustForOrientation(cv)` (L148-156)

### class `class PopplerViewerItem(AbstractViewerItem)` : AbstractViewerItem (L162-210)
- fn `def reset(self)` (L164-167)
- fn `def doLoad(self, filename)` (L168-173)
- fn `def numPages(self)` (L174-179)
- fn `def cacheImage(self, idx)` (L180-184)
- fn `def pageGetRotation(self, idx)` (L185-196)
- fn `def pageGetSizePoints(self, idx)` (L197-210)
  - Brief: Returns Poppler page size in point units.
  - Details: Queries Poppler page metadata and exposes width/height values used by command-backend crop-box generation logic.
  - Param: idx {int} Zero-based page index.
  - Return: {tuple[float,float]} Width and height pair in points.

### class `class MuPDFViewerItem(AbstractViewerItem)` : AbstractViewerItem (L211-255)
- fn `def reset(self)` (L213-216)
- fn `def doLoad(self, filename)` (L217-222)
- fn `def numPages(self)` (L223-228)
- fn `def cacheImage(self, idx)` (L229-239)
- fn `def pageGetRotation(self, idx)` (L240-243)
- fn `def pageGetSizePoints(self, idx)` (L244-255)
  - Brief: Returns MuPDF media-box dimensions in point units.
  - Details: Reads page media-box coordinates and provides width/height for deterministic bbox conversion in command-based cropping.
  - Param: idx {int} Zero-based page index.
  - Return: {tuple[float,float]} Width and height pair in points.

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
- Brief: Interactive selection items and gestures used by viewer backends.
- Details: Defines selection geometry, resize handles, and mouse-driven edit behavior in scene coordinates.
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
  - Brief: Creates the selection area when absent.
  - Details: Enforces single-selection mode by returning the existing area when one is already present.
  - Param: rect {QRectF|None} Optional initial rectangle for first creation.
  - Return: {ViewerSelectionItem} Current selection area.
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
  - Brief: Starts scene-level selection creation gesture.
  - Details: Creates a first selection on left click only when no selection exists; otherwise keeps the existing area current.
  - Param: event {QGraphicsSceneMouseEvent} Mouse event object.
  - Return: {None} Applies selection creation side effects.
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

