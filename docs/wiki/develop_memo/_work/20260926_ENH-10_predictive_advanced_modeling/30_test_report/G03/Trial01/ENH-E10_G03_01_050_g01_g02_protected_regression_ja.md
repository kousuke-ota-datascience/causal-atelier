# ENH-E10 G03 Trial 01 — テスト項目 050: G01/G02 保護回帰

| Candidate | Tested SHA | AC | 結果 |
| --- | --- | --- | --- |
| `64bd2a18dd583349283cd5745edf63d9b28d61ad` | `df278f76ff476143545d73037fe55f96664dae28` | AC-11 | **PASS** |

## コマンド・生出力

item 010 の independent command と生出力を使用した。結果は `58 passed, 2 warnings in 15.03s`、exit `0`。このコマンドは ENH-E10 G01 の contract/unit/integration、ENH-E10 G02 の contract/integration、baseline predictive training/evaluation/explanation/leakage/API-worker tests を実行する。

## 観測事実・解釈

- G01 は model registry、deterministic LightGBM adapter behavior、artifact serialization/load/predict parity、明示的 invalid parameter/model error を維持した。
- G02 は coefficient、SHAP binary/regression、LIME binary/regression、TRAIN reference provenance、dependency absence、output-scale と Result/Artifact/Model Card contract を維持した。
- assertion failure はなく、2 warnings は non-failing SHAP provider notification のみである。

G03 product integration 下で必要な G01/G02 protected semantics は有効である。正本記載の G01/G02 と baseline predictive tests の pytest command を実行し、complete G03 suite で上記の生出力を要求して再現する。candidate change は advanced runtime/browser verification に限定され G01/G02 implementation mutation ではなく、post-candidate diff は documentation-only である。AC-11 は **PASS**。
