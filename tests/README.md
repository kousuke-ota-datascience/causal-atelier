# Test classification

Baseline: `bb059ffee047c777ab68a52393ebe492d579fca9`.

- Active Product Test: `tests/product/`
- Scientific Characterization / Regression Test: `tests/scientific/` and retained `tests/integration/test_inference.py`
- Compatibility Contract Test: none, because the approved C2 set is empty
- Retired Legacy Control Plane Test: `tests/legacy_archive/retired_control_plane/` (excluded from default pytest collection)

The retired tests are retained as historical evidence. They are intentionally not supported by namespace shims.
