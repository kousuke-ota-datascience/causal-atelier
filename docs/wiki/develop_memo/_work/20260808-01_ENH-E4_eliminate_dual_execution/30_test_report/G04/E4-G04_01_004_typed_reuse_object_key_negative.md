# E4-G04 Trial 01 Test 004 — Artifact Semantic ID / Typed Downstream Reuse

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G04
- Trial: 01
- Test Item ID (3-digit): 004
- Status: FAIL
- Tested implementation commit: 3d88781c1b69ba03bb06c0b8f143612b81feb4bf
- Handoff report path: docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G04/E4-G04_01_implementation_completion_report.md
- Branch: refactor/ariadne_mvp_e4
- Migration head: 20260809_product_0009
- Working directory: /loc0/bigbrother/repositories/causal-atelier
- Started at: 2026-08-09T05:35:49Z
- Finished at: 2026-08-09T05:40:17Z
- Duration: 4 minutes 28 seconds

## 1. Purpose
Verify that downstream Result/Artifact reuse has typed semantic identity and rejects physical locators and hashes as identity.

## 2. Acceptance Criteria
E4-G04-AC-004 and the typed-reuse part of E4-G04-AC-002.

## 3. Preconditions / Environment
### Runtime
Python 3.12.13; source/static audit and repository-managed pytest.
### External Services
NONE for the unit test.
### Environment Variables
`UV_CACHE_DIR=/tmp/ariadne-uv-cache`; `PYTHONDONTWRITEBYTECODE=1`.

## 4. Commands Executed
`UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_enh_e4_g03_generic_executor_boundary.py`

`rg -n -C 2 'input_result_id|ResultReuseRef|role|context|object_key|content_hash' src/ariadne/product/application/output_ownership_service.py src/ariadne/product/domain/execution.py tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_enh_e4_g04_result_artifact_postgres.py`

## 5. Exact Result
- passed: 12 unit tests
- failed: 1 audit finding
- skipped: 0
- warnings: 0
- exit code: 1

## 6. Log / Evidence
### stdout / stderr
Pytest output: `12 passed in 1.42s`. Static audit found `ResultReuseRef` has exactly one field, `result_id: str`; neither its API nor its test supplies or validates a typed role/context.
### Failure traceback / assertion
Contract failure: 06 §11.1 and 07 item 004 require Result reuse to use `Result ID + typed role/context`. The implementation at `src/ariadne/product/application/output_ownership_service.py` defines only `ResultReuseRef.result_id` and `reuse_result()` resolves only that ID.
### Artifact paths
NONE.

## 7. Findings
Fact: object-key string inputs are rejected by type checking and Artifact reuse uses `artifact_id`. Fact: no typed Result role/context exists. Conclusion: AC-004 is not satisfied even though the current object-key negative test passes. The current test also does not demonstrate the required hash-only and object-key-only ownership negatives independently.

## 8. Required Correction
Add a typed Result reuse reference containing the required role/context and validate it in the canonical reuse boundary. Add automated negatives for object_key-only Artifact ownership and content_hash-only semantic identity. Do not treat physical locators or hashes as semantic IDs.

## 9. Reproduction Procedure
Run the unit command in section 4, then inspect `ResultReuseRef` and `reuse_result` with the rg command in section 4.

## 10. Expected Result
Result reuse requires an explicit typed role/context in addition to `result_id`; object keys and hashes cannot fulfill semantic identity or ownership.

## 11. Decision Rationale
The required Result ID plus typed role/context contract is absent. This is an implementation defect, not an environment blocker.

## 12. Source Modification by Test Agent
NONE. Only test evidence documents were created.

## 13. Supplemental Execution Context
The unit test’s TypeError check proves only that an unwrapped string is rejected; it does not prove the missing role/context requirement.
