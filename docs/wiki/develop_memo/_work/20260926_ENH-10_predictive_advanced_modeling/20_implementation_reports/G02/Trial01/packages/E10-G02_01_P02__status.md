# ENH-E10 G02 Trial 01 P02 — Package Status

| Field | Value |
| --- | --- |
| PROJECT_NAME | Ariadne |
| ENHANCE_ID | ENH-E10 |
| GATE_ID | G02 |
| PACKAGE_ID | P02 |
| TRIAL_NO | 01 |
| State | PACKAGE_COMPLETE |
| Coding Agent outcome | PACKAGE_READY |
| Normative contract | `10_enhance_instruction/G02/06_G02_P02_shap_backend.md` |
| START_SHA | `f9a7de18148b49fb3a4d4b90b27741d8beb3d42d` |
| PACKAGE_CHECKPOINT_SHA | `c3684d3b6b0213b609e6db510f80b94cb93a532d` |

Added the SHAP optional dependency and low-level TreeExplainer adapter with tree-path-dependent/raw semantics, canonical global/local normalization, output-scale metadata, and additivity check. Focused test: `test_enh_e10_g02_p02_shap_backend.py` PASS (1 passed; provider warning only). No blocker within P02.
