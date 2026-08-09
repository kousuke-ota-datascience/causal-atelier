# Test PostgreSQL Infrastructure Independent Verification Result

## 1. Metadata

- Audit date: 2026-08-09
- Branch: `refactor/ariadne_mvp_e4`
- Tested commit: `ec80188cc8f9104a4239e1e7ef7bafc388d00889`
- Docker Compose project: `ariadne-test`

## 2. Implementation Commit

`d2e2187179358b4bd6ee10dbabc0c2b1d80bb99f` (`test: standardize isolated PostgreSQL infrastructure`).
The tested commit is its descendant and differs only by the standardization result-document update; infrastructure source is unchanged.

## 3. Evidence Commit

`ec80188cc8f9104a4239e1e7ef7bafc388d00889` is the fixed source/evidence reference for this audit. Raw execution evidence was generated at `/tmp/ariadne-audit-evidence/` and contains timestamped stdout/stderr and metadata files.

## 4. Change Boundary Audit

PASS. The implementation commit changes only `.dockerignore`, `Dockerfile.test`, `compose.test.yaml`, `scripts/test/*`, and the result document. No production source, Product migration, production Dockerfile/Compose, dependency lockfile, or G03 implementation changed.

## 5. Development Isolation

PASS. `database_test`, `ariadne-test-product-data`, and `ariadne-test-network` are distinct from development `database` and `metadata-data`. The test DSNs target `database_test:5432/ariadne_test`; reset refuses maintenance/missing database targets.

## 6. Test Runner Architecture

PASS. `Dockerfile.test` installs locked dev dependencies in a test-only image. The production runtime image is not modified. The host runner builds the image, starts the database service, and delegates reset, Product migration, and pytest to the container runner.

## 7. Docker Networking

PASS. Runner-to-database traffic uses the Compose service name on `ariadne-test-network`. No host loopback, Docker gateway, published database port, or machine-specific IP is used.

## 8. Cold Start

PASS. After `docker compose -f compose.test.yaml -p ariadne-test down`, the standard command recreated the network and database, reached healthy state, reset the database, migrated to `20260809_product_0007 (head)`, and ran the PostgreSQL contract successfully.

## 9. Warm Reuse

PASS. With `database_test` already running and healthy, the same standard command reused it and the atomic claim test passed.

## 10. Dirty DB Reset

PASS. A subsequent standard invocation against the prior run's persisted test state performed `DROP DATABASE ... WITH (FORCE)` and recreation, then migrated from clean state and passed all four PostgreSQL contract tests.

## 11. Product Migration

PASS. The runner invokes only `alembic -c alembic_product.ini upgrade head` and `current`. Observed head: `20260809_product_0007`. No root legacy migration was invoked.

## 12. PostgreSQL Contract Test

PASS. `tests/product/test_postgres_contract.py`: 4 passed, exit 0, with real PostgreSQL assertions and no skip.

## 13. Atomic Claim Test

PASS. `tests/product/test_postgres_contract.py::test_claim_next_is_atomic_across_concurrent_workers`: 1 passed, exit 0, using the standard runner and real PostgreSQL.

## 14. G02 Regression

PASS. `tests/product/test_enh_e4_g02_canonical_execution.py`: 5 passed, exit 0.

## 15. Failure Propagation

PASS. An invalid pytest node produced `pytest_exit_code=4` and `outer_exit_code=4`; the runner did not convert failure to zero.

## 16. Evidence Contract

PASS. Metadata records tested commit, timestamps, database service/image, Compose project, pytest command, exit code, and stdout/stderr path. Evidence files are written under the configurable evidence directory and are covered by the existing `test-results/` ignore rule.

## 17. Human Fallback Audit

PASS. `scripts/test/README.md` instructs the Human Operator to execute the same one repository-managed command. No manual `docker run`, network IP lookup, DSN export, migration, or pytest sequence is required.

## 18. Cleanup Audit

PASS. The documented `docker compose -f compose.test.yaml -p ariadne-test down` command stopped and removed only the test container/network. Development services and `metadata-data` are not referenced.

## 19. Repository Integrity

PASS. No source, test, migration, compose, Dockerfile, dependency, or `.gitignore` files were modified by this audit. Pre-existing worktree changes were preserved: the unrelated `deploy/.nfs000000000076202f00000088` deletion and the two operator prompt files remain unstaged/unmodified by the audit.

## 20. Audit Matrix

| ID | Status | Evidence |
|---|---|---|
| IA-001 | PASS | Implementation diff boundary |
| IA-002 | PASS | Compose/DSN/volume inspection |
| IA-003 | PASS | Test-only Dockerfile and frozen `uv.lock` install |
| IA-004 | PASS | `database_test` service route and named network |
| IA-005 | PASS | Cold-start standard runner, exit 0 |
| IA-006 | PASS | Warm-reuse standard runner, exit 0 |
| IA-007 | PASS | Re-run reset from persisted test state, exit 0 |
| IA-008 | PASS | Product migration head `20260809_product_0007` |
| IA-009 | PASS | Contract: 4 passed |
| IA-010 | PASS | Atomic claim: 1 passed |
| IA-011 | PASS | G02 regression: 5 passed |
| IA-012 | PASS | Invalid node propagated exit 4 |
| IA-013 | PASS | Timestamped metadata/raw evidence |
| IA-014 | PASS | README one-command fallback |
| IA-015 | PASS | Documented cleanup executed |

## 21. Remaining Risks

Docker daemon availability and host disk capacity remain environment prerequisites. The audit itself initially lacked Docker socket permission in the sandbox, then succeeded with approved Docker access; this is not a repository infrastructure defect.

## 22. Decision

`PASS_READY_FOR_G03`

G03 contract authoring may begin. G03 implementation was not started by this audit.
