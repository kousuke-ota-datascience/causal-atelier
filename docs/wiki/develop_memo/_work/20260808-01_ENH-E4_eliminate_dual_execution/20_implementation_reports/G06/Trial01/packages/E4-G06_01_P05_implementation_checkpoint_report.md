# E4-G06 Trial01 P05 Implementation Checkpoint Report

## Identification

| Field | Value |
|---|---|
| Gate | E4-G06 |
| Trial | 01 |
| Package | P05 |
| Package Status | COMPLETE |
| P05 Entry SHA | `e53da5fe1ac2112684908cd6f2082775b39ec7d8` |
| P05 Implementation Checkpoint SHA | `502592d7de7af10274d544c9778bbcd1347461d3` |
| Product Migration Head | `20260809_product_0010` |
| Migration | NONE |
| TD-004 | OPEN |
| Gate Status | E4-G06 NOT_COMPLETE |
| Next Package | P06 |

## Changed Files

- `src/ariadne/product/application/product_closure_service.py`
- `tests/product/test_enh_e4_g06_p05_projection_convergence.py`
- `tests/product/test_enh_e4_g06_p05_projection_convergence_postgres.py`
- `tests/product/test_results_lineage_export_e3.py`
- `tests/product/test_cross_analysis_lineage_e3.py`

## Projection Source-class Contract

| Projection input | `source_class` | Compatibility `explicit` |
|---|---|---|
| Canonical typed structural reconstruction | `TYPED_STRUCTURAL` | `False` |
| Persisted P01-approved generic-only edge | `GENERIC_ONLY` | `True` |

`result_lineage()` filters the graph without modifying edge records, so it preserves `source_class`. `create_export()` obtains `lineage_references` from the same result-closure projection and preserves the field in the `ariadne-export-manifest/1` manifest.

## Authority-drift Removal

Removed export-local `_synthetic_export_lineage()` use. Export no longer emits snapshot-derived:

- `ResearchContextVersion USED_INPUT Execution`
- `AnalysisSpecification USED_INPUT Execution`
- `ExecutionPlan USED_INPUT Execution`

No P05 method creates `LineageEdgeOrm`; export persists only its ExportBundle/manifest artifact.

## Verification Evidence

| Command | Exit | Passed | Failed | Evidence |
|---|---:|---:|---:|---|
| `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e4_g06_p05_projection_convergence.py tests/product/test_enh_e4_g06_p04_typed_read_reconstruction.py` | 0 | 4 | 0 | Local pytest output. |
| `scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g06_p05_projection_convergence_postgres.py -q` | 0 | 1 | 0 | `test-results/postgres/run-20260809T145633Z.metadata.txt` |
| `scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g06_p05_projection_convergence_postgres.py tests/product/test_enh_e4_g06_p04_typed_read_reconstruction_postgres.py tests/product/test_results_lineage_export_e3.py tests/product/test_cross_analysis_lineage_e3.py -q` | 0 | 8 | 0 | `test-results/postgres/run-20260809T145956Z.metadata.txt` |
| `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run python -m compileall -q src/ariadne/product/application/product_closure_service.py tests/product/test_enh_e4_g06_p05_projection_convergence.py tests/product/test_enh_e4_g06_p05_projection_convergence_postgres.py tests/product/test_results_lineage_export_e3.py tests/product/test_cross_analysis_lineage_e3.py` | 0 | N/A | 0 | Local compile verification. |
| `git diff --check` | 0 | N/A | 0 | Local diff verification. |

All listed PostgreSQL runs reset the database, applied migration `20260809_product_0010`, and recorded `run_exit_code=0`.

## Facts / Interpretation / Unknown

### Facts

- Project lineage labels every emitted edge with one of the two permitted authority source classes.
- The focused PostgreSQL test observes both source classes in project lineage, result closure, and export lineage references.
- The test observes `LineageEdgeOrm` count before/after export as unchanged.

### Interpretation

P05 satisfies the closure/export projection boundary. Authority remains canonical typed state or approved persisted generic-only state; no snapshot-derived export authority remains.

### Unknown / Unconfirmed

- P06 mutation-lineage/negative-authority audit has not run.
- Retired-source boundary remains G07 scope.

## Residual Work

- P06: mutation and negative-authority audit.
- G07: retired source boundary.

