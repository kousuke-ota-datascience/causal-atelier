# G02 Trial 01 — 050 lime_binary_local

AC-05/09/10/11. Result: **FAIL**.

Direct call `lime_local_contract({"model_id":"lightgbm_classifier.v1"}, row_ordinal=9, sampling_seed=17, feature_order=["x","group=A"])` returned only keys `effective_seed, feature_order, limitation, method, parameters, representation, row_ordinal, scope` (exit 0). It contains no instance values, reference/background identity, provider contribution values, model output, positive-class probability, package/runtime provenance, or model task identity.

Repository observation: `lime_backend.py` does not import or invoke the `lime` package and its function accepts no feature matrix, fitted model payload, prediction callable, or reference data. Therefore it cannot produce a LIME explanation of the required positive-class probability. This is a verified candidate product-contract violation, not a test failure.

Target/candidate identities are as in item 001.
