# ENH-E10 G03 Trial 01 — 独立検証レポート日本語版（side output）

> この文書は canonical evidence の日本語 side output である。候補 SHA、tested SHA、実行結果、AC 判定、制約、Gate Decision は変更していない。canonical authority は `30_test_report/G03/Trial01/ENH-E10_G03_01_*.md` のままとする。

## 共通実行情報

| 項目 | 値 |
| --- | --- |
| Fixed Trial Candidate | `64bd2a18dd583349283cd5745edf63d9b28d61ad` |
| Tested SHA / TEST_START_SHA | `df278f76ff476143545d73037fe55f96664dae28` |
| Branch | `feature/ariadne_mvp_e10` |
| 非ブラウザ independent suite | `58 passed, 2 warnings in 15.03s`、exit `0` |
| Browser runtime | clean compose project `ariadne-enh-e10`、API/worker `Dockerfile.predictive-advanced`、Playwright Chromium `1.62.0` |

SHAP warning 2 件は LightGBM binary array-shape の upstream notification であり、凍結 assertion の失敗ではない。

## 001 Candidate Identity

対応 canonical: `ENH-E10_G03_01_001_candidate_identity.md`。AC mapping は META（mandatory candidate identity precondition）。判定は **PASS**。

`git cat-file`、`git show`、`git merge-base --is-ancestor`、candidate→HEAD diff、clean-tree preflight を実行し、全 audit command は exit `0` だった。completion report からのみ取得した candidate object は存在し、tested HEAD の ancestor である。candidate は advanced runtime Dockerfile、G03 browser runner、runner readiness test を変更する。candidate 後の変更は凍結 instruction、implementation/status/evidence report のみで、`src/`、`frontend/`、`tests/`、dependency、compose に semantic diff はない。

したがって `PRODUCT_SEMANTIC_CHANGE=NONE`、`TEST_IMPLEMENTATION_CHANGE=NONE`、`TEST_INFRASTRUCTURE_CHANGE=NONE`、`DOCUMENTATION_ONLY` であり、actual test target は Fixed Trial Candidate と同一の semantic implementation state である。clean tree の branch で同じ audit command を順に実行して再現する。後続 item の唯一の valid candidate input として使用できるため **PASS**。

## 010 Capabilities and Model Selector

対応 canonical: `ENH-E10_G03_01_010_capabilities_and_model_selector.md`。AC-01、AC-02、AC-08。判定は **PASS**。

`pytest` で G03 runner readiness、ENH-E10 G01/G02、Predictive training/evaluation/explanation/leakage/API-worker、ENH-E8 Causal/Predictive stage tests を実行し、`58 passed, 2 warnings in 15.03s`（exit `0`）だった。Browser scenario 100 で visible Train selector から `lightgbm_classifier.v1`、scenario 110 で `lightgbm_regressor.v1` を選択し、双方 `SUCCEEDED` となった。

G01 tests は logistic/linear defaults、LightGBM task compatibility、deterministic parameter、explicit error taxonomy を保護する。browser evidence は capability-driven selector から API request construction へ至ることを示す。candidate は selector production source を candidate 後に変更していない。上記 command と frozen browser lifecycle を再実行し、58 tests と両 LightGBM journey の success を要求する。compatible selection、parameter serialization、advanced runtime availability を満たすため **PASS**。

## 020 Stage Responsibility Regression

対応 canonical: `ENH-E10_G03_01_020_stage_responsibility_regression.md`。AC-03、AC-05、AC-12。判定は **PASS**。

再現コマンドは `pytest -q tests/product/test_enh_e8_g02_p02_causal_stage_surface_separation.py tests/product/test_enh_e8_g02_p03_predictive_stage_feature_selector.py tests/product/test_predictive_training_e3.py tests/product/test_predictive_evaluation_e3.py`（advanced extra / cached environment）であり、complete suite の一部として exit `0` だった。ENH-E8 tests は Setup-only feature edit authority と Train/Predict read-only feature context を保つ。両 browser scenario は API terminal execution を待ち、`PREDICTION`、`EVALUATION_RESULT`、`PREDICTIVE_EXPLANATION_RESULT`、`MODEL_CARD_RESULT` を確認したため、client-side numeric authority ではない。

candidate は frontend/navigation/API product semantic change を含まず、post-candidate は documentation only。Setup ownership、canonical backend output、targeted non-predictive regression が保持されるため **PASS**。

## 030 Explainability Capability UI

対応 canonical: `ENH-E10_G03_01_030_explainability_capability_ui.md`。AC-04、AC-07、AC-08。判定は **PASS**。

再現は `pytest -q tests/enhancement/enh_e10/g02/contract tests/enhancement/enh_e10/g02/integration`（advanced extra）と frozen browser lifecycle。complete suite 内で exit `0`。G02 contract は unknown method=`EXPLANATION_METHOD_NOT_REGISTERED`、linear SHAP=`EXPLANATION_METHOD_NOT_APPLICABLE`、global LIME=`EXPLANATION_SCOPE_NOT_SUPPORTED` を確認し、pseudo-global/fallback はない。Browser 100 は SHAP global/local、110 は local LIME を選択し、generated explanation result、predictive-not-causal UI text、persisted result/artifact を確認した。

candidate/post-candidate audit に未レビューの frontend/API semantic mutation はない。explicit incompatible/scope/dependency boundary と compatible method selection が実証されたため **PASS**。

## 040 Model Management Provenance

対応 canonical: `ENH-E10_G03_01_040_model_management_provenance.md`。AC-06、AC-07。判定は **PASS**。

再現は `pytest -q tests/enhancement/enh_e10/g01/integration tests/enhancement/enh_e10/g02/integration tests/product/test_predictive_api_worker_e2e_e3.py`（advanced extra）と frozen browser journeys。complete suite 内で exit `0`。G01 artifact tests は `fitted-model/2`、provider/version/runtime identity、load/predict parity を保持する。G02 tests は Result → Explanation Artifact → Model Card provenance equality（model/task/preprocessor/feature、provider/runtime、output scale、background/reference）を検証する。

Browser 100/110 は `MODEL_CARD_RESULT`、`FITTED_MODEL`、`MODEL_CARD`、`PREDICTIVE_EXPLANATION` を確認する。candidate 後は documentation only であり、read-oriented Model Management provenance contract は **PASS**。

## 050 G01/G02 Protected Regression

対応 canonical: `ENH-E10_G03_01_050_g01_g02_protected_regression.md`。AC-11。判定は **PASS**。

再現は `pytest -q tests/enhancement/enh_e10/g01 tests/enhancement/enh_e10/g02 tests/product/test_predictive_training_e3.py tests/product/test_predictive_evaluation_e3.py tests/product/test_predictive_explanation_e3.py tests/product/test_predictive_leakage_e3.py tests/product/test_predictive_api_worker_e2e_e3.py`（advanced extra）。complete G03 suite では exit `0`、`58 passed, 2 warnings` である。

G01 は registry、deterministic LightGBM adapter、artifact serialize/load/predict、invalid model/parameter error を保持する。G02 は coefficient、SHAP binary/regression、LIME binary/regression、TRAIN reference provenance、dependency absence、output scale、Result/Artifact/Model Card contract を保持する。candidate は G01/G02 implementation mutation ではなく advanced runtime/browser verification scoped であるため AC-11 は **PASS**。

## 100 Browser Binary LightGBM SHAP

対応 canonical: `ENH-E10_G03_01_100_browser_binary_lightgbm_shap.md`。AC-09、AC-03、AC-04、AC-06、AC-07。判定は **PASS**。

frozen lifecycle は `docker compose -f compose.yaml -f compose.e1a.yaml -f compose.enh_e10.yaml -p ariadne-enh-e10 down -v --remove-orphans`、同 project の `--profile e2e run --build --rm --entrypoint python browser-e2e tests/enhancement/enh_e10/g03/browser_e2e/run_predictive_advanced.py`、最終 `down -v --remove-orphans` である。runner と teardown の exit code は `0`。

`test-results/browser_e2e/enh_e10/evidence.json` は scenario 100=`PASS`、execution `4e45628b-a05e-4ceb-8b6f-782c88d4b992` を記録する。split/prepare/train/evaluate/explain は全て attempt 1 で `SUCCEEDED`。`PREDICTIVE_EXPLANATION_RESULT`、`MODEL_CARD_RESULT`、`FITTED_MODEL`、`PREDICTIVE_EXPLANATION`、`MODEL_CARD`、`PREDICTION` を確認した。Trace/video は同 directory にある。database/API は healthy、migrate exit 0、worker/frontend started。failed synchronization、page/console/network/API/worker error はないため failure classification は該当しない。

Browser は Binary、`lightgbm_classifier.v1`、`SHAP_TREE` を選択し、API terminal execution、Result/Artifact、final UI visibility を同期して generated explanation、Model Card identity、predictive-not-causal wording を要求した。これは direct backend success だけでない cross-layer proof であり **PASS**。

## 110 Browser Regression LightGBM LIME

対応 canonical: `ENH-E10_G03_01_110_browser_regression_lightgbm_lime.md`。AC-10、AC-03、AC-04、AC-06、AC-07。判定は **PASS**。

再現 lifecycle、runtime、exit code、trace/video の扱いは item 100 と同一。scenario は独立した deterministic regression project/dataset/context を生成し、100 の persistent state を使わない。

`evidence.json` は scenario 110=`PASS`、execution `96b4c134-37bc-498c-a751-4a00aa613c84` を記録する。全 stage は first attempt で `SUCCEEDED`、`PREDICTIVE_EXPLANATION_RESULT`、`MODEL_CARD_RESULT`、`FITTED_MODEL`、`PREDICTIVE_EXPLANATION`、`MODEL_CARD`、`PREDICTION` が存在する。Browser は Regression、`lightgbm_regressor.v1`、explicit local `LIME_TABULAR` を選択し、generated explanation、Model Card identity、artifact、predictive-not-causal wording を確認する。G02 protected test は LIME PREDICTION scale、TRAIN reference/row provenance、global-LIME explicit unavailable を別途確認する。failure/synchronization/page/console/network/API/worker error はない。よって pseudo-global fallback なしの frozen journeyとして **PASS**。

## 120 Non-predictive Smoke

対応 canonical: `ENH-E10_G03_01_120_non_predictive_smoke.md`。AC-12。判定は **PASS**。

再現は `pytest -q tests/product/test_enh_e8_g02_p02_causal_stage_surface_separation.py tests/product/test_enh_e8_g02_p03_predictive_stage_feature_selector.py`（advanced extra）。complete suite の一部として exit `0`。ENH-E8 Causal/Predictive protected surface tests は成功し、candidate diff は advanced Docker runtime、G03 runner/readiness test のみで、frontend/Causal/Project/Graph/API/persistence/navigation product semantic change を含まない。clean compose startup は両 predictive journey を実行可能にした。

本 item は ENH-E9 full suite を主張せず、凍結された「candidate-caused semantic regression がない」targeted condition を protected tests と diff audit で評価する。したがって AC-12 は **PASS**。

## 999 Gate Decision

対応 canonical: `ENH-E10_G03_01_999_gate_decision.md`。final authority は **PASS**。

Gate acceptance claim は、advanced predictive model/explanation capabilities が Train/Predict/Metrics/Explainability/Model Management から選択・実行・確認でき、existing Predictive Navigation Stage responsibility を維持することである。001 candidate identity、010 capability/model selector、020 stage responsibility、030 explainability UI、040 Model Management provenance、050 G01/G02 protected regression、100 Binary SHAP browser journey、110 Regression LIME browser journey、120 targeted non-predictive/transition-debt smoke はすべて PASS。AC-01〜AC-12、candidate identity、protected regression、blocking transition-debt conditions、2 browser journeys を満たす。

再現は item 010 の complete independent suite と item 100/110 の frozen clean-compose lifecycle。両 command group は exit `0`。candidate→tested state は semantic-state preserving、post-candidate は documentation/evidence only。verified failure、BLOCKED condition、未評価 MUST criterion はない。

この canonical 999 は downstream workflow が記録済み **PASS** に依拠できることを示すが、Test Agent は G03 promotion と G04 start を実行しない。
