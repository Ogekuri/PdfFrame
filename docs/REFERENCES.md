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

# application.py | Python | 102L | 1 symbols | 7 imports | 7 comments
> Path: `src/pdfframe/application.py`

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

### fn `def main()` (L27-102)

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`main`|fn|pub|27-102|def main()|


---

# autotrim.py | Python | 73L | 3 symbols | 1 imports | 6 comments
> Path: `src/pdfframe/autotrim.py`

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

# config.py | Python | 17L | 2 symbols | 3 imports | 1 comments
> Path: `src/pdfframe/config.py`

## Imports
```
import sys
from PyQt6 import QtCore
from PyQt5 import QtCore
```

## Definitions

- var `PYQT6 = False` (L3)
- var `PYQT6 = True` (L10)
## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`PYQT6`|var|pub|3||
|`PYQT6`|var|pub|10||


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

# mainwindow.py | Python | 1315L | 87 symbols | 14 imports | 64 comments
> Path: `src/pdfframe/mainwindow.py`

## Imports
```
import sys
import re
from datetime import datetime
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

### class `class AspectRatioType` (L44-49)
- fn `def __init__(self, name, width, height)` `priv` (L45-49)

### class `class AspectRatioTypeManager` (L50-102)
- fn `def __init__(self)` `priv` (L52-55)
- fn `def __iter__(self)` `priv` (L56-58)
- fn `def addType(self, name, width, height)` (L59-61)
- fn `def getType(self, index)` (L62-66)
- fn `def addDefaults(self)` (L67-69)
- fn `def settingsCaption(self)` (L70-72)
- fn `def saveTypes(self, settings)` (L73-89)
- fn `def loadTypes(self, settings)` (L90-102)

### class `class SelAspectRatioTypeManager(AspectRatioTypeManager)` : AspectRatioTypeManager (L103-116)
- fn `def settingsCaption(self)` (L105-107)
- fn `def addDefaults(self)` (L108-116)

### class `class DeviceTypeManager(AspectRatioTypeManager)` : AspectRatioTypeManager (L117-129)
- fn `def settingsCaption(self)` (L119-121)
- fn `def addDefaults(self)` (L122-129)

### class `class MainWindow(QMainWindow)` : QMainWindow (L130-329)
- fn `def __init__(self)` `priv` (L134-247)
- fn `def viewer(self)` (L249-251)
- fn `def selections(self)` (L253-255)
- fn `def _setupConversionModeControls(self)` `priv` (L256-273)
  - Brief: Adds conversion mode controls to the basic tab.
  - Details: Creates `Mode` group with `Frame` and `Crop` radio buttons, defaults to `Frame`, and inserts it into the basic-tab layout.
  - Return: {None} Applies UI side effects.
- fn `def _setupTrimSettingsControls(self)` `priv` (L274-284)
  - Brief: Relocates trim configuration controls into the Basic tab.
  - Details: Reuses the existing trim-settings group from the advanced UI definition, moves it to the bottom of the basic layout with all controls visible.
  - Return: {None} Applies UI side effects.
- fn `def _setupTrimPresetControls(self)` `priv` (L285-320)
  - Brief: Adds dedicated Basic-tab trim preset controls.
  - Details: Creates a standalone `Presets` group placed immediately after `Trim settings`, configures stretch/fixed columns so preset names fill row width up to the right-edge remove button, and wires apply/rename/delete flows.
  - Return: {None} Applies UI side effects.

### fn `def _setupTrimPresetAction(self)` `priv` (L321-338)
- Brief: Adds the `Save Margins` toolbar action next to trim action.
- Details: Inserts a dedicated action directly to the right of `Trim Margins`, then binds it to preset creation and keeps it disabled until a PDF is loaded.
- Return: {None} Applies UI side effects.

### fn `def _trimPresetEditableFlag(self)` `priv` (L339-343)

### fn `def _trimPresetRole(self)` `priv` (L344-348)

### fn `def _defaultTrimPresetName(self)` `priv` (L349-356)
- Brief: Returns default trim preset name.
- Details: Generates timestamp name in `%Y/%m/%d %H:%M:%S` format.
- Return: {str} Default preset display label.

### fn `def _toBool(self, value)` `priv` (L357-367)
- Brief: Normalizes persisted boolean-like values.
- Details: Accepts bools and common string tokens produced by historical settings writers.
- Param: value {object} Input value from settings/config source.
- Return: {bool} Parsed boolean result.

### fn `def _updateTrimPagesRangeControls(self, enabled)` `priv` (L368-378)
- Brief: Updates `Pages range` control enabled state.
- Details: Enables range input only when trim-range mode is active and ensures default text `1-1` when empty.
- Param: enabled {bool} State propagated from trim-range toggle.
- Return: {None} Applies UI side effects.

### fn `def _parseTrimPagesRange(self)` `priv` (L379-395)
- Brief: Parses and validates the trim pages range expression.
- Details: Accepts only `N-M` one-based inclusive format, validates positive ordered bounds, and converts to zero-based bounds.
- Return: {tuple[int,int]} `(start_index, end_index)` inclusive zero-based page bounds.
- Throws: {ValueError} If the range is missing or syntactically/semantically invalid.

### fn `def _collectRuntimeConfigValues(self)` `priv` (L396-411)
- Brief: Collects runtime config values mapped to JSON `config` keys.
- Details: Converts current UI control state into serializable values for `~/.pdfframe/config.json`.
- Return: {dict[str,object]} Persistable runtime config key/value mapping.

### fn `def _preserveFieldsEnabled(self)` `priv` (L412-425)
- Brief: Returns Preserve fields option state.
- Details: Reads `checkPreserveFields` when available and normalizes truthy values for compatibility with test stubs.
- Return: {bool} True when `-dPreserveAnnots=true` must be emitted.

### fn `def _trimPresetFromCurrentSelection(self)` `priv` (L426-445)
- Brief: Creates a trim preset payload from current UI state.
- Details: Captures mode and trim parameters plus the primary current-page crop tuple when available.
- Return: {dict[str,object]} New preset payload ready for persistence.

### fn `def _refreshTrimPresetList(self)` `priv` (L446-474)
- Brief: Rebuilds trim preset tree rows from in-memory presets.
- Details: Clears the list, creates editable name rows, and attaches one remove button per row mapped to preset index inside a right-aligned cell container.
- Return: {None} Applies UI side effects.

### fn `def _persistTrimPresetDocument(self)` `priv` (L475-492)
- Brief: Persists runtime config and preset list to JSON config file.
- Details: Writes both `config` values and `presets` array through JsonConfigStore, surfacing warning on I/O failures.
- Return: {None} Writes `~/.pdfframe/config.json`.

### fn `def _applyCropPreset(self, crop_values)` `priv` (L493-524)
- Brief: Applies normalized crop tuple to current selection.
- Details: Maps `[left,top,right,bottom]` normalized margins to viewer coordinates and updates (or creates) the current selection.
- Param: crop_values {list[float]} Normalized crop tuple values.
- Return: {None} Mutates current selection geometry.

### fn `def _applyTrimPreset(self, index)` `priv` (L525-550)
- Brief: Applies one stored preset to current runtime controls.
- Details: Restores mode and trim values, then applies saved crop tuple when present.
- Param: index {int} Preset list index.
- Return: {None} Applies UI and selection updates.

### fn `def slotTrimPresetClicked(self, item, column)` (L551-563)
- Brief: Applies a preset when the preset name cell is clicked.
- Details: Ignores delete-button column and list rebuild events.
- Param: item {QTreeWidgetItem} Clicked row item.
- Param: column {int} Clicked column index.
- Return: {None} Applies preset side effects.

### fn `def slotTrimPresetDoubleClicked(self, item, column)` (L564-574)
- Brief: Starts inline rename for preset names.
- Details: Enables user-driven preset rename on double-click of first column.
- Param: item {QTreeWidgetItem} Double-clicked row item.
- Param: column {int} Double-clicked column index.
- Return: {None} Opens in-place editor.

### fn `def slotTrimPresetChanged(self, item, column)` (L575-598)
- Brief: Persists preset rename changes from inline editing.
- Details: Normalizes empty labels to timestamp defaults and rewrites JSON config after updates.
- Param: item {QTreeWidgetItem} Changed row item.
- Param: column {int} Changed column index.
- Return: {None} Persists preset list updates.

### fn `def slotDeleteTrimPreset(self)` (L599-617)
- Brief: Deletes one preset from remove-button click.
- Details: Resolves row index from sender button metadata, updates in-memory list, refreshes UI, and persists JSON state.
- Return: {None} Applies preset delete side effects.

### fn `def slotSaveMarginsPreset(self)` (L618-629)
- Brief: Saves current crop/trim state as a new preset.
- Details: Captures active control values, appends new preset with timestamp default name, refreshes list, and persists JSON state.
- Return: {None} Applies preset creation side effects.

### fn `def selectedConversionMode(self)` (L630-637)
- Brief: Returns selected conversion mode for Ghostscript execution.
- Details: Maps GUI mode controls to backend mode tokens expected by command generation.
- Return: {str} Conversion mode token (`frame` or `crop`).

### fn `def currentSelectionUpdated(self)` (L638-653)

### fn `def readSettings(self)` (L654-702)
- Brief: Reads persisted runtime settings from QSettings and JSON config.
- Details: Restores window geometry from QSettings, loads trim/runtime defaults from `~/.pdfframe/config.json`, and refreshes preset UI entries.
- Return: {None} Applies UI state restoration side effects.

### fn `def writeSettings(self)` (L703-727)
- Brief: Persists runtime settings to legacy and JSON backends.
- Details: Writes window/session metadata to QSettings and writes trim/runtime config plus presets to `~/.pdfframe/config.json`.
- Return: {None} Persists runtime state.

### fn `def openFile(self, fileName)` (L728-747)

### fn `def slotOpenFile(self)` (L748-753)

### fn `def slotSelectFile(self)` (L754-763)

### fn `def showWarning(self, title, text)` (L764-771)

### fn `def str2pages(self, s)` (L772-789)

### fn `def primarySelectionCropValue(self, page_indexes)` (L790-803)
- Brief: Gets primary selection crop tuple for conversion planning.
- Details: Resolves first available normalized crop tuple from current page first, then requested pages, and returns only the primary tuple used for all output pages.
- Param: page_indexes {list[int]} Ordered page indexes selected for processing.
- Return: {tuple[float,float,float,float]|None} Primary normalized crop tuple or None when no selections are available.

### fn `def buildGhostscriptCropPlan(self, inputFileName, outputFileName, requestedPageIndexes=None)` (L804-839)
- Brief: Builds single Ghostscript crop plan from GUI-derived parameters.
- Details: Iterates only requested pages (or all pages when omitted), derives geometry from the primary GUI selection tuple, computes crop bbox from page-size metadata, and emits one Ghostscript command for the full selected range using `-dFirstPage/-dLastPage` plus preserve-fields flag state.
- Param: inputFileName {str} Source PDF path.
- Param: outputFileName {str} Destination cropped PDF path.
- Param: requestedPageIndexes {set[int]|None} Optional zero-based page-index filter derived from `--whichpages`.
- Return: {dict[str,object]|None} Crop plan containing selected page indexes and one Ghostscript command vector.

### fn `def createConversionProgressDialog(self, totalPages)` (L840-862)
- Brief: Creates modal conversion progress dialog for crop execution.
- Details: Configures progress dialog with deterministic page range and cancellable stop action used during long-running conversion command execution.
- Param: totalPages {int} Number of selected pages to process.
- Return: {QProgressDialog} Configured progress dialog instance.

### fn `def slotPdfFrame(self)` (L863-985)
- Brief: Executes PDF crop action using Ghostscript command backend.
- Details: Verifies Ghostscript availability, builds one Ghostscript crop command from GUI state, and streams command output to update conversion progress across the selected page range.
- Return: {None} Triggers output PDF generation side effect.

### fn `def mark_page_processed(page_number)` (L917-935)
- Brief: Executes PDF crop action using Ghostscript command backend.
- Brief: Marks one selected page as processed for progress updates.
- Details: Verifies Ghostscript availability, builds one Ghostscript crop command from GUI state, and streams command output to update conversion progress across the selected page range.
- Details: Updates dialog value and label only once per page number to keep deterministic monotonic progress during streamed subprocess output handling.
- Param: page_number {int} One-based page number reported by Ghostscript.
- Return: {None} Triggers output PDF generation side effect.
- Return: {None} Applies progress side effects.

### fn `def on_output_line(line)` (L936-950)
- Brief: Processes streamed Ghostscript output lines during conversion.
- Details: Uses parsed Ghostscript page numbers from captured output to advance conversion progress without forwarding captured command output to user-visible UI messages.
- Param: line {str} Single output line emitted by Ghostscript.
- Return: {None} Applies progress side effects.

### fn `def slotZoomIn(self)` (L986-989)

### fn `def slotZoomOut(self)` (L990-993)

### fn `def slotFitInView(self, checked)` (L994-998)

### fn `def slotSplitterMoved(self, pos, idx)` (L999-1001)

### fn `def slotPreviousPage(self)` (L1002-1005)

### fn `def slotNextPage(self)` (L1006-1009)

### fn `def slotFirstPage(self)` (L1010-1013)

### fn `def slotLastPage(self)` (L1014-1017)

### fn `def slotCurrentPageEdited(self, text)` (L1018-1025)

### fn `def updateControls(self)` (L1026-1034)

### fn `def slotSelectionMode(self, checked)` (L1035-1038)

### fn `def slotSelExceptionsChanged(self)` (L1039-1041)

### fn `def slotSelExceptionsEdited(self, text)` (L1042-1046)

### fn `def slotSelAspectRatioChanged(self)` (L1047-1055)

### fn `def slotSelAspectRatioTypeChanged(self, index)` (L1056-1075)

### fn `def distributeAspectRatioChanged(self, aspectRatio)` (L1076-1078)

### fn `def slotDistributeAspectRatioChanged(self)` (L1079-1081)

### fn `def slotDeviceTypeChanged(self, index)` (L1082-1088)

### fn `def slotContextMenu(self, pos)` (L1089-1109)

### fn `def slotDeleteSelection(self)` (L1110-1113)

### fn `def slotNewSelection(self)` (L1114-1116)

### fn `def slotNewSelectionGrid(self)` (L1117-1126)

### fn `def createSelectionGrid(self, grid)` (L1127-1160)

### fn `def getPadding(self)` (L1161-1188)
- Brief: Returns trim padding in CSS-expanded order.
- Details: Reads trim padding text from the dedicated Basic-tab controls and expands one-to-four comma-separated values to `[top,right,bottom,left]`.
- Return: {list[float]} Padding tuple in top,right,bottom,left order.

### fn `def slotTrimMarginsAll(self)` (L1189-1201)

### fn `def slotTrimMargins(self)` (L1202-1206)

### fn `def trimMarginsSelection(self, sel)` (L1207-1310)
- Brief: Computes auto-trim rectangle for a selection using configured thresholds.
- Details: Reads color-sensitivity and grayscale-sensitivity values from Basic-tab controls, selects page scope using current page by default or a validated `Pages range` slice of visible pages when range mode is enabled, and applies auto-trim with padding and aspect-ratio adjustments.
- Param: sel {ViewerSelectionItem} Selection item to trim.
- Return: {None} Mutates selection bounding rectangle.

### fn `def resizeEvent(self, event)` (L1311-1313)

### fn `def closeEvent(self, event)` (L1314-1315)

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`AspectRatioType`|class|pub|44-49|class AspectRatioType|
|`AspectRatioType.__init__`|fn|priv|45-49|def __init__(self, name, width, height)|
|`AspectRatioTypeManager`|class|pub|50-102|class AspectRatioTypeManager|
|`AspectRatioTypeManager.__init__`|fn|priv|52-55|def __init__(self)|
|`AspectRatioTypeManager.__iter__`|fn|priv|56-58|def __iter__(self)|
|`AspectRatioTypeManager.addType`|fn|pub|59-61|def addType(self, name, width, height)|
|`AspectRatioTypeManager.getType`|fn|pub|62-66|def getType(self, index)|
|`AspectRatioTypeManager.addDefaults`|fn|pub|67-69|def addDefaults(self)|
|`AspectRatioTypeManager.settingsCaption`|fn|pub|70-72|def settingsCaption(self)|
|`AspectRatioTypeManager.saveTypes`|fn|pub|73-89|def saveTypes(self, settings)|
|`AspectRatioTypeManager.loadTypes`|fn|pub|90-102|def loadTypes(self, settings)|
|`SelAspectRatioTypeManager`|class|pub|103-116|class SelAspectRatioTypeManager(AspectRatioTypeManager)|
|`SelAspectRatioTypeManager.settingsCaption`|fn|pub|105-107|def settingsCaption(self)|
|`SelAspectRatioTypeManager.addDefaults`|fn|pub|108-116|def addDefaults(self)|
|`DeviceTypeManager`|class|pub|117-129|class DeviceTypeManager(AspectRatioTypeManager)|
|`DeviceTypeManager.settingsCaption`|fn|pub|119-121|def settingsCaption(self)|
|`DeviceTypeManager.addDefaults`|fn|pub|122-129|def addDefaults(self)|
|`MainWindow`|class|pub|130-329|class MainWindow(QMainWindow)|
|`MainWindow.__init__`|fn|priv|134-247|def __init__(self)|
|`MainWindow.viewer`|fn|pub|249-251|def viewer(self)|
|`MainWindow.selections`|fn|pub|253-255|def selections(self)|
|`MainWindow._setupConversionModeControls`|fn|priv|256-273|def _setupConversionModeControls(self)|
|`MainWindow._setupTrimSettingsControls`|fn|priv|274-284|def _setupTrimSettingsControls(self)|
|`MainWindow._setupTrimPresetControls`|fn|priv|285-320|def _setupTrimPresetControls(self)|
|`_setupTrimPresetAction`|fn|priv|321-338|def _setupTrimPresetAction(self)|
|`_trimPresetEditableFlag`|fn|priv|339-343|def _trimPresetEditableFlag(self)|
|`_trimPresetRole`|fn|priv|344-348|def _trimPresetRole(self)|
|`_defaultTrimPresetName`|fn|priv|349-356|def _defaultTrimPresetName(self)|
|`_toBool`|fn|priv|357-367|def _toBool(self, value)|
|`_updateTrimPagesRangeControls`|fn|priv|368-378|def _updateTrimPagesRangeControls(self, enabled)|
|`_parseTrimPagesRange`|fn|priv|379-395|def _parseTrimPagesRange(self)|
|`_collectRuntimeConfigValues`|fn|priv|396-411|def _collectRuntimeConfigValues(self)|
|`_preserveFieldsEnabled`|fn|priv|412-425|def _preserveFieldsEnabled(self)|
|`_trimPresetFromCurrentSelection`|fn|priv|426-445|def _trimPresetFromCurrentSelection(self)|
|`_refreshTrimPresetList`|fn|priv|446-474|def _refreshTrimPresetList(self)|
|`_persistTrimPresetDocument`|fn|priv|475-492|def _persistTrimPresetDocument(self)|
|`_applyCropPreset`|fn|priv|493-524|def _applyCropPreset(self, crop_values)|
|`_applyTrimPreset`|fn|priv|525-550|def _applyTrimPreset(self, index)|
|`slotTrimPresetClicked`|fn|pub|551-563|def slotTrimPresetClicked(self, item, column)|
|`slotTrimPresetDoubleClicked`|fn|pub|564-574|def slotTrimPresetDoubleClicked(self, item, column)|
|`slotTrimPresetChanged`|fn|pub|575-598|def slotTrimPresetChanged(self, item, column)|
|`slotDeleteTrimPreset`|fn|pub|599-617|def slotDeleteTrimPreset(self)|
|`slotSaveMarginsPreset`|fn|pub|618-629|def slotSaveMarginsPreset(self)|
|`selectedConversionMode`|fn|pub|630-637|def selectedConversionMode(self)|
|`currentSelectionUpdated`|fn|pub|638-653|def currentSelectionUpdated(self)|
|`readSettings`|fn|pub|654-702|def readSettings(self)|
|`writeSettings`|fn|pub|703-727|def writeSettings(self)|
|`openFile`|fn|pub|728-747|def openFile(self, fileName)|
|`slotOpenFile`|fn|pub|748-753|def slotOpenFile(self)|
|`slotSelectFile`|fn|pub|754-763|def slotSelectFile(self)|
|`showWarning`|fn|pub|764-771|def showWarning(self, title, text)|
|`str2pages`|fn|pub|772-789|def str2pages(self, s)|
|`primarySelectionCropValue`|fn|pub|790-803|def primarySelectionCropValue(self, page_indexes)|
|`buildGhostscriptCropPlan`|fn|pub|804-839|def buildGhostscriptCropPlan(self, inputFileName, outputF...|
|`createConversionProgressDialog`|fn|pub|840-862|def createConversionProgressDialog(self, totalPages)|
|`slotPdfFrame`|fn|pub|863-985|def slotPdfFrame(self)|
|`mark_page_processed`|fn|pub|917-935|def mark_page_processed(page_number)|
|`on_output_line`|fn|pub|936-950|def on_output_line(line)|
|`slotZoomIn`|fn|pub|986-989|def slotZoomIn(self)|
|`slotZoomOut`|fn|pub|990-993|def slotZoomOut(self)|
|`slotFitInView`|fn|pub|994-998|def slotFitInView(self, checked)|
|`slotSplitterMoved`|fn|pub|999-1001|def slotSplitterMoved(self, pos, idx)|
|`slotPreviousPage`|fn|pub|1002-1005|def slotPreviousPage(self)|
|`slotNextPage`|fn|pub|1006-1009|def slotNextPage(self)|
|`slotFirstPage`|fn|pub|1010-1013|def slotFirstPage(self)|
|`slotLastPage`|fn|pub|1014-1017|def slotLastPage(self)|
|`slotCurrentPageEdited`|fn|pub|1018-1025|def slotCurrentPageEdited(self, text)|
|`updateControls`|fn|pub|1026-1034|def updateControls(self)|
|`slotSelectionMode`|fn|pub|1035-1038|def slotSelectionMode(self, checked)|
|`slotSelExceptionsChanged`|fn|pub|1039-1041|def slotSelExceptionsChanged(self)|
|`slotSelExceptionsEdited`|fn|pub|1042-1046|def slotSelExceptionsEdited(self, text)|
|`slotSelAspectRatioChanged`|fn|pub|1047-1055|def slotSelAspectRatioChanged(self)|
|`slotSelAspectRatioTypeChanged`|fn|pub|1056-1075|def slotSelAspectRatioTypeChanged(self, index)|
|`distributeAspectRatioChanged`|fn|pub|1076-1078|def distributeAspectRatioChanged(self, aspectRatio)|
|`slotDistributeAspectRatioChanged`|fn|pub|1079-1081|def slotDistributeAspectRatioChanged(self)|
|`slotDeviceTypeChanged`|fn|pub|1082-1088|def slotDeviceTypeChanged(self, index)|
|`slotContextMenu`|fn|pub|1089-1109|def slotContextMenu(self, pos)|
|`slotDeleteSelection`|fn|pub|1110-1113|def slotDeleteSelection(self)|
|`slotNewSelection`|fn|pub|1114-1116|def slotNewSelection(self)|
|`slotNewSelectionGrid`|fn|pub|1117-1126|def slotNewSelectionGrid(self)|
|`createSelectionGrid`|fn|pub|1127-1160|def createSelectionGrid(self, grid)|
|`getPadding`|fn|pub|1161-1188|def getPadding(self)|
|`slotTrimMarginsAll`|fn|pub|1189-1201|def slotTrimMarginsAll(self)|
|`slotTrimMargins`|fn|pub|1202-1206|def slotTrimMargins(self)|
|`trimMarginsSelection`|fn|pub|1207-1310|def trimMarginsSelection(self, sel)|
|`resizeEvent`|fn|pub|1311-1313|def resizeEvent(self, event)|
|`closeEvent`|fn|pub|1314-1315|def closeEvent(self, event)|


---

# mainwindowui_qt5.py | Python | 460L | 3 symbols | 1 imports | 7 comments
> Path: `src/pdfframe/mainwindowui_qt5.py`

## Imports
```
from PyQt5 import QtCore, QtGui, QtWidgets
```

## Definitions

### class `class Ui_MainWindow(object)` : object (L14-213)

### fn `def setupUi(self, MainWindow)` (L15-214)

### fn `def retranslateUi(self, MainWindow)` (L372-381)

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`Ui_MainWindow`|class|pub|14-213|class Ui_MainWindow(object)|
|`setupUi`|fn|pub|15-214|def setupUi(self, MainWindow)|
|`retranslateUi`|fn|pub|372-381|def retranslateUi(self, MainWindow)|


---

# mainwindowui_qt6.py | Python | 458L | 3 symbols | 1 imports | 6 comments
> Path: `src/pdfframe/mainwindowui_qt6.py`

## Imports
```
from PyQt6 import QtCore, QtGui, QtWidgets
```

## Definitions

### class `class Ui_MainWindow(object)` : object (L12-211)

### fn `def setupUi(self, MainWindow)` (L13-212)

### fn `def retranslateUi(self, MainWindow)` (L370-379)

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`Ui_MainWindow`|class|pub|12-211|class Ui_MainWindow(object)|
|`setupUi`|fn|pub|13-212|def setupUi(self, MainWindow)|
|`retranslateUi`|fn|pub|370-379|def retranslateUi(self, MainWindow)|


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

# pdfframeper.py | Python | 329L | 62 symbols | 10 imports | 43 comments
> Path: `src/pdfframe/pdfframeper.py`

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

### class `class PdfEncryptedError(Exception)` : Exception (L22-25)

### class `class AbstractPdfFile` (L26-33)
- fn `def loadFromStream(self, stream)` (L29-30)
- fn `def loadFromFile(self, filename)` (L31-33)

### class `class PyPdfFile(AbstractPdfFile)` : AbstractPdfFile (L34-48)
- fn `def __init__(self)` `priv` (L36-37)
- fn `def loadFromStream(self, stream)` (L38-45)
- fn `def getPage(self, nr)` (L46-48)

### class `class PyPdfOldFile(PyPdfFile)` : PyPdfFile (L49-62)
- fn `def loadFromStream(self, stream)` (L52-59)
- fn `def getPage(self, nr)` (L60-62)

### class `class PyMuPdfFile(AbstractPdfFile)` : AbstractPdfFile (L63-73)
- fn `def __init__(self)` `priv` (L65-66)
- fn `def loadFromStream(self, stream)` (L67-70)
- fn `def getPage(self, nr)` (L71-73)

### class `class PikePdfFile(AbstractPdfFile)` : AbstractPdfFile (L74-85)
- fn `def __init__(self)` `priv` (L76-77)
- fn `def loadFromStream(self, stream)` (L78-81)
- fn `def getPage(self, nr)` (L82-85)

### class `class AbstractPdfFrameper` (L86-99)
- fn `def writeToStream(self, stream)` (L89-90)
- fn `def writeToFile(self, filename)` (L91-94)
- fn `def addPageCropped(self, pdffile, pagenumber, croplist, rotate=0)` (L95-96)
- fn `def copyDocumentRoot(self, pdffile)` (L97-99)

### class `class SemiAbstractPdfFrameper(AbstractPdfFrameper)` : AbstractPdfFrameper (L100-120)
- fn `def addPageCropped(self, pdffile, pagenumber, croplist, alwaysinclude, rotate=0)` (L103-113)
- fn `def doAddPage(self, page, rotate)` (L114-115)
- fn `def pageGetCropBox(self, page)` (L116-117)
- fn `def pageSetCropBox(self, page, box)` (L118-120)

### class `class PyPdfFrameper(SemiAbstractPdfFrameper)` : SemiAbstractPdfFrameper (L121-152)
- fn `def __init__(self)` `priv` (L123-124)
- fn `def writeToStream(self, stream)` (L125-133)
- fn `def doAddPage(self, page, rotate)` (L134-137)
- fn `def pageGetCropBox(self, page)` (L138-141)
- fn `def pageSetCropBox(self, page, box)` (L142-146)
- fn `def copyDocumentRoot(self, pdffile)` (L147-152)

### class `class PyPdfOldCropper(PyPdfFrameper)` : PyPdfFrameper (L153-173)
- fn `def doAddPage(self, page, rotate)` (L155-158)
- fn `def pageGetCropBox(self, page)` (L159-162)
- fn `def pageSetCropBox(self, page, box)` (L163-167)
- fn `def copyDocumentRoot(self, pdffile)` (L168-173)

### class `class PyMuPdfFrameper(SemiAbstractPdfFrameper)` : SemiAbstractPdfFrameper (L174-214)
- fn `def __init__(self)` `priv` (L176-177)
- fn `def writeToStream(self, stream)` (L178-179)
- fn `def addPageCropped(self, pdffile, pagenumber, croplist, alwaysinclude, rotate=0)` (L180-197)
- fn `def addPage()` (L181-184)
- fn `def pageGetCropBox(self, page)` (L198-199)
- fn `def pageSetCropBox(self, page, box)` (L200-210)
- fn `def copyDocumentRoot(self, pdffile)` (L211-214)

### class `class PikePdfFrameper(SemiAbstractPdfFrameper)` : SemiAbstractPdfFrameper (L215-238)
- fn `def __init__(self)` `priv` (L217-218)
- fn `def writeToStream(self, stream)` (L219-220)
- fn `def doAddPage(self, page, rotate)` (L221-224)
- fn `def pageGetCropBox(self, page)` (L225-230)
- fn `def pageSetCropBox(self, page, box)` (L231-234)
- fn `def copyDocumentRoot(self, pdffile)` (L235-238)

### fn `def computeCropBoxCoords(box, crop, pdf_coords=True)` (L239-249)

### fn `def optimizePdfGhostscript(oldfilename, newfilename)` (L250-255)

### fn `def import_pymupdf()` (L259-266)

### fn `def import_pikepdf()` (L267-272)

### fn `def import_pypdf()` (L273-278)

### fn `def import_pypdf2()` (L279-293)

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`PdfEncryptedError`|class|pub|22-25|class PdfEncryptedError(Exception)|
|`AbstractPdfFile`|class|pub|26-33|class AbstractPdfFile|
|`AbstractPdfFile.loadFromStream`|fn|pub|29-30|def loadFromStream(self, stream)|
|`AbstractPdfFile.loadFromFile`|fn|pub|31-33|def loadFromFile(self, filename)|
|`PyPdfFile`|class|pub|34-48|class PyPdfFile(AbstractPdfFile)|
|`PyPdfFile.__init__`|fn|priv|36-37|def __init__(self)|
|`PyPdfFile.loadFromStream`|fn|pub|38-45|def loadFromStream(self, stream)|
|`PyPdfFile.getPage`|fn|pub|46-48|def getPage(self, nr)|
|`PyPdfOldFile`|class|pub|49-62|class PyPdfOldFile(PyPdfFile)|
|`PyPdfOldFile.loadFromStream`|fn|pub|52-59|def loadFromStream(self, stream)|
|`PyPdfOldFile.getPage`|fn|pub|60-62|def getPage(self, nr)|
|`PyMuPdfFile`|class|pub|63-73|class PyMuPdfFile(AbstractPdfFile)|
|`PyMuPdfFile.__init__`|fn|priv|65-66|def __init__(self)|
|`PyMuPdfFile.loadFromStream`|fn|pub|67-70|def loadFromStream(self, stream)|
|`PyMuPdfFile.getPage`|fn|pub|71-73|def getPage(self, nr)|
|`PikePdfFile`|class|pub|74-85|class PikePdfFile(AbstractPdfFile)|
|`PikePdfFile.__init__`|fn|priv|76-77|def __init__(self)|
|`PikePdfFile.loadFromStream`|fn|pub|78-81|def loadFromStream(self, stream)|
|`PikePdfFile.getPage`|fn|pub|82-85|def getPage(self, nr)|
|`AbstractPdfFrameper`|class|pub|86-99|class AbstractPdfFrameper|
|`AbstractPdfFrameper.writeToStream`|fn|pub|89-90|def writeToStream(self, stream)|
|`AbstractPdfFrameper.writeToFile`|fn|pub|91-94|def writeToFile(self, filename)|
|`AbstractPdfFrameper.addPageCropped`|fn|pub|95-96|def addPageCropped(self, pdffile, pagenumber, croplist, r...|
|`AbstractPdfFrameper.copyDocumentRoot`|fn|pub|97-99|def copyDocumentRoot(self, pdffile)|
|`SemiAbstractPdfFrameper`|class|pub|100-120|class SemiAbstractPdfFrameper(AbstractPdfFrameper)|
|`SemiAbstractPdfFrameper.addPageCropped`|fn|pub|103-113|def addPageCropped(self, pdffile, pagenumber, croplist, a...|
|`SemiAbstractPdfFrameper.doAddPage`|fn|pub|114-115|def doAddPage(self, page, rotate)|
|`SemiAbstractPdfFrameper.pageGetCropBox`|fn|pub|116-117|def pageGetCropBox(self, page)|
|`SemiAbstractPdfFrameper.pageSetCropBox`|fn|pub|118-120|def pageSetCropBox(self, page, box)|
|`PyPdfFrameper`|class|pub|121-152|class PyPdfFrameper(SemiAbstractPdfFrameper)|
|`PyPdfFrameper.__init__`|fn|priv|123-124|def __init__(self)|
|`PyPdfFrameper.writeToStream`|fn|pub|125-133|def writeToStream(self, stream)|
|`PyPdfFrameper.doAddPage`|fn|pub|134-137|def doAddPage(self, page, rotate)|
|`PyPdfFrameper.pageGetCropBox`|fn|pub|138-141|def pageGetCropBox(self, page)|
|`PyPdfFrameper.pageSetCropBox`|fn|pub|142-146|def pageSetCropBox(self, page, box)|
|`PyPdfFrameper.copyDocumentRoot`|fn|pub|147-152|def copyDocumentRoot(self, pdffile)|
|`PyPdfOldCropper`|class|pub|153-173|class PyPdfOldCropper(PyPdfFrameper)|
|`PyPdfOldCropper.doAddPage`|fn|pub|155-158|def doAddPage(self, page, rotate)|
|`PyPdfOldCropper.pageGetCropBox`|fn|pub|159-162|def pageGetCropBox(self, page)|
|`PyPdfOldCropper.pageSetCropBox`|fn|pub|163-167|def pageSetCropBox(self, page, box)|
|`PyPdfOldCropper.copyDocumentRoot`|fn|pub|168-173|def copyDocumentRoot(self, pdffile)|
|`PyMuPdfFrameper`|class|pub|174-214|class PyMuPdfFrameper(SemiAbstractPdfFrameper)|
|`PyMuPdfFrameper.__init__`|fn|priv|176-177|def __init__(self)|
|`PyMuPdfFrameper.writeToStream`|fn|pub|178-179|def writeToStream(self, stream)|
|`PyMuPdfFrameper.addPageCropped`|fn|pub|180-197|def addPageCropped(self, pdffile, pagenumber, croplist, a...|
|`PyMuPdfFrameper.addPage`|fn|pub|181-184|def addPage()|
|`PyMuPdfFrameper.pageGetCropBox`|fn|pub|198-199|def pageGetCropBox(self, page)|
|`PyMuPdfFrameper.pageSetCropBox`|fn|pub|200-210|def pageSetCropBox(self, page, box)|
|`PyMuPdfFrameper.copyDocumentRoot`|fn|pub|211-214|def copyDocumentRoot(self, pdffile)|
|`PikePdfFrameper`|class|pub|215-238|class PikePdfFrameper(SemiAbstractPdfFrameper)|
|`PikePdfFrameper.__init__`|fn|priv|217-218|def __init__(self)|
|`PikePdfFrameper.writeToStream`|fn|pub|219-220|def writeToStream(self, stream)|
|`PikePdfFrameper.doAddPage`|fn|pub|221-224|def doAddPage(self, page, rotate)|
|`PikePdfFrameper.pageGetCropBox`|fn|pub|225-230|def pageGetCropBox(self, page)|
|`PikePdfFrameper.pageSetCropBox`|fn|pub|231-234|def pageSetCropBox(self, page, box)|
|`PikePdfFrameper.copyDocumentRoot`|fn|pub|235-238|def copyDocumentRoot(self, pdffile)|
|`computeCropBoxCoords`|fn|pub|239-249|def computeCropBoxCoords(box, crop, pdf_coords=True)|
|`optimizePdfGhostscript`|fn|pub|250-255|def optimizePdfGhostscript(oldfilename, newfilename)|
|`import_pymupdf`|fn|pub|259-266|def import_pymupdf()|
|`import_pikepdf`|fn|pub|267-272|def import_pikepdf()|
|`import_pypdf`|fn|pub|273-278|def import_pypdf()|
|`import_pypdf2`|fn|pub|279-293|def import_pypdf2()|


---

# qt.py | Python | 10L | 0 symbols | 7 imports | 0 comments
> Path: `src/pdfframe/qt.py`

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

# vieweritem.py | Python | 302L | 43 symbols | 8 imports | 25 comments
> Path: `src/pdfframe/vieweritem.py`

## Imports
```
import sys
from pdfframe.config import PYQT6
from pdfframe.qt import *
from pdfframe.viewerselections import ViewerSelections
from pdfframe.config import PYQT6
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

# viewerselections.py | Python | 654L | 71 symbols | 2 imports | 40 comments
> Path: `src/pdfframe/viewerselections.py`

## Imports
```
from math import ceil
from pdfframe.qt import *
```

## Definitions

### class `class ViewerSelections(object)` : object (L21-150)
- fn `def __init__(self, viewer)` `priv` (L29-37)
- fn `def items(self)` (L39-46)
- fn `def addSelection(self, rect=None)` (L47-52)
- fn `def deleteSelection(self, s)` (L53-59)
- fn `def deleteSelections(self)` (L60-63)
- fn `def getCurrentSelection(self)` (L64-66)
- fn `def setCurrentSelection(self, currentSelection)` (L67-78)
- fn `def autoSetCurrentSelection(self)` (L81-94)
- fn `def currentSelectionUpdated(self)` (L95-97)
- fn `def getDistributeAspectRatio(self)` (L98-100)
- fn `def setDistributeAspectRatio(self, distributeAspectRatio)` (L101-104)
- fn `def getSelectionMode(self)` (L107-109)
- fn `def setSelectionMode(self, mode)` (L110-113)
- fn `def getSelectionExceptions(self)` (L116-118)
- fn `def setSelectionExceptions(self, exceptions)` (L119-122)
- fn `def updateSelectionVisibility(self)` (L125-130)
- fn `def cropValues(self, idx)` (L131-134)
- fn `def mousePressEvent(self, event)` (L135-141)
- fn `def mouseMoveEvent(self, event)` (L142-146)
- fn `def mouseReleaseEvent(self, event)` (L147-150)

### class `class ViewerSelectionItem(QGraphicsItem)` : QGraphicsItem (L151-350)
- fn `def __init__(self, parent, rect=None)` `priv` (L157-183)
- fn `def selection(self)` (L185-188)
- fn `def viewer(self)` (L190-192)
- fn `def selections(self)` (L194-197)
- fn `def isCurrent(self)` (L198-200)
- fn `def setAsCurrent(self)` (L201-204)
- fn `def orderIndex(self)` (L206-214)
- fn `def aspectRatio(self)` (L216-218)
- fn `def getAspectRatioData(self)` (L219-221)
- fn `def setAspectRatioData(self, data)` (L222-235)
- fn `def distributeAspectRatio(self)` (L240-243)
- fn `def selectionVisibleOnPage(self, pageIndex)` (L244-249)
- fn `def boundingRect(self)` (L250-252)
- fn `def setBoundingRect(self, pt1, pt2)` (L253-262)
- fn `def adjustBoundingRect(self, dx1=0, dy1=0, dx2=0, dy2=0)` (L263-334)
- fn `def moveBoundingRect(self, dx, dy)` (L335-349)

### fn `def distributeRect(self)` (L350-362)

### fn `def cropValues(self)` (L363-379)

### fn `def clamp(v)` (L365-366)

### fn `def cV(r)` (L367-377)

### fn `def mapRectToImage(self, r)` (L380-383)

### fn `def mapRectFromImage(self, r)` (L384-387)

### fn `def paint(self, painter, option, widget)` (L388-427)

### fn `def drawLine(pt1, pt2)` (L399-404)

### fn `def mousePressEvent(self, event)` (L428-439)

### fn `def mouseMoveEvent(self, event)` (L440-458)

### fn `def mouseReleaseEvent(self, event)` (L459-462)

### fn `def keyPressEvent(self, event)` (L463-482)

### class `class SelectionHandleItem(QGraphicsItem)` : QGraphicsItem (L483-582)
- fn `def __init__(self, parent, role)` `priv` (L490-505)
- fn `def selection(self)` (L507-509)
- fn `def handleColor(self)` (L511-515)
- fn `def boundingRect(self)` (L516-535)
- fn `def paint(self, painter, option, widget)` (L536-554)
- fn `def mousePressEvent(self, event)` (L555-560)
- fn `def mouseMoveEvent(self, event)` (L561-578)
- fn `def mouseReleaseEvent(self, event)` (L579-582)

### class `class SelectionCornerHandleItem(QGraphicsItem)` : QGraphicsItem (L583-642)
- fn `def __init__(self, parent, lr, tb)` `priv` (L584-594)
- fn `def selection(self)` (L596-598)
- fn `def handleColor(self)` (L600-604)
- fn `def corner(self, rect)` (L605-608)
- fn `def direction(self, pt)` (L609-614)
- fn `def boundingRect(self)` (L615-620)
- fn `def paint(self, painter, option, widget)` (L621-626)
- fn `def mousePressEvent(self, event)` (L627-632)
- fn `def mouseMoveEvent(self, event)` (L633-638)
- fn `def mouseReleaseEvent(self, event)` (L639-642)

### fn `def aspectRatioFromStr(s)` (L643-654)

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`ViewerSelections`|class|pub|21-150|class ViewerSelections(object)|
|`ViewerSelections.__init__`|fn|priv|29-37|def __init__(self, viewer)|
|`ViewerSelections.items`|fn|pub|39-46|def items(self)|
|`ViewerSelections.addSelection`|fn|pub|47-52|def addSelection(self, rect=None)|
|`ViewerSelections.deleteSelection`|fn|pub|53-59|def deleteSelection(self, s)|
|`ViewerSelections.deleteSelections`|fn|pub|60-63|def deleteSelections(self)|
|`ViewerSelections.getCurrentSelection`|fn|pub|64-66|def getCurrentSelection(self)|
|`ViewerSelections.setCurrentSelection`|fn|pub|67-78|def setCurrentSelection(self, currentSelection)|
|`ViewerSelections.autoSetCurrentSelection`|fn|pub|81-94|def autoSetCurrentSelection(self)|
|`ViewerSelections.currentSelectionUpdated`|fn|pub|95-97|def currentSelectionUpdated(self)|
|`ViewerSelections.getDistributeAspectRatio`|fn|pub|98-100|def getDistributeAspectRatio(self)|
|`ViewerSelections.setDistributeAspectRatio`|fn|pub|101-104|def setDistributeAspectRatio(self, distributeAspectRatio)|
|`ViewerSelections.getSelectionMode`|fn|pub|107-109|def getSelectionMode(self)|
|`ViewerSelections.setSelectionMode`|fn|pub|110-113|def setSelectionMode(self, mode)|
|`ViewerSelections.getSelectionExceptions`|fn|pub|116-118|def getSelectionExceptions(self)|
|`ViewerSelections.setSelectionExceptions`|fn|pub|119-122|def setSelectionExceptions(self, exceptions)|
|`ViewerSelections.updateSelectionVisibility`|fn|pub|125-130|def updateSelectionVisibility(self)|
|`ViewerSelections.cropValues`|fn|pub|131-134|def cropValues(self, idx)|
|`ViewerSelections.mousePressEvent`|fn|pub|135-141|def mousePressEvent(self, event)|
|`ViewerSelections.mouseMoveEvent`|fn|pub|142-146|def mouseMoveEvent(self, event)|
|`ViewerSelections.mouseReleaseEvent`|fn|pub|147-150|def mouseReleaseEvent(self, event)|
|`ViewerSelectionItem`|class|pub|151-350|class ViewerSelectionItem(QGraphicsItem)|
|`ViewerSelectionItem.__init__`|fn|priv|157-183|def __init__(self, parent, rect=None)|
|`ViewerSelectionItem.selection`|fn|pub|185-188|def selection(self)|
|`ViewerSelectionItem.viewer`|fn|pub|190-192|def viewer(self)|
|`ViewerSelectionItem.selections`|fn|pub|194-197|def selections(self)|
|`ViewerSelectionItem.isCurrent`|fn|pub|198-200|def isCurrent(self)|
|`ViewerSelectionItem.setAsCurrent`|fn|pub|201-204|def setAsCurrent(self)|
|`ViewerSelectionItem.orderIndex`|fn|pub|206-214|def orderIndex(self)|
|`ViewerSelectionItem.aspectRatio`|fn|pub|216-218|def aspectRatio(self)|
|`ViewerSelectionItem.getAspectRatioData`|fn|pub|219-221|def getAspectRatioData(self)|
|`ViewerSelectionItem.setAspectRatioData`|fn|pub|222-235|def setAspectRatioData(self, data)|
|`ViewerSelectionItem.distributeAspectRatio`|fn|pub|240-243|def distributeAspectRatio(self)|
|`ViewerSelectionItem.selectionVisibleOnPage`|fn|pub|244-249|def selectionVisibleOnPage(self, pageIndex)|
|`ViewerSelectionItem.boundingRect`|fn|pub|250-252|def boundingRect(self)|
|`ViewerSelectionItem.setBoundingRect`|fn|pub|253-262|def setBoundingRect(self, pt1, pt2)|
|`ViewerSelectionItem.adjustBoundingRect`|fn|pub|263-334|def adjustBoundingRect(self, dx1=0, dy1=0, dx2=0, dy2=0)|
|`ViewerSelectionItem.moveBoundingRect`|fn|pub|335-349|def moveBoundingRect(self, dx, dy)|
|`distributeRect`|fn|pub|350-362|def distributeRect(self)|
|`cropValues`|fn|pub|363-379|def cropValues(self)|
|`clamp`|fn|pub|365-366|def clamp(v)|
|`cV`|fn|pub|367-377|def cV(r)|
|`mapRectToImage`|fn|pub|380-383|def mapRectToImage(self, r)|
|`mapRectFromImage`|fn|pub|384-387|def mapRectFromImage(self, r)|
|`paint`|fn|pub|388-427|def paint(self, painter, option, widget)|
|`drawLine`|fn|pub|399-404|def drawLine(pt1, pt2)|
|`mousePressEvent`|fn|pub|428-439|def mousePressEvent(self, event)|
|`mouseMoveEvent`|fn|pub|440-458|def mouseMoveEvent(self, event)|
|`mouseReleaseEvent`|fn|pub|459-462|def mouseReleaseEvent(self, event)|
|`keyPressEvent`|fn|pub|463-482|def keyPressEvent(self, event)|
|`SelectionHandleItem`|class|pub|483-582|class SelectionHandleItem(QGraphicsItem)|
|`SelectionHandleItem.__init__`|fn|priv|490-505|def __init__(self, parent, role)|
|`SelectionHandleItem.selection`|fn|pub|507-509|def selection(self)|
|`SelectionHandleItem.handleColor`|fn|pub|511-515|def handleColor(self)|
|`SelectionHandleItem.boundingRect`|fn|pub|516-535|def boundingRect(self)|
|`SelectionHandleItem.paint`|fn|pub|536-554|def paint(self, painter, option, widget)|
|`SelectionHandleItem.mousePressEvent`|fn|pub|555-560|def mousePressEvent(self, event)|
|`SelectionHandleItem.mouseMoveEvent`|fn|pub|561-578|def mouseMoveEvent(self, event)|
|`SelectionHandleItem.mouseReleaseEvent`|fn|pub|579-582|def mouseReleaseEvent(self, event)|
|`SelectionCornerHandleItem`|class|pub|583-642|class SelectionCornerHandleItem(QGraphicsItem)|
|`SelectionCornerHandleItem.__init__`|fn|priv|584-594|def __init__(self, parent, lr, tb)|
|`SelectionCornerHandleItem.selection`|fn|pub|596-598|def selection(self)|
|`SelectionCornerHandleItem.handleColor`|fn|pub|600-604|def handleColor(self)|
|`SelectionCornerHandleItem.corner`|fn|pub|605-608|def corner(self, rect)|
|`SelectionCornerHandleItem.direction`|fn|pub|609-614|def direction(self, pt)|
|`SelectionCornerHandleItem.boundingRect`|fn|pub|615-620|def boundingRect(self)|
|`SelectionCornerHandleItem.paint`|fn|pub|621-626|def paint(self, painter, option, widget)|
|`SelectionCornerHandleItem.mousePressEvent`|fn|pub|627-632|def mousePressEvent(self, event)|
|`SelectionCornerHandleItem.mouseMoveEvent`|fn|pub|633-638|def mouseMoveEvent(self, event)|
|`SelectionCornerHandleItem.mouseReleaseEvent`|fn|pub|639-642|def mouseReleaseEvent(self, event)|
|`aspectRatioFromStr`|fn|pub|643-654|def aspectRatioFromStr(s)|

