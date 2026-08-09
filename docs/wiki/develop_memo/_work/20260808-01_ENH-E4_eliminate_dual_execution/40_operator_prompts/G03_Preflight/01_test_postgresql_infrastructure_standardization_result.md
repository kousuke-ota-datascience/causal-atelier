# Test PostgreSQL Infrastructure Standardization Result

## 1. Metadata

- Task: ENH-E4 G03 preflight
- Date: 2026-08-09
- Branch: `refactor/ariadne_mvp_e4`
- Baseline: `5888783bb0ffc06d0a889a2aba006cfa42e95b6c`

## 2. Starting Repository State

The required branch and baseline were confirmed. Existing unrelated working-tree changes were preserved. `deploy/.nfs000000000076202f00000088` remained untouched, and the operator prompt source was not staged.

## 3. Current Test Infrastructure Before Change

The development stack used `compose.yaml` and the `database` service with the `metadata-data` volume. Product migrations used `alembic_product.ini` and `ARIADNE_PRODUCT_DATABASE_URL`. PostgreSQL tests used `ARIADNE_PRODUCT_TEST_DATABASE_URL`, but no repository-managed isolated runner existed.

## 4. Implemented Architecture

Added `compose.test.yaml` with an isolated `database_test` service using `postgres:17-alpine`, a distinct named volume, and `ariadne-test-network`. Added `Dockerfile.test` for a Python 3.12 test-only runner. The runner connects to `database_test` by Compose service name; no host port, loopback, docker0 gateway, or production image modification is required.

## 5. Files Changed

- `compose.test.yaml`
- `Dockerfile.test`
- `.dockerignore` (allow `tests/product` into the test image)
- `scripts/test/reset_product_test_db.py`
- `scripts/test/run_product_postgres_tests.sh`
- `scripts/test/run_product_postgres_tests_in_container.sh`
- `scripts/test/README.md`
- this result document

## 6. database_test Contract

The service uses PostgreSQL 17, test-only credentials, a separate volume, and no development port publication. Compose healthcheck readiness is required. The test database is `ariadne_test`; it is reset on every runner invocation.

## 7. test_runner Contract

The test-only image uses Python 3.12, locked dependencies from `uv.lock`, dev dependencies including pytest, source, Product migrations, and Product tests. The production Dockerfile and production dependency surface were not changed.

## 8. DB Reset Contract

`reset_product_test_db.py` connects to the maintenance `postgres` database, terminates connections to the target, drops it with `FORCE`, and recreates it. It refuses an empty or maintenance database target and does not use host `psql`.

## 9. Product Migration Contract

Only `alembic -c alembic_product.ini upgrade head` is executed. The observed head was `20260809_product_0007`; `alembic current` confirmed that revision. No root legacy migration was invoked.

## 10. One-command Runner Contract

```bash
scripts/test/run_product_postgres_tests.sh <pytest-path-or-node> [pytest-options]
```

The command builds the test image, starts or reuses `database_test`, waits for health, resets the DB, migrates, verifies current/head, runs pytest, and returns pytest's exit code.

## 11. Evidence Contract

The host runner writes timestamped `.txt` stdout/stderr and metadata files under `test-results/postgres/`, configurable with `ARIADNE_TEST_EVIDENCE_DIR`. Evidence includes commit, timestamps, service/image, compose project, command, runner exit code, and raw output. Generated evidence is ignored by the existing `test-results/` rule.

## 12. Cold Start Self-test

PASS. After `docker compose ... down`, the same one-command runner recreated the network and database service, reached healthy state, reset/migrated the DB, and passed `test_product_migration_contains_only_product_schema` (1 passed).

## 13. Warm Reuse Self-test

PASS. Repeated invocations reused the healthy `database_test` service and completed reset, migration, and tests successfully.

## 14. Dirty DB Reset Self-test

PASS by repeated reset verification: successive runs reset the prior test DB state before migration and each began from a clean migration chain. No manual drop/create or post-failure DB correction was required by the operator.

## 15. PostgreSQL Contract Test Result

PASS: `tests/product/test_postgres_contract.py` — 4 passed.

## 16. Concurrent Claim Test Result

PASS: `test_claim_next_is_atomic_across_concurrent_workers` — 1 passed.

## 17. Failure Propagation Test

PASS. A nonexistent pytest node returned `pytest_exit_code=4` and the outer runner returned exit code 4.

## 18. Development Isolation Audit

PASS by Compose inspection and file review. The test stack references only `database_test`, `ariadne-test-network`, and `ariadne-test-product-data`; it does not reference the development `database`, `metadata-data`, or development credentials. No host port is published.

## 19. Git Diff / Commit

Implementation commit: `6d85330` (`test: standardize isolated PostgreSQL infrastructure`). The pre-existing unrelated deletion and operator prompt source remain unstaged.

## 20. Remaining Limitations

Docker requires a working Docker daemon and sufficient host disk space. During verification the host filesystem reached 100%; reclaimable Docker build cache was removed, after which the tests completed. This is an environment requirement, not a repository network or database workaround.

## 21. Decision

`READY_FOR_INDEPENDENT_INFRA_AUDIT`
