# Ariadneコードベースギャップ分析

## 0. 評価基準

`01_必要なライフサイクル.md`を目標状態とし、現行Ariadneとの差を整理する。

分類:

- `実装済み`: 主要要件を満たす
- `部分実装`: 概念または一部機能はあるが、ライフサイクルとして不足
- `未実装`: 対応resource、service、backend、artifactが確認できない
- `要確認`: ソース全件調査または実行検証が必要

## 1. 現行の強み

### 事実

現行コードには次がある。

- `CausalDesign`
- Feature Semantics
- adjustment set validation
- DiscoveryとInferenceの分離
- PC、GES、LiNGAM、NOTEARS
- edge-weightとtreatment-effectの分離
- ATE／ATTを意識した推定
- diff-in-means、OLS、g-computation、IPW、AIPW系処理
- robust SE、propensity clipping、cross-fitting設定
- balance、overlap、outcome diagnostics
- ExecutionPlan、dry-run、validate-only
- manifest、config hash、artifact lineage
- FastAPI、Worker、Transactional Outbox、lease、Attempt履歴
- Project RBAC、Dataset／Configurationのimmutable version

### 評価

Ariadneは単なるNotebook集ではない。再現性、実行管理、Artifact管理、因果設計の一部をDomain Modelとして持つ。ただし、因果分析ライフサイクル全体には未接続の領域がある。

# 2. ライフサイクル別ギャップ

## 2.1 Causal Question

- 状態: `未実装または要確認`
- 現状: treatment、outcome、estimand等は設定に存在するが、業務上の問いから独立したversioned causal question resourceは確認できない
- ギャップ:
  - population、comparison、decision useの欠落
  - question versionとRunの明示的紐付け不足
  - API／UI上のreview lifecycle不足
- 必要対応:
  - `CausalQuestion` entity／schema／repository／API
  - Run inputへの`causal_question_version_id`

## 2.2 Target Trial／Causal Design

- 状態: `部分実装`
- 現状: estimand、treatment、outcome、window、unit、time zero、adjustment set、assumptionsを持つCausal Design設定がある
- ギャップ:
  - eligibility criteria
  - assignment procedure
  - follow-up／censoring
  - adherence／intercurrent event
  - versioned DB resourceとしてのreview状態
- 必要対応:
  - schema拡張
  - backward-compatible migration
  - review statusとapproval metadata

## 2.3 Estimand

- 状態: `部分実装`
- 現状: ATE／ATT、edge weight、OLS coefficientを区別する思想がある
- ギャップ:
  - ATC、CATE、LATE
  - direct／indirect effect
  - estimand独立resource
  - estimator compatibility validation
- リスク:
  - mode名とestimandの結合が強く、拡張時に条件分岐が増える

## 2.4 Graph Representation

- 状態: `部分実装`
- 現状: Discovery graph、edge artifact、Saved Graphがある
- ギャップ:
  - DAG／CPDAG／PAGの型区別
  - circle／bidirected endpoint
  - Markov equivalenceの保持
  - graph source／uncertainty metadata
  - FCI等のlatent-confounder-aware output
- リスク:
  - GESやPCの出力を一意DAGのように扱う可能性

## 2.5 Identification

- 状態: `未実装`
- 現状: adjustment set validationはあるが、graphからestimandを識別し、識別式や不可識別理由を保存する独立stageは確認できない
- ギャップ:
  - back-door／front-door／IV identification
  - `NOT_IDENTIFIED`の正規結果
  - candidate adjustment set
  - identification artifact
  - DoWhy等のbackend
- 影響: 推定器実行前の因果的妥当性gateが不足

## 2.6 Data Eligibility

- 状態: `部分実装`
- 現状: required columns、constant／all-missing drop、feature semantics、role validation、sample minimum、overlap診断がある
- ギャップ:
  - eligibility criteria
  - time-zero consistency
  - censoring
  - cluster／panel structure
  - missingness assumptions
  - override audit
  - Run前fail／warn policyの統一

## 2.7 Estimation

- 状態: `部分実装`
- 現状: ATE系の基本推定器を持つ
- ギャップ:
  - DML、DRLearner、Causal Forest
  - CATE／HTE
  - IV＋ML
  - DiD、RDD、Synthetic Control
  - continuous／multiple treatment
  - estimator registryの能力メタデータ
- 依存上の注意:
  - `econml`は依存に存在するが、利用実装は確認できない

## 2.8 Statistical Inference

- 状態: `部分実装`
- 現状: robust SE、診断、推定結果出力がある
- ギャップ:
  - estimator横断の統一CI contract
  - cluster SE
  - bootstrap specification resource
  - multiplicity policyのRun-level適用
  - uncertainty unavailableの明示状態

## 2.9 Diagnostics

- 状態: `部分実装`
- 現状: balance、overlap、outcome、skipped edge、dropped column等がある
- ギャップ:
  - effective sample size
  - influence／extreme weights
  - CATE calibration
  - algorithm agreement
  - CI-test sensitivity
  - graph uncertainty report

## 2.10 Refutation

- 状態: `未実装`
- ギャップ:
  - placebo treatment
  - negative controls
  - random common cause
  - subset refuter
  - bootstrap refuter
  - graph perturbation
  - refutation artifact

## 2.11 Sensitivity Analysis

- 状態: `部分実装`
- 現状: alpha sensitivity、bootstrap stability、propensity clippingは一部存在
- ギャップ:
  - unobserved-confounding sensitivity
  - omitted-variable bias
  - adjustment-set variation
  - specification curve
  - conclusion reversal threshold
  - graph uncertainty propagation

## 2.12 Heterogeneous Effects

- 状態: `未実装`
- ギャップ:
  - CATE schema
  - DML／DR／Forest／Meta Learner backend
  - subgroup support／overlap
  - calibration
  - honest split
  - CATE artifact storage

## 2.13 Policy Evaluation

- 状態: `未実装`
- ギャップ:
  - policy resource
  - treatment cost／capacity
  - policy value
  - off-policy evaluation
  - approval
  - reject option

## 2.14 Time-series Causality

- 状態: `未実装または限定的`
- 現状: lagを意識する業務構想はあるが、PCMCI系の専用backendは確認できない
- ギャップ:
  - PCMCI／PCMCI+
  - LPCMCI
  - time-series graph schema
  - stationarity／autocorrelation diagnostics
  - lag selection
  - regime change

## 2.15 Discovery Uncertainty

- 状態: `部分実装`
- 現状: bootstrap stability、複数algorithm、diagnostic artifactがある
- ギャップ:
  - consensus graph
  - CPDAG／PAG uncertainty
  - downstream inference warning
  - edge-selection probabilityの標準schema
  - algorithm disagreement UI

## 2.16 Reproducibility

- 状態: `実装済みに近いが拡張必要`
- 現状: manifest、config hash、dataset／configuration version、seed、artifact checksum、Attempt履歴
- ギャップ:
  - causal question version
  - identification result version
  - external package backend version
  - split indices／fold assignment
  - reviewer decision

## 2.17 Monitoring

- 状態: `未実装`
- ギャップ:
  - effect drift
  - overlap drift
  - graph drift
  - policy value drift
  - re-analysis trigger

# 3. アーキテクチャギャップ

## 3.1 Domain Model

追加候補:

- `CausalQuestion`
- `CausalQuestionVersion`
- `CausalDesignVersion`
- `CausalGraphVersion.graph_type`
- `IdentificationResult`
- `EstimationSpecification`
- `DiagnosticResult`
- `RefutationResult`
- `SensitivityResult`
- `HeterogeneityResult`
- `Policy`
- `PolicyEvaluation`

## 3.2 Application Layer

追加use case:

- causal-question catalog
- identification
- scientific validation
- refutation
- sensitivity
- heterogeneity
- policy evaluation
- monitoring

## 3.3 Ports／Adapters

追加port:

- `IdentificationBackend`
- `CausalEstimatorBackend`
- `DiscoveryBackend`
- `RefutationBackend`
- `SensitivityBackend`
- `PolicyBackend`

候補adapter:

- DoWhy
- EconML
- causal-learn extended
- Tigramite
- statsmodels／linearmodels

## 3.4 Pipeline

現行の固定`DISCOVERY -> INFERENCE`だけでは不足する。

目標:

```text
VALIDATE_DESIGN
 -> IDENTIFY
 -> ESTIMATE
 -> DIAGNOSE
 -> REFUTE
 -> SENSITIVITY
 -> HETEROGENEITY optional
 -> POLICY_EVALUATION optional
```

Discoveryは必須前段ではない。ユーザー定義DAG、import graph、Saved GraphからIdentificationへ進める必要がある。

# 4. 品質・運用ギャップ

- 外部backendのversion compatibility matrixがない
- known-truth synthetic benchmarkが不足
- cross-library parity testがない
- algorithmごとの前提条件をUI／APIで強制していない
- scientific warningのseverity／override規約が不足
- performance budgetがない
- optional dependency分離が不足

# 5. 優先順位

## Critical

- Identification stage
- DAG／CPDAG／PAG型
- Refutation／Sensitivity
- scientific validation gate

## High

- EconML CATE backend
- FCI
- CATE diagnostics
- time-series backend
- quasi-experimental design

## Medium

- policy evaluation
- Bayesian SCM
- mediation
- monitoring

# 6. 移行上の原則

- 既存CLI、API、manifestを破壊しない
- `edge_weight`は探索的係数として残す
- 既存ATE／ATT estimatorをreference backendとして残す
- 新機能はport／adapterとして追加する
- optional dependency groupを利用する
- DB migrationはforward-onlyで作成する
- 旧Runの表示を維持する
