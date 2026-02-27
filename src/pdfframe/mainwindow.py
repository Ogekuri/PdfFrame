# -*- coding: iso-8859-1 -*-

"""
The main window of pdfframe

Copyright (C) 2010-2025 ogekuri, http://ogekuri.com
"""

"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

import sys
import re
from datetime import datetime
from os.path import splitext
from shutil import which

from pdfframe.qt import *
from pdfframe.config import PYQT6
from pdfframe.jsonconfig import DEFAULT_CONFIG_VALUES, JsonConfigStore

if PYQT6:
    from pdfframe.mainwindowui_qt6 import Ui_MainWindow
else:
    from pdfframe.mainwindowui_qt5 import Ui_MainWindow

from pdfframe.viewerselections import ViewerSelections, aspectRatioFromStr
from pdfframe.vieweritem import ViewerItem
from pdfframe.pdfframecmd import (
    GhostscriptCommandCancelledError,
    GhostscriptCommandError,
    build_ghostscript_page_crop_command,
    extract_ghostscript_page_numbers,
    normalized_crop_tuple_to_bbox,
    run_ghostscript_command,
)
from pdfframe.autotrim import autoTrimMargins


class AspectRatioType:
    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height

class AspectRatioTypeManager:

    def __init__(self):
        self.types = []
        self.defaultsUsed = False

    def __iter__(self):
        return iter(self.types)

    def addType(self, name, width, height):
        self.types.append(AspectRatioType(name, width, height))

    def getType(self, index):
        if index >= len(self.types):
            return None
        return self.types[index]

    def addDefaults(self):
        pass

    def settingsCaption(self):
        pass
  
    def saveTypes(self, settings):
        c = self.settingsCaption()
        # if the defaults have been used, we still write them to the config
        # file, making it easier for the user to edit/add, but we append
        # Defaults to the caption so that these get automatically overriden by
        # future versions of pdfframe (which may have updated defaults)
        if self.defaultsUsed:
            c += "Defaults"
        settings.beginWriteArray(c)
        for i in range(len(self.types)):
            t = self.types[i]
            settings.setArrayIndex(i)
            settings.setValue("Name", t.name)
            settings.setValue("Width", t.width)
            settings.setValue("Height", t.height)
        settings.endArray()
  
    def loadTypes(self, settings):
        count = settings.beginReadArray(self.settingsCaption())
        for i in range(count):
            settings.setArrayIndex(i)
            name = settings.value("Name")
            width = float(settings.value("Width"))
            height = float(settings.value("Height"))
            self.addType(name, width, height)
        settings.endArray()
        if count==0:
            self.defaultsUsed = True
            self.addDefaults()

class SelAspectRatioTypeManager(AspectRatioTypeManager):

    def settingsCaption(self):
        return "SelAspectRatios"

    def addDefaults(self):
        self.addType("Flexible aspect ratio", 0, 0)
        self.addType("A4/A5 etc.", 1, 1.414)
        self.addType("A4/A5 etc. (landscape)", 1.414, 1)
        self.addType("Letter", 8.5, 11)
        self.addType("Letter (landscape)", 11, 8.5)
        self.addType("Legal", 8.5, 14)
        self.addType("Legal (landscape)", 14, 8.5)

class DeviceTypeManager(AspectRatioTypeManager):

    def settingsCaption(self):
        return "DeviceTypes"

    def addDefaults(self):
        self.addType("No fitting", 0, 0)
        self.addType("4:3 eReader", 4, 3)
        self.addType("4:3 eReader (widescreen)", 3, 4)
        self.addType("Nook 1st Ed.", 600, 730)
        self.addType("Nook 1st Ed. (widescreen)", 730, 600)


class MainWindow(QMainWindow):

    fileName = None

    def __init__(self):
        QMainWindow.__init__(self)
        self.verbose = False
        self.debug = False
        self.configStore = JsonConfigStore()
        self.trimPresets = []
        self._updatingTrimPresetList = False

        self.selAspectRatioTypes = SelAspectRatioTypeManager()
        self.deviceTypes = DeviceTypeManager()

        self._viewer = ViewerItem(self)

        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        self._setupConversionModeControls()
        self._setupTrimSettingsControls()
        self._setupTrimPresetControls()
        self._setupTrimPresetAction()
        advanced_index = self.ui.tabWidget.indexOf(self.ui.tabAdvanced)
        if advanced_index >= 0:
            self.ui.tabWidget.removeTab(advanced_index)
        self.ui.checkIncludePagesWithoutSelections.setChecked(False)
        self.ui.checkIncludePagesWithoutSelections.hide()
        self.ui.groupSelectionMode.hide()
        self.selections.selectionMode = ViewerSelections.all
        self.selections.selectionExceptions = []

        # http://standards.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html
        self.setWindowIcon(QIcon.fromTheme('edit-cut'))
        self.ui.actionOpenFile.setIcon(QIcon.fromTheme('document-open'))
        self.ui.actionPdfFrame.setIcon(QIcon.fromTheme('face-smile'))
        self.ui.actionZoomIn.setIcon(QIcon.fromTheme('zoom-in'))
        self.ui.actionZoomOut.setIcon(QIcon.fromTheme('zoom-out'))
        self.ui.actionFitInView.setIcon(QIcon.fromTheme('zoom-fit-best'))
        self.ui.actionPreviousPage.setIcon(QIcon.fromTheme('go-previous'))
        self.ui.actionNextPage.setIcon(QIcon.fromTheme('go-next'))
        self.ui.actionFirstPage.setIcon(QIcon.fromTheme('go-first'))
        self.ui.actionLastPage.setIcon(QIcon.fromTheme('go-last'))
        self.ui.actionTrimMargins.setIcon(QIcon.fromTheme('transform-crop'))
        self.ui.actionTrimMarginsAll.setIcon(QIcon.fromTheme('transform-crop'))
        # self.ui.actionTrimMarginsAll.setIcon(QIcon.fromTheme('select-rectangular'))
        # self.ui.actionTrimMarginsAll.setIcon(QIcon.fromTheme('edit-guides'))
        self.ui.actionNewSelection.setIcon(QIcon.fromTheme('select-rectangular'))
        # self.ui.actionNewSelection.setIcon(QIcon.fromTheme('draw-rectangle'))
        self.ui.actionDeleteSelection.setIcon(QIcon.fromTheme('edit-delete'))

        if QIcon.hasThemeIcon('document-open'):
            self.ui.buttonFileSelect.setIcon(QIcon.fromTheme('document-open'))
        else:
            self.ui.buttonFileSelect.setText('...')
            self.ui.buttonFileSelect.setAutoRaise(False)

        if QIcon.hasThemeIcon('go-first') and QIcon.hasThemeIcon('go-previous') \
                and QIcon.hasThemeIcon('go-next') and QIcon.hasThemeIcon('go-last'):
            self.ui.buttonFirst.setIcon(QIcon.fromTheme('go-first'))
            self.ui.buttonPrevious.setIcon(QIcon.fromTheme('go-previous'))
            self.ui.buttonNext.setIcon(QIcon.fromTheme('go-next'))
            self.ui.buttonLast.setIcon(QIcon.fromTheme('go-last'))
        else:
            self.ui.buttonFirst.setText('<<')
            self.ui.buttonPrevious.setText('<')
            self.ui.buttonNext.setText('>')
            self.ui.buttonLast.setText('>>')
            self.ui.buttonFirst.setFlat(False)
            self.ui.buttonPrevious.setFlat(False)
            self.ui.buttonNext.setFlat(False)
            self.ui.buttonLast.setFlat(False)

        # we need to add the action to a widget in order for keyboard shortcuts to work
        self.addAction(self.ui.actionNewSelection)
        self.addAction(self.ui.actionNewSelectionGrid)
        self.addAction(self.ui.actionDeleteSelection)
        self.addAction(self.ui.actionFirstPage)
        self.addAction(self.ui.actionLastPage)

        self.ui.actionOpenFile.triggered.connect(self.slotOpenFile)
        self.ui.actionSelectFile.triggered.connect(self.slotSelectFile)
        self.ui.actionPdfFrame.triggered.connect(self.slotPdfFrame)
        self.ui.actionZoomIn.triggered.connect(self.slotZoomIn)
        self.ui.actionZoomOut.triggered.connect(self.slotZoomOut)
        self.ui.actionFitInView.toggled.connect(self.slotFitInView)
        self.ui.actionPreviousPage.triggered.connect(self.slotPreviousPage)
        self.ui.actionNextPage.triggered.connect(self.slotNextPage)
        self.ui.actionFirstPage.triggered.connect(self.slotFirstPage)
        self.ui.actionLastPage.triggered.connect(self.slotLastPage)
        self.ui.actionDeleteSelection.triggered.connect(self.slotDeleteSelection)
        self.ui.actionNewSelection.triggered.connect(self.slotNewSelection)
        self.ui.actionNewSelectionGrid.triggered.connect(self.slotNewSelectionGrid)
        self.ui.actionTrimMargins.triggered.connect(self.slotTrimMargins)
        self.ui.actionTrimMarginsAll.triggered.connect(self.slotTrimMarginsAll)
        self.ui.documentView.customContextMenuRequested.connect(self.slotContextMenu)
        self.ui.editCurrentPage.textEdited.connect(self.slotCurrentPageEdited)
        self.ui.splitter.splitterMoved.connect(self.slotSplitterMoved)
        self.ui.checkTrimPagesRange.toggled.connect(self._updateTrimPagesRangeControls)

        self.pdfScene = QGraphicsScene(self.ui.documentView)
        self.pdfScene.setBackgroundBrush(self.pdfScene.palette().dark())
        self.pdfScene.addItem(self.viewer)

        self.readSettings()

        # populate combobox with aspect ratio types
        for t in self.selAspectRatioTypes:
            self.ui.comboSelAspectRatioType.addItem(t.name)
        self.ui.comboSelAspectRatioType.addItem("Custom")
        # populate combobox with device types
        for t in self.deviceTypes:
            self.ui.comboDistributeDevice.addItem(t.name)
        self.ui.comboDistributeDevice.addItem("Custom")

        # disable Ghostscript option if gs is not available
        if not which('gs'):
            self.ui.checkGhostscript.setChecked(False)
            self.ui.checkGhostscript.setEnabled(False)

        self.ui.documentView.setScene(self.pdfScene)
        self.ui.documentView.setFocus()


    @property
    def viewer(self):
        return self._viewer

    @property
    def selections(self):
        return self.viewer.selections

    def _setupConversionModeControls(self):
        """
        @brief Adds conversion mode controls to the basic tab.
        @details Creates `Mode` group with `Frame` and `Crop` radio buttons, defaults to `Frame`, and inserts it into the basic-tab layout.
        @return {None} Applies UI side effects.
        """
        self.groupMode = QGroupBox(self.ui.tabBasic)
        self.groupMode.setTitle(self.tr("Mode"))
        mode_layout = QVBoxLayout(self.groupMode)
        self.radioModeFrame = QRadioButton(self.groupMode)
        self.radioModeFrame.setText(self.tr("Frame"))
        self.radioModeFrame.setChecked(True)
        self.radioModeCrop = QRadioButton(self.groupMode)
        self.radioModeCrop.setText(self.tr("Crop"))
        mode_layout.addWidget(self.radioModeFrame)
        mode_layout.addWidget(self.radioModeCrop)
        self.ui.verticalLayout_4.insertWidget(3, self.groupMode)

    def _setupTrimSettingsControls(self):
        """
        @brief Relocates trim configuration controls into the Basic tab.
        @details Reuses the existing trim-settings group from the advanced UI definition, moves it to the bottom of the basic layout with all controls visible.
        @return {None} Applies UI side effects.
        """
        self.ui.verticalLayout_5.removeWidget(self.ui.groupTrimMargins)
        self.ui.groupTrimMargins.setParent(self.ui.tabBasic)
        self.ui.groupTrimMargins.setTitle(self.tr("Trim settings"))
        self.ui.verticalLayout_4.insertWidget(self.ui.verticalLayout_4.count() - 1, self.ui.groupTrimMargins)

    def _setupTrimPresetControls(self):
        """
        @brief Adds trim preset controls under trim settings.
        @details Creates a `Presets` section with editable list rows and per-row remove buttons, then wires click/double-click/item-change signals for apply/rename flows.
        @return {None} Applies UI side effects.
        """
        self.groupTrimPresets = QGroupBox(self.ui.groupTrimMargins)
        self.groupTrimPresets.setTitle(self.tr("Presets"))
        group_layout = QVBoxLayout(self.groupTrimPresets)
        self.treeTrimPresets = QTreeWidget(self.groupTrimPresets)
        self.treeTrimPresets.setColumnCount(2)
        self.treeTrimPresets.setHeaderHidden(True)
        self.treeTrimPresets.setRootIsDecorated(False)
        self.treeTrimPresets.setUniformRowHeights(True)
        if PYQT6:
            self.treeTrimPresets.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        else:
            self.treeTrimPresets.setEditTriggers(QAbstractItemView.NoEditTriggers)
        header = self.treeTrimPresets.header()
        if PYQT6:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        else:
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        group_layout.addWidget(self.treeTrimPresets)
        self.ui.gridLayout_3.addWidget(self.groupTrimPresets, 6, 0, 1, 2)
        self.treeTrimPresets.itemClicked.connect(self.slotTrimPresetClicked)
        self.treeTrimPresets.itemDoubleClicked.connect(self.slotTrimPresetDoubleClicked)
        self.treeTrimPresets.itemChanged.connect(self.slotTrimPresetChanged)

    def _setupTrimPresetAction(self):
        """
        @brief Adds the `Save Margins` toolbar action next to trim action.
        @details Inserts a dedicated action directly to the right of `Trim Margins`, then binds it to preset creation and keeps it disabled until a PDF is loaded.
        @return {None} Applies UI side effects.
        """
        self.actionSaveMargins = QAction(self)
        self.actionSaveMargins.setText(self.tr("Save Margins"))
        self.actionSaveMargins.setEnabled(False)
        self.actionSaveMargins.triggered.connect(self.slotSaveMarginsPreset)
        toolbar_actions = self.ui.toolBar.actions()
        insert_before = None
        if self.ui.actionTrimMarginsAll in toolbar_actions:
            index = toolbar_actions.index(self.ui.actionTrimMarginsAll)
            if index + 1 < len(toolbar_actions):
                insert_before = toolbar_actions[index + 1]
        self.ui.toolBar.insertAction(insert_before, self.actionSaveMargins)

    def _trimPresetEditableFlag(self):
        if PYQT6:
            return Qt.ItemFlag.ItemIsEditable
        return Qt.ItemIsEditable

    def _trimPresetRole(self):
        if PYQT6:
            return Qt.ItemDataRole.UserRole
        return Qt.UserRole

    def _defaultTrimPresetName(self):
        """
        @brief Returns default trim preset name.
        @details Generates timestamp name in `%Y/%m/%d %H:%M:%S` format.
        @return {str} Default preset display label.
        """
        return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    def _toBool(self, value):
        """
        @brief Normalizes persisted boolean-like values.
        @details Accepts bools and common string tokens produced by historical settings writers.
        @param value {object} Input value from settings/config source.
        @return {bool} Parsed boolean result.
        """
        if isinstance(value, bool):
            return value
        return str(value).strip().lower() in ("1", "true", "yes", "on")

    def _updateTrimPagesRangeControls(self, enabled):
        """
        @brief Updates `Pages range` control enabled state.
        @details Enables range input only when trim-range mode is active and ensures default text `1-1` when empty.
        @param enabled {bool} State propagated from trim-range toggle.
        @return {None} Applies UI side effects.
        """
        self.ui.editTrimPagesRange.setEnabled(enabled)
        if not self.ui.editTrimPagesRange.text().strip():
            self.ui.editTrimPagesRange.setText("1-1")

    def _parseTrimPagesRange(self):
        """
        @brief Parses and validates the trim pages range expression.
        @details Accepts only `N-M` one-based inclusive format, validates positive ordered bounds, and converts to zero-based bounds.
        @return {tuple[int,int]} `(start_index, end_index)` inclusive zero-based page bounds.
        @throws {ValueError} If the range is missing or syntactically/semantically invalid.
        """
        text = self.ui.editTrimPagesRange.text().strip()
        match = re.fullmatch(r"(\d+)\s*-\s*(\d+)", text)
        if not match:
            raise ValueError("bad trim pages range format")
        page_start = int(match.group(1))
        page_end = int(match.group(2))
        if page_start <= 0 or page_end <= 0 or page_start > page_end:
            raise ValueError("bad trim pages range bounds")
        return page_start - 1, page_end - 1

    def _collectRuntimeConfigValues(self):
        """
        @brief Collects runtime config values mapped to JSON `config` keys.
        @details Converts current UI control state into serializable values for `~/.pdfframe/config.json`.
        @return {dict[str,object]} Persistable runtime config key/value mapping.
        """
        return {
            "PDF/Optimize": "gs" if self.ui.checkGhostscript.isChecked() else "no",
            "PDF/Mode": self.selectedConversionMode(),
            "Trim/Padding": self.ui.editPadding.text(),
            "Trim/GrayscaleSensitivity": self.ui.editGrayscaleSensitivity.text(),
            "Trim/Sensitivity": self.ui.editSensitivity.text(),
            "Trim/PagesRangeEnabled": self.ui.checkTrimPagesRange.isChecked(),
            "Trim/PagesRange": self.ui.editTrimPagesRange.text(),
        }

    def _trimPresetFromCurrentSelection(self):
        """
        @brief Creates a trim preset payload from current UI state.
        @details Captures mode and trim parameters plus the primary current-page crop tuple when available.
        @return {dict[str,object]} New preset payload ready for persistence.
        """
        preset = {
            "name": self._defaultTrimPresetName(),
            "mode": self.selectedConversionMode(),
            "padding": self.ui.editPadding.text(),
            "grayscale_sensitivity": self.ui.editGrayscaleSensitivity.text(),
            "sensitivity": self.ui.editSensitivity.text(),
            "pages_range_enabled": self.ui.checkTrimPagesRange.isChecked(),
            "pages_range": self.ui.editTrimPagesRange.text(),
        }
        crop_values = self.viewer.cropValues(self.viewer.currentPageIndex)
        if crop_values:
            preset["crop"] = [float(value) for value in crop_values[0]]
        return preset

    def _refreshTrimPresetList(self):
        """
        @brief Rebuilds trim preset tree rows from in-memory presets.
        @details Clears the list, creates editable name rows, and attaches one remove button per row mapped to preset index inside a right-aligned cell container.
        @return {None} Applies UI side effects.
        """
        self._updatingTrimPresetList = True
        try:
            self.treeTrimPresets.clear()
            for index, preset in enumerate(self.trimPresets):
                name = str(preset.get("name") or self._defaultTrimPresetName())
                item = QTreeWidgetItem([name, ""])
                item.setFlags(item.flags() | self._trimPresetEditableFlag())
                item.setData(0, self._trimPresetRole(), index)
                self.treeTrimPresets.addTopLevelItem(item)
                remove_button = QPushButton("-", self.treeTrimPresets)
                remove_button.setMaximumWidth(24)
                remove_button.setProperty("preset_index", index)
                remove_button.clicked.connect(self.slotDeleteTrimPreset)
                row_widget = QWidget(self.treeTrimPresets)
                row_layout = QHBoxLayout(row_widget)
                row_layout.setContentsMargins(0, 0, 0, 0)
                row_layout.setSpacing(0)
                row_layout.addStretch(1)
                row_layout.addWidget(remove_button)
                self.treeTrimPresets.setItemWidget(item, 1, row_widget)
        finally:
            self._updatingTrimPresetList = False

    def _persistTrimPresetDocument(self):
        """
        @brief Persists runtime config and preset list to JSON config file.
        @details Writes both `config` values and `presets` array through JsonConfigStore, surfacing warning on I/O failures.
        @return {None} Writes `~/.pdfframe/config.json`.
        """
        document = {
            "config": self._collectRuntimeConfigValues(),
            "presets": self.trimPresets,
        }
        try:
            self.configStore.save(document)
        except (OSError, ValueError, TypeError) as err:
            self.showWarning(
                self.tr("Could not write config file"),
                self.tr("Failed to save ~/.pdfframe/config.json:\n\n{0}").format(err),
            )

    def _applyCropPreset(self, crop_values):
        """
        @brief Applies normalized crop tuple to current selection.
        @details Maps `[left,top,right,bottom]` normalized margins to viewer coordinates and updates (or creates) the current selection.
        @param crop_values {list[float]} Normalized crop tuple values.
        @return {None} Mutates current selection geometry.
        """
        if self.viewer.isEmpty():
            return
        if not isinstance(crop_values, (list, tuple)) or len(crop_values) != 4:
            return
        left, top, right, bottom = [float(value) for value in crop_values]
        left = min(1.0, max(0.0, left))
        top = min(1.0, max(0.0, top))
        right = min(1.0, max(0.0, right))
        bottom = min(1.0, max(0.0, bottom))
        if left + right >= 1.0 or top + bottom >= 1.0:
            return

        page_rect = self.viewer.irect
        rect_left = page_rect.left() + left * page_rect.width()
        rect_top = page_rect.top() + top * page_rect.height()
        rect_right = page_rect.right() - right * page_rect.width()
        rect_bottom = page_rect.bottom() - bottom * page_rect.height()
        target_rect = QRectF(QPointF(rect_left, rect_top), QPointF(rect_right, rect_bottom)).normalized()
        if target_rect.isEmpty():
            return
        selection = self.selections.currentSelection or self.selections.addSelection()
        local_rect = selection.mapRectFromParent(target_rect)
        selection.setBoundingRect(local_rect.topLeft(), local_rect.bottomRight())
        self.pdfScene.update()

    def _applyTrimPreset(self, index):
        """
        @brief Applies one stored preset to current runtime controls.
        @details Restores mode and trim values, then applies saved crop tuple when present.
        @param index {int} Preset list index.
        @return {None} Applies UI and selection updates.
        """
        if index < 0 or index >= len(self.trimPresets):
            return
        preset = self.trimPresets[index]
        mode = str(preset.get("mode", self.selectedConversionMode()))
        self.radioModeFrame.setChecked(mode != "crop")
        self.radioModeCrop.setChecked(mode == "crop")
        self.ui.editPadding.setText(str(preset.get("padding", self.ui.editPadding.text())))
        self.ui.editGrayscaleSensitivity.setText(
            str(preset.get("grayscale_sensitivity", self.ui.editGrayscaleSensitivity.text()))
        )
        self.ui.editSensitivity.setText(str(preset.get("sensitivity", self.ui.editSensitivity.text())))
        self.ui.checkTrimPagesRange.setChecked(
            self._toBool(preset.get("pages_range_enabled", self.ui.checkTrimPagesRange.isChecked()))
        )
        self.ui.editTrimPagesRange.setText(str(preset.get("pages_range", self.ui.editTrimPagesRange.text())))
        self._updateTrimPagesRangeControls(self.ui.checkTrimPagesRange.isChecked())
        if "crop" in preset:
            self._applyCropPreset(preset.get("crop"))

    def slotTrimPresetClicked(self, item, column):
        """
        @brief Applies a preset when the preset name cell is clicked.
        @details Ignores delete-button column and list rebuild events.
        @param item {QTreeWidgetItem} Clicked row item.
        @param column {int} Clicked column index.
        @return {None} Applies preset side effects.
        """
        if self._updatingTrimPresetList or column != 0:
            return
        index = self.treeTrimPresets.indexOfTopLevelItem(item)
        self._applyTrimPreset(index)

    def slotTrimPresetDoubleClicked(self, item, column):
        """
        @brief Starts inline rename for preset names.
        @details Enables user-driven preset rename on double-click of first column.
        @param item {QTreeWidgetItem} Double-clicked row item.
        @param column {int} Double-clicked column index.
        @return {None} Opens in-place editor.
        """
        if column == 0:
            self.treeTrimPresets.editItem(item, 0)

    def slotTrimPresetChanged(self, item, column):
        """
        @brief Persists preset rename changes from inline editing.
        @details Normalizes empty labels to timestamp defaults and rewrites JSON config after updates.
        @param item {QTreeWidgetItem} Changed row item.
        @param column {int} Changed column index.
        @return {None} Persists preset list updates.
        """
        if self._updatingTrimPresetList or column != 0:
            return
        index = self.treeTrimPresets.indexOfTopLevelItem(item)
        if index < 0 or index >= len(self.trimPresets):
            return
        name = item.text(0).strip()
        if not name:
            name = self._defaultTrimPresetName()
            self._updatingTrimPresetList = True
            try:
                item.setText(0, name)
            finally:
                self._updatingTrimPresetList = False
        self.trimPresets[index]["name"] = name
        self._persistTrimPresetDocument()

    def slotDeleteTrimPreset(self):
        """
        @brief Deletes one preset from remove-button click.
        @details Resolves row index from sender button metadata, updates in-memory list, refreshes UI, and persists JSON state.
        @return {None} Applies preset delete side effects.
        """
        button = self.sender()
        if button is None:
            return
        preset_index = button.property("preset_index")
        if preset_index is None:
            return
        index = int(preset_index)
        if index < 0 or index >= len(self.trimPresets):
            return
        del self.trimPresets[index]
        self._refreshTrimPresetList()
        self._persistTrimPresetDocument()

    def slotSaveMarginsPreset(self):
        """
        @brief Saves current crop/trim state as a new preset.
        @details Captures active control values, appends new preset with timestamp default name, refreshes list, and persists JSON state.
        @return {None} Applies preset creation side effects.
        """
        if self.viewer.isEmpty():
            return
        self.trimPresets.append(self._trimPresetFromCurrentSelection())
        self._refreshTrimPresetList()
        self._persistTrimPresetDocument()

    def selectedConversionMode(self):
        """
        @brief Returns selected conversion mode for Ghostscript execution.
        @details Maps GUI mode controls to backend mode tokens expected by command generation.
        @return {str} Conversion mode token (`frame` or `crop`).
        """
        return "crop" if self.radioModeCrop.isChecked() else "frame"

    def currentSelectionUpdated(self):
        sel = self.selections.currentSelection
        if sel:
            r = sel.boundingRect()
            self.ui.groupCurrentSel.setEnabled(True)
            index, s = sel.aspectRatioData
            self.ui.comboSelAspectRatioType.setCurrentIndex(index)
            self.ui.editSelAspectRatio.setText(s)
            if index == 0:
                w, h = int(r.width()), int(r.height())
                self.ui.editSelAspectRatio.setText("{} : {}".format(w, h))
        else:
            self.ui.comboSelAspectRatioType.setCurrentIndex(0)
            self.ui.editSelAspectRatio.setText("")
            self.ui.groupCurrentSel.setEnabled(False)

    def readSettings(self):
        """
        @brief Reads persisted runtime settings from QSettings and JSON config.
        @details Restores window geometry from QSettings, loads trim/runtime defaults from `~/.pdfframe/config.json`, and refreshes preset UI entries.
        @return {None} Applies UI state restoration side effects.
        """
        settings = QSettings()
        geometry = settings.value("Window/Geometry", "")
        if geometry:
            self.restoreGeometry(geometry)
        splitter = settings.value("Window/Splitter", "")
        if splitter:
            self.ui.splitter.restoreState(splitter)
        self.ui.actionFitInView.setChecked(settings.value("Window/FitInView", "") == "true")
        config_document = None
        try:
            config_document = self.configStore.load_or_initialize()
        except (OSError, ValueError, TypeError) as err:
            self.showWarning(
                self.tr("Could not read config file"),
                self.tr("Failed to load ~/.pdfframe/config.json:\n\n{0}").format(err),
            )
        config_values = dict(DEFAULT_CONFIG_VALUES)
        if config_document is not None:
            config_values.update(config_document.get("config", {}))
            self.trimPresets = list(config_document.get("presets", []))
        else:
            self.trimPresets = []

        optimize = str(config_values.get("PDF/Optimize", "gs"))
        self.ui.checkGhostscript.setChecked(optimize == "gs")
        mode = settings.value("PDF/Mode", "frame")
        mode = str(config_values.get("PDF/Mode", mode) or mode)
        self.radioModeFrame.setChecked(mode != "crop")
        self.radioModeCrop.setChecked(mode == "crop")
        self.ui.editPadding.setText(str(config_values.get("Trim/Padding", "0") or "0"))
        self.ui.editGrayscaleSensitivity.setText(str(config_values.get("Trim/GrayscaleSensitivity", "0") or "0"))
        self.ui.editSensitivity.setText(str(config_values.get("Trim/Sensitivity", "5") or "5"))
        self.ui.checkTrimPagesRange.setChecked(
            self._toBool(config_values.get("Trim/PagesRangeEnabled", False))
        )
        self.ui.editTrimPagesRange.setText(str(config_values.get("Trim/PagesRange", "1-1") or "1-1"))
        self._updateTrimPagesRangeControls(self.ui.checkTrimPagesRange.isChecked())

        self.selAspectRatioTypes.loadTypes(settings)
        self.deviceTypes.loadTypes(settings)
        self._refreshTrimPresetList()

    def writeSettings(self):
        """
        @brief Persists runtime settings to legacy and JSON backends.
        @details Writes window/session metadata to QSettings and writes trim/runtime config plus presets to `~/.pdfframe/config.json`.
        @return {None} Persists runtime state.
        """
        settings = QSettings()
        settings.setValue("Window/Geometry", self.saveGeometry())
        settings.setValue("Window/Splitter", self.ui.splitter.saveState())
        settings.setValue("Window/FitInView", "true" if
                self.ui.actionFitInView.isChecked() else "false")
        settings.setValue("PDF/Optimize", "gs" if
                self.ui.checkGhostscript.isChecked() else "no")
        settings.setValue("PDF/Mode", self.selectedConversionMode())
        settings.setValue("Trim/Padding", self.ui.editPadding.text())
        settings.setValue("Trim/GrayscaleSensitivity", self.ui.editGrayscaleSensitivity.text())
        settings.setValue("Trim/Sensitivity", self.ui.editSensitivity.text())
        settings.setValue("Trim/PagesRangeEnabled", "true" if
                self.ui.checkTrimPagesRange.isChecked() else "false")
        settings.setValue("Trim/PagesRange", self.ui.editTrimPagesRange.text())

        self.selAspectRatioTypes.saveTypes(settings)
        self.deviceTypes.saveTypes(settings)
        self._persistTrimPresetDocument()

    def openFile(self, fileName):
        if fileName:
            self.viewer.load(fileName)
            if not self.viewer.isEmpty():
                self.fileName = fileName
                outputFileName = "%s-cropped.pdf" % splitext(fileName)[0]
                self.slotFitInView(self.ui.actionFitInView.isChecked())
            else:
                self.fileName = ''
                outputFileName = ''
                self.showWarning(self.tr("Something got in our way"),
                        self.tr("The PDF file couldn't be read. "
                            "Please check the file and its permissions."))
            self.setWindowFilePath(self.fileName)
            self.ui.actionPdfFrame.setEnabled(not self.viewer.isEmpty())
            self.ui.actionTrimMarginsAll.setEnabled(not self.viewer.isEmpty())
            self.actionSaveMargins.setEnabled(not self.viewer.isEmpty())
            self.ui.editFile.setText(outputFileName)
            self.updateControls()

    def slotOpenFile(self):
        fileName = QFileDialog.getOpenFileName(self,
             self.tr("Open PDF"), "", self.tr("PDF Files (*.pdf)"));
        fileName = fileName[0]
        self.openFile(fileName)

    def slotSelectFile(self):
        fileName = QFileDialog.getSaveFileName(self,
                self.tr("Save cropped PDF to ..."), "", self.tr("PDF Files (*.pdf)"))
                # None, QFileDialog.DontConfirmOverwrite)
        try:
            self.ui.editFile.setText(fileName)
        except TypeError:
            # new versions of Qt return a tuple (fileName, selectedFilter)
            self.ui.editFile.setText(fileName[0])

    def showWarning(self, title, text):
        # if pdfframe is called with parameter --go, then the main window is never
        # shown; in that case, we output the warning to the shell
        if self.isVisible():
            QMessageBox.warning(self, title, text)
        else:
            sys.stderr.write(self.tr('WARNING: ') + title + '\n' + text + '\n')

    def str2pages(self, s):
        token = s.strip()
        if not token or "," in token:
            raise ValueError("Unsupported page-range format.")
        if "-" not in token:
            page = int(token)
            if page <= 0:
                raise ValueError("Page numbers must be positive.")
            return [page - 1]
        start_str, end_str = [part.strip() for part in token.split("-", 1)]
        if not start_str and not end_str:
            raise ValueError("Empty page range.")
        start = int(start_str) if start_str else 1
        end = int(end_str) if end_str else self.viewer.numPages()
        if start <= 0 or end <= 0 or start > end:
            raise ValueError("Invalid page range bounds.")
        return list(range(start - 1, end))

    def requestedUnsupportedGhostscriptOptions(self):
        """
        @brief Lists GUI options unsupported by the Ghostscript backend.
        @details Returns empty list because unsupported options were removed from conversion controls.
        @return {list[str]} Unsupported option identifiers requested by the user.
        """
        return []

    def primarySelectionCropValue(self, page_indexes):
        """
        @brief Gets primary selection crop tuple for conversion planning.
        @details Resolves first available normalized crop tuple from current page first, then requested pages, and returns only the primary tuple used for all output pages.
        @param page_indexes {list[int]} Ordered page indexes selected for processing.
        @return {tuple[float,float,float,float]|None} Primary normalized crop tuple or None when no selections are available.
        """
        indexes = [self.viewer.currentPageIndex] + [i for i in page_indexes if i != self.viewer.currentPageIndex]
        for page_index in indexes:
            crop_values = self.viewer.cropValues(page_index)
            if crop_values:
                return crop_values[0]
        return None

    def buildGhostscriptCropPlan(self, inputFileName, outputFileName, requestedPageIndexes=None):
        """
        @brief Builds single Ghostscript crop plan from GUI-derived parameters.
        @details Iterates only requested pages (or all pages when omitted), derives geometry from the primary GUI selection tuple, computes crop bbox from page-size metadata, and emits one Ghostscript command for the full selected range using `-dFirstPage/-dLastPage`.
        @param inputFileName {str} Source PDF path.
        @param outputFileName {str} Destination cropped PDF path.
        @param requestedPageIndexes {set[int]|None} Optional zero-based page-index filter derived from `--whichpages`.
        @return {dict[str,object]|None} Crop plan containing selected page indexes and one Ghostscript command vector.
        """
        if requestedPageIndexes is None:
            page_indexes = list(range(self.viewer.numPages()))
        else:
            page_indexes = sorted(requestedPageIndexes)
        if not page_indexes:
            return None
        primary_crop_value = self.primarySelectionCropValue(page_indexes)
        if primary_crop_value is None:
            return None
        conversion_mode = self.selectedConversionMode()
        first_page = page_indexes[0] + 1
        last_page = page_indexes[-1] + 1
        width, height = self.viewer.pageGetSizePoints(page_indexes[0])
        crop_box = normalized_crop_tuple_to_bbox(primary_crop_value, width, height)
        command = build_ghostscript_page_crop_command(
            inputFileName,
            outputFileName,
            first_page=first_page,
            last_page=last_page,
            page_width=width,
            page_height=height,
            crop_box=crop_box,
            mode=conversion_mode,
        )
        return {"page_indexes": page_indexes, "command": command}

    def createConversionProgressDialog(self, totalPages):
        """
        @brief Creates modal conversion progress dialog for crop execution.
        @details Configures progress dialog with deterministic page range and cancellable stop action used during long-running conversion command execution.
        @param totalPages {int} Number of selected pages to process.
        @return {QProgressDialog} Configured progress dialog instance.
        """
        maximum = totalPages if totalPages > 0 else 1
        dialog = QProgressDialog(
            self.tr("Converting selected page 0 of {0}...").format(totalPages),
            self.tr("Stop conversion"),
            0,
            maximum,
            self,
        )
        dialog.setWindowTitle(self.tr("Conversion progress"))
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        dialog.setMinimumDuration(0)
        dialog.setAutoClose(False)
        dialog.setAutoReset(False)
        dialog.setValue(0)
        return dialog

    def slotPdfFrame(self):
        """
        @brief Executes PDF crop action using Ghostscript command backend.
        @details Validates unsupported GUI options, verifies Ghostscript availability, builds one Ghostscript crop command from GUI state, and streams command output to update conversion progress across the selected page range.
        @return {None} Triggers output PDF generation side effect.
        """
        inputFileName = self.fileName
        outputFileName = self.ui.editFile.text()
        unsupported = self.requestedUnsupportedGhostscriptOptions()
        if unsupported:
            self.showWarning(self.tr("Unsupported options for Ghostscript backend"),
                    self.tr("Ghostscript backend does not support the requested options:\n\n{0}").format(
                        ", ".join(unsupported)))
            return
        if not which('gs'):
            self.showWarning(self.tr("Missing Ghostscript executable"),
                    self.tr("Could not find `gs` on PATH. "
                        "Please install Ghostscript and retry."))
            return

        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        progress_dialog = None
        try:
            requested_page_indexes = None
            whichpages_text = self.ui.editWhichPages.text().strip()
            if whichpages_text:
                try:
                    requested_page_indexes = {
                        page_index for page_index in self.str2pages(whichpages_text)
                        if 0 <= page_index < self.viewer.numPages()
                    }
                except Exception:
                    self.showWarning(self.tr("Bad value for --whichpages"),
                            self.tr("The value of --whichpages must be one range in one of these forms: `N`, `N-`, `-N`, or `N-M`."))
                    return
                if not requested_page_indexes:
                    self.showWarning(self.tr("No pages selected by --whichpages"),
                            self.tr("The selected --whichpages range does not match any page in the current document."))
                    return

            plan = self.buildGhostscriptCropPlan(
                inputFileName,
                outputFileName,
                requestedPageIndexes=requested_page_indexes)
            if not plan:
                self.showWarning(self.tr("No pages selected for cropping"),
                        self.tr("No GUI selections are visible on any page, so no cropped output can be generated."))
                return

            total_pages = len(plan["page_indexes"])
            selected_page_numbers = [page_index + 1 for page_index in plan["page_indexes"]]
            selected_page_number_set = set(selected_page_numbers)
            relative_to_selected_page = {
                offset + 1: page_number for offset, page_number in enumerate(selected_page_numbers)
            }
            progress_dialog = self.createConversionProgressDialog(total_pages)
            processed_pages = set()
            if self.verbose:
                sys.stderr.write(self.tr("Starting conversion for {0} selected pages.\n").format(total_pages))

            def mark_page_processed(page_number):
                """
                @brief Marks one selected page as processed for progress updates.
                @details Updates dialog value and label only once per page number to keep deterministic monotonic progress during streamed subprocess output handling.
                @param page_number {int} One-based page number reported by Ghostscript.
                @return {None} Applies progress side effects.
                """
                if page_number in processed_pages:
                    return
                processed_pages.add(page_number)
                processed_count = min(len(processed_pages), total_pages)
                progress_dialog.setValue(processed_count)
                progress_dialog.setLabelText(self.tr(
                    "Converting selected page {0} of {1}...").format(
                        processed_count, total_pages))
                if self.verbose:
                    sys.stderr.write(self.tr("Processed page {0} ({1}/{2}).\n").format(
                        page_number, processed_count, total_pages))

            def on_output_line(line):
                """
                @brief Processes streamed Ghostscript output lines during conversion.
                @details Uses parsed Ghostscript page numbers from captured output to advance conversion progress without forwarding captured command output to user-visible UI messages.
                @param line {str} Single output line emitted by Ghostscript.
                @return {None} Applies progress side effects.
                """
                for page_number in extract_ghostscript_page_numbers(line):
                    if page_number in selected_page_number_set:
                        mark_page_processed(page_number)
                        continue
                    mapped_page_number = relative_to_selected_page.get(page_number)
                    if mapped_page_number is not None:
                        mark_page_processed(mapped_page_number)

            progress_dialog.show()
            run_ghostscript_command(
                plan["command"],
                event_pump=QApplication.processEvents,
                output_callback=on_output_line,
                cancel_requested=progress_dialog.wasCanceled,
                log_command=self.verbose and self.debug,
                debug_output=self.verbose and self.debug,
            )
            progress_dialog.setValue(progress_dialog.maximum())
            if self.verbose:
                sys.stderr.write(self.tr("Conversion completed.\n"))
        except GhostscriptCommandCancelledError:
            self.showWarning(self.tr("Conversion interrupted"),
                    self.tr("The PDF conversion was stopped by user request."))
        except GhostscriptCommandError as err:
            command = " ".join(err.command)
            self.showWarning(self.tr("Could not crop PDF using Ghostscript"),
                    self.tr("Command failed:\n{0}").format(command))
        except IOError as err:
            self.showWarning(self.tr("Could not write cropped PDF"),
                    self.tr("An error occured while writing the cropped PDF. "
                        "Please make sure that you have permission to write to "
                        "the selected file."
                        "\n\nThe official error is:\n\n{0}").format(err))
        except Exception as err:
            self.showWarning(self.tr("Something got in our way"),
                    self.tr("The following unexpected error has occured:"
                    "\n\n{0}").format(err))
            raise err
        finally:
            if progress_dialog is not None:
                progress_dialog.close()
            QApplication.restoreOverrideCursor()

    def slotZoomIn(self):
        self.ui.actionFitInView.setChecked(False)
        self.ui.documentView.scale(1.2, 1.2)

    def slotZoomOut(self):
        self.ui.actionFitInView.setChecked(False)
        self.ui.documentView.scale(1/1.2, 1/1.2)

    def slotFitInView(self, checked):
        if checked:
            self.ui.documentView.fitInView(self.pdfScene.sceneRect(),
                    Qt.AspectRatioMode.KeepAspectRatio)

    def slotSplitterMoved(self, pos, idx):
        self.slotFitInView(self.ui.actionFitInView.isChecked())

    def slotPreviousPage(self):
        self.viewer.previousPage()
        self.updateControls()

    def slotNextPage(self):
        self.viewer.nextPage()
        self.updateControls()

    def slotFirstPage(self):
        self.viewer.firstPage()
        self.updateControls()

    def slotLastPage(self):
        self.viewer.lastPage()
        self.updateControls()

    def slotCurrentPageEdited(self, text):
        try:
            n = int(text)
            self.viewer.currentPageIndex = n-1
            self.updateControls()
        except ValueError:
            pass

    def updateControls(self):
        cur = ''
        num = ''
        if not self.viewer.isEmpty():
            cur = str(self.viewer.currentPageIndex+1)
            num = str(self.viewer.numPages())
        self.ui.editCurrentPage.setText(cur)
        self.ui.editMaxPage.setText(num)

    def slotSelectionMode(self, checked):
        del checked
        self.selections.selectionMode = ViewerSelections.all

    def slotSelExceptionsChanged(self):
        self.selections.selectionExceptions = []

    def slotSelExceptionsEdited(self, text):
        del text
        self.selections.selectionExceptions = []


    def slotSelAspectRatioChanged(self):
        sel = self.selections.currentSelection
        if sel:
            index = self.ui.comboSelAspectRatioType.currentIndex()
            # index=0: flexible
            # index=last: custom
            s = self.ui.editSelAspectRatio.text()
            sel.aspectRatioData = [index, s]

    def slotSelAspectRatioTypeChanged(self, index):
        sel = self.selections.currentSelection
        t = self.selAspectRatioTypes.getType(index)
        # index=0: flexible
        # t=None: custom
        ar = ""
        if index == 0 or t is None:
            if sel:
                r = sel.boundingRect()
                w, h = int(r.width()), int(r.height())
                ar = "{} : {}".format(w, h)
        elif t is not None:
            ar = "{} : {}".format(t.width, t.height)
        self.ui.editSelAspectRatio.setEnabled(t is None)
        self.ui.editSelAspectRatio.setText(ar)
        if sel:
            s = self.ui.editSelAspectRatio.text()
            sel.aspectRatioData = [index, s]


    def distributeAspectRatioChanged(self, aspectRatio):
        self.selections.distributeAspectRatio = aspectRatio

    def slotDistributeAspectRatioChanged(self):
        self.selections.distributeAspectRatio = aspectRatioFromStr(self.ui.editDistributeAspectRatio.text())

    def slotDeviceTypeChanged(self, index):
        t = self.deviceTypes.getType(index)
        ar = t and "%s : %s" % (t.width, t.height) or "w : h"
        self.ui.editDistributeAspectRatio.setEnabled(t is None)
        self.ui.editDistributeAspectRatio.setText(ar)
        self.slotDistributeAspectRatioChanged()

    def slotContextMenu(self, pos):
        if self.viewer.isEmpty():
            return

        item = self.ui.documentView.itemAt(pos)
        menuForSelection= False
        try:
            self.selections.currentSelection = item.selection
            menuForSelection= True
        except AttributeError:
            pass
        popMenu = QMenu()
        popMenu.addAction(self.ui.actionNewSelection)
        popMenu.addAction(self.ui.actionNewSelectionGrid)
        if menuForSelection:
            popMenu.addAction(self.ui.actionDeleteSelection)
            popMenu.addAction(self.ui.actionTrimMargins)
        else:
            popMenu.addAction(self.ui.actionTrimMarginsAll)
        popMenu.exec_(self.ui.documentView.mapToGlobal(pos))

    def slotDeleteSelection(self):
        if self.selections.currentSelection is not None:
            self.selections.deleteSelection(self.selections.currentSelection)

    def slotNewSelection(self):
        self.createSelectionGrid("1")

    def slotNewSelectionGrid(self):
        if not self.viewer.isEmpty():
            default = "2x1"
            if self.viewer.isPortrait():
                default = "1x2"
            grid, ok = QInputDialog.getText(self, self.tr('New Selection Grid...'),
                    self.tr('Enter the dimensions of the grid:'), text=default)
            if ok:
                self.createSelectionGrid(grid)

    def createSelectionGrid(self, grid):
        if self.viewer.isEmpty():
            return

        try:
            colsrows = [int(x) for x in grid.split('x')]
            cols = colsrows[0]
            # if only one value is specified, we determine the number of
            # columns/rows according to whether the page is landscape or
            # portrait
            if len(colsrows) == 1:
                if self.viewer.isPortrait():
                    cols, rows = 1, cols
                else:
                    rows = 1
            else:
                rows = colsrows[1]
        except:
            self.showWarning(self.tr("Bad value for grid parameter"), self.tr("For creating a grid "
                "of selections, you need to specify the dimensions of the grid in the form '2x3'. "
                "You can also enter a single number, in which case the number of columns/rows is "
                "determined according to whether the page is landscape or portrait."))
            return

        for j in range(rows):
            for i in range(cols):
                sel = self.selections.addSelection()
                r = sel.boundingRect()
                w = r.width()/cols
                h = r.height()/rows
                p0 = QPointF(r.left()+i*w, r.top()+j*h)
                sel.setBoundingRect(p0, p0 + QPointF(w, h))
        self.pdfScene.update()

    def getPadding(self):
        """
        @brief Returns trim padding in CSS-expanded order.
        @details Reads trim padding text from the dedicated Basic-tab controls and expands one-to-four comma-separated values to `[top,right,bottom,left]`.
        @return {list[float]} Padding tuple in top,right,bottom,left order.
        """
        try:
            padding = [
                float(value.strip())
                for value in self.ui.editPadding.text().split(",")
                if value.strip()
            ]
            if len(padding) == 0:
                return [0.0, 0.0, 0.0, 0.0]
            if len(padding) == 1:
                return 4 * padding
            if len(padding) == 2:
                return 2 * padding
            if len(padding) == 3:
                return padding + [padding[1]]
            if len(padding) == 4:
                return padding
            raise ValueError
        except ValueError:
            self.showWarning(self.tr("Bad value for padding"), self.tr("The value of padding "
                "must be a list of one to four floats separated by commas."))
            return [0.0, 0.0, 0.0, 0.0]

    def slotTrimMarginsAll(self):
        # trim margins of all selections on the current page
        noSelections = True
        for sel in self.selections.items:
            if sel.isVisible():
                noSelections = False
                self.trimMarginsSelection(sel)
        # if there is no selections, then create one
        if noSelections and not self.viewer.isEmpty():
            sel = self.selections.addSelection()
            self.trimMarginsSelection(sel)
        self.pdfScene.update()

    def slotTrimMargins(self):
        if self.selections.currentSelection is not None:
            self.trimMarginsSelection(self.selections.currentSelection)
            self.pdfScene.update()

    def trimMarginsSelection(self, sel):
        """
        @brief Computes auto-trim rectangle for a selection using configured thresholds.
        @details Reads color-sensitivity and grayscale-sensitivity values from Basic-tab controls, selects page scope
        using current page by default or a validated `Pages range` slice of visible pages when range mode is enabled,
        and applies auto-trim with padding and aspect-ratio adjustments.
        @param sel {ViewerSelectionItem} Selection item to trim.
        @return {None} Mutates selection bounding rectangle.
        """
        try:
            sensitivity = float(self.ui.editSensitivity.text())
        except ValueError:
            self.showWarning(self.tr("Bad value for color sensitivity"), self.tr("The value of "
                "color sensitivity (under trim settings) must be a float."))
            sensitivity = 5.0
        try:
            grayscale_sensitivity = float(self.ui.editGrayscaleSensitivity.text())
        except ValueError:
            self.showWarning(self.tr("Bad value for grayscale sensitivity"), self.tr("The value of "
                "grayscale sensitivity (under trim settings) must be a float indicating tolerated grayscale transitions."))
            grayscale_sensitivity = 0.0

        pages = [self.viewer.currentPageIndex]
        if self.ui.checkTrimPagesRange.isChecked():
            try:
                range_start, range_end = self._parseTrimPagesRange()
            except ValueError:
                self.showWarning(
                    self.tr("Bad value for pages range"),
                    self.tr("The value of pages range (under trim settings) must use N-M with positive integers; falling back to 1-1."),
                )
                self.ui.editTrimPagesRange.setText("1-1")
                range_start, range_end = 0, 0
            pages = [
                i for i in range(self.viewer.numPages())
                if range_start <= i <= range_end and sel.selectionVisibleOnPage(i)
            ]

        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        try:
            # orect is the original selection, nrect is the trimmed version
            orect = sel.mapRectToImage(sel.rect).toRect()
            nrect = None
            for idx in pages:
                # calculate values for trimming
                img = self.viewer.getImage(idx)
                if img is None:
                    continue
                nrect = autoTrimMargins(img, orect, nrect, sensitivity, grayscale_sensitivity)
            if nrect is None:
                self.showWarning(self.tr("Something got in our way"),
                    self.tr("Trim Margins could not load page images for automatic trimming."))
                return

            orect = QRectF(orect)
            nrect = QRectF(nrect)

            # adjust for padding ...
            dtop, dright, dbottom, dleft = self.getPadding()
            nrect.adjust(-dleft, -dtop, dright, dbottom)
            # ... but don't overadjust beyond page bounds
            page_image = self.viewer.getImage(self.viewer.currentPageIndex)
            if (
                page_image is not None
                and hasattr(page_image, "width")
                and hasattr(page_image, "height")
            ):
                page_rect = QRectF(
                    0.0,
                    0.0,
                    float(page_image.width()),
                    float(page_image.height()),
                )
                nrect = nrect.intersected(page_rect)
            else:
                nrect = nrect.intersected(orect)

            # take fixed aspect ratio into account
            if sel.aspectRatio:
                r, w, h = sel.aspectRatio, nrect.width(), nrect.height()
                nw, nh = max(w, h*r), max(h, w/r)
                if nw > w:
                    d1 = (nw - w) / 2
                    if nrect.left() - orect.left() < d1:
                        d1 = nrect.left() - orect.left()
                    elif orect.right() - nrect.right() < d1:
                        d1 = nw - w - orect.right() + nrect.right()
                    d2 = nw - w - d1
                    nrect.adjust(-d1, 0, d2, 0)
                elif nh > h:
                    d1 = (nh - h) / 2
                    if nrect.top() - orect.top() < d1:
                        d1 = nrect.top() - orect.top()
                    elif orect.bottom() - nrect.bottom() < d1:
                        d1 = nh - h - orect.bottom() + nrect.bottom()
                    d2 = nh - h - d1
                    nrect.adjust(0, -d1, 0, d2)

            # set selection to new values
            nrect = sel.mapRectFromImage(nrect)
            sel.setBoundingRect(nrect.topLeft(), nrect.bottomRight())
        finally:
            QApplication.restoreOverrideCursor()

    def resizeEvent(self, event):
        self.slotFitInView(self.ui.actionFitInView.isChecked())

    def closeEvent(self, event):
        self.writeSettings()
