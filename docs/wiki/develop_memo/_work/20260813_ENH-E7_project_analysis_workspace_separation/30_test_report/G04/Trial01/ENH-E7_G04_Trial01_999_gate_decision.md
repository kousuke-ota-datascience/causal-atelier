# G04 Trial01 Gate Decision

- Decision: **FAIL**
- Fixed Trial Candidate full SHA: `4f9efd1a738303fba49a245511faf7ca3ba333b7`
- Tested Repository State full SHA: `ff6bf3b1f5dcb1c9630184fdcd7932fed510ecc6`

## Decision basis

All blocking items must PASS. Item 010 is FAIL (`.venv/bin/pytest -q`: `9 failed, 387 passed, 33 skipped`), so Gate 07 section 10 requires FAIL.

## AC support and direct-predicate summary

| AC | Supporting items | Direct predicate/result |
|---|---|---|
| 01 | 002, 008, 009 | root uses replace to `/projects`; browser normalization/history PASS |
| 02 | 002 | canonical Project route classifier/serializer PASS |
| 03 | 003 | PM URL/selected-nav/surface predicates PASS |
| 04 | 004 | context selection does not rewrite Analysis route PASS |
| 05 | 004, 008 | catalog default, selected Family/Stage, browser switch PASS |
| 06 | 005, 008 | PM→Analysis PASS |
| 07 | 005, 008 | Analysis→PM PASS |
| 08 | 005, 008 | Analysis→Results PASS |
| 09 | 002, 005, 009 | reload/back/forward and pathname/surface/project predicates PASS |
| 10 | 006 | legacy analytical URL normalization PASS |
| 11 | 006 | resource route round trip / restore authority PASS |
| 12 | 007 | operation-contract predicates PASS |
| 13 | 003–005, 008, 010 | focused/browser PASS, but protected full regression FAIL |
| 14 | 005, 008, 009 | exactly-one surface and no console/page error PASS |
| 15 | 010 | protected full regression FAIL |

## Facts

Candidate identity audit passed. Focused G04 tests (`20 passed`) and Chromium journey (`PASS`) passed. Full product suite failed in nine tests.

## Interpretation

The evidence directly demonstrates a blocking protected-regression failure. No implementation was modified by this Test Agent.

## Reproduction procedure

Run each command in items 002–010, especially `.venv/bin/pytest -q` for the blocking failure.
