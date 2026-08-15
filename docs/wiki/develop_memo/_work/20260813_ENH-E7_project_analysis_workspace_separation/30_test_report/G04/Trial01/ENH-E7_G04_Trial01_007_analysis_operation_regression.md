# 007 analysis_operation_regression

- Result: PASS
- Fixed Trial Candidate full SHA: `4f9efd1a738303fba49a245511faf7ca3ba333b7`
- Tested Repository State full SHA: `ff6bf3b1f5dcb1c9630184fdcd7932fed510ecc6`
- Exact command / method: `.venv/bin/pytest -q tests/product/test_enh_e7_g04_p05_legacy_operation_resource_regression.py`
- Exit code: 0

## AC mapping

AC-G04-12.

## Direct assertion / predicate mapping

Data Quality is read-only with no exploration execution/preview endpoint; TIME_TREND and CHART retain required output/artifact contracts; Causal/Predictive stage navigation is presentation-only and has no execution submission.

## Raw relevant evidence

Focused P05 contains and passed direct assertions for `GROUP_SUMMARY_RESULT`, `exploratory-time-trend-result/1`, `CHART_RESULT`, `exploratory-chart-result/1`, Chart specification artifact media type, and absence of prohibited POST routes.

## Facts

The specified protected operation predicates passed.

## Interpretation

Within the direct operation-contract coverage, AC-G04-12 passes.

## Protected contract relation

Existing Causal/Exploratory/Predictive semantics.

## Reproduction procedure

Run the command above.

## Browser evidence

Not applicable; primary layer is frontend/API integration assertions.
