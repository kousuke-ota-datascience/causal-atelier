# G6 Trial 004 Gate Decision

- Status: FAIL
- Tested implementation: `0c89989ac46603c7557664383e9a54e2443e4a7d`
- Handoff: `87732caae0eb3cf75b0a075ad56dd65aad86e8a6`
- Migration head: `20260807_product_0006`
- Test Agent source modification: NONE

## Item summary

| Item | Status |
|---:|:---|
| 001 | PASS |
| 002 | PASS |
| 003 | PASS |
| 004 | PASS |
| 005 | PASS |
| 006 | FAIL |
| 007 | PASS |
| 008 | PASS |
| 009 | PASS |
| 010 | PASS |
| 011 | PASS |
| 012 | PASS |
| 013 | PASS |

## Evidence

- Targeted G6 suite: `32 passed`.
- API worker E2E: `10 passed`.
- G1–G5 targeted regression: `65 passed`.
- PostgreSQL contract: `4 passed`; migration downgrade/re-upgrade preserved seeded result data.
- Scientific suite: `48 passed`.
- Full active pytest: `190 passed, 4 skipped`.
- Browser runner built and started successfully, but failed deterministically during `E2E-06-regression` when the results endpoint returned HTTP 404. The failure is recorded in `G6_004_006_e2e_01_08_browser.md`.

## Decision

**Fact:** G6-006 is a required Browser item and its runner exited non-zero after HTTP 404 while retrieving the newly completed predictive regression results.

**Judgment:** Under the 07b Gate rules, one required item FAIL makes the trial FAIL. The successful lower-cost and non-browser tests do not override this browser regression.

Therefore, G6 Trial 004 is **FAIL**.

## Next allowed action

Coding Agent may fix the G6-006 regression and request a new trial.
