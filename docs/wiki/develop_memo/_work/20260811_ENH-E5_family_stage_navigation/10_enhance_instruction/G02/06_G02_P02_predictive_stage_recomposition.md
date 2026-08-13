# Ariadne ENH-E5 G02 — P02 Predictive Stage Recomposition and Subgroup Evaluation

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: `G02`
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

Predictive 6 Navigation Stageとfrozen subgroup evaluation semanticsを実装する。

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


### Predictive Subgroup Evaluation Contract

- evaluation population=`untouched TEST`。
- `evaluation_spec.subgroups`の各columnを独立sliceし、automatic intersection/discovery/fairness frameworkを追加しない。
- subgroup columnはmodel featureである必要はない。TEST row ordinal/identityとともにevaluation bundleへ保持する。
- nullはexplicit null group。
- primary metricとrequested secondary metricsをgroupごとに評価。
- 全recordへ`sample_count`必須。
- uncertainty=`nonparametric percentile bootstrap`。
- `confidence=0.95`, `requested_resamples=1000`。
- bootstrap seedは、immutable split/spec seed、subgroup column、canonicalized `subgroup_value`、metric、namespaceからdeterministically derive。
- `sample_count < 2`または`valid_resamples < 200` => `uncertainty=null` + warning。
- metric non-computable => `value=null`, `uncertainty=null`, status/warning。numeric valueを捏造しない。
- outputはgroup value keyed mapではなくrecord list。

Record shape:

```text
subgroup_column
subgroup_value
is_null_group
metric
sample_count
value?
uncertainty?:
  method = percentile_bootstrap
  confidence = 0.95
  lower
  upper
  requested_resamples = 1000
  valid_resamples
status
warnings[]
```

External serialized fieldは`subgroup_value`に固定する。`group_value`はinternal algorithm/model termとしてのみ使用可能で、alternative JSON field nameとしては使用しない。


## 2. Surface rules

- Train Navigation Stageはruntime train identityではない。
- Predictでnew standalone scoring/serving executionを追加しない。
- Metricsはsaved evaluation readで成立可能。
- ExplainabilityはPredictive semanticsのみ。
- Model Managementはread-oriented。

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

- six Navigation Stageへcanonical routeで到達可能。
- subgroup null group / non-feature column / TEST row identity / primary+secondary metrics。
- deterministic seed derivation。
- `n<2`と`valid_resamples<200`の両方をCI suppression。
- record-list output shape。
- non-computable metricでfabricated value 0件。

## Completion evidence

- changed production / test / schema / migration files
- focused test commands and results
- relevant regression commands and results
- candidate SHA / checkpoint SHA
- blocker status (`NONE` or explicit blocker)
