# Phase 3 修正指示書

## 0. Coding Agentへの指示

時系列因果および準実験デザインを追加せよ。横断データ用Estimatorへ無理に統合せず、Identification Strategyごとの設計、入力契約、診断、Artifactを分離すること。

## 1. 目的

- 時間差、自己相関、同時点関係、regime変化を扱う
- PCMCI系の因果探索を追加する
- DiD、Event Study、RDD、IV、Synthetic Control／Synthetic DiDを追加する
- 各design固有の仮定と診断をfirst-classにする

# 2. Scope

## 2.1 Time-series Discovery

- PCMCI
- PCMCI+
- LPCMCI
- 条件付き独立性検定registry
  - ParCorr
  - robust linear option
  - nonlinear option
  - discrete／mixed optionはlibrary capabilityに合わせる

RPCMCI／J-PCMCI+はextension pointを用意し、初期実装の必須とはしない。

## 2.2 Quasi-experimental Design

- Difference-in-Differences
- Event Study
- Regression Discontinuity
- Instrumental Variables／LATE
- Synthetic Control
- Synthetic Difference-in-Differences
- Interrupted Time Series

# 3. Domain Model

## 3.1 TemporalDesign

- unit_id
- time_column
- treatment_time
- lag range
- contemporaneous links policy
- stationarity assumption
- regime metadata
- panel structure
- missing time policy
- temporal aggregation

## 3.2 QuasiExperimentalDesign

共通:

- strategy
- treated units
- control units／donor pool
- intervention time
- outcome
- covariates
- estimand
- assumptions

strategy固有:

- DiD: group、time、staggered adoption、cluster
- RDD: running variable、cutoff、bandwidth、fuzzy／sharp
- IV: instrument、endogenous treatment
- Synthetic Control: donor pool、pre-period、post-period

# 4. Tigramite Adapter

## 原則

- Domain層へTigramite型を漏らさない
- DataFrameからlibrary inputへの変換を独立component化
- lagged／contemporaneous edgeを標準Graphへ変換
- LPCMCIはPAG相当の不確定endpointを保持
- methodとCI testの仮定をmanifestへ保存

## Validation

- time index order
- duplicate unit-time
- frequency consistency
- missing timestamps
- minimum time points
- lag range
- stationarity declaration
- contemporaneous link assumption
- hidden confounder assumption

# 5. DiD／Event Study

## 必須診断

- pre-trend
- event-time support
- treatment timing distribution
- cluster count
- staggered adoption warning
- anticipation
- spillover declaration

単純なtwo-way fixed effectsだけを唯一の実装にしない。staggered adoptionでの適用制約を明示する。

# 6. RDD

必須:

- sharp／fuzzy
- bandwidth
- polynomial order
- kernel
- manipulation／density diagnostic
- covariate continuity
- bandwidth sensitivity
- local estimandであることの表示

# 7. IV／LATE

必須:

- relevance
- exclusion restrictionの宣言
- independenceの宣言
- monotonicityの宣言
- first-stage strength
- weak-instrument warning
- LATE populationの説明

# 8. Synthetic Control／SDID

必須:

- donor pool
- pre-treatment fit
- donor weight
- placebo-in-space
- placebo-in-time
- leave-one-out
- post／pre RMSPE
- intervention contamination warning

# 9. Artifact

- temporal graph
- lagged edges
- time-series diagnostic
- event-study coefficients
- pre-trend report
- RDD bandwidth sensitivity
- IV first-stage report
- synthetic weights
- placebo distribution
- design-specific Markdown report

# 10. API／UI

- design typeごとのschemaをdiscriminated unionで表現
- 不適切なfield combinationを422で拒否
- design assumptionsを明示
- graphでlagを表示
- Event Study plot
- RDD plot
- Synthetic Control observed vs synthetic

Chart生成は既存Visualization architectureを再利用する。

# 11. Tests

## Time-series

- known lag graph
- contemporaneous relation
- autocorrelation
- latent confounder scenario
- irregular timestamp rejection

## DiD

- parallel trends synthetic
- pre-trend violation
- staggered treatment

## RDD

- sharp cutoff
- fuzzy cutoff
- manipulation warning

## IV

- strong instrument
- weak instrument
- invalid configuration

## Synthetic Control

- known intervention effect
- poor pre-fit warning
- placebo workflow

# 12. Acceptance Criteria

- lagged graphがcross-sectional DAGと区別される
- PCMCI+とLPCMCIを同一Graph contractへ正規化できる
- DiD／RDD／IV／Synthetic Controlが独立strategyとして実行できる
- design固有のvalidationとdiagnosticがある
- causal effectとforecast metricを混同しない
- all resultsにdesign、assumption、package version、seed、Artifact lineageが残る
- 既存Phase 1／2 Runが後方互換で表示される

# 13. Deliverables

- temporal／quasi-experimental domain models
- ports／adapters
- optional dependency groups
- migrations
- API／UI／CLI
- scientific synthetic tests
- benchmark／limitations
- methodology docs
