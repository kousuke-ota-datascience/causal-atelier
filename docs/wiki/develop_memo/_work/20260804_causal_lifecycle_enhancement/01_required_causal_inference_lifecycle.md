# Ariadneに必要な因果分析ライフサイクル

## 0. 文書の目的

本書は、Ariadneを「因果探索アルゴリズムと効果推定器の集合」から、「因果的な問い、仮定、識別、推定、診断、反証、意思決定までを監査可能に管理する分析基盤」へ拡張するために必要なライフサイクルを定義する。

本書では、以下を区別する。

- **事実**: 現行コードまたは設定で確認できる事項
- **要求**: 今後Ariadneが満たすべき仕様
- **非目標**: 本改修で自動保証しない事項

## 1. ライフサイクル全体

```text
Business Question
  -> Causal Question
  -> Target Trial / Causal Design
  -> Causal Graph and Assumptions
  -> Identification
  -> Data Eligibility and Quality
  -> Estimation
  -> Statistical Inference
  -> Diagnostics
  -> Refutation and Sensitivity
  -> Heterogeneity
  -> Policy Evaluation
  -> Decision and Review
  -> Monitoring and Re-analysis
```

重要な原則は、**推定器を先に選ばないこと**である。因果的な問い、estimand、識別戦略、必要仮定、データ適格性を確定してから推定へ進む。

# 2. 必要な考え方

## 2.1 Business QuestionからCausal Questionへの変換

### 要求

業務上の問いを、最低限次の要素を持つ機械可読な因果的問いへ変換する。

- 対象母集団
- 処置または介入
- 比較対象
- outcome
- 観測開始時点
- 処置時点
- outcome window
- 分析単位
- estimand
- 意思決定用途

### 受入条件

- 推定器の実行前に因果的問いが永続化されていること
- API、CLI、Workerの全経路で同じ定義を参照すること
- 因果的問いのversionとRunを紐付けること

## 2.2 Target Trial／Causal Design

### 要求

観察研究であっても、可能な限り次を明示する。

- eligibility criteria
- treatment strategies
- assignment procedureの仮定
- time zero
- follow-up
- outcome
- causal contrast
- analysis plan

現行の`CausalDesign`はこの概念の核として利用し、後方互換性を保ちながら拡張する。

## 2.3 Estimandの第一級オブジェクト化

### 必須estimand

- ATE
- ATT
- ATC
- CATE
- LATE
- controlled direct effect
- natural direct／indirect effectは将来拡張

### 要求

estimandごとに次を保持する。

- 対象母集団
- treatment contrast
- outcome scale
- conditioning set
- identification strategy
- estimatorとの適合条件

`OLS coefficient`や探索グラフ上の`edge weight`をATE、ATT、CATEとして扱ってはならない。

## 2.4 因果グラフと仮定

### 必須表現

- DAG
- CPDAG
- PAG
- time-series graph

### 必須edge mark

- directed
- undirected
- bidirected
- circle endpoint
- lagged directed

### 要求

- グラフ種別を明示する
- Markov equivalenceを保持する
- CPDAG／PAGを恣意的に単一DAGへ変換しない
- 背景知識、禁止edge、必須edge、時間順序をversion管理する
- graph sourceを`USER_DEFINED`、`DISCOVERED`、`IMPORTED`、`CONSENSUS`等として記録する

## 2.5 Identification-first

### 必須識別戦略

- randomized assignment
- back-door adjustment
- front-door adjustment
- instrumental variable
- Difference-in-Differences
- Regression Discontinuity
- Synthetic Control／Synthetic DiD
- interrupted time series
- mediation

### Identification Result

最低限次を保存する。

- status: `IDENTIFIED`、`NOT_IDENTIFIED`、`PARTIALLY_IDENTIFIED`、`REQUIRES_REVIEW`
- estimand
- strategy
- adjustment set候補
- graph version
- assumptions
- derivationまたは説明
- non-identifiability reason
- reviewer status

### 原則

`NOT_IDENTIFIED`を単なる実行エラーにしない。分析上の有効な結果として保存する。

## 2.6 データ適格性と品質

### 必須検査

- treatment／outcome／covariateの型
- 欠測率と欠測機構に関する宣言
- analysis unitの一意性
- time zeroの整合
- treatment leakage
- post-treatment variable混入
- positivity／overlap
- extreme propensity
- 重複、外れ値、定数列
- cluster構造
- censoring
- sample size
- panel balance
- time-series stationarity要件

### 出力

検査結果は`PASS`、`WARN`、`FAIL`でRun前に保存する。警告を無視して実行する場合は、override理由と実行者を監査情報として保持する。

## 2.7 Estimation

### 必須ファミリー

- outcome regression
- matching／weighting
- g-computation
- IPW
- AIPW／doubly robust
- DML／orthogonal ML
- meta-learners
- causal forest
- IV estimators
- panel／quasi-experimental estimators

### 要求

- estimatorは識別済みestimandと互換であること
- nuisance modelとtarget modelを区別すること
- cross-fittingのfold、seed、splitを保存すること
- estimator固有の仮定を保存すること
- 複数推定器の結果を同一estimandの下で比較可能にすること

## 2.8 Statistical Inference

### 必須項目

- point estimate
- standard error
- confidence interval
- p-valueは必要な場合のみ
- effective sample size
- cluster／robust SE
- bootstrap specification
- multiple testing adjustment

### 原則

point estimateだけを成功結果として扱わない。不確実性が算出不能な場合は、その理由を明示する。

## 2.9 Diagnostics

### 共通診断

- covariate balance
- propensity overlap
- positivity violation
- residual diagnostics
- influence／extreme weight
- effective sample size
- model fitは因果妥当性とは別指標として表示

### Discovery診断

- algorithm agreement
- bootstrap edge stability
- hyperparameter sensitivity
- conditional independence test sensitivity
- graph density
- unresolved orientation
- latent confounder warning
- nonstationarity warning

## 2.10 Refutation／Falsification

### 必須refuter

- placebo treatment
- negative-control exposure
- negative-control outcome
- random common cause
- data subset
- bootstrap refutation
- simulated confounder
- graph perturbation

### 出力

- refuter name
- null／alternative
- perturbation
- result
- interpretation
- severity
- reproducibility metadata

Refutation成功は仮定の証明ではない。特定の破綻を検出できなかったことのみを意味する。

## 2.11 Sensitivity Analysis

### 必須観点

- unobserved confounding
- omitted-variable bias
- propensity clipping threshold
- adjustment set variation
- outcome model variation
- treatment model variation
- graph uncertainty
- sample inclusion rule
- missing-data assumption

### 必須出力

- 結論が反転する閾値
- effect estimateの範囲
-主要仮定ごとの頑健性
- base specificationとの差

## 2.12 Heterogeneous Treatment Effects

### 必須概念

- CATE
- subgroup effect
- ITEは観測不能な個体反実仮想の直接観測値ではないこと
- honest sample splitting
- subgroup multiplicity
- calibration
- stability

### 必須診断

- treatment effect distribution
- subgroup support
- within-subgroup overlap
- CATE calibration
- policy value
- uncertainty

## 2.13 Policy Evaluation／Decision

### 必須概念

- treatment cost
- capacity constraint
- risk constraint
- policy value
- incremental value
- off-policy evaluation
- reject option
- human approval

CATEの順位をそのまま施策対象者リストにしてはならない。費用、容量、適格性、fairness、推定不確実性を考慮したPolicyとして扱う。

## 2.14 時系列因果

### 必須概念

- lag
- contemporaneous relation
- autocorrelation
- causal stationarity
- regime change
- latent confounding
- temporal aggregation
- forecastingとcausal effectの区別

Granger causalityを介入効果と同一視しない。

## 2.15 Discovery Uncertainty

### 要求

- discovery resultを真のDAGと断定しない
- CPDAG／PAGの不確定方向を保持する
- algorithm間差異を保存する
- bootstrap selection probabilityを保存する
- graph selection後の推定でselection uncertaintyを無視している場合は警告する

## 2.16 Reproducibility／Auditability

### 必須記録

- input dataset version
- configuration version
- causal question version
- causal design version
- graph version
- identification result
- estimator version
- package version
- random seed
- data split
- environment hash
- code revision
- artifacts checksum
- reviewer／approval

## 2.17 Monitoring／Re-analysis

### 必須観点

- covariate drift
- treatment assignment drift
- overlap degradation
- outcome drift
- effect drift
- graph instability
- policy value degradation
- package／model version change

再分析のtriggerは時間経過だけでなく、データ、処置割当、outcome定義、業務ルール、因果仮定の変更を含む。

# 3. 非目標

Ariadneは以下を自動保証しない。

- 真の因果グラフの発見
- 未観測交絡が存在しないこと
- 識別仮定の真実性
- 推定値の業務妥当性
- Policyの自動実行
- 人手レビューの代替

# 4. 横断的な品質要件

- 各段階は独立したversioned resourceであること
- `validation`と`scientific review`を区別すること
- `WARN`を黙って成功扱いしないこと
- UI、API、CLI、Workerで意味を統一すること
- 既存のArtifact／Manifest／Run／Attemptを再利用すること
- 外部ライブラリはAdapter経由で利用し、domain modelへ型を漏らさないこと
