# G02 Trial 01 — 999 gate_decision (reverification 03)

## Decision

**FAIL**

- Fixed Trial Candidate SHA: `d2d87e074338b06fc740252506ae1dba2b2a5c04`
- Tested Repository State: `7de36e443e193fd0fdf1ba6ce00b71f8ba0551eb`
- Promotion eligibility: **PROMOTION_NOT_ALLOWED**

## Basis

Candidate identity passed. SHAP, binary/regression LIME provider execution, capability boundaries, dependency absence, and several protected tests passed. However, two mandatory product contracts fail:

1. AC-09 / item 080: Model Card does not retain required LIME explanation/provenance fields.
2. AC-12 / item 090: baseline G01 predictive flows fail in PREPARE with `KeyError: 'sampling'` when `explanation_spec` is empty.

All G02 blocking items were assessed; no G02 Browser E2E item is required. This is a candidate product failure. No production/test/frozen-contract change was made by the independent verifier.
