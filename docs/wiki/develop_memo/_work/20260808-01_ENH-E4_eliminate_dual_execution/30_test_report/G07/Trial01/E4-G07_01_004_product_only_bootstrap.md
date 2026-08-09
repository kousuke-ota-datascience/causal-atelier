# E4-G07 Trial01 — 004 Product-only Bootstrap

## Result

`PASS`

## Evidence

Commands:

```text
uv run alembic -c alembic_product.ini heads
20260809_product_0010 (head)

scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g07_p02_bootstrap_boundary.py tests/product/test_postgres_contract.py -q
reset_exit_code=0
migration_exit_code=0
migration_current_exit_code=0
7 passed, 2 warnings
```

Fresh PostgreSQL evidence is recorded by the runner under `/tmp/ariadne-g07-t01-bootstrap/` (`run-20260809T232021Z.txt` and metadata). The fresh database reset succeeded, Product migration succeeded, `alembic_version_product` was used at revision `20260809_product_0010`, and the G07 bootstrap/static contract plus PostgreSQL contract passed. The root `alembic.ini`/`migrations` chain is HISTORY_ONLY for Product bootstrap; no root migration authority was invoked.

## AC mapping

- AC-004: PASS — Product bootstrap uses `product_migrations` only.
- TD-005 bootstrap half: PASS.

## Facts / Interpretation / Unknown

- Fact: mandatory real PostgreSQL runner completed successfully.
- Interpretation: fresh Product bootstrap is Product-only.
- Unknown: Alembic emitted two pre-existing `prepend_sys_path` deprecation warnings; they did not affect revision or test outcomes.

