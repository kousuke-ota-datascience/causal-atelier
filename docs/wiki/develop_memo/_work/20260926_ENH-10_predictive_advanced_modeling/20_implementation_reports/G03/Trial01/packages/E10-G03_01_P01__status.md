# ENH-E10 G03 Trial 01 P01 — Package Status

| Field | Value |
| --- | --- |
| PROJECT_NAME | Ariadne |
| ENHANCE_ID | ENH-E10 |
| GATE_ID | G03 |
| PACKAGE_ID | P01 |
| TRIAL_NO | 01 |
| Normative contract | `10_enhance_instruction/G03/06_G03_P01_capabilities_and_train_integration.md` |
| START_SHA | `faadcb38bee7d3fea963cf1a7092dc3b0aa28c2f` |
| Package status | `PACKAGE_READY` |
| State | `PACKAGE_COMPLETE` |
| PACKAGE_CHECKPOINT_SHA | `db1b15259d27134d6d6754524a77ca777e16c94e` |

## 実装内容

- `predictive-capabilities/1` に task default、structured model parameter、provider/dependency/availability、serializer/loader、determinism、model-explanation compatibility を additive に追加した。
- legacy `parameter_schema`、`deterministic_seed`、`compatibility`、既存 explanation fields を維持した。
- Train UI は backend capability を唯一の authority として、task-compatible model、unavailable 理由、model 固有 parameter controls、capability-derived serialization を扱うようにした。
- Setup の feature editing authority と Train/Predict の read-only feature context は変更していない。

## 変更ファイル

- `src/ariadne/product/application/predictive_workflow_service.py`
- `frontend/index.html`
- `frontend/app.js`
- `tests/product/test_predictive_split_api_e3.py`
- `tests/product/test_predictive_frontend_contract_e3.py`

## Focused verification

```bash
node --check frontend/app.js

MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run --extra predictive-advanced pytest -q \
  tests/product/test_predictive_api_worker_e2e_e3.py \
  tests/product/test_predictive_split_api_e3.py \
  tests/product/test_predictive_frontend_contract_e3.py \
  tests/product/test_predictive_training_e3.py
```

結果: JavaScript syntax check PASS、pytest `11 passed in 14.04s`。

## Blocker / remaining work

NONE for P01. P02/P03、Candidate Assembly、Independent Verification は本 Package の責務外であり未実行。
