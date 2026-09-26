# Ariadne ENH-E10 G03 実装指示書 — Predictive Product Integration Contract

**Document class:** Primary Execution Contract — MATERIALIZED DRAFT  
**Self-containment:** MUST after freeze  
**Execution eligibility:** **NOT EXECUTABLE** until G01 and G02 PASS and G03 product-integration decisions are frozen.

- Project: Ariadne
- Enhancement: ENH-E10
- Active Gate: G03
- Gate name: Predictive Product Integration Contract
- Branch: `feature/ariadne_mvp_e10`
- Accepted pre-E10 code baseline: `c56a8809dea688380b113210bef12c30b50ca7f6`
- Contract status: `MATERIALIZED_DRAFT`
- Execution Mode: `UNFROZEN` — `WORK_PACKAGE` expected
- Depends on: G01 PASS + G02 PASS
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

## 3. Freeze blockers — MUST resolve before coding

1. predictive capabilities APIのresponse schema/version revision要否
2. model registry capability metadataのUI-consumable fields
3. model-specific parameter schemaをUIへどう公開/描画するか
4. unavailable optional capabilityのUI semantics: hide / disabled / visible-with-reason
5. task change時のdefault model選択ルール
6. incompatible model/method selectionのclient/server responsibility
7. Explainability global/local control semantics
8. Model Managementで表示するmodel/library/runtime provenance set
9. Result/Artifact displayのcanonical labels / limitations
10. schema compatibility policy for existing `predictive-analysis-spec/1`
11. Browser E2E canonical command、hermetic environment、fixture、bootstrap/teardown
12. Browser E2E critical journeyのexact route/synchronization/assertion
13. accessibility/focus/error presentation requirements for new controls

## 4. Expected execution-mode decomposition

`WORK_PACKAGE` を第一候補とする。

- capabilities/API contract + frontend model parameter rendering
- Explainability capability/compatibility UI
- Model Management/result/provenance presentation
- browser critical journey + protected navigation regression

P00/Pxxはfreeze後に作成する。

## 5. Required implementation semantics

1. **Capability-driven Train**
   - model selectorはG01 registry/capabilityのcurrent task-compatible modelsから構成する。
   - current logistic/linearだけを前提にしたhard-coded parameter payloadを解消する。
   - backend parameter controlsはfrozen parameter schemaに基づき、invalid/unsupported combinationを明示する。
   - task change時にsilent incompatible selectionを残さない。
   - Setup-owned feature selectionをTrainへ移さない。Trainはselected feature contextをread-onlyとして扱う。

2. **Capability-driven Explainability**
   - explanation selectorはG02 compatibility contractに従い、current modelでvalidなmethods/global/local capabilityを提示する。
   - unavailable dependency / unsupported model-method combinationのreasonをユーザーが認識可能にする。
   - unsupported combinationを別methodへsilent fallbackしない。

3. **Predict / Metrics**
   - existing responsibilityを維持し、G03のために新規standalone scoring engineを必須化しない。
   - prediction/evaluation outputsはG01 canonical model contractに従う。
   - numeric correctnessをfrontendで再計算しない。

4. **Model Management**
   - read-oriented scopeを維持する。
   - fitted model artifact、model ID/version、task、effective parameters、feature/preprocessor identity、analytical library/version、runtime provenance、Model Card、lineageをcurrent contractの範囲で確認可能にする。
   - deployment registry / online serving lifecycleへ拡張しない。

5. **Explainability presentation**
   - method、global/local、output scale、sample/background provenance、limitationsを表示可能にする。
   - Predictive Explanationをcausal explanationとして表記しない。
   - raw provider object dumpだけをuser-facing contractにしない。

6. **Optional capability state**
   - LightGBM/SHAP/LIME不在でもapplication startup/navigationは成立する。
   - unavailable capabilityを選択不能/明示errorとし、既存linear pathは利用可能なままにする。

## 6. Allowed scope

- predictive capabilities API/schema
- predictive frontend Train/Explainability/Model Management controls/presentation
- G01/G02 result/artifact/provenance read model integration
- validation/error display
- G03 browser journey/supporting tests
- accessibility/focus behavior for changed predictive controls

## 7. Explicitly prohibited scope

- Project Management変更
- Causal workflow / Graph workflow / Identification UX / Causal diagnostics変更
- Setup以外へfeature editing authorityを移すこと
- Predict Stageをfeature editing surfaceへ変更
- standalone scoring engineの新設を必須化
- deployment/online inference/model serving/production registry
- causal interpretation of SHAP/LIME
- repository-wide test migration
- G01/G02 semantic contractのsilent rewrite

## 8. Protected passed-Gate/upstream contracts

| Source | Protected semantic | Mandatory regression |
|---|---|---|
| G01 | model capability, artifact/load/predict/provenance | backend integration regression |
| G02 | explanation compatibility/global-local/provenance | explanation integration regression |
| ENH-E8 | Predictive stage responsibilities and Setup-owned feature editing | navigation/stage contract |
| ENH-E9 | Project/Causal/Graph stabilized flows | no unrelated regression |
| FR-149–152 | six Predictive stages, existing spec semantics, Metrics/Explainability separation, read-oriented Model Management | contract/frontend tests |

## 9. Schema / API / runtime policy

- capabilities APIをextension pointとして使う。UI側にlibrary-specific authorityを重複実装しない。
- frontend表示都合だけでmodel/explanation compatibilityをclient-only authorityにしない。backend validationを維持する。
- existing analysis specificationを破壊的に変更しない。schema revisionが必要ならfreezeされたmigration/compatibility ruleを適用する。
- package availability/versionはruntime capability stateであり、hard-coded frontend constantにしない。

## 10. Automated test obligations

新規/materially rebuilt testは `tests/enhancement/enh_e10/g03/<layer>/` に置く。

Lower deterministic layers:

- capabilities response model/method compatibility
- model-specific parameter schema rendering/serialization
- classification/regression task switch
- invalid/incompatible selection error
- optional dependency unavailable UI/API state
- Setup feature edit vs Train/Predict read-only contract
- Explainability global/local capability
- Model Management provenance/result/artifact rendering
- predictive-not-causal wording
- existing linear flow regression

Gate-blocking Browser E2Eは原則2 journeys:

1. Binary Classification → LightGBM → execute → Predict/Metrics → SHAP Explainability → Model Management artifact/model-card/provenance確認
2. Regression → LightGBM → execute → Predict/Metrics → LIME local Explainability → Model Management確認

Browser E2Eの責務はreal cross-layer connectivity。SHAP/LIME numeric correctness、serialization parity、fine-grained validationはG01/G02 lower layerをprimary proofとする。

## 11. Browser E2E operational contract — freeze required

FROZEN 07へ以下を具体値として記載する。

- canonical command
- current-source/hermetic bootstrap
- dataset/fixture
- route and user journey
- semantic synchronization points
- observable assertions
- screenshot/trace/network/log evidence
- teardown
- failure classification

fixed sleepをprimary synchronizationにしない。historical runnerがcurrent UIへ到達できない場合、ACを弱めずrunner/test orchestrationをcurrent journeyへ追従させる。

## 12. Candidate Assembly requirement

`READY_FOR_TEST` 前に:

- all G03 packages complete
- G01/G02 protected regression complete
- frontend/API focused tests complete
- Browser E2E coding-side smoke reaches both critical journeys or explicit BLOCKED evidence exists
- unresolved candidate-affecting change = NONE
- Fixed Trial Candidate SHA fixed
- Completion Report created

## 13. Coding Agent prohibited work

- Gate Decision / AC変更
- G01/G02 redefinition
- non-predictive cleanup
- Browser failureを根拠なしにproduction defectと決め打ちして修正
- test-side workaroundによるAC weakening
- repository-wide migration
- PASS declaration

## 14. Stop condition

draft中は `BLOCKED_CONTRACT_NOT_FROZEN`。  
FROZEN後は `READY_FOR_TEST` または `BLOCKED_*` で停止する。
