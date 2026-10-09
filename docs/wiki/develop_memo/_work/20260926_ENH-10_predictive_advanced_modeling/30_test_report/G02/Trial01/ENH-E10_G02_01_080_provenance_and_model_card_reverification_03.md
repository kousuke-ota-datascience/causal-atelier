# G02 Trial 01 — 080 provenance_and_model_card (reverification 03)

## Scope

AC-09 / AC-11: result, artifact, and Model Card must preserve model/method identity, feature/sample/reference identity, output scale, effective seed/parameters, package/runtime provenance, and predictive-not-causal boundary.

## Raw observation

The regression LIME runtime probe in item 060 succeeded and its explanation result contained `LIME_TABULAR`, local rows, `PREDICTION` output scale, provider contributions, and the TRAIN reference identity. Its `MODEL_CARD_RESULT` did **not** contain `explanation_method`; its complete observed key set was:

```text
code_runtime_metadata, deployment_population, feature_set, intended_use,
limitations, model_artifact_provenance, model_descriptor, schema_version,
selected_hyperparameters, split_strategy, test_metrics, training_data,
validation_metrics, warnings
```

## Interpretation / result

The Model Card omits the entire method-specific explanation/provenance set: LIME method/version, local TEST sample identity, TRAIN reference identity/hash, effective seed/parameters, output scale, and provider package/runtime version. Therefore the frozen AC-09 requirement for the Model Card is not met. This is an executable candidate product violation, not an environment or test defect. Target/candidate identities are in item 001. **Result: FAIL.**

## failure classification・再現条件

分類は `PRODUCT_INTEGRATION_DEFECT` である。LIME provider が unavailable だった、test harness が Model Card を取得できなかった、または assertion が曖昧だったためではない。successful regression LIME execution が実際に `MODEL_CARD_RESULT` を生成しており、その normalized payload に frozen provenance fields が存在しない。

再現時は item 060 の regression LIME end-to-end probe の `MODEL_CARD_RESULT.payload` keys を列挙し、`explanation_method`、method version、reference/sample identity、effective seed/parameters、output scale、provider runtime fields の欠落を確認する。必要なのは単なる documentation 追記ではなく、existing schema v1 に additive method-specific fields を product output として統合することである。
