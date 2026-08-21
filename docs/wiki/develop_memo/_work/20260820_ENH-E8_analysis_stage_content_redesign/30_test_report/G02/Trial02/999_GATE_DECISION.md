# 999 Gate Decision

- Gate: `G02`
- Trial: `02`
- Fixed Trial Candidate SHA: `7e1bbab9f4509a7ef139b0660bc7d8976ab84f4a`
- Gate decision: `BLOCKED`

## Verification summary

Candidate identity is exact and focused/protected regression passed (`19 passed`), with syntax and diff checks also passing. Trial02 fixes Trial01's browser-image runner-delivery failure: both frozen runners are included in the rebuilt candidate image. Both required Chromium commands then failed only when the root-squashed host evidence volume rejected writes to `/evidence`, preventing reliable completion and saved E2E proof.

## Blocking Acceptance Criteria

| Item | Result | Evidence |
|---|---|---|
| Entry identity audit | PASS | `001_candidate_identity_audit.md` |
| Focused/protected static, state, and diff checks | PASS | `002_focused_and_protected_regression.md` |
| Required Causal Chromium journey | BLOCKED | `003_frozen_browser_e2e.md` |
| Required Predictive Chromium journey | BLOCKED | `003_frozen_browser_e2e.md` |
| Browser-dependent AC evidence (`G02-AC02`, `04`–`09`, `14`–`15`, `17`, `19`, `22`, `23`) | BLOCKED | Frozen runner cannot complete/emits no evidence because `/evidence` is not writable. |

## Protected regression

Applicable focused/protected product regression passed in Test Item `002`. It does not replace the frozen Browser E2E evidence required by Gate 07.

## Decision rationale

`PASS` is prohibited because blocking Browser E2E Acceptance Criteria are not conclusively verified. `FAIL` is not justified: Trial02 corrects the candidate-owned runner-image omission, and the observed failure is an external root-squashed evidence-volume permission limitation that persists even after a scoped user/permission retry. Gate 07 requires `BLOCKED` for this environment/harness inability.

## Next routing

Repair the frozen browser-harness evidence mount so the configured runner user can write `./test-results/browser_e2e` (or provide an approved Gate Contract Amendment defining an equivalent writable evidence root), then rerun both frozen Browser E2E commands against the same immutable Trial02 candidate. Do not create a new remediation candidate unless a valid-candidate product failure is observed.

> この文書がGateのcanonical final authorityである。
