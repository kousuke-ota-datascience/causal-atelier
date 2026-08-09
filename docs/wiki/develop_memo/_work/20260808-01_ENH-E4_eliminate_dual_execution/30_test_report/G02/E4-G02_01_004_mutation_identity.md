# E4-G02 Trial 01 — Test Item 004

- Tested implementation commit: `166e90cd1c2d0e523fb863795a88343403d8cc44`
- Current HEAD: `e3cbf212c859baf151ea2f1e9c917a7d0c9ba169`
- Environment: Python 3.12 via repository `uv`, pytest
- Result: **PASS**

Exact command was the targeted G02 command recorded in Item 002. Exit code `0`; `5 passed`. The mapped nodes `test_g02_003` and `test_g02_004` passed: retry retains the execution ID and increments retry occurrence; rerun/revise create new IDs with typed `base_execution_id` and distinct `revision_kind`. Domain cancellation rules were inspected; no silent terminal cancellation acceptance was found in the canonical entity.

Raw log: `/tmp/e4-g02-001-004-005.log`.

## Acceptance mapping

AC-003: **PASS**.
