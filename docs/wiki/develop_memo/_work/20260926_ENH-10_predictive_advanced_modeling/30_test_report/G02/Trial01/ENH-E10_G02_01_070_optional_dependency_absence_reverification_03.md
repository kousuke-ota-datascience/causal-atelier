# G02 Trial 01 — 070 optional_dependency_absence (reverification 03)

## Scope / method

AC-08. A Python `-S` process used an isolated temporary site layer that contains the current runtime packages except `shap`, `shap-0.52.0.dist-info`, `lime`, and `lime-0.2.0.1.dist-info`. It imported core capability code and resolved each advanced method.

## Raw observation

```text
SHAP_TREE_availability={'available': False, 'version': None,
 'reason': 'Optional dependency shap is not installed'}
SHAP_TREE_error=EXPLANATION_DEPENDENCY_UNAVAILABLE
LIME_TABULAR_availability={'available': False, 'version': None,
 'reason': 'Optional dependency lime is not installed'}
LIME_TABULAR_error=EXPLANATION_DEPENDENCY_UNAVAILABLE
exit code: 0
```

**Interpretation:** absence does not prevent core import; selecting either unavailable provider is explicit and has no fallback. Target/candidate identities are in item 001. **Result: PASS.**
