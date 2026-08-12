# Ariadne ENH-E5 G04 — P03 Exploratory Regression and Visualization Boundary

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: `G04`
- Branch: `feature/ariadne_mvp_e5`
- Remediation baseline SHA: `a4d96b33c81b5a263a2e82e6d64475de5085b616`
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

Exploratory current operations/results/artifactsを保持し、visualizationをscientific runtime Stageへ昇格させない。

## 2. Protected behavior

- operations: `PROFILE / DISTRIBUTION / ASSOCIATION / GROUP_SUMMARY / TIME_TREND / CHART`。
- read-only Data Quality/Findings surfaceのために不要なExecutionを生成しない。
- chart specificationは各Navigation Stageのrepresentationとして利用可能。
- chart/panel UI stateをAnalysisView data-selection contractへ混ぜない。
- Result/Artifact/Annotation current semanticsを維持。

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

- existing Explore operation/result regression green。
- read-only surfaceでunnecessary Execution 0件。
- visualization-only state non-persistence。
- Navigation stage namesからruntime operation/result typeを自動生成しない。

## Completion evidence

- changed production / test / schema / migration files
- focused test commands and results
- relevant regression commands and results
- candidate SHA / checkpoint SHA
- blocker status (`NONE` or explicit blocker)
