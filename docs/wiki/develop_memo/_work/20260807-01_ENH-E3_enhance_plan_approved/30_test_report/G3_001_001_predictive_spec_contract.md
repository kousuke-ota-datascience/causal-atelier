# G3 Trial 001 Test 001 — predictive_spec_contract

- Gate: G3
- Trial: 001
- Test item: 001
- Status: FAIL
- Tested implementation commit: `73a92c1b5899bc0d072df0faf8621b5171b00e5a`
- Handoff report commit / path: `6540499bcf062b6af9dfe251b156e833a5142c06` / `20_implementation_reports/G3_001_implementation_completion_report.md`
- Branch: `prototype/ariadne_mvp_e3`
- Migration head: `20260807_product_0004`
- Started at: `2026-08-07T08:04:22Z`
- Finished at: `2026-08-07T08:04:32Z`

## Purpose

Predictive Specification の型、必須 field、strict validation、task/metric compatibility、および canonical/deterministic behavior の automated test coverage を検証する。

## Acceptance Criteria

- `BINARY_CLASSIFICATION` / `REGRESSION` を受け付ける。
- unsupported task、unknown field、missing prediction question field、duplicate feature、task/metric mismatch を reject する。
- specification の canonical/deterministic behavior を automated assertion で検証する。

## Preconditions / Environment

- Current HEAD: `6540499bcf062b6af9dfe251b156e833a5142c06`
- implementation commit 後の source / migration / automated test code 差分: 0
- Python execution: `uv run`
- `UV_CACHE_DIR=/tmp/ariadne-uv-cache`
- `PYTHONDONTWRITEBYTECODE=1`

## Commands Executed

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q tests/product/test_predictive_spec_e3.py

rg -n "canonical|determin|canonical_hash|canonical_bytes|specification_hash" \
  tests/product/test_predictive_spec_e3.py \
  tests/product/test_predictive_split_api_e3.py \
  tests/product/test_predictive_split_e3.py

rg -n "predictive-analysis-spec/1|validate_predictive_specification|specification_hash|canonical_hash|canonical_bytes" \
  tests -g '*.py'
```

## Exact Result

- pytest exit code: 0
- passed: 4
- failed: 0
- skipped: 0
- pytest duration: 3.40s
- command wall duration: 10s
- coverage audit: required canonical/deterministic Predictive Specification assertion 0件

## Log / Evidence

```text
....                                                                     [100%]
4 passed in 3.40s
```

`tests/product/test_predictive_spec_e3.py` は task acceptance/rejection、availability、metric mismatch、unknown/missing/duplicate field、stratify ambiguity を検証する。一方、Predictive Specification の key-order independence、canonical bytes/hash stability、または同一 specification の deterministic identity を assert する test は存在しない。`tests/product/test_enh_e3_workflow_core.py` には generic canonical hash test があるが、Predictive Specification validator/envelope を対象としていない。

## Findings

- product defect: none established by the executed pytest
- test infrastructure issue: none
- regression: not evaluated in this item
- deviation: `REQUIRED_TEST_COVERAGE_MISSING`
- none: false

```text
Failure category: REQUIRED_TEST_COVERAGE_MISSING
Missing contract: Predictive Specification canonical/deterministic behavior
Expected test scope: tests/product/test_predictive_spec_e3.py で、意味的に同一の specification が key order 等に依存せず canonical/deterministic identity を持つことを assert する
Observed existing coverage: generic canonical_hash の test は存在するが、Predictive Specification を対象とする assertion は存在しない
```

## Required Correction

Predictive Specification の canonical/deterministic behavior を直接検証する automated test coverage が必要である。

## Decision Rationale

Canonical pytest の既存 assertion は全て成功した。しかしテスト指示書 G3-001 の必須 contract が automated test で検証されていないため、同書 §17 に従い FAIL とする。既存 test の PASS は coverage 欠落を補完しない。

## Source Modification by Test Agent

NONE
