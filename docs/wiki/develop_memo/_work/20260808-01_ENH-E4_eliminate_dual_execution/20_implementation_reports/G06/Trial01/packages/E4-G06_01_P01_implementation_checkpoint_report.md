# E4-G06 Trial01 P01 Implementation Checkpoint Report

## Identification

| Field | Value |
|---|---|
| Gate ID | E4-G06 |
| Trial ID | 01 |
| Package ID | P01 |
| Package Status | COMPLETE |
| G06 Architecture Baseline | `aae491519472f87bfbda88069eb1e65a858a9fcc` |
| P01 Entry SHA | `aae491519472f87bfbda88069eb1e65a858a9fcc` |
| P01 Implementation Checkpoint SHA | `ad982f55b73e9602ba7430f6a4820c1bd96b009d` |
| Product Migration Head | `20260809_product_0010` |
| Migration | NONE |
| TD-004 | OPEN |
| Gate Status | E4-G06 NOT_COMPLETE |
| Next Package | P02 — Structural writer cutover |

## Scope

### Purpose

Establish a central Product lineage authority policy and connect the manual generic writer, `ProductClosureService.create_lineage_link()`, to a closed-by-default generic-only admission guard.

### Changed Production Files

- `src/ariadne/product/domain/lineage.py`
- `src/ariadne/product/application/product_closure_service.py`

### Changed Test Files

- `tests/product/test_enh_e4_g06_p01_lineage_authority_policy.py`
- `tests/product/test_enh_e4_g06_p01_authority_policy_postgres.py`

### Explicit Out of Scope

- Causal, Exploratory, and Predictive structural writer cutover (P02).
- Convergence of all direct generic-only writers, including annotation writers (P03).
- Typed read reconstruction (P04), closure/export projection changes (P05), and mutation audit (P06).
- Migration, legacy source retirement, TD-004 closure, E4-G06 PASS, and READY_FOR_TEST.

## Implementation Facts

### Authority Policy

`LineageAuthority` now defines `TYPED_STRUCTURAL`, `GENERIC_ONLY`, `PROJECTION_ONLY`, and `OUT_OF_SCOPE`. `classify_lineage_authority(source_type, relation_type, target_type)` is the single pure semantic classifier. It returns `None` for an unknown or unapproved tuple.

`assert_generic_lineage_allowed(...)` permits only `GENERIC_ONLY`; it rejects typed structural and unapproved tuples with the existing `InvalidSchema` taxonomy.

The syntactic relation vocabulary is centralized as `LINEAGE_RELATION_TYPES`. It includes the formal vocabulary additions `EVIDENCE_FOR`, `DOCUMENTS`, and `SUMMARIZES`, but syntactic recognition is not generic-write admission.

`ProductClosureService.create_lineage_link()` retains role and endpoint/project checks before calling the central admission guard and before constructing `LineageEdgeOrm`.

### Formal Relation Vocabulary Reconciliation

| Semantic tuple | Classification |
|---|---|
| `Execution --GENERATED--> Result` | TYPED_STRUCTURAL |
| `Result --GENERATED--> Artifact` | TYPED_STRUCTURAL |
| `DatasetVersion/AnalysisView/Result --USED_INPUT--> Execution` | TYPED_STRUCTURAL |
| `Result --DERIVED_FROM--> GraphVersion` | TYPED_STRUCTURAL |
| `Artifact --DERIVED_FROM--> DatasetVersion` | TYPED_STRUCTURAL |
| `Execution --DERIVED_FROM/REVISED_FROM--> Execution` | TYPED_STRUCTURAL |
| `Artifact --DERIVED_FROM--> Artifact` | GENERIC_ONLY |
| `Result --SUMMARIZES--> Result/Artifact` | GENERIC_ONLY |
| approved `Result/Artifact --DOCUMENTS/SUPPORTED_BY/EVIDENCE_FOR--> Product resource` | GENERIC_ONLY |
| approved manual `Result --MOTIVATED--> Execution/AnalysisSpecification` | GENERIC_ONLY |
| approved annotation decision `SELECTED/REJECTED --> Annotation` tuples | GENERIC_ONLY |

### Authority Assertions

| Assertion | Result |
|---|---|
| Structural generic negative write | PASS — `Execution --GENERATED--> Result` raised `InvalidSchema`; matching `product_lineage_edge` row count was `0`; the canonical Result owner was unchanged. |
| Generic-only positive write | PASS — `Artifact --DERIVED_FROM--> Artifact` persisted exactly one row and preserved `{"stage": "model-card"}` evidence. |
| Unknown tuple negative write | PASS — recognized `DERIVED_FROM` with `Artifact --> Result` raised `InvalidSchema`; matching row count was `0`. |
| Same relation, different authority | PASS — `Execution --DERIVED_FROM--> Execution` is TYPED_STRUCTURAL and `Artifact --DERIVED_FROM--> Artifact` is GENERIC_ONLY. |
| Project-boundary regression | PASS. |
| Existing manual semantic-link regression | PASS — existing `Result --MOTIVATED--> Execution/AnalysisSpecification` requests remain accepted. |

## Verification Evidence

| Command | Exit | Passed | Failed | Skipped | Evidence |
|---|---:|---:|---:|---:|---|
| `UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run pytest -q tests/product/test_enh_e4_g06_p01_lineage_authority_policy.py` | 0 | 22 | 0 | 0 | Local pytest output; no PostgreSQL evidence directory. |
| `scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g06_p01_authority_policy_postgres.py -q` | 0 | 1 | 0 | 0 | `test-results/postgres/run-20260809T134627Z.metadata.txt`; stdout/stderr: `test-results/postgres/run-20260809T134627Z.txt` |
| `scripts/test/run_product_postgres_tests.sh tests/product/test_cross_analysis_lineage_e3.py::test_explicit_lineage_link_rejects_cross_project_resources -q` | 0 | 1 | 0 | 0 | `test-results/postgres/run-20260809T134650Z.metadata.txt`; stdout/stderr: `test-results/postgres/run-20260809T134650Z.txt` |
| `scripts/test/run_product_postgres_tests.sh tests/product/test_cross_analysis_lineage_e3.py::test_project_lineage_combines_families_and_explicit_relations -q` | 0 | 1 | 0 | 0 | `test-results/postgres/run-20260809T134724Z.metadata.txt`; stdout/stderr: `test-results/postgres/run-20260809T134724Z.txt` |
| `UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run python -m compileall -q src/ariadne/product/domain/lineage.py src/ariadne/product/application/product_closure_service.py tests/product/test_enh_e4_g06_p01_lineage_authority_policy.py tests/product/test_enh_e4_g06_p01_authority_policy_postgres.py` | 0 | N/A | 0 | 0 | Local compile verification; no PostgreSQL evidence directory. |
| `git diff --check` | 0 | N/A | 0 | 0 | Local diff verification; no PostgreSQL evidence directory. |

The standard PostgreSQL runner reset the test database, migrated to `20260809_product_0010`, and reported `pytest_exit_code=0` for every PostgreSQL command above.

## Residual Writer Inventory

### P02 Structural Writers

- `src/ariadne/product/application/predictive_split_service.py::_lineage()` writes `DatasetVersion/AnalysisView --USED_INPUT--> Execution` and `Execution --GENERATED--> Artifact` directly to `LineageEdgeOrm`.
- `src/ariadne/product/application/predictive_workflow_service.py::_lineage()` writes structural `USED_INPUT`, `GENERATED`, and execution mutation tuples directly to `LineageEdgeOrm`.
- `src/ariadne/product/application/exploratory_service.py::_add_lineage()` writes structural `USED_INPUT` and `GENERATED` tuples directly to `LineageEdgeOrm`.

### P03 Generic-only Writers

- `src/ariadne/product/application/predictive_workflow_service.py::_lineage()` writes `EVIDENCE_FOR`, `DOCUMENTS`, `SUMMARIZES`, and `Artifact --DERIVED_FROM--> Artifact` directly.
- `src/ariadne/product/application/exploratory_service.py::_add_lineage()` writes `Result --MOTIVATED--> AnalysisSpecificationDraft` directly.
- `src/ariadne/product/application/product_closure_service.py::create_annotation()` writes `SELECTED/REJECTED` decision edges directly.

## Protected-Gate Impact

No G02–G05 aggregate, lifecycle, Result, Artifact, or migration implementation was changed. The P01 service integration preserves role, endpoint existence, project-boundary, self-edge, and duplicate/idempotent processing order; existing cross-project and manual-link PostgreSQL regressions passed.

## Facts, Interpretation, Unknown / Unconfirmed

### Facts

- The central policy is tuple-based and denies unapproved tuples by default.
- The manual generic writer cannot persist structural semantic relations after this checkpoint.
- Direct workflow and annotation `LineageEdgeOrm` writers remain in source.

### Interpretation

- P01 satisfies the policy-foundation portion of AC-002 and provides the admission guard required to support AC-003.
- Remaining direct writers are intentionally deferred to P02/P03 and therefore do not establish gate-wide structural dual-write removal.

### Unknown / Unconfirmed

- Gate-wide structural writer removal, typed read reconstruction, projection source classification, and mutation semantics have not been verified in P01.
- P01 does not classify the eventual P02/P03 cutover as complete and does not close TD-004.

## Working Tree at Report Creation

```text
?? docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/10_enhance_instruction/G06/
?? docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G06/
```
-----
# Addendum

## Process deviation

P01 implementation began from aae4915... while the G06 P00/P01
instruction documents were present in the working tree but had not yet
been committed.

This deviated from the P01 entry-SHA rule requiring P00 to be committed
before package execution.

The deviation did not change the fixed G06 architecture baseline or the
P01 implementation checkpoint identity.

P02 and subsequent packages must start only after their governing
instruction artifacts are committed.