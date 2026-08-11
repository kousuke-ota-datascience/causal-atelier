# E4-G08 Trial01 P03 — Final Integrated Verification Checkpoint

## 1. Identification

| Field | Value |
|---|---|
| Gate / Trial / Package | E4-G08 / 01 / P03 |
| Status | COMPLETE |
| Entry SHA | `c267729362441a9db7e2ae6e5ec68ad0fa578a92` |
| Checkpoint SHA | PENDING — this checkpoint is committed after creation |
| Product migration head | `20260809_product_0010` |
| TD-006 implementation-side state | `CLOSURE_CANDIDATE` |
| Next package | P04 — candidate freeze / completion |

P03 is implementation-side verification. It does not declare G08 PASS or formal `TD-006 CLOSED`.

## 2. AC Evidence Matrix

| AC | Result | Current-state evidence |
|---|---|---|
| AC-001 Clean Product bootstrap | PASS | Real PostgreSQL reset → `alembic_product.ini` Product chain → head `20260809_product_0010` → Product API `/health/ready` and DB-backed `/api/v1/projects` initialization/query passed. |
| AC-002 Three-family Golden Path | PASS | PostgreSQL canonical Result/Artifact round-trip plus Causal, Exploratory, and Predictive selections passed; each confirms canonical Execution / StageExecution / Result / Artifact ownership/persistence. |
| AC-003 Mutation + lineage | PASS | PostgreSQL retry/rerun/revise plus G06 authority-selection tests cover same-ID retry, new-ID rerun/revise, typed revision projection, canonical cancellation authority, typed structural lineage, GENERIC_ONLY semantic persistence, and derived closure/export. |
| AC-004 Final authority audit | PASS | Static/runtime/deployment/bootstrap guards prove canonical Product authority, Product-only bootstrap, GenericExecutor boundary, and no Product legacy dependency/new-write fallback. |
| AC-005 Shared science + zero debt candidate | PASS | Product scientific adapter and identification tests passed; P01/P02 inventory has two explicit `ARCHIVE` items and genuine active bounded transition = 0. |

## 3. AC-001 — Clean Bootstrap / Startup

### Fact

The final PostgreSQL runner performed, in order:

```text
reset Product test database
→ alembic -c alembic_product.ini upgrade head
→ alembic -c alembic_product.ini current
→ Product API startup/readiness and DB-backed request
```

The migration sequence reached only `20260809_product_0010`; the runner then passed the G08 API startup test and Product PostgreSQL contract.

### Evidence

- Test: `tests/product/test_enh_e4_g08_clean_bootstrap_postgres.py`
- Test: `tests/product/test_postgres_contract.py`
- PostgreSQL stdout/stderr: `/tmp/ariadne-g08-p03-pg-evidence/run-20260809T235914Z.txt`
- PostgreSQL metadata: `/tmp/ariadne-g08-p03-pg-evidence/run-20260809T235914Z.metadata.txt`

The G08-focused test is newly added because prior PostgreSQL tests proved migration/schema but did not directly perform a Product API initialization and DB-backed request after clean migration.

## 4. AC-002 — Three-family Golden Path

| Family | Execution | StageExecution | Result | Artifact | Authority | Evidence |
|---|---:|---:|---:|---:|---:|---|
| Causal | PASS | PASS | PASS | PASS | PASS | `test_enh_e4_g04_result_artifact_postgres.py`; `test_enh_e4_g05_phase_a_postgres.py`; Product/API worker protected test |
| Exploratory | PASS | PASS | PASS | PASS | PASS | `test_enh_e4_g05_phase_b_exploratory_postgres.py`; `test_enh_e4_g05_submission_convergence.py` |
| Predictive | PASS | PASS | PASS | PASS | PASS | `test_enh_e4_g05_phase_c_retry_postgres.py`; `test_enh_e4_g05_phase_c_rerun_postgres.py`; `test_enh_e4_g05_phase_c_revise_postgres.py` |

Interpretation: the selected current tests jointly observe all three Product families through canonical persistent output ownership. They are not merely prior Gate provenance.

## 5. AC-003 — Mutation and Lineage

| Semantics | Result | Evidence |
|---|---|---|
| Retry retains Execution identity | PASS | `test_enh_e4_g05_phase_c_retry_postgres.py` |
| Rerun creates new ID / `base_execution_id` / `RERUN` / typed `DERIVED_FROM` | PASS | `test_enh_e4_g05_phase_c_rerun_postgres.py`; G06 P06 local/PG selections |
| Revise creates new ID / `base_execution_id` / `REVISED` / preserved reason / typed `REVISED_FROM` | PASS | `test_enh_e4_g05_phase_c_revise_postgres.py`; G06 P06 local/PG selections |
| Cancel uses canonical Execution transition | PASS | `test_enh_e4_g05_phase_d_d3_global_authority_audit_postgres.py`; local global authority audit |
| Typed structural authority / GENERIC_ONLY semantic persistence / derived projection | PASS | G06 P01–P06 local and PostgreSQL selections, including P04/P05/P06 |

## 6. AC-004 — Final Authority Audit

### Positive authority model

| Authority | Result | Current evidence |
|---|---|---|
| Product lifecycle → canonical `Execution` | PASS | G02 canonical execution, G05 convergence, and G05 D3 authority audit |
| Stage lifecycle → `StageExecution` | PASS | G03 persistent-stage tests and PostgreSQL three-family selections |
| Output ownership → canonical `Result` / `Artifact` | PASS | G04 contract/PostgreSQL tests and G05 selections |
| Structural lineage → typed state; semantic lineage → GENERIC_ONLY persisted edge | PASS | G06 P01–P06 tests |
| Product bootstrap → Product migration chain | PASS | clean runner, PostgreSQL contract, G07 bootstrap guard |
| `GenericExecutor` → subordinate mechanism | PASS | G03 generic-executor boundary and G05 D3 authority audit |
| Retired legacy architecture → no Product active authority | PASS | architecture, G07 runtime/deployment/bootstrap, and P02 archive-boundary guards |

## 7. AC-005 — Shared Science and TD-006

### Facts

- `tests/scientific/test_product_adapters.py` and `tests/scientific/test_identification_e1a.py` passed in the protected local selection.
- P02 archived the Family ORM historical-data readers and revision-context fallback as explicit non-authoritative read projections.
- P01's remaining material candidates are resolved as `ARCHIVE`, `RETAIN_NON_AUTHORITY`, or `RETAIN_SHARED_CAPABILITY`; no candidate is unclassified.

### Interpretation

Implementation-side evidence supports `OPEN TRANSITION DEBT = 0` as a closure candidate. Independent Test alone can change TD-006 from `CLOSURE_CANDIDATE` to formally `CLOSED`.

## 8. Exact Verification Commands and Results

### Real PostgreSQL

```bash
ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g08-p03-pg-evidence \
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g08_clean_bootstrap_postgres.py \
  tests/product/test_postgres_contract.py \
  tests/product/test_enh_e4_g04_result_artifact_postgres.py \
  tests/product/test_enh_e4_g05_phase_a_postgres.py \
  tests/product/test_enh_e4_g05_phase_b_exploratory_postgres.py \
  tests/product/test_enh_e4_g05_phase_c_retry_postgres.py \
  tests/product/test_enh_e4_g05_phase_c_rerun_postgres.py \
  tests/product/test_enh_e4_g05_phase_c_revise_postgres.py \
  tests/product/test_enh_e4_g05_phase_d_d3_global_authority_audit_postgres.py \
  tests/product/test_enh_e4_g06_p01_authority_policy_postgres.py \
  tests/product/test_enh_e4_g06_p02_structural_writer_cutover_postgres.py \
  tests/product/test_enh_e4_g06_p03_generic_only_convergence_postgres.py \
  tests/product/test_enh_e4_g06_p04_typed_read_reconstruction_postgres.py \
  tests/product/test_enh_e4_g06_p05_projection_convergence_postgres.py \
  tests/product/test_enh_e4_g06_p06_negative_authority_postgres.py -q
```

Result: PASS — `23 passed`; runner metadata records `run_exit_code=0`, reset/migration/current all exit 0.

### Protected local regression

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q --disable-warnings \
  tests/product/test_enh_e4_g02_canonical_execution.py \
  tests/product/test_enh_e4_g03_generic_executor_boundary.py \
  tests/product/test_enh_e4_g03_persistent_stage_execution.py \
  tests/product/test_enh_e4_g04_result_artifact_contract.py \
  tests/product/test_enh_e4_g05_submission_convergence.py \
  tests/product/test_enh_e4_g05_phase_d_d3_global_authority_audit.py \
  tests/product/test_enh_e4_g06_p01_lineage_authority_policy.py \
  tests/product/test_enh_e4_g06_p02_structural_writer_cutover.py \
  tests/product/test_enh_e4_g06_p03_generic_only_convergence.py \
  tests/product/test_enh_e4_g06_p04_typed_read_reconstruction.py \
  tests/product/test_enh_e4_g06_p05_projection_convergence.py \
  tests/product/test_enh_e4_g06_p06_mutation_lineage.py \
  tests/product/test_architecture.py \
  tests/product/test_enh_e4_g07_p01_runtime_boundary.py \
  tests/product/test_enh_e4_g07_p02_bootstrap_boundary.py \
  tests/product/test_enh_e4_g07_p03_cli_boundary.py \
  tests/product/test_cli_contract.py \
  tests/product/test_api_worker_e2e.py \
  tests/scientific/test_product_adapters.py \
  tests/scientific/test_identification_e1a.py
```

Result: PASS — 108 collected; 106 passed and 2 expected PostgreSQL-only skips. The same selection was run twice successfully after the final PostgreSQL pass.

Additional checks:

```text
git diff --check: PASS
uv run alembic -c alembic_product.ini heads: 20260809_product_0010 (head)
```

## 9. Self-test Corrections

The new G08 startup test initially had two test-only defects: it used SQLAlchemy's password-masked string URL, then expected a response lacking the documented `next_cursor` field. Both were corrected in Trial01; no Product code failure was observed. The final clean reset/migration run above is the sole P03 PostgreSQL acceptance evidence.

## 10. Unknown and P04 Handoff

Material Unknown: `0`.

P04 must use this AC matrix, the P01 final TD-006 inventory, P02 closure candidate, exact commands above, and migration head `20260809_product_0010` to freeze one candidate. Remaining work is completion documentation and Independent Test handoff only.
