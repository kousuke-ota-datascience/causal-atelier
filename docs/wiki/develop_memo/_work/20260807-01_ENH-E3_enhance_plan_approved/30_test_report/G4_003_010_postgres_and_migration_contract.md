# G4 Trial 003 Test 010 — postgres_and_migration_contract

- Gate: G4
- Trial: 003
- Test item: 010
- Status: BLOCKED
- Tested implementation commit: a8b656b463b2f8251eff8006538d04ad5af83918
- Handoff report commit / path: 28c57400a2966568975698297eb7554ce51af80c / docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/G4_003_implementation_completion_report.md
- Branch: prototype/ariadne_mvp_e3
- Migration head: 20260807_product_0005
- Started at: UNKNOWN for interrupted attempt; supplemental 2026-08-07T09:56:46Z
- Finished at: supplemental 2026-08-07T10:00:08Z
- User-directed re-execution status: PASS
- User-directed re-execution started at: 2026-08-07T10:14:38Z
- User-directed re-execution finished at: 2026-08-07T10:15:28Z

## Purpose

PostgreSQL persistenceと変更されていないmigration headのschema適合を検証する。

## Acceptance Criteria

PostgreSQL predictive persistence、migration追加なしのhead unchanged/single head/schema充足、および必須test中断時のTrial規約。

## Preconditions / Environment

- Current HEAD: 28c57400a2966568975698297eb7554ce51af80c
- Project .venv via uv run; Test Agentによるsource/test/migration変更なし。

## Commands Executed

~~~bash
# Initial required execution was aborted by user after 121.9s; completion output unavailable.
# Supplemental:
env ARIADNE_PRODUCT_DATABASE_URL=postgresql+psycopg://ariadne:ariadne@127.0.0.1:5432/ariadne_g4_003_test .venv/bin/alembic -c alembic_product.ini upgrade head
env PYTHONPATH=/tmp/g4_003_pg_pytest UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q --noconftest -p g4_003_pg_plugin tests/product/test_predictive_api_worker_e2e_e3.py
docker compose exec -T database dropdb -U ariadne ariadne_g4_003_test

# User-directed re-execution on a new clean database:
.venv/bin/alembic -c alembic_product.ini heads
env ARIADNE_PRODUCT_DATABASE_URL=postgresql+psycopg://ariadne:ariadne@127.0.0.1:5432/ariadne_g4_003_010_rerun .venv/bin/alembic -c alembic_product.ini upgrade head
env G4_010_RERUN_DATABASE_URL=postgresql+psycopg://ariadne:ariadne@127.0.0.1:5432/ariadne_g4_003_010_rerun PYTHONPATH=/tmp/g4_003_g4_010_rerun UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q --noconftest -p g4_010_rerun_plugin tests/product/test_predictive_api_worker_e2e_e3.py
docker compose exec -T database dropdb -U ariadne ariadne_g4_003_010_rerun
~~~

## Exact Result

- initial attempt: user-aborted after 121.9s, exit unavailable. State audit: DB existed but Alembic version/Result tables absent. Supplemental: upgrade exit 0, head/database 0005, pytest exit 0, 3 passed, 0 failed, 0 skipped, pytest 1.86s, Result 8, Artifact 3, 202s wall interval including permission/tool wait. Dedicated DB removed.
- user-directed re-execution: exit code 0; single head `20260807_product_0005`; clean database revision `20260807_product_0005`; 3 passed, 0 failed, 0 skipped in pytest 2.06s; Execution 3, Result 8, Artifact 3; 50s wall clock; dedicated database removal verified with remaining database count 0.

## Log / Evidence

- /tmp/g4_003_010_postgres_and_migration_contract.log contains supplemental run; initial attempt has no complete log due explicit turn/tool abort; temporary plugin was under /tmp only。
- `/tmp/g4_003_010_postgres_rerun.log` contains the complete user-directed re-execution. The fixture plugin remained under `/tmp`; no source-tree helper was added.

## Findings

- product defect: none observed; test infrastructure issue: historical user interruption; regression: none observed; deviation: two completed PostgreSQL executions succeeded, but neither can restore Trial PASS under instruction section 5.

## Decision Rationale

ユーザー指示による再実行を含む2回の完走では製品/migration契約が成立した。最新の技術的実行結果はPASS。ただし最初のuser interruptionはsection 4のBLOCKED事由かつsection 5により当該trialはPASS不可のため、itemのTrial statusはBLOCKEDを維持する。

## Source Modification by Test Agent

NONE
