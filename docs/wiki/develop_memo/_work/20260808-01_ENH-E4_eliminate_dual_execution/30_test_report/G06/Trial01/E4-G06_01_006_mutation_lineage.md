# E4-G06 Trial01 — Test Item 006: Mutation Lineage

Result: PASS

## Facts

Commands:

```text
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e4_g06_p06_mutation_lineage.py
scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g06_p06_negative_authority_postgres.py tests/product/test_enh_e4_g05_phase_c_rerun_postgres.py tests/product/test_enh_e4_g05_phase_c_revise_postgres.py -q
```

Local mutation tests passed (`2 passed`); the PostgreSQL mutation run passed (`3 passed`). Observed behavior: retry retained the same Execution ID and created no new Execution or lineage authority; rerun created a new Execution with `base_execution_id` and `RERUN`, and revise created a new Execution with `base_execution_id`, `REVISED`, and preserved `change_reason`. `DERIVED_FROM` and `REVISED_FROM` were returned as `TYPED_STRUCTURAL`, with no structural generic duplicate.

## Interpretation

AC-005 is independently satisfied.

## Unknown / Unconfirmed

No material unknown for retry/rerun/revise semantics.
