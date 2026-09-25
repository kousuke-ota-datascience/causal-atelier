# ENH-E9 G03 Trial 01 P01 — Package Status

- Gate: G03
- Package: P01
- Trial: 01
- State: PACKAGE_COMPLETE
- Normative contract: `10_enhance_instruction/G03/06_G03_P01_identification_input_ergonomics.md` (FROZEN)
- START_SHA: `d86983696f614cfc44bfddf97f720dd07f9598ae`
- PACKAGE_CHECKPOINT_SHA: `f11be531dc34b7fbbf6aa8f1d74aaf28e0205e35`

## Dependency evidence

`30_test_report/G02/Trial01/ENH-E9-G02_01__999_gate_decision.md` is the exactly-one current canonical G02 decision and records `Status: 999 / PASS` and `PASS — PROMOTION_ALLOWED`.

## Implemented scope

- Added Population and Comparator tooltips that explain target population and counterfactual/reference-condition meaning without changing their fields or serialization.
- Replaced the free-text Identification Treatment field with a selector populated only from the selected Dataset Version schema.
- Made absent dataset/schema an explicitly disabled empty state, retained valid current Treatment values, and cleared/announced stale values after Dataset Version changes.
- Preserved the selected FIXED Graph's read-only Outcome projection and existing Identification Result → Estimation prefill lineage.
- Updated the existing Estimation regression assertions from obsolete loader/button literals to the current equivalent runtime implementation; this does not change production behavior.

## Changed files

- `frontend/index.html`
- `frontend/app.js`
- `tests/enhancement/enh_e9/g03/frontend/test_identification_input_ergonomics.py`
- `tests/enhancement/enh_e9/g03/frontend/test_estimation_submission_regression.py`

## Focused verification

```text
node --check frontend/app.js
uv run pytest -q \
  tests/enhancement/enh_e9/g03/frontend/test_identification_input_ergonomics.py \
  tests/enhancement/enh_e9/g03/frontend/test_estimation_submission_regression.py
```

Result: PASS — JavaScript syntax check passed; pytest reported `7 passed in 2.44s`.

The deterministic tests cover Population/Comparator help, Dataset A schema-only candidates, unavailable schema, valid Treatment retention, Dataset A→B stale-value invalidation, unchanged Treatment serialization field semantics, read-only Graph Outcome projection, and existing Identification→Estimation lineage.

## Remaining work / blockers

None within P01. Browser E2E is intentionally deferred to Gate-level Independent Verification.
