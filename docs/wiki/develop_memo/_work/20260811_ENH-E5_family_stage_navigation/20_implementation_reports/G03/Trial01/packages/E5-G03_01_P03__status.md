# ENH-E5 G03 Trial 01 P03 — Package Status

| Field | Value |
| --- | --- |
| PROJECT_NAME | Ariadne |
| ENHANCE_ID | ENH-E5 |
| GATE_ID | G03 |
| PACKAGE_ID | P03 |
| TRIAL_NO | 01 |
| Normative contract | `docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/10_enhance_instruction/G03/06_G03_P03_causal_regression_and_candidate.md` |
| START_SHA | `fe60891bc1c03ec3bc710fb9f015c50893a9349d` |
| Package status | PACKAGE_READY |
| PACKAGE_CHECKPOINT_SHA | `bb4afd2b94e724e64d60945bc961cea044acacef` |
| Blocker / remaining work | NONE |

## Changed files

- `tests/product/test_enh_e5_g03_p03_causal_runtime_regression.py`

## Implementation summary

- Added focused regression coverage for the exact five-operation Causal runtime-to-StageType mapping and its input prerequisite matrix.
- Added a navigation route-state regression check that changing Causal navigation stages cannot create `base_execution_id`, `revision_kind`, or `change_reason` metadata.
- Added a dependency guard for the prohibited LightGBM, DoWhy, and EconML additions.
- No production runtime, persistence, schema, or migration change was required.

## Verification

| Command | Result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q tests/product/test_enh_e5_g03_p03_causal_runtime_regression.py tests/product/test_enh_e3_causal_workflow_regression.py tests/product/test_api_worker_e2e.py tests/product/test_enh_e5_g03_p01_causal_stage_mapping.py` | `24 passed in 16.03s` |
| `git diff --check` | passed |

