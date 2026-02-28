# -*- coding: iso-8859-1 -*-
# ruff: noqa: F403, F405
# pyright: reportMissingImports=false, reportUndefinedVariable=false, reportAttributeAccessIssue=false, reportIncompatibleMethodOverride=false, reportOperatorIssue=false, reportOptionalMemberAccess=false, reportOptionalSubscript=false

"""
@file vieweritem.py
@brief Viewer backends and rendering abstractions for PDF page display.
@details Implements Qt graphics-item viewer classes for Poppler and PyMuPDF rendering backends.
Copyright (C) 2010-2025 Ogekuri.
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

import sys

from pdfframe.config import PYQT6
from pdfframe.qt import *

from pdfframe.viewerselections import ViewerSelections


class AbstractViewerItem(QGraphicsItem):
    """Abstract class for displaying a PDF document and for allowing the user
    to create selections."""
    def __init__(self, mainwindow):
        QGraphicsItem.__init__(self)
        self.selections = ViewerSelections(self)
        self.reset()
        self.mainwindow = mainwindow

    def reset(self):
        self._currentPageIndex = 0
        self.brect = QRectF()
        self.irect = QRectF()
        self._images = []
        self.selections.deleteSelections()

    def boundingRect(self):
        return self.brect

    def isPortrait(self):
        return self.irect.width() <= self.irect.height()

    def paint(self, painter, option, widget):
        img = self.getImage(self.currentPageIndex)
        if img is None:
            return
        painter.drawRect(self.irect.adjusted(-1,-1,1,1))
        painter.drawImage(self.irect, img)

    def mapRectToImage(self, r):
        return r.translated(-self.irect.left(), -self.irect.top())

    def mapRectFromImage(self, r):
        return r.translated(self.irect.left(), self.irect.top())

    def getCurrentPageIndex(self):
        return self._currentPageIndex

    def setCurrentPageIndex(self, idx):
        if idx >= self.numPages():
            idx = self.numPages()-1
        if idx < 0:
            idx = 0
        self._currentPageIndex = idx

        img = self.getImage(idx)
        if img is None:
            return
        self.selections.updateSelectionVisibility()

        self.prepareGeometryChange()
        rect = QRectF(img.rect())
        # inflate slightly so that bounding rect will be visible
        padding = 5
        self.brect = QRectF(0,0,rect.width()+2*padding,rect.height()+2*padding)
        self.irect = QRectF(padding,padding,rect.width(),rect.height())
        self.scene().setSceneRect(self.brect)

    currentPageIndex = property(getCurrentPageIndex, setCurrentPageIndex)

    def previousPage(self):
        self.currentPageIndex = self.currentPageIndex-1

    def nextPage(self):
        self.currentPageIndex = self.currentPageIndex+1

    def firstPage(self):
        self.currentPageIndex = 0

    def lastPage(self):
        self.currentPageIndex = self.numPages()-1

    def getImage(self, idx):
        if idx < 0 or idx >= self.numPages():
            return None
        if self._images[idx] is None:
            self._images[idx] = self.cacheImage(idx)
        return self._images[idx]        

    def mousePressEvent(self, event):
        self.selections.mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.selections.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.selections.mouseReleaseEvent(event)

    def load(self, filename):
        self.reset()
        self.doLoad(filename)
        self._images = [None for i in range(self.numPages())]
        self.firstPage()

    # To be implemented in deriving classes:

    def doLoad(self, filename):
        pass

    def numPages(self):
        return 0

    def isEmpty(self):
        return self.numPages() <= 0

    def cacheImage(self, idx):        
        return None

    def pageGetRotation(self, idx):        
        return 0

    def pageGetSizePoints(self, idx):
        """
        @brief Returns page size for bbox conversion when backend metadata is unavailable.
        @details Uses rendered image dimensions as fallback point-like units for callers that require non-zero geometry values.
        @param idx {int} Zero-based page index.
        @return {tuple[float,float]} Width and height pair.
        """
        img = self.getImage(idx)
        if img is None:
            return 0.0, 0.0
        return float(img.width()), float(img.height())

    def cropValues(self, idx):
        def adjustForOrientation(cv):
            if r == 90: # Landscape
                return [ cv[1], cv[2], cv[3], cv[0] ]
            elif r == 180: # UpsideDown
                return [ cv[2], cv[3], cv[0], cv[1] ]
            elif r == 270: # Seascape
                return [ cv[3], cv[0], cv[1], cv[2] ]
            else: # r == 0, Portrait
                return cv
        crop_values = self.selections.cropValues(idx)
        r = self.pageGetRotation(idx)
        return [ adjustForOrientation(cv) for cv in crop_values ]


class PopplerViewerItem(AbstractViewerItem):
    """Viewer implementation which uses Poppler to display PDF documents."""
    def reset(self):
        AbstractViewerItem.reset(self)
        self._pdfdoc = None

    def doLoad(self, filename):
        self._pdfdoc = Poppler.Document.load(filename)
        if self._pdfdoc:
            self._pdfdoc.setRenderHint(Poppler.Document.Antialiasing and
                    Poppler.Document.TextAntialiasing)

    def numPages(self):
        if self._pdfdoc is None:    
            return 0
        else:
            return self._pdfdoc.numPages()

    def cacheImage(self, idx):        
        page = self._pdfdoc.page(idx)
        return page.renderToImage(96.0, 96.0) # dpi = 96
        # return page.renderToImage() # default dpi = 72

    def pageGetRotation(self, idx):        
        page = self._pdfdoc.page(idx)
        o = page.orientation()
        if o == page.Landscape:
            return 90
        elif o == page.UpsideDown:
            return 180
        elif o == page.Seascape:
            return 270
        else: # o == page.Portrait
            return 0

    def pageGetSizePoints(self, idx):
        """
        @brief Returns Poppler page size in point units.
        @details Queries Poppler page metadata and exposes width/height values used by command-backend crop-box generation logic.
        @param idx {int} Zero-based page index.
        @return {tuple[float,float]} Width and height pair in points.
        """
        page = self._pdfdoc.page(idx)
        if page is None:
            return 0.0, 0.0
        size = page.pageSizeF()
        return float(size.width()), float(size.height())


class MuPDFViewerItem(AbstractViewerItem):
    """Viewer implementation which uses PyMuPDF to display PDF documents."""
    def reset(self):
        AbstractViewerItem.reset(self)
        self._pdfdoc = None

    def doLoad(self, filename):
        self._pdfdoc = fitz.open(filename)
        # if self._pdfdoc:
        #     self._pdfdoc.setRenderHint(Poppler.Document.Antialiasing and
        #             Poppler.Document.TextAntialiasing)

    def numPages(self):
        if self._pdfdoc is None:    
            return 0
        else:
            return len(self._pdfdoc)

    def cacheImage(self, idx):        
        page = self._pdfdoc[idx]
        pix = page.get_pixmap(alpha=False, dpi=96) # default dpi is 72
        return QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
        # It might be faster to use samples_ptr but the code results in crashes.
        # https://pymupdf.readthedocs.io/en/latest/tutorial.html
        # pix = page.get_pixmap()
        # set the correct QImage format depending on alpha
        # fmt = QImage.Format_RGBA8888 if pix.alpha else QImage.Format.Format_RGB888
        # return QImage(pix.samples_ptr, pix.width, pix.height, fmt)

    def pageGetRotation(self, idx):        
        page = self._pdfdoc[idx]
        return page.rotation

    def pageGetSizePoints(self, idx):
        """
        @brief Returns MuPDF media-box dimensions in point units.
        @details Reads page media-box coordinates and provides width/height for deterministic bbox conversion in command-based cropping.
        @param idx {int} Zero-based page index.
        @return {tuple[float,float]} Width and height pair in points.
        """
        page = self._pdfdoc[idx]
        rect = page.mediabox
        return float(rect.width), float(rect.height)


# determine whether to use PopplerQt or PyMuPDF for rendering
POPPLERQT = 1
PYMUPDF = 2
lib_render = 0

# for PyQt6 use PyMuPDF
if PYQT6:
    try:
        import fitz
        lib_render = PYMUPDF
    except ImportError:
        _msg = "Please install PyMuPDF first (PyQt6 is being used)."\
            "\n\tOn recent versions of Ubuntu, the following should do the trick:"\
            "\n\tsudo apt-get install python3-pymupdf"
        raise RuntimeError(_msg)
else:
    # PyQt5 was requested
    if '--use-poppler' not in sys.argv:
        try:
            import fitz
            lib_render = PYMUPDF
        except ImportError:
            pass
    if not lib_render:
        try:
            from popplerqt5 import Poppler
            lib_render = POPPLERQT
        except ImportError:
            pass
    # complain if no version is available
    if not lib_render:
        _msg = "Please install PyMuPDF or Poppler Qt first (PyQt5 is being used)."\
            "\n\tOn versions of Ubuntu such as 22.04, one of the following should do the trick:"\
            "\n\tsudo apt install python3-fitz"\
            "\n\tsudo apt install python3-poppler-qt5"
        raise RuntimeError(_msg)

if lib_render == PYMUPDF:
    ViewerItem = MuPDFViewerItem
    if '--verbose' in sys.argv:
        print("Using PyMuPDF for rendering.", file=sys.stderr)
else:
    ViewerItem = PopplerViewerItem
    if '--verbose' in sys.argv:
        print("Using PopplerQt for rendering.", file=sys.stderr)
