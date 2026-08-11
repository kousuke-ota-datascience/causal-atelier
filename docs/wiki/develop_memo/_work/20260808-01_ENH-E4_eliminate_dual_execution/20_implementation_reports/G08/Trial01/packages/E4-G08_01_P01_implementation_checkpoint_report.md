# E4-G08 Trial01 P01 — TD-006 Inventory / Closure Decision Checkpoint

## 1. Identification

| Field | Value |
|---|---|
| Gate / Trial / Package | E4-G08 / 01 / P01 |
| Status | COMPLETE |
| Entry branch | `refactor/ariadne_mvp_e4` |
| Entry SHA | `5edf48a2a2fb38aa8bb3bdfb76373e223b1bf7be` |
| Checkpoint SHA | PENDING — this checkpoint is committed after creation |
| Entry working tree | G08 instruction directory was untracked; no tracked-file modification was present in `git status --short` |
| Product migration head | `20260809_product_0010` |
| TD-006 state | OPEN — P01 does not close transition debt |
| P02 input | TD-006-ITEM-01 and TD-006-ITEM-02 archive actions below |

## 2. Facts, interpretation, and scope

### Facts

- `UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run alembic -c alembic_product.ini heads` returned the sole Product head `20260809_product_0010`.
- Product/API/worker and retained shared-science package roots have no transitive import path to `ariadne.legacy`; the deployment boundary excludes `src/ariadne/legacy/**` from the wheel and `src/ariadne/legacy` from Docker context.
- Repository-managed Product bootstrap uses `alembic_product.ini` and `product_migrations`; the root `alembic.ini` / `migrations` surface is not an active Product bootstrap surface.
- The Product runtime still has deliberate historical read contracts: legacy snapshot-schema validation, Family ORM historical-data readers, and a pre-dedicated-column revision-context lineage projection.
- Product runtime wiring injects `ExecutionService` into exploratory, predictive, and split services. Guard tests establish that absent canonical lifecycle DI rejects mutation before session access, and a canonical lookup miss does not fall back to a Family lifecycle write.

### Interpretation

`TD-006` is not the physical presence of every pre-E4 file or the word `legacy`. Its actual bounded scope is the two historical-read compatibility projections below. Both have live readers but no active new-write/lifecycle authority. They require archival status to be made explicit in P02; they must not be deleted while their historical-data consumers remain.

### Unknown

None material to classification. P01 did not inspect production database contents; whether a particular deployment contains historical rows is not required to classify the repository contract and is not asserted here.

## 3. Material TD-006 Inventory

| Surface / path | Current consumer | Runtime reachable? | Deployment reachable? | Bootstrap reachable? | Persistent authority? | New-write authority? | Compatibility consumed? | Shared capability? | Temporary transition? | Classification | P02 action | Evidence |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| `src/ariadne/legacy/` | No Product consumer; only archived legacy tests/reference source | no | no | no | no | no | no | no | no | ARCHIVE | No production change; record as retired historical source, not TD-006 active scope | `test_enh_e4_g07_p01_runtime_boundary.py`; `pyproject.toml`; `.dockerignore`; G07 decision |
| Root `alembic.ini` / `migrations/` | Historical migration history only | no | no | no | no | no | no | no | no | ARCHIVE | No production change; retain as non-active history | `test_enh_e4_g07_p02_bootstrap_boundary.py`; `alembic_product.ini`; G07 P02 evidence |
| `ariadne.causal`, `ariadne.preprocessing`, `ariadne.shared`, `ariadne.scientific` | Product scientific adapters and standalone scientific utilities | yes | indirectly, as packaged dependencies | no | no | no | no | yes | no | RETAIN_SHARED_CAPABILITY | None | G07 P01 import-graph guard; `scientific_core.py`; CLI contracts |
| `pyproject.toml` scientific CLI entries and `ariadne.interfaces.cli.*` | Five local scientific/file/manifest utilities | yes | no | no | no | no | no | yes | no | RETAIN_SHARED_CAPABILITY | None | `test_enh_e4_g07_p03_cli_boundary.py`; `test_cli_contract.py` |
| `LEGACY_SNAPSHOT_SCHEMA_VERSION = legacy-product-snapshot/1` and `ck_product_execution_input_by_operation` exception | `Execution.validate_input_contract`, PostgreSQL schema constraint, historical `product_execution` rows | yes | yes | yes, as a Product schema constraint | no | no | yes | no | no | RETAIN_NON_AUTHORITY | None; preserve bounded historical input validation | `execution.py`; `orm_models.py`; `test_enh_e1_contract.py`; `test_postgres_contract.py` |
| Family ORM historical-data readers: `product_family_execution`, `product_family_stage_execution`, `product_family_result`, `product_family_artifact`; reads in closure/workspace/predictive services | Product closure/export, workspace archival checks, family list/read compatibility, partition-artifact reader | yes | yes | yes, tables are retained in Product migration chain | no | no — all retained mutation facades reject without canonical `ExecutionService`; deployment injects it | yes | no | yes — bounded historical-read projection | ARCHIVE | Explicitly archive the projection as read-only historical retention; keep no-write guard; no production deletion | `product_closure_service.py`; `exploratory_service.py`; `predictive_workflow_service.py`; `predictive_split_service.py`; API dependencies; G05 D1/D2 guards |
| `ProductClosureService.project_lineage()` fallback from `analysis_spec_json.revision_context` when canonical revision columns are absent | Project lineage read/export for canonical rows created before dedicated revision columns | yes | yes | yes, `analysis_spec_json` is Product schema | no | no | yes | no | yes — bounded historical-read projection | ARCHIVE | Explicitly archive the read fallback; retain it pending historical-row retirement; no production deletion | `product_closure_service.py:337-346`; G06 P04 checkpoint; `test_cross_analysis_lineage_e3.py` |
| `ScientificResultBatch` legacy-shaped convenience projections | CLI and scientific-adapter consumers (`scientific_status`, `summary`, `artifacts`, graph convenience fields) | yes | indirectly | no | no | no | yes | yes | no | RETAIN_SHARED_CAPABILITY | None | `scientific_core.py`; CLI consumers; scientific adapter tests |

## 4. Genuine TD-006 Set and P02 Action Set

```text
TD-006-ITEM-01
surface: Family ORM historical-data read projections and retained Family tables
classification: ARCHIVE
action: Explicitly record/archive the surface as historical read-only retention.
        Preserve the existing canonical-DI/no-fallback mutation guard. Do not
        delete tables or readers while the identified Product consumers remain.
verification: Focused guard tests prove Product DI, rejected legacy mutations,
              and no legacy runtime/bootstrap reachability.

TD-006-ITEM-02
surface: revision_context JSON lineage fallback for rows predating dedicated
         base_execution_id / revision_kind columns
classification: ARCHIVE
action: Explicitly record/archive the fallback as historical read-only lineage
        projection. Do not remove it without a verified historical-row
        retirement/migration decision.
verification: Source inspection plus G06 typed read reconstruction and
              cross-analysis lineage test coverage.
```

There are no `REMOVE` items: current consumers make removal unsupported by repository evidence. There are no material unclassified candidates.

## 5. Work Performed and Verification

No production change was made. This is evidence-driven: the repository already provides canonical lifecycle injection and rejects retained mutation facades, so P01 found no justified code deletion.

| Command | Outcome | Purpose |
|---|---|---|
| `git branch --show-current`; `git rev-parse HEAD`; `git status --short` | PASS | Entry identity and working-tree state recorded |
| `UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run alembic -c alembic_product.ini heads` | PASS — `20260809_product_0010` | Product migration head |
| Focused `rg` / source inspection of legacy, compatibility, projection, bootstrap, and Family ORM consumers | PASS | Consumer/reachability/authority inventory |
| `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e4_g07_p01_runtime_boundary.py tests/product/test_enh_e4_g07_p02_bootstrap_boundary.py tests/product/test_enh_e4_g07_p03_cli_boundary.py tests/product/test_enh_e1_contract.py` | PASS — 28 passed, 1 skipped | Runtime/deployment/bootstrap, CLI boundary, and snapshot-contract evidence |

The one skipped test is the PostgreSQL-only fresh-bootstrap node, correctly skipped because its database URL was not configured in this focused local run. P01 does not substitute this for G08 P03 real-PostgreSQL verification.

## 6. Acceptance and Handoff

| P01 acceptance condition | Result | Basis |
|---|---|---|
| Current Product migration head recorded | PASS | `20260809_product_0010` |
| Material candidate inventory complete | PASS | Eight material candidates assessed |
| Every candidate has a five-class classification | PASS | Inventory table |
| Genuine TD-006 set explicit | PASS | Two ARCHIVE items |
| Every genuine item has a P02 action | PASS | Section 4 |
| Material Unknown = 0 | PASS | Section 2 |

P02 may act only on `TD-006-ITEM-01` and `TD-006-ITEM-02`. P01 itself leaves `TD-006` OPEN and makes no Gate PASS judgment.
