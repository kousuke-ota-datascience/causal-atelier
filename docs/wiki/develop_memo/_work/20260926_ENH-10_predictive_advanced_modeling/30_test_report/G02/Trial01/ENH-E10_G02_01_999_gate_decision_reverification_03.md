# G02 Trial 01 — 999 gate_decision (reverification 03)

## Decision

**FAIL**

- Fixed Trial Candidate SHA: `d2d87e074338b06fc740252506ae1dba2b2a5c04`
- Tested Repository State: `7de36e443e193fd0fdf1ba6ce00b71f8ba0551eb`
- Promotion eligibility: **PROMOTION_NOT_ALLOWED**

## Test Item summary

| Test Item | AC | Result | Independent evidence |
| --- | --- | --- | --- |
| 001 candidate identity | META | PASS | candidate ancestry and documentation-only post-candidate diff audited |
| 010 coefficient protected regression | 01, 11 | PASS | G02 suite: 13 passed |
| 020 compatibility registry | 02, 07 | PASS | explicit unavailable/inapplicable/scope errors |
| 030 SHAP binary | 03 | PASS | raw LOG_ODDS global/local adapter assertions |
| 040 SHAP regression | 04 | PASS | raw PREDICTION; max residual about `1.1e-14` |
| 050 LIME binary local | 05 | PASS | provider contribution / probability / TRAIN reference assertions |
| 060 LIME regression local | 06 | PASS | full five-stage run; PREDICTION / TRAIN reference |
| 070 dependency absence | 08 | PASS | isolated unavailable-provider explicit errors |
| 080 provenance and Model Card | 09, 11 | FAIL | Model Card omits LIME method-specific provenance |
| 090 G01 protected regression | 12 | FAIL | baseline PREPARE raises `KeyError: 'sampling'` |

## Basis

Candidate identity passed. SHAP, binary/regression LIME provider execution, capability boundaries, dependency absence, and several protected tests passed. However, two mandatory product contracts fail:

1. AC-09 / item 080: Model Card does not retain required LIME explanation/provenance fields.
2. AC-12 / item 090: baseline G01 predictive flows fail in PREPARE with `KeyError: 'sampling'` when `explanation_spec` is empty.

The failures are independent: either one prevents PASS. They are executable candidate product failures, not test-orchestration or environment defects. All G02 blocking items were assessed; the frozen contract defines zero G02 Browser E2E blocking items. No production/test/frozen-contract change was made by the independent verifier.

## Reproduction boundary

Use item 080's regression LIME probe to inspect result/Model Card payloads and item 090's isolated G01 command to reproduce the protected regression. A remediation candidate must repair both conditions, retain prior passing boundaries, and be submitted with a distinct Fixed Trial Candidate SHA before a new independent verification can decide promotion.

詳細な command、raw output、fixture、identity audit、PASS/FAIL classification は `ENH-E10_G02_01_reverification_03_execution_detail.md` を参照すること。
