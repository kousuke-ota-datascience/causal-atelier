# Phase 2 修正指示書

## 0. Coding Agentへの指示

Phase 1完了状態を前提に、EconMLを主backendとする異質処置効果、DML、Doubly Robust Learning、Causal Forest、Policy-ready artifactを実装せよ。単にEconML classを呼ぶwrapperにせず、Ariadneのestimand、validation、Artifact、Run、診断契約へ統合すること。

## 1. 目的

- CATE／HTEを第一級estimandとして扱う
- flexible nuisance modelを使いつつ、識別仮定と推定を分離する
- CATEの精度だけでなく、support、overlap、calibration、stabilityを評価する
- Phase 4のPolicy Evaluationへ渡せる標準Artifactを作る

# 2. Scope

## 必須Estimator

- LinearDML
- CausalForestDML
- DRLearner
- ForestDRLearner
- S-Learner
- T-Learner
- X-Learner
- DRIVまたは適切なIV＋ML estimator

実際のEconML versionで利用可能なclass名とsignatureを確認して実装すること。

## 非目標

- 全EconML estimatorのwrapper
- neural causal model
- automatic best estimator selection
- Policyの自動実行

# 3. Domain Model

## 3.1 EstimationSpecification

追加項目:

- estimand
- treatment type
- outcome type
- effect modifiers
- controls
- instruments
- estimator backend
- estimator name
- nuisance model specifications
- final model specification
- cross-fitting folds
- random seed
- inference method
- confidence level
- clipping／trimming

## 3.2 HeterogeneityResult

- ate summary
- cate artifact reference
- subgroup summaries
- support diagnostics
- overlap diagnostics
- calibration diagnostics
- uncertainty
- model interpretation artifact
- split metadata
- warnings

個人単位CATEをAPI responseへ無制限に埋め込まず、Artifact＋paged queryで扱う。

# 4. CausalEstimatorBackend

```python
class CausalEstimatorBackend(Protocol):
    def capabilities(self) -> EstimatorCapabilities: ...
    def fit(self, request: EstimationRequest) -> FittedEstimatorResult: ...
    def predict_effect(self, request: EffectPredictionRequest) -> EffectPredictionResult: ...
    def infer(self, request: InferenceRequest) -> InferenceResult: ...
```

Capabilities:

- supported estimands
- binary／continuous／multiple treatment
- discrete／continuous outcome
- instrument support
- CATE support
- interval support
- sample-weight support
- missing-value policy

# 5. EconML Adapter

## 実装原則

- EconML objectはWorker process内に閉じ込める
- serialized modelの互換性を保証できない場合は、model object保存より再現可能なspecificationとtraining artifactを正本とする
- sklearn estimatorはallowlist方式で構成する
- arbitrary import pathやpickle uploadを許可しない
- backend／estimator／sklearn package versionを保存する

## Cross-fitting

- fold数
- split seed
- group-aware splitの有無
- split assignment artifact
- time leakage防止

を保存する。

# 6. Validation

## 共通

- Phase 1でIDENTIFIEDであること
- treatment／outcome型
- effect modifierとconfounderを区別
- post-treatment feature禁止
- minimum sample
- treatment arm count
- overlap

## Estimator別

- IV estimatorではinstrument必須
- binary treatment限定Estimatorの検査
- continuous treatment互換性
- forest系のsample size warning
- cross-fitting foldとgroup数の整合

# 7. Diagnostics

必須:

- propensity distribution
- overlap by treatment arm
- effective sample size
- extreme weight rate
- CATE distribution
- subgroup support
- CATE calibration
- stability across folds／seeds
- feature importanceまたはinterpreter output
- interval coverageをsynthetic testで評価

predictive fit指標とcausal diagnosticsを別sectionに表示する。

# 8. CATE Artifact

Parquet schema例:

- unit_id
- treatment
- baseline_treatment
- cate
- ci_lower
- ci_upper
- support_flag
- fold_id
- eligibility_flag

PII policyとProject RBACを適用する。download policyも既存Column Policyと統合する。

# 9. API／UI

## API

- estimator capability一覧
- estimation specification CRUD／version
- HTE Run作成
- CATE paged query
- subgroup summary
- diagnostics

## UI

- estimandとestimatorの互換性を表示
- CATE distribution
- overlap警告
- subgroup table
- uncertainty
- 「個人の確定的効果ではない」旨を表示

# 10. Benchmark

以下のknown-truth synthetic scenarioを用意する。

- constant treatment effect
- linear heterogeneity
- nonlinear heterogeneity
- poor overlap
- treatment imbalance
- irrelevant covariates
- observed confounding
- valid IV
- weak IV

各Estimatorについてbias、RMSE、coverage、runtime、peak memoryを記録する。ただしCIで厳密なperformance thresholdを課すtestと、長時間benchmarkを分離する。

# 11. Tests

- capability validation
- estimator configuration validation
- deterministic seed
- split leakage prevention
- CATE artifact schema
- optional dependency error
- serialization／re-run
- API RBAC
- Worker retry／cancel
- synthetic effect recovery
- poor overlap warning
- IV validity input checks

# 12. Acceptance Criteria

- ATEとCATEを混同しない
- CATE RunはPhase 1 Identification Resultを必須inputとする
- 4つ以上の主要Estimator familyが同一contractで実行できる
- fold／seed／package versionがmanifestに残る
- CATE resultがpaged retrievalできる
- overlap不良時に警告またはpolicyに基づくFAILとなる
- synthetic benchmark reportを生成できる
- 既存ATE backendとの比較ができる
- 既存testを破壊しない

# 13. Deliverables

- EconML adapter
- estimator registry
- schema／migration
- API／UI
- diagnostics
- benchmark suite
- example notebooksではなく再実行可能なCLI／pipeline example
- Sphinx docs／ADR／limitations
