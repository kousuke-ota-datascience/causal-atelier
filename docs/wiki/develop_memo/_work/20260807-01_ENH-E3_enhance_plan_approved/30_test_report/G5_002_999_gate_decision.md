# G5 Trial 002 Gate Decision

- Status: BLOCKED
- Tested implementation commit: 4a83bb6860c895f00e4dfd7c9e7880105387373e
- Handoff report: 4ccbfbb196ba384aa362450666c00b4c936c58d7 / docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/G5_002_implementation_completion_report.md
- Test report set: G5_002_001 through G5_002_008 and G5_002_999
- Migration head: 20260807_product_0005
- Test Agent source modification: NONE

## Item Summary

| Item | Name | Status | Report |
|---:|---|:---:|---|
| 001 | predictive_explanation_contract | PASS | [G5_002_001_predictive_explanation_contract.md](G5_002_001_predictive_explanation_contract.md) |
| 002 | model_card_lineage | PASS | [G5_002_002_model_card_lineage.md](G5_002_002_model_card_lineage.md) |
| 003 | predictive_frontend_contract | PASS | [G5_002_003_predictive_frontend_contract.md](G5_002_003_predictive_frontend_contract.md) |
| 004 | predictive_browser_e2e | BLOCKED | [G5_002_004_predictive_browser_e2e.md](G5_002_004_predictive_browser_e2e.md) |
| 005 | terminology_and_causal_claim_guard | PASS | [G5_002_005_terminology_and_causal_claim_guard.md](G5_002_005_terminology_and_causal_claim_guard.md) |
| 006 | g1_g4_regression | PASS | [G5_002_006_g1_g4_regression.md](G5_002_006_g1_g4_regression.md) |
| 007 | full_active_pytest | PASS | [G5_002_007_full_active_pytest.md](G5_002_007_full_active_pytest.md) |
| 008 | static_dependency_and_diff_checks | PASS | [G5_002_008_static_dependency_and_diff_checks.md](G5_002_008_static_dependency_and_diff_checks.md) |

## Gate Acceptance Summary

- G5-001/002/003/005/006/007/008: PASS.
- Trial 001 missing coverage: all detected as corrected; canonical suites passed.
- PostgreSQL persistence: PASS; single head, Explanation/Model Card Result and Artifact persistence, 37 lineage edges.
- G5-004 Browser: BLOCKED before Chromium launch because canonical Browser image cannot be built.

## Blocking Findings

- Category: TEST_INFRASTRUCTURE_BUILD_CONTEXT_MISMATCH
- Host file `tests/browser_e2e/run_enh_e3_predictive.py` exists.
- `.dockerignore` excludes `tests/browser_e2e/*` and only re-includes `run_enh_e1a.py`.
- `Dockerfile.browser-e2e` requires `COPY tests/browser_e2e/run_enh_e3_predictive.py`, causing deterministic build failure.
- Browser product behavior and the new error-rendering scenario were not executed.

## Regression Summary

- G1〜G4 targeted: 57 passed, 0 failed, 0 skipped.
- Full active pytest: 182 passed, 0 failed, 4 skipped.
- Non-Browser regression: none observed.

## Scientific / Analytical Contract Summary

- Predictive explanation/model card suite: 5 passed.
- strict TEST-only explanation, deterministic global/local contribution, output scales, NOT_APPLICABLE, Model Card semantic values, complete lineage, and Artifact terminology guard passed.
- Real PostgreSQL persistence contract passed.

## Reason for Decision

**Fact:** All non-Browser required items passed. The Browser runner failed at Docker build before Chromium or product scenarios started.

**Cause evidence:** The build context excludes the exact file newly referenced by `Dockerfile.browser-e2e`. This is deterministic and independent of Browser product behavior.

**Alternative hypothesis:** Running the host runner through an ad-hoc bind mount or using the stale pre-Trial image could exercise some UI behavior. That would bypass the canonical packaging contract and would not validate the delivered Browser test infrastructure, so it was not adopted.

Under instruction section 18, product-defect determination is impossible because the required test infrastructure is broken. Therefore G5 Trial 002 is BLOCKED, not FAIL and not PASS.

## Next Allowed Action

- BLOCKED: Product code must not be changed solely to bypass the block.
- The canonical Browser test infrastructure must become buildable before G5 can be decided.

