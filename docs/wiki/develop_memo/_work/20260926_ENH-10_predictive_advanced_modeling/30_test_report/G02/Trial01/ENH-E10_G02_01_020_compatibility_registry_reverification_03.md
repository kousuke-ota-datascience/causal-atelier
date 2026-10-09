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
