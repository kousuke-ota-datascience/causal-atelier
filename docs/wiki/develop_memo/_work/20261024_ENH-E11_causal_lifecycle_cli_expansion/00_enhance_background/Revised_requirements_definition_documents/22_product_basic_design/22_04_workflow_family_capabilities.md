<!-- ENH-E11 split working copy: not a formal approval. -->
# 22 — workflow family capabilities

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [22_product_basic_design.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/22_product_basic_design.md) · blob `87196f2f03a7f3367724bc05fb254d1a4d98109e`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

---

## 9. Generic Workflow Core

### 9.1 Planner

`PlannerRegistry`はAnalysis FamilyとSpecification Schema VersionからPlannerを解決する。

```text
AnalysisSpecification
  ↓
PlannerRegistry.resolve(family, schema_version)
  ↓
Family Planner
  ↓
ExecutionPlan
```

PlannerはDomain上のruntime planを生成し、browser navigation stateを入力として要求しない。

### 9.2 Plan

Execution Planはruntime Stage DAGである。

- Stage keyはPlan内一意。
- Stage Typeはruntime operation identityを表す。
- Edgeはoutput / input bindingを表す。
- cycle禁止。
- required input未解決禁止。
- Runner未登録禁止。

Navigation Stageのsidebar orderをExecution Plan dependencyへ変換しない。

### 9.3 Executor

Generic Executorはcanonical lifecycle/application serviceが所有するworkflow execution context内で、Analysis内容を知らずにruntime Stageを実行する。

1. dependency解決
2. runtime Stage sequencing
3. Runner解決・invocation
4. workflow-level validation
5. temporary output binding

canonical Execution lifecycleはNavigation改修の対象外とし、current contractを維持する。基本設計上の境界は次のとおり。

- Execution technical statusは`QUEUED / RUNNING / SUCCEEDED / FAILED / CANCELLED`で管理する。
- Worker ownershipは`Execution.lease_owner / lease_expires_at`とrepository-level claim / renew / completeで管理し、Navigation stateをclaim条件へ追加しない。
- retry/rerun/reviseはcanonical Execution / revision semanticsとして扱い、Navigation Stage遷移へ変換しない。
- runtime Stageの進行は`StageExecution`とappend-only `StageAttempt`で表現する。
- Result / Artifactはcanonical Execution / StageExecution ownershipから生成・永続化し、browser routeやCurrent Navigation Stageをpersistent ownership fieldへ追加しない。
- transaction境界とpersistent lifecycle authorityはproduct application / persistence側に残し、Navigation componentへ移さない。

### 9.4 Runner Registry

runtime Runner Registryは`StageType`によりrunnerを解決する。

Navigation Stage IDを`StageType`として登録しない。巨大な`if navigation_stage == ...`をExecutorへ追加しない。

### 9.5 Navigation Stageとの境界

次を禁止する。

- `NavigationStageDescriptor`を`StageDefinition` / `StageExecution`のsubtypeにする。
- Navigation Stage IDをruntime `StageType`へ流用する。
- `AnalysisSpecification.navigation_stage`をexecution prerequisiteとして追加する。
- runtime moduleからbrowser route / Navigation Stage moduleへ依存する。

#### 9.5.1 Distribution

`Exploratory / Distribution`がDataset/profile/resultのreadだけで成立する場合、対応するruntime Execution Stageを作らない。

#### 9.5.2 Metrics

`Predictive / Metrics`は既存evaluation Resultを読むだけで成立してよい。Navigation taxonomyを理由に`METRICS` runtime Stageを新設しない。

#### 9.5.3 Explainability

1 Navigation Stageから複数read/compute use caseを呼び出してよい。Navigation StageとExecution Stageのcardinalityを1:1へ固定しない。

### 9.6 CLI / Library independence

CLI / Python library / backend use caseは、Analysis Specificationまたは既存use-case inputだけでexecutionを開始できる。

`Current Navigation Stage`、browser route、sidebar stateをrequired inputへ追加しない。


## 10. Family別Workflow / Capability

この章で扱う`Workflow`はruntime execution semanticsであり、5章のNavigation Stage一覧とは別概念である。

### 10.1 Exploratory

現行実装の`ExploratoryPlanner`は、`exploratory-analysis-spec/1`のoperationを次のruntime Stageへ写像し、**1 Execution Planにつき1 runtime Stage**を生成する。

| family_spec.operation | runtime stage_key | StageType |
| --- | --- | --- |
| `PROFILE` | `profile` | `exploratory.profile.v1` |
| `DISTRIBUTION` | `distribution` | `exploratory.distribution.v1` |
| `ASSOCIATION` | `association` | `exploratory.association.v1` |
| `GROUP_SUMMARY` | `aggregate` | `exploratory.aggregate.v1` |
| `TIME_TREND` | `time_trend` | `exploratory.time_trend.v1` |
| `CHART` | `chart` | `exploratory.chart.v1` |

Navigation Stage:

```text
Profile / Data Quality / Distribution / Relationships / Comparison / Findings
```

は上記runtime operationと同一taxonomyではない。例えば`Data Quality`や`Findings`に同名runtime Stageは存在しなくてよく、保存済みDataset/Result/Annotation/Artifactのreadで成立してよい。Navigation Stageを開いたことだけを理由にpersistent Executionを作らない。

### 10.2 Causal

現行実装の`CausalPlanner`は`causal-analysis-spec/2`向けcompatibility plannerである。canonical `Execution.operation`を次のruntime StageTypeへ写像し、**1 canonical Executionにつき1 runtime StageからなるExecution Plan**を生成する。

| ExecutionOperation | StageType |
| --- | --- |
| `DISCOVERY` | `causal.discovery.v1` |
| `IDENTIFICATION` | `causal.identification.v1` |
| `ESTIMATION` | `causal.estimation.v2` |
| `REFUTATION` | `causal.refutation.v1` |
| `SENSITIVITY` | `causal.sensitivity.v1` |

したがって、現行実装のruntimeを次のような単一Plan内のDAGとして扱わない。

```text
IDENTIFICATION -> ELIGIBILITY -> ESTIMATION -> ...
```

`IDENTIFICATION`処理から`DATA_ELIGIBILITY_RESULT`等が生成され得ることと、`ELIGIBILITY`というruntime Stageが存在することは別である。科学的な前提関係はcanonical Executionの`input_graph_version_id` / `input_result_id`等とResult lineageで表現される。

Navigation側の`Setup / Discovery / Identification / Estimation / Effects / Diagnostics / Sensitivity`はユーザーの作業・閲覧コンテキストであり、runtime StageTypeと1:1対応させない。Identification / Estimationの科学的責務分離はNavigation設計として維持するが、それを理由に既存Causal runtime planを多段化しない。

### 10.3 Predictive

現行実装のfull Predictive planは次のruntime Stageを生成する。

```text
SPLIT -> PREPARE -> TRAIN -> EVALUATE -> optional EXPLAIN
```

主なdependencyは次である。

- `split.partition_manifest -> prepare.partition_manifest`
- `prepare.training_bundle / fitted_preprocessor -> train`
- `prepare.evaluation_bundle / fitted_preprocessor`および`train.frozen_model -> evaluate`
- Explainが有効な場合はprepare/train/evaluateの必要outputをExplainへbindingする。

各runtime Stageの責務:

- SPLIT: immutable partition artifactを生成する。
- PREPARE: partition manifestを用いてtraining/evaluation bundle、fitted preprocessor、explanation向け入力を生成する。
- TRAIN: training bundleとfitted preprocessorからfrozen modelとtraining summaryを生成する。
- EVALUATE: frozen modelとevaluation bundleを用いてevaluation summaryを生成する。
- EXPLAIN: 有効なexplanation specificationに従ってexplanation summary / model card等を生成する。

Navigation側の`Setup / Train / Predict / Metrics / Explainability / Model Management`は、これらruntime stageと1:1対応させない。特にNavigation `Train`はruntime `train`単体実行を意味せず、`Metrics`は保存済みevaluation Resultのreadで成立し得る。

Predictiveの既存設定項目、default、validation、generated `predictive-analysis-spec/1` semanticsは全量保持する。

#### 10.3.1 Predictive subgroup evaluation

- evaluation populationはuntouched TEST。
- user-specified subgroup columnごとに独立sliceし、automatic intersection/discovery/fairness frameworkは追加しない。
- subgroup columnはfeatureである必要はなく、partition row identity/ordinalによりTEST rowへ対応付ける。
- nullはexplicit subgroupとして扱う。
- primary/secondary metricそれぞれに`sample_count`を必須で返す。
- uncertaintyはnonparametric percentile bootstrap、confidence=0.95、resamples=1000、deterministic seed。
- `n < 2`またはvalid resamples < 200ではCIを返さずwarningを返す。
- metricが計算不能なgroupではvalue/uncertaintyを`null`とし値を捏造しない。
- outputはgroup valueをmap keyに埋め込まずrecord listとする。


#### 10.3.2 Predictive advanced model / XAI capability

ENH-E10ではexisting Predictive lifecycleを変更せず、model / explanation capabilityをprovider-neutralに拡張する。

Canonical model IDs:

| Model | Task | Default |
|---|---|---:|
| `logistic_regression.v1` | BINARY_CLASSIFICATION | Yes |
| `linear_regression.v1` | REGRESSION | Yes |
| `lightgbm_classifier.v1` | BINARY_CLASSIFICATION | No |
| `lightgbm_regressor.v1` | REGRESSION | No |

Model selection / compatibility / availability / parameter definitionのauthorityはbackend Model Capability registryとする。Frontendはこのmetadataのconsumerであり、model IDごとの独自compatibility tableをcanonical authorityとして持たない。

Advanced dependencyはoptional extra `predictive-advanced` とし、current approved boundsはLightGBM `>=4.7.0,<4.8`、SHAP `>=0.52.0,<0.53`、LIME `==0.2.0.1`。core startup/importはこのextraを要求しない。Unavailable capabilityは明示し、existing model/methodへのsilent fallbackを行わない。

LightGBMはexisting TRAIN-fitted numeric/one-hot feature matrixを受け取る。ENH-E10ではnative categorical、native missing handling、early stoppingを導入せず、TRAIN-only preprocessingとTEST isolationを維持する。

LightGBM exposed parameter set:

- `num_boost_round`
- `learning_rate`
- `num_leaves`
- `max_depth`
- `min_data_in_leaf`
- `lambda_l2`

実行はCPU、`deterministic=true`、`force_col_wise=true`、`num_threads=1`をcurrent reproducibility contractとし、same-runtime/config stabilityを対象とする。cross-platform bitwise identityは保証しない。

New fitted model writes use provider-neutral `fitted-model/2` envelope。linear payloadは`ariadne-linear-json/1`、LightGBM payloadは`lightgbm-model-string/1`。existing `fitted-model/1`はread compatibilityを維持する。Python pickle/joblibをcanonical portable model representationとしない。

Explanation methods:

| Method | Compatible model | Scope | Model-output semantics |
|---|---|---|---|
| `LINEAR_COEFFICIENT_CONTRIBUTION` | logistic / linear | global + local | LOG_ODDS / PREDICTION |
| `SHAP_TREE` | LightGBM classifier/regressor | global + local | raw LOG_ODDS / raw PREDICTION |
| `LIME_TABULAR` | logistic / linear / LightGBM | local only | positive-class PROBABILITY / PREDICTION |

`SHAP_TREE`はTreeExplainer + tree-path-dependent reference semanticsを用いる。globalはimmutable TEST explanation population上のmean absolute contribution、localはdeterministic sampleとする。

`LIME_TABULAR`はmodelが消費するpreprocessed feature space上のlocal explanationのみを提供する。TRAIN transformed featuresからdeterministic explanation referenceを構成し、global LIMEはunsupportedとして明示する。

Train / Explainability / Model Managementはcapability metadataを使用する。Unavailable advanced optionはhideせずreason付きでdisabled表示可能とし、Model Managementはread-onlyのままmodel/provider/version/effective parameters/seed/determinism/feature/preprocessor/artifact/Model Card/explanation/lineage provenanceを提示する。

No new persistent Model Registry aggregate or DB migration is required. Existing generic Execution / Result / Artifact lifecycle remains authority。
