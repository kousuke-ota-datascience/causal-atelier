# ENH-E10 G02 Trial 01 — Test Item 010: Coefficient Protected Regression（reverification 05）

| Fixed Candidate | Tested SHA | AC | 判定 |
| --- | --- | --- | --- |
| `fbd97c5b7a95084affe5e2381d85d86d0dfa2558` | `1bf3026ba1918c8ca74af64318bdd42e90d7ed67` | AC-01, AC-11 | **PASS** |

## 実行環境・再現コマンド

Python `3.12.3`、LightGBM `4.7.0`、SHAP `0.52.0`、LIME `0.2.0.1`、`uv run --extra predictive-advanced` を用いた。以下の独立 suite を実行した。

```bash
MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run --extra predictive-advanced pytest -q \
 tests/product/test_predictive_explanation_e3.py \
 tests/product/test_predictive_leakage_e3.py \
 tests/product/test_enh_e10_g02_p01_explanation_capabilities.py
```

suite 全体の生出力は item 030 に記録した `43 passed, 2 warnings in 18.97s`（exit 0）である。warnings は SHAP provider の binary array-shape notification のみで、coefficient assertion の失敗はない。

## 観測事実

- compatible linear model の global/local coefficient explanation、feature-order mismatch の明示 reject、TEST-only explanation の assertion が成功した。
- binary coefficient の model-output scale は `LOG_ODDS`、prediction scale は `PROBABILITY` のまま維持された。
- Result diagnostics と limitation は predictive-not-causal 境界を維持し、因果効果・causal feature importance と表現しない。

## 解釈

SHAP/LIME の成功を coefficient の根拠にしていない。既存の線形 explanation semantics と terminology boundary が保護され、AC-01 と AC-11 を満たすため **PASS**。

## 実際に実行した suite と生出力

item 010 の assertion は次の complete independent command に含めて実行した（短縮した subset command を PASS 根拠にしていない）。

```bash
MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run --extra predictive-advanced pytest -q \
 tests/product/test_enh_e10_g02_p01_explanation_capabilities.py \
 tests/product/test_enh_e10_g02_p02_shap_backend.py \
 tests/product/test_enh_e10_g02_p03_lime_backend.py \
 tests/product/test_predictive_training_e3.py \
 tests/product/test_predictive_evaluation_e3.py \
 tests/product/test_predictive_explanation_e3.py \
 tests/product/test_predictive_leakage_e3.py \
 tests/product/test_enh_e10_g01_p02_lightgbm_adapters.py \
 tests/product/test_enh_e10_g01_p03_model_artifacts.py \
 tests/product/test_predictive_api_worker_e2e_e3.py
```

```text
...........................................                              [100%]
43 passed, 2 warnings in 18.97s
```

## Assertion と AC の対応

| assertion 群 | 確認する契約 | AC への寄与 |
| --- | --- | --- |
| `test_predictive_explanation_e3.py` | linear global/local の feature order、intercept / contribution、binary output scale | AC-01 |
| `test_predictive_leakage_e3.py` | explanation dataset の TEST-only / selection prohibition | AC-01 |
| P01 capability test | compatible linear method と terminology boundary | AC-01, AC-11 |

## 警告・非対象

2 件の warning は SHAP provider が binary array の API shape 変更を通知したもので、coefficient runner は対象外である。exit code、coefficient assertion、frozen scale assertion に failure はない。本 item は SHAP/LIME の provider semantics そのものを判定せず、item 030–080 がその根拠である。
