# Ariadne ENH-E5 G03 — Causal Family Recomposition — Gate Integration

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: `G03`
- Branch: `feature/ariadne_mvp_e5`
- Remediation baseline SHA: `83d33f5c981fa1aa5740e91c30bb969dd6097c42`
- 契約状態: `PHASE_K_REMEDIATED / REAUDIT_PENDING`
- Canonical convergence source: `10 / 21 / 22 / 23 / 30 = NFR-019 PASS / FROZEN`
- Document role: `Gate 06 integration contract`
- Execution Mode: `WORK_PACKAGE`

## 0. Authority / execution isolation

- 本文書は`WORK_PACKAGE` Gate全体の**Operator / Gate Orchestrator向けintegration contract**である。
- Package Coding Agentへ本`06`をnormative sourceとして渡してはならない。Package Coding Agentの唯一のnormative implementation contractはassigned `Pxx` 1文書である。
- Gate Orchestratorはpackage分割、統合candidate、Gate-level protected invariant、completion evidenceの管理に本書を使用する。
- Package Coding Agentがassigned `Pxx`だけで実装を一意に決定できない場合は、他文書を読ませず`BLOCKED_CONTRACT_AMBIGUITY`として停止する。
- Test / Audit Agentのnormative verification sourceはGate `07`のみであり、本`06`や`Pxx`を期待挙動の補完に利用しない。


## 1. Gate outcome

Causal current semantics/runtimeを維持して7 Navigation Stageへ再配置し、Identification/Estimation責務を明確化する。Phase G trace=`PF-D2-04` Causal-side compatibility input。

### Causal Navigation and Runtime Boundary

Navigation Stages:

```text
setup
discovery
identification
estimation
effects
diagnostics
sensitivity
```

Current runtime `ExecutionOperation` remains:

```text
DISCOVERY
IDENTIFICATION
ESTIMATION
REFUTATION
SENSITIVITY
```

Current compatibility planner generates one runtime Stage per canonical Execution:

```text
DISCOVERY      -> causal.discovery.v1
IDENTIFICATION -> causal.identification.v1
ESTIMATION     -> causal.estimation.v2
REFUTATION     -> causal.refutation.v1
SENSITIVITY    -> causal.sensitivity.v1
```

Input prerequisites:

| operation | input_graph_version_id | input_result_id |
|---|---:|---:|
| DISCOVERY | no | no |
| IDENTIFICATION | required | no |
| ESTIMATION | required | required |
| REFUTATION | required | required |
| SENSITIVITY | required | required |

Sidebar orderをruntime prerequisiteへ変換しない。


### Causal Surface Responsibilities

- `Setup`: question/design/graph/spec preparation。
- `Discovery`: DAG、candidate confounder/mediator/collider、temporal ordering、domain assumptions。
- `Identification`:
  - causal estimand/question
  - identification strategy
  - adjustment set
  - exchangeability
  - positivity
  - consistency
  - IV / parallel trends等strategy-specific assumptions
  - identified / not identified / partially identified status
  - failure/warning reason
  - estimator tuningを混在させない
- `Estimation`:
  - estimator selection
  - nuisance model configuration
  - bootstrap/uncertainty
  - execution submission
  - estimation result linkage
  - Identification assumptionsをestimator parametersへ埋没させない
- `Effects`: effect result、ATE/ATT/CATE等、uncertainty、heterogeneity projection。
- `Diagnostics`: balance/overlap/effective sample size/weight等。
- `Sensitivity`: alternate assumptions/specification依存性。
- Effects/Diagnostics/Sensitivityはsaved Result readで成立し得る。Navigation Stageごとのnew runtime Stageは必須でない。


## 2. Comparison input

Causal semantic key:

```text
treatment/exposure
outcome
estimand
target population
```

semantic compatibilityが成立しない場合、direct quantitative comparisonを行わない。

## Prohibited changes

- `Navigation Stage = Execution Stage`となるmapping、alias、inheritanceを導入しない。
- Navigation Stageを`AnalysisSpecification / ExecutionPlan / Execution / StageExecution`へpersistしない。
- CLI / Python library / backend execution use caseへCurrent Navigation Stageを必須inputとして追加しない。
- `AnalysisSpecification.analysis_family`と重複するFamily discriminatorを追加しない。
- Predictive existing fieldの削除、rename、default semantics変更を行わない。
- LightGBM / DoWhy / EconMLを追加しない。
- D3 / `DEFERRED / FUTURE` requirementをENH-E5 implementationまたはmandatory acceptanceへ混ぜない。
- testをgreenにする目的のassertion弱体化、削除、skip、xfailを行わない。


## Gate Acceptance Criteria

- `AC-G03-001`: 7 Navigation Stage exact。
- `AC-G03-002`: current Causal runtime operation/StageType/input prerequisiteを変更しない。
- `AC-G03-003`: Identification surfaceが本文のsemantic/assumption/statusを明示し、estimator tuningを混ぜない。
- `AC-G03-004`: Estimationはgraph+upstream result prerequisiteを保持し、estimator/nuisance/uncertainty/submit/result linkageを扱う。
- `AC-G03-005`: Effects/Diagnostics/Sensitivity read surfaceのために同名runtime Stageを新設しない。
- `AC-G03-006`: Causal comparison semantic key=`treatment/exposure,outcome,estimand,target population`を保持。
- `AC-G03-007`: semantic compatibilityが成立しないResultへdirect metric comparisonを許可しない。
