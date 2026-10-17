# ENH-E10 G03 Trial 01 P03 status

```text
PROJECT_NAME=Ariadne
ENHANCE_ID=ENH-E10
GATE_ID=G03
PACKAGE_ID=P03
TRIAL_NO=01
Package status=PACKAGE_COMPLETE
State=PACKAGE_COMPLETE
```

## Contract and identity

- Normative contract: `docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling/10_enhance_instruction/G03/06_G03_P03_browser_e2e_and_product_regression.md`
- START_SHA: `5bab0d305612dea67ef63393a876867405fb1929`
- PACKAGE_CHECKPOINT_SHA: `64bd2a18dd583349283cd5745edf63d9b28d61ad`

## Preserved P03 implementation files

- `.dockerignore`
- `Dockerfile.browser-e2e`
- `Dockerfile.predictive-advanced`
- `compose.enh_e10.yaml`
- `tests/enhancement/enh_e10/g03/browser_e2e/run_predictive_advanced.py`
- `tests/enhancement/enh_e10/g03/integration/test_predictive_advanced_browser_readiness.py`

These files add the hermetic predictive-advanced runtime, Compose overlay, browser runner, evidence capture, and static integration coverage required for P03. They are preserved in `785e73b9e8d3c01d9f6130247654cae922b576a7` (`Preserve G03 P03 blocked implementation`), which is explicitly not a `PACKAGE_CHECKPOINT_SHA` and does not change the BLOCKED state.

## Verification performed

Passed:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run --extra predictive-advanced python -m py_compile tests/enhancement/enh_e10/g03/browser_e2e/run_predictive_advanced.py
UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run --extra predictive-advanced pytest -q \
  tests/enhancement/enh_e10/g03/integration/test_predictive_advanced_browser_readiness.py \
  tests/product/test_predictive_frontend_contract_e3.py \
  tests/product/test_enh_e7_g02_p05_predictive_stage_surface_migration.py \
  tests/product/test_enh_e5_g00_navigation.py
```

Result: `15 passed in 3.82s`.

Browser runtime was started from a clean isolated stack using `compose.yaml`, `compose.e1a.yaml`, and `compose.enh_e10.yaml` under project `ariadne-enh-e10`, with `down -v --remove-orphans` teardown. The advanced image initially exposed source/configuration mode defects; P03-local Dockerfile permissions were corrected and the migration subsequently exited successfully.

The stage-aware runner then reached the visible `lightgbm_classifier.v1` + `SHAP_TREE` submission path. The API trace proves the UI created, validated, and fixed the analysis specification and created/validated its execution plan, but `POST /projects/{project_id}/executions` returned HTTP 400. No predictive execution was created.

## Blocker

Observed response body:

```json
{
  "error": {
    "code": "IDEMPOTENCY_KEY_REQUIRED",
    "message": "Idempotency-Key header is required for this command"
  }
}
```

The existing frontend Predictive submit implementation (`frontend/app.js`, submit handler near line 577) sends the execution POST with only `Content-Type`; it omits `Idempotency-Key`. The execution endpoint requires that header. This is an existing frontend/P02-scope defect, not a P03 browser-test or Compose-harness defect. P03 must not modify another package's scope to bypass it.

Consequences: neither required browser journey (scenario 100 classifier + SHAP_TREE, scenario 110 regressor + LIME_TABULAR) can reach a generated execution, result/artifact verification, or final evidence PASS. The failure evidence (screenshot, trace, video, and `evidence.json`) was generated under `test-results/browser_e2e/enh_e10/`; the Compose resources were torn down including volumes and orphans.

## Resume condition

Restore the required `Idempotency-Key` header on the frontend Predictive execution submission through the responsible package/remediation route. Then rerun P03 from this status with the uncommitted P03 implementation intact; do not treat this report as a Package checkpoint or Gate decision.

## Blocker-resolution completion (2026-10-17)

The authorized frontend blocker resolution remains unchanged:

- `BLOCKER_FIX_SHA`: `3a4cbef4bb104550f5c24c61661f5dafe265d618`
- The existing `idempotencyKey()` helper supplies the Predictive execution submission header only.

The subsequent worker diagnosis corrected the prior unsupported inference that this was a Causal dispatch failure:

- `WORKER_DIAGNOSTIC_FIX_SHA`: `263c234ff007c9da1e9a357f4745dc8f19682dbb`
- Generic execution terminal errors now use the actual `FAILED` stage's `last_error`, not the final downstream stage, which may be `SKIPPED_DUE_TO_PREREQUISITE`.
- Browser evidence is stage-aware and records `stage_key`, `status`, `last_error`, and `attempt_history` before teardown.
- The actual scenario 100 failure was `train` / `OSError: libgomp.so.1: cannot open shared object file: No such file or directory`; `split` and `prepare` succeeded, while `evaluate` and `explain` were prerequisite skips.
- The minimal runtime repair added `libgomp1` to `Dockerfile.predictive-advanced`. No workflow, API contract, model-selection behavior, or browser assertion was changed.

The rebuilt hermetic stack passed both frozen journeys. Evidence is retained at `test-results/browser_e2e/enh_e10/evidence.json`:

| Scenario | Execution | Result |
| --- | --- | --- |
| 100: Binary + `lightgbm_classifier.v1` + `SHAP_TREE` | `44c87e36-58cf-4fde-9388-07bc7398056f` | PASS; split/prepare/train/evaluate/explain all `SUCCEEDED` |
| 110: Regression + `lightgbm_regressor.v1` + `LIME_TABULAR` | `16a9a049-dd40-47ca-a218-5f434f8305fa` | PASS; split/prepare/train/evaluate/explain all `SUCCEEDED` |

Both journeys asserted execution completion, required Result/Artifact availability, generated predictive explanation, Model Card, and visible predictive-not-causal terminology.

Protected regression:

```bash
MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run --extra predictive-advanced pytest -q \
  tests/enhancement/enh_e10/g03/integration/test_predictive_advanced_browser_readiness.py \
  tests/product/test_predictive_frontend_contract_e3.py \
  tests/product/test_enh_e7_g02_p05_predictive_stage_surface_migration.py \
  tests/product/test_enh_e5_g00_navigation.py \
  tests/product/test_predictive_api_worker_e2e_e3.py \
  tests/product/test_predictive_explanation_e3.py
```

Result: `24 passed in 11.03s`.

The Compose stack was torn down with `down -v --remove-orphans` after evidence collection. P03 is complete; this report is not a Candidate Assembly, Independent Verification, or Gate decision.
