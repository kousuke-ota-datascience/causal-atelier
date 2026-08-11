# ENH-E5 Enhancement 構想・要件改定計画

- 状態: `DRAFT_FOR_REVIEW`
- 対象branch: `feature/ariadne_mvp_e5`
- Planning pin: `46122c68333df03680b97c253a7b5d32bf9393e7`

## 1. 課題認識

AriadneはExploratory / Predictive / Causalという複数のanalytical perspectiveを扱う一方、application navigation上ではFamilyとFamily内work/view contextの責務が十分に分離されていない。

またbackendには既に`AnalysisFamily`と、runtime execution lifecycleを表す`StageType / StageDefinition / ExecutionPlan / StageExecution`が存在する。画面上のStageをruntime Stageへ流用すると、UI taxonomy変更がCLI/library/backend runtimeへ漏れる。

## 2. 改定目的

1. `Family -> Navigation Stage*`をapplication navigation modelとして確立する。
2. concrete Navigation Stage catalogをFamily-specific Capability ownershipへ置く。
3. Navigation StageとExecution Stageを分離する。
4. existing analytical capability、特にPredictive設定を完全保持する。
5. current Project / Execution / Result / Lineage architectureを不要に変更しない。

## 3. Requirement / Design snapshot改定方針

Revised documentsは差分要約ではなく、改定後に有効なeffective snapshotとして作成する。

- Product Conceptは過去Enhancementを知らなくても読めるproduct visionから開始する。
- RequirementsはENH-E4までの章構成を継承し、E2E / FR / NFR / analytical requirement / state / auditを体系化する。
- Logical Data Designはpersistent Domain ResourceとDomain Resource外のnavigation conceptを分類する。
- Basic/API/Detailed DesignはENH-E4の責務構造をbaselineとし、Family navigationをUIだけのトップレベル構造として突出させない。
- Change Logは本文末尾へ分離する。

## 4. In scope

### 4.1 Application / Navigation

- Family navigation
- Family-local Navigation Stage
- Current Family / Stage state
- route / deep link / browser history
- legacy analytical route compatibility

### 4.2 Capability ownership

- Exploratory Stage catalog
- Predictive Stage catalog
- Causal Stage catalog
- generic aggregation/validation boundary

### 4.3 Family recomposition

Exploratory:
`Profile / Data Quality / Distribution / Relationships / Comparison / Findings`

Predictive:
`Setup / Train / Predict / Metrics / Explainability / Model Management`

Causal:
`Setup / Discovery / Identification / Estimation / Effects / Diagnostics / Sensitivity`

### 4.4 Compatibility

- Predictive existing settings 100% preservation
- existing Analysis Specification family semantics preservation
- existing ExecutionPlan / StageExecution runtime semantics preservation
- Result / Artifact / Lineage preservation
- CLI/library direct execution preservation

## 5. Out of scope

- LightGBM / DoWhy / EconML integration
- new generic model registry
- new persistent Finding/Evidence aggregate
- Navigation state DB persistence
- Overview / Flagship implementation
- runtime Execution Stage architecture redesign
- common Stage taxonomy across Families

## 6. Architecture Discovery必須確認

1. current `AnalysisFamily` ownership/value
2. `AnalysisSpecification.analysis_family`とfamily schema validation
3. `ExecutionPlan / StageDefinition / StageExecution` responsibility
4. current frontend routes / navigation / DOM/state ownership
5. Predictive visible settings / generated spec全量
6. capability/module ownership
7. existing API/router naming convention
8. persistence/migration baseline

## 7. Gate decomposition initial plan

| Gate | Acceptance boundary |
| --- | --- |
| G00 | Family / Navigation Stage contractとruntime independence |
| G01 | Family/Stage navigation shell、route/history |
| G02 | Predictive recomposition + compatibility |
| G03 | Causal recomposition |
| G04 | Exploratory recomposition |
| G05 | Cross-family convergence / product regression |

## 8. Review / Freeze条件

- Architecture ReviewがHuman approvalされる。
- Revised 00〜30がself-containedで整合する。
- 06/07/Pxxに必要なnormative decisionが完全に収束する。
- Execution Agentが上流資料を読まずに判断できる。
- ambiguityが残る場合はfreezeしない。
