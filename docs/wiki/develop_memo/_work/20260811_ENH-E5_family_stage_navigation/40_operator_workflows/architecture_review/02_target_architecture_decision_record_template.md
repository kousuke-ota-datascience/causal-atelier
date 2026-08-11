# ENH-E5 Target Architecture Decision Record（目標アーキテクチャ決定記録）

文書区分: Architecture Decision Artifact  
状態: **DRAFT_FOR_HUMAN_APPROVAL**  
レビュー対象Planning pin: `46122c68333df03680b97c253a7b5d32bf9393e7`

## ADR-1 — Application navigation model

```text
AnalysisFamily
  -> FamilyNavigationDescriptor
       -> NavigationStageDescriptor*
```

concrete descriptorは各analytical Capabilityが所有する。generic product/application codeはaggregation/validationを担当し、Frontendはread-only descriptor interfaceを利用する。

## ADR-2 — Navigation Stage != Execution Stage

Navigation StageはUI/application上のwork/view context、Execution Stageはruntime lifecycle単位である。

1:1 mappingを前提にしない。

### Problem scenario 1 — Distribution
`Exploratory / Distribution`はread-only viewであり、対応するruntime executionが存在しなくてもよい。

### Problem scenario 2 — Metrics
`Predictive / Metrics`はtraining中に生成済みevaluation resultを読むだけの場合がある。

### Problem scenario 3 — Explainability
1つのNavigation Stageの裏で複数use case/executionが動いてよい。

### Problem scenario 4 — CLI/library leakage
Navigation Stageをexecution inputにすると、headless callerまで`current_stage=train`等のUI contextを設定する必要が生じる。

したがってruntime layerはNavigation Stageへ依存しない。

加えて、Navigation Stageを `AnalysisSpecification` / `ExecutionPlan` / `Execution` / `StageExecution` のpersistent fieldとして追加しない。

## ADR-3 — Capability ownership

- Exploratory Capability: Exploratory Stage catalog
- Predictive Capability: Predictive Stage catalog
- Causal Capability: Causal Stage catalog

product/application layerはFamily-specific Stage semanticsを集中所有しない。

## ADR-4 — Existing AnalysisFamilyの再利用

current product-domain `AnalysisFamily` values `EXPLORATORY`, `CAUSAL`, `PREDICTIVE`をinternal Family identityとして再利用する。

current `AnalysisSpecification` が既に `analysis_family: AnalysisFamily` を保持し、family-specific schema validationへ利用していることをcurrent sourceで確認済みである。

duplicate Family enum/string taxonomyまたは重複discriminator fieldは作らない。`AnalysisSpecification.current_family`等を追加しない。

## ADR-5 — Canonical catalog interface

**Decision status: DRAFT candidate. exact endpoint/pathはHuman approvalとcurrent API convention照合後にfreezeする。**

Target endpoint candidate:

```http
GET /api/v1/navigation/analysis
```

Response schema: `analysis-navigation/1`。

Frontendはrenderer binding registryを持てるが、label/order/default catalogを二重管理しない。

## ADR-6 — URL canonical navigation state

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}
```

E5ではlast Family/StageをDB/workspace-stateへ永続化しない。

## ADR-7 — Global surface / Overview

Project Management、Research Context、Data、Results/LineageはFamily外のglobal surfaceとして維持する。

E5では`Overview`/FlagshipをFamily peerとして追加しない。将来global workspaceとして再検討する。

## ADR-8 — Persistence / engine boundary

- DB migration: `N/A` target
- AnalysisSpecification / ExecutionPlan / Execution / StageExecution / Result schema migration: `N/A`
- duplicate AnalysisFamily discriminator: `PROHIBITED`
- Navigation Stage persistent field: `PROHIBITED`
- LightGBM / DoWhy / EconML: out of scope
- new persistent Finding/Evidence domain: out of scope

## ADR-9 — CLI/library independence

`Family × Navigation Stage`はanalysis executionの必須input contractではない。

Allowed:

```text
CLI/library -> Analysis Spec / Use Case -> Runtime
```

Prohibited dependency:

```text
CLI/library -> Navigation Stage -> Runtime
```

`AnalysisFamily`がdomain discriminatorとして存在することは許容する。

## ADR-10 — Execution Agent contract isolation

Planning/architectureの判断はGate freeze前にPrimary Execution Contractへ収束する。

- SINGLE_EXECUTION Coding Agent: freeze済み06のみをnormative sourceとする。
- WORK_PACKAGE Coding Agent: assigned freeze済みPxxのみをnormative sourceとする。
- Test/Audit Agent: freeze済み07のみをnormative verification sourceとする。

repositoryはfact/evidence/substrateであり、仕様authorityではない。

single contractだけでrequired behaviorを一意に決められない場合は`BLOCKED_CONTRACT_AMBIGUITY`。

### 目的

- 無駄なspecification searchを減らす
- Agent自身のarchitecture再判断を減らす
- code/testへreasoning budgetを集中する
- interpretation varianceを下げる
- 品質を維持したAI credit利用効率向上を狙う

## ADR-11 — Family Stage catalog

Exploratory: Profile, Data Quality, Distribution, Relationships, Comparison, Findings.  
Predictive: Setup, Train, Predict, Metrics, Explainability, Model Management.  
Causal: Setup, Discovery, Identification, Estimation, Effects, Diagnostics, Sensitivity.

## ADR-12 — Alternatives

### Frontend-static full catalog
不採用。Capability ownershipとcanonical semantic sourceを二重化する。

### Execution StageType reuse
不採用。navigationとruntime lifecycleが混線する。

### Navigation state persistence
E5では不採用。URLで必要なdeep-link/history semanticsを表現でき、cross-session last-viewは未要件。

### Overviewを4番目のFamily tabにする
不採用。Overviewはanalytical Familyではない。

## ADR-13 — Approval

Human architecture owner: `PENDING`  
Approved at: `PENDING`  
Coding開始条件: approval + preflight + Gate contract freeze
