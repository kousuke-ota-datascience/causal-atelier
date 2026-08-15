# 006 legacy_resource_routing

- Result: PASS
- Fixed Trial Candidate full SHA: `4f9efd1a738303fba49a245511faf7ca3ba333b7`
- Tested Repository State full SHA: `ff6bf3b1f5dcb1c9630184fdcd7932fed510ecc6`
- Exact command / method: `.venv/bin/pytest -q tests/product/test_enh_e7_g04_p05_legacy_operation_resource_regression.py`
- Exit code: 0

## AC mapping

AC-G04-10, AC-G04-11.

## Direct assertion / predicate mapping

Legacy explore/predictive/causal URLs serialize to canonical Analysis URLs; a resource route round-trips identically; restore uses resource authority without POST/PUT.

## Raw relevant evidence

`4 passed` in the focused suite. Assertions directly inspect parsed/serialized URLs and restore handler restrictions.

## Facts

All legacy and resource routing predicates passed.

## Interpretation

Legacy analytical URL normalization and resource route semantics pass.

## Protected contract relation

G02 legacy cutover semantics.

## Reproduction procedure

Run the command above.

## Browser evidence

Not independently exercised by the Chromium runner; frontend direct assertions are the primary evidence.
