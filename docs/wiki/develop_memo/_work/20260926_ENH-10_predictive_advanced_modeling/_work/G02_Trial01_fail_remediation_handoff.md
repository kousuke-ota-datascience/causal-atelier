# ENH-E10 G02 Trial 01 — FAIL Remediation Handoff

## Status

`FAIL` — verified product / contract violation. This is not a test, orchestration, or environment failure.

| Item | Value |
| --- | --- |
| Gate / Trial | `G02` / `01` |
| Previous failed candidate | `67f1c4ef1281700a14b5a9acd0eacf00b5c904e0` |
| Independent evidence commit | `a9e701d5cf734326ff9292165040def47c69ff79` |
| Gate decision | `30_test_report/G02/Trial01/ENH-E10_G02_01_999_gate_decision.md` |
| Promotion | Not allowed |

## Verified failure

The candidate's `src/ariadne/capabilities/predictive/lime_backend.py` does not implement LIME explanations. `lime_local_contract()` accepts only a minimal model ID and metadata inputs; it does not import or invoke the `lime` provider and does not receive a fitted model payload, feature matrix, prediction callable, or training-derived reference data.

For both `lightgbm_classifier.v1` and `lightgbm_regressor.v1`, the observed output has only:

```text
effective_seed, feature_order, limitation, method, parameters,
representation, row_ordinal, scope
```

It lacks provider-derived local contributions, prediction/model output, binary positive-class probability, instance values/identity, reference/background identity, model task identity, package/runtime provenance, and explanation result/artifact/model-card integration.

This violates:

- AC-05 / Test Item 050 — Binary LIME local explanation.
- AC-06 / Test Item 060 — Regression LIME local explanation.
- AC-09 / Test Item 080 — normalized result/artifact/model-card provenance.
- AC-10 cannot be established for LIME because there is no execution-pipeline integration or isolated data lineage.

## Required remediation boundary

Implement actual local LIME explanation execution for binary classification and regression.

1. Call the LIME provider against preprocessed feature space.
2. Bind the fitted model, prediction callable, local instance, and deterministic TRAIN-derived reference data.
3. For binary classification, explain positive-class probability; for regression, explain the prediction output.
4. Retain frozen LIME defaults: 2000 samples, `min(10, n_features)`, no continuous discretization, euclidean distance, `0.75 * sqrt(n_features)` kernel width, and `sample_around_instance=false`.
5. Persist canonical explanation fields: method/version, model/task and feature/preprocessor identity, output scale, local contribution values, sample/instance identity, reference identity, effective seed/parameters, provider package/runtime version, and predictive-not-causal limitation.
6. Integrate canonical output into explanation result, artifact, and Model Card without changing their schema version.
7. Preserve G01 model artifact/load/predict behavior, TEST-only explanation inputs, TRAIN-only fitting/selection, existing linear coefficient explanation, explicit unsupported-global-LIME rejection, and explicit unavailable-dependency errors.

## Required tests and evidence

Add/execute deterministic integration tests that verify, for each task:

- provider-generated local explanation values (not metadata-only output);
- binary positive-class probability or regression prediction scale;
- preprocessed feature representation and feature mapping;
- fixed instance and reference identities;
- fixed effective seed and all frozen parameters;
- runtime-scoped reproducibility;
- result/artifact/Model Card provenance;
- explanation-only TEST lineage, without model-selection or training changes.

Do not delete, weaken, skip, or xfail failing tests. Do not alter frozen G02 acceptance criteria.

## Re-entry guard

Before coding, create the required self-contained formal remediation contract at:

```text
docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling/
10_enhance_instruction/G02/
08_ENH-E10_G02_01_Remediation_Instruction.md
```

It must declare `Remediation Mode: CONSOLIDATED`, `Execution Mode: SINGLE_EXECUTION`, and record:

```text
PREVIOUS_FAILED_CANDIDATE_SHA=67f1c4ef1281700a14b5a9acd0eacf00b5c904e0
```

The remediation candidate must be a distinct SHA and contain a non-empty semantic diff in production/test/dependency paths relative to the previous failed candidate. Only then create the Trial 01 completion report and request a new independent verification run.

## Evidence links

- `docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling/30_test_report/G02/Trial01/ENH-E10_G02_01_050_lime_binary_local.md`
- `docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling/30_test_report/G02/Trial01/ENH-E10_G02_01_060_lime_regression_local.md`
- `docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling/30_test_report/G02/Trial01/ENH-E10_G02_01_080_provenance_and_model_card.md`
- `docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling/30_test_report/G02/Trial01/ENH-E10_G02_01_999_gate_decision.md`
