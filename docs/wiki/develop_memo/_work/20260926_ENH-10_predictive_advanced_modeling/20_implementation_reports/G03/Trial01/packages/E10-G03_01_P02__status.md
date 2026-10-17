# ENH-E10 G03 Trial 01 P02 — Package Status

| Field | Value |
| --- | --- |
| PROJECT_NAME | Ariadne |
| ENHANCE_ID | ENH-E10 |
| GATE_ID | G03 |
| PACKAGE_ID | P02 |
| TRIAL_NO | 01 |
| Normative contract | `10_enhance_instruction/G03/06_G03_P02_explainability_and_model_management_integration.md` |
| START_SHA | `7b77b5136926f2b663121633c729c0548f82ca88` |
| Package status | `PACKAGE_READY` |
| State | `PACKAGE_COMPLETE` |
| PACKAGE_CHECKPOINT_SHA | `14b3d3064723356227c08c42ee1d3fdc935f199d` |

## 実装内容

- Explainability selector を backend の model-method compatibility、availability、GLOBAL/LOCAL support、method default から構成した。
- unavailable/incompatible method は disable と理由表示で明示し、frontend 独自 fallback を持たせていない。
- Explanation read surface に method、scope、output/prediction scale、TEST sample、background/reference provenance、limitations を read-only 表示した。
- Model Management read surface に model/task/parameters/seed、provider/library、feature/preprocessor identity、fitted-model/Model Card artifact identity、Model Card と explanation provenance を read-only 表示した。
- predictive-not-causal wording を保持した。

## 変更ファイル

- `frontend/index.html`
- `frontend/app.js`
- `tests/product/test_enh_e10_g03_p02_explainability_model_management.py`

## Focused verification

```bash
node --check frontend/app.js

MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run --extra predictive-advanced pytest -q \
  tests/product/test_enh_e10_g03_p02_explainability_model_management.py \
  tests/product/test_predictive_frontend_contract_e3.py \
  tests/product/test_enh_e5_g02_p03_predictive_read_surfaces.py \
  tests/product/test_enh_e7_g02_p05_predictive_stage_surface_migration.py \
  tests/product/test_predictive_explanation_e3.py \
  tests/product/test_predictive_api_worker_e2e_e3.py
```

結果: JavaScript syntax check PASS、pytest `18 passed in 9.54s`。

## Blocker / remaining work

NONE for P02. P03、Candidate Assembly、Independent Verification は本 Package の責務外であり未実行。
