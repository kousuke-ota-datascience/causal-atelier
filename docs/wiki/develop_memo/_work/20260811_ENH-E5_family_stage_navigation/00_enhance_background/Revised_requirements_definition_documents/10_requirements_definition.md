# 10 要件定義

- 文書状態: `PHASE_I_REVISED / NFR-019_PASS`
- 文書種別: 現行requirementsのeffective snapshot
- 上位文書: `00_product_concept_memo.md`
- 下位文書: `21_logical_data_design.md` / `22_product_basic_design.md` / `23_api_interface_design.md` / `30_detailed_design.md`

## 0. INTRODUCTION

### 0.1. プロダクトコンセプトから導かれる要件上の課題

Ariadneのプロダクトコンセプトを、次のとおり定義する。

> **Ariadneは、Research Topicに紐づくResearch Contextを共通の分析コンテキストとし、Dataset VersionおよびAnalysis Viewとの関係を保持しながら、探索・可視化、因果分析および予測分析を実行し、その条件、結果、判断理由および相互関係を追跡可能にする分析ワークスペースである。**

このプロダクトコンセプトに基づき、Ariadneでは、探索的分析、予測分析、因果分析という、目的・判断基準・成果物の意味が異なる分析活動を、一つのProjectの中で継続的に扱う必要がある。

これらの分析活動を適切に扱うため、ユーザーは少なくとも次の二つの情報を明確に把握できなければならない。

* **どのAnalysis Familyで分析しているか**
  探索、予測、因果のいずれの分析目的・分析観点に基づいて作業しているか。

* **そのAnalysis Familyの中で、現在どの分析作業を行っているか**
  データ確認、分析条件の定義、モデルまたは推定方法の構築、評価、診断、結果確認など、分析ワークフロー上の現在位置。

この二つが明確に区別されない場合、ユーザーは現在の分析目的と作業位置を把握しづらくなり、異なるAnalysis Familyに属する操作、結果および判断を混同する可能性がある。

特に、予測分析における予測性能や特徴量寄与と、因果分析における因果効果や識別結果は、意味および判断基準が異なる。したがって、異なるAnalysis FamilyのResultを同一の意味を持つ結果として扱ってはならない。

また、探索から予測分析または因果分析へ進む場合、あるいは複数の分析結果を比較、再利用または改訂する場合には、少なくとも次の情報を追跡できなければならない。

* Research TopicおよびResearch Context
* DatasetおよびDataset Version
* Analysis Viewその他の分析対象データの導出条件
* Analysis Specification
* ExecutionおよびExecution Plan
* ResultおよびArtifact
* 分析時の判断、AnnotationおよびWarning
* これらの間のLineage

これらの情報が失われた場合、分析結果の再現、比較、根拠確認、改訂、および後続分析への適切な引継ぎが困難になる。

したがってAriadneは、異なるAnalysis Familyの意味論を明確に分離しながら、一つのProject内で分析ワークフローを継続的に扱うことができ、各分析の問い、入力データ、分析条件、実行、結果、判断およびLineageを一貫して追跡可能な分析環境を提供しなければならない。

### 0.2. Legends

#### 0.2.1. Requirement levels

- `MUST`: acceptanceに必須。
- `MUST NOT`: 実装してはならない。
- `SHOULD`: 強い推奨。逸脱には明示理由が必要。
- `MAY`: 任意。必須acceptanceには含めない。

#### 0.2.2. Requirement lifecycle

各Requirementは、Requirementそのものの有効性、現在の実装状態、およびdelivery対象を独立した属性として管理する。

##### Requirement Status

Requirementがproduct requirementとして現在どの状態にあるかを表す。

| Value      | Meaning                                                          |
| ---------- | ---------------------------------------------------------------- |
| `ACTIVE`   | 現在有効なRequirement。現在実装済みか、将来実装予定かには依存しない。                         |
| `DEFERRED` | Requirementとしての必要性は維持するが、現在のdelivery対象からは除外され、将来の実装対象として延期されている。 |
| `RETIRED`  | Requirementとして廃止され、今後のproduct contractとして維持しない。                  |

##### Implementation Status

Requirementに対する現在の実装充足状態を表す。

| Value             | Meaning                                                   |
| ----------------- | --------------------------------------------------------- |
| `IMPLEMENTED`     | Requirementを満たす実装が現在存在し、current implementationとして確認されている。 |
| `PARTIAL`         | Requirementの一部は実装されているが、Requirement全体を満たしていない。            |
| `NOT_IMPLEMENTED` | Requirementを満たす実装が現在存在しない。                                |
| `UNVERIFIED`      | 実装有無またはRequirement充足状態を、利用可能なevidenceから確定できていない。          |

##### Delivery

Requirementをどのdelivery scopeで実現または維持するかを表す。

| Value      | Meaning                                                               |
| ---------- | --------------------------------------------------------------------- |
| `BASELINE` | ENH-E5開始時点のcurrent implementationに既に含まれており、ENH-E5では既存contractとして維持する。 |
| `ENH-E5`   | ENH-E5で実装または不足部分を完成させるdelivery対象。                                     |
| `FUTURE`   | ENH-E5では実装せず、将来のenhancementで取り扱うdelivery対象。                           |

これら三つの属性は独立した軸として扱う。

例えば、

* `ACTIVE / IMPLEMENTED / BASELINE` は、現在有効で既に実装済みのRequirementを表す。
* `ACTIVE / NOT_IMPLEMENTED / ENH-E5` は、現在有効でありENH-E5で新たに実装するRequirementを表す。
* `ACTIVE / PARTIAL / ENH-E5` は、現在一部のみ実装されておりENH-E5で不足部分を完成させるRequirementを表す。
* `DEFERRED / NOT_IMPLEMENTED / FUTURE` は、Requirementとしては維持するがENH-E5では実装しないRequirementを表す。
* `DEFERRED / PARTIAL / FUTURE` は、一部実装済みであるものの、残りの実装をENH-E5では行わず将来へ延期するRequirementを表す。

#### 0.2.3. 用語

- `Family`: Exploratory / Predictive / Causalのanalytical capability context。
- `Navigation Stage`: Family内でユーザーが選択するwork/view context。
- `Execution Stage`: ExecutionPlan / StageExecutionに属するruntime execution unit。
- `Stage`を単独で用いる場合、UI/application文脈ではNavigation Stageを指す。

## 1. 適用範囲

Ariadneは、Project / Research Topicを境界として、Research Context、Dataset Version、Exploratory / Predictive / Causalの三つのAnalysis Family、Execution、Result、Artifact、AnnotationおよびLineageを管理する。Analysis Familyはglobal analytical context、Navigation StageはFamily-local work/view contextとして扱う。

対象データは前処理可能な表形式データとし、予測分析の対象TaskはBinary ClassificationとRegressionとする。因果分析はGraph Discovery、Identification、Data Eligibility、ATE / ATT Estimation、Diagnostics、RefutationおよびSensitivityを対象とする。

## 2. Actor

| Actor | 責務 | 権限上の位置づけ |
| --- | --- | :--- |
| Analyst | Context、Data、Analysis Specification、Execution、比較、Annotationを作成・操作する | ProjectMembership roleに従う。WRITE / MUTATEおよびExecution mutationはOWNER / EDITOR |
| Reviewer / Viewer | Result、warning、diagnostics、Lineage、Annotationを確認する | ProjectMembership roleに従う。VIEWERを含むOWNER / EDITOR / VIEWERがread可能 |
| Infrastructure Operator | 実行基盤、保存領域、認証、監視等のinfrastructureを運用する | ProjectMembership roleではない運用persona。system-level authorization policyはDEFERRED / FUTURE |

## 3. 業務Capability

| Capability | 目的 | 正本Resource |
| --- | --- | --- |
| Project / Research Context | 分析の意味、問い、意思決定を固定する | Project、ResearchContextVersion |
| Data / Analysis View | 入力データと分析対象条件を固定する | DatasetVersion、AnalysisView |
| Exploratory Analysis | データ品質・分布・関係・比較を探索し、Finding候補を蓄積する | AnalysisSpecification(EXPLORATORY)、Result、Artifact、Annotation |
| Causal Analysis | 介入効果を仮定・識別・診断とともに評価する | AnalysisSpecification(CAUSAL)、GraphVersion、Result |
| Predictive Analysis | 将来targetの予測可能性とmodel挙動を評価する | AnalysisSpecification(PREDICTIVE)、Result、Artifact |
| Workflow | Planner、Plan、Stage、Runner、Executorを制御する | ExecutionPlan、Execution、StageExecution |
| Results / Lineage | 結果比較、判断、来歴、Exportを提供する | Result、Artifact、Annotation、LineageEdge |
| Analytical Navigation | Analysis FamilyとFamily-local Navigation Stageを独立したnavigation dimensionとして提示する | AnalysisFamily、Navigation metadata/state（non-persistent） |

### 3.1. Analytical Navigation frozen catalog

Navigation catalogのauthorityはFamily Capability descriptorをaggregateするbackend read-only metadata interfaceとする。

```text
GET /api/v1/navigation/analysis
schema: analysis-navigation/1
```

| Family | family_slug | default_stage_id | Navigation Stages |
| --- | --- | --- | --- |
| EXPLORATORY | `exploratory` | `profile` | `profile`, `data-quality`, `distribution`, `relationships`, `comparison`, `findings` |
| PREDICTIVE | `predictive` | `setup` | `setup`, `train`, `predict`, `metrics`, `explainability`, `model-management` |
| CAUSAL | `causal` | `setup` | `setup`, `discovery`, `identification`, `estimation`, `effects`, `diagnostics`, `sensitivity` |

Canonical analytical route:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}
```

Resource deep route:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}/resource/{resource_type}/{resource_id}
```

E5 resource typeは`analysis-specification / execution / result / graph-version`とする。Legacy analytical routeを残す場合は各Family default Stageへ一方向normalizeする。

`analysis-navigation/1`はpresentation/application metadata schemaであり、scientific generic `SchemaRegistry`へ登録しない。Frontendはfull catalogをduplicate ownershipしない。


## 4. E2Eシナリオ

| ID | シナリオ | 完了条件 |
| --- | --- | --- |
| E2E-01 | Research Workspaceを作成する | ProjectとResearch Contextを作成し、Dataset Versionを登録してProject-global surfaceと三つのAnalytical Familyへ遷移できる |
| E2E-02 | 探索・可視化を保存する | Datasetの品質・分布・関連を確認し、ChartとAnalysis Viewを保存できる |
| E2E-03 | 探索から分析draftを作る | 探索ResultからCausalまたはPredictive Specification draftを作成し、source relationを保持できる |
| E2E-04 | 因果効果を評価する | Graph、Question、Design、Identification、Eligibility、Estimation、Diagnostics、Refutation、Sensitivityを実行できる |
| E2E-05 | 分類モデルを評価する | Binary Classificationをsplit、train、evaluate、explainし、test isolationを確認できる |
| E2E-06 | 回帰モデルを評価する | Regressionをsplit、train、evaluate、error analysisし、複数modelを比較できる |
| E2E-07 | 条件変更を比較する | base ExecutionからRERUNまたはREVISEDを作成し、changed dimensionsと結果差分を確認できる |
| E2E-08 | 横断来歴を確認する | ReviewerがResearch ContextからExploratory、Causal、PredictiveのResultと判断理由へ遡れる |
| E2E-09 | Analysis Familyを横断する | Family tabでExploratory / Predictive / Causalを切り替え、selected FamilyのNavigation Stageだけを左navigationから選択できる |
| E2E-10 | UIを経由せずanalysisを実行する | CLI / Python library / backend use caseからCurrent Navigation Stageを指定せず既存analysis executionを開始できる |

### 4.1. E2E共通受入条件

- Command受付時にProject権限、Resource状態、SchemaおよびFamily固有validationが実行される
- すべてのExecutionがResearch Context Version、Dataset VersionまたはAnalysis Viewを固定する
- ResultとArtifactがExecution / Stageへ紐付く
- UI表示とAPI payloadが同じ保存済み正本を参照する
- 失敗時にtechnical failure、validation rejection、analytical negative resultを区別する
- Navigation Stageの存在・順序をruntime Execution Stageやworkflow completionへ読み替えない

## 5. 機能要件

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | Project / Context | ProjectをResearch Topicの権限・来歴境界として作成、更新、archiveできる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-002 | Project / Context | Projectはtopic、objective、memoを保持し、decision contextはversioned `ResearchContextVersion`の責務として保持する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-003 | Project / Context | Research Contextをversioned resourceとして作成し、過去Versionを上書きしない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-004 | Project / Context | Research Contextに複数のResearch QuestionとHypothesisを保持できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-005 | Project / Context | Context間にREFINES、DERIVED_FROM、SUPERSEDES、RELATED_TO relationを設定できる | SHOULD | ACTIVE | IMPLEMENTED | BASELINE |
| FR-006 | Project / Context | Analysis Specificationは一つのResearch Context Versionを参照する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-007 | Project / Context | Executionは参照ResearchContextVersionを固定し、受付時のobjective/rationale等の再現に必要なsnapshot metadata/hashを保持する。ResearchContext全体の重複保存を必須化しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-008 | Project / Context | ResearchContextVersionから利用AnalysisSpecification、Execution、Resultへcanonical lineage/read modelで遡及・追跡できる | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-009 | Project / Context | ARCHIVED Projectでは新規Executionを受け付けず、既存Resultを保持する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-010 | Data / View | CSVまたはParquetをDataset Versionとして不変登録する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-011 | Data / View | DatasetVersionにcontent hash、schema、row count、column countおよびcurrent profile summaryを保持する。登録時の独立full profile生成を必須化しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-012 | Data / View | Dataset previewとcolumn metadataを権限内で取得できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-013 | Data / View | 同一Dataset系列に複数Versionを登録し、Executionが参照Versionを固定する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-014 | Data / View | Analysis Viewにrow filter、column selection、derived column、missing policy、time cutoffを定義する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-015 | Data / View | AnalysisViewのsource Dataset logical type × operator × value compatibilityをdomain/application validationで検証し、type mismatchを`FILTER_TYPE_MISMATCH`として返す | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-016 | Data / View | 固定済みAnalysis Viewを上書きせず、変更時は新Versionを作成する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-017 | Data / View | Analysis Viewからsource Dataset Versionと生成条件へ遡れる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-018 | Data / View | 同じAnalysis Viewを複数Analysis Familyから参照できる | SHOULD | ACTIVE | IMPLEMENTED | BASELINE |
| FR-019 | Data / View | Dataset columnにグローバルなTreatment、Outcome、Target等の役割を固定しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-020 | Data / View | Explore stateのdata-selection semantics（row_filter、selected_columns、derived_columns、missing_value_policy、time_cutoff、sampling）からAnalysisView DRAFTを作成できる。presentation-only chart stateはAnalysisViewへ保存しない | SHOULD | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-021 | Data / View | 機微列、利用制限および説明をcolumn metadataへ付与し、configurable sensitive-column policyに利用できる | SHOULD | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| FR-022 | Data / View | Analysis View生成時に不正列、空母集団、非決定的式を拒否する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-023 | Explore | Dataset overview、schema、型、欠損率、cardinalityを表示する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-024 | Explore | 数値列・カテゴリ列の記述統計と分布を生成する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-025a | Explore | 列別missingnessを確認できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-025b | Explore | 複数列のjoint missing-pattern analysisを行える | MUST | DEFERRED | PARTIAL | FUTURE |
| FR-026a | Explore | current capabilityとして型に応じた二変量association / bivariate analysisを生成できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-026b | Explore | 散布図、箱ひげ、クロス集計等のfull exploratory bivariate visualization surfaceを提供する | MUST | DEFERRED | PARTIAL | FUTURE |
| FR-027 | Explore | group-by集計および時系列推移を生成できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-028 | Explore | correlation / association matrixを型に応じて生成できる | SHOULD | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| FR-029 | Explore | Chart Specificationを保存し、同じDataset Versionで再実行できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-030 | Explore | 探索実行のResultとArtifactを保存する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-031 | Explore | 保存した探索Resultに観察メモと限界をAnnotationできる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-032 | Explore | Exploratory Resultからcanonical Causal/Predictive `AnalysisSpecification`をDRAFTとしてpersistし、source Resultとの`MOTIVATED` relationを保持できる。auto FIX / auto executionは行わない | SHOULD | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-033 | Explore | 探索結果をEXPLORATORYと表示し、確認的結論として自動昇格しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-034 | Explore | Exploratory provenanceとしてdata-selection semantics、analysis-significant family_spec、sampling、Execution code/runtime metadataおよびResult/Artifact lineageを再構成できる | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-035 | Causal | 複数algorithm / parameterでcausal discoveryを実行できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-036 | Causal | User-definedまたはImported GraphをDiscoveryなしで登録できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-037 | Causal | DAG、CPDAG、PAGおよびendpoint semanticsを保持する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-038 | Causal | Graph Candidateの共通条件、変更条件およびedge差分を比較できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-039 | Causal | FIXED Graphからchild DRAFTを作成し、編集理由を記録して再固定できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-040 | Causal | Population、Treatment、Comparator、Outcome、Time、Estimand、Decision UseをCausal Questionに固定する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-041 | Causal | assignment、time zero、eligibility、strategy、adjustment set、assumptionsをCausal Designに固定する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-042 | Causal | Graph、Question、DesignからIdentification Resultを生成する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-043 | Causal | Identificationは全reasonを収集後、確定的不整合をreview statusより優先してstatus決定する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-044 | Causal | 型、欠測、post-treatment、sample size、overlapをData Eligibilityとして評価する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-045 | Causal | Treatment / Outcome inferred typeを正規化文字列で保存し、外部型objectを永続化しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-046 | Causal | Identification、Eligibility、Estimator互換性を満たす場合のみEstimationを受け付ける | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-047 | Causal | ATEまたはATTと区間推定を生成できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-048 | Causal | estimator/analysisに適用可能なoverlap、balance、weight、sample loss等のdiagnosticをResultとして保存する。全estimatorへ同一diagnostic setを強制しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-049 | Causal | Placebo TreatmentおよびData SubsetによるRefutationを実行できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-050 | Causal | Adjustment SetおよびPropensity ClippingのSensitivityを実行できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-051 | Causal | 同一immutable `dataset_version_id`の先行Exploratory Resultを用いたconfirmatory分析では`EXPLORATORY_REUSE_SAME_DATA` warningとevidence Result IDを保持する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-052 | Causal | 同一条件のRERUNと条件変更のREVISEDを区別し、changed dimensionsとreasonを保存する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-053 | Causal | 科学的負結果をExecution failureと区別する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-054 | Causal | Causal ResultからResearchContextVersion、AnalysisSpecification、ExecutionPlan、Execution、StageExecution、DatasetVersion/AnalysisView、GraphVersion、上流Result、Artifactへcanonical lineageで遡れる | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-055 | Predictive | 表形式Binary ClassificationとRegressionをPrediction Taskとして作成できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-056 | Predictive | Prediction unit、target、prediction time、horizon、intended use、deployment populationを固定する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-057 | Predictive | feature setと各featureのavailability cutoffを固定する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-058 | Predictive | random、stratified、group、time-based splitを選択できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-059 | Predictive | target leakage、future leakage、group leakage、split overlapをBackendで拒否する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-060 | Predictive | imputation、encoding、scaling等のfitをtraining partitionのみに限定する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-061 | Predictive | Algorithm Registryからtask対応modelを選択できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-062 | Predictive | validation partitionまたはcross-validationによるautomated hyperparameter selectionを提供する | SHOULD | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| FR-063 | Predictive | 固定済みspecとsplitからmodelをtrainingできる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-064 | Predictive | test partitionをmodel selectionに使用せず、最終評価まで隔離する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-065 | Predictive | classificationとregressionでtask対応metricを生成する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-066 | Predictive | classificationでclass balance、threshold、calibrationを確認できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-067 | Predictive | untouched TEST population上で指定subgroup columnごとのmetric、`sample_count`、計算可能な場合のbootstrap uncertaintyを確認できる | SHOULD | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-068 | Predictive | fitted model、fitted preprocessor、prediction等のdurable binary/tabular outputはArtifactとして、metric/error等の分析値はResult payloadとして保存する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-069 | Predictive | global / local Predictive Explanationを生成できる | SHOULD | ACTIVE | IMPLEMENTED | BASELINE |
| FR-070 | Predictive | Predictive Explanationを因果説明と区別して表示・exportする | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-071 | Predictive | intended use、training data、metric、limitationsをModel Cardへ記録する | SHOULD | ACTIVE | IMPLEMENTED | BASELINE |
| FR-072 | Predictive | Result比較はまずsemantic compatibilityを検証し、direct metric comparisonではさらに同一DatasetVersion、同一TEST-row identity/hash、同一定義metricを要求する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-073 | Predictive | Prediction Taskからsource Context、Dataset、Analysis Viewへ遡れる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-074 | Workflow | Analysis FamilyをEXPLORATORY、CAUSAL、PREDICTIVEとして識別する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-075 | Workflow | Family別PlannerをRegistryから解決する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-076 | Workflow | Plannerはversionedで不変なExecution Planを生成する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-077 | Workflow | Stage Typeをnamespace、name、versionで識別する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-078 | Workflow | PlanはStage dependencyとinput/output bindingをDAGとして保持する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-079 | Workflow | Stage RunnerをRegistryから解決し、Executorへif/elif分岐を集約しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-080 | Workflow | canonical lifecycle/application serviceがExecutionのclaim、state、cancel、retry、Result/Artifact metadata commitを所有し、Generic Executorはowned workflow context内で依存順、Stage sequencing、runner invocationを実行する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-081 | Workflow | Stage ExecutionとAttemptのstatus、開始・終了時刻、errorを保持する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-082 | Workflow | idempotency対象Commandでは`(project_id, command_scope, idempotency_key)`をauthorityとし、同一semantic requestをreplay、異なるrequestを`IDEMPOTENCY_CONFLICT`で拒否する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-083 | Workflow | 技術retryは同一Execution、条件変更は新Executionとする | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-084 | Workflow | 上流Artifactを下流Stage inputへ型付きでbindingする | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-085 | Workflow | 未登録Runner、cycle、missing output、schema mismatchをPlan受付時に拒否する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-086a | Workflow | stochastic Stageのactual effective random seedを`StageAttempt.effective_random_seed`へ保存し、同一logical Stageのretryで同じseedを再利用する | SHOULD | ACTIVE | PARTIAL | ENH-E5 |
| FR-086b | Workflow | Stageごとのtimeout / operational resource limitをpersistent/configurable policyとして保持する | SHOULD | DEFERRED | PARTIAL | FUTURE |
| FR-087a | Workflow | Execution snapshotにcurrent code/runtime/schema再現性metadataを保持する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-087b | Workflow | Execution `runtime_version_json`にAriadne code、Python、platform、machineおよび実際に利用したscientific library versionを保持する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-088 | Workflow | Execution StatusとResult analytical statusを分離する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-089 | Workflow | Generic validationとFamily-specific validationを分離して実行する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-090 | Result / Lineage | canonical Resultはexecution/stage relation、result type、scientific status、summary/payload/diagnostics/warningsを保持する。family/generic schema_versionをResult direct fieldへ重複保持しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-091 | Result / Lineage | Result payloadはFamily・Type別Schemaで検証する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-092 | Result / Lineage | canonical Artifactはproject/execution/stage/result relation、artifact type/scope、object_key、media type、hash、size、metadataを保持する。family/generic schema_versionをdirect fieldへ重複保持しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-093 | Result / Lineage | 同一または明示的に互換なResult Typeのみ定量比較する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-094 | Result / Lineage | Project単位でExplore、Causal、Predictiveのsummaryを横断表示する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-095 | Result / Lineage | ResultからResearchContextVersion、AnalysisSpecification、ExecutionPlan、Execution、StageExecution、DatasetVersion、AnalysisView、GraphVersion、input Result、base Execution、Artifactへ遡れるcanonical lineage read modelを提供する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-096 | Result / Lineage | 探索Resultから分析draft等のcross-analysis relationを明示保存する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-097 | Result / Lineage | Result、Graph、Analysis SpecificationまたはProjectへAnnotationできる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-098 | Result / Lineage | 採用判断、仮定、適用範囲、限界、次ActionをAnnotationへ記録できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-099 | Result / Lineage | Manifest、Result summary、Specification、Artifact参照をexportできる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-100 | Result / Lineage | 保存済みResultを上書きせず、訂正は新ResultまたはAnnotationで行う | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-101 | Result / Lineage | 改訂Executionとbase ExecutionのedgeをLineage表示する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-102 | Result / Lineage | AUC等とATE等を単一Scoreへ正規化しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-103 | Result / Lineage | Viewerがread-onlyで全来歴を確認できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-104 | UI | Project WorkspaceはProject-global surfaceとAnalytical Family navigationを別navigation dimensionとして提供する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-105 | UI | route-backed navigationは独立URL、deep link、reload、browser back / forwardに対応する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-106 | UI | 選択中Project、Context Version、Dataset Version、Analysis Viewを常時確認できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-107 | UI | 操作可否をBackend authoritative state/authorizationから導出し、`allowed / reason_code / message`としてpresentationへ返す | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-108 | UI | AnalysisSpecification、Execution、Result、GraphVersionへFamily/Navigation Stage contextを保持したdeep routeで直接遷移できる | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-109 | UI | 非同期presentation stateを`IDLE / LOADING / READY / EMPTY / PARTIAL / ERROR / CANCELLED`として区別する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-110a | UI | current result/list surfaceでfamily/type/status等の既存filterを提供する | SHOULD | ACTIVE | IMPLEMENTED | BASELINE |
| FR-110b | UI | 一覧・比較filterをdataset、context、date等へ拡張する | SHOULD | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| FR-111 | UI | ENH-E5変更surfaceでkeyboard、deterministic focus、accessible name、error association、non-color semanticsおよびcontrast要件を満たす | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-112 | UI | Exploratory、Predictive、Causalの用語と警告を明示的に分離する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-113 | API / CLI | HTTP APIをversioned pathとversioned payloadで提供する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-114a | API / CLI | Idempotency要否をHTTP method/create一般ではなく、retryでduplicate durable side effectを生成し得るCommandかどうかで判定する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-114b | API / CLI | 対象Commandで`Idempotency-Key`を必須化し、missing keyを`IDEMPOTENCY_KEY_REQUIRED`、same key/different requestをHTTP 409 `IDEMPOTENCY_CONFLICT`として扱う | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-115 | API / CLI | validation、conflict、not found、forbidden、execution failureをcanonical errorで返す | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-116 | API / CLI | 既存Executionから再実行用prefillを取得できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-117 | API / CLI | ExportをAPIとUIから同一contractで生成する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-118 | API / CLI | generic Product CLIからFamily別Specificationをsubmitし、Product Execution status/resultを取得できる | SHOULD | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| FR-119 | API / CLI | 履歴を持たないCLIは探索後警告等を独自推測しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-120a | API / CLI | runtime API schemaから生成されるFastAPI OpenAPIをcurrent API contractとして提供する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-120b | API / CLI | canonical schema exampleとOpenAPI/exampleをsystematically同期・検証する | MUST | DEFERRED | PARTIAL | FUTURE |
| FR-121 | Security / Ops | 全project-scoped routeでpersisted ProjectMembership role（OWNER/EDITOR/VIEWER）に基づくauthorizationをservice action前に検証する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-122 | Security / Ops | 作成、更新、archive、execution、cancel、retry、export等をgeneral operational audit trailへ記録する | MUST | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| FR-123a | Security / Ops | Project authorizationに基づきexplicit sensitive outputをOWNER/EDITORへ制限し、VIEWERにはaggregate/suppressed viewのみ許可する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-123b | Security / Ops | sensitive-column metadata等に基づくconfigurable exposure/minimization policyを提供する | MUST | DEFERRED | PARTIAL | FUTURE |
| FR-124a | Security / Ops | Artifact metadata/downloadでProject境界とsafe content dispositionを検証するcurrent contractを維持する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-124b | Security / Ops | legacy/generic routeを含むArtifact downloadでProjectMembership authorizationを一貫適用する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-125 | Security / Ops | Project archive後も監査・Lineageを保持する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-126 | Security / Ops | Metadata、Artifact、logのconfigurable retention/deletion policyを提供する | SHOULD | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| FR-127a | Security / Ops | current basic health endpointを提供する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-127b | Security / Ops | API、DB、Worker、ArtifactStoreのcomponent readinessを提供する | MUST | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| FR-128a | Security / Ops | Algorithm/Runnerをregistry/capabilityから解決・管理するcurrent contractを維持する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-128b | Security / Ops | size limit、timeout等のoperational resource configurationを一元管理する | MUST | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| FR-129 | Navigation | Exploratory / Predictive / Causalをfirst-classなAnalysis Familyとして常時選択可能にする | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-130 | Navigation | Current Familyをactive stateとcanonical route `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`の双方で一意に識別できる | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-131 | Navigation | Family-local navigationにはselected Familyが所有するNavigation Stageだけを表示する | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-132 | Navigation | Family切替時はCapability descriptorが宣言するdefault Navigation Stage（Exploratory=`profile`, Causal=`setup`, Predictive=`setup`）へ遷移する | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-133 | Navigation | FamilyごとにCapability-owned immutable descriptorでStage ID、slug、label、order、default Stageを独立定義する | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-134 | Navigation | Family間でStage数・名称を揃える目的のdummy/common Stageを導入しない | MUST NOT | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-135 | Navigation | Navigation Stageの表示順をwizard completion、runtime dependency、実行前提として強制しない | MUST NOT | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-136 | Navigation | canonical URL `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`からProject、Family、Navigation Stageを復元できる | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-137 | Navigation | reload、browser back、browser forwardでFamily / Stage stateをdeterministicに復元できる | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-138 | Navigation | unknown Family / Stageをsilent fallbackで意味変換せず明示errorと有効な遷移先を提示する | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-139 | Navigation | Project Management、Research Context、Data、Results / Lineage等をAnalytical Familyと同一taxonomyへ混在させない | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-140 | Navigation / Runtime | Navigation Stageをruntime `StageType` / `StageDefinition` / `StageExecution`として再利用・継承しない | MUST NOT | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-141 | Navigation / Runtime | Navigation StageとExecution Stageの1:1 mappingを要求するcontractを導入しない | MUST NOT | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-142 | API / CLI | CLI / Python library / backend use case / runtime executorはCurrent Navigation Stageを指定せずanalysis executionを開始できる | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-143 | Workflow | runtime layerはNavigation Stage ID、browser route、tab/sidebar stateへ依存しない | MUST NOT | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-144 | Capability | concrete Navigation Stage catalogは各Family-specific Capabilityが所有し、application/interface aggregatorがread-only metadataとして集約する | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-145 | Capability | generic application layerはFamily-specific Stage semanticsを集中所有しない | MUST NOT | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-146 | Exploratory | Exploratoryは`profile / data-quality / distribution / relationships / comparison / findings`をFamily-local Navigation Stageとして提供する | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-147 | Exploratory | Visualizationは各分析Stageの表現手段とし、独立Navigation Stageを設けない | MUST NOT | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-148 | Exploratory | Findingsは既存Result / Annotation / Lineageを利用可能とし、新規persistent Finding resourceを必須化しない | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-149 | Predictive | Predictiveは`setup / train / predict / metrics / explainability / model-management`をFamily-local Navigation Stageとして提供する | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-150 | Predictive | 既存Predictive UIの設定項目、validation、generated `predictive-analysis-spec/1` semanticsを全量保持する | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-151 | Predictive | MetricsとExplainabilityを異なる目的のNavigation Stageとして扱い、Predict Stage導入を理由に新規standalone scoring engineを必須化しない | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-152 | Predictive | Model Managementは現行scopeではfitted model、model card、artifact、lineageのread-oriented確認を中心とする | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-153 | Causal | Causalは`setup / discovery / identification / estimation / effects / diagnostics / sensitivity`をFamily-local Navigation Stageとして提供する | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-154 | Causal | IdentificationとEstimationを別Navigation Stageとして扱い、識別可能性と有限標本推定を混同しない | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-155 | Causal | EstimationとEffectsを別Navigation Stageとして扱い、推定設定と推定結果の閲覧・利用を混同しない | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-156 | Causal | DiagnosticsとSensitivityを別Navigation Stageとして扱う | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-157 | Domain / Compatibility | 既存`AnalysisSpecification.analysis_family`をFamily discriminatorとして再利用し、duplicate Family field/enumを追加しない | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-158 | Domain / Compatibility | AnalysisSpecification / ExecutionPlan / Execution / StageExecutionへNavigation Stage fieldを追加しない | MUST NOT | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-159 | Compatibility | legacy `/explore` / `/causal` / `/predictive` routeを各Family default Stageのcanonical routeへ一方向normalizeする | MUST | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-160 | Compatibility | Family/Navigation導入それ自体を理由にDB schema migrationまたはnavigation-state persistenceを導入しない。ENH-E5の再現性metadata migrationは別Requirementとして扱う | MUST NOT | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-161 | Scope | LightGBM / DoWhy / EconML等のexternal analytical engineを必須dependencyとして追加しない | MUST NOT | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| FR-162 | Scope | Overview / FlagshipをAnalytical Family peerとして追加しない | MUST NOT | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |

## 6. 非機能要件

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| NFR-001a | 再現性 | current snapshot、code/runtime metadata、seed、schema identity等の再現性情報を保持する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-001b | 再現性 | actual scientific library versionとStageAttempt effective seedを含むenvironment再構築metadataを保持する | — | ACTIVE | PARTIAL | ENH-E5 |
| NFR-002 | 追跡可能性 | canonical lineage read modelでResearchContextVersion→AnalysisSpecification→ExecutionPlan→Execution→StageExecution→Result→Artifactを追跡し、DatasetVersion/AnalysisView/GraphVersion/input Result/base Executionも接続する | — | ACTIVE | PARTIAL | ENH-E5 |
| NFR-003 | 決定性 | Canonical JSONとhash生成はfield順やprocessに依存しない | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-004 | 応答性能 | 通常一覧・詳細APIの95 percentile 2秒等のgeneral performance SLOとregression gateを定義する | — | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| NFR-005 | 拡張性 | 新Analysis Familyを既存Executor変更なしにRegistry追加できる | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-006a | 信頼性 | current claim/lease/retry mechanicsでExecution/Stage lifecycleを安全に再試行できる | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-006b | 信頼性 | retry/restartでsuccessful Stage outputのduplicate durable Artifact materializationを防止する。exactly-once executionは保証しない | — | ACTIVE | PARTIAL | ENH-E5 |
| NFR-007 | 整合性 | Metadata transactionとArtifact writeのcross-store failure compensationを定義する | — | DEFERRED | PARTIAL | FUTURE |
| NFR-008a | 安全性 | current input validation、path traversal防止、secret非露出等のsafeguardを維持する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-008b | 安全性 | 全project-scoped routeへProjectMembership authorizationを一貫適用する | — | ACTIVE | PARTIAL | ENH-E5 |
| NFR-008c | 安全性 | production-grade authentication/security hardeningを完成させる | — | DEFERRED | PARTIAL | FUTURE |
| NFR-009a | Privacy | current sensitive Result suppressionを維持する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-009b | Privacy | prediction/local explanation/exportのconfigurable minimization policyを提供する | — | DEFERRED | PARTIAL | FUTURE |
| NFR-010a | 可用性 | API processとWorker processを分離するcurrent deployment boundaryを維持する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-010b | 可用性 | Worker restart後の明示的resume/recovery semanticsを定義する | — | DEFERRED | PARTIAL | FUTURE |
| NFR-011a | 観測性 | current request/execution/stage correlation identifiersをlogへ出力する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-011b | 観測性 | comprehensive structured logging、metrics、operational telemetryを提供する | — | DEFERRED | PARTIAL | FUTURE |
| NFR-012 | Accessibility | ENH-E5変更surfaceの主要操作をkeyboardで実行でき、focus/name/error/non-color/contrast semanticsを満たす | — | ACTIVE | PARTIAL | ENH-E5 |
| NFR-013 | Schema evolution | schema versionはversioned Spec/Plan/payload/descriptor等のcontract boundaryで識別し、全persistent Result/Artifact entityへgeneric schema_version fieldを要求しない | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-014 | 互換性 | `causal-analysis-spec/2`の正規contractおよび保存済みCausal Resultをschema versionに従って読取可能に保つ | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-015 | Testability | Domain、Planner、Runner、API、Worker、UI、scientific benchmarkを分離testできる | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-016 | Scientific transparency | 仮定、warning、negative result、limitationを省略せず表示する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-017 | Resource control | upload size、row/column count、memory、timeout等にexplicit operational hard limitを定義する | — | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| NFR-018 | Dependency direction | Product DomainからWeb Framework、ORMおよびlegacy packageへ依存しない | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-019 | Documentation | `10/21/22/23/30`だけでcurrent implementation contractとENH-E5 target contractを自己完結して理解できる | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-020a | 移植性 | Artifact storageを`ArtifactStore` Port abstraction越しに利用する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-020b | 移植性 | Local filesystemに加えobject storage adapterを提供し、Port越しに切替可能にする | — | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| NFR-021 | Navigation separation | Navigation concernの変更がruntime execution lifecycleへ不要に伝播しない | — | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| NFR-022 | Navigation determinism | 同一Project / Family / Stage routeは同一navigation stateへdeterministicに復元される | — | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| NFR-023 | Maintainability | Family-specific Navigation Stage catalogをCapability ownershipで局所化する | — | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| NFR-024 | Testability | Navigation descriptor、route、renderer binding、runtime independenceをunit/integration/E2Eで分離検証できる | — | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| NFR-025 | Portability | CLI / library executionがWeb UI route、tab/sidebar state、NavigationStageDescriptorへ依存しない | — | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| NFR-026 | Accessibility | Current Family / Stageを色だけでなくsemantic active state、label、focus等でも識別できる | — | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| NFR-027 | Performance | navigation metadata取得・renderingがanalysis executionのcritical pathへ不要なI/Oまたはblocking dependencyを追加しない | — | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |

## 7. 科学・統計・分析上の要件

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| AR-001 | Scientific Integrity | 探索的可視化は仮説生成であり、因果結論または確認的検定へ自動変換しない | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-002 | Scientific Integrity | 予測性能は因果効果を示さない | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-003 | Scientific Integrity | Predictive Explanationはmodel behaviorの説明でありcausal explanationではない | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-004 | Scientific Integrity | 同一immutable `dataset_version_id`を探索とconfirmatory analysisで再利用した場合、`EXPLORATORY_REUSE_SAME_DATA` warningとlineage evidenceを保持する | — | ACTIVE | PARTIAL | ENH-E5 |
| AR-005 | Scientific Integrity | 因果推定はIdentification ResultとData Eligibility Resultを参照してgateする | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-006 | Scientific Integrity | Identification statusは全reasonを収集後に決定する | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-007 | Scientific Integrity | Collider判定はback-door path上のcolliderまたはその子孫を対象とする | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-008 | Scientific Integrity | Eligibilityの型はBINARY、CONTINUOUS、UNSUPPORTED等の正規値で保存する | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-009 | Scientific Integrity | 外部libraryのdtype objectまたはmodel objectをJSON正本へ保存しない | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-010 | Scientific Integrity | Estimation前提不成立時は数値を無理に返さず分析状態を保存する | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-011 | Scientific Integrity | Predictive preprocessingはtrain partitionのみでfitする | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-012 | Scientific Integrity | test partitionをfeature selection、model selection、threshold selectionに利用しない | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-013 | Scientific Integrity | 時系列Taskは未来観測がtrain featureへ混入しないsplitを使用する | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-014 | Scientific Integrity | 同一entityがtrainとtestへ跨る場合はgroup leakageを検査する | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-015 | Scientific Integrity | classification metricはclass imbalance、threshold、calibrationと併記する | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-016 | Scientific Integrity | subgroup metricは`sample_count`を必須とし、0.95 percentile bootstrap（1000 resamples、deterministic seed）で計算可能な場合にuncertaintyを併記し、計算不能値を捏造しない | — | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| AR-017 | Scientific Integrity | Result比較はsemantic compatibilityとdirect metric comparabilityを分離して判定する | — | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| AR-018 | Scientific Integrity | AUC、RMSE、ATE等を単一の優劣scoreへ変換しない | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-019 | Scientific Integrity | random seedだけでなくsplit indexまたはpartition artifactを保存する | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-020 | Scientific Integrity | prediction row / local explanationをpotentially sensitive outputとして扱い、Project roleに応じてdetail exposureを制御する | — | ACTIVE | PARTIAL | ENH-E5 |
| AR-021 | Scientific Integrity | Navigation Stageの表示順を分析上必須の実行順序として解釈しない | — | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| AR-022 | Scientific Integrity | Family間でStage数・名称を揃えることを科学的workflow要件としない | — | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| AR-023 | Scientific Integrity | Causal Identificationでは観測データと仮定からestimandが識別可能かをEstimationと分離して扱う | — | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| AR-024 | Scientific Integrity | Causal Effectsは推定されたeffectの閲覧・利用を扱い、estimator configurationと混在させない | — | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| AR-025 | Scientific Integrity | Predictive MetricsとPredictive Explainabilityを別目的として扱い、feature importance等をcausal effectへ読み替えない | — | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| AR-026 | Scientific Integrity | Exploratory Findings / visualizationをcausal conclusionまたはconfirmatory resultへ自動昇格しない | — | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |



### 7.0.1. Predictive subgroup uncertainty contract

指定subgroup columnはuntouched TEST populationを各column独立にsliceする。automatic intersection/discovery/fairness frameworkはENH-E5 scope外。各recordは`sample_count`を必須とし、uncertaintyはnonparametric percentile bootstrap（confidence=0.95, resamples=1000, deterministic seed）とする。`n < 2`またはvalid resamples < 200ではCIを返さずwarningを返す。metricを計算できない場合はvalue/uncertaintyを`null`とし、値を捏造しない。

### 7.0.2. Scientific comparability contract

Comparisonは次の二段階で判定する。

1. `semantic_compatible`
2. `direct_metric_comparable`

Predictive semantic keyは`task_type / prediction target(outcome) / prediction unit / prediction time / horizon / deployment/evaluation population semantics`。Direct metric comparisonではさらに`same dataset_version_id / same TEST-row identity(hash) / same metric definition`を要求する。

Causal semantic keyは`treatment(exposure) / outcome / estimand / target population`。Direct comparisonではsame data/view/analysis populationも要求する。

semantic mismatchは比較request自体のtechnical failureにせず、compatible=falseとreasonを返し、quantitative delta/rankingを生成しない。AUC/RMSE/ATE等を単一scoreへ正規化しない。


## 7.1. Project Authorization / Sensitive Output Boundary

Persisted Project roleは次の3値のみとする。

- `OWNER`
- `EDITOR`
- `VIEWER`

| Action | OWNER | EDITOR | VIEWER |
| --- | --- | --- | --- |
| Project READ | allow | allow | allow |
| WRITE / MUTATE | allow | allow | deny |
| Execution submit/cancel/retry/rerun/revise | allow | allow | deny |
| Export create | allow | allow | deny |
| Membership administration | allow | deny | deny |
| Explicit sensitive output | allow | allow | deny |

独立`EXECUTE` roleは追加しない。prediction row / local explanationはpotentially sensitive outputとして扱う。configurable sensitive-column governanceはD3/FUTUREでありENH-E5 acceptanceへ含めない。



## 7.2. Canonical Lineage / Reproducibility / Retry Safety

Canonical lineage read modelは最低限次を接続する。

```text
ResearchContextVersion
  ↓
AnalysisSpecification
  ↓
ExecutionPlan
  ↓
Execution
  ↓
StageExecution
  ↓
Result
  ↓
Artifact
```

加えて`DatasetVersion / AnalysisView / GraphVersion / input Result / base Execution`を接続する。FK/snapshotからdeterministically導出できるstructural relationをgeneric `LineageEdge`へ重複persistしない。`MOTIVATED`等のsemantic relationだけをgeneric LineageEdgeで保持する。

ENH-E5では`StageAttempt.effective_random_seed: int | null`を追加し、stochastic Stageのactual seedをattempt単位で保存する。同一logical Stageのretryは同じseedを再利用し、deterministic Stageは`null`とする。

`runtime_version_json`は最低限`ariadne_code_version / python_version / platform_system / platform_release / machine / libraries`を保持する。これはbit-for-bit numerical identity保証ではなくenvironment再構築情報である。

Idempotencyはduplicate durable side effectを生成し得るCommandに適用し、scopeを`(project_id, command_scope, idempotency_key)`とする。exactly-once executionは保証しないが、retryで同一successful Stage outputのdurable Artifactを重複materializeしてはならない。


## 8. 状態要件

Ariadneのpersistent Resource、Execution lifecycleおよびNavigation stateは、それぞれ独立した状態体系として扱う。異なる状態体系を相互に読み替えない。

### 8.1. Project

Projectは次の状態遷移に従う。

```text
ACTIVE -> ARCHIVED
```

ARCHIVEDからACTIVEへの復元は、管理操作として別途定義するまで対象外とする。

### 8.2. Versioned Resource

DRAFT / FIXED lifecycleを持つVersioned Resourceは、次の状態遷移に従う。

```text
DRAFT -> FIXED
```

FIXED Resourceは上書きしない。変更時は新Versionまたはchild DRAFTを作成する。

### 8.3. Execution

Executionは次の状態遷移に従う。

```text
QUEUED -> RUNNING -> SUCCEEDED
                  -> FAILED -> QUEUED
QUEUED / RUNNING -> CANCELLED
```

`FAILED -> QUEUED`はtechnical retryによる再実行を表す。分析条件を変更する場合は同一Executionのretryではなく、新しいExecutionとして扱う。

### 8.4. Stage Execution

StageExecutionは次の状態遷移に従う。

```text
PENDING -> READY
READY -> RUNNING
RUNNING -> SUCCEEDED
RUNNING -> FAILED
FAILED -> PENDING
FAILED -> RUNNING
PENDING / READY -> SKIPPED_DUE_TO_PREREQUISITE
PENDING / READY / RUNNING -> CANCELLED
```

`FAILED -> PENDING`はretry準備、`FAILED -> RUNNING`はretry attempt開始時の遷移を表す。

StageExecutionの状態はruntime Execution Stageの実行状態であり、Navigation Stageの状態または完了状態として扱わない。

### 8.5. Analytical Status

Resultのanalytical statusはResult Typeごとに許可値を定義する。

ExecutionおよびStageExecutionのruntime statusと、Resultのanalytical statusを混在させない。technical failure、validation rejectionおよびanalytical negative resultは区別して扱う。

### 8.6. Navigation State

現在の分析navigation contextは、次の組合せとして扱う。

```text
Project
+ Current Family
+ Current Navigation Stage
```

* Current FamilyおよびCurrent Navigation StageはURL / application navigation stateをauthorityとする。
* Navigation stateをDBへworkspace preferenceとして永続化しない。
* Family切替時のlast-stage memoryを必須化しない。
* Navigation stateをAnalysisSpecification、ExecutionPlan、ExecutionまたはStageExecutionへ保存しない。
* Navigation Stageの状態をExecutionまたはStageExecutionのruntime statusへ読み替えない。

## 9. 権限要件

Project-scoped Resourceおよび操作の認可は、§7.1で定義するpersisted Project role `OWNER / EDITOR / VIEWER`をauthorityとする。

* Project-scoped Resourceへアクセスするには、対象Projectに対するmembershipと必要なProject権限を持たなければならない。
* `OWNER / EDITOR / VIEWER`はProjectをreadできる。
* Context、Analysis View、Analysis Specification、Annotationその他のProject ResourceのWRITE / MUTATEは`OWNER / EDITOR`のみ許可する。
* Executionのsubmit / cancel / retry / rerun / reviseは`OWNER / EDITOR`のみ許可する。
* Exportの作成は`OWNER / EDITOR`のみ許可する。
* Project membershipの管理は`OWNER`のみ許可する。
* prediction row / local explanation等のexplicit sensitive outputは`OWNER / EDITOR`のみ取得可能とし、`VIEWER`には返さない。
* 独立した`EXECUTE` Project roleは設けない。
* 認可失敗時は、権限を持たない利用者がResourceの存在を推測できない応答を選択できる。
* system-level Operator authorizationはENH-E5のProject authorization contractには含めず、`DEFERRED / FUTURE`として扱う。

## 10. データ保持要件とDeferred Audit / Retention Boundary

ENH-E5で有効なcurrent data-retention contractは次のとおりとする。

* Dataset Version、Result、Artifact metadataおよびExecution snapshotはappend-onlyを基本とする。
* Projectをarchiveしても、Projectに属する既存の分析Resourceをarchive操作だけを理由として物理削除しない。
* Annotationについて、current contractで保持されている変更履歴を維持する。

以下はRequirementとして維持するが、ENH-E5のdelivery対象には含めない。

* general operational audit trail (`FR-122`): `DEFERRED / FUTURE`
* configurable retention/deletion policy (`FR-126`): `DEFERRED / FUTURE`

したがってENH-E5では、general Audit recordの共通field contract、configurable retention期間、Artifactの一般的な物理削除policyおよび削除audit contractを必須acceptanceとして要求しない。

## 11. 対象外要件

- Multi-class classification
- survival analysis、forecasting、ranking、recommendation
- online inference endpoint
- model deployment / registry / monitoring
- arbitrary Python execution
- arbitrary SQL query
- dashboard layout editor
- causal effectの自動保証
- unbounded AutoML
- automatic business decision
- LightGBM / DoWhy / EconML等のexternal analytical engine追加
- Navigation stateのDB persistence / last-stage memory
- Overview / FlagshipをAnalytical Family peerとして追加すること
- 新規persistent Findings / Evidence domain modelの必須化

## 12. 総合完了条件

1. E2E-01〜E2E-10がWeb API、Worker、Persistence、FrontendおよびCLI/library境界を通して成立する。
2. FR / NFR / ARの各Requirementについて、Requirement Status、Implementation StatusおよびDeliveryが正本文書上で一意に定義されている。
3. `Requirement Status = ACTIVE`かつ`Delivery = BASELINE`のRequirementについて、ENH-E5変更によって既存contractが破壊されていないことを、必要なregression testまたはreview evidenceで確認する。
4. `Requirement Status = ACTIVE`かつ`Delivery = ENH-E5`のRequirementについて、Requirement Levelおよび設計上のverification contractに応じたtest、benchmarkまたはreview evidenceが存在する。
5. `Requirement Status = DEFERRED`または`Delivery = FUTURE`のRequirementは、ENH-E5のmandatory acceptanceおよび必須test targetへ含めない。
6. ACTIVEなScientific Integrity Requirementについて、必要な自動test、scientific benchmarkまたはreview checklistによるverification evidenceが存在する。
7. `causal-analysis-spec/2`および`predictive-analysis-spec/1`の既存正規contractを読取り、既存scientific/regression testが通る。
8. `AnalysisSpecification.analysis_family`を再利用し、duplicate Family discriminatorを追加していない。
9. AnalysisSpecification / ExecutionPlan / Execution / StageExecutionへNavigation Stage fieldを追加していない。
10. CLI / Python library / backend use case / runtime executorがCurrent Navigation Stageなしで既存analysisを実行できる。
11. Product Domain / runtime execution layerからbrowser route / Navigation Stageへの新規逆依存がない。
12. Predictive既存設定項目およびgenerated specification semanticsが保持される。
13. 正本文書、OpenAPI、DB schema、Frontend文言およびtestが同じFamily / Navigation Stage / Execution Stage用語とcontractを使用する。

## 13. CHANGE LOG

### 13.4. ENH-E4 Canonical Execution Architecture Requirements

- canonical Execution lifecycle / StageExecution / Result / Artifact / Lineage authorityをrequirementsへ統合した。
- Family-specific Analysis Specificationとgeneric workflow coreの境界を明確化した。
- FR-001〜FR-128、NFR-001〜NFR-020、AR-001〜AR-020を現行requirements baselineとして継承する。

### 13.5. ENH-E5 Family × Navigation Stage Application Architecture Requirements

- FR-104 / FR-105をProject Workspaceの新navigation architectureに合わせて改定した。
- FR-129〜FR-162を追加し、Family / Navigation Stage、Capability ownership、Navigation / Runtime separation、Family-specific Stage set、互換性とscope境界を定義した。
- NFR-021〜NFR-027、AR-021〜AR-026、Navigation State要件を追加した。
- 既存`AnalysisSpecification.analysis_family`を再利用し、Navigation Stageをpersistent analysis/runtime modelへ追加しないことを明示した。

### 13.6. ENH-E5 Phase I Canonical Convergence

- D1/D2/D3をRequirement lifecycle（Status / Implementation Status / Delivery）へ反映した。
- Phase Gの11 D2 freeze packageをRequirement本文へ具体化した。
- D3を削除せず`DEFERRED / FUTURE`として保持した。
- Navigation endpoint/schema/catalog/default Stage/routeをfrozen contractへ収束した。
