# E4-G03_01_008 G02 Regression / PostgreSQL Contract

- Implementation commit: `f455354e3724b66360bed6d3cfd4646ca1463a89`
- Exact command: `scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g03_persistent_stage_execution.py tests/product/test_postgres_contract.py tests/product/test_enh_e4_g02_canonical_execution.py`
- Result: migration exit 0, `10 passed`, pytest exit 0, outer runner exit 0
- Raw evidence: `/tmp/ariadne-g03-evidence/`

## Findings

The G03 persistence test, PostgreSQL contract (including concurrent claim), and five G02 regression tests all passed through the repository-managed runner. Migration head was `20260809_product_0008`.

## Status

`PASS`
