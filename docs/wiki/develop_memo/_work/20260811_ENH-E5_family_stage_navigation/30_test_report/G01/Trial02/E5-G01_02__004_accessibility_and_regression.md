# E5-G01 Trial 02 — Test Item 004: Accessibility and Protected Regression

## Verification purpose

Verify AC-G01-008, AC-G01-009, and the protected predictive frontend regression.

## Command / input

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q \
  tests/product/test_enh_e5_g00_navigation.py \
  tests/product/test_enh_e5_g01_navigation_state.py \
  tests/product/test_enh_e5_g01_navigation_shell.py \
  tests/product/test_enh_e5_g01_history_accessibility.py \
  tests/product/test_predictive_frontend_contract_e3.py
```

## Raw evidence

```text
..............                                                           [100%]
14 passed in 4.05s
```

The successful assertions verify the required asynchronous state vocabulary; keyboard focus target; accessible family/stage labels; non-color unavailable-state semantics; visible focus styling; and existing predictive deep-link frontend behavior.

## Result

`PASS`

## Decision rationale

The required accessibility evidence and protected predictive regression assertions passed against the audited semantic candidate state. This 14-test command also supplied Test Item 002's automated evidence.
