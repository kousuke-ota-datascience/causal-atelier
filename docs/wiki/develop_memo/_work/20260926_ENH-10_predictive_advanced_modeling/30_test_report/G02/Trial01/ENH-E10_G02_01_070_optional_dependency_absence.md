# G02 Trial 01 — 070 optional_dependency_absence

AC-08. An isolated Python `-S` process used `PYTHONPATH=src:/tmp/e10-g02-no-explanation-site`, whose temporary site layer deliberately excluded both SHAP and LIME distributions. Raw output:

```text
SHAP_TREE_availability={'available': False, 'version': None, 'reason': 'Optional dependency shap is not installed'}
SHAP_TREE_error=EXPLANATION_DEPENDENCY_UNAVAILABLE
LIME_TABULAR_availability={'available': False, 'version': None, 'reason': 'Optional dependency lime is not installed'}
LIME_TABULAR_error=EXPLANATION_DEPENDENCY_UNAVAILABLE
exit code: 0
```

Target/candidate identities are as in item 001. Result: **PASS**.
