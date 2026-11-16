# 22_17_stage_contents


---

## 17. Analysis Stage Contents の機能設計

### 17.1. Selected Project parent navigation

Selected Project shellは、`overview`, `context`, `data`, `results` の各local sectionで、canonical Project List `/projects` へ戻る明示的parent navigation actionを提供する。

このactionはbrowser historyのoriginに依存せず、既存Project Navigation authorityを用いて `/projects` をtargetとする。

### 17.2. Stage Contents identity

Analysis WorkspaceのStage Contentsでは、current canonical Navigation Stageをprimary heading / descriptionの主語とする。

legacy implementation grouping（例: `Inference` workspace）は内部実装として残してもよいが、current Stage identityを置換してはならない。

### 17.3. Causal presentation-only grouping

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

### 17.4. Causal Stage Contents responsibility matrix

| Stage | 主責務 |
|---|---|
| Identification | estimand、識別戦略、adjustment set、assumption、Identification / Data Eligibility、Estimation gate |
| Estimation | identified estimandに対するestimator/nuisance/uncertainty/revision、Estimation実行 |
| Effects | saved Treatment Effect Result、ATE/ATT/CATE、interval、uncertainty、heterogeneity/comparison |
| Diagnostics | balance、overlap、ESS、weights、scientific warning |
| Sensitivity | Refutation / Sensitivity control、Result、robustness interpretation |

他Stageの情報が必要な場合はcompactなprerequisite/referenceとして表示し、他Stageのmain operation surfaceを複製しない。

Sensitivity/Refutation operationはSensitivityのみが所有する。

### 17.5. Predictive Stage Contents responsibility matrix

| Stage | 主責務 |
|---|---|
| Setup | Prediction Task、context/input、target/features、timing/horizon、Split/specification-level configuration。feature-column selectionはここで編集する |
| Train | read-only selected feature set、preprocessing/model/tuning、execution/status、fitted result reference |
| Predict | relevant execution specification由来のread-only feature set + existing prediction output/result/artifact。Navigationのためにstandalone scoring engineを追加しない |
| Metrics | Evaluation Result、primary/secondary metrics、subgroup/error analysis |
| Explainability | predictive explanation result/artifact。predictive-not-causal semanticsを明示する |
| Model Management | Model Card、fitted-model/preprocessor Artifact、Result/Artifact/Lineage reference |

既存 `predictive-analysis-spec/1` のfield/default/validation/generated semanticsは、presentation ownershipを再編しても維持する。Stage切替によってvalid draft inputを破棄しない。

#### 17.5.1. Predictive feature-column selector

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

### 17.6. Layout principle

Analysis Stageの主要semantic sectionは縦方向のreading flowを基本とする。

compactな関連controlはlocal grid/flexを使用してよい。table/chart/preformatted result等のintrinsically wide contentはcomponent-local overflowを許可する。

独立semantic sectionを横方向へ連結し、primary operationにpage-level horizontal scrollを要求する構成は避ける。

### 17.7. Compatibility

ENH-E8はUI/IA変更のみを理由として以下を変更しない。

- canonical Navigation Stage catalog
- API contract
- persistence/schema
- backend domain/scientific semantics
- Predictive algorithm/explanation capability
- runtime `StageType`, `ExecutionPlan`, `Execution`, `StageExecution`
- existing `predictive-analysis-spec/1` semantics

ENH-E8時点ではLightGBM / LIME / SHAPを後続Enhancementへdeferした。current effective snapshotではENH-E10 §10.3.2がそのadvanced Predictive capability contractを所有する。

**当該機能に適用する設計制約（関連Requirement）**

- **`FR-175`**：Data Qualityはdedicated backend operationを新設せずread-only availabilityとして扱い、Comparisonの`TIME_TREND`は既存grouping/aggregation semanticsを維持し、Findingsの`CHART`は既存persistent operation/result/artifact semanticsを維持する
- **`FR-174`**：existing Causal / Exploratory / Predictive capabilityを定義済みStage Contentsから操作可能にし、UI再配置だけを理由にanalysis execution semanticsを変更しない
