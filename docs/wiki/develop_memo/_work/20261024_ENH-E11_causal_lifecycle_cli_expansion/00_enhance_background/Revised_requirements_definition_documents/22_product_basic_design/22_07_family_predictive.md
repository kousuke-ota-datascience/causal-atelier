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
