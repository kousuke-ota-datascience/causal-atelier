# 22_07_family_predictive

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `87196f2f03a7f3367724bc05fb254d1a4d98109e`.

---

### 10.3 Predictive

現行実装のfull Predictive planは次のruntime Stageを生成する。

```text
SPLIT -> PREPARE -> TRAIN -> EVALUATE -> optional EXPLAIN
```

主なdependencyは次である。

- `split.partition_manifest -> prepare.partition_manifest`
- `prepare.training_bundle / fitted_preprocessor -> train`
- `prepare.evaluation_bundle / fitted_preprocessor`および`train.frozen_model -> evaluate`
- Explainが有効な場合はprepare/train/evaluateの必要outputをExplainへbindingする。

各runtime Stageの責務:

- SPLIT: immutable partition artifactを生成する。
- PREPARE: partition manifestを用いてtraining/evaluation bundle、fitted preprocessor、explanation向け入力を生成する。
- TRAIN: training bundleとfitted preprocessorからfrozen modelとtraining summaryを生成する。
- EVALUATE: frozen modelとevaluation bundleを用いてevaluation summaryを生成する。
- EXPLAIN: 有効なexplanation specificationに従ってexplanation summary / model card等を生成する。

Navigation側の`Setup / Train / Predict / Metrics / Explainability / Model Management`は、これらruntime stageと1:1対応させない。特にNavigation `Train`はruntime `train`単体実行を意味せず、`Metrics`は保存済みevaluation Resultのreadで成立し得る。

Predictiveの既存設定項目、default、validation、generated `predictive-analysis-spec/1` semanticsは全量保持する。

#### 10.3.1 Predictive subgroup evaluation

- evaluation populationはuntouched TEST。
- user-specified subgroup columnごとに独立sliceし、automatic intersection/discovery/fairness frameworkは追加しない。
- subgroup columnはfeatureである必要はなく、partition row identity/ordinalによりTEST rowへ対応付ける。
- nullはexplicit subgroupとして扱う。
- primary/secondary metricそれぞれに`sample_count`を必須で返す。
- uncertaintyはnonparametric percentile bootstrap、confidence=0.95、resamples=1000、deterministic seed。
- `n < 2`またはvalid resamples < 200ではCIを返さずwarningを返す。
- metricが計算不能なgroupではvalue/uncertaintyを`null`とし値を捏造しない。
- outputはgroup valueをmap keyに埋め込まずrecord listとする。


#### 10.3.2 Predictive advanced model / XAI capability

ENH-E10ではexisting Predictive lifecycleを変更せず、model / explanation capabilityをprovider-neutralに拡張する。

Canonical model IDs:

| Model | Task | Default |
|---|---|---:|
| `logistic_regression.v1` | BINARY_CLASSIFICATION | Yes |
| `linear_regression.v1` | REGRESSION | Yes |
| `lightgbm_classifier.v1` | BINARY_CLASSIFICATION | No |
| `lightgbm_regressor.v1` | REGRESSION | No |

Model selection / compatibility / availability / parameter definitionのauthorityはbackend Model Capability registryとする。Frontendはこのmetadataのconsumerであり、model IDごとの独自compatibility tableをcanonical authorityとして持たない。

Advanced dependencyはoptional extra `predictive-advanced` とし、current approved boundsはLightGBM `>=4.7.0,<4.8`、SHAP `>=0.52.0,<0.53`、LIME `==0.2.0.1`。core startup/importはこのextraを要求しない。Unavailable capabilityは明示し、existing model/methodへのsilent fallbackを行わない。

LightGBMはexisting TRAIN-fitted numeric/one-hot feature matrixを受け取る。ENH-E10ではnative categorical、native missing handling、early stoppingを導入せず、TRAIN-only preprocessingとTEST isolationを維持する。

LightGBM exposed parameter set:

- `num_boost_round`
- `learning_rate`
- `num_leaves`
- `max_depth`
- `min_data_in_leaf`
- `lambda_l2`

実行はCPU、`deterministic=true`、`force_col_wise=true`、`num_threads=1`をcurrent reproducibility contractとし、same-runtime/config stabilityを対象とする。cross-platform bitwise identityは保証しない。

New fitted model writes use provider-neutral `fitted-model/2` envelope。linear payloadは`ariadne-linear-json/1`、LightGBM payloadは`lightgbm-model-string/1`。existing `fitted-model/1`はread compatibilityを維持する。Python pickle/joblibをcanonical portable model representationとしない。

Explanation methods:

| Method | Compatible model | Scope | Model-output semantics |
|---|---|---|---|
| `LINEAR_COEFFICIENT_CONTRIBUTION` | logistic / linear | global + local | LOG_ODDS / PREDICTION |
| `SHAP_TREE` | LightGBM classifier/regressor | global + local | raw LOG_ODDS / raw PREDICTION |
| `LIME_TABULAR` | logistic / linear / LightGBM | local only | positive-class PROBABILITY / PREDICTION |

`SHAP_TREE`はTreeExplainer + tree-path-dependent reference semanticsを用いる。globalはimmutable TEST explanation population上のmean absolute contribution、localはdeterministic sampleとする。

`LIME_TABULAR`はmodelが消費するpreprocessed feature space上のlocal explanationのみを提供する。TRAIN transformed featuresからdeterministic explanation referenceを構成し、global LIMEはunsupportedとして明示する。

Train / Explainability / Model Managementはcapability metadataを使用する。Unavailable advanced optionはhideせずreason付きでdisabled表示可能とし、Model Managementはread-onlyのままmodel/provider/version/effective parameters/seed/determinism/feature/preprocessor/artifact/Model Card/explanation/lineage provenanceを提示する。

No new persistent Model Registry aggregate or DB migration is required. Existing generic Execution / Result / Artifact lifecycle remains authority。


## 98. RD-04：要件由来の基本設計制約

**Status:** `RD04_DESIGN_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。要件文の抽象化・設計移管で失われてはならない元の実現方式・責務境界を保持する。旧Requirement IDとStatusを維持する。コード検証やArchitecture GateのPASSを意味しない。

### 98.1. FR-059（SPLIT）

- 既存要件の設計情報を含む原文：target leakage、future leakage、group leakage、split overlapをBackendで拒否する
- RDに残る能力／Legacy Trace：目的変数・将来情報・同一GroupなどのLeakageを検出して不適切な評価を拒否する
- Original Requirement：`FR-059`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.2. FR-061（SPLIT）

- 既存要件の設計情報を含む原文：Algorithm Registryはtask compatibilityに加えてmodel capability、parameter schema/default、provider/optional dependency availability/versionを表現し、利用可能なtask-compatible modelをbackend authorityで選択できる
- RDに残る能力／Legacy Trace：対象Taskと実行環境に適合するモデルと設定候補を選択できる
- Original Requirement：`FR-061`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.3. FR-067（SPLIT）

- 既存要件の設計情報を含む原文：untouched TEST population上で指定subgroup columnごとのmetric、`sample_count`、計算可能な場合のbootstrap uncertaintyを確認できる
- RDに残る能力／Legacy Trace：指定Subgroupの評価指標・標本数と計算可能な不確実性を確認できる
- Original Requirement：`FR-067`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.4. FR-068（SPLIT）

- 既存要件の設計情報を含む原文：fitted model、fitted preprocessor、prediction等のdurable outputをArtifactとして保存し、provider-specific fitted modelはartifact schema/provider/payload identityから対応loaderを一意に解決してfresh-process相当で再読込・predictionできる
- RDに残る能力／Legacy Trace：学習済みモデルと前処理を保存し、適合する環境で復元して再予測できる
- Original Requirement：`FR-068`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.5. FR-069（SPLIT）

- 既存要件の設計情報を含む原文：explanation method capabilityが宣言するsupported scopeに従いglobal / local Predictive Explanationを生成でき、unsupported scopeを擬似出力で補完しない
- RDに残る能力／Legacy Trace：利用可能な範囲でモデル全体・個別予測の説明を生成でき、未対応の範囲を偽装しない
- Original Requirement：`FR-069`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.6. FR-150（SPLIT）

- 既存要件の設計情報を含む原文：既存Predictive UIの設定項目、validation、generated `predictive-analysis-spec/1` semanticsを全量保持する
- RDに残る能力／Legacy Trace：既存の予測機能・入力検証・保存済み仕様の意味を維持する
- Original Requirement：`FR-150`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.7. FR-151（SPLIT）

- 既存要件の設計情報を含む原文：MetricsとExplainabilityを異なる目的のNavigation Stageとして扱い、Predict Stage導入を理由に新規standalone scoring engineを必須化しない
- RDに残る能力／Legacy Trace：予測指標と予測説明の目的を区別して利用できる
- Original Requirement：`FR-151`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.8. FR-176（SPLIT）

- 既存要件の設計情報を含む原文：Predictive Navigation Stageを新しいbackend Execution modelまたは1:1 runtime Stageとして扱わず、既存Prediction Task → Split → Training → Evaluation → Explanation → Model Card semanticsを保持する
- RDに残る能力／Legacy Trace：既存の予測タスク設定・データ分割・学習・評価・説明・Model Cardの意味を維持し、Navigation変更で分析実行契約を変更しない
- Original Requirement：`FR-176`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.9. FR-178（SPLIT）

- 既存要件の設計情報を含む原文：Binary Classification / RegressionでLightGBM backend（`lightgbm_classifier.v1` / `lightgbm_regressor.v1`）をtask-compatible modelとして選択できる
- RDに残る能力／Legacy Trace：表形式分類・回帰で承認済み追加学習方式を選択して学習・評価できる
- Original Requirement：`FR-178`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.10. FR-180（SPLIT）

- 既存要件の設計情報を含む原文：fitted modelはserialize/load round-trip後もmodel/task/feature/preprocessor identityを保持し、同一runtime/config fixtureでprediction contractを満たす
- RDに残る能力／Legacy Trace：保存済み学習モデルを復元し、適合条件下で同等の予測を再実行できる
- Original Requirement：`FR-180`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.11. FR-181（SPLIT）

- 既存要件の設計情報を含む原文：Predictive Explanationはmodel-method compatibilityをbackend authorityで検証し、`LINEAR_COEFFICIENT_CONTRIBUTION` / `SHAP_TREE` / `LIME_TABULAR`を明示methodとして解決する
- RDに残る能力／Legacy Trace：利用可能なモデル説明方式を適合性に応じて選択し、予測への変数寄与を定量的に説明できる
- Original Requirement：`FR-181`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.12. FR-182（SPLIT）

- 既存要件の設計情報を含む原文：`SHAP_TREE`はapproved compatibility範囲でglobal/localを提供し、`LIME_TABULAR`はlocal-onlyを提供する。unsupported capabilityを別methodまたは擬似global出力で補完しない
- RDに残る能力／Legacy Trace：個別予測・モデル全体への説明の提供範囲を明示し、未対応の説明を擬似出力しない
- Original Requirement：`FR-182`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.13. FR-184（SPLIT）

- 既存要件の設計情報を含む原文：Train / Explainability / Model Managementはbackend capability metadataからcompatible option、availability/reason、parameter definition、provenanceを表示し、Frontendを独立したmodel-method compatibility authorityにしない
- RDに残る能力／Legacy Trace：利用可能な学習・説明機能と不可理由、設定条件、由来を一貫して表示する
- Original Requirement：`FR-184`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.14. FR-177（SPLIT）

- 既存要件の設計情報を含む原文：UI / IA再編だけを理由に既存API contract、persistence schema、backend analysis/domain semanticsを変更しない
- RDに残る能力／Legacy Trace：UI・IA再編によって既存API契約・永続化Schema・分析の意味を変更しない
- Original Requirement：`FR-177`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.15. AR-016（SPLIT）

- 既存要件の設計情報を含む原文：subgroup metricは`sample_count`を必須とし、0.95 percentile bootstrap（1000 resamples、deterministic seed）で計算可能な場合にuncertaintyを併記し、計算不能値を捏造しない
- RDに残る能力／Legacy Trace：評価Subgroupの標本数と不確実性を明示し、標本条件・推論方法が不適切な場合は計算不能理由を示して未検証区間を生成しない
- Original Requirement：`AR-016`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../96_rd04_nfr_ar_application_review.md)
