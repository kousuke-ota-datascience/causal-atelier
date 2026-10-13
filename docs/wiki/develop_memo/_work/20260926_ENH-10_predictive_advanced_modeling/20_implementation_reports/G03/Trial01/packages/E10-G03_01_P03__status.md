# ENH-E10 G03 Trial 01 P03 status

```text
PROJECT_NAME=Ariadne
ENHANCE_ID=ENH-E10
GATE_ID=G03
PACKAGE_ID=P03
TRIAL_NO=01
Package status=BLOCKED_IMPLEMENTATION
State=BLOCKED
```

## Contract and identity

- Normative contract: `docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling/10_enhance_instruction/G03/06_G03_P03_browser_e2e_and_product_regression.md`
- START_SHA: `5bab0d305612dea67ef63393a876867405fb1929`
- PACKAGE_CHECKPOINT_SHA: none (incomplete implementation must not be checkpointed)

## Changed, uncommitted P03 files

- `.dockerignore`
- `Dockerfile.browser-e2e`
- `Dockerfile.predictive-advanced`
- `compose.enh_e10.yaml`
- `tests/enhancement/enh_e10/g03/browser_e2e/run_predictive_advanced.py`
- `tests/enhancement/enh_e10/g03/integration/test_predictive_advanced_browser_readiness.py`

These files add the hermetic predictive-advanced runtime, Compose overlay, browser runner, evidence capture, and static integration coverage required for P03. They remain uncommitted because the required browser journeys do not complete.

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

## Blocker-resolution resume (2026-10-13)

The authorized cross-package frontend resolution was made without altering any P01/P02 checkpoint:

- `BLOCKER_FIX_SHA`: `3a4cbef4bb104550f5c24c61661f5dafe265d618`
- Change: the existing `idempotencyKey()` helper is now supplied as `Idempotency-Key` for the Predictive execution submission only.
- Regression: `node --check frontend/app.js` plus the focused Predictive frontend/API suite passed (`10 passed in 6.18s`).

After the fix, the browser scenario 100 UI created, validated, and fixed the Analysis Specification, created and validated the Execution Plan, and received `202 Accepted` for execution creation. This confirms that the original `IDEMPOTENCY_KEY_REQUIRED` blocker is resolved.

The resumed browser runner then observed the created execution reach `FAILED`, with exact terminal error `Causal Stage failed`. The runner now asserts terminal execution status before waiting for the success notice; its evidence records `AssertionError: Causal Stage failed` rather than masking the failure as a notification timeout. The worker log independently records that it claimed the execution as `PREDICTIVE/DISCOVERY` and failed it in the generic Causal Stage dispatch.

This is a worker-side Predictive execution-dispatch failure, outside the P03 browser/runtime scope. P03 does not modify it speculatively. Scenario 110 was not run because scenario 100 did not complete; no scenario 100/110 PASS evidence exists.

Additional verification after the runner failure classification update:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run --extra predictive-advanced python -m py_compile tests/enhancement/enh_e10/g03/browser_e2e/run_predictive_advanced.py
UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run --extra predictive-advanced pytest -q \
  tests/enhancement/enh_e10/g03/integration/test_predictive_advanced_browser_readiness.py \
  tests/product/test_predictive_frontend_contract_e3.py
```

Result: `6 passed in 3.05s`. The hermetic Compose stack was torn down using `down -v --remove-orphans` after evidence collection.
