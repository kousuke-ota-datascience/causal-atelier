# G4 Trial 003 Test 003 — train_only_preprocessing

- Gate: G4
- Trial: 003
- Test item: 003
- Status: PASS
- Tested implementation commit: a8b656b463b2f8251eff8006538d04ad5af83918
- Handoff report commit / path: 28c57400a2966568975698297eb7554ce51af80c / docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/G4_003_implementation_completion_report.md
- Branch: prototype/ariadne_mvp_e3
- Migration head: 20260807_product_0005
- Started at: 2026-08-07T09:54:17Z
- Finished at: 2026-08-07T09:54:45Z

## Purpose

前処理fitがTRAINに限定され、TESTがselection/fitへ流入せずschema/orderが固定されることを検証する。

## Acceptance Criteria

fitはTRAINのみ、validation/test transform only、TESTはPREPARE/TRAIN選択入力に不在、fitted preprocessor Artifact、multi-feature schema/order決定性。

## Preconditions / Environment

- Current HEAD: 28c57400a2966568975698297eb7554ce51af80c
- Project .venv via uv run; Test Agentによるsource/test/migration変更なし。

## Commands Executed

~~~bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_predictive_training_e3.py
~~~

## Exact Result

- exit code 0; 2 passed; 0 failed; 0 skipped; 28s wall clock (pytest 6.04s).

## Log / Evidence

- /tmp/g4_003_002_004_predictive_training.log; direct assertions: fit_partition TRAIN, schema score/segment, output order score/segment=A/segment=B, repeat equality, training bundleにtestなし。

## Findings

- product defect: none; test infrastructure issue: none; regression: none; deviation: none.

## Decision Rationale

Trial 002で不足したfeature schema/orderの直接assertionを含め成功したためPASS。

## User-directed Full Re-execution

- Execution HEAD before evidence update: `430f6411665bd72d3436b3a42cc7fd593e75a953`
- Technical status: PASS
- Started at: 2026-08-07T10:27:01Z
- Finished at: 2026-08-07T10:27:09Z

~~~bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_predictive_training_e3.py
~~~

- Exact result: exit code 0; 2 passed; 0 failed; 0 skipped; 8s wall clock (pytest 1.39s).
- Log / evidence: `/tmp/g4_003_full_rerun_002_004.log`
- Source/test/migration modification by Test Agent: NONE

## Source Modification by Test Agent

NONE
