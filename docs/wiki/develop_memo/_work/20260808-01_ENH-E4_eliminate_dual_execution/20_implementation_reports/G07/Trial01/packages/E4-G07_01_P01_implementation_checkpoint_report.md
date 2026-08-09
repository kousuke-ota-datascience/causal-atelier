# E4-G07 Trial01 P01 Implementation Checkpoint

## Identification

| Field | Value |
|---|---|
| Gate | E4-G07 |
| Trial | 01 |
| Package | P01 — Runtime / Deployment / Shared-Science Boundary |
| Status | COMPLETE |
| Entry SHA | `16a7cfe3951ffe71b53332c8c26831118f1815e0` |
| Checkpoint SHA | PENDING — the repository commit containing this checkpoint |
| Branch | `refactor/ariadne_mvp_e4` |
| TD-005 | OPEN; P01 establishes only the runtime/deployment half |
| Gate status | E4-G07 NOT_COMPLETE |
| Next package | P02 — Product-only migration / bootstrap boundary |

This checkpoint does not declare Gate PASS, TD-005 CLOSED, or READY_FOR_TEST.

## Facts Established

- Canonical Product runtime source roots are `ariadne.product`, `ariadne.interfaces.web_api`, and `ariadne.interfaces.worker`.  The API entry point is `ariadne.interfaces.web_api.app:main`; the worker entry point is `ariadne.interfaces.worker.runner:main`.
- `ScientificCoreAdapter` is wired by the Product worker and delegates through `ariadne.scientific.*`; scientific adapters consume retained `ariadne.causal`, `ariadne.preprocessing`, and `ariadne.shared` capabilities.
- A static AST import-graph audit over each Product/API/worker package and over retained shared-science packages found no transitive path to `ariadne.legacy`.
- `pyproject.toml` excludes `src/ariadne/legacy/**` from the wheel. `.dockerignore` excludes `src/ariadne/legacy`. `Dockerfile` starts the canonical web API, and `compose.yaml` starts `ariadne-worker`; neither invokes `ariadne.legacy`.
- `compose.yaml` also names `alembic_product.ini` for migration. This is an observation only; runtime bootstrap authority and real PostgreSQL evidence are deferred to P02.

## Changes

### Production

None. No active Product dependency on retired legacy runtime was found, so P00 §10's verification-only outcome applies.

### Tests

- Added `tests/product/test_enh_e4_g07_p01_runtime_boundary.py`.
  - Builds a deterministic AST import graph for repository `ariadne.*` modules.
  - Detects direct and transitive legacy reachability from Product, API, worker, and retained shared-science source packages.
  - Pins package scripts, wheel exclusion, `.dockerignore`, Docker API startup, and compose worker startup to canonical Product roots.

### Documentation / reports

- This checkpoint.
- `E4-G07_01_P01__in_progress.md`, as required by the execution request.

## Verification

| Command | Outcome | Material finding |
|---|---|---|
| `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_architecture.py tests/product/test_enh_e4_g07_p01_runtime_boundary.py` | PASS — 6 passed | New guard includes worker and transitive import reachability. |
| `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run python -` (P01 import smoke for web API, worker, `ScientificCoreAdapter`, causal, preprocessing, shared) | PASS | Intended runtime/shared imports remain usable. |
| `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e4_g02_canonical_execution.py tests/product/test_enh_e4_g03_generic_executor_boundary.py tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_enh_e4_g05_submission_convergence.py tests/product/test_enh_e4_g06_p06_mutation_lineage.py tests/product/test_enh_e4_g06_p01_lineage_authority_policy.py` | PASS — 42 passed | Focused preservation evidence for G02–G06 authority contracts. |
| Static deployment inspection of `pyproject.toml`, `.dockerignore`, `Dockerfile`, and `compose.yaml` | PASS | Canonical API/worker roots and legacy package/build exclusion confirmed. |

P01 did not change DB behavior; real PostgreSQL bootstrap verification is not a P01 requirement and remains P02 work.

## Residual Legacy Inventory

| Path / surface | Classification | Product runtime reachable? | Product deployment reachable? | Product bootstrap reachable? | Persistent authority? | Shared capability required? | G07 action | G08 residual | Verification evidence |
|---|---|---:|---:|---:|---:|---:|---|---|---|
| `src/ariadne/legacy/` | RETIRED_UNREACHABLE | no | no | DEFER_P02 | no | no | Retain; do not speculatively delete. | Physical archive/source cleanup, if later desired. | AST guard; wheel and Docker context exclusions. |
| `pyproject.toml` runtime/package surface | ACTIVE_PRODUCT_DEPENDENCY (canonical only) | yes | yes | no | yes | no | Guard scripts and wheel exclusion. | none | P01 deployment contract test. |
| `.dockerignore` | ACTIVE_PRODUCT_DEPENDENCY (boundary control) | no | yes | no | no | no | Keep `src/ariadne/legacy` excluded. | none | P01 deployment contract test. |
| `Dockerfile` | ACTIVE_PRODUCT_DEPENDENCY (canonical API startup) | yes | yes | no | yes | no | Keep `ariadne.interfaces.web_api.app:app`. | none | P01 deployment contract test. |
| `compose.yaml` API/worker surfaces | ACTIVE_PRODUCT_DEPENDENCY (canonical deployment wiring) | yes | yes | DEFER_P02 | yes | no | Keep Docker API command and `ariadne-worker`; migration command deferred. | none for API/worker; bootstrap assessed in P02. | P01 deployment contract test. |
| Product API root | ACTIVE_PRODUCT_DEPENDENCY | yes | yes | no | yes | no | Preserve canonical root; prohibit legacy reachability. | none | AST guard and import smoke. |
| Product worker root | ACTIVE_PRODUCT_DEPENDENCY | yes | yes | no | yes | no | Preserve canonical root and `ScientificCoreAdapter` wiring. | none | AST guard and import smoke. |
| Product scientific adapter path | ACTIVE_PRODUCT_DEPENDENCY | yes | yes | no | no | yes | Preserve `ScientificCoreAdapter`; prohibit legacy reachability. | none | AST guard and import smoke. |
| `ariadne.causal` | RETAIN_SHARED_CAPABILITY | yes | indirectly | no | no | yes | Keep unchanged. | none | AST guard and import smoke. |
| `ariadne.preprocessing` | RETAIN_SHARED_CAPABILITY | yes | indirectly | no | no | yes | Keep unchanged. | none | AST guard and import smoke. |
| `ariadne.shared` | RETAIN_SHARED_CAPABILITY | yes | indirectly | no | no | yes | Keep compatibility components unless consumer analysis proves otherwise. | possible compatibility cleanup only | AST guard and import smoke. |
| Root `alembic.ini` / `migrations` | HISTORY_ONLY (expected; not decided here) | no | no | DEFER_P02 | DEFER_P02 | no | P02 must prove actual Product bootstrap non-reachability on PostgreSQL. | none unless P02 finds a classified residual. | Compose observation only. |

## Acceptance

| Criterion | Result | Basis |
|---|---|---|
| P01-AC-01 Runtime reachability | PASS | New transitive AST guard covers Product, web API, and worker packages; no `ariadne.legacy` path exists. |
| P01-AC-02 Deployment boundary | PASS | Scripts, wheel exclusion, Docker context, Docker API startup, and compose worker startup are pinned to canonical roots. |
| P01-AC-03 Shared science preserved | PASS | Retained roots and `ScientificCoreAdapter` have no legacy path and import successfully. |
| P01-AC-04 No legacy authority revival | PASS | No production behavior changed; focused G02–G06 authority tests pass. |
| P01-AC-05 Residual inventory ready | PASS | Material surfaces are classified above; bootstrap decision is explicitly deferred to P02. |
| P01-AC-06 Passed-Gate preservation | PASS | Focused G02–G06 regression selection: 42 passed. |

## P02 Entry

- P01 checkpoint commit SHA must be recorded by the subsequent P02 checkpoint after this commit is created.
- P02 must establish the complete Product bootstrap path, prove `alembic_product.ini -> product_migrations` on real PostgreSQL, and classify root `alembic.ini -> migrations` as history-only or report a contradiction.
- Reuse `tests/product/test_enh_e4_g07_p01_runtime_boundary.py` together with `tests/product/test_architecture.py` for runtime/deployment boundary regression.
