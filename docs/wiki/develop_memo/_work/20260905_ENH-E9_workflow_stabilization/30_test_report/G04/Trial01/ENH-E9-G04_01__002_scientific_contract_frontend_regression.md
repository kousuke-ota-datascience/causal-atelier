# ENH-E9 G04 Trial 01 Test Item 002 — Scientific, contract, frontend and regression verification

> **Document class:** Evidence Artifact

- Status: PASS / SCIENTIFIC_UNIT, API_INTEGRATION, FRONTEND_CONTRACT
- Fixed Candidate: `0a841487d8b114563e5db6cacda406619fae4e5b`
- Tested state: `083c3f14b6cd0efc5c9e86de41b0eab4c9cad6eb`
- 07: `10_enhance_instruction/G04/07_Ariadne_ENH-E9_G04_test_instruction.md` (FROZEN)
- Timestamp: 2026-09-06T09:10:03Z

## Exact command

```bash
node --check frontend/causal_diagnostics_presentation.js
git diff --check
uv run pytest -q tests/enhancement/enh_e9/g04/scientific/test_weighting_applicability_contract.py tests/enhancement/enh_e9/g04/scientific/test_ipw_weighting_persistence.py tests/enhancement/enh_e9/g04/scientific/test_balance_applicability.py tests/integration/test_inference.py tests/scientific/test_product_adapters.py tests/enhancement/enh_e9/g04/frontend/test_causal_result_presentation.py tests/enhancement/enh_e9/g04/frontend/test_structured_diagnostics_consumption.py tests/product/test_enh_e8_g02_p02_causal_stage_surface_separation.py tests/product/test_enh_e5_g03_p02_identification_estimation_separation.py
```

Exit code: `0`.

```text
...........................................                              [100%]
43 passed in 8.04s
```

## Evaluation

The required independent fixtures pass for actual ATE/ATT IPW weights, arm ESS, statistics/linear quantiles, exactly-10 extreme boundary, weighted before/after balance, OLS/DIM NOT_APPLICABLE, AIPW PROPENSITY_COMPONENT, finite/null structured fields, payload persistence/compatibility, and frontend structured consumption without scientific recomputation/string parsing. Existing integration and stage/lineage regressions also pass.

| AC | Result |
|---|---|
| AC1–AC11 | PASS — structured weighting, applicability, numeric/scientific fixture contracts |
| AC12 | PASS — persisted structured frontend consumption |
| AC13–AC15 | PASS — lineage/stage compatibility and finite numeric persistence |

Test Agent production/migration/dependency changes: NONE.
