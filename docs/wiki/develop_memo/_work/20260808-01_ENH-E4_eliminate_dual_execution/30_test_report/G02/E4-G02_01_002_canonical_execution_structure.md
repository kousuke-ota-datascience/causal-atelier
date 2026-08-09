# E4-G02 Trial 01 — Test Item 002

- Tested implementation commit: `166e90cd1c2d0e523fb863795a88343403d8cc44`
- Current HEAD: `e3cbf212c859baf151ea2f1e9c917a7d0c9ba169`
- Environment: Python 3.12 via repository `uv`, pytest
- Result: **PASS**

## Evidence

Exact command:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e4_g02_canonical_execution.py::test_g02_001_one_execution_identity_contract_supports_all_families tests/product/test_enh_e4_g02_canonical_execution.py::test_g02_002_common_state_machine_rejects_invalid_terminal_transition tests/product/test_enh_e4_g02_canonical_execution.py::test_g02_003_retry_keeps_identity_and_distinguishes_occurrence tests/product/test_enh_e4_g02_canonical_execution.py::test_g02_004_rerun_and_revise_use_new_typed_base_identity tests/product/test_enh_e4_g02_canonical_execution.py::test_g02_005_lease_is_explicit_and_clearable
```

Exit code `0`; result `5 passed in 1.31s`. The source audit found one `Execution` contract with the three `AnalysisFamily` values, persistent `analysis_family`, globally generated `execution_id`, and `SqlExecutionRepository` as the canonical persistence authority. A real DB persistence proof is covered by Items 003/006.

Raw log: `/tmp/e4-g02-001-004-005.log`.

## Acceptance mapping

AC-001: **PASS**.
