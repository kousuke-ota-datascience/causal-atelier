# ENH-E5 G02 Trial 01 P01 — Package Status

- PROJECT_NAME: Ariadne
- ENHANCE_ID: ENH-E5
- GATE_ID: G02
- PACKAGE_ID: P01
- TRIAL_NO: 01
- Normative Pxx contract: `docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/10_enhance_instruction/G02/06_G02_P01_predictive_compatibility_inventory.md`
- START_SHA: `c0e4c528a69333fbe558a12283630b6d54703e75`
- Package status: `PACKAGE_READY`
- PACKAGE_CHECKPOINT_SHA: `6aa2c59b106d274222e840803ae2ad961f2ac398`
- Blocker: `NONE` within the P01 implementation scope.

## Changed files

- `tests/product/test_enh_e5_g02_p01_predictive_compatibility.py`

## Implementation summary

- Added a focused compatibility inventory that maps every existing Predictive setup control to a preserved `predictive-analysis-spec/1` top-level destination and asserts unmapped count is zero.
- Fixed the top-level Predictive payload field set, deterministic canonical payload parity, and the unchanged runtime plan `split -> prepare -> train -> evaluate` as a regression seam.
- The test does not introduce a Navigation Stage / Execution Stage mapping and does not modify persisted or runtime execution structures.

## Verification

| Command | Result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q tests/product/test_enh_e5_g02_p01_predictive_compatibility.py tests/product/test_predictive_spec_e3.py tests/product/test_predictive_leakage_e3.py tests/product/test_predictive_training_e3.py tests/product/test_predictive_explanation_e3.py -k 'not test_api_worker_persists_explanation_model_card_artifacts_and_lineage'` | PASS — 16 passed, 1 deselected |
| `git diff --check` | PASS |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q tests/product/test_enh_e5_g02_p01_predictive_compatibility.py tests/product/test_predictive_spec_e3.py tests/product/test_predictive_leakage_e3.py tests/product/test_predictive_training_e3.py tests/product/test_predictive_explanation_e3.py` | FAIL — 16 passed, 1 failed. The existing `test_api_worker_persists_explanation_model_card_artifacts_and_lineage` expected a `FITTED_MODEL --USED_INPUT--> PREDICTIVE_EXPLANATION_RESULT` lineage edge that was absent. P01 changes only its new test file, so this is recorded without weakening the assertion or changing out-of-scope lineage behavior. |

## Remaining work

- No uncommitted P01 implementation changes remain.
- The recorded explanation-lineage regression is outside P01 scope and requires separate ownership if it is to be remediated.
