# E4-G07 Trial01 P03 Implementation Checkpoint

## Identification

| Field | Value |
|---|---|
| Gate | E4-G07 |
| Trial | 01 |
| Package | P03 — CLI / Compatibility Boundary |
| Status | COMPLETE |
| Entry SHA | `b3d03b270f3c64bf380a37a1934d871ba7406696` |
| P02 checkpoint SHA | `102d0c1539eee8a1d605a709c599a21e99e3ab15` |
| Checkpoint SHA | PENDING — repository commit containing this checkpoint |
| Product migration head | `20260809_product_0010` |
| TD-005 | OPEN; formal closure remains P04 |
| Gate status | E4-G07 NOT_COMPLETE |
| Next package | P04 — Gate completion / TD-005 closure / test handoff |

This checkpoint does not declare Gate PASS, TD-005 CLOSED, or READY_FOR_TEST.

## Facts Established

- All repository-managed analysis scripts are explicitly classified: `ariadne-discover`, `ariadne-estimate`, `ariadne-identify`, `ariadne-refute`, and `ariadne-sensitivity` are `LOW_LEVEL_UTILITY`.
- `ariadne-api` and `ariadne-worker` are Product deployment roots, not analysis CLIs. No repository-managed `AUDITABLE_PRODUCT_CLI` exists (`AUDITABLE_PRODUCT_CLI = 0`).
- AST import-graph reachability from every low-level CLI entry point to `ariadne.legacy` or `ariadne.product.persistence` is zero.
- Discovery and estimation complete from local inputs to local `manifest.json` with an explicitly unreachable `ARIADNE_PRODUCT_DATABASE_URL`, using a deterministic scientific adapter fake. Thus neither Product DB bootstrap nor persistent lifecycle ownership is required by the utility path.
- Portable CLI manifests contain scientific provenance but no `execution_id`, `stage_execution_id`, `result_id`, or `artifact_id` field.

## Changes

### Production

None. Existing CLI behavior already satisfies ADR-011; converting utilities into Product lifecycle orchestration would violate the fixed boundary.

### Tests

- Added `tests/product/test_enh_e4_g07_p03_cli_boundary.py`.
  - Discovers every `[project.scripts]` target under `ariadne.interfaces.cli.*` and fails for an unclassified analysis CLI.
  - Requires the current five analysis scripts to be low-level utilities.
  - Traverses repository `ariadne.*` imports transitively and fails if a utility can reach retired legacy runtime or Product persistence.
  - Reserves Product persistent identity fields from `CliManifest`.
- Strengthened `tests/product/test_cli_contract.py`.
  - Discovery and estimation run with `ARIADNE_PRODUCT_DATABASE_URL` set to an unreachable endpoint.
  - Both resulting local manifests are checked against all reserved persistent identity fields.

### Documentation / reports

- This checkpoint.
- `E4-G07_01_P03__in_progress.md`, required by the execution request.

## Verification

| Command | Outcome | Material finding |
|---|---|---|
| `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_cli_contract.py tests/product/test_enh_e4_g07_p03_cli_boundary.py` | PASS — 7 passed | Discovery and estimation local-output contracts, CLI classification, no persistence/legacy reachability, and manifest identity boundary hold. |
| `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e4_g07_p01_runtime_boundary.py tests/product/test_enh_e4_g07_p02_bootstrap_boundary.py tests/product/test_enh_e4_g07_p03_cli_boundary.py` | PASS — 8 passed, 1 skipped | P01/P02 boundary regressions remain intact. The skip is P02's PostgreSQL-only node; its real PostgreSQL evidence is recorded in the P02 checkpoint. |

The P02 static node emits its existing Alembic `prepend_sys_path` deprecation warning; it does not affect the result.

## CLI Inventory

| Entry point | Target | Classification | Persistent authority | Evidence / action |
|---|---|---|---:|---|
| `ariadne-discover` | `ariadne.interfaces.cli.discovery:main` | LOW_LEVEL_UTILITY | no | Local scientific adapter + manifest; guarded. |
| `ariadne-estimate` | `ariadne.interfaces.cli.estimation:main` | LOW_LEVEL_UTILITY | no | Local scientific adapter + manifest; guarded. |
| `ariadne-identify` | `ariadne.interfaces.cli.identification:main` | LOW_LEVEL_UTILITY | no | Delegates to local `scientific_stage`; guarded. |
| `ariadne-refute` | `ariadne.interfaces.cli.refutation:main` | LOW_LEVEL_UTILITY | no | Delegates to local `scientific_stage`; guarded. |
| `ariadne-sensitivity` | `ariadne.interfaces.cli.sensitivity:main` | LOW_LEVEL_UTILITY | no | Delegates to local `scientific_stage`; guarded. |
| Auditable Product analysis CLI | none | AUDITABLE_PRODUCT_CLI = 0 | no | No feature was invented; future entry points must be explicitly classified. |

## Compatibility Terminology Inventory

| Surface | Classification | Consumer / evidence | G07 action | Residual |
|---|---|---|---|---|
| `LEGACY_SNAPSHOT_SCHEMA_VERSION = legacy-product-snapshot/1` | COMPATIBILITY_DATA_CONTRACT | `Execution.validate_input_contract()` accepts the historical discovery/estimation input matrix; ORM constraint preserves the same read/persistence contract; `test_enh_e1_contract.py` and `test_postgres_contract.py` exercise it. Renaming/removal would reject existing compatibility data. | Retain. | Compatibility cleanup requires a product data-contract decision, not P03. |
| `LegacyProductAuthorityDisabled` | RETIRED_RUNTIME_REFERENCE | Product domain error explicitly rejects lifecycle authority from a retained legacy facade. It does not import or activate legacy runtime. | Retain protective terminology. | none. |
| `ScientificResultBatch` legacy projections | COMPATIBILITY_DATA_CONTRACT | Product scientific port documents read-only projections for local integrations; this is a result-shape compatibility term, not a persistence owner. | Retain. | Consumer-specific cleanup, if desired, is outside G07. |
| `legacy_*` identifiers in G05/G06 regression fixtures | TEST_HISTORY_ONLY | Test sentinel data asserts that canonical behavior does not revive/alter old-family records. | Retain tests. | none. |
| `legacy_artifacts` variable naming in closure code | COMPATIBILITY_DATA_CONTRACT | Reads retained family artifact projections for closure/export compatibility; the naming alone is not an `ariadne.legacy` runtime dependency. | No rename in P03. | Evaluate only with a distinct closure compatibility change. |

## Residual Legacy Inventory Update

| Path / surface | Classification | Product runtime reachable? | Product deployment reachable? | Product bootstrap reachable? | Persistent authority? | Shared capability required? | G07 action | G08 residual | Verification evidence |
|---|---|---:|---:|---:|---:|---:|---|---|---|
| `pyproject.toml` scientific scripts / `interfaces/cli/` | LOW_LEVEL_UTILITY | yes | no | no | no | yes | Preserve direct scientific/file/manifest interface; guard classification and reachability. | Future auditable CLI must be deliberately classified. | P03 guard + runtime CLI tests. |
| CLI portable manifests | LOW_LEVEL_UTILITY | yes | no | no | no | yes | Reserve Product persistent identity fields. | none | P03 guard + discovery/estimation local manifests. |
| `legacy-product-snapshot/1` | COMPATIBILITY_DATA_CONTRACT | Product domain only | no | no | no | no | Retain historical validation contract. | Future data-contract retirement decision. | Source/test consumers listed above. |

## Acceptance

| Criterion | Result | Basis |
|---|---|---|
| P03-AC-01 CLI classification complete | PASS | Five analysis scripts discovered and explicitly classified; unclassified analysis scripts fail the guard. |
| P03-AC-02 Low-level utility no persistence | PASS | Transitive reachability to legacy and Product persistence is zero. |
| P03-AC-03 Portable manifest boundary | PASS | Discovery and estimation succeed with unreachable Product DB URL and produce manifests without reserved IDs. |
| P03-AC-04 Auditable boundary | PASS | `AUDITABLE_PRODUCT_CLI = 0`; no new CLI was introduced. |
| P03-AC-05 Compatibility terminology evidence | PASS | Material compatibility/rejected-runtime/test-history names are classified with consumers and action. |
| P03-AC-06 Prior G07 boundaries preserved | PASS | P01/P02/P03 boundary selection passes (8 passed, 1 expected PostgreSQL-only skip). |

## P04 Entry

- Reuse P01 runtime/deployment/shared-science, P02 bootstrap, and P03 CLI guard paths.
- TD-005 may be closed only after P04's Gate-wide negative-authority audit proves both runtime and bootstrap independence and confirms this CLI boundary.
- Residuals are classification/cleanup only; no active Product legacy authority was found in P01–P03.
