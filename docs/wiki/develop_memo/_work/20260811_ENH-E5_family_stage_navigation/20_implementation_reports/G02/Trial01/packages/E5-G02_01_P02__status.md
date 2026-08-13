# ENH-E5 G02 Trial 01 P02 — Package Status

- PROJECT_NAME: Ariadne
- ENHANCE_ID: ENH-E5
- GATE_ID: G02
- PACKAGE_ID: P02
- TRIAL_NO: 01
- Normative Pxx contract: `docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/10_enhance_instruction/G02/06_G02_P02_predictive_stage_recomposition.md`
- START_SHA: `e02c70c64e1d02e484db49d034f00b2bfd2137fe`
- Package status: `PACKAGE_READY`
- PACKAGE_CHECKPOINT_SHA: `cce169fbca57ff49d214168f18e0907481be59b7`
- Blocker: `NONE`

## Changed files

- `frontend/index.html`
- `frontend/app.js`
- `src/ariadne/capabilities/predictive/training_runners.py`
- `tests/product/test_enh_e5_g02_p02_subgroup_evaluation.py`

## Implementation summary

- Extended the Predictive setup surface for availability, group/time split prerequisites, preprocessing, model, tuning selection, metrics, subgroups, and explanation inputs while preserving every `predictive-analysis-spec/1` top-level field.
- Retained TEST row ordinals and configured non-feature subgroup columns in the evaluation bundle.
- Added independent subgroup record-list evaluation for primary and secondary metrics, explicit null groups, deterministic seed derivation, percentile-bootstrap uncertainty, and non-computable/suppressed uncertainty warnings.
- Kept navigation metadata separate from the unchanged Predictive runtime plan; no navigation stage was persisted or used as an execution input.

## Verification

| Command | Result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q tests/product/test_enh_e5_g02_p02_subgroup_evaluation.py tests/product/test_predictive_evaluation_e3.py tests/product/test_predictive_training_e3.py tests/product/test_enh_e5_g00_navigation.py tests/product/test_enh_e5_g01_navigation_state.py tests/product/test_predictive_frontend_contract_e3.py` | PASS — 21 passed |
| `git diff --check` | PASS |

## Remaining work

- No uncommitted P02 implementation changes remain.
