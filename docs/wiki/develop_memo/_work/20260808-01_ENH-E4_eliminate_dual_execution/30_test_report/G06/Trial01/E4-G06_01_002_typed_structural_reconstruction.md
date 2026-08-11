# E4-G06 Trial01 — Test Item 002: Typed Structural Reconstruction

Result: PASS

## Facts

Command:

```text
scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g06_p04_typed_read_reconstruction_postgres.py -q
```

The command passed as part of the focused G06 PostgreSQL suite: `6 passed`; migration head was `20260809_product_0010`.

Observed assertions include:

- canonical `DatasetVersion --USED_INPUT--> Execution` and `AnalysisView --USED_INPUT--> Execution` are reconstructed as `TYPED_STRUCTURAL`;
- `Execution --GENERATED--> Result` and `Result --GENERATED--> Artifact` are reconstructed from canonical typed Product state;
- matching structural `LineageEdgeOrm` rows are absent (`0`);
- Product closure and predictive lineage reads expose the structural relations;
- canonical `Execution` is used for the read path, without requiring a FamilyExecution authority.

## Interpretation

AC-001 is independently satisfied: typed structural lineage remains visible while duplicate structural generic persistence is zero.

## Unknown / Unconfirmed

Coverage is representative rather than an exhaustive enumeration of every Product resource type.
