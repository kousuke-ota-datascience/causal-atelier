# E5-G01 Trial 03 — Test Item 999: Gate Decision

## Gate Decision

`FAIL`

## Inputs and evidence

| Field | Value |
|---|---|
| Gate | `G01` |
| Trial | `03` |
| `TEST_START_SHA` | `faabf7275642b43e3481e6256c30a9b45b3679b8` |
| `FIXED_TRIAL_CANDIDATE_SHA` | `27e87faecd2b5dac0da6a688201931456c1a6077` |
| Test target | `faabf7275642b43e3481e6256c30a9b45b3679b8` (candidate-equivalent semantic state) |
| Completed Test Items | `001 PASS`, `002 PASS`, `003 FAIL`, `004 PASS` |
| Independent suite | `14 passed in 4.35s` |

## Failed Acceptance Criteria

`AC-G01-003` and `AC-G01-007` fail. Operation Availability accepts `/projects/p1/analysis/causal/unknown-stage` and returns a normal HTTP-200-shaped operation projection with `RESOURCE_REQUIRED`. Gate 07 requires unknown Stage / malformed or unknown canonical route handling as `INVALID_NAVIGATION_ROUTE` (HTTP 422).

See `E5-G01_03__003_operation_availability.md` for raw reproducer output.

## Promotion eligibility

`PROMOTION_NOT_ALLOWED`
