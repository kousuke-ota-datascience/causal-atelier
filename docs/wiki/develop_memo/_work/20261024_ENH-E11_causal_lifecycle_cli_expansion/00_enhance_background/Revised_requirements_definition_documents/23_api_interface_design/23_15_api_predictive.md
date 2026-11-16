# 23_15_api_predictive


---

### 5.6 Predictive Interface

Predictive analysisは`predictive-analysis-spec/1`を入力契約とする。現行実装のfull runtime planは`split -> prepare -> train -> evaluate -> optional explain`である。

Predictive Navigation Stage:

- Setup
- Train
- Predict
- Metrics
- Explainability
- Model Management

これらのStage名に合わせて独立execution APIを6本新設することは要件ではない。

現行実装で存在するPredictive support API:

| Method | Path | 用途 |
| --- | --- | --- |
| GET | `/projects/{project_id}/predictive/capabilities` | Predictive capability metadata |
| POST | `/projects/{project_id}/predictive/split-validations` | split validationを実行しpartition artifactを保存 |
| GET | `/projects/{project_id}/predictive/partition-artifacts/{artifact_id}` | partition artifact metadata取得 |

Split validation requestは`dataset_version_id / analysis_view_id? / family_spec`を受け取る。responseは`predictive-split-validation/1`で、`status=VALID / execution_id / task_type / strategy / partition_counts / partition_artifact / source_snapshot`を返す。

`Metrics`は保存済み`EVALUATION_RESULT`をreadして成立し得る。`Model Management`は`TRAINING_RESULT`、`MODEL_CARD_RESULT`、`FITTED_MODEL`、`MODEL_CARD`等のResult / Artifactをreadするsurfaceとして成立し得る。Navigation再配置を理由にPredictive spec/validation/defaultを変更しない。


#### 5.6.1 Predictive subgroup evaluation response contract

Predictive evaluation outputは指定subgroupごとにrecord listを返す。group valueをJSON object keyへ埋め込まない。

```json
{
  "subgroup_metrics": [
    {
      "subgroup_column": "segment",
      "subgroup_value": "A",
      "is_null_group": false,
      "metric": "roc_auc",
      "sample_count": 120,
      "value": 0.81,
      "uncertainty": {
        "method": "percentile_bootstrap",
        "confidence": 0.95,
        "lower": 0.76,
        "upper": 0.86,
        "requested_resamples": 1000,
        "valid_resamples": 1000
      },
      "status": "OK",
      "warnings": []
    }
  ]
}
```

- evaluation population = untouched TEST。
- specified subgroup columnごとに独立sliceし、自動intersection/discoveryをしない。
- `sample_count`は常に必須。
- bootstrapはnonparametric percentile、confidence=0.95、1000 resamples、deterministic seed。
- `n < 2`またはvalid resamples < 200では`uncertainty=null` + warning。
- metric計算不能は`value=null`、`uncertainty=null`、status/warningを返す。値を捏造しない。

### 5.6.2 Predictive advanced capabilities contract

`GET /projects/{project_id}/predictive/capabilities` remains the canonical Predictive capability metadata endpoint.

Response schema remains:

```text
predictive-capabilities/1
```

Existing fields/types remain backward-compatible. ENH-E10 adds the following metadata from the same backend model/explanation capability authorities.

```json
{
  "schema_version": "predictive-capabilities/1",
  "task_defaults": {
    "BINARY_CLASSIFICATION": {"model_id": "logistic_regression.v1"},
    "REGRESSION": {"model_id": "linear_regression.v1"}
  },
  "model_registry": [
    {
      "model_id": "lightgbm_classifier.v1",
      "contract_version": "1",
      "supported_tasks": ["BINARY_CLASSIFICATION"],
      "parameter_schema": ["num_boost_round", "learning_rate", "num_leaves", "max_depth", "min_data_in_leaf", "lambda_l2"],
      "parameters": {
        "num_boost_round": {"type": "integer", "minimum": 1, "maximum": 2000, "default": 100},
        "learning_rate": {"type": "number", "exclusive_minimum": 0, "maximum": 1, "default": 0.1}
      },
      "provider": "lightgbm",
      "dependency": "lightgbm",
      "available": true,
      "unavailable_reason": null,
      "provider_version": "4.7.x",
      "deterministic_seed": true,
      "determinism": {"mode": "same-runtime-config", "num_threads": 1, "device_type": "cpu"},
      "serializer_id": "lightgbm-model-string/1",
      "loader_id": "lightgbm-booster/1",
      "default_for_tasks": []
    }
  ],
  "explanation_methods": [
    {
      "method": "SHAP_TREE",
      "contract_version": "1",
      "supported_models": ["lightgbm_classifier.v1", "lightgbm_regressor.v1"],
      "supports_global": true,
      "supports_local": true,
      "model_output_scales": ["LOG_ODDS", "PREDICTION"],
      "dependency": "shap",
      "available": true,
      "unavailable_reason": null,
      "provider_version": "0.52.x",
      "default_for_models": ["lightgbm_classifier.v1", "lightgbm_regressor.v1"]
    }
  ],
  "model_explanation_compatibility": {}
}
```

The example is illustrative; exact ordering is not semantic. Existing `parameter_schema`, `deterministic_seed`, `compatibility`, and existing explanation fields remain compatibility projections. Structured model controls consume `parameters`.

Backend validation is final authority. A client-provided model/method that is unregistered, task-incompatible, dependency-unavailable, parameter-invalid or scope-incompatible must be rejected explicitly; the server does not substitute a different model/method.

Stable Predictive validation/failure codes include:

- `MODEL_NOT_REGISTERED`
- `MODEL_TASK_MISMATCH`
- `MODEL_PARAMETER_INVALID`
- `MODEL_DEPENDENCY_UNAVAILABLE`
- `MODEL_ARTIFACT_UNSUPPORTED`
- `MODEL_ARTIFACT_LOAD_FAILED`
- `MODEL_FEATURE_MISMATCH`
- `PREPROCESSOR_MODEL_MISMATCH`
- `EXPLANATION_METHOD_NOT_REGISTERED`
- `EXPLANATION_METHOD_NOT_APPLICABLE`
- `EXPLANATION_DEPENDENCY_UNAVAILABLE`
- `EXPLANATION_SCOPE_NOT_SUPPORTED`
- `EXPLANATION_COMPUTATION_FAILED`

Synchronous request/domain validation uses the canonical 422 validation envelope. Provider runtime failures are persisted as execution/stage failure evidence rather than silently converted to another capability.

Model artifacts continue to use existing Artifact resources. New model writes carry `fitted-model/2` in Artifact content/metadata; existing `fitted-model/1` remains readable. No new Model Registry API or persistence aggregate is introduced.

**当該Interfaceの追加契約（関連Requirement）**

- **`FR-061`**：Algorithm Registryはtask compatibilityに加えてmodel capability、parameter schema/default、provider/optional dependency availability/versionを表現し、利用可能なtask-compatible modelをbackend authorityで選択できる
- **`FR-071`**：intended use、training data、metric、limitationsに加え、model/provider/version、effective parameters、seed/deterministic settings、feature/preprocessor identity、explanation method等の再現性provenanceをModel Cardへ記録する
- **`FR-181`**：Predictive Explanationはmodel-method compatibilityをbackend authorityで検証し、`LINEAR_COEFFICIENT_CONTRIBUTION` / `SHAP_TREE` / `LIME_TABULAR`を明示methodとして解決する
- **`FR-183`**：explanation Result/Artifactはmethod/model/provider、feature/sample identity、model/prediction output scale、background/reference、effective seed/parameters、library version等のprovenanceを保持する
- **`FR-184`**：Train / Explainability / Model Managementはbackend capability metadataからcompatible option、availability/reason、parameter definition、provenanceを表示し、Frontendを独立したmodel-method compatibility authorityにしない
