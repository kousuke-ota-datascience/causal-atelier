# E4-G06 Trial01 — Test Item 003: Generic-only Policy

Result: PASS

## Facts

Commands:

```text
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e4_g06_p01_lineage_authority_policy.py
scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g06_p01_authority_policy_postgres.py tests/product/test_enh_e4_g06_p03_generic_only_convergence_postgres.py -q
```

The local policy test passed (`22 passed`), and the PostgreSQL authority/convergence tests passed (`6 passed` within the G06 focused suite).

Direct source inspection confirmed `classify_lineage_authority` uses `(source_type, relation_type, target_type)` and returns closed-by-default `None` for unknown tuples. `Execution DERIVED_FROM Execution` is `TYPED_STRUCTURAL`; `Artifact DERIVED_FROM Artifact` is `GENERIC_ONLY`. `assert_generic_lineage_allowed` rejects typed and unknown tuples. Active API writers also validate endpoint existence and project boundary before persistence.

## Interpretation

AC-002 is independently satisfied. Relation name alone does not select persistence authority.

## Unknown / Unconfirmed

No material unknown for the required policy tuples.
