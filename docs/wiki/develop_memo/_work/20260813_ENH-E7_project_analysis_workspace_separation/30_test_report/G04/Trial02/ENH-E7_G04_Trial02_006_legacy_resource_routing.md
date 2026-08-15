# 006 legacy_resource_routing

- Result: PASS
- Fixed Trial Candidate full SHA: `d2d5a9a7f6df352d787c8d561fce937012eef854`
- Tested Repository State full SHA: `9e85e4a6a2365869b48e5bc6c0b0ac6845698869`
- Exact command / method: `.venv/bin/pytest -q tests/product/test_enh_e7_g04_p05_legacy_operation_resource_regression.py`
- Exit code: 0

## AC mapping

AC-G04-10, AC-G04-11.

## Direct assertion / predicate mapping

The four tests assert legacy/resource routing remains canonical Analysis semantics, Data Quality read-only behavior and Exploratory result contracts, presentation-only Causal/Predictive stage navigation, and resource-authoritative restore without backend/persistence change.

## Raw relevant evidence

`4 passed` in `test_enh_e7_g04_p05_legacy_operation_resource_regression.py`.

## Facts

All canonical-route, legacy/resource restore, and operation-boundary predicates passed.

## Interpretation

Legacy URLs normalize into the current Family/Stage architecture; no historical six-route or independent-workspace requirement was used.

## Protected contract relation

G02 legacy cutover and Project resource route semantics.

## Reproduction procedure

Run the command above.

## Browser evidence

Item 008 provides Chromium route/history evidence; this Item supplies the direct routing/resource predicates.
