# G02 Trial 01 — 090 g01_protected_regression (reverification 03)

AC-12: **FAIL.** `test_predictive_training_e3.py` fails when run alone: 2 failed. Direct execution of the established logistic flow observed `outcome_status=FAILED`; `prepare` failed with `KeyError: 'sampling'`, then `train`/`evaluate` were skipped due to prerequisite. The candidate unconditionally indexes `explanation_specification["sampling"]` in `PredictivePrepareRunner`, breaking baseline flows whose explanation specification is empty.

Other isolated G01 registry/adapter/artifact/leakage tests passed (`25 passed in 5.39s`), but they do not negate this protected integration regression. Target/candidate identities are in item 001.
