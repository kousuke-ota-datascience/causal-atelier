# ENH-E5 G04 Trial02 — Implementation Completion

- PROJECT_NAME: Ariadne
- ENHANCE_ID: ENH-E5
- GATE_ID: G04
- TRIAL_NO: 02
- Execution status: READY_FOR_TEST
- PREVIOUS_FAILED_CANDIDATE_SHA: `bd4092c21c5c7fac86bdcf36a87af53dfa2c0fab`
- FIXED_TRIAL_CANDIDATE_SHA: `564df2da67efa43c4455718b9b3d81f6d3e98c61`
- Blocker / remaining work: NONE

## Candidate identity and scope

`564df2da67efa43c4455718b9b3d81f6d3e98c61` is the Trial02 semantic
implementation checkpoint.  It is distinct from the Trial01 failed candidate.
The semantic diff from the Trial01 candidate includes the required production
correction under `frontend/` and regression coverage under `tests/`; it also
includes the selected Compose orchestration correction.

| Surface | Implemented correction |
| --- | --- |
| `frontend/app.js` | Exploratory Result downstream draft requests send `analysis_mode: "EXPLORATORY"` (with the selected research-context version when present); the existing backend-required mode remains required. |
| `compose.e1a.yaml` | Browser E2E service depends on a started worker, so the repository-defined `--build` run uses current candidate API/worker orchestration rather than an operator-started historical worker. |
| `tests/product/test_exploratory_frontend_contract_e3.py` | Locks the actual frontend caller payload for both Causal and Predictive drafts. |
| `tests/product/test_predictive_frontend_contract_e3.py` and `tests/browser_e2e/run_enh_e3.py` | Locks the active canonical lifecycle and canonical navigation synchronization used by the real-Chromium path. |

No backend request validation was relaxed and no implicit `analysis_mode` default
was introduced.

## Analysis View submit diagnostic (mechanically observed)

Evidence: `test-results/browser_e2e/enh-e3-evidence.json`, key
`analysis_view_submit_diagnostic`.

| Observation immediately before submit | Result |
| --- | --- |
| `#analysis-view-form.checkValidity()` | `true` |
| `#analysis-view-form :invalid` | `[]` (no invalid controls) |
| Named controls | `dataset_version_id`, `view_key`, `name`, and `spec` each had `validity.valid=true` and an empty `validationMessage` |
| Actual `dataset_version_id` | `f9577318-fb39-453d-9519-20342431432f` |
| `FormData` snapshot | `dataset_version_id`, `view_key=final_view`, `name=Final population`, and the typed `spec` JSON were present |

### Root-cause decision

- **Rejected hypotheses (evidence):** HTML native validation, a missing/invalid
  Analysis View control, and a missing `dataset_version_id` were rejected by
  the diagnostic above.  The successful evidence also records the Analysis
  View flow as `PASS`.
- **Adopted root cause (evidence):** the browser runner waited for retired
  analysis-family URLs after click, although the frontend navigates through the
  canonical navigation serializer.  The runner now synchronizes with the
  canonical active workspace/refresh state instead of a legacy URL alias.
- **Additional exact failure found after form validation was rejected:** the
  Predictive submit form was valid, but its frontend called the retired
  `/predictive/split-validations` endpoint, whose legacy shutdown rejects the
  request.  The frontend follows the existing canonical
  AnalysisSpecification -> validate/fix -> ExecutionPlan -> validate ->
  Execution lifecycle; the retirement assertion remains covered.

Thus no change was made on the unproven premise that HTML validation or
asynchronous form redraw blocked the Analysis View POST.

## Mandatory self-verification

| Check | Result |
| --- | --- |
| Acceptance verification command in Trial02 instruction §10 | `30 passed in 7.52s` |
| Protected regression command in Trial02 instruction §10 | `17 passed, 2 skipped in 17.85s` |
| Canonical Chromium command in Trial02 instruction §7.4/§10 | PASS; evidence status `PASS` (Chromium `151.0.7922.34`) |
| Browser handoff evidence | Explore terminal success, Exploratory Result saved, Predictive draft transition and downstream DRAFT succeeded; browser console evidence is empty (no `INVALID_REQUEST`) |
| `git diff --check` | success |
| Candidate semantic-diff invariant | satisfied: `frontend/app.js`, `compose.e1a.yaml`, `tests/browser_e2e/run_enh_e3.py`, `tests/product/test_exploratory_frontend_contract_e3.py`, and `tests/product/test_predictive_frontend_contract_e3.py` are present in the relevant candidate diff |

This is implementation-side self-verification only.  It does not declare a
Gate PASS / FAIL or promotion decision; those remain the Test Agent's scope.
