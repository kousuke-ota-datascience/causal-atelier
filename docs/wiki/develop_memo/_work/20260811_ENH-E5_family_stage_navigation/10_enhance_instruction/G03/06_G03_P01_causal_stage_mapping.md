# Ariadne ENH-E5 G03 — P01 Causal Seven-stage Presentation Mapping

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: `G03`
- Branch: `feature/ariadne_mvp_e5`
- Remediation baseline SHA: `83d33f5c981fa1aa5740e91c30bb969dd6097c42`
- 契約状態: `PHASE_K_REMEDIATED / REAUDIT_PENDING`
- Canonical convergence source: `10 / 21 / 22 / 23 / 30 = NFR-019 PASS / FROZEN`
- Document role: `assigned Pxx implementation contract`

## 0. Authority / execution isolation

- 本文書は、このPackage Coding Agentに対する**唯一のnormative implementation contract**である。
- Package Coding Agentは仕様補完のためにGate `06`、他`Pxx`、`P00`、Gate `07`、`00〜30`、ADR、issue、commit message、外部Webを参照してはならない。
- repositoryはcurrent implementation factと実装方法を調査するsubstrateとして参照してよいが、仕様authorityではない。
- 本文書だけでrequired behavior / protected boundary / error semanticsを一意に決定できない場合は、探索を広げず`BLOCKED_CONTRACT_AMBIGUITY`で停止する。
- Test / Audit Agentのnormative verification sourceはGate `07`のみであり、本Pxxを期待挙動の補完に利用しない。


## 1. Outcome

current Causal resources/use casesを7 Navigation Stageへpresentation bindingする。

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


## Prohibited changes

- `Navigation Stage = Execution Stage`となるmapping、alias、inheritanceを導入しない。
- Navigation Stageを`AnalysisSpecification / ExecutionPlan / Execution / StageExecution`へpersistしない。
- CLI / Python library / backend execution use caseへCurrent Navigation Stageを必須inputとして追加しない。
- `AnalysisSpecification.analysis_family`と重複するFamily discriminatorを追加しない。
- Predictive existing fieldの削除、rename、default semantics変更を行わない。
- LightGBM / DoWhy / EconMLを追加しない。
- D3 / `DEFERRED / FUTURE` requirementをENH-E5 implementationまたはmandatory acceptanceへ混ぜない。
- testをgreenにする目的のassertion弱体化、削除、skip、xfailを行わない。


## 3. Package Acceptance Criteria

- seven stages exact。
- Navigation Stageからruntime StageType/ExecutionOperationを生成しない。
- Effects/Diagnostics/Sensitivity saved Result readで不要Executionを作らない。
- runtime input prerequisite matrixをsidebar順序で代替しない。

## Completion evidence

- changed production / test / schema / migration files
- focused test commands and results
- relevant regression commands and results
- candidate SHA / checkpoint SHA
- blocker status (`NONE` or explicit blocker)
