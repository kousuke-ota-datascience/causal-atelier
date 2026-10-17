# G02 Trial 01 — 030 shap_binary

AC-03/09/10/11. Command: G02 suite in item 020; `test_enh_e10_g02_p02_shap_backend.py` passed. It trains fixed-seed LightGBM binary data and observes `SHAP_TREE`, `LOG_ODDS`, two global feature mappings and two local rows. Provider emitted one known SHAP warning about binary list-of-ndarray shape; no assertion failed.

The backend itself applies `tree_path_dependent`, raw output, and frozen additivity tolerances (`atol=1e-6`, `rtol=1e-5`). Target/candidate identities are as in item 001.

Result: **PASS** for the SHAP adapter contract. This does not cure the separate result/artifact integration failure recorded in item 080.
