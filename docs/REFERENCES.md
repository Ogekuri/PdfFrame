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

# autotrim.py | Python | 65L | 3 symbols | 1 imports | 6 comments
> Path: `src/pdfframe/autotrim.py`

## Imports
```
from pdfframe.qt import *
```

## Definitions

### fn `def autoTrimMargins(img, r, minr, sensitivity, allowedchanges)` (L19-65)

### fn `def pixAt(x, y)` (L23-25)

### fn `def isTrimmable(L)` (L26-38)

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`autoTrimMargins`|fn|pub|19-65|def autoTrimMargins(img, r, minr, sensitivity, allowedcha...|
|`pixAt`|fn|pub|23-25|def pixAt(x, y)|
|`isTrimmable`|fn|pub|26-38|def isTrimmable(L)|


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

# mainwindow.py | Python | 921L | 68 symbols | 11 imports | 46 comments
> Path: `src/pdfframe/mainwindow.py`

## Imports
```
import sys
from os.path import splitext
from shutil import which
from pdfframe.qt import *
from pdfframe.config import PYQT6
from pdfframe.mainwindowui_qt6 import Ui_MainWindow
from pdfframe.mainwindowui_qt5 import Ui_MainWindow
from pdfframe.viewerselections import ViewerSelections, aspectRatioFromStr
from pdfframe.vieweritem import ViewerItem
from pdfframe.pdfframecmd import (
from pdfframe.autotrim import autoTrimMargins
```

## Definitions

### class `class AspectRatioType` (L41-46)
- fn `def __init__(self, name, width, height)` `priv` (L42-46)

### class `class AspectRatioTypeManager` (L47-99)
- fn `def __init__(self)` `priv` (L49-52)
- fn `def __iter__(self)` `priv` (L53-55)
- fn `def addType(self, name, width, height)` (L56-58)
- fn `def getType(self, index)` (L59-63)
- fn `def addDefaults(self)` (L64-66)
- fn `def settingsCaption(self)` (L67-69)
- fn `def saveTypes(self, settings)` (L70-86)
- fn `def loadTypes(self, settings)` (L87-99)

### class `class SelAspectRatioTypeManager(AspectRatioTypeManager)` : AspectRatioTypeManager (L100-113)
- fn `def settingsCaption(self)` (L102-104)
- fn `def addDefaults(self)` (L105-113)

### class `class DeviceTypeManager(AspectRatioTypeManager)` : AspectRatioTypeManager (L114-126)
- fn `def settingsCaption(self)` (L116-118)
- fn `def addDefaults(self)` (L119-126)

### class `class MainWindow(QMainWindow)` : QMainWindow (L127-326)
- fn `def __init__(self)` `priv` (L131-245)
- fn `def viewer(self)` (L247-249)
- fn `def selections(self)` (L251-253)
- fn `def _setupConversionModeControls(self)` `priv` (L254-271)
  - Brief: Adds conversion mode controls to the basic tab.
  - Details: Creates `Mode` group with `Frame` and `Crop` radio buttons, defaults to `Frame`, and inserts it into the basic-tab layout.
  - Return: {None} Applies UI side effects.
- fn `def _setupTrimSettingsControls(self)` `priv` (L272-282)
  - Brief: Relocates trim configuration controls into the Basic tab.
  - Details: Reuses the existing trim-settings group from the advanced UI definition, moves it to the bottom of the basic layout with all controls visible.
  - Return: {None} Applies UI side effects.
- fn `def selectedConversionMode(self)` (L283-290)
  - Brief: Returns selected conversion mode for Ghostscript execution.
  - Details: Maps GUI mode controls to backend mode tokens expected by command generation.
  - Return: {str} Conversion mode token (`frame` or `crop`).
- fn `def currentSelectionUpdated(self)` (L291-306)

### fn `def readSettings(self)` (L307-328)

### fn `def writeSettings(self)` (L329-346)

### fn `def openFile(self, fileName)` (L347-365)

### fn `def slotOpenFile(self)` (L366-371)

### fn `def slotSelectFile(self)` (L372-381)

### fn `def showWarning(self, title, text)` (L382-389)

### fn `def str2pages(self, s)` (L390-407)

### fn `def requestedUnsupportedGhostscriptOptions(self)` (L408-415)
- Brief: Lists GUI options unsupported by the Ghostscript backend.
- Details: Returns empty list because unsupported options were removed from conversion controls.
- Return: {list[str]} Unsupported option identifiers requested by the user.

### fn `def primarySelectionCropValue(self, page_indexes)` (L416-429)
- Brief: Gets primary selection crop tuple for conversion planning.
- Details: Resolves first available normalized crop tuple from current page first, then requested pages, and returns only the primary tuple used for all output pages.
- Param: page_indexes {list[int]} Ordered page indexes selected for processing.
- Return: {tuple[float,float,float,float]|None} Primary normalized crop tuple or None when no selections are available.

### fn `def buildGhostscriptCropPlan(self, inputFileName, outputFileName, requestedPageIndexes=None)` (L430-464)
- Brief: Builds single Ghostscript crop plan from GUI-derived parameters.
- Details: Iterates only requested pages (or all pages when omitted), derives geometry from the primary GUI selection tuple, computes crop bbox from page-size metadata, and emits one Ghostscript command for the full selected range using `-dFirstPage/-dLastPage`.
- Param: inputFileName {str} Source PDF path.
- Param: outputFileName {str} Destination cropped PDF path.
- Param: requestedPageIndexes {set[int]|None} Optional zero-based page-index filter derived from `--whichpages`.
- Return: {dict[str,object]|None} Crop plan containing selected page indexes and one Ghostscript command vector.

### fn `def createConversionProgressDialog(self, totalPages)` (L465-487)
- Brief: Creates modal conversion progress dialog for crop execution.
- Details: Configures progress dialog with deterministic page range and cancellable stop action used during long-running conversion command execution.
- Param: totalPages {int} Number of selected pages to process.
- Return: {QProgressDialog} Configured progress dialog instance.

### fn `def slotPdfFrame(self)` (L488-616)
- Brief: Executes PDF crop action using Ghostscript command backend.
- Details: Validates unsupported GUI options, verifies Ghostscript availability, builds one Ghostscript crop command from GUI state, and streams command output to update conversion progress across the selected page range.
- Return: {None} Triggers output PDF generation side effect.

### fn `def mark_page_processed(page_number)` (L548-566)
- Brief: Executes PDF crop action using Ghostscript command backend.
- Brief: Marks one selected page as processed for progress updates.
- Details: Validates unsupported GUI options, verifies Ghostscript availability, builds one Ghostscript crop command from GUI state, and streams command output to update conversion progress across the selected page range.
- Details: Updates dialog value and label only once per page number to keep deterministic monotonic progress during streamed subprocess output handling.
- Param: page_number {int} One-based page number reported by Ghostscript.
- Return: {None} Triggers output PDF generation side effect.
- Return: {None} Applies progress side effects.

### fn `def on_output_line(line)` (L567-581)
- Brief: Processes streamed Ghostscript output lines during conversion.
- Details: Uses parsed Ghostscript page numbers from captured output to advance conversion progress without forwarding captured command output to user-visible UI messages.
- Param: line {str} Single output line emitted by Ghostscript.
- Return: {None} Applies progress side effects.

### fn `def slotZoomIn(self)` (L617-620)

### fn `def slotZoomOut(self)` (L621-624)

### fn `def slotFitInView(self, checked)` (L625-629)

### fn `def slotSplitterMoved(self, pos, idx)` (L630-632)

### fn `def slotPreviousPage(self)` (L633-636)

### fn `def slotNextPage(self)` (L637-640)

### fn `def slotFirstPage(self)` (L641-644)

### fn `def slotLastPage(self)` (L645-648)

### fn `def slotCurrentPageEdited(self, text)` (L649-656)

### fn `def updateControls(self)` (L657-665)

### fn `def slotSelectionMode(self, checked)` (L666-669)

### fn `def slotSelExceptionsChanged(self)` (L670-672)

### fn `def slotSelExceptionsEdited(self, text)` (L673-677)

### fn `def slotSelAspectRatioChanged(self)` (L678-686)

### fn `def slotSelAspectRatioTypeChanged(self, index)` (L687-706)

### fn `def distributeAspectRatioChanged(self, aspectRatio)` (L707-709)

### fn `def slotDistributeAspectRatioChanged(self)` (L710-712)

### fn `def slotDeviceTypeChanged(self, index)` (L713-719)

### fn `def slotContextMenu(self, pos)` (L720-740)

### fn `def slotDeleteSelection(self)` (L741-744)

### fn `def slotNewSelection(self)` (L745-747)

### fn `def slotNewSelectionGrid(self)` (L748-757)

### fn `def createSelectionGrid(self, grid)` (L758-791)

### fn `def getPadding(self)` (L792-819)
- Brief: Returns trim padding in CSS-expanded order.
- Details: Reads trim padding text from the dedicated Basic-tab controls and expands one-to-four comma-separated values to `[top,right,bottom,left]`.
- Return: {list[float]} Padding tuple in top,right,bottom,left order.

### fn `def slotTrimMarginsAll(self)` (L820-832)

### fn `def slotTrimMargins(self)` (L833-837)

### fn `def trimMarginsSelection(self, sel)` (L838-916)
- Brief: Computes auto-trim rectangle for a selection using configured thresholds.
- Details: Reads sensitivity/allowed-changes from Basic-tab controls, selects page scope based on "Use all pages" checkbox (current page only when unchecked, all visible pages when checked), and applies auto-trim with padding and aspect-ratio adjustments.
- Param: sel {ViewerSelectionItem} Selection item to trim.
- Return: {None} Mutates selection bounding rectangle.

### fn `def resizeEvent(self, event)` (L917-919)

### fn `def closeEvent(self, event)` (L920-921)

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`AspectRatioType`|class|pub|41-46|class AspectRatioType|
|`AspectRatioType.__init__`|fn|priv|42-46|def __init__(self, name, width, height)|
|`AspectRatioTypeManager`|class|pub|47-99|class AspectRatioTypeManager|
|`AspectRatioTypeManager.__init__`|fn|priv|49-52|def __init__(self)|
|`AspectRatioTypeManager.__iter__`|fn|priv|53-55|def __iter__(self)|
|`AspectRatioTypeManager.addType`|fn|pub|56-58|def addType(self, name, width, height)|
|`AspectRatioTypeManager.getType`|fn|pub|59-63|def getType(self, index)|
|`AspectRatioTypeManager.addDefaults`|fn|pub|64-66|def addDefaults(self)|
|`AspectRatioTypeManager.settingsCaption`|fn|pub|67-69|def settingsCaption(self)|
|`AspectRatioTypeManager.saveTypes`|fn|pub|70-86|def saveTypes(self, settings)|
|`AspectRatioTypeManager.loadTypes`|fn|pub|87-99|def loadTypes(self, settings)|
|`SelAspectRatioTypeManager`|class|pub|100-113|class SelAspectRatioTypeManager(AspectRatioTypeManager)|
|`SelAspectRatioTypeManager.settingsCaption`|fn|pub|102-104|def settingsCaption(self)|
|`SelAspectRatioTypeManager.addDefaults`|fn|pub|105-113|def addDefaults(self)|
|`DeviceTypeManager`|class|pub|114-126|class DeviceTypeManager(AspectRatioTypeManager)|
|`DeviceTypeManager.settingsCaption`|fn|pub|116-118|def settingsCaption(self)|
|`DeviceTypeManager.addDefaults`|fn|pub|119-126|def addDefaults(self)|
|`MainWindow`|class|pub|127-326|class MainWindow(QMainWindow)|
|`MainWindow.__init__`|fn|priv|131-245|def __init__(self)|
|`MainWindow.viewer`|fn|pub|247-249|def viewer(self)|
|`MainWindow.selections`|fn|pub|251-253|def selections(self)|
|`MainWindow._setupConversionModeControls`|fn|priv|254-271|def _setupConversionModeControls(self)|
|`MainWindow._setupTrimSettingsControls`|fn|priv|272-282|def _setupTrimSettingsControls(self)|
|`MainWindow.selectedConversionMode`|fn|pub|283-290|def selectedConversionMode(self)|
|`MainWindow.currentSelectionUpdated`|fn|pub|291-306|def currentSelectionUpdated(self)|
|`readSettings`|fn|pub|307-328|def readSettings(self)|
|`writeSettings`|fn|pub|329-346|def writeSettings(self)|
|`openFile`|fn|pub|347-365|def openFile(self, fileName)|
|`slotOpenFile`|fn|pub|366-371|def slotOpenFile(self)|
|`slotSelectFile`|fn|pub|372-381|def slotSelectFile(self)|
|`showWarning`|fn|pub|382-389|def showWarning(self, title, text)|
|`str2pages`|fn|pub|390-407|def str2pages(self, s)|
|`requestedUnsupportedGhostscriptOptions`|fn|pub|408-415|def requestedUnsupportedGhostscriptOptions(self)|
|`primarySelectionCropValue`|fn|pub|416-429|def primarySelectionCropValue(self, page_indexes)|
|`buildGhostscriptCropPlan`|fn|pub|430-464|def buildGhostscriptCropPlan(self, inputFileName, outputF...|
|`createConversionProgressDialog`|fn|pub|465-487|def createConversionProgressDialog(self, totalPages)|
|`slotPdfFrame`|fn|pub|488-616|def slotPdfFrame(self)|
|`mark_page_processed`|fn|pub|548-566|def mark_page_processed(page_number)|
|`on_output_line`|fn|pub|567-581|def on_output_line(line)|
|`slotZoomIn`|fn|pub|617-620|def slotZoomIn(self)|
|`slotZoomOut`|fn|pub|621-624|def slotZoomOut(self)|
|`slotFitInView`|fn|pub|625-629|def slotFitInView(self, checked)|
|`slotSplitterMoved`|fn|pub|630-632|def slotSplitterMoved(self, pos, idx)|
|`slotPreviousPage`|fn|pub|633-636|def slotPreviousPage(self)|
|`slotNextPage`|fn|pub|637-640|def slotNextPage(self)|
|`slotFirstPage`|fn|pub|641-644|def slotFirstPage(self)|
|`slotLastPage`|fn|pub|645-648|def slotLastPage(self)|
|`slotCurrentPageEdited`|fn|pub|649-656|def slotCurrentPageEdited(self, text)|
|`updateControls`|fn|pub|657-665|def updateControls(self)|
|`slotSelectionMode`|fn|pub|666-669|def slotSelectionMode(self, checked)|
|`slotSelExceptionsChanged`|fn|pub|670-672|def slotSelExceptionsChanged(self)|
|`slotSelExceptionsEdited`|fn|pub|673-677|def slotSelExceptionsEdited(self, text)|
|`slotSelAspectRatioChanged`|fn|pub|678-686|def slotSelAspectRatioChanged(self)|
|`slotSelAspectRatioTypeChanged`|fn|pub|687-706|def slotSelAspectRatioTypeChanged(self, index)|
|`distributeAspectRatioChanged`|fn|pub|707-709|def distributeAspectRatioChanged(self, aspectRatio)|
|`slotDistributeAspectRatioChanged`|fn|pub|710-712|def slotDistributeAspectRatioChanged(self)|
|`slotDeviceTypeChanged`|fn|pub|713-719|def slotDeviceTypeChanged(self, index)|
|`slotContextMenu`|fn|pub|720-740|def slotContextMenu(self, pos)|
|`slotDeleteSelection`|fn|pub|741-744|def slotDeleteSelection(self)|
|`slotNewSelection`|fn|pub|745-747|def slotNewSelection(self)|
|`slotNewSelectionGrid`|fn|pub|748-757|def slotNewSelectionGrid(self)|
|`createSelectionGrid`|fn|pub|758-791|def createSelectionGrid(self, grid)|
|`getPadding`|fn|pub|792-819|def getPadding(self)|
|`slotTrimMarginsAll`|fn|pub|820-832|def slotTrimMarginsAll(self)|
|`slotTrimMargins`|fn|pub|833-837|def slotTrimMargins(self)|
|`trimMarginsSelection`|fn|pub|838-916|def trimMarginsSelection(self, sel)|
|`resizeEvent`|fn|pub|917-919|def resizeEvent(self, event)|
|`closeEvent`|fn|pub|920-921|def closeEvent(self, event)|


---

# mainwindowui_qt5.py | Python | 466L | 3 symbols | 1 imports | 7 comments
> Path: `src/pdfframe/mainwindowui_qt5.py`

## Imports
```
from PyQt5 import QtCore, QtGui, QtWidgets
```

## Definitions

### class `class Ui_MainWindow(object)` : object (L14-213)

### fn `def setupUi(self, MainWindow)` (L15-214)

### fn `def retranslateUi(self, MainWindow)` (L377-390)

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`Ui_MainWindow`|class|pub|14-213|class Ui_MainWindow(object)|
|`setupUi`|fn|pub|15-214|def setupUi(self, MainWindow)|
|`retranslateUi`|fn|pub|377-390|def retranslateUi(self, MainWindow)|


---

# mainwindowui_qt6.py | Python | 464L | 3 symbols | 1 imports | 6 comments
> Path: `src/pdfframe/mainwindowui_qt6.py`

## Imports
```
from PyQt6 import QtCore, QtGui, QtWidgets
```

## Definitions

### class `class Ui_MainWindow(object)` : object (L12-211)

### fn `def setupUi(self, MainWindow)` (L13-212)

### fn `def retranslateUi(self, MainWindow)` (L375-388)

## Symbol Index
|Symbol|Kind|Vis|Lines|Sig|
|---|---|---|---|---|
|`Ui_MainWindow`|class|pub|12-211|class Ui_MainWindow(object)|
|`setupUi`|fn|pub|13-212|def setupUi(self, MainWindow)|
|`retranslateUi`|fn|pub|375-388|def retranslateUi(self, MainWindow)|


---

# pdfframecmd.py | Python | 365L | 16 symbols | 8 imports | 15 comments
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

### fn `def build_ghostscript_page_crop_command(input_path, output_path, first_page,` (L166-235)
- Brief: Builds Ghostscript command vector for cropping a page range.
- Details: Assembles script-style pdfwrite command with BeginPage clipping for selected pages, using either physical crop (`crop`) or original-size clipped output (`frame`).
- Param: input_path {str} Source PDF path.
- Param: output_path {str} Destination output PDF path.
- Param: first_page {int} One-based first page index to process.
- Param: last_page {int} One-based last page index to process.
- Param: page_width {float} Target media width in points.
- Param: page_height {float} Target media height in points.
- Param: crop_box {tuple[float,float,float,float]} Crop box in left,bottom,right,top order.
- Param: mode {str} Conversion mode (`frame` or `crop`).
- Param: command_name {str} Executable name for Ghostscript binary.
- Return: {list[str]} Complete subprocess command vector.
- Throws: {ValueError} If mode is not supported or crop size is invalid.

### fn `def extract_ghostscript_page_numbers(line)` (L236-247)
- Brief: Extracts all processed page indices from Ghostscript output text.
- Details: Parses each output line that matches `^Page\\s+\\d+\\n` in the provided chunk and returns one-based page numbers in encounter order.
- Param: line {str} One output line or chunk produced by Ghostscript.
- Return: {list[int]} Processed page numbers found in the chunk.

### fn `def extract_ghostscript_page_number(line)` (L248-261)
- Brief: Extracts processed page index from Ghostscript output lines.
- Details: Parses `Page N` line format emitted by Ghostscript and returns one-based page number when a match is present.
- Param: line {str} One output line produced by Ghostscript.
- Return: {int|None} Processed page number or None when line does not contain page progress information.

### fn `def format_shell_command(command)` (L262-272)
- Brief: Formats command vectors into deterministic shell-escaped strings.
- Details: Serializes subprocess command vectors with POSIX shell escaping to provide exact reproducible command diagnostics.
- Param: command {list[str]} Subprocess command vector.
- Return: {str} Shell-escaped command string preserving argument boundaries.

### fn `def write_cropped_pages_output(output_file_name, cropped_page_paths)` (L273-295)
- Brief: Writes output PDF using only selected cropped page files.
- Details: Loads one-page cropped PDF files in provided order and writes a new output PDF that contains exactly those pages.
- Param: output_file_name {str} Destination PDF file path.
- Param: cropped_page_paths {list[str]} Ordered one-page cropped PDF paths selected for export.
- Return: {None} Writes assembled output PDF to filesystem.
- Throws: {ValueError} If no cropped pages are provided.

### fn `def run_ghostscript_command(command, event_pump=None, poll_interval=0.05,` (L296-365)
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

### fn `def reader()` (L325-332)
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
|`build_ghostscript_page_crop_command`|fn|pub|166-235|def build_ghostscript_page_crop_command(input_path, outpu...|
|`extract_ghostscript_page_numbers`|fn|pub|236-247|def extract_ghostscript_page_numbers(line)|
|`extract_ghostscript_page_number`|fn|pub|248-261|def extract_ghostscript_page_number(line)|
|`format_shell_command`|fn|pub|262-272|def format_shell_command(command)|
|`write_cropped_pages_output`|fn|pub|273-295|def write_cropped_pages_output(output_file_name, cropped_...|
|`run_ghostscript_command`|fn|pub|296-365|def run_ghostscript_command(command, event_pump=None, pol...|
|`reader`|fn|pub|325-332|def reader()|


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

