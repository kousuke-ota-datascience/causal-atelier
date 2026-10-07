# G02 Trial 01 — 060 lime_regression_local

AC-06/09/10/11. Result: **FAIL**.

The same direct call with `model_id=lightgbm_regressor.v1` produced the identical static metadata-only object (same eight keys and no prediction, local contributions, instance/reference identity, or provider provenance). The function does not receive training/reference data or a prediction function, and does not invoke `lime`; it therefore cannot generate a regression local explanation.

This is a verified candidate product-contract violation. Target/candidate identities are as in item 001.
