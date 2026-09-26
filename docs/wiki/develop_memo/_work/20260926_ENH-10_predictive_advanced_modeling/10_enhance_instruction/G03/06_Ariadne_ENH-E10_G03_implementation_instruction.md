# Ariadne ENH-E10 G03 実装指示書 — Predictive Product Integration Contract

**Document class:** Primary Execution Contract
**Contract status:** `MATERIALIZED_DRAFT / NOT_EXECUTABLE`
**Execution mode:** `WORK_PACKAGE` — decision materialized; execution remains blocked until contract freeze
**Required packages:** `P01, P02, P03`
**First executable package:** `P01`
**Depends on:** `G01 PASS + G02 PASS`
**Self-containment:** MUST when FROZEN; current artifact is a materialized authoring draft
**Execution eligibility:** **NOT EXECUTABLE** until Human approval is recorded, G01/G02 PASS exist, and 06/07/P01-P03 are explicitly FROZEN.

- Project: Ariadne
- Enhancement: ENH-E10
- Active Gate: G03
- Gate name: Predictive Product Integration Contract
- Branch: `feature/ariadne_mvp_e10`
- Accepted pre-E10 code baseline: `c56a8809dea688380b113210bef12c30b50ca7f6`
- Mutable Control Sheet: N/A

## 1. Gate definition / acceptance claim

### Gate objective

G01のadvanced model capabilityとG02のexplanation capabilityを、ENH-E8で確立したPredictive Navigation Stage responsibilityを壊さずにTrain / Explainability / Model Managementへ統合し、userがmodel/method capabilityを選択・実行・確認できるproduct contractを成立させる。

### Contract claim established by PASS

G03 PASS後、ENH-E10全体として以下を利用可能とみなせる。

- Train surfaceでtask-compatible model backendをcapabilityから選択し、backend固有parameterを明示的に設定できる。
- Explainability surfaceでcurrent modelにcompatibleなexplanation methodとglobal/local capabilityを確認・選択できる。
- optional dependency unavailable状態がUI/APIで明示され、silent fallbackやinvalid selectionを起こさない。
- Predict / Metrics / Explainability / Model Managementでmodel identity、explanation method、artifact/result、runtime/package provenance、limitationsを追跡できる。
- existing `setup / train / predict / metrics / explainability / model-management` stage responsibility、Setup-owned feature editing、Train/Predict read-only feature semanticsを維持する。
- Binary Classification + LightGBM + SHAP、およびRegression + LightGBM + LIMEのcritical user journeyがreal browserからsystem boundaryを跨いで成立する。
- detailed numeric/scientific correctnessはG01/G02 lower deterministic testsがprimary proofであり、Browser E2Eはcross-layer connectivity proofに限定される。

### Why this is one Gate

G03は「advanced predictive capabilityが既存product surfaceから選択・実行・確認できる」という一つのproduct integration acceptance boundaryである。個別UI widget単位でGateを分割しない。

## 2. Effective current context

Accepted pre-E10 baselineでは以下を確認済み。

- Predictive Navigation Stagesは `setup / train / predict / metrics / explainability / model-management`。
- frontendは `/projects/{project_id}/predictive/capabilities` から `model_registry` と `explanation_methods` を取得して表示する。
- explanation method selectorはcapabilities responseから生成される。
- 一方、current `predictiveFamilySpec()` はmodel parameter payloadを `logistic_regression.v1` かそれ以外かでhard-codeし、task change handlerもclassification=logistic / regression=linearへ直接設定する。
- Train/Predictはfeature contextをread-only表示し、feature editingはSetup側のselectorがauthority。
- execution完了後、Results/Artifacts/Lineageを取得し、stageごとのResult/Artifactを表示する。
- `FR-149`〜`FR-152` はPredictive stage構成、既存spec semantics、Metrics/Explainability分離、read-oriented Model Managementを保護する。
- `FR-161` はLightGBM等をmandatory dependencyにしない。

G03は既存capabilities APIを拡張可能な軸として利用し、hard-coded model/method assumptionsをcapability-driven contractへ置換する。

## 3. Architecture Review decisions — effective values for freeze

Source decision record: `40_operator_workflows/architecture_review/02_target_architecture_decision_record.md`.

1. **Capabilities API**
   - endpoint remains `GET /projects/{project_id}/predictive/capabilities`.
   - schema remains `predictive-capabilities/1`.
   - existing top-level/model/method fields and their types remain available.
   - additive fields:
     - `task_defaults`
     - model `contract_version`
     - model `parameters` structured definitions
     - model `provider`, `dependency`, `available`, `unavailable_reason`, `provider_version`, `determinism`, `serializer_id`, `loader_id`, `default_for_tasks`
     - explanation `contract_version`, `dependency`, `available`, `unavailable_reason`, `provider_version`, `default_for_models`
     - `model_explanation_compatibility`
   - legacy `parameter_schema`, `deterministic_seed`, `compatibility`, and explanation `method/supported_models/supports_global/supports_local/model_output_scales` remain compatibility projections.
2. **Train UI**
   - current compatible model is retained on task change.
   - incompatible model switches to backend-declared `task_defaults[task].model_id`.
   - logistic/linear remain defaults.
   - model parameter controls are generated from structured model `parameters`.
3. **Unavailable state**
   - unavailable advanced model/method is visible but disabled with backend-provided reason.
   - no auto-fallback from explicitly selected unavailable advanced capability.
4. **Explainability UI**
   - linear default = `LINEAR_COEFFICIENT_CONTRIBUTION`.
   - LightGBM default = `SHAP_TREE`.
   - compatible `LIME_TABULAR` remains an explicit alternate local method.
   - scope control is derived from supports_global/supports_local.
5. **Model Management**
   - remains read-only.
   - display model ID/task/effective parameters, provider/library version, seed/determinism, feature/preprocessor identity, fitted-model artifact identity/schema, Model Card, explanation method metadata, lineage/runtime provenance.
6. **Predictive spec**
   - keep `predictive-analysis-spec/1`.
7. **Browser runtime**
   - `Dockerfile.predictive-advanced` installs `.[predictive-advanced]` for API/worker.
   - `compose.enh_e10.yaml` overrides API/worker builds to that image.
   - core Dockerfile/normal compose remain core-only.
   - Browser image remains Playwright 1.62.0 and includes ENH-E10 runner.
8. **Blocking Browser runner**
   - canonical runner path: `tests/enhancement/enh_e10/g03/browser_e2e/run_predictive_advanced.py`.
   - one runner contains exactly two required advanced predictive scenarios: Binary+LightGBM+SHAP and Regression+LightGBM+LIME.
   - detailed numeric correctness remains G01/G02 responsibility.

Human approval remains required before changing this Gate set to FROZEN.


