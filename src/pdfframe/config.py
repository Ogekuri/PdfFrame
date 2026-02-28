# pyright: reportMissingImports=false, reportUndefinedVariable=false, reportAttributeAccessIssue=false
"""
@file config.py
@brief Runtime backend-selection flags for pdfframe.
@details Detects which Qt binding is available and exposes the `PYQT6` switch consumed by UI modules.
"""

import importlib.util
import sys

PYQT6 = False

if '--use-qt5' not in sys.argv and importlib.util.find_spec("PyQt6") is not None:
    PYQT6 = True
elif importlib.util.find_spec("PyQt5") is None:
    _msg = "Please install PyQt6 (or PyQt5) first."
    raise RuntimeError(_msg)
