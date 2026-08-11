# E4-G02 Trial 01 — Gate Decision

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate / Trial: E4-G02 / 01
- Implementation commit: `166e90cd1c2d0e523fb863795a88343403d8cc44`
- Current HEAD: `e3cbf212c859baf151ea2f1e9c917a7d0c9ba169`
- Decision: **BLOCKED**

## Test Items

| Item | Result |
|---|---|
| 001 Commit/change boundary | PASS |
| 002 Canonical structure | PASS |
| 003 Cross-family claim/lifecycle | BLOCKED |
| 004 Mutation identity | PASS |
| 005 Old claimer negative audit | PASS |
| 006 Claim/concurrency negative | BLOCKED |
| 007 Product migration | BLOCKED |
| 008 Relevant regression | PASS |

## Acceptance Criteria

- AC-001: PASS
- AC-002: BLOCKED — required real PostgreSQL claim/lifecycle evidence unavailable
- AC-003: PASS
- AC-004: PASS
- AC-005: BLOCKED — required real PostgreSQL concurrency/ownership evidence unavailable

## Blocking condition

No isolated PostgreSQL environment was available. `test_claim_next_is_atomic_across_concurrent_workers` produced `1 skipped` because `ARIADNE_PRODUCT_TEST_DATABASE_URL` was unset; Docker had no running containers. Consequently the mandatory real-DB claim/concurrency and isolated migration upgrade checks cannot distinguish implementation correctness from environment absence. No source, test, migration, dependency, or report content was modified during testing.

## Transition Debt

`E4-TD-001` — Status: **OPEN**; Owner: ENH-E4 migration sequence; Exit Gate: E4-G05; Exit Criterion: no old Causal / Family lifecycle accepts new Product writes.

## Known limitations

The completion report's declared lack of real PostgreSQL evidence was independently reproduced. This decision does not advance to E4-G03 and does not authorize a code fix.

## Git evidence

The implementation target is fixed at the full SHA above. Commits after it are documentation/report-only; the known unrelated `.nfs` working-tree deletion was not changed or staged. Evidence files are under `30_test_report/`; raw logs are in `/tmp/e4-g02-*.log`.
