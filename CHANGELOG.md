# Changelog

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

[0.1.0]: https://github.com/Ogekuri/PdfFrame/releases/tag/v0.1.0
[0.2.0]: https://github.com/Ogekuri/PdfFrame/compare/v0.1.0..v0.2.0
