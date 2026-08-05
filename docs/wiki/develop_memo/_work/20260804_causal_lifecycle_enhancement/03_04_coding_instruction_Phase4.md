# Phase 4 修正指示書

## 0. Coding Agentへの指示

Phase 1から3の推定結果を、監査可能なPolicy Evaluation、意思決定支援、Monitoringへ接続せよ。自動施策実行は行わず、human approvalを必須とする。加えてBayesian SCM、Mediation、複数処置、連続処置等の拡張点を導入するが、無制限な任意コード実行機構を作ってはならない。

## 1. 目的

- CATE／ATEを業務Policyの価値評価へ接続
- cost、capacity、risk、eligibilityを考慮
- off-policy evaluationを提供
- review／approval／auditを提供
- driftと再分析triggerを提供
- 高度因果モデルをpluginとして追加可能にする

# 2. Scope

## 必須

- Policy resourceとimmutable version
- Policy Evaluation
- cost／capacity constraint
- eligibility／reject option
- off-policy evaluation
- human approval workflow
- monitoring
- re-analysis trigger
- Bayesian SCM backend extension point
- mediation extension point

## 選択実装

- continuous treatment／dose response
- multiple treatment
- dynamic treatment regime
- interference／network effect
- transportability

選択実装は少なくともdomain modelとcapability contractを定義し、1つ以上をend-to-endで実装する。

## 非目標

- 外部業務システムへの自動施策配信
- 完全自動のPolicy選択
- 因果仮定の自動証明
- arbitrary Python plugin upload

# 3. Policy Domain

## 3.1 Policy

- project_id
- name
- objective
- source estimation result
- eligible population
- action set
- treatment cost
- capacity
- risk constraints
- fairness／business constraints
- abstain rule
- status

## 3.2 PolicyVersion

- canonical specification
- content hash
- source Run／Artifact
- created_by
- reviewed_by
- approved_by
- approval status

## 3.3 PolicyEvaluation

- baseline policy
- candidate policy
- estimated policy value
- incremental value
- uncertainty
- coverage
- treatment rate
- expected cost
- capacity use
- subgroup values
- diagnostics
- limitations

# 4. PolicyBackend

```python
class PolicyBackend(Protocol):
    def fit(self, request: PolicyFitRequest) -> PolicyModelResult: ...
    def evaluate(self, request: PolicyEvaluationRequest) -> PolicyEvaluationResult: ...
```

最低限:

- threshold policy
- cost-sensitive policy
- capacity-constrained top-k policy
- policy treeまたはinterpreter

`top-k`はCATE単純順位ではなくeligibility、support、uncertainty、costを検査する。

# 5. Off-policy Evaluation

対応候補:

- inverse propensity scoring
- self-normalized IPS
- doubly robust policy value
- cross-fitted policy evaluation

必須診断:

- behavior propensity
- support
- effective sample size
- extreme weights
- confidence interval
- policy leakage

Policy学習用dataと評価用dataを分離する。

# 6. Human Review

状態:

- DRAFT
- VALIDATED
- REVIEWED
- APPROVED
- REJECTED
- DEPRECATED

承認前に必須:

- causal question
- identification result
- estimator diagnostics
- sensitivity summary
- target population
- cost／capacity
- policy value uncertainty
- known limitations

承認履歴をimmutable audit eventとして保存する。

# 7. Monitoring

## Metric

- covariate drift
- treatment propensity drift
- overlap drift
- outcome drift
- effect drift
- graph edge stability
- policy treatment rate
- policy value proxy
- abstention rate
- data quality failure

## Trigger

- threshold breach
- source Dataset Version change
- Configuration Version change
- graph／design revision
- package backend revision
- treatment／outcome definition change

triggerは自動再分析を直接実行せず、再分析候補eventを作成する。実行は権限を持つ利用者が承認する。

# 8. Bayesian SCM／Mediation

## Extension Point

- structural equation specification
- mechanism per node
- posterior artifact
- intervention
- counterfactual query
- direct／indirect／total effect

## Guardrail

- graphとmechanism assumptionを明示
- posterior predictive fitとcausal identificationを分離
- arbitrary codeを受け付けない
- model family allowlist
- expensive computationはWorkerのみ

# 9. Multiple／Continuous／Dynamic Treatment

Estimator capabilityに以下を追加する。

- treatment cardinality
- continuous treatment support
- dose-response support
- sequential treatment support
- interference support

未対応Estimatorを選択した場合はRun前validationで拒否する。

# 10. API／UI

## API

- Policy CRUD／version
- validate／review／approve／reject
- evaluate
- monitoring configuration
- monitoring result
- re-analysis proposal

## UI

- policy comparison
- value／cost／capacity
- uncertainty
- subgroup support
- sensitivity summary
- approval checklist
- monitoring dashboard

UIで「推奨」を断定表示せず、「指定した仮定とデータの下で推定された候補」と表示する。

# 11. Security／Governance

- Project RBAC
- approval権限の分離
- PII列のPolicy input制御
- sensitive attributeの利用規約
- Artifact download policy
- audit log
- model／policy export制御
- no arbitrary code execution

# 12. Tests

- cost-sensitive policy value
- capacity constraint
- no-overlap rejection
- train／evaluation split leakage
- off-policy estimator synthetic truth
- approval state machine
- RBAC
- immutable audit event
- monitoring threshold
- re-analysis proposal idempotency
- Bayesian adapter optional dependency
- unsupported treatment validation

# 13. Acceptance Criteria

- Policyが推定結果から独立したversioned resourceである
- 学習用dataと評価用dataが分離される
- costとcapacityを含むpolicy valueが算出される
- overlap不良対象にはabstainできる
- human approvalなしでAPPROVEDにならない
- 外部施策実行は行わない
- monitoring breachが再分析候補eventを作る
-全結果がlineageとaudit trailを持つ
- Phase 1から3のArtifactをsourceとして追跡できる

# 14. Deliverables

- policy／monitoring domain models
- adapters
- migrations
- API／UI／Worker
- approval workflow
- synthetic scientific tests
- security review document
- operational runbook
- Sphinx methodology docs
- known limitations
