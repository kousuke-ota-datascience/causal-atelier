# G02 Trial 01 — 020 compatibility_registry (reverification 03)

## Scope / command

AC-02 / AC-07. Command and environment are the independent G02 suite recorded in item 010.

## Facts

The capability tests asserted these exact negative boundaries:

| Input | Expected / observed code |
| --- | --- |
| unknown method | `EXPLANATION_METHOD_NOT_REGISTERED` |
| `SHAP_TREE` with `linear_regression.v1` | `EXPLANATION_METHOD_NOT_APPLICABLE` |
| `LIME_TABULAR` with `GLOBAL` scope | `EXPLANATION_SCOPE_NOT_SUPPORTED` |

The suite result was `13 passed, 1 warning`, exit 0. The LIME global request is rejected rather than converted to a pseudo-global or fallback result.

Target/candidate identities are in item 001. **Result: PASS.**

## 判定境界・再現条件

この item は「method が登録されている」だけでは PASS としない。model × method × scope の各不適合が区別可能な code で失敗し、fallback output が生成されないことを確認対象とする。

実行対象は `explanation_capabilities()` と `resolve_explanation_method()` の contract layer である。item 010 の exact G02 suite command を再実行し、上表の 3 error code と suite exit `0` を確認する。`LIME_TABULAR` の global request が空配列や NOT_APPLICABLE ではなく `EXPLANATION_SCOPE_NOT_SUPPORTED` になることが AC-07 の判定根拠である。

Fixed Candidate / tested state は item 001 を参照。結果は **PASS**。
