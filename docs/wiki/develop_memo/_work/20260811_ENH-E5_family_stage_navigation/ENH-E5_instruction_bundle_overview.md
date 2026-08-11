# ENH-E5 指示書一式 — 次版概要

## 1. Enhancement claim

Ariadneのanalytical capabilityを`Family -> Navigation Stage*`としてapplication/navigation上で再構成し、Exploratory / Predictive / Causalを同一Project内で横断可能にする。

既存のanalysis execution、persistence、Result / Artifact / Lineage semanticsを保持し、Navigation taxonomyをruntime lifecycleへ流用しない。

## 2. Product / architectureの中心境界

```text
Project-global context
       │
       ├─ Family = global analytical context
       │      └─ Navigation Stage* = Family-local work/view context
       │
       └─ Result / Artifact / Lineage

Navigation / Presentation
       ↓
Application / Capability
       ↓
Runtime Execution
```

`Navigation Stage != Execution Stage`。

具体的には、Distributionはread-onlyでもよく、Metricsは保存済みevaluation Resultを読むだけでもよく、Explainabilityは1 Navigation Stageから複数use case/executionを呼び出してよい。

CLI / Python library / backend use caseはCurrent Navigation Stageを必須入力としない。

## 3. Current sourceとの整合

current codeには既に`AnalysisFamily`および`AnalysisSpecification.analysis_family`があるため、新Family discriminatorは追加しない。

runtime側の`StageType / StageDefinition / StageExecution`は既存execution semanticsとして維持し、Navigation Stageをpersistent fieldとしてAnalysisSpecification / ExecutionPlan / Execution / StageExecutionへ追加しない。

ENH-E5で変更しない領域はPlanning baseline sourceとRevised 21/22/23/30を再突合し、Resource field、runtime planner、Worker lease、API/CLI、Lineage authority等の設計乖離を修正済みである。監査記録は`00_enhance_background/06_existing_implementation_design_alignment_review.md`に置く。

## 4. Gate sequence

```text
G00 -> G01 -> G02 ----\
             G03 -----+-> G05
             G04 ----/
```

- G00: Family / Navigation Stage contractとruntime分離
- G01: Family/Stage navigation shell / route / history
- G02: Predictive compatibility + 6 Navigation Stage
- G03: Causal 7 Navigation Stage
- G04: Exploratory 6 Navigation Stage
- G05: cross-family convergence / full regression

## 5. Documentation / execution strategy

Planning文書はENH-E4水準の自己完結性・説明粒度を持たせる。

Executionでは参照範囲を狭める。

```text
SINGLE Coding  -> 06のみ
Package Coding -> assigned Pxxのみ
Test/Audit     -> 07のみ
```

P00はOperator / Planning用でありPackage Agentへ渡さない。

## 6. Current status

全contractは`DRAFT_FOR_REVIEW`。Human Architecture Review / preflight / baseline test / exact route・navigation metadata interface decision後にGateごとにfreezeする。
