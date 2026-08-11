# ENH-E5 既存実装・設計整合性レビュー

- 状態: `COMPLETED_FOR_DRAFT`
- 対象branch: `feature/ariadne_mvp_e5`
- Planning baseline SHA: `46122c68333df03680b97c253a7b5d32bf9393e7`
- 目的: ENH-E5で**変更しない**とする既存contractをcurrent sourceと突合し、Revised 21/22/23/30に旧資料由来・推測・架空contractが混入していないか確認する。

## 1. Review rule

本レビューでは次を区別する。

1. **Current implementation fact**: Planning baseline sourceに実在する型、field、route、state、planner、repository contract。
2. **ENH-E5 target design**: Family / Navigation Stage、route、navigation metadata等、今回追加・変更する設計。
3. **Deferred decision**: Architecture Review / Human approval前でfreezeしていないtarget値。

ENH-E5で変更しない領域について、current implementation factとRevised designが異なる場合は**設計側をcurrent implementationへ合わせる**。一方、ENH-E5 target designを「現在実装されていない」という理由だけで削除しない。

## 2. Alignment result

結論: **乖離を検出し、Revised 21/22/23/30を修正した。**

主な乖離は、ENH-E4由来の概念をcurrent implementationへ再照合せず継承したこと、既存contractを要約する過程で存在しないfield/API/moduleを補完してしまったことに起因していた。

## 3. Corrected discrepancies

| Area | 修正前の乖離 | Planning baselineの実装fact | 修正 |
| --- | --- | --- | --- |
| `AnalysisFamily` | Family discriminatorの追加余地があるように読めた | `AnalysisFamily={EXPLORATORY, CAUSAL, PREDICTIVE}`が存在し、`AnalysisSpecification.analysis_family`が既に保持する | duplicate Family discriminator禁止を21/23/30へ明示 |
| `Execution` | `execution_plan_id`をcanonical Execution fieldのように扱う箇所があった | canonical `Execution`に独立`execution_plan_id` columnはない | 21/23/30からcanonical field扱いを除去。current workflowで必要なplan identityはsubmission metadataと区別 |
| `StageExecution` | `attempt_count`のような集約fieldを想定していた | retry attemptは`StageAttempt` append-only row。`StageExecution`とは別entity | 21/30を`StageExecution + StageAttempt`構造へ修正 |
| `Result` | `project_id / analysis_family / schema_version`をcanonical Result fieldのように扱った | canonical Resultは`execution_id / result_level / stage_execution_id / result_type / scientific_status / summary_json / payload_json / diagnostics_json / warning_json / created_at` | 親ExecutionからProject/Familyを解決する設計へ修正 |
| Result status matrix | Predictive/Exploratoryにcurrent enumにないstatusを含めていた | SPLIT=`PASS`; TRAINING=`TRAINED/TRAINED_WITH_WARNINGS`; EVALUATION=`EVALUATED/INSUFFICIENT_TEST_SAMPLE`; Exploratory=`GENERATED/GENERATED_WITH_WARNINGS`等 | 21/30のstatus matrixをcurrent constraintへ修正 |
| `Artifact` | `family / storage_uri / deleted_at`等をcanonical fieldのように扱った | canonical Artifactは`object_key`をstorage locatorとし、`family / storage_uri / deleted_at`を持たない | 21/23/30をcurrent fieldへ修正 |
| `GraphVersion` | origin/reference ruleを概略化していた | `DISCOVERED / CONSTRAINT_ADJUSTED / USER_DEFINED / IMPORTED / USER_EDITED`ごとにsource/parent制約を持つ | 21へcurrent origin invariantを展開 |
| Annotation | simple Annotationとworkspace annotationを一つのcontractのように扱う余地があった | Result/GraphVersion XOR targetのsimple Annotationと、Project closure向けWorkspaceAnnotationが別persistence/API | 21/23/30で2系統を明確に分離 |
| Canonicalization | generic listを自動sortするような記載があった | list/tupleは入力順を保持し、JSON object keyをcanonical serialization時にsortする | 21のcanonicalization規則を修正 |
| Schema Registry | `resource_type + schema_version`複合keyのように記載していた | current registryは`schema_version`文字列をkeyとして登録・validate/canonicalize/hashする | 21/30を修正 |
| Authentication | Bearer/OIDCをcurrent contractのように記載した箇所があった | common Bearer/OIDC middlewareはなく、identityを要するrouterでは`X-User-Id`、未指定`anonymous`の実装がある | 22/23をcurrent request identityへ修正 |
| Project role | `ANALYST / OPERATOR`等をcurrent roleのように扱っていた | Project closure roleは`OWNER / EDITOR / VIEWER` | 22/23を修正 |
| Worker claim | public `claim_token` resource/APIを想定していた | repository `claim_next / renew_lease / complete`と`Execution.lease_owner / lease_expires_at`がclaim/lease authority。process-local worker tokenは内部値 | 23/30を内部repository contractへ修正 |
| Runtime events | independent Execution/Stage event publisher/schemaが存在するように記載していた | Planning baselineに独立public `ExecutionEventPublisher / StageEventPublisher`は確認できず、persistent lifecycle stateがauthority | 23/30から架空event contractを除去 |
| Causal planner | `IDENTIFICATION -> ELIGIBILITY -> ESTIMATION ...`のmulti-stage DAGをcurrent runtimeのように扱った | current `CausalPlanner`はcanonical `Execution.operation`を1つのruntime StageTypeへ写像し、1 Executionにつき1 Stageのcompatibility planを生成 | 22/23/30をone-operation/one-stage runtimeへ修正 |
| Predictive planner | `PREPARE -> SPLIT`等、current planと異なる順序が混入 | full planは`split -> prepare -> train -> evaluate -> optional explain` | 22/23/30を修正 |
| Exploratory planner | Navigation Stageと同名のmulti-stage runtimeを想定できる記述だった | current plannerはoperationごとに1 runtime Stageを生成 | 22/23/30にcurrent mappingを明記 |
| `PlanValidator` | family-specific policyやProject ownership等もgeneric validatorが担うように読めた | current validatorはplan schema、stage/runner、timeout、dependency/binding、cycle等のgeneric checksを担当 | 22/30でgeneric validationとapplication/domain validationを分離 |
| `StageRunnerRegistry` | register signatureを誤って記載していた | `register(runner)`し、keyは`runner.stage_type`; `resolve(stage_type)`, `contains(stage_type)` | 30を修正 |
| CLI | generic `ariadne project list / execution submit / result show`等をcurrent CLIのように扱った | current entry pointは`ariadne-discover / estimate / identify / refute / sensitivity / api / worker`。scientific CLIはlocal/headless boundary | 22/23/30を修正 |
| API routes | 架空routeや一律のAPI conventionが混入していた | current router群は`annotations/artifacts/dataset_versions/executions/exploration/graph_versions/predictive/predictive_workflow/product_closure/projects/results/workspace_lifecycle` | 23を実route中心に再展開 |
| Idempotency | export等すべてが`Idempotency-Key`対応するように一般化していた | endpointごとに異なる。Result export等は対応する一方、Project Closure `POST /projects/{project_id}/exports`はheaderを受けない | 23をendpoint別contractへ修正 |
| Lineage authority | ENH-E4 Phase分類を根拠にsemantic relationを説明し、current classifierと向き/tupleが一致しない箇所があった | `classify_lineage_authority`のtyped/generic-only tupleがcurrent authority | 21/30をclassifierのexact tupleへ置換。Phase依存記述を除去 |
| Package/module map | `analysis_spec_service.py / planning_service.py / lineage_service.py / export_service.py`等、存在しないmodule名をcurrent構造のように列挙していた | current `product/application`, `product/workflow`, `capabilities`, `interfaces`には具体的な別file setが存在する | 30 §2をcurrent package baselineへ置換し、ENH-E5新規Navigation module名はfreeze前に捏造しない方針へ修正 |
| Research Context relation | relation typeごとの一般cycle禁止がcurrent schemaにあるように記載していた | domainはrelation shape/typeを検証し、FIX時に同一Project targetを解決して自己参照を拒否する。一方、relation graph全体の一般cycle検出はPlanning baselineにはない | 21から未実装cycle policyを除去し、current validation範囲を明記 |
| Analysis Specification list API | `/analysis-specifications`がFamily / Context / Dataset query filterを受けるように記載していた | Planning baseline routerは`project_id`のみを受け、Project内Specificationを一覧返却する | 23のroute semanticsを修正 |
| Research Context usage API | canonical Execution / Result全体のusageを返すように読める記載だった | Planning baseline serviceはAnalysisSpecificationとhistorical `FamilyExecutionOrm / FamilyResultOrm`を参照する | 23でcompatibility projectionであることと限界を明記 |

## 4. Current package boundary confirmed

### 4.1 Product domain

current domainには少なくとも次が存在する。

```text
analysis_spec.py
analysis_specification.py
analysis_view.py
annotation.py
artifact.py
dataset_version.py
enums.py
errors.py
execution.py
execution_plan.py
graph_semantics.py
graph_version.py
lineage.py
project.py
research_context.py
result.py
schemas.py
stage_execution.py
```

### 4.2 Product application

current application layerには`execution_service.py / exploratory_service.py / predictive_workflow_service.py / comparison_query_service.py / lineage_query_service.py / product_closure_service.py / workspace_lifecycle_service.py`等が存在する。ENH-E5詳細設計では、これらを存在しない汎用service名へ読み替えない。

### 4.3 Workflow

current workflow package:

```text
bindings.py
canonical_plan_provider.py
contracts.py
executor.py
output_contract.py
plan_validator.py
planner_registry.py
runner_registry.py
stage_materialization.py
```

Navigation descriptorを理由にこのruntime packageへbrowser route/current Stage dependencyを導入しない。

### 4.4 Capability

```text
causal/workflow.py
exploratory/planner.py
exploratory/runners.py
exploratory/view_compiler.py
predictive/planner.py
predictive/split_runner.py
predictive/training_runners.py
predictive/explanation_runner.py
...
```

concrete analytical runtime semanticsはこのCapability側と既存application/workflow collaborationに残す。

## 5. Lineage authority current contract

`product/domain/lineage.py`のcurrent classifierをdesign authorityとして照合した。

### 5.1 Typed structural

```text
Execution --GENERATED--> Result
Result --GENERATED--> Artifact
DatasetVersion --USED_INPUT--> Execution
AnalysisView --USED_INPUT--> Execution
Result --USED_INPUT--> Execution
Result --DERIVED_FROM--> GraphVersion
Artifact --DERIVED_FROM--> DatasetVersion
Execution --DERIVED_FROM--> Execution
Execution --REVISED_FROM--> Execution
```

### 5.2 Generic-only

fixed tuple:

```text
Artifact --DERIVED_FROM--> Artifact
Result --SUMMARIZES--> Result
Result --SUMMARIZES--> Artifact
Result --MOTIVATED--> Execution
Result --MOTIVATED--> AnalysisSpecification
Result --MOTIVATED--> AnalysisSpecificationDraft
```

加えてResult/Artifactの`DOCUMENTS / SUPPORTED_BY / EVIDENCE_FOR`およびapproved sourceからAnnotationへの`SELECTED / REJECTED`がtype allowlistに従ってgeneric-onlyとなる。unknown tupleはclosed-by-defaultである。

このcurrent classifierに合わせ、21/30の旧Phase-based説明を撤去した。


## 6. Source paths used for unchanged-contract alignment

Planning baseline SHA上で、少なくとも次のcurrent sourceを直接照合した。

```text
src/ariadne/product/domain/enums.py
src/ariadne/product/domain/schemas.py
src/ariadne/product/domain/analysis_specification.py
src/ariadne/product/domain/execution_plan.py
src/ariadne/product/domain/result.py
src/ariadne/product/domain/stage_execution.py
src/ariadne/product/domain/research_context.py
src/ariadne/product/domain/lineage.py
src/ariadne/product/persistence/orm_models.py
src/ariadne/product/persistence/repositories.py
src/ariadne/product/application/execution_service.py
src/ariadne/product/application/exploratory_service.py
src/ariadne/product/application/predictive_workflow_service.py
src/ariadne/product/application/comparison_query_service.py
src/ariadne/product/application/output_ownership_service.py
src/ariadne/product/application/workspace_lifecycle_service.py
src/ariadne/product/workflow/contracts.py
src/ariadne/product/workflow/plan_validator.py
src/ariadne/product/workflow/runner_registry.py
src/ariadne/capabilities/causal/workflow.py
src/ariadne/capabilities/exploratory/planner.py
src/ariadne/capabilities/predictive/planner.py
src/ariadne/interfaces/web_api/routers/projects.py
src/ariadne/interfaces/web_api/routers/dataset_versions.py
src/ariadne/interfaces/web_api/routers/executions.py
src/ariadne/interfaces/web_api/routers/exploration.py
src/ariadne/interfaces/web_api/routers/graph_versions.py
src/ariadne/interfaces/web_api/routers/predictive.py
src/ariadne/interfaces/web_api/routers/predictive_workflow.py
src/ariadne/interfaces/web_api/routers/results.py
src/ariadne/interfaces/web_api/routers/annotations.py
src/ariadne/interfaces/web_api/routers/artifacts.py
src/ariadne/interfaces/web_api/routers/product_closure.py
src/ariadne/interfaces/web_api/routers/workspace_lifecycle.py
```

照合対象は「ENH-E5で変更しないcurrent contract」であり、未実装のENH-E5 target Navigation設計をcurrent sourceへ一致させるためのものではない。

### 6.1 Resource field表の機械照合

`orm_models.py`のPlanning baseline定義からmapped column名を抽出し、21章の明示Field表と比較した。次のResourceはfield名が一致した。複数fieldを1行へ併記した設計表（例: `planner_id / planner_version`）は個々のORM columnへ展開して比較した。

```text
Project
ResearchContextVersion
DatasetVersion
ExecutionPlan
Execution
StageExecution
Artifact
GraphVersion
Annotation
```

`Result`は21章でcanonical field listをcode blockとして定義しているため別途domain/ORMと照合し、`result_id / execution_id / result_level / stage_execution_id / result_type / scientific_status / summary_json / payload_json / diagnostics_json / warning_json / created_at`で一致することを確認した。

`AnalysisSpecification` / `AnalysisView`はpersistent rowとversioned JSON contractを分けて記載しているため、単純なField表比較ではなくdomain envelope / ORM field / API contractを個別照合した。

## 7. Areas intentionally not forced to current implementation

以下はENH-E5で変更するtargetであるため、「current codeに存在しない」ことを乖離とは判定しない。

- Family top tabs
- Family-local Navigation Stage sidebar
- `NavigationStageDescriptor` / Family navigation descriptor
- exact browser route / default Stage
- navigation metadata delivery方式
- legacy route normalization
- Family/Stage renderer binding

ただしこれらtargetが既存runtime contractを壊さないことは、本レビューで確認したcurrent boundaryをAcceptance Criteriaとして保護する。

## 8. Residual limitations / freeze conditions

- remote sourceとの照合はPlanning baseline SHAを基準とした。local checkoutでの`git rev-parse HEAD`、migration head、full regression testはpreflight時に再確認する。
- FrontendのPredictive全設定control inventoryはG02-P01でsource/UIを全量棚卸しし、その結果をP02/P03 contractへ収束させる。100%保持はこのinventory完了をfreeze条件とする。
- Navigation metadata API / static descriptorの方式はArchitecture Review未承認のため、current implementationへの一致ではなくtarget decisionとして別管理する。

## 9. Review verdict

`PASS_WITH_CORRECTIONS_APPLIED`

ENH-E5で変更しない既存実装contractについて、今回確認した乖離はRevised designへ反映した。以後、freeze前に同種の`existing/current/維持する/再利用する`記述を追加する場合は、対象contract自体を本文へ展開し、current sourceと照合する。
