# E4-G08 Trial01 — Item 007 Protected Final Regression

Result: **PASS**

## Local

Command: P03 protected selection, with `ARIADNE_PRODUCT_TEST_DATABASE_URL` unset so PostgreSQL-only nodes are skipped.

Result: `106 passed, 2 skipped` (one warning). The selection covers Execution identity/claim, StageExecution, Result/Artifact, three-family convergence, retry/rerun/revise, lineage authority, legacy/runtime/bootstrap boundary, API/worker, CLI, and shared science.

## PostgreSQL

The repository-managed G08 selection reset the Product database, applied Product migrations, reached `20260809_product_0010 (head)`, and passed `23` tests. Evidence: `/tmp/ariadne-g08-trial01-pg-evidence/`.

## Interpretation

Protected G02–G07 semantics are preserved on both local and real-PostgreSQL paths. The two local skips are intentional PostgreSQL-only nodes, covered by the PostgreSQL run.
