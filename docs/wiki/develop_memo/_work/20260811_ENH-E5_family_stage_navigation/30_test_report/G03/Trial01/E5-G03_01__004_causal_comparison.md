# ENH-E5 G03 Trial 01 — Test Item 004: Causal comparison compatibility

## Scope and result

| Acceptance criterion | Result |
| --- | --- |
| `AC-G03-006` — causal comparison semantic key retained | PASS |
| `AC-G03-007` — incompatible direct metric comparison blocked | PASS |

Test target: `1a80c1cec740126f66e21e251ee2d0204819cfd9`.

## Raw evidence

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q \
  tests/product/test_enh_e5_g03_p02_identification_estimation_separation.py \
  tests/product/test_enh_e5_g03_p03_causal_runtime_regression.py
```

Observed output:

```text
......                                                                   [100%]
6 passed in 1.08s
```

The executed comparison tests assert both of the following observations:

1. Different treatments (`coupon` versus `email`) raise `ScientificContractViolation` with code `CAUSAL_COMPARISON_INCOMPATIBLE` and identify `treatment/exposure` as a causal key component.
2. Same causal semantic values remain comparable without warnings.

Direct source observation of the exercised comparison service found the exact key labels: `treatment/exposure`, `outcome`, `estimand`, and `target population`; it raises the stated violation when any key component differs.

## Judgment

**Fact:** the incompatible-comparison block and compatible-comparison path both passed automated assertions.

**Inference:** direct quantitative comparison is not permitted for semantic incompatibility, and the exact G03 semantic key is retained.
