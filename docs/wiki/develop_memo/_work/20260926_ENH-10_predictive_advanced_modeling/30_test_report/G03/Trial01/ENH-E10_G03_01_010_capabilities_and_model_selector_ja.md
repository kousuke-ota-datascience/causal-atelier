# ENH-E10 G03 Trial 01 — テスト項目 010: 機能能力とモデル選択子

| Candidate | Tested SHA | AC | 結果 |
| --- | --- | --- | --- |
| `64bd2a18dd583349283cd5745edf63d9b28d61ad` | `df278f76ff476143545d73037fe55f96664dae28` | AC-01, AC-02, AC-08 | **PASS** |

## 方法・生出力

正本記載の `MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run --extra predictive-advanced pytest -q` による G03 integration、ENH-E10 G01/G02、baseline predictive、ENH-E8 protected tests の完全コマンドを実行した。生出力は `58 passed, 2 warnings in 15.03s` である。browser scenario 100 は可視の Train selector から `lightgbm_classifier.v1` を、110 は `lightgbm_regressor.v1` を選択し、両方とも `SUCCEEDED` に到達した。

## 事実・解釈・判定

G01 capability/parameter validation は logistic/linear default、LightGBM の model-task compatibility、deterministic model parameter、明示的 error taxonomy を保護する。browser journey は backend-only の推測経路ではなく、UI-to-API request construction により LightGBM option を選択することを示す。2 warnings は SHAP provider の binary-array notification であり selector/request failure ではない。したがって capability-driven compatible selection、parameter serialization、advanced-runtime availability の AC-01/02/08 を満たす。suite と browser command の exit code はいずれも `0`。正本の完全コマンドと item 100 の frozen browser command を実行し、`58 passed` と両 LightGBM journey の `SUCCEEDED` を要求して再現する。**PASS**。
