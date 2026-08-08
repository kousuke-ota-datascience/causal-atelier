# G5 Trial 002 Test 002 — model_card_lineage

- Gate: G5
- Trial: 002
- Test item: 002
- Status: PASS
- Tested implementation commit: 4a83bb6860c895f00e4dfd7c9e7880105387373e
- Handoff report commit / path: 4ccbfbb196ba384aa362450666c00b4c936c58d7 / docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/G5_002_implementation_completion_report.md
- Branch: prototype/ariadne_mvp_e3
- Migration head: 20260807_product_0005
- Started at: 2026-08-07T11:32:11Z
- Finished at: 2026-08-07T11:35:31Z

## Purpose

Model Card必須意味値、Artifact association、complete lineage、PostgreSQL persistenceを検証する。

## Acceptance Criteria

intended use、population、training data、features、split、model、metrics、limitations/warnings、runtime/code、Spec/Dataset/View/Split/Preprocessor/Model/Prediction/Evaluation lineage。

## Preconditions / Environment

- G4 Trial 003: PASS
- Current handoff HEAD: 4ccbfbb196ba384aa362450666c00b4c936c58d7
- Project `.venv` via `uv run`; Test Agent source/test/migration modification: NONE

## Commands Executed

~~~bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_predictive_explanation_e3.py
env ARIADNE_PRODUCT_DATABASE_URL=postgresql+psycopg://ariadne:ariadne@127.0.0.1:5432/ariadne_g5_002_test .venv/bin/alembic -c alembic_product.ini upgrade head
env G5_002_DATABASE_URL=postgresql+psycopg://ariadne:ariadne@127.0.0.1:5432/ariadne_g5_002_test PYTHONPATH=/tmp/g5_002_pg_pytest UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q --noconftest -p g5_002_pg_plugin tests/product/test_predictive_explanation_e3.py::test_api_worker_persists_explanation_model_card_artifacts_and_lineage
~~~

## Exact Result

- SQLite canonical: exit 0; 5 passed; pytest 3.11s
- PostgreSQL test: exit 0; 1 passed; pytest 1.12s
- single head/database revision: `20260807_product_0005`
- persisted: MODEL_CARD_RESULT=1, PREDICTIVE_EXPLANATION_RESULT=1, MODEL_CARD Artifact=1, PREDICTIVE_EXPLANATION Artifact=1, lineage edges=37
- PostgreSQL audit interval: 91s including SQL diagnosis/correction
- dedicated DB removed; remaining DB count 0

## Log / Evidence

- `/tmp/g5_002_001_002_005_explanation.log`
- `/tmp/g5_002_postgres_and_migration_contract.log`
- Initial helper query used old `product_artifact` and wrapper exited 1; product pytest had already passed. Read-only schema inspection showed `FamilyArtifactOrm` maps to `product_family_artifact`; corrected query exited 0 and found both required artifacts.

## Findings

- product defect: none
- test infrastructure issue: none
- audit tooling issue: initial auxiliary SQL targeted the wrong artifact table; corrected once without rerunning the product test
- regression: none
- deviation: no migration round-trip because Trial 002 adds no migration

## Decision Rationale

All Model Card fields/lineage assertions and real PostgreSQL persistence passed. The auxiliary SQL error was an auditor table-selection error, not a product failure.

## Source Modification by Test Agent

NONE

