# E4-G03_01_002 Product Migration / Stage Schema

- Implementation commit: `f455354e3724b66360bed6d3cfd4646ca1463a89`
- Exact command: `scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g03_persistent_stage_execution.py tests/product/test_postgres_contract.py tests/product/test_enh_e4_g02_canonical_execution.py`
- Raw evidence: `/tmp/ariadne-g03-evidence/`

## Findings

Migration `20260809_product_0008` has parent `20260809_product_0007`, creates `product_stage_execution` and append-only `product_stage_attempt`, and declares the required FK, uniqueness, status, ordinal, and attempt-number constraints. The standard runner reset a clean `ariadne_test`, applied Product migrations only, reported `20260809_product_0008 (head)`, and exited 0. Root legacy migration was not invoked.

The runtime test passed the persistent round-trip item, but does not independently cover every schema field and lifecycle constraint listed by the contract.

## Status

`PASS` for migration/schema existence and clean Product migration. Coverage limitations are recorded in Items 003–007.
