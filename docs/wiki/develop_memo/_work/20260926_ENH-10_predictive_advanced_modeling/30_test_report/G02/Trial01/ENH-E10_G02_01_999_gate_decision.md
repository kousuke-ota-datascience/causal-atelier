# G02 Trial 01 — 999 gate_decision

## Decision

**FAIL**

- GATE_ID: `G02`
- TRIAL_NO: `01`
- TEST_START_SHA: `b5fa47c8e3e299445a3efd4ef791242fc040ea50`
- FIXED_TRIAL_CANDIDATE_SHA: `67f1c4ef1281700a14b5a9acd0eacf00b5c904e0`
- Promotion eligibility: **PROMOTION_NOT_ALLOWED**

## Basis

Candidate identity audit passed. Independent tests confirmed SHAP adapter behavior, optional dependency boundaries, and G01 protected regression. However, LIME is not implemented as an explanation provider: the candidate returns static metadata without invoking LIME or accepting model/data/prediction/reference inputs. Binary and regression LIME acceptance requirements, plus required explanation result/artifact/model-card provenance and isolation integration, are therefore violated.

Failed Test Items: `050_lime_binary_local` (AC-05), `060_lime_regression_local` (AC-06), `080_provenance_and_model_card` (AC-09; also prevents AC-10 verification for LIME).

Passing Test Items: `001`, `010`, `020`, `030`, `040`, `070`, `090`.

See individual Test Item reports for raw evidence. This is a product implementation defect; no test-side repair was made.
