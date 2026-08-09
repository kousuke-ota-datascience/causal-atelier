# E4-G06 Trial01 — Test Item 004: Negative Authority Audit

Result: PASS

## Facts

Command:

```text
scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g06_p06_negative_authority_postgres.py -q
```

The audit passed. Its non-vacuous fixture persisted one generic row: `GENERIC_ONLY >= 1`, while persisted `TYPED_STRUCTURAL = 0` and unapproved persisted rows `= 0`. Every persisted row classified as `GENERIC_ONLY`.

Static audit command:

```text
rg -n "LineageEdgeOrm|assert_generic_lineage_allowed|classify_lineage_authority" src/ariadne/product
```

Classification:

- `ProductClosureService.create_lineage_link` and annotation writer: `ACTIVE_POLICY_GUARDED_GENERIC_ONLY`.
- `ExploratoryWorkspaceService._add_lineage`: `ACTIVE_POLICY_GUARDED_GENERIC_ONLY`.
- `ProductClosureService.project_lineage` and predictive lineage readers: `READ_ONLY`.
- `PredictiveSplitService` and old `PredictiveWorkflowService` lineage helpers: `RETIRED_UNREACHABLE`; their public mutation/lifecycle entry points raise `LegacyProductAuthorityDisabled` before the retained code.

Active unguarded Product generic writer: `0`.

## Interpretation

AC-003 is independently satisfied, including the final persisted-authority invariant.

## Unknown / Unconfirmed

The retained unreachable legacy helper bodies remain in source; their retirement is explicitly G07 scope and does not constitute an active authority path.
