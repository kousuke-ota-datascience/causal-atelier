# Ariadne ENH-E5 G02 — P03 Predictive Regression, Draft Preservation and Read Surfaces

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: `G02`
- Branch: `feature/ariadne_mvp_e5`
- Remediation baseline SHA: `acc43f744360e25fc504f608716bed2023817a29`
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

Predictive navigation後のcompatibility、draft preservation、Explainability/Model Management scientific boundaryをregressionで保護する。

### Predictive Compatibility Contract

`predictive-analysis-spec/1` top-level fieldを削除/rename/default semantic変更しない:

```text
schema_version
task_type
prediction_question
feature_spec
split_spec
preprocessing_spec
model_spec
tuning_spec
evaluation_spec
explanation_spec
```

Setup surfaceは少なくとも次を編集・検証できる:

- task / prediction question
- target
- feature selection / availability / exclusion
- split strategy / ratio / group / time boundaries / seed
- preprocessing
- model spec
- tuning selection
- evaluation metrics / subgroups
- explanation method / sampling

Current runtime plan:

```text
split -> prepare -> train -> evaluate -> optional explain
```

Navigation taxonomyとruntime planを同一視しない。


## 2. Required behavior

- Navigation Stage切替でunsaved Predictive DRAFT inputを失わない。state authorityはroute-independent parent/application form state等へ一意化する。
- `Metrics` openだけで新Executionを作らない。
- `Model Management`はread-orientedで`ModelRegistry` aggregateを新設しない。
- Predictive explanationをcausal effect/identification resultとして表示/exportしない。
- Predictでnew general-purpose scoring/online serving subsystemを作らない。

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

- existing Predictive regression green。
- route switch前後でDRAFT input parity。
- saved Result/Artifact read surfacesで不要なExecution 0件。
- no new ModelRegistry。
- no causal interpretation leakage。

## Completion evidence

- changed production / test / schema / migration files
- focused test commands and results
- relevant regression commands and results
- candidate SHA / checkpoint SHA
- blocker status (`NONE` or explicit blocker)
