# Changelog

## [0.5.0](https://github.com/Ogekuri/PdfFrame/compare/v0.4.0..v0.5.0) - 2026-03-03
### ⛰️  Features
- enforce uniform page format on load [useReq] *(mainwindow.openFile)*
  - add REQ-037 and TST-015 for mixed-page-format handling\n- reject mixed size/orientation documents at open time with modal warning\n- add openFile unit tests and refresh WORKFLOW/REFERENCES traceability

### 🐛  Bug Fixes
- use fill=False to avoid white rectangles over redacted areas [useReq] *(_redact_outside_selection)*
  - Change add_redact_annot fill parameter from (1,1,1) to False so that
  - apply_redactions() removes content without drawing white fill rectangles
  - over the redacted page areas. Frame mode now removes content outside
  - selection cleanly without visible artifacts.
  - Add reproducer test verifying no fill rectangles are added.
- use redaction to physically remove content outside selection [useReq] *(crop_pdf_pages)*
  - Replace _blank_outside_selection (white rectangle overlay) with
  - _redact_outside_selection (PyMuPDF redaction API) to physically remove
  - text, images, and line art outside the selection boundary.
  - Both frame and crop modes now use redaction before page sizing:
  - Frame mode: redact + keep original page dimensions
  - Crop mode: redact + resize page to selection bounds
  - No hidden artifacts remain outside the visible area.
  - Adds two reproducer tests verifying content removal via get_text().
- Fix frame mode, annotation cleanup, and UI freeze [useReq] *(crop_pdf_pages)*
  - Frame mode now draws white fill outside selection instead of setting CropBox,
  - preserving original page dimensions (REQ-010)
  - Add xref-level /Annots null cleanup after API-based annotation/widget deletion
  - to ensure all annotation types are removed (REQ-032)
  - Add event_pump call before doc.save() to prevent UI freeze during PDF write
  - (REQ-015, DES-009)
  - Add _blank_outside_selection helper for frame-mode white rectangle drawing
  - Add 3 reproducer tests: frame page size, mixed annotation types, event pump count
  - Update pre-existing frame mode test for correct original-size page assertion

### 🚜  Changes
- BREAKING CHANGE: Replace GhostScript with PyMuPDF for PDF crop/frame processing [useReq] *(core)*
  - Replace all GhostScript subprocess calls with PyMuPDF fitz API (crop_pdf_pages)
  - Consolidate PreserveFields+ShowAnnots into single DeleteAnnots checkbox (default: enabled)
  - Add bookmark preservation via TOC save/restore across page selection
  - Remove GhostScript thread (THR:PROC:main#ghostscript-output-reader) and queue-based progress
  - Implement callback-based per-page progress reporting with Qt event pump
  - Use raw xref_set_key for crop-mode MediaBox to bypass coordinate transform issues
  - Update all affected tests to use PyMuPDF-based assertions (77 tests pass)
  - Update REQUIREMENTS.md, WORKFLOW.md, REFERENCES.md for new architecture
  - Remove GhostScript-specific functions and error types from pdfframecmd.py
  - Remove optimizePdfGhostscript from pdfframeper.py

### 📚  Documentation
- align usage docs with current CLI/GUI/config surfaces [useReq] *(readme)*
  - update feature and quick-start text for current GUI behavior\n- document current CLI flags and compatibility semantics\n- add ~/.pdfframe/config.json schema and defaults

## [0.4.0](https://github.com/Ogekuri/PdfFrame/compare/v0.3.0..v0.4.0) - 2026-02-28
### 📚  Documentation
- Update README.md doc.

## [0.3.0](https://github.com/Ogekuri/PdfFrame/compare/v0.2.0..v0.3.0) - 2026-02-28
### 🐛  Bug Fixes
- Fix version number in tests.sh file.
- Remove unused files.

### 🚜  Changes
- enable uv and uvx execution workflow [useReq] *(core)*
  - Update REQUIREMENTS.md for uv/uvx packaging behavior.
  - Add pyproject.toml with pdfframe console script metadata.
  - Switch pdfframe.sh and tests.sh to Astral uv-based execution.
  - Document Astral uv install and uvx live run in README.
  - Add pyproject metadata unit tests and required desktop metadata files.

## [0.2.0](https://github.com/Ogekuri/PdfFrame/compare/v0.1.0..v0.2.0) - 2026-02-28
### 🐛  Bug Fixes
- Fix requirements.txt file.

## [0.1.0](https://github.com/Ogekuri/PdfFrame/releases/tag/v0.1.0) - 2026-02-28
### ⛰️  Features
- add Preserve fields Ghostscript flag [useReq] *(mainwindow)*
  - Append REQ-032 and TST-011 for Preserve fields behavior.
  - Add unchecked Preserve fields option before existing PDF operations.
  - Emit -dPreserveAnnots=true/false in frame and crop commands.
  - Persist preserve-fields setting and add command/UI tests.
- add JSON config and trim presets [useReq] *(mainwindow)*
  - Append REQ-023..REQ-029 and TST-007..TST-008 in SRS.
  - Implement ~/.pdfframe/config.json bootstrap and runtime override loading.
  - Add Presets UI section, Save Margins action, apply/rename/delete preset flows.
  - Persist preset updates and runtime trim config to JSON config file.
  - Add unit tests for JSON config bootstrap/override and preset CRUD logic.
  - Regenerate WORKFLOW.md and REFERENCES.md for updated runtime and symbols.
- Initial commit.

### 🐛  Bug Fixes
- stabilize Qt UI static checks and Doxygen metadata [useReq] *(ui)*
  - disable Pyright missing-import noise for generated Qt UI modules
  - remove unused PyQt5 QtGui import in mainwindowui_qt5.py
  - add structured Doxygen metadata on generated UI module/class/methods
  - regenerate docs/REFERENCES.md to reflect updated source metadata
- Fix clean.sh script.
- Minord bug fixes.
- prevent preset name mid-row truncation [useReq] *(mainwindow)*
  - Add failing reproducer test for preset row width truncation.
  - Disable tree header last-section stretch in presets list setup.
  - Keep preset behavior unchanged and preserve right-edge delete button.
  - Update workflow/references docs after runtime-layout fix.
- apply trim padding to highlighted area [useReq] *(mainwindow)*
  - add failing reproducer for trim padding highlight behavior
  - clamp padded trim rectangle to page bounds when image geometry is available
  - update workflow/reference docs for trim runtime behavior
- Rename programs.

### 🚜  Changes
- rename preserve field and add show annots flag [useReq] *(core)*
  - update REQ-032/TST-011 and related evidence matrix rows
  - rename UI label to Preserve annotations fields
  - add Show annotations fields toggle default false
  - persist PDF/ShowAnnots and propagate it into crop planning
  - emit Ghostscript -dShowAnnots=true/false alongside PreserveAnnots
  - extend unit tests for UI order/defaults and command flags
  - update WORKFLOW.md and regenerate REFERENCES.md
- enforce single trim selection area [useReq] *(viewerselections)*
  - Update REQ-002/REQ-003 and add REQ-034 for single-area behavior.
  - Limit selection creation paths to one area and remove center ordinal label rendering.
  - Adjust grid input handling to single-area mode and update CLI help text.
  - Add regression tests, refresh WORKFLOW, and regenerate REFERENCES.
- add dedicated toolbar icons [useReq] *(mainwindow)*
  - Update REQ-021/REQ-027/TST-008 for dedicated toolbar icon assets.
  - Bind generated icons for Go, Trim Margins, and Save Margins actions.
  - Add icon assets and regression tests for icon presence and bindings.
  - Update WORKFLOW and regenerate REFERENCES for traceability.
- move Go button after Save Margins [useReq] *(mainwindow)*
  - Update REQ-021 and TST-008 for toolbar right-edge ordering.
  - Reorder toolbar in _setupTrimPresetAction by appending Go after Save Margins.
  - Add regression test for Save Margins/Go order in presets test module.
  - Refresh WORKFLOW and regenerate REFERENCES for traceability.
- reposition presets panel in Basic tab [useReq] *(mainwindow)*
  - Update REQ-026/REQ-028/TST-008 for dedicated Presets group placement.
  - Move Presets panel below Trim settings without changing preset behavior.
  - Adjust row layout so preset text stretches up to right-edge delete button.
  - Add/adjust tests for placement and row-width expectations.
- remove deprecated basic controls [useReq] *(mainwindow)*
  - Update CTN-007 and REQ-009 to remove Rotation/Optimize/Include controls.
  - Remove related UI widgets, config key, and conversion-option branches.
  - Refresh Help text and add tests for control/logic removal.
- add trim pages range controls [useReq] *(mainwindow)*
  - Update REQ-005/REQ-007 and add REQ-031 plus TST-010 coverage.
  - Replace Use all pages with Trim pages range and Pages range field.
  - Validate N-M range, apply range-bounded trimming, and add UI separator.
  - Update persistence keys, tests, WORKFLOW, and regenerated REFERENCES.
- rename trim threshold nomenclature [useReq] *(mainwindow)*
  - Update REQ-004/REQ-007 and add REQ-030 plus TST-009 coverage.
  - Rename Allowed changes to Grayscale sensitivity in UI and runtime keys.
  - Update trim tooltips/help text and auto-trim parameter naming.
  - Adjust presets/tests and regenerate workflow/references docs.
- align preset delete control to row edge [useReq] *(mainwindow)*
  - Update REQ-028 and TST-008 to require right-edge delete control alignment.
  - Render each preset delete button inside a right-aligned row container.
  - Keep preset rename/delete/save behavior unchanged.
  - Add test coverage asserting right-aligned row-container wiring.
  - Regenerate WORKFLOW.md and REFERENCES.md for updated evidence.

### 📚  Documentation
- Add screenshot.
- Fix README.md doc.
- align annotation fields guidance [useReq] *(readme)*
  - add Feature Highlights coverage for Preserve annotations fields
  - add Feature Highlights coverage for Show annotations fields
  - update Quick Start with optional annotation-fields step
- regenerate runtime workflow model [useReq] *(core)*
  - rewrite execution-unit model for src/ and release workflow jobs
  - add explicit Ghostscript output reader thread execution unit
  - add thread communication edges and update process call-trace tree
  - keep parser-stable section/schema order for downstream LLM agents
- Update source code docs.
- Edit README.md file.
- document toolbar actions and icons [useReq] *(readme)*
  - Align Feature Highlights and Quick Start with current GUI behavior.
  - Document Trim Margins, Save Margins, and Go! toolbar usage and placement.
- add Krop acknowledgment [useReq] *(readme)*
  - Add thanks to Prof. Armin Straub for developing Krop.


# History

- \[0.1.0\]: https://github.com/Ogekuri/PdfFrame/releases/tag/v0.1.0
- \[0.2.0\]: https://github.com/Ogekuri/PdfFrame/releases/tag/v0.2.0
- \[0.3.0\]: https://github.com/Ogekuri/PdfFrame/releases/tag/v0.3.0
- \[0.4.0\]: https://github.com/Ogekuri/PdfFrame/releases/tag/v0.4.0
- \[0.5.0\]: https://github.com/Ogekuri/PdfFrame/releases/tag/v0.5.0

[0.1.0]: https://github.com/Ogekuri/PdfFrame/releases/tag/v0.1.0
[0.2.0]: https://github.com/Ogekuri/PdfFrame/compare/v0.1.0..v0.2.0
[0.3.0]: https://github.com/Ogekuri/PdfFrame/compare/v0.2.0..v0.3.0
[0.4.0]: https://github.com/Ogekuri/PdfFrame/compare/v0.3.0..v0.4.0
[0.5.0]: https://github.com/Ogekuri/PdfFrame/compare/v0.4.0..v0.5.0
