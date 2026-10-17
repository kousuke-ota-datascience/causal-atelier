# ENH-E10 G02 Trial 01 — Independent Reverification 03 Remediation Contract

- Gate/Trial: `G02/01`
- Remediation Mode: `CONSOLIDATED`
- Execution Mode: `SINGLE_EXECUTION`
- Status: `AUTHORIZED_NOT_VERIFIED`
- Immediately previous failed candidate: `d2d87e074338b06fc740252506ae1dba2b2a5c04`
- Evidence authority: `30_test_report/G02/Trial01/*_reverification_03.md`

## Authority and boundary

`06_Ariadne_ENH-E10_G02_implementation_instruction.md`,
`07_Ariadne_ENH-E10_G02_test_instruction.md`, and frozen P01--P03 remain the
acceptance authority.  This document authorizes only product/test remediation
of verified failures.  It neither changes acceptance criteria nor promotes
G02; Trial 01 remains FAIL pending separate independent verification.

## Verified failures to repair

1. **AC-09 / item 080:** the LIME result had local provider facts, but the
   Model Card lacked method-specific provenance.  The result, its JSON
   artifact, and Model Card must each preserve additive v1 provenance: method
   ID/version; model/task/preprocessor identity; transformed feature
   representation/identity; TEST instance identity; TRAIN reference
   identity/hash; output scale; effective seed/frozen parameters; provider
   package/runtime versions; and the predictive-not-causal limitation.  Raw
   TRAIN reference rows must remain runtime-only.
2. **AC-12 / item 090:** a G01 flow with `explanation_spec={}` fails because
   PREPARE indexes `sampling`.  No explanation reference, request, or sampling
   parameter may be fabricated when no explanation is requested.

## Required audit and implementation scope

- Construct the LIME TRAIN reference by deterministic sampling without
  replacement, at most 500 rows, with the frozen explanation sampling seed.
- Treat transformed one-hot columns as binary categorical LIME features and
  retain the frozen invalid-original-category perturbation limitation.
- Exercise actual LIME integration for every frozen LIME model/task
  combination, explicitly including `lightgbm_regressor.v1`; no inference from
  linear regression success is sufficient.
- Preserve schema versions, G01 model train/predict/serialization behavior,
  TEST isolation, coefficient and SHAP behavior, and explicit LIME scope and
  dependency errors.

## Required implementation-side verification

Run the frozen G02 P01--P03 and protected suites, including predictive
training/explanation, G01 artifact/load/predict, TRAIN/TEST isolation,
result/artifact/Model Card provenance, and SHAP/LIME regressions.  Record exact
commands and results in the completion report.  Do not delete, weaken, skip,
or xfail tests.

## Candidate assembly and re-entry

Create a non-empty semantic production/test/dependency diff against
`d2d87e074338b06fc740252506ae1dba2b2a5c04`, commit it as the fixed candidate,
then update the canonical completion report in a separate evidence-only commit.
The report must identify both candidates, commands, results, changed files and
remaining limitations.  No semantic change may follow the fixed-candidate
checkpoint.  Push only after implementation-side verification passes and hand
off as `READY_FOR_TEST`; do not independently verify, declare PASS, or promote
the gate.
