# E4-G08 Trial01 P04 — Gate Completion / Candidate Freeze Checkpoint

## Identification

| Field | Value |
|---|---|
| Gate / Trial / Package | E4-G08 / 01 / P04 |
| Status | COMPLETE |
| P04 entry SHA | `a6c3211d9873632c6e8a19d6c8db71a33d4bb6ef` |
| Fixed implementation/test candidate | `a6c3211d9873632c6e8a19d6c8db71a33d4bb6ef` |
| Product migration head | `20260809_product_0010` |
| Independent Test contract SHA | `bd2386e1f4df93c387422f38123ef5193d86832a` |
| Contract ancestor proof | PASS — `git merge-base --is-ancestor …` exit 0 |
| Implementation-side Gate state | `READY_FOR_TEST` |
| TD-006 | `CLOSURE_CANDIDATE` |

This checkpoint does not declare formal G08 PASS or `TD-006 CLOSED`.

## P01–P04 Summary

| Package | Status | Material output |
|---|---|---|
| P01 | COMPLETE | Eight material candidates classified; genuine TD-006 set fixed to two historical-read projections. |
| P02 | COMPLETE | Both genuine items explicitly archived; genuine active bounded transition = 0. |
| P03 | COMPLETE | AC-001–005 implementation-side evidence matrix; PostgreSQL 23-pass and protected local selection. |
| P04 | COMPLETE | Final verification on fixed candidate, hygiene, contract identity/ancestor proof, completion handoff. |

## Final Verification

| Selection | Result | Evidence |
|---|---|---|
| Real PostgreSQL clean reset → Product migration → current → integrated AC selection | PASS — 23 passed | `/tmp/ariadne-g08-p04-pg-evidence/run-20260810T000611Z.txt`; metadata counterpart records reset/migration/current and `run_exit_code=0` at candidate SHA `a6c3211…` |
| Protected local regression | PASS — 108 collected, 106 passed, 2 expected PostgreSQL-only skips | P03 exact selected test paths rerun before freeze |
| `git diff --check` | PASS | No diff/check errors before report creation |
| `git status --short` | PASS | Clean candidate worktree before report creation |
| Product migration head | PASS — `20260809_product_0010` | `uv run alembic -c alembic_product.ini heads` |

The PostgreSQL selection is the exact P03 AC selection, including `test_enh_e4_g08_clean_bootstrap_postgres.py`, Product migration/constraint, three-family output, mutation, global authority, and G06 lineage nodes. The protected local selection is the exact P03 local authority/lifecycle/shared-science selection.

## Completion Conditions

| Condition | Result | Basis |
|---|---|---|
| P01–P04 COMPLETE | PASS | Package checkpoints |
| AC-001 clean bootstrap + startup | PASS | P03/P04 PostgreSQL selection |
| AC-002 three-family lifecycle | PASS | P03/P04 three-family evidence matrix |
| AC-003 mutation + lineage | PASS | P03/P04 mutation and G06 selections |
| AC-004 final authority audit | PASS | P03/P04 G02/G03/G05/G07 architecture/authority selections |
| AC-005 shared science + zero-debt candidate | PASS | P01/P02 disposition and P03/P04 shared-science selection |
| Genuine active bounded transition = 0 | PASS | Two genuine TD-006 items are explicit ARCHIVE read projections |
| Material Unknown = 0 | PASS | P01–P03 checkpoints |
| One fixed candidate SHA | PASS | `a6c3211…` |
| Test contract SHA + ancestor proof | PASS | `bd2386e…` is candidate ancestor (exit 0) |

## Handoff

Independent Test input is:

```text
fixed candidate: a6c3211d9873632c6e8a19d6c8db71a33d4bb6ef
test contract:   bd2386e1f4df93c387422f38123ef5193d86832a
migration head:  20260809_product_0010
P01–P03 checkpoints and this P04 checkpoint
G08 implementation completion report
```

After candidate freeze, only documentation/report commits may follow. They are not part of the fixed candidate and must be distinguished by Independent Test.
