# Ariadne ENH-E5 G02 — Predictive Family Recomposition — Gate Integration

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: `G02`
- Branch: `feature/ariadne_mvp_e5`
- Remediation baseline SHA: `acc43f744360e25fc504f608716bed2023817a29`
- 契約状態: `PHASE_K_CONVERGED / EXECUTION_FREEZE_READY`
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

Predictive existing settings/spec/runtime semanticsを保持しつつ6 Navigation Stageへ再配置し、subgroup evaluationを追加する。Phase G trace=`PF-D2-03`。

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


## 2. Navigation surface responsibilities

- `Setup`: existing configuration編集/validation。
- `Train`: current full predictive planへの入口。Navigation Stageとruntime train Stageを同一視しない。
- `Predict`: existing model/result/prediction artifact capabilityの範囲。new online serving/model deploymentはscope外。
- `Metrics`: saved `EVALUATION_RESULT` read/compare。開くだけでExecutionを生成しない。
- `Explainability`: Predictive explanation/result/artifactを扱い、causal interpretationへ変換しない。
- `Model Management`: `TRAINING_RESULT / EVALUATION_RESULT / MODEL_CARD_RESULT` と `FITTED_PREPROCESSOR / FITTED_MODEL / MODEL_CARD` のread-oriented surface。UI名だけを理由にpersistent `ModelRegistry`を作らない。
- Stage switchでunsaved DRAFT form inputを失わない。

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

- `AC-G02-001`: existing Predictive visible settings/control inventory unmapped count=0。
- `AC-G02-002`: generated `predictive-analysis-spec/1` payload parity。field削除/rename/default semantic変更なし。
- `AC-G02-003`: Navigation Stages=`setup/train/predict/metrics/explainability/model-management`。
- `AC-G02-004`: Navigation Trainはruntime `predictive.train.v1`と同一identityではなく、current full planを起動し得る。
- `AC-G02-005`: Predictはnew general-purpose online scoring/serving subsystemを必須化しない。
- `AC-G02-006`: Metricsはsaved `EVALUATION_RESULT` readで成立し、新Executionを要求しない。
- `AC-G02-007`: subgroup evaluationが本文のTEST/null/metric/bootstrap/seed/list-record contractに一致。
- `AC-G02-008`: Explainabilityをcausal explanationとして表示/exportしない。
- `AC-G02-009`: Model Managementはread-orientedで、新`ModelRegistry` aggregateを追加しない。
- `AC-G02-010`: Stage switchでunsaved Predictive DRAFT inputを意図せず失わない。
