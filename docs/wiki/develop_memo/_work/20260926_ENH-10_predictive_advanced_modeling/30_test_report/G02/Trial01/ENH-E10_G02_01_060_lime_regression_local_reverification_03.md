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

## 入力、isolation、再現条件

probe は `REGRESSION` task、`linear_regression.v1`、120-row numeric frame、non-stratified RANDOM split、`FIRST_N` sampling size 5/seed 17 を使用した。TEST row を explanation instance とし、PREPARE output の TRAIN partition 72 rows を reference として渡した。

したがって `reference.partition=TRAIN` と `local_count=5` は、reference/instance identity が method output に含まれることを示す。一方、Model Card がそれらを保存するかは AC-09 の別判定であり、item 080 の FAIL を参照する。本 report の command 相当の probe が全 five stages `SUCCEEDED` を返すことが再現条件である。

Target/candidate identities are in item 001.
