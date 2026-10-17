# ENH-E10 G03 Trial 01 — Independent Verification 状況報告

## 状態

| 項目 | 値 |
| --- | --- |
| Gate / Trial | `G03` / `01` |
| Fixed Trial Candidate | `64bd2a18dd583349283cd5745edf63d9b28d61ad` |
| Tested SHA | `df278f76ff476143545d73037fe55f96664dae28` |
| Independent Gate Decision | **PASS** |
| evidence commit | `0a5638abcac6c5977225dfffede32fb77c764308` |
| evidence push | `causal-atelier/feature/ariadne_mvp_e10` へ完了 |
| G03 promotion | 未実施 |
| G04 | 未開始 |

## 実施内容

1. frozen G03 Test Instruction 07 を normative verification contract として使用した。
2. canonical G03 completion report からのみ Fixed Trial Candidate SHA を取得した。
3. candidate object、tested HEAD への ancestry、clean preflight、candidate 後の semantic diff を監査した。
4. G03 Test Item `001, 010, 020, 030, 040, 050, 100, 110, 120, 999` を実行・記録した。
5. ENH-E10 G01/G02 protected contracts、Predictive lifecycle、ENH-E8 stage responsibility regression、G03 browser runner readiness を非ブラウザ suite で検証した。
6. frozen compose lifecycle により Chromium browser journeys を clean environment で実行した。
7. browser 実行後は `docker compose ... down -v --remove-orphans` を完了した。

## Candidate identity audit

- candidate object は存在する。
- candidate は TEST_START_SHA の ancestor である。
- candidate 後の差分は frozen instruction、implementation report、status/evidence report のみであり、`src/`、`frontend/`、`tests/`、dependency、compose の semantic change はない。
- よって actual tested state は Fixed Trial Candidate と同一の product/test semantic state である。

## 検証結果

| 対象 | 結果 | 根拠 |
| --- | --- | --- |
| Candidate identity (001) | PASS | object / ancestry / post-candidate semantic diff audit |
| capabilities and model selector (010) | PASS | G01/G02 contract + browser model selection |
| stage responsibility regression (020) | PASS | ENH-E8 protected tests + canonical persisted outputs |
| explainability capability UI (030) | PASS | SHAP/LIME method selection、explicit unsupported boundaries |
| model management provenance (040) | PASS | Result/Artifact/Model Card / fitted-model evidence |
| G01/G02 protected regression (050) | PASS | model / explanation contract regression |
| Browser 100 | PASS | Binary + LightGBM + SHAP |
| Browser 110 | PASS | Regression + LightGBM + LIME |
| non-predictive smoke (120) | PASS | ENH-E8 protected surface tests + candidate diff audit |

### Non-browser suite

```text
58 passed, 2 warnings in 15.03s
```

warnings は SHAP provider の LightGBM binary array-shape notification 2 件であり、frozen assertion failure ではない。

### Browser evidence

| Scenario | Execution ID | Stage result | Required persistence |
| --- | --- | --- | --- |
| 100: Binary / LightGBM / SHAP | `4e45628b-a05e-4ceb-8b6f-782c88d4b992` | split/prepare/train/evaluate/explain: all `SUCCEEDED` | Explanation / Model Card Result、FITTED_MODEL / PREDICTIVE_EXPLANATION / MODEL_CARD artifact |
| 110: Regression / LightGBM / LIME | `96b4c134-37bc-498c-a751-4a00aa613c84` | split/prepare/train/evaluate/explain: all `SUCCEEDED` | Explanation / Model Card Result、FITTED_MODEL / PREDICTIVE_EXPLANATION / MODEL_CARD artifact |

Browser runtime は clean compose project `ariadne-enh-e10`、API/worker `Dockerfile.predictive-advanced`、Playwright Chromium `1.62.0`。raw runner evidence は `test-results/browser_e2e/enh_e10/evidence.json`、trace/video は同ディレクトリに保存された。

## 作成ファイル

独立検証 evidence:

- `30_test_report/G03/Trial01/ENH-E10_G03_01_001_candidate_identity.md`
- `30_test_report/G03/Trial01/ENH-E10_G03_01_010_capabilities_and_model_selector.md`
- `30_test_report/G03/Trial01/ENH-E10_G03_01_020_stage_responsibility_regression.md`
- `30_test_report/G03/Trial01/ENH-E10_G03_01_030_explainability_capability_ui.md`
- `30_test_report/G03/Trial01/ENH-E10_G03_01_040_model_management_provenance.md`
- `30_test_report/G03/Trial01/ENH-E10_G03_01_050_g01_g02_protected_regression.md`
- `30_test_report/G03/Trial01/ENH-E10_G03_01_100_browser_binary_lightgbm_shap.md`
- `30_test_report/G03/Trial01/ENH-E10_G03_01_110_browser_regression_lightgbm_lime.md`
- `30_test_report/G03/Trial01/ENH-E10_G03_01_120_non_predictive_smoke.md`
- `30_test_report/G03/Trial01/ENH-E10_G03_01_999_gate_decision.md`

本状況報告:

- `_work/G03_Trial01_independent_verification_status_report.md`

## 残存制約

- G03 Test Agent は promotion を実施しない。本報告は Gate Decision の独立 evidence であり、Gate status の外部更新ではない。
- G04 は開始していない。
- SHAP は LightGBM-only、LIME は local-only である。LIME one-hot perturbation の元カテゴリ組合せ制約は canonical limitation として維持される。
- provider/runtime version が変わる将来環境での数値同一性は主張しない。今回の判定は記録済み runtime / fixture / frozen contract に対するもの。
- 過去 evidence は削除・改変していない。
