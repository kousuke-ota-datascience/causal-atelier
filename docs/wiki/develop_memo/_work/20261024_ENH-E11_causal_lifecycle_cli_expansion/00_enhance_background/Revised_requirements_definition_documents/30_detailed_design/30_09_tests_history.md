<!-- ENH-E11 split working copy: not a formal approval. -->
# 30 — tests history

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [30_detailed_design.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/30_detailed_design.md) · blob `04d83541e55ab0364500afb4b92ef55c10785a0c`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

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

## 24. Current design invariants

次はcurrent detailed designのMUST NOT invariantである。

1. Project ManagementとAnalysis Workspaceを1つのpeer-tab navigationへ再混在させない。
2. Project-global resource管理をAnalytical Familyとして扱わない。
3. Family/Navigation StageをExecution/StageExecution statusへ読み替えない。
4. current Navigation Stageをscientific reproducibility inputへ保存しない。
5. frontendにbackend catalogのduplicate full definitionを持たせない。
6. Analysis Contextをnew persistent aggregate/APIとして実装しない。
7. Analysis Workspace内でCurrent Projectを直接switchさせない。
8. missing contextをfake default resourceで補完しない。
9. Data Quality用backend operationをUI都合で新設しない。
10. TIME_TRENDへ新しい時系列scientific semanticsをUI都合で導入しない。
11. CHARTのpersistent operation semanticsを表示専用へ退化させない。
12. legacy analytical entryをparallel navigation authorityとして維持しない。
13. Project/Analysis route stateをruntime domainへ逆流させない。
14. UI IA変更だけを理由にDB/API/backend domain semanticsを変更しない。
15. Selected ProjectからProject Listへのparent actionを`history.back()`で実装しない。
16. legacy `Inference`等のworkspace groupingをcurrent canonical Stage identityとして表示しない。
17. Causal presentation groupingをroute/Navigation Stage/runtime Stage/persistent stateへ昇格させない。
18. Identification / Estimation / Effects / Diagnostics / Sensitivityのmain responsibilityを1つのgeneric surfaceへflattenしない。
19. Refutation/Sensitivity editable controlをSensitivity以外のStageへ配置しない。
20. Predictive Train/Predictでfeature setをad-hocに編集させない。
21. feature selectorのためだけにnew Predictive specification/API/backend operationを追加しない。
22. Predict Navigation Stageのためだけにstandalone scoring engineを新設しない。
23. UI/IA再編だけを理由にLightGBM / LIME / SHAP等のnew analytical capabilityを暗黙追加しない。
24. major semantic sectionの横並びを理由にpage-level horizontal scrollを必須化しない。

---

## 30. CHANGE LOG

### 30.1 Effective snapshot baseline

Domain/runtime/capability/result/lineage、Family/Navigation Stage catalog、browser navigation、operation availability等のcurrent detailed designをeffective snapshotとして統合した。

### 30.2 Project Management / Analysis Workspace separation

Project ManagementとAnalysis Workspaceを別application/navigation scopeとして定義し、Project routes、resource ownership、Analysis Context、browser restoration、frontend component responsibilityをcurrent detailed designへ統合した。

### 30.3 Analytical surface placement

Causal / Exploratory / Predictiveのanalytical semanticsをNavigation Stage Contentsへ配置した。Exploratory Data Quality、TIME_TREND、CHARTについてbackend semanticsを変更しないcontractを明文化した。

### 30.4 Analysis Stage Content Architecture

Selected ProjectからProject Listへの明示的parent navigation、current Navigation Stageをprimary identityとするStage presentation、Causal Stage responsibility separation、Predictive Stage responsibility separation、Dataset-schema-backed Predictive feature selector、vertical layout/accessibility/history/test seamをcurrent effective detailed design本文へ統合した。

この変更はUI/IA/presentation designの具体化であり、canonical Navigation Stage catalog、API、persistence schema、backend analytical semantics、runtime execution lifecycleを変更しない。

### 30.5 ENH-E10 Predictive Advanced Modeling / XAI

- Model Capability / Explanation Method Capability registry、optional dependency isolation、LightGBM adapterを追加設計した。
- provider-neutral `fitted-model/2`、v1 read compatibility、same-runtime/config reproducibility contractを定義した。
- SHAP_TREE raw-output semantics、LIME_TABULAR local-only + TRAIN explanation referenceを定義した。
- `predictive-capabilities/1`をbackend authorityからadditiveに拡張し、Train / Explainability / Model Managementのconsumer contractを具体化した。
- G01/G02はdeterministic lower-level correctness、G03 Browser E2Eは2 critical product journeyをprimary scopeとする。
