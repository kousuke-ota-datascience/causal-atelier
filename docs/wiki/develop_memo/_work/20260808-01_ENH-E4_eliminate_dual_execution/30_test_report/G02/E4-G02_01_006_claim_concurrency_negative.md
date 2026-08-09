# E4-G02 Trial 01 — Test Item 006

- Tested implementation commit: `166e90cd1c2d0e523fb863795a88343403d8cc44`
- Current HEAD: `e3cbf212c859baf151ea2f1e9c917a7d0c9ba169`
- Result: **BLOCKED**

## Evidence

Exact mandatory PostgreSQL command:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_postgres_contract.py::test_claim_next_is_atomic_across_concurrent_workers
```

Exit code `0`, but result `1 skipped in 1.72s`: `ARIADNE_PRODUCT_TEST_DATABASE_URL` is not configured. `docker compose ps` was also checked; it returned no running containers. Therefore two-claimer atomicity, non-owner renewal/completion, terminal reclaim, and stale lease behavior are not proven against real PostgreSQL. Mock/domain evidence cannot substitute for this requirement.

Raw log: `/tmp/e4-g02-006-postgres.log`.

## Acceptance mapping

AC-005: **BLOCKED**; this is an environment block, not a defect finding.
