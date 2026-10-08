# ENH-E10 G02 Trial 01 — Consolidated FAIL Remediation Contract

- Gate/Trial: `G02/01`
- Remediation Mode: `CONSOLIDATED`
- Execution Mode: `SINGLE_EXECUTION`
- Status: `AUTHORIZED_NOT_VERIFIED`
- PREVIOUS_FAILED_CANDIDATE_SHA=67f1c4ef1281700a14b5a9acd0eacf00b5c904e0
- Independent evidence commit: `a9e701d5cf734326ff9292165040def47c69ff79`
- Gate decision: `30_test_report/G02/Trial01/ENH-E10_G02_01_999_gate_decision.md`

## Authority and freeze

The frozen G02 implementation and test contracts remain unchanged, including acceptance criteria AC-05, AC-06, AC-09 and AC-10, G01 guarantees, existing schema versions, runtime defaults and TEST/TRAIN isolation. This remediation authorizes correcting the product violation only. Trial 01 remains FAIL and promotion is prohibited until a separate independent verification passes. Never delete, weaken, skip or xfail failing tests.

## Verified deficiency

`lime_backend.lime_local_contract` returns parameter metadata but does not execute the provider, bind a fitted model or training reference, or produce signed local explanation contributions. `explanation_runner` handles only coefficient explanations. This fails binary/regression local LIME and canonical result/artifact/model-card integration (Test Items 050, 060, 080) and leaves LIME isolation unverified.

## Consolidated implementation scope

1. Execute actual `lime.lime_tabular.LimeTabularExplainer` in preprocessed feature space aligned with the frozen model's `feature_order`, bound to the serialized fitted model's real predict/predict-proba callable, each TEST instance, and deterministically sampled TRAIN reference rows. Use `predictive-explanation-reference/1`: TRAIN-only, sample without replacement, max 500, seed from explanation sampling; persist reference hash/count/seed/provenance but do not persist raw reference rows.
2. Explain positive-class probability for binary classification and numeric prediction for regression; capture provider-generated signed local feature contributions, feature index/name mapping, original transformed instance values, row identity, predicted model output and proper scale.
3. Preserve every default: `num_samples=2000`, `num_features=min(10,n_features)`, `feature_selection=auto`, `discretize_continuous=False`, `distance_metric=euclidean`, `kernel_width=0.75*sqrt(n_features)`, `sample_around_instance=False`. Stable per-instance effective random seeds; binary one-hot feature handling and invalid original-category perturbation limitation; provider version `lime==0.2.0.1`.
4. Canonical output in explanation result, its JSON artifact and Model Card (existing schema versions unchanged) must include method ID/version, model/task/preprocessor and feature identities, output scale, provider contributions, instance/sample/reference identity, effective seed/all parameters, package/runtime provenance and predictive-not-causal limitation.
5. Reject global LIME and `local_explanations=False` explicitly with `EXPLANATION_SCOPE_NOT_SUPPORTED`. Fail explicitly with `EXPLANATION_DEPENDENCY_UNAVAILABLE` when LIME is unavailable/incompatible; never silently substitute metadata. Keep coefficient and SHAP explanation behavior and G01 fitted-model load/predict contracts intact. Explanations consume only TEST data; all fitting, model selection and reference construction consume only TRAIN data.

## Tests and evidence

Add and run deterministic binary/regression integration tests that prove provider-valued contributions; correct class/probability or regression prediction scale; transformed feature order; stable row and reference hashes; frozen seed/configuration; fixed-runtime reproducibility; result/artifact/Model Card provenance; and TRAIN/TEST information isolation. Exercise dependency-unavailable/global rejection, SHAP and coefficient regressions, and G01 model serialization/prediction. Preserve original failing tests. Capture exact commands, runtime versions and outputs; never claim PASS for unexecuted tests.

## Re-entry requirements

Create a distinct remediation candidate SHA, with a verified non-empty semantic production/test/dependency diff relative to `67f1c4ef1281700a14b5a9acd0eacf00b5c904e0`. Only then write a Trial 01 completion report identifying the exact candidate, changes, test results and residual limits, and request **new independent G02 verification**. Original FAIL reports remain immutable. Documentation-only commits do not satisfy re-entry.

## Frozen references

- `10_enhance_instruction/G02/06_G02_P03_lime_backend_and_integration.md`
- `10_enhance_instruction/G02/07_Ariadne_ENH-E10_G02_test_instruction.md`
- `30_test_report/G02/Trial01/ENH-E10_G02_01_050_lime_binary_local.md`
- `30_test_report/G02/Trial01/ENH-E10_G02_01_060_lime_regression_local.md`
- `30_test_report/G02/Trial01/ENH-E10_G02_01_080_provenance_and_model_card.md`
- `30_test_report/G02/Trial01/ENH-E10_G02_01_999_gate_decision.md`
