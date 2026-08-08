# G3 Trial 002 Test 006 — postgres_predictive_split_contract

- Gate: G3
- Trial: 002
- Test item: 006
- Status: PASS
- Tested implementation commit: `fd4e332939f93cc35adbf4a03929818e47c04b7e`
- Handoff report commit / path: `908ce954e4f155560861c91fae169cbe35f63866` / `20_implementation_reports/G3_002_implementation_completion_report.md`
- Branch: `prototype/ariadne_mvp_e3`
- Migration head: `20260807_product_0004` (single head)
- Started at: `2026-08-07T08:19:19Z`
- Finished at: `2026-08-07T08:21:07Z`

## Purpose

Predictive split API/persistence が SQLite 固有でないことと、G3 migration head が単一かつ変更されていないことを PostgreSQL で検証する。

## Acceptance Criteria

- PostgreSQL test DB を head まで migrate できる。
- `test_predictive_split_api_e3.py` の同一 test code が PostgreSQL 上で全 PASS する。
- migration は `20260807_product_0004` single head で、trial 002 に追加 migration がない。

## Preconditions / Environment

- Docker Compose PostgreSQL 17 service: healthy
- Dedicated database: `ariadne_g3_002_test`
- Existing canonical `product_env` fixture は SQLite を強制するため、source tree を変更せず `/tmp/g3_002_pg_pytest/g3_002_pg_plugin.py` で DB fixture のみ PostgreSQL に差し替えた。
- Test file `tests/product/test_predictive_split_api_e3.py` は変更・複製せず、そのまま実行した。
- Dedicated database は PASS 後に `dropdb` で削除した。

## Commands Executed

```bash
docker compose ps
docker compose exec -T database createdb -U ariadne ariadne_g3_002_test

ARIADNE_PRODUCT_DATABASE_URL=postgresql+psycopg://ariadne:ariadne@127.0.0.1:5432/ariadne_g3_002_test \
UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run alembic -c alembic_product.ini upgrade head

UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run alembic -c alembic_product.ini heads

PYTHONPATH=/tmp/g3_002_pg_pytest \
UV_CACHE_DIR=/tmp/ariadne-uv-cache \
PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q --noconftest -p g3_002_pg_plugin \
  tests/product/test_predictive_split_api_e3.py

docker compose exec -T database dropdb -U ariadne ariadne_g3_002_test
```

## Exact Result

- first attempt exit code: 1
- first attempt passed: 0
- first attempt failed: 0
- first attempt errors: 4
- first attempt skipped: 0
- first attempt duration: 12s
- retry exit code: 0
- retry passed: 4
- retry failed: 0
- retry skipped: 0
- retry pytest duration: 1.52s
- retry command duration: 11s
- migration upgrade exit code on retry: 0
- Alembic heads exit code: 0
- observed head: `20260807_product_0004 (head)`
- active execution duration: 23s

## Log / Evidence

初回は sandbox 内から host PostgreSQL socket への接続制限により、migration と全 test setup が同じ接続 error で失敗した。

```text
psycopg.OperationalError: connection is bad: no error details available
sqlalchemy.exc.OperationalError: (psycopg.OperationalError) connection is bad
ERROR ...test_predictive_split_api_e3.py::test_split_api_persists_reproducible_partition_artifact_and_lineage[asyncio]
ERROR ...test_predictive_split_api_e3.py::test_split_from_fixed_analysis_view_records_view_lineage[asyncio]
ERROR ...test_predictive_split_api_e3.py::test_split_runner_validation_error_preserves_machine_code_and_field_path[asyncio]
ERROR ...test_predictive_split_api_e3.py::test_g3_capabilities_do_not_advertise_training[asyncio]
4 errors in 1.96s
```

Docker service は healthy であり、product assertion 到達前の一様な infrastructure failure だったため、trial 規約に基づき sandbox 外で1回だけ再試行した。

```text
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Running upgrade 20260806_product_0003 -> 20260807_product_0004
20260807_product_0004 (head)
....                                                                     [100%]
4 passed in 1.52s
```

## Findings

- product defect: none
- test infrastructure issue: initial sandbox host-network restriction; resolved by the one permitted retry
- regression: none
- deviation: none
- none: false (resolved infrastructure event recorded)

## Decision Rationale

初回 failure は product code へ到達しない環境要因で、明確な一時的 environment failure と判定した。許可された1回の再試行で clean PostgreSQL migration と全4 contract tests が成功したため PASS。

## Source Modification by Test Agent

NONE
