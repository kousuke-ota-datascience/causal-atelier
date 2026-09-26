# ENH-E10 Architecture Discovery — Predictive Advanced Modeling / XAI

> **Document class:** Architecture Review / Current-State Fact Record  
> **Status:** `REVIEW_COMPLETE`  
> **Enhancement:** `ENH-E10`  
> **Reviewed branch:** `feature/ariadne_mvp_e10`  
> **Accepted pre-E10 baseline:** `c56a8809dea688380b113210bef12c30b50ca7f6`

## 1. Scope

LightGBM Binary Classification / Regression、SHAP、LIMEを追加しつつ、existing Predictive workflow、TEST isolation、TRAIN-only preprocessing、linear model behavior、predictive-not-causal boundaryを維持するためのcurrent architecture factを確認した。

本レビューではproduct codeを変更しない。

## 2. Current architecture facts

### 2.1 Runtime / lifecycle

**Fact**

Predictive full planは `split -> prepare -> train -> evaluate -> optional explain` であり、`PredictivePlanner` が同一 `predictive-analysis-spec/1` を各Stageへ渡す。

**Fact**

canonical Product execution lifecycleはgeneric `ExecutionService` / canonical Execution tablesへ移行済みで、`PredictiveWorkflowService` のlegacy Family-table claim/process authorityは明示的に無効化されている。

**Implication**

ENH-E10は新しいPredictive専用execution lifecycleを作らず、既存StageRunner/Generic Executor上でmodel/explanation backendを拡張する。

### 2.2 Predictive model authority

**Fact**

`src/ariadne/capabilities/predictive/modeling.py` の `MODEL_REGISTRY` がcurrent model selection authorityであり、以下のみ登録されている。

- `logistic_regression.v1` — `BINARY_CLASSIFICATION`
- `linear_regression.v1` — `REGRESSION`

**Fact**

current `fit_model()` / `predict()` はlibrary-neutral dict modelを使用し、`fitted-model/1` はcoefficients/intercept中心のJSON shapeである。

**Fact**

`PredictiveTrainRunner` はmodelへ `preprocessor_hash`, `feature_order`, `seed` を付与し、`FITTED_MODEL` Artifactを生成する。

**Fact**

`PredictiveEvaluateRunner` はTEST-only final evaluationとpreprocessor identityを検証する。

### 2.3 Preprocessing / data boundary

**Fact**

TRAINでfitされる `fitted-preprocessor/1` はnumeric mean imputation、numeric scaling、categorical one-hot encodingを行い、下流modelへfinite numeric matrixを渡す。

**Fact**

`predictive-analysis-spec/1` は既に `model_spec.model_id / parameters` と `explanation_spec.method / sampling / local_explanations` を保持可能である。

**Inference**

LightGBM native categorical/missing handlingを導入しなくてもadvanced modelを既存data boundaryへ追加できる。

### 2.4 Explanation authority

**Fact**

`PredictiveExplainRunner` は現在 `LINEAR_COEFFICIENT_CONTRIBUTION` のみを実装する。

**Fact**

unsupported methodはapproximate fallbackせず `NOT_APPLICABLE` + `EXPLANATION_METHOD_NOT_APPLICABLE` とする。

**Fact**

binary coefficient explanationのmodel output scaleは `LOG_ODDS`、prediction output scaleは `PROBABILITY`。

**Fact**

`predictive-explanation-result/1`, `predictive-explanation-artifact/1`, `predictive-model-card-result/1` が既に存在し、global/local、background reference、warnings/limitationsを格納できる。

### 2.5 Persistence / Artifact

**Fact**

`ArtifactDraft` はarbitrary bytes + media type + metadataをcanonical Artifact persistenceへ渡せる。artifact bytesはArtifactStore、identity/metadataはcanonical Artifact ownershipへ保存される。

**Implication**

LightGBM provider-supported serializationをdurable Artifact payloadとして保持するためのDB migrationは不要。

### 2.6 Capabilities API / frontend

**Fact**

`GET /projects/{project_id}/predictive/capabilities` は `predictive-capabilities/1` を返し、model registry、compatibility、explanation methodsをfrontendへ提供する。

**Fact**

capabilitiesは現在static `MODEL_REGISTRY` とsingle explanation methodから生成される。

**Fact**

frontend explanation selectorはcapabilities-drivenだが、Trainのmodel parametersとtask-change defaultはlogistic/linear IDをhard-codeしている。

### 2.7 Dependency topology

**Fact**

project Python requirementは `>=3.12,<3.13`。core dependenciesにはLightGBM/SHAP/LIMEが存在しない。

**External fact checked 2026-09-26**

- LightGBM stable: `4.7.0`
- SHAP stable: `0.52.0`; `0.53.0rc0` is pre-release
- LIME PyPI stable/latest: `0.2.0.1`

### 2.8 Browser E2E

**Fact**

existing Predictive Browser E2Eは `tests/browser_e2e/run_enh_e3_predictive.py`。

**Fact**

current browser harness uses `compose.yaml + compose.e1a.yaml`, Playwright Chromium 1.62.0 container, API/worker/frontend services, and evidence under `test-results/browser_e2e`.

**Fact**

current `Dockerfile` installs only core dependencies. Advanced engines therefore require a dedicated optional-extra runtime image/compose override for G03 blocking E2E.

## 3. Authority boundaries confirmed

| Concern | Current authority |
|---|---|
| Predictive spec | `predictive-analysis-spec/1` validation/domain |
| Model selection | backend `MODEL_REGISTRY` / resolver |
| TRAIN preprocessing | `PredictivePrepareRunner` + `fitted-preprocessor/1` |
| Model fit/predict | predictive modeling backend |
| TEST final evaluation | `PredictiveEvaluateRunner` |
| Explanation | `PredictiveExplainRunner` |
| Execution lifecycle | generic Product Execution / StageRunner / Generic Executor |
| Result/Artifact persistence | canonical Result/Artifact ownership + ArtifactStore |
| Product model/method option display | capabilities API consumer |
| Feature editing | Predictive Setup surface |

## 4. Duplicate / legacy paths

- legacy Family-table predictive processing code is retained but explicitly unreachable as lifecycle authority.
- no second canonical model/explanation authority should be introduced in frontend.
- existing coefficient-only `fitted-model/1` cannot represent LightGBM without semantic falsification; a versioned artifact path is required.

## 5. Current tests encoding protected behavior

Primary protected behaviors include:

- model/task registry compatibility
- logistic/linear fit/predict
- TRAIN-only preprocessing
- TEST selection prohibition
- feature/preprocessor identity
- coefficient global/local explanation
- predictive-not-causal wording
- predictive staged navigation
- Browser Predictive end-to-end execution/result/artifact flow

New/materially rebuilt ENH-E10 tests remain under `tests/enhancement/enh_e10/<gate>/<layer>/`.

## 6. Target decisions required

Architecture Review must decide:

1. optional dependency group/version bounds
2. LightGBM model IDs and parameter subset
3. categorical/missing/early-stopping policy
4. deterministic runtime policy
5. fitted-model artifact evolution and loader dispatch
6. failure taxonomy
7. explanation method IDs/compatibility
8. SHAP output/background/global/local/additivity
9. LIME scope/feature representation/sampling/reproducibility
10. explanation reference data
11. Predictive spec/result/capabilities schema versioning
12. UI default/unavailable behavior
13. Browser E2E advanced runtime and canonical execution model

All listed target decisions are resolved in `02_target_architecture_decision_record.md`.
