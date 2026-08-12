# Ariadne ENH-E5 G02 — Predictive Family Recomposition — Verification

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: `G02`
- Branch: `feature/ariadne_mvp_e5`
- Remediation baseline SHA: `acc43f744360e25fc504f608716bed2023817a29`
- 契約状態: `PHASE_K_REMEDIATED / REAUDIT_PENDING`
- Canonical convergence source: `10 / 21 / 22 / 23 / 30 = NFR-019 PASS / FROZEN`
- Document role: `Gate 07 verification contract`

## 0. Authority / verification isolation

- 本文書は、このGateを検証する**Test / Audit Agentに対する唯一のnormative verification contract**である。
- Test / Audit Agentは期待挙動を補完するためにGate `06`、`Pxx`、`P00`、`00〜30`、ADR、issue、commit message、外部Webを参照してはならない。
- repository、candidate diff、test output、migration state、API responseはverification evidenceとして参照してよいが、仕様authorityではない。
- 本文書だけでPASS / FAILを一意に判定できない場合は`BLOCKED_CONTRACT_AMBIGUITY`として報告し、仕様を発明しない。


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


## Verification architecture

- contract/regression: UI control inventory、generated spec parity、runtime plan。
- scientific/unit: TEST-only subgroup、non-feature column、null group、primary/secondary metric、sample_count。
- uncertainty: 0.95/1000、exact deterministic seed inputs、`n<2`、`valid_resamples<200`。
- serialization: record-list shape、null representation、status/warnings。
- browser: six stages、draft preservation、Metrics read/no Execution、Predict scope、Model Management read-only。
- negative: fabricated numeric value、new ModelRegistry、causal explanation、new serving subsystem。
