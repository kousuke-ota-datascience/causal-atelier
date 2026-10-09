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
