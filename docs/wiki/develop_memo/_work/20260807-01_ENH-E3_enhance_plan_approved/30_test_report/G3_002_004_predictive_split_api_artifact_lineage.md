# G3 Trial 002 Test 004 — predictive_split_api_artifact_lineage

- Gate: G3
- Trial: 002
- Test item: 004
- Status: PASS
- Tested implementation commit: `fd4e332939f93cc35adbf4a03929818e47c04b7e`
- Handoff report commit / path: `908ce954e4f155560861c91fae169cbe35f63866` / `20_implementation_reports/G3_002_implementation_completion_report.md`
- Branch: `prototype/ariadne_mvp_e3`
- Migration head: `20260807_product_0004`
- Started at: `2026-08-07T08:17:04Z`
- Finished at: `2026-08-07T08:17:15Z`

## Purpose

Predictive split API、Generic Executor、artifact persistence/hash/metadata、Dataset/View lineage を検証する。

## Acceptance Criteria

Capabilities、split-validations、dedicated 422 code/path、`PREDICTIVE` execution、`predictive.split.v1` stage、partition artifact persistence、Dataset/View lineage、same spec/source/seed content hash を確認する。

## Preconditions / Environment

- Default product test fixture (SQLite) targeted integration
- `UV_CACHE_DIR=/tmp/ariadne-uv-cache`
- `PYTHONDONTWRITEBYTECODE=1`

## Commands Executed

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q tests/product/test_predictive_split_api_e3.py
```

## Exact Result

- exit code: 0
- passed: 4
- failed: 0
- skipped: 0
- pytest duration: 5.54s
- command duration: 11s

## Log / Evidence

```text
....                                                                     [100%]
4 passed in 5.54s
```

Automated assertions は `PARTITION_INDEX` artifact、source snapshot、group/class summary、TEST selection contract、PREDICTIVE execution、stage namespace/name/version、Dataset/View lineage、422 error code/path、split-only capabilities を検証する。

## Findings

- product defect: none
- test infrastructure issue: none
- regression: none
- deviation: none
- none: true

## Decision Rationale

API/artifact/lineage の全 canonical assertions が成功したため PASS。

## Source Modification by Test Agent

NONE
