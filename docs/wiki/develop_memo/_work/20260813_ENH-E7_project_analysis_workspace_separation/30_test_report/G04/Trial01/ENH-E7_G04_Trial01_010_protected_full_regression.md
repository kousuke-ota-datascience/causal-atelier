# 010 protected_full_regression

- Result: FAIL
- Fixed Trial Candidate full SHA: `4f9efd1a738303fba49a245511faf7ca3ba333b7`
- Tested Repository State full SHA: `ff6bf3b1f5dcb1c9630184fdcd7932fed510ecc6`
- Exact command / method: `.venv/bin/pytest -q`
- Exit code: 1

## AC mapping

AC-G04-13, AC-G04-15.

## Direct assertion / predicate mapping

Protected full suite must pass: G03 structural contract, G01/G02 semantics, ENH-E6 semantics, backend/API/persistence.

## Raw relevant evidence

`9 failed, 387 passed, 33 skipped, 1 warning in 107.94s`. Failing tests: `test_domain_and_snapshot.py::test_scientific_status_is_exact_design_contract`; two `test_enh_e2_contract.py` tests (expected 202/409, received 400); `test_enh_e3_api_worker_e2e.py` cross-family E2E and six-route contract; `test_exploratory_frontend_contract_e3.py`; `test_predictive_explanation_e3.py`; two `test_predictive_frontend_contract_e3.py` route/workspace contract tests.

## Facts

The full protected suite has verified failures. Frontend failures expect legacy `explore`/`predictive` route/workspace tokens absent from the current HTML; API failures observe documented status/body mismatches.

## Interpretation

AC-G04-15 fails. This is a testable candidate with verified protected-regression violations; per Gate 07, this yields FAIL, not BLOCKED. Attribution to G04 itself is not established by this test alone, but Gate acceptance requires the protected suite to pass.

## Protected contract relation

G01/G02/ENH-E6 and backend/API/persistence protected regression.

## Reproduction procedure

Run the command above.

## Browser evidence

G04-specific Chromium journey passed; it does not override the blocking full-regression failure.
