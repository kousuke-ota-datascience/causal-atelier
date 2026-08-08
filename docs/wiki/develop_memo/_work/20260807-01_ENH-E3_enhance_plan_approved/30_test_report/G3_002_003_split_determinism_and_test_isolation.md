# G3 Trial 002 Test 003 — split_determinism_and_test_isolation

- Gate: G3
- Trial: 002
- Test item: 003
- Status: PASS
- Tested implementation commit: `fd4e332939f93cc35adbf4a03929818e47c04b7e`
- Handoff report commit / path: `908ce954e4f155560861c91fae169cbe35f63866` / `20_implementation_reports/G3_002_implementation_completion_report.md`
- Branch: `prototype/ariadne_mvp_e3`
- Migration head: `20260807_product_0004`
- Started at: `2026-08-07T08:16:29Z`
- Finished at: `2026-08-07T08:16:44Z`

## Purpose

4 split strategies の決定性、partition isolation、temporal ordering、TEST isolation を検証する。

## Acceptance Criteria

- RANDOM / STRATIFIED / GROUP / TIME_BASED
- same input/specification/seed の deterministic partition
- overlap なし、population union、group isolation、strict time ordering
- TEST selection 不可、final evaluation only metadata

## Preconditions / Environment

- `UV_CACHE_DIR=/tmp/ariadne-uv-cache`
- `PYTHONDONTWRITEBYTECODE=1`
- TEST artifact metadata は item 004 canonical test と併せて確認した。

## Commands Executed

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q tests/product/test_predictive_split_e3.py
```

## Exact Result

- exit code: 0
- passed: 6
- failed: 0
- skipped: 0
- pytest duration: 5.72s
- command duration: 15s

## Log / Evidence

```text
......                                                                   [100%]
6 passed in 5.72s
```

4 strategies、same-seed determinism、partition completeness/isolation、group separation、exact temporal boundaries、time reversal rejection、TRAIN-only fit、TEST selection rejection を確認した。Item 004 で `selection_allowed=false` / `final_evaluation_only=true` も確認した。

## Findings

- product defect: none
- test infrastructure issue: none
- regression: none
- deviation: none
- none: true

## Decision Rationale

Split determinism/isolation の全必須 contract が automated assertions で成立したため PASS。

## Source Modification by Test Agent

NONE
