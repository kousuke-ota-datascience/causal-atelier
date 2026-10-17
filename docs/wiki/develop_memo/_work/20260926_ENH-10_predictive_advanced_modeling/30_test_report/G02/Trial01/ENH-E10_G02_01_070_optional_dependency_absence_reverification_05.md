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

## 隔離方法の妥当性

この probe は current `.venv` を削除・変更しない。temporary site layer をコピーして `shap/`、`lime/` と各 `*.dist-info` だけを除外し、`python -S` で通常の site-packages 自動追加を停止した。従って installed provider を import 可能な通常 runtime を誤って参照して PASS にしていない。NumPy 等の core runtime dependency は layer に残して、欠落 provider 以外の import failure を避けた。

## probe の判定順序

1. `explanation_capabilities()` で package availability、version、reason を読む。
2. compatible model/method/scope を指定して `resolve_explanation_method()` を呼ぶ。
3. `PredictiveValidationError.code` が dependency-specific `EXPLANATION_DEPENDENCY_UNAVAILABLE` であることを確認する。

この順序により、unknown method や scope mismatch の error を dependency absence と誤分類しない。SHAP / LIME の双方を独立に確認した。

## 判定の限界

absence runtime は provider execution の数値 correctness を検証するものではない。その点は installed runtime の item 030–060 が担う。また package が存在しても version range outside の場合の operational policyは registry の availability contract に従うが、今回の absence evidence は package not installed case に限定される。
