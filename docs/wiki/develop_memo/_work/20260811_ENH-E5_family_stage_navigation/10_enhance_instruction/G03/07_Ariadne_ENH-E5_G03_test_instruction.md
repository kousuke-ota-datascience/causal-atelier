# Ariadne ENH-E5 G03 — Causal Family Recomposition — Verification

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: `G03`
- Branch: `feature/ariadne_mvp_e5`
- Remediation baseline SHA: `a4d96b33c81b5a263a2e82e6d64475de5085b616`
- 契約状態: `PHASE_K_REMEDIATED / REAUDIT_PENDING`
- Canonical convergence source: `10 / 21 / 22 / 23 / 30 = NFR-019 PASS / FROZEN`
- Document role: `Gate 07 verification contract`

## 0. Authority / verification isolation

- 本文書は、このGateを検証する**Test / Audit Agentに対する唯一のnormative verification contract**である。
- Test / Audit Agentは期待挙動を補完するためにGate `06`、`Pxx`、`P00`、`00〜30`、ADR、issue、commit message、外部Webを参照してはならない。
- repository、candidate diff、test output、migration state、API responseはverification evidenceとして参照してよいが、仕様authorityではない。
- 本文書だけでPASS / FAILを一意に判定できない場合は`BLOCKED_CONTRACT_AMBIGUITY`として報告し、仕様を発明しない。


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


## Gate Acceptance Criteria

- `AC-G03-001`: 7 Navigation Stage exact。
- `AC-G03-002`: current Causal runtime operation/StageType/input prerequisiteを変更しない。
- `AC-G03-003`: Identification surfaceが本文のsemantic/assumption/statusを明示し、estimator tuningを混ぜない。
- `AC-G03-004`: Estimationはgraph+upstream result prerequisiteを保持し、estimator/nuisance/uncertainty/submit/result linkageを扱う。
- `AC-G03-005`: Effects/Diagnostics/Sensitivity read surfaceのために同名runtime Stageを新設しない。
- `AC-G03-006`: Causal comparison semantic key=`treatment/exposure,outcome,estimand,target population`を保持。
- `AC-G03-007`: semantic compatibilityが成立しないResultへdirect metric comparisonを許可しない。


## Verification architecture

- browser: seven-stage binding。
- domain/integration: exact input prerequisite matrix。
- scientific UI/service: Identification fields/assumptions/status/warnings、Estimation separation。
- result: Effects/Diagnostics/Sensitivity saved readでunnecessary execution 0件。
- comparison: Causal semantic key exact、incompatible direct comparison block。
- static: Navigation Stage -> runtime Stage/ExecutionOperation generationなし。
