# E4-G06 Trial01 P04 Implementation Checkpoint Report

## Identification

| Field | Value |
|---|---|
| Gate | E4-G06 |
| Trial | 01 |
| Package | P04 |
| Package Status | COMPLETE |
| P04 Entry SHA | `04a4f58a40773b84af7c0fe194ae4c62204bd2d4` |
| P04 Implementation Checkpoint SHA | `c69e57efff74d567e3e1b0fc152a252faba1e2f7` |
| Product Migration Head | `20260809_product_0010` |
| Migration | NONE |
| TD-004 | OPEN |
| Gate Status | E4-G06 NOT_COMPLETE |
| Next Package | P05 |

## Changed Files

### Production

- `src/ariadne/product/application/product_closure_service.py`
- `src/ariadne/product/application/predictive_workflow_service.py`

### Tests

- `tests/product/test_enh_e4_g06_p04_typed_read_reconstruction.py`
- `tests/product/test_enh_e4_g06_p04_typed_read_reconstruction_postgres.py`

## Reconstructed Typed Relation Matrix

| Canonical source | Relation | Target | Read endpoint |
|---|---|---|---|
| `ExecutionOrm.dataset_version_id` | `DatasetVersion USED_INPUT Execution` | canonical Execution | project lineage; Predictive lineage |
| `ExecutionOrm.analysis_spec_json.analysis_view_id` | `AnalysisView USED_INPUT Execution` | canonical Execution | project lineage; Predictive lineage |
| `ExecutionOrm.input_result_id` | `Result USED_INPUT Execution` | canonical Execution | project lineage; Predictive lineage |
| `ResultOrm.execution_id` | `Execution GENERATED Result` | canonical Result | project lineage; Predictive lineage |
| `ArtifactOrm.result_id` | `Result GENERATED Artifact` | canonical Artifact | project lineage; Predictive lineage |
| `ExecutionOrm.base_execution_id` / `revision_kind` | `Execution DERIVED_FROM/REVISED_FROM Execution` | canonical Execution | project lineage; Predictive lineage |

The project projection uses canonical `ExecutionOrm` for all three Product analysis families. A read-only compatibility fallback remains for historical canonical rows whose revision identity predates the dedicated base/revision columns.

## Generic-only Merge and Zero-row Proof

- `ProductClosureService.project_lineage()` merges only persisted tuples classified `GENERIC_ONLY`; typed structural persisted rows are not read as generic authority.
- Canonical Predictive `list_lineage()` returns the deduplicated union of reconstructed typed edges and persisted `GENERIC_ONLY` edges connected to the requested execution/result/artifact IDs.
- The PostgreSQL P04 fixture persisted no `USED_INPUT` structural generic row for its canonical Predictive execution. It nevertheless observed DatasetVersion and AnalysisView inputs, Execution-to-Result, and Result-to-Artifact in both read projections.
- The same fixture persisted `Result MOTIVATED Execution` and verified that it remains visible as a policy-approved generic-only relation.

## Unapproved Relations

P04 does not reconstruct the P03-removed snapshot-only tuples:

- `ResearchContextVersion USED_INPUT Execution`
- `AnalysisSpecification USED_INPUT Execution`
- `ExecutionPlan USED_INPUT Execution`

No generic lineage rows are created by P04 reads.

## Verification Evidence

| Command | Exit | Passed | Failed | Evidence |
|---|---:|---:|---:|---|
| `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e4_g06_p04_typed_read_reconstruction.py tests/product/test_enh_e4_g06_p01_lineage_authority_policy.py tests/product/test_enh_e4_g06_p02_structural_writer_cutover.py tests/product/test_enh_e4_g06_p03_generic_only_convergence.py` | 0 | 34 | 0 | Local pytest output. |
| `scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g06_p04_typed_read_reconstruction_postgres.py -q` | 0 | 1 | 0 | `test-results/postgres/run-20260809T144435Z.metadata.txt` |
| `scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g06_p04_typed_read_reconstruction_postgres.py tests/product/test_enh_e4_g06_p02_structural_writer_cutover_postgres.py tests/product/test_enh_e4_g06_p03_generic_only_convergence_postgres.py tests/product/test_enh_e4_g05_phase_c_authority_audit_postgres.py tests/product/test_cross_analysis_lineage_e3.py -q` | 0 | 6 | 0 | `test-results/postgres/run-20260809T144606Z.metadata.txt` |
| `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run python -m compileall -q src/ariadne/product/application/product_closure_service.py src/ariadne/product/application/predictive_workflow_service.py tests/product/test_enh_e4_g06_p04_typed_read_reconstruction.py tests/product/test_enh_e4_g06_p04_typed_read_reconstruction_postgres.py` | 0 | N/A | 0 | Local compile verification. |
| `git diff --check` | 0 | N/A | 0 | Local diff verification. |

All listed PostgreSQL runs reset the database, applied migration `20260809_product_0010`, and recorded `run_exit_code=0`.

## Facts / Interpretation / Unknown

### Facts

- P01 authority classification is unchanged.
- P02/P03 regression tests pass after P04.
- The P04 implementation adds no migration and no generic lineage writer.

### Interpretation

P04 satisfies the typed read reconstruction acceptance boundary: structural lineage can be read from canonical typed state even with zero matching structural generic rows, and generic-only evidence remains visible alongside it.

### Unknown / Unconfirmed

- P05 source-class/closure/export projection and P06 mutation/negative-authority audit have not been executed.
- Retired-source removal remains G07 work.

## Residual Work

- P05: closure/export source-class projection.
- P06: mutation and negative-authority audit.
- G07: retired source boundary.
