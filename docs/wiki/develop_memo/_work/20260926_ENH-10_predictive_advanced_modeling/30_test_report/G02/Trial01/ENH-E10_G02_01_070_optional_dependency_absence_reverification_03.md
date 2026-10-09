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

## 隔離方法・再現条件

これは monkeypatch だけの確認ではない。`python -S` により通常の site-package discovery を無効化し、temporary site layer から `shap`/`lime` と各 distribution metadata を明示的に除外した runtime を用いた。したがって availability の `False` と distribution version の `None` は provider 不在環境の実測値である。

core capability module import が成功した後、各 method selection が同じ `EXPLANATION_DEPENDENCY_UNAVAILABLE` taxonomy を返すことを確認した。linear/coefficient fallback、silent NOT_APPLICABLE、import-time core failure は観測されない。上記の isolated runtime command と raw output が再現条件である。
