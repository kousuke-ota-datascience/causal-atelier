# 999 Gate Decision

- Gate: `G01`
- Trial: `01`
- Fixed Trial Candidate SHA: `f62e3e75ba474928d6f2ca886e9992375c6f16e5`
- Gate decision: `BLOCKED`

## Verification summary

The exact fixed candidate was verified from a clean isolated worktree. Static candidate audit passes `G01-AC01`, `G01-AC02`, `G01-AC05`, `G01-AC07`, and `G01-AC09`. The frozen Chromium integration journey could not start because the Compose migration dependency failed DNS resolution before API/frontend readiness.

## Blocking Acceptance Criteria

| AC | Result | Basis |
|---|---|---|
| G01-AC01 | PASS | Shared-shell native return button is present. |
| G01-AC02 | PASS | Handler pushes canonical collection route `/projects`. |
| G01-AC03 | BLOCKED | Destination rendering requires the unavailable browser integration environment. |
| G01-AC04 | BLOCKED | Direct-entry interaction requires the unavailable browser integration environment. |
| G01-AC05 | PASS | Handler has no `history.back()` origin dependency. |
| G01-AC06 | BLOCKED | Back/Forward determinism requires the unavailable browser integration environment. |
| G01-AC07 | PASS | Native button has accessible text name and is keyboard-focusable. |
| G01-AC08 | BLOCKED | Applicable Project local-navigation / Analysis launcher browser regression was not runnable. |
| G01-AC09 | PASS | Diff audit found no API/schema/backend/runtime semantic implementation change. |

## Protected regression

`tests/browser_e2e/run_enh_e7_project_integration.py` is the applicable protected regression but remains unexecuted because the required Compose browser harness did not bootstrap.

## Decision rationale

`PASS` is prohibited because blocking browser/integration criteria are unverified. `FAIL` is not justified: the observed failure is the migration container's pre-test DNS resolution failure, while the candidate has no change to the failing infrastructure layer. Gate 07 therefore requires `BLOCKED`.

## Next routing

Repair or stabilize the frozen Compose bootstrap environment, then rerun the frozen G01 browser command and the applicable protected browser regression against the same fixed candidate SHA. Do not create a remediation candidate unless a valid candidate product failure is observed.

> この文書がGateのcanonical final authorityである。
