# G6 Trial 001 Test 002 — cross_analysis_lineage

- Gate: G6
- Trial: 001
- Test item: 002
- Status: FAIL
- Tested implementation commit: `265b69a3317a0b9747cacee457e72b36a62daa7e`
- Handoff report commit / path: `963f1f2` / `docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/G6_001_implementation_completion_report.md`
- Branch: `prototype/ariadne_mvp_e3`
- Migration head: `20260807_product_0006`
- Started at: 2026-08-07T12:32:15Z
- Finished at: 2026-08-07T12:32:32Z

## Purpose

ContextからDataset/View、Explore/Causal/Predictive draft、Execution/Result/Artifact、Annotation、RERUN/REVISEDまでのcross-analysis lineageとproject boundaryを検証する。

## Acceptance Criteria

Context → Dataset、Dataset → View、Explore → Causal draft、Explore → Predictive draft、Execution → Result → Artifact、Result → Annotation、RERUN/REVISED lineage、same-project restriction。

## Preconditions / Environment

- Canonical file `tests/product/test_cross_analysis_lineage_e3.py`は存在する。
- current automated tests全体をread-only検索した。

## Commands Executed

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q --collect-only tests/product/test_cross_analysis_lineage_e3.py
rg -n 'REVISED_FROM|RERUN|Result.*Annotation|Context.*Dataset|DatasetVersion.*AnalysisView|MOTIVATED|USED_INPUT' tests/product
sed -n '1,240p' tests/product/test_cross_analysis_lineage_e3.py
```

## Exact Result

- read-only coverage audit exit code: 0
- canonical tests collected: 2
- canonical tests executed: 0
- missing mandatory direct assertions: 4 relationship classes
- duration: within initial 17s coverage/static audit

## Log / Evidence

- Canonical test asserts DatasetVersion → Execution、Execution → Result、explicit Result → Result、cross-project link rejection。
- Existing earlier-family tests assert RERUN/REVISED and selected Result/Artifact relationships。
- No direct assertion was found for Context → Dataset、Dataset → View、Explore → Causal draft、Result → Annotation。
- Explore → Predictive draft is created in the full API E2E, but the resulting source/target edge identity is not directly asserted。

## Findings

- Failure category: REQUIRED_TEST_COVERAGE_MISSING
- Missing contract: mandatory cross-analysis lineage relationship assertions listed above.
- Expected test scope: automated assertions over each required relationship and same-project restriction.
- Observed existing coverage: partial lineage plus cross-project explicit-link rejection.
- product defect: not established
- test infrastructure issue: none
- regression: not evaluated

## Required Correction

次trialでは、07bが列挙するcross-analysis lineage関係を直接検証するautomated evidenceが必要。

## Decision Rationale

07b §17はcritical contractのautomated testが存在しない場合をFAILと定義する。部分的なlineage coverageではG6-002をPASSにできない。

## Source Modification by Test Agent

NONE
