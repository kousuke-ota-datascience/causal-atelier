# E4-G03_01_999 Gate Decision

## Metadata

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G03 Persistent StageExecution and runner boundary
- Trial: 01
- Baseline: `cb28a18c07cad00cf12f01e9124651aa45aab16f`
- Implementation commit: `f455354e3724b66360bed6d3cfd4646ca1463a89`
- Evidence/report commit: `692a8b8899f5c862826648f2f03d88b45bf51c4f`

## Decision

`FAIL`

This is a required-test-coverage failure, not an environment failure. The repository-managed PostgreSQL runner worked and the requested migration/G03/G02 tests passed. However, the declared G03 test suite does not independently verify the mandatory cross-family persistence, retry attempt history, failure/cancel/lease consistency, GenericExecutor behavioral negative, and atomic materialization rollback scenarios. The instruction explicitly treats required automated-test coverage defects as FAIL.

## Acceptance Criteria

| Criterion | Status | Reason |
|---|---|---|
| E4-G03-AC-001 | FAIL | Cross-family persistence and atomic negative coverage incomplete |
| E4-G03-AC-002 | FAIL | Query/attempt-history and lifecycle coverage incomplete |
| E4-G03-AC-003 | FAIL | GenericExecutor static check passes; behavior negative coverage absent |
| E4-G03-AC-004 | FAIL | Causal-only round-trip; cross-family/rollback negatives absent |
| E4-G03-AC-005 | FAIL | G02 regression passes, but failure/retry/cancel/lease mandatory scenarios absent |

## Executed Evidence

- GenericExecutor boundary: `5 passed`, exit 0.
- Standard runner: Product migration `20260809_product_0008 (head)`, G03 persistence + PostgreSQL contract + G02 regression `10 passed`, exit 0.
- Full `uv run pytest -q`: failed in two PostgreSQL tests against pre-existing external `ariadne_g02_test` at `172.17.0.1:55432`, because `product_stage_execution` is absent. This is not used as a G03 implementation failure because G03 mandates the standardized runner; it is recorded as environment/configuration evidence.
- Raw standardized-runner evidence: `/tmp/ariadne-g03-evidence/`.

## Scope / Integrity

No production source, tests, migrations, dependencies, compose, or infrastructure were modified by the Test Agent. The `.nfs` deletion and operator instruction files remain unrelated working-tree state. `E4-TD-001` and `E4-TD-002` remain OPEN until G05. G04+ implementation was not started.

## Blocking Defects

The next Coding Trial must add the missing required automated coverage or otherwise provide equivalent fixed evidence. The Test Agent did not modify implementation or tests.
