# ENH-E10 — Test Path Migration Addendum

## 目的と適用範囲

本 addendum は、ENH-E10 固有 test の physical path を `tests/product/` から
`tests/enhancement/enh_e10/<gate>/<layer>/` へ移設した後の current path authority を記録する。

対象 Gate は `G01` と `G02`。本書は過去の implementation completion、independent verification、FAIL/BLOCKED/PASS evidence を書き換えない。既存 report の旧 path は、その report が実行された時点の実コマンドであり、historical evidence として保持する。

## 移設の根拠

要求定義 `30_detailed_design.md` §23.8.1 は、新規または materially rebuilt した ENH-E10 test の配置を次に定める。

```text
tests/enhancement/enh_e10/<gate>/<layer>/
```

移設前には ENH-E10 固有 test 6 件が `tests/product/` に残っていた。これは target test architecture と一致しない。移設により、enhancement provenance、gate、verification layer を path から判別可能にした。

## Current path authority

| Gate | Layer | 旧 path（historical execution path） | current path（再実行 authority） |
| --- | --- | --- | --- |
| G01 | contract | `tests/product/test_enh_e10_g01_p01_model_capability.py` | `tests/enhancement/enh_e10/g01/contract/test_model_capability.py` |
| G01 | unit | `tests/product/test_enh_e10_g01_p02_lightgbm_adapters.py` | `tests/enhancement/enh_e10/g01/unit/test_lightgbm_adapters.py` |
| G01 | integration | `tests/product/test_enh_e10_g01_p03_model_artifacts.py` | `tests/enhancement/enh_e10/g01/integration/test_model_artifacts.py` |
| G02 | contract | `tests/product/test_enh_e10_g02_p01_explanation_capabilities.py` | `tests/enhancement/enh_e10/g02/contract/test_explanation_capabilities.py` |
| G02 | integration | `tests/product/test_enh_e10_g02_p02_shap_backend.py` | `tests/enhancement/enh_e10/g02/integration/test_shap_backend.py` |
| G02 | integration | `tests/product/test_enh_e10_g02_p03_lime_backend.py` | `tests/enhancement/enh_e10/g02/integration/test_lime_backend.py` |

`tests/enhancement/enh_e10/conftest.py` は ENH-E10 固有 deterministic predictive specification fixture を提供する。`g02/integration/predictive_execution.py` は SHAP/LIME full-DAG tests の shared execution helper である。これらは旧 `tests/product/test_predictive_explanation_e3.py` の private helper import への暗黙依存を置き換えるための test-support code であり、production code ではない。

## 移設 identity

| 項目 | 値 |
| --- | --- |
| Migration commit | `c46db7adcba206f317925ee7d250411327e7124b` |
| Commit subject | `test: organize ENH-E10 tests by gate and layer` |
| Production code change | なし |
| Dependency / lockfile change | なし |
| Frozen instruction change | なし |
| Historical test evidence rewrite | なし |

## 移設後の収集・動作確認

### Collection

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run --extra predictive-advanced pytest --collect-only -q \
  tests/enhancement/enh_e10/g01 \
  tests/enhancement/enh_e10/g02
```

```text
34 tests collected in 4.31s
```

### G01 contract isolation

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run --extra predictive-advanced pytest -q \
  tests/enhancement/enh_e10/g01/contract/test_model_capability.py
```

```text
.......                                                                  [100%]
7 passed in 3.78s
```

G01 capability test は LightGBM lazy-import isolation を含むため、SHAP provider を先に import しない独立 process で実行した。

### G01/G02 test と protected regression

```bash
MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run --extra predictive-advanced pytest -q \
  tests/enhancement/enh_e10/g01/unit \
  tests/enhancement/enh_e10/g01/integration \
  tests/enhancement/enh_e10/g02/contract \
  tests/enhancement/enh_e10/g02/integration \
  tests/product/test_predictive_training_e3.py \
  tests/product/test_predictive_evaluation_e3.py \
  tests/product/test_predictive_explanation_e3.py \
  tests/product/test_predictive_leakage_e3.py \
  tests/product/test_predictive_api_worker_e2e_e3.py
```

```text
...........................................                              [100%]
43 passed, 2 warnings in 16.52s
```

warnings は SHAP provider の LightGBM binary array-shape notification のみであり、test failure ではない。

## 既存 test report との整合性判断

| 観点 | 判断 |
| --- | --- |
| 過去 report の command / path | 当時の実行事実として正しいため変更しない |
| 過去 report の PASS / FAIL / BLOCKED decision | candidate と当時の実行に対する判断のため変更しない |
| current rerun path | 本 addendum の current path table と command を authority とする |
| frozen 07 instruction | current physical path を acceptance authority にせず、first discovery location として扱うため変更しない |
| future verification | `tests/enhancement/enh_e10/<gate>/` を第一探索先とし、本 addendum の path を用いる |

従って旧 path を残す historical report と、新 path を示す本 addendum は矛盾しない。前者は時間付き execution evidence、後者は post-migration current-state evidence である。

## 制約

- 本移設は test architecture correction であり、G02 Reverification 05 の Gate PASS を再判定・promotion しない。
- current test paths は移設 commit 以後の rerun authority である。過去 candidate SHA の内容に test path 移設を遡及適用しない。
- `tests/product/` の generic predictive regression tests は enhancement-specific test ではないため移設対象外とした。
