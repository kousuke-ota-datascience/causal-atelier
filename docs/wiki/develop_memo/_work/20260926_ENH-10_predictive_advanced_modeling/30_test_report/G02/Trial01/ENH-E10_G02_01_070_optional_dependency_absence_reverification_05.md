# ENH-E10 G02 Trial 01 — Test Item 070: Optional Dependency Absence（reverification 05）

| Fixed Candidate | Tested SHA | AC | 判定 |
| --- | --- | --- | --- |
| `fbd97c5b7a95084affe5e2381d85d86d0dfa2558` | `1bf3026ba1918c8ca74af64318bdd42e90d7ed67` | AC-08 | **PASS** |

## 隔離 runtime による再現

`/tmp/e10-g02-reverify05-no-explanation-site.0YccWf` は current site-packages から `shap` / `lime` と各 distribution metadata を除外した一時 layer である。`-S` により通常 site を読まない。

```bash
PYTHONPATH=src:/tmp/e10-g02-reverify05-no-explanation-site.0YccWf \
.venv/bin/python -S -c '<capability availability / resolve_explanation_method probe>'
```

```text
SHAP_TREE availability={'available': False, 'version': None,
 'reason': 'Optional dependency shap is not installed'}
LIME_TABULAR availability={'available': False, 'version': None,
 'reason': 'Optional dependency lime is not installed'}
SHAP_TREE error=EXPLANATION_DEPENDENCY_UNAVAILABLE
LIME_TABULAR error=EXPLANATION_DEPENDENCY_UNAVAILABLE
exit code: 0
```

## 解釈

core capability module は optional providers が無くても import でき、選択された unavailable method に package availability / version evidence と明示 error code を返す。silent fallback、core import failure、`NOT_APPLICABLE` への誤変換はない。AC-08 は **PASS**。
