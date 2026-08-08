# G5 Trial 002 Test 004 — predictive_browser_e2e

- Gate: G5
- Trial: 002
- Test item: 004
- Status: BLOCKED
- Tested implementation commit: 4a83bb6860c895f00e4dfd7c9e7880105387373e
- Handoff report commit / path: 4ccbfbb196ba384aa362450666c00b4c936c58d7 / docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/G5_002_implementation_completion_report.md
- Branch: prototype/ariadne_mvp_e3
- Migration head: 20260807_product_0005
- Started at: 2026-08-07T11:38:34Z
- Finished at: 2026-08-07T11:38:54Z

## Purpose

Real ChromiumでPredictive workflow、deep link、reload/back、saved-result revisit、error renderingを検証する。

## Acceptance Criteria

deep link、reload、browser back、execution polling、saved result revisit、`UNKNOWN_PREDICTIVE_COLUMN` error rendering。

## Preconditions / Environment

- G4 Trial 003: PASS
- Current handoff HEAD: 4ccbfbb196ba384aa362450666c00b4c936c58d7
- Project `.venv` via `uv run`; Test Agent source/test/migration modification: NONE

## Commands Executed

~~~bash
docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a \
  --profile e2e run --build --rm --entrypoint python browser-e2e \
  tests/browser_e2e/run_enh_e3_predictive.py
sed -n '1,240p' .dockerignore
rg -n 'run_enh_e3_predictive' .dockerignore Dockerfile.browser-e2e
~~~

## Exact Result

- canonical runner exit code: 1
- Browser scenarios executed: 0
- passed: 0
- failed product assertions: 0
- duration: 20s
- failure phase: Docker image build
- error: `COPY ... tests/browser_e2e/run_enh_e3_predictive.py: not found`

## Log / Evidence

- `/tmp/g5_002_004_predictive_browser_e2e.log`
- Host runner exists.
- `.dockerignore` excludes `tests/browser_e2e/*` and re-includes only `run_enh_e1a.py`.
- `Dockerfile.browser-e2e` attempts to copy `run_enh_e3_predictive.py`.

## Findings

- product defect: indeterminate; browser product behavior was never reached
- test infrastructure issue: deterministic Docker build-context mismatch
- regression: indeterminate for Browser
- deviation: no retry because this is not a transient environment failure

## Decision Rationale

Instruction section 18 requires BLOCKED when broken test infrastructure prevents product-defect determination. Using an ad-hoc bind mount or stale image would bypass the canonical packaging contract, so no workaround was used.

## Source Modification by Test Agent

NONE

