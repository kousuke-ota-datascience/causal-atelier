<!-- ENH-E11 split working copy: not a formal approval. -->
# 22 — history e8

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [22_product_basic_design.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/22_product_basic_design.md) · blob `87196f2f03a7f3367724bc05fb254d1a4d98109e`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

---

## 20. CHANGE LOG

### 20.4 ENH-E4 Canonical Execution Architecture

canonical Product runtime Execution authority、generic workflow core、persistent StageExecution、Result / Artifact / Lineage authority等の設計を継承する。

### 20.5 ENH-E5 Family × Navigation Stage Application Architecture

Project Workspaceのanalytical navigationをFamily / Family-local Navigation Stageへ再構成する。Navigation taxonomyはPresentation / Application / Capabilityの責務として追加し、Generic Workflow Coreおよびruntime Execution Stageへ依存を逆流させない。

### 20.6 ENH-E5 Phase I Canonical Convergence

- Outbox/nonexistent Port overstatementをD1 current contractへ訂正した。
- Navigation metadata endpoint/schema/route/default Stageをfreezeした。
- typed filter、subgroup、comparability、authorization、idempotency、lineage、reproducibility、frontend accessibilityをD2 targetとして具体化した。
- `StageAttempt.effective_random_seed` migrationを明示し、D3 capabilityをE5 acceptanceから分離した。


### 20.7 ENH-E7 Project Management / Analysis Workspace Basic Architecture

Application IAをProject ManagementとAnalysis Workspaceへ分離し、Project route、Analysis Context、resource ownership、existing Causal/Exploratory/Predictive surface placementをcurrent basic designへ統合した。API/persistence/backend execution semanticsはUI再配置だけを理由に変更しない。

### 20.8 ENH-E7 Product Basic Design Structure Restoration

- ENH-E2で確立していた「文書の設計粒度」「screen/function boundary」「operation / prerequisite / Resource effect / post-state / UI Gate」「画面遷移とlogical context handoff」という基本設計の記載粒度を復元した。
- Top-level IAのconcept authorityは`00_product_concept_memo.md > 3. Ariadne application model`へ集約し、本書ではsurface responsibility、route authority、resource lifecycle ownership、operation/state boundaryを詳細化する責務分離とした。
- Project Management / Analysis Workspace分離、Analysis Context、Family/Navigation Stage、existing capability placement、runtime/capability semanticsは維持した。



### 20.9 ENH-E10 Predictive Advanced Modeling / XAI

- backend Model / Explanation Capability registryをcompatibility・availability authorityとして追加した。
- LightGBM Binary Classification / Regression、`fitted-model/2`、SHAP_TREE、LIME_TABULARのproduct-level responsibilityを定義した。
- optional dependency isolation、no-silent-fallback、same-runtime/config reproducibility、Model Management provenanceをcurrent designへ統合した。
- existing `predictive-analysis-spec/1`、generic execution lifecycle、TRAIN-only preprocessing、TEST isolation、Predictive Stage responsibilityを維持した。


---


## ENH-E8 Addendum — Analysis Stage Content Architecture

### E8.1 Selected Project parent navigation

Selected Project shellは、`overview`, `context`, `data`, `results` の各local sectionで、canonical Project List `/projects` へ戻る明示的parent navigation actionを提供する。

このactionはbrowser historyのoriginに依存せず、既存Project Navigation authorityを用いて `/projects` をtargetとする。

### E8.2 Stage Contents identity

Analysis WorkspaceのStage Contentsでは、current canonical Navigation Stageをprimary heading / descriptionの主語とする。

legacy implementation grouping（例: `Inference` workspace）は内部実装として残してもよいが、current Stage identityを置換してはならない。

### E8.3 Causal presentation-only grouping

Causal sidebarに補助的なgroupingを表示する場合、presentation-onlyとする。

```text
分析設計
  Setup
因果構造
  Discovery
識別
  Identification
推定・評価
  Estimation
  Effects
  Diagnostics
  Sensitivity
```

group labelはroute、stage slug、canonical Navigation Stage、runtime Stage、persistent stateにならない。

### E8.4 Causal Stage Contents responsibility matrix

| Stage | 主責務 |
|---|---|
| Identification | estimand、識別戦略、adjustment set、assumption、Identification / Data Eligibility、Estimation gate |
| Estimation | identified estimandに対するestimator/nuisance/uncertainty/revision、Estimation実行 |
| Effects | saved Treatment Effect Result、ATE/ATT/CATE、interval、uncertainty、heterogeneity/comparison |
| Diagnostics | balance、overlap、ESS、weights、scientific warning |
| Sensitivity | Refutation / Sensitivity control、Result、robustness interpretation |

他Stageの情報が必要な場合はcompactなprerequisite/referenceとして表示し、他Stageのmain operation surfaceを複製しない。

Sensitivity/Refutation operationはSensitivityのみが所有する。

### E8.5 Predictive Stage Contents responsibility matrix

| Stage | 主責務 |
|---|---|
| Setup | Prediction Task、context/input、target/features、timing/horizon、Split/specification-level configuration。feature-column selectionはここで編集する |
| Train | read-only selected feature set、preprocessing/model/tuning、execution/status、fitted result reference |
| Predict | relevant execution specification由来のread-only feature set + existing prediction output/result/artifact。Navigationのためにstandalone scoring engineを追加しない |
| Metrics | Evaluation Result、primary/secondary metrics、subgroup/error analysis |
| Explainability | predictive explanation result/artifact。predictive-not-causal semanticsを明示する |
| Model Management | Model Card、fitted-model/preprocessor Artifact、Result/Artifact/Lineage reference |

既存 `predictive-analysis-spec/1` のfield/default/validation/generated semanticsは、presentation ownershipを再編しても維持する。Stage切替によってvalid draft inputを破棄しない。

#### E8.5.1 Predictive feature-column selector

Predictive Setupは、Dataset-schema-backed popup/dialog + checkbox multi-selectionをfeature-column編集のprimary interactionとして提供する。

```text
Selected Dataset Version
  -> schema columns
  -> open feature selector
  -> checkbox selection
  -> Confirm
  -> existing feature_spec.feature_columns
```

Design rule:

1. selected Dataset Versionのschemaをcandidate-column authorityとする。
2. comma-delimited free-textをprimary editing interactionにしない。
3. Confirmはchecked columnをexisting Predictive form/draft stateへcommitし、Cancelは変更しない。
4. Confirm後のcolumn orderはdeterministicとする。
5. Dataset Version変更時、新schemaに存在しないselected columnをsilentに保持しない。clearまたはvalid intersection保持を許可するが、破壊的reconcileは利用者へ示す。
6. target/excluded-column、feature availability、split、leakage、backend validationはexisting semanticsをauthorityとし、selector独自のanalytical validationを追加しない。
7. Trainではcurrent execution input feature setをread-only contextとして表示する。
8. Predictではrelevant saved execution specificationのfeature setをread-only contextとして表示する。
9. Train/Predictはeditable feature selectorを提供しない。
10. Causal Discovery selectorをgeneralize/reuseする場合、existing Discovery behaviorをprotected regressionとする。
11. このinteractionだけのために新しいDataset schema APIを追加しない。existing Dataset Version/schema authorityを使用する。

### E8.6 Layout principle

Analysis Stageの主要semantic sectionは縦方向のreading flowを基本とする。

compactな関連controlはlocal grid/flexを使用してよい。table/chart/preformatted result等のintrinsically wide contentはcomponent-local overflowを許可する。

独立semantic sectionを横方向へ連結し、primary operationにpage-level horizontal scrollを要求する構成は避ける。

### E8.7 Compatibility

ENH-E8はUI/IA変更のみを理由として以下を変更しない。

- canonical Navigation Stage catalog
- API contract
- persistence/schema
- backend domain/scientific semantics
- Predictive algorithm/explanation capability
- runtime `StageType`, `ExecutionPlan`, `Execution`, `StageExecution`
- existing `predictive-analysis-spec/1` semantics

ENH-E8時点ではLightGBM / LIME / SHAPを後続Enhancementへdeferした。current effective snapshotではENH-E10 §10.3.2がそのadvanced Predictive capability contractを所有する。
