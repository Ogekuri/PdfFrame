# -*- coding: iso-8859-1 -*-

"""
pdfframe: A tool to crop PDF files

You can use command line arguments in addition to (or, to a degree, instead of) the graphical interface.

For instance, to run conversion with a predefined single selection area:
    pdfframe --go --grid=1 file.pdf
Omit the --go to further edit the selections in the graphical interface before cropping.

Copyright (C) 2010-2025 Ogekuri
"""

"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

import sys

from pdfframe.version import __version__


def main():
    from argparse import ArgumentParser, RawTextHelpFormatter
    parser = ArgumentParser(prog='pdfframe', description=__doc__,
            formatter_class=RawTextHelpFormatter)

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    parser.add_argument('file', nargs='?', help='PDF file to open')
    parser.add_argument('-o', '--output', help='where to save the cropped PDF')
    parser.add_argument('--whichpages', help='requested page range to process (accepted forms: "5", "5-", "-5", "5-9")')
    parser.add_argument('--mode', type=str, choices=['frame', 'crop'], help='conversion mode: frame keeps original page size, crop shrinks output page to selection bounds')

    parser.add_argument('--grid', help='creates the initial trim/selection area; single-area mode is enforced and values larger than 1 area are reduced to one area')

    parser.add_argument('--initialpage', help='which page to open initially (default: 1)')
    parser.add_argument('--verbose', action='store_true', help='enable verbose console output from the Python program')
    parser.add_argument('--debug', action='store_true', help='enable debug output for Ghostscript command execution (effective with --verbose)')

    parser.add_argument('--go', action='store_true', help='output PDF without opening the pdfframe GUI (using the choices supplied on the command line); if used in a script without X server access, you can run pdfframe using xvfb-run')

    parser.add_argument('--use-qt5', action='store_true', help='use PyQt5 instead of PyQt6 (default: use PyQt6 if available)')
    parser.add_argument('--use-pymupdf', action='store_true', help='use PyMuPDF for rendering (default)')
    parser.add_argument('--use-pikepdf', action='store_true', help='legacy flag retained for compatibility (no crop backend effect)')
    parser.add_argument('--use-pypdf', action='store_true', help='legacy flag retained for compatibility (no crop backend effect)')
    parser.add_argument('--use-pypdf2', action='store_true', help='legacy flag retained for compatibility (no crop backend effect)')
    parser.add_argument('--use-poppler', action='store_true', help='use Poppler Qt for rendering (PyQt5 only, default: use PyMuPDF)')

    args = parser.parse_args()

    from pdfframe.qt import QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("pdfframe")
    app.setApplicationDisplayName("pdfframe")

    app.setOrganizationName("ogekuri.com")
    app.setOrganizationDomain("ogekuri.com")

    from pdfframe.mainwindow import MainWindow
    window=MainWindow()
    window.verbose = args.verbose
    window.debug = args.debug

    if args.file is not None:
        fileName = args.file
        window.openFile(fileName)

    if args.output is not None:
        window.ui.editFile.setText(args.output)
    if args.whichpages is not None:
        window.ui.editWhichPages.setText(args.whichpages)
    if args.mode is not None:
        window.radioModeFrame.setChecked(args.mode == "frame")
        window.radioModeCrop.setChecked(args.mode == "crop")
    if args.initialpage is not None:
        window.ui.editCurrentPage.setText(args.initialpage)
        window.slotCurrentPageEdited(args.initialpage)

    # args.grid is specified as 2x3 for 2 cols, 3 rows
    if args.grid:
        window.createSelectionGrid(args.grid)

    # shut down on ctrl+c when pressed in terminal (not gracefully, though)
    # http://stackoverflow.com/questions/4938723/
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    if args.go:
        #  sys.stdout.write('pdfframeping...\n')
        from pdfframe.qt import QTimer
        QTimer.singleShot(0, window.slotPdfFrame)
        QTimer.singleShot(0, window.close)
    else:
        window.show()
        window.slotFitInView(window.ui.actionFitInView.isChecked())

    sys.exit(app.exec())
