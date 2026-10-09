# G02 Trial 01 — 080 provenance_and_model_card (reverification 03)

AC-09/11: **FAIL.** The successful regression LIME runtime probe reports provider-backed local output and TRAIN reference, but its `MODEL_CARD_RESULT` has no `explanation_method` field. Its keys are only `code_runtime_metadata, deployment_population, feature_set, intended_use, limitations, model_artifact_provenance, model_descriptor, schema_version, selected_hyperparameters, split_strategy, test_metrics, training_data, validation_metrics, warnings`.

Thus the Model Card does not preserve required LIME method identity/version, local sample/reference identity, effective seed/parameters, output scale, or provider package/runtime provenance. This is an executable candidate product-contract violation, not a test-side failure. Target/candidate identities are in item 001.
