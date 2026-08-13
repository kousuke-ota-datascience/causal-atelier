# Ariadne ENH-E5 G04 Trial02 Remediation Instruction

- Contract status: `APPROVED / FROZEN`
- GATE_ID: `G04`
- TRIAL_NO: `02`
- PREVIOUS_FAILED_CANDIDATE_SHA: `bd4092c21c5c7fac86bdcf36a87af53dfa2c0fab`
- PREVIOUS_TEST_EVIDENCE_COMMIT_SHA: `41846210dccec989afeb916c83d4d536bbee09fe`
- Remediation mode: `CONSOLIDATED`
- Execution mode: `SINGLE_EXECUTION`

## 1. Failure classification

Trial01 formal FAIL is a combined defect consisting of:

1. `IMPLEMENTATION_DEFECT`
   - Exploratory Result -> downstream DRAFT frontend handoff does not send the required `analysis_mode`.
2. `TEST_ORCHESTRATION_DEFECT`
   - canonical browser verification does not guarantee that the current-source worker is built and running, and therefore depends on pre-existing Docker Compose state.

Original G04 semantic claims and Acceptance Criteria remain unchanged.

Trial02 MUST create a new semantic implementation candidate. Trial01 P01/P02/P03 package checkpoints MUST NOT be reused as the Trial02 candidate.

## 2. Formal Trial01 failure

Trial01 independent Gate Test result:

```text
Gate Decision: FAIL
Promotion eligibility: PROMOTION_NOT_ALLOWED

FIXED_TRIAL_CANDIDATE_SHA:
bd4092c21c5c7fac86bdcf36a87af53dfa2c0fab
```

Non-browser independent verification passed:

```text
30 passed
15 passed, 2 skipped
git diff --check: success
```

The mandatory real-Chromium browser/regression verification failed.

Root-cause investigation established two distinct failure layers.

### 2.1. Browser worker orchestration defect

At the first Trial01 browser execution, the Compose worker was not running.

Observed state:

```text
api       = Up
frontend  = Up
database  = Up
worker    = Exited
```

The Explore execution therefore remained:

```text
QUEUED
```

until Playwright timed out.

After starting the old worker container, the queued execution was claimed but failed with:

```text
Unsupported algorithm: 'exploratory-workflow'
```

After rebuilding and recreating `worker` from current source, Explore execution advanced successfully beyond Result creation.

Therefore the browser verification environment MUST NOT rely on a previously running or previously built worker.

### 2.2. Frontend handoff implementation defect

With the current-source worker running, real Chromium advanced through Exploratory execution and saved:

```text
EXPLORATORY Resultを保存しました
```

The browser then clicked the existing:

```text
Predictive draft
```

transition.

The frontend invoked the handoff operation with a request body equivalent to:

```json
{
  "target_family": "PREDICTIVE"
}
```

The public G04 handoff contract requires:

```text
target_family: CAUSAL | PREDICTIVE
analysis_mode: EXPLORATORY | CONFIRMATORY
research_context_version_id?
family_spec_schema_version?
family_spec?
```

The API correctly rejected the incomplete request:

```text
HTTP 400
INVALID_REQUEST
analysis_mode: Field required
```

The UI consequently displayed:

```text
INVALID_REQUEST: Request validation failed. (analysis_mode: Field required)
```

This is the Trial01 production integration defect to remediate.

## 3. Required correction A — frontend Exploratory Result handoff

The existing Exploratory Result explicit transitions:

```text
Causal draft
Predictive draft
```

MUST call:

```text
POST /projects/{project_id}/exploration/results/{result_id}/create-analysis-draft
```

with a contract-valid request.

For these existing transitions, the source is an Exploratory Result and the current browser behavior is an exploratory-motivated downstream DRAFT transition.

Therefore the request MUST include:

```json
{
  "target_family": "<CAUSAL or PREDICTIVE>",
  "analysis_mode": "EXPLORATORY"
}
```

Specifically:

```text
Causal draft
  -> target_family = CAUSAL
  -> analysis_mode = EXPLORATORY

Predictive draft
  -> target_family = PREDICTIVE
  -> analysis_mode = EXPLORATORY
```

Do not add a new mode-selection UI solely for this remediation.

Do not remove or weaken the public backend support for:

```text
analysis_mode = CONFIRMATORY
```

The public API MUST continue to support both:

```text
EXPLORATORY
CONFIRMATORY
```

and existing confirmatory same-dataset reuse semantics MUST remain protected.

## 4. Required handoff semantics

After the frontend correction, the existing explicit transition MUST preserve the G04 handoff semantics:

1. `result_id` remains the source Exploratory Result path identity.
2. `dataset_version_id / analysis_view_id` are derived from source Result lineage and are not request overrides.
3. canonical `AnalysisSpecification` is persisted as `status=DRAFT`.
4. incomplete target-family `family_spec` is allowed while DRAFT.
5. `Result --MOTIVATED--> AnalysisSpecification` semantic lineage is persisted.
6. handoff alone MUST NOT FIX the AnalysisSpecification.
7. handoff alone MUST NOT start an Execution.
8. presentation-only Explore state MUST NOT be persisted as AnalysisView scientific state.

The successful UI path MUST reach the existing browser-visible outcome expected after an exploratory-motivated handoff rather than exposing an `INVALID_REQUEST`.

## 5. Protected confirmatory behavior

Trial02 MUST preserve the existing public contract:

```text
analysis_mode=CONFIRMATORY
```

When a confirmatory handoff reuses the same immutable `dataset_version_id`, the system MUST continue to preserve the data necessary for the later reuse guard, including:

```text
EXPLORATORY_REUSE_SAME_DATA
```

non-blocking warning/evidence semantics.

The remediation MUST NOT solve the browser defect by:

- making `analysis_mode` optional in the backend;
- adding an implicit backend default that hides missing callers;
- removing `CONFIRMATORY`;
- weakening request validation;
- deleting same-data provenance/warning behavior.

The defect is the frontend caller not satisfying the already-frozen request contract.

## 6. Required correction B — browser E2E worker orchestration

The canonical G04 browser verification MUST be reproducible without depending on historical Compose state.

The repository-encoded browser test orchestration MUST guarantee, before browser scenarios require asynchronous execution, that:

1. `worker` is running;
2. `worker` is built from the current candidate source;
3. API and worker execute the same current semantic candidate;
4. a previously exited worker does not leave executions indefinitely `QUEUED`;
5. a stale worker image cannot process a current API execution plan.

The implementation mechanism may be the minimal repository-native solution, for example:

- Compose dependency wiring;
- browser-E2E bootstrap logic;
- equivalent deterministic test orchestration.

Manual operator-only startup such as:

```bash
docker compose ... up -d worker
```

MUST NOT be the sole condition required for the canonical browser command to pass.

Do not introduce a new serving subsystem or unrelated runtime orchestration framework.

## 7. Required regression coverage

Add automated regression coverage for the actual Trial01 gap.

### 7.1. Frontend caller contract

Automated regression MUST verify that the existing Explore Result transitions submit:

```text
Causal draft:
  target_family = CAUSAL
  analysis_mode = EXPLORATORY

Predictive draft:
  target_family = PREDICTIVE
  analysis_mode = EXPLORATORY
```

A test that checks only backend request models is insufficient.

At least one regression MUST exercise or inspect the actual frontend caller contract such that omission of `analysis_mode` fails the test.

### 7.2. Handoff result

Regression coverage MUST preserve:

```text
DRAFT creation
MOTIVATED lineage
no automatic FIX
no automatic Execution
selection-only AnalysisView handoff
```

### 7.3. Confirmatory behavior

Existing automated coverage for:

```text
analysis_mode = CONFIRMATORY
same immutable dataset reuse evidence/warning
```

MUST remain green.

### 7.4. Real browser regression

The canonical Chromium regression:

```bash
docker compose \
  -f compose.yaml \
  -f compose.e1a.yaml \
  -p ariadne-e1a \
  --profile e2e \
  run --build --rm \
  --entrypoint python \
  browser-e2e \
  tests/browser_e2e/run_enh_e3.py
```

MUST pass with repository-defined orchestration.

Its success MUST NOT depend on a worker that happened to be running from a previous manual session.

## 8. Protected G04 behavior

Preserve unrelated G04 semantics, including:

- six Exploratory Navigation Stages:
  - `profile`
  - `data-quality`
  - `distribution`
  - `relationships`
  - `comparison`
  - `findings`
- visualization remains a representation concern and does not introduce a new runtime Stage taxonomy;
- AnalysisView POST/PATCH/validate/fix use the common typed validator;
- existing filter operator/value semantics;
- `FILTER_TYPE_MISMATCH`;
- boolean-as-INTEGER rejection;
- NaN/Infinity REAL rejection;
- invalid datetime rejection;
- empty `IN` rejection;
- unknown source type rejection;
- AnalysisView handoff copies data-selection semantics only;
- Predictive existing fields/default semantics;
- common AnalysisSpecification validate/fix/revise behavior;
- cross-family lineage;
- Results/lineage/export behavior;
- legacy lifecycle shutdown protections.

Do not weaken/delete/skip/xfail existing tests.

Do not introduce:

- `Navigation Stage = Execution Stage`;
- persisted Navigation Stage runtime state;
- duplicate Family discriminator;
- LightGBM / DoWhy / EconML;
- D3 or `DEFERRED / FUTURE` requirements.

## 9. Expected change surfaces

Expected minimal production/test surfaces include:

```text
frontend/
tests/product/
tests/browser_e2e/        # only if required for deterministic regression/orchestration
compose.e1a.yaml           # if Compose dependency wiring is selected
```

Backend semantic changes under `src/` are not expected merely to make `analysis_mode` optional or defaulted.

If a backend production change is made, it MUST be justified by the frozen remediation semantics and MUST NOT weaken the exact request contract.

## 10. Mandatory verification

Run at minimum the G04 independent non-browser command sets that passed in Trial01, plus new remediation regression coverage.

Acceptance verification:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q \
  tests/product/test_enh_e5_g04_p01_exploratory_stage_mapping.py \
  tests/product/test_analysis_view_e3.py \
  tests/product/test_enh_e5_g04_p03_exploratory_boundary.py \
  tests/product/test_exploratory_contract_e3.py \
  tests/product/test_exploratory_api_worker_e2e_e3.py
```

Protected regression:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q \
  tests/product/test_exploratory_frontend_contract_e3.py \
  tests/product/test_analysis_specification_e3.py \
  tests/product/test_cross_analysis_lineage_e3.py \
  tests/product/test_results_lineage_export_e3.py \
  tests/product/test_enh_e3_api_worker_e2e.py \
  tests/product/test_enh_e4_g05_phase_b_exploratory_postgres.py \
  tests/product/test_enh_e4_g05_phase_d_d2_legacy_lifecycle_shutdown.py
```

Browser regression:

```bash
docker compose \
  -f compose.yaml \
  -f compose.e1a.yaml \
  -p ariadne-e1a \
  --profile e2e \
  run --build --rm \
  --entrypoint python \
  browser-e2e \
  tests/browser_e2e/run_enh_e3.py
```

Formatting:

```bash
git diff --check
```

All required checks MUST pass.

The browser evidence MUST demonstrate that:

```text
Explore execution reaches terminal success
-> Exploratory Result is saved
-> Predictive draft transition succeeds
-> downstream DRAFT is created
-> no INVALID_REQUEST for missing analysis_mode
```

## 11. New candidate invariant

Trial02 candidate MUST NOT equal:

```text
bd4092c21c5c7fac86bdcf36a87af53dfa2c0fab
```

Before `READY_FOR_TEST`:

```bash
git diff --name-only \
  bd4092c21c5c7fac86bdcf36a87af53dfa2c0fab..<FIXED_TRIAL_CANDIDATE_SHA> \
  -- src frontend tests pyproject.toml uv.lock alembic compose.yaml compose.e1a.yaml
```

The semantic diff MUST include:

- production correction under `frontend/`;
- automated regression correction/addition under `tests/`.

If browser orchestration is corrected through Compose, the diff SHOULD also include the relevant Compose file.

If the required production and regression diff is absent:

```text
BLOCKED_REMEDIATION_NOT_APPLIED
```

The previous failed candidate MUST NOT be resubmitted under Trial02.

## 12. Execution / handoff

Use only:

```text
fail_rework_coding_agent_prompt.md
GATE_ID=G04
TRIAL_NO=02
```

Do NOT run Trial02 P01/P02/P03 Work Package agents.

The FAIL Rework Coding Agent owns:

```text
implementation correction
-> regression tests
-> browser orchestration correction
-> implementation checkpoint
-> FIXED_TRIAL_CANDIDATE_SHA
-> canonical Completion Report
-> evidence commit/push
-> READY_FOR_TEST
```

Canonical Completion Report:

```text
docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/
20_implementation_reports/G04/Trial02/
E5-G04_02__implementation_completion.md
```

Trial01 package status reports, Completion Report, independent test reports, Gate Decision, and failure evidence remain immutable.
