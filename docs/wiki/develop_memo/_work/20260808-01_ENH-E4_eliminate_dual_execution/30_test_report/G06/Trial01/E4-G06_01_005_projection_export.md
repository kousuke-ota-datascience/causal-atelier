# E4-G06 Trial01 — Test Item 005: Projection / Export

Result: PASS

## Facts

Command:

```text
scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g06_p05_projection_convergence_postgres.py -q
```

The command passed as part of the focused G06 PostgreSQL suite (`6 passed`). The test observed `TYPED_STRUCTURAL` for reconstructed canonical edges and `GENERIC_ONLY` for persisted approved generic edges in `project_lineage`, `result_lineage`, and exported manifest lineage references.

The test compared `LineageEdgeOrm` count before and after closure/export and required equality. It also rejected resurrection of `ResearchContextVersion`, `AnalysisSpecification`, or `ExecutionPlan USED_INPUT Execution` references. Direct inspection showed export delegates to `result_lineage` and does not write synthetic lineage.

## Interpretation

AC-004 is independently satisfied: projection/export preserves source class and is not lineage authority.

## Unknown / Unconfirmed

No material unknown for the required projection/export contract.
