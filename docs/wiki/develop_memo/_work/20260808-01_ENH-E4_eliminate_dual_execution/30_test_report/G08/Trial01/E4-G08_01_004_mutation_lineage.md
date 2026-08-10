# E4-G08 Trial01 — Item 004 Mutation + Lineage

Result: **PASS** (AC-003)

| Operation / relation | Result | Evidence |
|---|---:|---|
| retry retains same Execution ID | PASS | `test_enh_e4_g05_phase_c_retry_postgres.py` |
| rerun creates new ID, base ID, `RERUN`, typed `DERIVED_FROM` | PASS | `test_enh_e4_g05_phase_c_rerun_postgres.py`, G06 selections |
| revise creates new ID, base ID, `REVISED`, reason, typed `REVISED_FROM` | PASS | `test_enh_e4_g05_phase_c_revise_postgres.py`, G06 selections |
| cancel is canonical Execution transition | PASS | G05 D3 authority audit |
| typed structural / GENERIC_ONLY / derived projection authority | PASS | G06 P01–P06 PostgreSQL and local selections |

The PostgreSQL selection passed 23 tests. Structural generic duplicate persistence was not observed by the selected authority tests.
