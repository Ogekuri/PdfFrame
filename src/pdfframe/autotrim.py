# -*- coding: iso-8859-1 -*-

"""
Code for auto trimming margins in pdfframe.

Copyright (C) 2010-2020 ogekuri
"""

"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

from pdfframe.qt import *


def autoTrimMargins(img, r, minr, sensitivity, grayscale_sensitivity):
    """
    @brief Auto-trims margins of a rectangle using grayscale-transition thresholds.
    @details Scans rectangle border lines and trims sides while per-line grayscale
    transitions remain within configured sensitivity and grayscale-sensitivity.
    @param img {QImage} Page image used for grayscale sampling.
    @param r {QRect} Candidate rectangle to trim.
    @param minr {QRect|None} Optional minimum rectangle that limits trimming.
    @param sensitivity {float} Minimum pixel delta counted as a transition.
    @param grayscale_sensitivity {float} Maximum accepted transition count per scan line.
    @return {QRect} Trimmed rectangle clamped to image bounds.
    """

    def pixAt(x, y):
        return qGray(img.pixel(x, y))

    def isTrimmable(L):
        if not L:
            return True
        changes = 0
        y = L[0]
        for x in L:
            if abs(x-y) > sensitivity:
                changes += 1
                if changes > grayscale_sensitivity:
                    return False
            y = x
        return True

    # rounding r to QRect might overshoot the picture by a pixel
    r = r.intersected(img.rect())

    # we shouldn't trim r to something smaller than minr
    while r.height() > 0 and (minr is None or r.top() < minr.top()):
        L = [ pixAt(x, r.top()) for x in range(r.left(), r.right()) ]
        if not isTrimmable(L):
            break
        r.setTop(r.top()+1)
    while r.height() > 0 and (minr is None or r.bottom() > minr.bottom()):
        L = [ pixAt(x, r.bottom()) for x in range(r.left(), r.right()) ]
        if not isTrimmable(L):
            break
        r.setBottom(r.bottom()-1)
    while r.width() > 0 and (minr is None or r.left() < minr.left()):
        L = [ pixAt(r.left(), y) for y in range(r.top(), r.bottom()) ]
        if not isTrimmable(L):
            break
        r.setLeft(r.left()+1)
    while r.width() > 0 and (minr is None or r.right() > minr.right()):
        L = [ pixAt(r.right(), y) for y in range(r.top(), r.bottom()) ]
        if not isTrimmable(L):
            break
        r.setRight(r.right()-1)

    return r
