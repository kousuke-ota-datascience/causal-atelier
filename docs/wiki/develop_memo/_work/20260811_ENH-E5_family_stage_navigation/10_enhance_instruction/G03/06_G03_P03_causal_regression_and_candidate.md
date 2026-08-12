# Ariadne ENH-E5 G03 — P03 Causal Runtime and Regression Preservation

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: `G03`
- Branch: `feature/ariadne_mvp_e5`
- Remediation baseline SHA: `acc43f744360e25fc504f608716bed2023817a29`
- 契約状態: `APPROVED / FROZEN`
- Canonical convergence source: `10 / 21 / 22 / 23 / 30 = APPROVED`
- Document role: `assigned Pxx implementation contract`

## 0. Authority / execution isolation

- 本文書は、このPackage Coding Agentに対する**唯一のnormative implementation contract**である。
- Package Coding Agentは仕様補完のためにGate `06`、他`Pxx`、`P00`、Gate `07`、`00〜30`、ADR、issue、commit message、外部Webを参照してはならない。
- repositoryはcurrent implementation factと実装方法を調査するsubstrateとして参照してよいが、仕様authorityではない。
- 本文書だけでrequired behavior / protected boundary / error semanticsを一意に決定できない場合は、探索を広げず`BLOCKED_CONTRACT_AMBIGUITY`で停止する。
- Test / Audit Agentのnormative verification sourceはGate `07`のみであり、本Pxxを期待挙動の補完に利用しない。


## 1. Outcome

Navigation再配置後もcurrent Causal runtime/scientific behaviorを保持する。

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


## 2. Protected result semantics

- Discovery graph Result。
- Identification Result / Data Eligibility Result。
- Treatment Effect Result。
- Diagnostics / Refutation / Sensitivity Result。
- Navigation Stage名をResult Typeへ自動変換しない。
- route changeで`base_execution_id / revision_kind / change_reason`を生成しない。

## Prohibited changes

- `Navigation Stage = Execution Stage`となるmapping、alias、inheritanceを導入しない。
- Navigation Stageを`AnalysisSpecification / ExecutionPlan / Execution / StageExecution`へpersistしない。
- CLI / Python library / backend execution use caseへCurrent Navigation Stageを必須inputとして追加しない。
- `AnalysisSpecification.analysis_family`と重複するFamily discriminatorを追加しない。
- Predictive existing fieldの削除、rename、default semantics変更を行わない。
- LightGBM / DoWhy / EconMLを追加しない。
- D3 / `DEFERRED / FUTURE` requirementをENH-E5 implementationまたはmandatory acceptanceへ混ぜない。
- testをgreenにする目的のassertion弱体化、削除、skip、xfailを行わない。


## 4. Package Acceptance Criteria

- current Causal operation/StageType/input matrix regression green。
- Graph/Identification/Estimation/Diagnostics/Refutation/Sensitivity existing tests green。
- Navigation-only changeでExecution revision metadata mutationなし。
- no DoWhy/EconML addition。

## Completion evidence

- changed production / test / schema / migration files
- focused test commands and results
- relevant regression commands and results
- candidate SHA / checkpoint SHA
- blocker status (`NONE` or explicit blocker)
