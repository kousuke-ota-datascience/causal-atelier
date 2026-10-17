# ENH-E10 G03 Trial 01 — テスト項目 030: Explainability の機能能力 UI

| Candidate | Tested SHA | AC | 結果 |
| --- | --- | --- | --- |
| `64bd2a18dd583349283cd5745edf63d9b28d61ad` | `df278f76ff476143545d73037fe55f96664dae28` | AC-04, AC-07, AC-08 | **PASS** |

## 方法・観測事実

item 010 の 58-test command は ENH-E10 G02 capability/explanation integration tests を含む。items 100/110 の frozen browser command は binary LightGBM の `SHAP_TREE`、regression LightGBM の `LIME_TABULAR` を可視に選択し、generated explanation result と predictive-not-causal UI text を要求した。

- G02 contract tests は unknown method を `EXPLANATION_METHOD_NOT_REGISTERED`、linear に対する SHAP を `EXPLANATION_METHOD_NOT_APPLICABLE`、global LIME を pseudo-global fallback なしの `EXPLANATION_SCOPE_NOT_SUPPORTED` とした。
- scenario 100 は SHAP global/local を選択して `PREDICTIVE_EXPLANATION_RESULT` を出力し、110 は local LIME を選択して同じ canonical result type を出力した。
- browser runner は `Predictive Explanation ≠ Causal Explanation`、terminal execution 後の result/artifact retrieval を検証した。
- optional provider absence は G02 contract tests が保護し、installed advanced runtime は二つの browser journey で確認した。

## 解釈・再現・判定

method compatibility、global/local boundary、明示的 unavailable behavior、predictive terminology は UI selection から persisted result まで維持される。正本の G02 contract/integration pytest command を実行し exit `0`、さらに item 100 の frozen compose command で generated explanation result と predictive-not-causal text を要求して再現する。incompatible/scope/dependency boundary と compatible SHAP/LIME selection に証拠があり、fallback は観測されない。**PASS**。
