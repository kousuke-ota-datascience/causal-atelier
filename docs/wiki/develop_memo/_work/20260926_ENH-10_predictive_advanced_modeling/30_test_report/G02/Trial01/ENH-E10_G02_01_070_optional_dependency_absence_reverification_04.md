# ENH-E10 G02 Trial 01 — Test Item 070: Optional Dependency Absence（reverification 04）

AC-08。`python -S` と temporary site layer を用い、`shap` / `lime` distribution と metadata を除外して core capability module を import した。

```text
SHAP_TREE availability=False, version=None
SHAP_TREE error=EXPLANATION_DEPENDENCY_UNAVAILABLE
LIME_TABULAR availability=False, version=None
LIME_TABULAR error=EXPLANATION_DEPENDENCY_UNAVAILABLE
exit code: 0
```

core import は成功し、linear/coefficient fallback、silent NOT_APPLICABLE、import-time failure は観測されない。dependency absence の package availability/version evidence と explicit error taxonomy を満たす。**PASS**。
