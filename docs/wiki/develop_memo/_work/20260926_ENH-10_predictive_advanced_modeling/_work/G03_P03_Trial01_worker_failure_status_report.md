# ENH-E10 G03 P03 Trial 01 Worker Failure 状況報告

## 結論

P03 は `PACKAGE_READY` である。実ブラウザ scenario 100 の stage-level evidence により、従来の「Causal Stage dispatch failure」という原因断定は誤りであることを確認した。実際の失敗は Predictive workflow の `train` stage で発生した `OSError: libgomp.so.1: cannot open shared object file` であった。

根本原因に限り、`Dockerfile.predictive-advanced` に LightGBM runtime 依存の `libgomp1` を追加した。修復後の hermetic Compose 再構築と scenario 100/110 再検証は完了し、両 scenario が PASS した。

## 実行識別

```text
PROJECT_NAME=Ariadne
ENHANCE_ID=ENH-E10
GATE_ID=G03
PACKAGE_ID=P03
TRIAL_NO=01
START_SHA=b1d6faee77fa123670249ee5053da8a5f7a11379
P03_PRESERVATION_SHA=785e73b9e8d3c01d9f6130247654cae922b576a7
BLOCKER_FIX_SHA=3a4cbef4bb104550f5c24c61661f5dafe265d618
WORKER_DIAGNOSTIC_FIX_SHA=263c234ff007c9da1e9a357f4745dc8f19682dbb
PACKAGE_CHECKPOINT_SHA=64bd2a18dd583349283cd5745edf63d9b28d61ad
```

`P03_PRESERVATION_SHA` は package checkpoint ではない。`WORKER_DIAGNOSTIC_FIX_SHA` は全 analysis family 共通の terminal error propagation を、最後の stage ではなく実際に `FAILED` となった stage の error に修正する、明示的に限定した cross-package blocker resolution である。

## 実施済み内容

- browser runner を修正し、terminal execution を取得した直後、teardown 前に `GET /projects/{project_id}/executions/{execution_id}/stages` を呼ぶようにした。
- JSON evidence の各 scenario に、各 stage の `stage_key`、`status`、`last_error`、`attempt_history` を保存するようにした。成功時 assertion は維持している。
- `GenericExecutor` の downstream `SKIPPED_DUE_TO_PREREQUISITE` が terminal error を隠す診断欠陥を修正し、回帰テストを追加した。
- scenario 100 を実行し、実際の failure stage と例外を収集した。
- 確定した image runtime 欠落に対し、predictive-advanced image に `libgomp1` を追加した。API contract、runner assertion、model/workflow contract は変更していない。

## 検証結果

以下は成功した。

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run pytest -q \
  tests/product/test_execution_processor_failure_propagation.py \
  tests/enhancement/enh_e10/g03/integration/test_predictive_advanced_browser_readiness.py
```

結果: `3 passed`。

修復前の hermetic browser scenario 100 は Predictive execution の作成後に失敗した。evidence は `test-results/browser_e2e/enh_e10/evidence.json` に保存されている。

| stage_key | status | 観測 |
| --- | --- | --- |
| `split` | `SUCCEEDED` | attempt 1 成功 |
| `prepare` | `SUCCEEDED` | attempt 1 成功 |
| `train` | `FAILED` | `OSError: libgomp.so.1: cannot open shared object file: No such file or directory` |
| `evaluate` | `SKIPPED_DUE_TO_PREREQUISITE` | train の失敗により未実行 |
| `explain` | `SKIPPED_DUE_TO_PREREQUISITE` | train の失敗により未実行 |

## 根拠とスコープ判断

事実として、failure は `analysis_family=PREDICTIVE` の実行における `train` stage で発生し、split と prepare は成功している。`Causal Stage failed` は `ExecutionProcessor._dispatch_generic` の旧 fallback message であり、実際の失敗 stage を表さない。従って Causal workflow への誤 dispatch は、この証拠からは導けない。

LightGBM の native runtime は OpenMP shared library `libgomp.so.1` を要求する。`Dockerfile.predictive-advanced` は `python:3.12-slim` を基底としており、当該ライブラリを含めていなかった。このため、必要最小限の OS package `libgomp1` を image に追加した。

## 完了検証

`libgomp1` を含む hermetic Compose image を rebuild し、`down -v --remove-orphans` から再実行した。`test-results/browser_e2e/enh_e10/evidence.json` に次を記録した。

| Scenario | Execution | 結果 |
| --- | --- | --- |
| 100: Binary + `lightgbm_classifier.v1` + `SHAP_TREE` | `44c87e36-58cf-4fde-9388-07bc7398056f` | PASS、split/prepare/train/evaluate/explain はすべて `SUCCEEDED` |
| 110: Regression + `lightgbm_regressor.v1` + `LIME_TABULAR` | `16a9a049-dd40-47ca-a218-5f434f8305fa` | PASS、split/prepare/train/evaluate/explain はすべて `SUCCEEDED` |

両 journey は Execution 成功、Result/Artifact availability、説明結果、Model Card、predictive-not-causal UI を確認した。次の protected regression も PASS した。

```bash
MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run --extra predictive-advanced pytest -q \
  tests/enhancement/enh_e10/g03/integration/test_predictive_advanced_browser_readiness.py \
  tests/product/test_predictive_frontend_contract_e3.py \
  tests/product/test_enh_e7_g02_p05_predictive_stage_surface_migration.py \
  tests/product/test_enh_e5_g00_navigation.py \
  tests/product/test_predictive_api_worker_e2e_e3.py \
  tests/product/test_predictive_explanation_e3.py
```

結果: `24 passed in 11.03s`。Compose resources、volumes、orphans は検証後に teardown 済みである。

本報告は Gate 判定、Candidate Assembly、Independent Verification を意味しない。P03 完了後は停止する。
