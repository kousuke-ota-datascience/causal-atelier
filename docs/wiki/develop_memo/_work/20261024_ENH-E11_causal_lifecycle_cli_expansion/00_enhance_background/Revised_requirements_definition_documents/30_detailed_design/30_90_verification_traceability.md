# 30_90_verification_traceability


---

## 23. Verification / test design

### 23.1 Architecture tests

- Domain/runtimeからbrowser/router/navigation descriptorへの禁止依存。
- Navigation descriptorをpersistent repository/UoWへ登録していないこと。
- Navigation Stage fieldをAnalysisSpecification / ExecutionPlan / Execution / StageExecutionへ追加していないこと。
- Project Management frontend responsibilityがAnalysis runtime moduleへ逆依存しないこと。
- presentation grouping / StagePresentationをruntime/persistence authorityへ流入させていないこと。

### 23.2 Catalog tests

- 3 Familyが各1件。
- exact Family slug/default Stage。
- Family内Stage id/slug uniqueness。
- deterministic order。
- backend catalogとfrontend表示一致。
- frontend duplicate full catalogなし。

### 23.3 Project routing / parent navigation tests

対象:

```text
/projects
/projects/new
/projects/{id}
/projects/{id}/overview
/projects/{id}/context
/projects/{id}/data
/projects/{id}/results
```

検証:

- direct link
- reload
- Back / Forward
- short-route replace normalization
- unauthorized Project
- unknown section
- Selected Project各sectionにProject List parent actionがある
- parent action targetがcanonical `/projects`
- parent actionが`history.back()`に依存しない
- direct-entry Selected Project -> Project List -> Back -> Selected Project -> Forward -> Project List
- keyboard activation / accessible name

### 23.4 Analysis routing tests

対象:

```text
/projects/{id}/analysis/{family}/{stage}
/resource/{resource_type}/{resource_id}
```

検証:

- direct link
- reload
- Back / Forward
- Family switch → catalog default Stage
- Stage switch
- resource/family mismatch
- invalid Family/Stage
- supported legacy entry one-way normalization
- current Stage heading/descriptionがroute-authoritative Stageと一致
- presentation-only groupがroute/stage authorityになっていない

### 23.5 Analysis Context tests

- Current Project = route `project_id`
- Analysis WorkspaceでProject switch不可/read-only
- cross-project Research Contextをrestoreしない
- cross-project Dataset Versionをrestoreしない
- incompatible Analysis Viewをrestoreしない
- Dataset Version変更 → incompatible Analysis View deselect
- missing context → Family/Stage route維持
- fake default resourceを生成しない

### 23.6 Exploratory placement tests

- Profile → `PROFILE`
- Data Quality → Profile result read-only
- Data Quality absence → `NO_PROFILE_RESULT` + Profile導線、Execution作成なし
- Distribution → `DISTRIBUTION`
- Relationships → `ASSOCIATION`
- Comparison → `GROUP_SUMMARY` + `TIME_TREND`
- TIME_TRENDで新しいtime-series model/type validationなし
- Findings → `CHART` + saved result
- CHARTがpersistent operation/result/artifact semanticsを維持

### 23.7 Causal placement / visibility tests

- Setup / Discovery / Identification / Estimation / Effects / Diagnostics / Sensitivityのcurrent semanticsを保持する。
- Navigation Stage切替がExecution Stage/lifecycleを変更しない。
- IdentificationはIdentification input/actionとEligibility/Gateをprimary表示する。
- Estimationはestimator config/actionをprimary表示し、Identification/Sensitivity controlを所有しない。
- EffectsとDiagnosticsはdistinct primary surfaceである。
- Refutation/Sensitivity control/resultはSensitivityだけがprimary ownerである。
- wrong-stage main controlはhiddenかつnon-interactiveである。
- affected Causal Stageに日本語中心のpurpose guidanceがある。
- current Stage headingをlegacy `Inference` headingで置換しない。

### 23.8 Predictive placement / feature selector tests

- Setup / Train / Predict / Metrics / Explainability / Model Managementを表示できる。
- Prediction Task → Split → Training → Evaluation → Explanation → Model Cardのbackend lifecycleを維持する。
- Navigation Stageとruntime Stageの1:1 mappingを要求しない。
- DRAFT form stateがStage switchで消失しない。
- Setup feature selector optionがselected Dataset Version schemaと一致する。
- Dataset/schemaなしではexplicit unavailable stateになり、架空optionを作らない。
- confirmed feature selectionがdialog open時にchecked stateへ復元される。
- pending change + Cancelでconfirmed selectionを変更しない。
- Confirmでchecked featureをdeterministic schema orderでcommitする。
- same logical feature listが`predictive-analysis-spec/1.feature_spec.feature_columns`へ同一semanticsでserializeされる。
- Dataset Version changeでnew schemaにないfeatureをsilent保持しない。
- Setup -> Train -> Setupでvalid confirmed feature selectionを保持する。
- Trainはfeature setをread-only表示しeditable selectorを持たない。
- Predictはrelevant execution specificationのfeature setをread-only表示しeditable selectorを持たない。
- ExplainabilityはPredictive Explanationをcausal effectとして表現しない。
- task-compatible model option / task default / structured parameter controlsをbackend capability metadataから構築する。
- LightGBM dependency unavailable時はoptionをreason付きでunavailable表示し、logistic/linearへsilent fallbackしない。
- `SHAP_TREE`はLightGBMでglobal/local、`LIME_TABULAR`はcompatible modelでlocal-onlyとしてscopeを表現する。
- global LIMEを選択可能にせず、pseudo-global resultを生成しない。
- Model Managementは`fitted-model/2` schema、provider/version、effective parameters、seed/determinism、feature/preprocessor identity、Model Card/explanation provenanceをread-only表示する。
- column-selector helperをFamily間で共有する場合、Causal Discovery等のcurrent selector/request validationをprotected regressionとする。

### 23.8.1 ENH-E10 predictive advanced model / XAI tests

- core-only environmentでAriadne import/startおよびexisting logistic/linear + coefficient flowがadvanced packagesなしで成立する。
- LightGBM classifier/regressorのtask/parameter validation、fixed deterministic settings、fit/predictをunit/contract testで検証する。
- `fitted-model/2` serialize→fresh load→predict parity、feature/preprocessor mismatch rejection、v1 read compatibilityをintegration testで検証する。
- SHAP binary/regression global/local、raw output scale、base/additivity、TEST identityをdeterministic testで検証する。
- LIME binary/regression local、TRAIN reference provenance、per-row seed、global unsupportedをdeterministic testで検証する。
- capability APIとFrontend model/method option、availability、parameter rendering、Model Management provenanceをcontract/integration testで検証する。
- Browser E2EはBinary + LightGBM + SHAP、Regression + LightGBM + LIMEの2 critical journeyに限定し、numeric/scientific correctnessのprimary proofにしない。
- new/materially rebuilt ENH-E10 testsは`tests/enhancement/enh_e10/<gate>/<layer>/`へ配置する。

### 23.9 Layout / accessibility tests

- major semantic sectionがvertical flowである。
- supported desktop/narrow viewportでsection composition起因のpage-level horizontal overflowがない。
- wide table/chartはcomponent-local overflowで扱える。
- hidden wrong-stage surfaceがfocus/interaction orderから除外される。
- current Stage heading、Project List parent action、feature selector dialog/checkbox/Confirm/Cancelがaccessible name/keyboard要件を満たす。

### 23.10 API / persistence regression tests

Project Management / Analysis Workspace分離やStage Content再編だけを理由とする次の変更がないことを確認する。

- new persistent navigation/AnalysisContext/presentation-group table
- new AnalysisContext backend API
- changed scientific operation semantics
- new DATA_QUALITY backend operation
- new Effects/Diagnostics Navigation-only runtime operation
- new standalone Predict scoring engine
- new Predictive specification version solely forfeature selector
- TIME_TREND scientific model mutation
- CHART display-only化

### 23.11 Headless execution tests

CLI / Python library / backend use caseからNavigation Stageなしでanalysis executionできることを確認する。

### 23.12 Browser E2E test seam

critical journeyはreal browserでcross-layer connectivityを確認する。

Project Management:

```text
Selected Project direct entry
  -> Project List
  -> Back
  -> Selected Project
  -> Forward
  -> Project List
```

Causal:

```text
Identification
  -> Estimation
  -> Effects
  -> Diagnostics
  -> Sensitivity
```

各transitionでcurrent headingとwrong-stage primary control absenceをkey checkpointとして確認する。

Predictive:

```text
Setup
  -> feature selector open / multi-select / Confirm
  -> Train (read-only selected feature context)
  -> Predict (execution-recorded feature context)
  -> Metrics
  -> Explainability
  -> Model Management
```

exhaustive visibility/state correctnessはdeterministic lower-level testをprimary proofとし、Browser E2Eはcross-layer journey proofとする。

---

**当該構成要素の詳細設計制約（関連Requirement）**

- **`NFR-015`**：Domain、Planner、Runner、API、Worker、UI、scientific benchmarkを分離testできる
- **`NFR-024`**：Navigation descriptor、route、renderer binding、runtime independenceをunit/integration/E2Eで分離検証できる
