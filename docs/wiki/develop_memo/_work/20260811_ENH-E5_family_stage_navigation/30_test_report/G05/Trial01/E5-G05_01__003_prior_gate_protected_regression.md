# ENH-E5 G05 Trial 01 — Test Item 003: Prior-Gate evidence and protected regression

- Test item: `003_prior_gate_protected_regression`
- Verification purpose: `AC-G05-009`.
- Test target: `ebc943d0401a838f429d1281b2e1a3863ca29bf4` (semantic implementation state: `5cf0caf515b8e57fc114eabea0efd9acffe23e62`)

## Prior-Gate PASS evidence

The supplied report tree contains final PASS decisions for G00 Trial01, G01 Trial04, G02 Trial01, G03 Trial01, and G04 Trial02. Earlier non-final G01/G04 trials include FAIL/BLOCKED reports; they are not treated as the final PASS evidence.

## Protected regression command

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q \
  tests/product/test_enh_e5_g00_navigation.py \
  tests/product/test_enh_e5_g01_navigation_state.py \
  tests/product/test_enh_e5_g02_p01_predictive_compatibility.py \
  tests/product/test_enh_e5_g03_p03_causal_runtime_regression.py \
  tests/product/test_enh_e5_g04_p03_exploratory_boundary.py
```

Observed output:

```text
16 passed in 4.62s
```

## Result

**PASS**

The prior-Gate protected regression selection is green, and the final PASS report for each required prior Gate is present.
