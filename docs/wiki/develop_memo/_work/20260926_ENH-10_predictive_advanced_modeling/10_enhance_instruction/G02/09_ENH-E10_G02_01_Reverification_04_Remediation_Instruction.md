# ENH-E10 G02 Trial 01 — Independent Reverification 04 Remediation Contract

- Gate/Trial: `G02/01`
- Remediation Mode: `CONSOLIDATED`
- Execution Mode: `SINGLE_EXECUTION`
- Status: `AUTHORIZED_NOT_VERIFIED`
- Immediately previous failed candidate: `e9a5b412349b10ced45d822aa08a54b6d9df00ba`
- Evidence authority: `30_test_report/G02/Trial01/*_reverification_04.md`

## Authority and boundary

The frozen G02 implementation/test instructions and P01--P03 work-package
contracts remain acceptance authority.  This contract only authorizes repair
of the independently observed SHAP integration failure.  It does not change
criteria, schema versions, historical package checkpoints, or G01 semantics.
Trial 01 remains FAIL until a separate independent verification; no gate
promotion is authorized here.

## Verified failure

For compatible `lightgbm_classifier.v1` and `lightgbm_regressor.v1` requests,
the actual EXPLAIN stage completed but returned `NOT_APPLICABLE` rather than
dispatching the existing `explain_shap_tree` backend.  Consequently global and
local SHAP outputs, result/artifact provenance, and Model Card provenance were
absent (AC-03, AC-04, and SHAP portions of AC-09/10/11).

## Required remediation scope

1. Dispatch `SHAP_TREE` for its frozen compatible LightGBM models, using
   `explain_shap_tree` without fallback.  Preserve binary raw `LOG_ODDS`,
   binary prediction `PROBABILITY`, regression `PREDICTION`, complete immutable
   TEST global aggregation, deterministic FIRST_N local rows, tree-path-
   dependent background, feature/sample identity, and the frozen additivity
   tolerance.
2. Preserve the explicit frozen error taxonomy for unavailable dependencies,
   incompatible models, scope and computation failure.  A supported SHAP
   request must never become a silent `NOT_APPLICABLE` result.
3. Add additive v1 SHAP provenance to result, JSON artifact and Model Card:
   method/version, provider/version, model/task/preprocessor/feature identity,
   output scale, global/local identity, TEST sample identity, tree-path-
   dependent background, sampling, runtime provenance and predictive-not-
   causal limitation.  Do not fabricate a TRAIN reference for SHAP.
4. Add deterministic full-DAG binary and regression integration tests.  They
   must inspect generated result/artifact/Model Card outputs, additivity and
   TEST isolation; direct backend tests alone are insufficient.

## Re-entry and evidence

Run the reverification_04 protected regression command and any import-order
isolated tests required by their existing contract.  Commit production/test
changes as a distinct, non-empty semantic candidate relative to
`e9a5b412349b10ced45d822aa08a54b6d9df00ba`; then commit completion evidence
separately.  No semantic change may follow the candidate checkpoint.  Report
only implementation-side `READY_FOR_TEST` after all listed checks pass; do not
run independent verification, declare PASS or promote G02.
