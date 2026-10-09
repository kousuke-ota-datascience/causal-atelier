# G02 Trial 01 — 060 lime_regression_local (reverification 03)

## Scope / reproduction

AC-06. An independent runtime probe built a regression spec with `linear_regression.v1`, `LIME_TABULAR`, random splitting (non-stratified), deterministic sampling `{strategy: FIRST_N, size: 5, seed: 17}`, and a 120-row numeric fixture. It executed the complete split → prepare → train → evaluate → explain plan.

## Raw observation

```text
outcome_status=SUCCEEDED
split=SUCCEEDED
prepare=SUCCEEDED
train=SUCCEEDED
evaluate=SUCCEEDED
explain=SUCCEEDED
lime_method=LIME_TABULAR
local_count=5
scale=PREDICTION
reference={schema_version: predictive-explanation-reference/1,
 partition: TRAIN, count: 72, seed: 17,
 hash: 274d65f9ce0fad30cddd1d7c31b5b23cdb647448b4dfbaf879ef7af7bd2d15b7}
exit code: 0
```

**Interpretation:** regression LIME consumes a TRAIN reference and returns local TEST explanations on PREDICTION scale. Target/candidate identities are in item 001. **Result: PASS.**

Target/candidate identities are in item 001.
