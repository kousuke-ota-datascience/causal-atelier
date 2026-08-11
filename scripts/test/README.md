# Repository-managed PostgreSQL tests

The single supported entry point is:

```bash
scripts/test/run_product_postgres_tests.sh tests/product/test_postgres_contract.py
```

It builds a test-only Python 3.12 runner, starts the isolated `database_test`
service, waits for health, resets the `ariadne_test` database, runs only the
Product migration chain, and passes all remaining arguments to pytest. The
runner and database communicate through the Compose service name on
`ariadne-test-network`; no host loopback or docker gateway is used.

Examples:

```bash
scripts/test/run_product_postgres_tests.sh -m postgres tests/product/test_postgres_contract.py
scripts/test/run_product_postgres_tests.sh tests/product/test_postgres_contract.py::test_claim_next_is_atomic_across_concurrent_workers
```

Evidence is written under `test-results/postgres/` (or the directory named by
`ARIADNE_TEST_EVIDENCE_DIR`) as a `.txt` log and metadata file. It is generated
output and is not a commit artifact. The test DB volume may be reused, but its
contents are reset on every invocation. To stop and remove test resources:

```bash
docker compose -f compose.test.yaml -p ariadne-test down
```

This stack has a distinct volume and network and never touches the development
`database` service or `metadata-data` volume. Cold and warm starts use the same
command. If an Agent cannot access Docker, a Human Operator runs exactly the
same one command and hands the resulting evidence directory to the Auditor.
