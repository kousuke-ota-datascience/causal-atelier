# ENH-E10 G03 P03 Trial 01 BLOCKED 状況報告

## 結論

P03 は `BLOCKED_IMPLEMENTATION` で停止した。P03 が要求する実ブラウザ二経路検証を完了できない直接原因は、既存 Predictive UI の実行送信が必須の `Idempotency-Key` を付与しないことである。これは P03 の browser E2E / regression 範囲ではなく、P02 のフロントエンド送信実装に属するため、本作業では修正していない。

## 実行識別

```text
PROJECT_NAME=Ariadne
ENHANCE_ID=ENH-E10
GATE_ID=G03
PACKAGE_ID=P03
TRIAL_NO=01
START_SHA=5bab0d305612dea67ef63393a876867405fb1929
PACKAGE_CHECKPOINT_SHA=なし
EVIDENCE_COMMIT_SHA=f69d44d3f75275b6a8432d48c8499b652f68de5f
```

Evidence commit は `causal-atelier/feature/ariadne_mvp_e10` へ push 済みである。

## 実施済み内容

- predictive-advanced 依存を含む隔離 Docker runtime を追加した。
- `compose.yaml + compose.e1a.yaml + compose.enh_e10.yaml`、project 名 `ariadne-enh-e10` による hermetic Compose 実行を構成した。
- ブラウザ runner に scenario 100（`lightgbm_classifier.v1` + `SHAP_TREE`）と scenario 110（`lightgbm_regressor.v1` + `LIME_TABULAR`）を追加した。
- runner は画面の stage 表示範囲に従って Setup / Train / Explainability を遷移し、trace、video、failure screenshot、JSON evidence を出力する。
- Docker runtime 内の Alembic configuration と source package の読み取り権限を調整し、`migrate` の正常終了まで確認した。
- 実行後は `down -v --remove-orphans` により Compose resources、volumes、orphans を teardown した。

## 検証結果

次の focused verification は成功した。

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run --extra predictive-advanced python -m py_compile tests/enhancement/enh_e10/g03/browser_e2e/run_predictive_advanced.py
UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run --extra predictive-advanced pytest -q \
  tests/enhancement/enh_e10/g03/integration/test_predictive_advanced_browser_readiness.py \
  tests/product/test_predictive_frontend_contract_e3.py \
  tests/product/test_enh_e7_g02_p05_predictive_stage_surface_migration.py \
  tests/product/test_enh_e5_g00_navigation.py
```

結果: `15 passed in 3.82s`。

実ブラウザ runner は scenario 100 の UI 操作で analysis specification の作成・validate・fix と execution plan の作成・validate まで到達した。しかし execution 作成時に HTTP 400 となり、Execution は作成されなかった。

```json
{
  "error": {
    "code": "IDEMPOTENCY_KEY_REQUIRED",
    "message": "Idempotency-Key header is required for this command"
  }
}
```

## 根拠とスコープ判断

事実として、`frontend/app.js` の Predictive submit handler は `POST /projects/{project_id}/executions` に `Content-Type` のみを付与している。一方、API は `Idempotency-Key` を必須とする。

したがって、ブラウザ E2E が停止した原因は runner の期待値や Compose の起動順ではない。実行 API を利用する既存フロントエンドの送信実装である。P03 が他 Package の実装を便乗修正することは禁止されているため、P03 では回避・修正を行わない。

## 未コミット変更

以下の P03 変更は、browser journeys が完了していないため Package checkpoint として commit されていない。

- `.dockerignore`
- `Dockerfile.browser-e2e`
- `Dockerfile.predictive-advanced`
- `compose.enh_e10.yaml`
- `tests/enhancement/enh_e10/g03/browser_e2e/run_predictive_advanced.py`
- `tests/enhancement/enh_e10/g03/integration/test_predictive_advanced_browser_readiness.py`

## 再開条件

責務を持つ Package / remediation route で、Predictive execution submission に `Idempotency-Key` を復元する。その後、上記の未コミット P03 実装を保持したまま P03 の隔離 browser runner を再実行し、scenario 100 と scenario 110 の Result / Artifact / Model Card evidence を確認する。

本報告は Gate 判定、Candidate Assembly、または Independent Verification を意味しない。
