# E4-G07 Trial01 P02 Implementation Checkpoint

## Identification

| Field | Value |
|---|---|
| Gate | E4-G07 |
| Trial | 01 |
| Package | P02 — Product-only Migration / Bootstrap Boundary |
| Status | COMPLETE |
| Entry SHA | `ef0a6dc9c35b2e42256a9569ac906a926ea579ff` |
| P01 checkpoint SHA | `e10a6e3d1305cf31d61d669f6e6d41a1b41e8ce1` |
| Checkpoint SHA | PENDING — repository commit containing this checkpoint |
| Product migration head | `20260809_product_0010` |
| Migration | NONE |
| TD-005 | OPEN; formal closure remains P04 |
| Gate status | E4-G07 NOT_COMPLETE |
| Next package | P03 — CLI / compatibility boundary |

This checkpoint does not declare Gate PASS, TD-005 CLOSED, or READY_FOR_TEST.

## Facts Established

- The production bootstrap graph is `compose.yaml:migrate` → `alembic -c alembic_product.ini upgrade head` → `product_migrations/env.py` → `ProductBase.metadata` → `alembic_version_product`.
- The test bootstrap graph is `run_product_postgres_tests.sh` → `compose.test.yaml:test_runner` → fresh database reset → `alembic -c alembic_product.ini upgrade head` → `alembic ... current` → pytest.
- `alembic_product.ini` uses `product_migrations`; its environment uses `ARIADNE_PRODUCT_DATABASE_URL`, `ProductBase.metadata`, and only `alembic_version_product`.
- Product history has exactly one head, `20260809_product_0010`. The displayed ancestry begins at `20260805_product_0001` and contains Product revisions only; no root revision appears.
- Root `alembic.ini` targets `migrations`, but it is not invoked by production/test Product bootstrap. It is therefore `HISTORY_ONLY` for Product bootstrap.
- A fresh PostgreSQL Product database contains `alembic_version_product` at the repository Product head, lacks root `alembic_version`, and lacks root-only `app_user`.

## Changes

### Production / bootstrap

None. No active Product invocation of the root chain was found; historical migrations were neither deleted nor rewritten.

### Tests

- Added `tests/product/test_enh_e4_g07_p02_bootstrap_boundary.py`.
  - Semantically verifies Product Alembic configuration, metadata owner, URL contract, version table, and intended single head.
  - Guards production/test bootstrap surfaces against root `alembic.ini` or `migrations` invocation/copy.
  - On real PostgreSQL compares the database Product revision with Alembic's repository head, verifies Product schema presence, root version-table absence, and root-only schema absence.
  - The test image intentionally omits root `alembic.ini`/`migrations`; in that environment, their absence is itself asserted rather than requiring unavailable files.

### Documentation / reports

- This checkpoint.
- `E4-G07_01_P02__in_progress.md`, required by the execution request.

## Static Verification

| Command | Outcome | Finding |
|---|---|---|
| `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e4_g07_p01_runtime_boundary.py tests/product/test_enh_e4_g07_p02_bootstrap_boundary.py` | PASS — 5 passed, 1 skipped | P01 runtime boundary remains intact; P02 static guard passes. The skipped test is the PostgreSQL case without a configured local test DB. |
| `UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run alembic -c alembic_product.ini heads` | PASS | `20260809_product_0010 (head)`; one intended head. |
| `UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run alembic -c alembic_product.ini history` | PASS | Product-only linear ancestry from `20260805_product_0001` through `20260809_product_0010`; no root-chain splice observed. |

The Alembic commands emit a pre-existing `prepend_sys_path` deprecation warning. It does not alter the selected script location, migration head, or test result, and is outside P02's authority-boundary scope.

## PostgreSQL Verification

Runner command:

```bash
ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g07-p02-evidence \
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g07_p02_bootstrap_boundary.py \
  tests/product/test_postgres_contract.py
```

| Evidence field | Result |
|---|---|
| Metadata | `/tmp/ariadne-g07-p02-evidence/run-20260809T175756Z.metadata.txt` |
| Log | `/tmp/ariadne-g07-p02-evidence/run-20260809T175756Z.txt` |
| Database | fresh `ariadne_test` on `postgres:17-alpine` |
| Reset exit code | 0 |
| Migration exit code | 0 |
| Migration current exit code | 0 |
| Pytest exit code | 0; 7 passed |
| Repository Product head | `20260809_product_0010` |
| DB `alembic_version_product.version_num` | `20260809_product_0010` |
| `alembic_version_product` | present |
| Root `alembic_version` | absent |
| Root-only `app_user` | absent |
| Product required tables | present (`product_project`, `product_execution`, `product_result`, `product_artifact`) |

## Residual Legacy Inventory

| Path / surface | Classification | Product runtime reachable? | Product deployment reachable? | Product bootstrap reachable? | Persistent authority? | Shared capability required? | G07 action | G08 residual | Verification evidence |
|---|---|---:|---:|---:|---:|---:|---|---|---|
| `alembic_product.ini` / `product_migrations/` | ACTIVE_PRODUCT_DEPENDENCY | no | yes | yes | yes | no | Preserve as the sole Product chain. | none | P02 guard, heads/history, fresh PostgreSQL runner. |
| `compose.yaml:migrate` | ACTIVE_PRODUCT_DEPENDENCY | no | yes | yes | yes | no | Preserve Product ini invocation. | none | P02 static guard. |
| `Dockerfile` / `Dockerfile.test` Product migration assets | ACTIVE_PRODUCT_DEPENDENCY | no | yes | yes | no | no | Preserve only Product config/migrations; test image excludes root chain. | none | P02 static guard and container run. |
| `scripts/test/run_product_postgres_tests*.sh` | test-only bootstrap support | no | no | yes | no | no | Preserve reset → Product upgrade/current → pytest sequence. | none | P02 static guard and runner metadata. |
| `alembic.ini` / `migrations/` | HISTORY_ONLY | no | no | no | no | no | Retain without rewrite/deletion. | Archive/source cleanup only, if later required. | Root config target plus static invocation guard; fresh DB lacks root version/schema. |

## Acceptance

| Criterion | Result | Basis |
|---|---|---|
| P02-AC-01 Bootstrap path | PASS | Canonical production and test graphs are identified and use `alembic_product.ini -> product_migrations` only. |
| P02-AC-02 Root chain history-only | PASS | Root config is retained but absent from active commands/assets; fresh Product DB has no root version table/schema. |
| P02-AC-03 Permanent guard | PASS | New focused test fails if active bootstrap surfaces invoke/copy root chain. |
| P02-AC-04 Real PostgreSQL | PASS | Fresh reset, upgrade, current, and 7-test suite all pass; required version/schema evidence is recorded. |
| P02-AC-05 Product chain integrity | PASS | `heads` reports one Product head; history is Product-only and unspliced. |
| P02-AC-06 Scope/preservation | PASS | No production migration/source rewrite or new authority; P01 runtime guard passes. |

## P03 Entry

- Canonical bootstrap is fixed as `alembic_product.ini -> product_migrations`, head `20260809_product_0010`.
- Root `alembic.ini -> migrations` is `HISTORY_ONLY` for Product bootstrap; P03 must not reopen migration authority.
- Reuse `tests/product/test_enh_e4_g07_p01_runtime_boundary.py` and `tests/product/test_enh_e4_g07_p02_bootstrap_boundary.py` as boundary regressions.
- Remaining scope is standalone scientific CLI lifecycle and compatibility semantics only.
