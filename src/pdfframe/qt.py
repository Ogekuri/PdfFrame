# ruff: noqa: F403
# pyright: reportMissingImports=false, reportUndefinedVariable=false, reportAttributeAccessIssue=false
"""
@file qt.py
@brief Unified Qt symbol export layer for PyQt6/PyQt5 compatibility.
@details Re-exports QtCore/QtGui/QtWidgets symbols based on runtime backend selection.
"""

from pdfframe.config import PYQT6

if PYQT6:
    from PyQt6.QtCore import *
    from PyQt6.QtGui import *
    from PyQt6.QtWidgets import *
else:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
