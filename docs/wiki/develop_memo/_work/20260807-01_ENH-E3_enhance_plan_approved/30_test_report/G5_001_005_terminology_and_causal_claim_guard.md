# G5 Trial 001 Test 005 — terminology_and_causal_claim_guard

- Gate: G5
- Trial: 001
- Test item: 005
- Status: FAIL
- Tested implementation commit: cb0f45164fe5190af37df466af70057b89b8c8cb
- Handoff report commit / path: d7b1c1a9a97d8c9474d628baa42824fa959caeff / docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/G5_001_implementation_completion_report.md
- Branch: prototype/ariadne_mvp_e3
- Migration head: 20260807_product_0005
- Started at: 2026-08-07T11:15:33Z
- Finished at: 2026-08-07T11:15:43Z

## Purpose

Predictive Explanation/feature importanceをcausal effectまたはTreatment Effectと誤表示しないことを監査する。

## Acceptance Criteria

Predictive/Causal/Treatment Effectの分離、predictive importanceをcausal effectと表示しない、一般predictive result名にeffectを用いない、Exportでも同様。

## Preconditions / Environment

- G4 Trial 003 Gate Decision: PASS
- Current handoff HEAD: d7b1c1a9a97d8c9474d628baa42824fa959caeff
- Test Agent source/test/migration modification: NONE

## Commands Executed

~~~bash
rg -n 'export|Export|manifest' \
  tests/product/test_predictive_explanation_e3.py \
  tests/product/test_predictive_frontend_contract_e3.py \
  tests/browser_e2e/run_enh_e3_predictive.py
rg -n 'Predictive Explanation|Treatment Effect' \
  tests/product/test_predictive_explanation_e3.py \
  tests/product/test_predictive_frontend_contract_e3.py
~~~

## Exact Result

- coverage audit exit code: 1
- explicit non-causal UI/Result assertions: present
- predictive export terminology assertion: absent
- tests executed: 0
- duration: 10s coverage audit

## Log / Evidence

- `/tmp/g5_001_required_coverage_audit.log`
- The sole `manifest` search match is `partition_manifest`, not Export coverage.
- Existing assertions verify visible non-causal wording but do not exercise predictive Result export.

## Findings

- Failure category: REQUIRED_TEST_COVERAGE_MISSING
- Missing contract: Export terminology/causal-claim guard for Predictive Explanation and Model Card.
- Expected test scope: automated exported-result/artifact contract that verifies predictive naming and absence of causal/effect claims outside the explicit limitation statement.
- Observed existing coverage: UI and in-memory Result limitation wording only.
- product defect: not established

## Required Correction

Add automated coverage for the missing predictive Export terminology contract. No product fix is prescribed by this report.

## Decision Rationale

Export is explicitly included in G5-005. Because it is untested, this critical coverage gap requires FAIL.

## Source Modification by Test Agent

NONE

