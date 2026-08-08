# G6 Trial 001 Test 012 — legacy_dependency_audit

- Gate: G6
- Trial: 001
- Test item: 012
- Status: PASS
- Tested implementation commit: `265b69a3317a0b9747cacee457e72b36a62daa7e`
- Handoff report commit / path: `963f1f2` / `docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/G6_001_implementation_completion_report.md`
- Branch: `prototype/ariadne_mvp_e3`
- Migration head: `20260807_product_0006`
- Started at: 2026-08-07T12:32:15Z
- Finished at: 2026-08-07T12:32:49Z

## Purpose

Product Domain/Application、新規Web API/Capabilityからlegacy packageへの新規依存がないことを監査する。

## Acceptance Criteria

対象実装diffの新規legacy dependency violation 0、architecture test PASS、diff/構文clean。

## Preconditions / Environment

- Implementation diff: `f97b9ec5..265b69a3`
- Handoff後にsource/test/migration変更なし。

## Commands Executed

```bash
git diff --check f97b9ec5..265b69a3
git diff --check
git diff f97b9ec5..265b69a3 -- src/ariadne/product src/ariadne/interfaces/web_api | \
  rg -n '^\+.*(ariadne\.legacy|from ariadne import legacy|import ariadne\.legacy)'
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q tests/product/test_architecture.py
node --check frontend/app.js
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \
uv run python -m compileall -q src tests experiments product_migrations
```

## Exact Result

- implementation diff check: exit 0
- working-tree tracked diff check: exit 0
- new legacy imports: 0
- architecture: 3 passed, 0 failed, exit 0, 1.21s（elapsed 7.11s）
- Node syntax: exit 0, 0.04s
- compileall first attempt: exit 2, 0.01s due read-only default uv cache
- compileall permitted retry: exit 0, 8.22s

## Log / Evidence

- Changed production scopeはProduct application/domain/persistenceおよびWeb API、frontend、migration。
- `ariadne.legacy`系の追加importは0。
- Initial uv cache failureはproduct-independent environment issueで、`/tmp` cache指定の唯一の再試行で解消。

## Findings

- product defect: none
- test infrastructure issue: transient/default-cache permission issue resolved on one permitted retry
- regression: none observed in architecture tests
- deviation: none

## Decision Rationale

対象diffにlegacy dependency追加はなく、canonical architecture testsと構文/diff checksが成功したためPASS。

## Source Modification by Test Agent

NONE
