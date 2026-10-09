# G02 Trial 01 — 独立検証詳細実行報告（reverification 03）

- Gate: `G02`
- Trial: `01`
- 対象 Test Item: `001`, `010`–`090`, `999`
- Fixed Trial Candidate SHA: `d2d87e074338b06fc740252506ae1dba2b2a5c04`
- 前回 FAIL Candidate SHA: `67f1c4ef1281700a14b5a9acd0eacf00b5c904e0`
- TEST_START_SHA / 実テスト対象 HEAD: `7de36e443e193fd0fdf1ba6ce00b71f8ba0551eb`
- 実行環境: `feature/ariadne_mvp_e10`、working tree clean、Python `3.12.3`、`uv run --extra predictive-advanced`
- 総合結果: **FAIL**

## 受入基準と判定範囲

frozen G02 07 を唯一の acceptance authority とした。G02 Browser E2E は blocking item が `0` 件であるため実施していない。ここでの FAIL は、test harness や依存環境の問題ではなく、実行可能な Fixed Trial Candidate の product contract violation を確認した結果である。

| Test Item | AC | 判定 | 要点 |
| --- | --- | --- | --- |
| 001 | META | PASS | candidate identity / post-candidate semantic state を監査 |
| 010 | AC-01, AC-11 | PASS | coefficient explanation と predictive-not-causal 保護 |
| 020 | AC-02, AC-07 | PASS | capability matrix と global LIME 明示拒否 |
| 030 | AC-03 | PASS | binary SHAP の raw LOG_ODDS / global-local output |
| 040 | AC-04 | PASS | regression SHAP の raw PREDICTION / additivity |
| 050 | AC-05 | PASS | binary LIME provider execution / positive-class probability |
| 060 | AC-06 | PASS | regression LIME provider execution / TRAIN reference |
| 070 | AC-08 | PASS | SHAP/LIME absent runtime の explicit error |
| 080 | AC-09, AC-11 | **FAIL** | Model Card に LIME provenance がない |
| 090 | AC-12 | **FAIL** | baseline G01 flow が PREPARE で失敗 |

## 001 — Candidate identity と semantic state

実行コマンド:

```bash
git cat-file -e d2d87e074338b06fc740252506ae1dba2b2a5c04^{commit}
git merge-base --is-ancestor d2d87e074338b06fc740252506ae1dba2b2a5c04 HEAD
git diff --name-status d2d87e074338b06fc740252506ae1dba2b2a5c04..7de36e443e193fd0fdf1ba6ce00b71f8ba0551eb
```

観測事実:

- candidate Git object は存在し、actual HEAD の祖先である（ancestry check exit `0`）。
- candidate 後の差分は canonical/remediation completion reports と prior verification evidence のみである。
- `src/`、`tests/`、`pyproject.toml`、`uv.lock`、migration、frontend に candidate 後の差分はない。
- candidate は前回 FAIL SHA と異なる remediation checkpoint である。

従って actual test target は Fixed Trial Candidate と同一の semantic implementation state である。結果は **PASS**。

## 010–030 — coefficient / compatibility / binary SHAP

実行コマンド:

```bash
MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run --extra predictive-advanced pytest -q \
  tests/product/test_enh_e10_g02_p01_explanation_capabilities.py \
  tests/product/test_enh_e10_g02_p02_shap_backend.py \
  tests/product/test_enh_e10_g02_p03_lime_backend.py \
  tests/product/test_predictive_explanation_e3.py
```

raw result:

```text
.............                                                            [100%]
13 passed, 1 warning in 14.24s
exit code: 0
```

warning は SHAP provider が binary classifier の array shape 変更を通知したものだけであり、assertion failure はない。

観測された契約境界は次のとおりである。

- unknown method: `EXPLANATION_METHOD_NOT_REGISTERED`
- `SHAP_TREE` + linear model: `EXPLANATION_METHOD_NOT_APPLICABLE`
- global `LIME_TABULAR`: `EXPLANATION_SCOPE_NOT_SUPPORTED`。pseudo-global output や fallback はない。
- coefficient explanation は既存の feature order、LOG_ODDS model output / PROBABILITY prediction output、TEST-only explanation、predictive-not-causal limitation を保持する。
- binary SHAP は LightGBM fixture で raw `LOG_ODDS`、tree-path-dependent、named global features、local TEST rows を生成する。

これらの範囲で 010 / 020 / 030 は **PASS**。

## 040 — regression SHAP

固定 synthetic fixture（60 rows、features `x` / `group`、LightGBM seed `3`、`num_boost_round=8`、`min_data_in_leaf=4`）で `explain_shap_tree` を実行した。

```text
method=SHAP_TREE
output_scale=PREDICTION
background={kind: TREE_PATH_DEPENDENT}
global_features=[x, group]
local_rows=[0, 1]
additivity_residuals=[1.0658141036401503e-14, 1.0658141036401503e-14]
exit code: 0
```

最大残差は frozen tolerance（`atol=1e-6`, `rtol=1e-5`）より十分に小さい。結果は **PASS**。

## 050 / 060 — binary / regression LIME

binary LIME は上記 13-test suite で provider execution を検証した。観測された事項は、`PROBABILITY` scale、非空の provider-derived signed contribution、TEST local row、TRAIN reference partition、per-row effective seed、frozen LIME parameter set である。結果は **PASS**。

regression LIME は、`linear_regression.v1`、`LIME_TABULAR`、`FIRST_N size=5 seed=17`、numeric 120-row fixture で独立の end-to-end probe を実行した。

```text
outcome_status=SUCCEEDED
split=SUCCEEDED
prepare=SUCCEEDED
train=SUCCEEDED
evaluate=SUCCEEDED
explain=SUCCEEDED
lime_method=LIME_TABULAR
local_count=5
output_scale=PREDICTION
reference.schema_version=predictive-explanation-reference/1
reference.partition=TRAIN
reference.count=72
reference.seed=17
reference.hash=274d65f9ce0fad30cddd1d7c31b5b23cdb647448b4dfbaf879ef7af7bd2d15b7
exit code: 0
```

この probe は LIME local output の provider execution、preprocessed feature representation、TRAIN-only reference と TEST explanation row の分離を支持する。050 / 060 は **PASS**。ただし Model Card への provenance 永続化は別 acceptance（080）であり、この結果だけから AC-09 を PASS としない。

## 070 — optional dependency absence

Python `-S` と temporary site layer を用い、`shap` / `lime` と各 dist-info を除外した。core capability module は import でき、raw output は以下であった。

```text
SHAP_TREE_availability={'available': False, 'version': None,
 'reason': 'Optional dependency shap is not installed'}
SHAP_TREE_error=EXPLANATION_DEPENDENCY_UNAVAILABLE
LIME_TABULAR_availability={'available': False, 'version': None,
 'reason': 'Optional dependency lime is not installed'}
LIME_TABULAR_error=EXPLANATION_DEPENDENCY_UNAVAILABLE
exit code: 0
```

依存欠如は core/model flow import を壊さず、method selection は明示的 error となる。silent fallback は観測されない。結果は **PASS**。

## 080 — provenance / Model Card（FAIL）

060 の regression LIME probe は explanation result に local provider output と TRAIN reference を保持した。一方、同じ execution の `MODEL_CARD_RESULT` は以下の keys だけを持った。

```text
code_runtime_metadata, deployment_population, feature_set, intended_use,
limitations, model_artifact_provenance, model_descriptor, schema_version,
selected_hyperparameters, split_strategy, test_metrics, training_data,
validation_metrics, warnings
```

`explanation_method` がなく、LIME method/version、local sample identity、TRAIN reference identity/hash、effective seed/parameters、output scale、provider package/runtime provenance のいずれも Model Card から追跡できない。

これは frozen AC-09 の「explanation result/artifact/model-card が provenance set を preserve」の violation である。runtime product output の観測に基づくため test-side defect ではない。結果は **FAIL**。

## 090 — G01 protected regression（FAIL）

実行コマンド:

```bash
MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run --extra predictive-advanced pytest -q tests/product/test_predictive_training_e3.py
```

raw result:

```text
test_full_predictive_dag_is_deterministic_and_keeps_test_out_of_training FAILED
test_regression_uses_only_registered_deterministic_linear_model FAILED
2 failed in 4.64s
```

直接 runtime reproduction:

```text
outcome_status=FAILED
split=SUCCEEDED
prepare=FAILED error={'type': 'KeyError', 'message': "'sampling'"}
train=SKIPPED_DUE_TO_PREREQUISITE
evaluate=SKIPPED_DUE_TO_PREREQUISITE
```

candidate diff inspection では、`PredictivePrepareRunner` が空の baseline `explanation_spec` に対して `explanation_specification["sampling"]` を無条件に参照する。既存 linear/logistic flow は explanation を要求しないため、PREPARE failure は G01 protected regression の product violation である。

なお、registry / adapter / artifact / leakage の isolated G01 command は `25 passed in 5.39s` だったが、この成功は baseline end-to-end flow failure を相殺しない。結果は **FAIL**。

## 判定理由と次の境界

AC-09 と AC-12 はいずれも MUST であり、どちらか一つでも未成立なら G02 PASS は許可されない。本実行では両方が independently confirmed された。よって Gate Decision は **FAIL**、promotion は **PROMOTION_NOT_ALLOWED** である。

修正側は、(1) LIME method-specific provenance を Model Card に schema v1 の additive fields として保持し、(2) 空の `explanation_spec` を使う既存 predictive flow を壊さないようにする必要がある。修正後は distinct remediation candidate を固定し、すべての protected / G02 acceptance を独立再検証すること。
