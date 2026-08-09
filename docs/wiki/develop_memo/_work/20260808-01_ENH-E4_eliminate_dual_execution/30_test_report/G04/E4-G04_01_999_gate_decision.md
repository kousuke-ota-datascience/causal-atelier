# E4-G04 Trial 01 Gate Decision

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G04
- Trial: 01
- Status: FAIL
- Tested implementation commit: 3d88781c1b69ba03bb06c0b8f143612b81feb4bf
- Handoff report path: docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G04/E4-G04_01_implementation_completion_report.md
- Branch: refactor/ariadne_mvp_e4
- Migration head: 20260809_product_0009
- Test Agent source modification: NONE. Only `30_test_report/G04/` evidence documents were created.

## 1. Item Summary
| Test Item ID (3-digit) | Name | Status | Report |
|---:|---|---|---|
| 001 | Commit / Report / Change Boundary Audit | PASS | `E4-G04_01_001_commit_report_change_boundary.md` |
| 002 | Product Migration / Result Level / Cardinality Audit | PASS | `E4-G04_01_002_result_schema_cardinality.md` |
| 003 | Canonical Result / Artifact Ownership Persistence | PASS | `E4-G04_01_003_result_artifact_ownership_persistence.md` |
| 004 | Artifact Semantic ID / Typed Downstream Reuse | FAIL | `E4-G04_01_004_typed_reuse_object_key_negative.md` |
| 005 | ArtifactStore Compensation / Reconciliation | FAIL | `E4-G04_01_005_artifact_store_compensation.md` |
| 006 | Artifact-Only Family Contract | PASS | `E4-G04_01_006_artifact_only_family_contract.md` |
| 007 | Canonical Ownership Service / GenericExecutor Boundary | PASS | `E4-G04_01_007_output_owner_generic_executor_boundary.md` |
| 008 | G02 / G03 / PostgreSQL Regression | PASS | `E4-G04_01_008_g02_g03_regression.md` |
| 009 | Transition Debt / Scope / Report-Format Audit | PASS | `E4-G04_01_009_transition_scope_report_format_audit.md` |

## 2. Gate Acceptance Summary
| Acceptance Criterion | Evidence | Status |
|---|---|---|
| E4-G04-AC-001 | 002, 003, 006 | SATISFIED |
| E4-G04-AC-002 | 002, 003, 007 | SATISFIED |
| E4-G04-AC-003 | 005 | NOT_SATISFIED |
| E4-G04-AC-004 | 004 | NOT_SATISFIED |
| E4-G04-AC-005 | 006 | SATISFIED |
| Product migration | 002 | SATISFIED |
| G02/G03 regression | 008 | SATISFIED |
| Transition debt / future-Gate boundary | 001, 009 | SATISFIED |
| Report format compliance | 001, 009 and this report | SATISFIED |

## 3. Blocking Findings
1. AC-004 is not satisfied: `ResultReuseRef` carries only `result_id`; 06 §11.1 requires Result ID plus typed role/context. The existing test proves only that an unwrapped string is rejected. See item 004.
2. AC-003 is not satisfied: DB failure/rollback durability is only tested with `MemoryUow`; 06 §15.3 and 07 item 005 require real PostgreSQL metadata durability/rollback evidence. See item 005.

## 4. Regression Summary
- Required regression scope: G02 canonical execution; G03 GenericExecutor boundary, persistent StageExecution, acceptance PostgreSQL; and PostgreSQL contract tests.
- Executed: Item 008; `ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g04-trial01-evidence scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_enh_e4_g04_result_artifact_postgres.py tests/product/test_enh_e4_g02_canonical_execution.py tests/product/test_enh_e4_g03_generic_executor_boundary.py tests/product/test_enh_e4_g03_persistent_stage_execution.py tests/product/test_enh_e4_g03_acceptance_postgres.py tests/product/test_postgres_contract.py`
- Result: PASS; 29 passed, runner exit code 0.

## 5. Scientific / Analytical Contract Summary
N/A. G04 preserves scientific payload/status semantics; this Gate verifies ownership, persistence, storage-boundary, and recovery contracts rather than a new scientific/statistical invariant.

## 6. Reproducibility Summary
| Test Item | Report | Primary Command |
|---|---|---|
| 001 | `E4-G04_01_001_commit_report_change_boundary.md` | `git diff --name-status 3d88781c1b69ba03bb06c0b8f143612b81feb4bf..HEAD` |
| 002 | `E4-G04_01_002_result_schema_cardinality.md` | `ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g04-trial01-evidence scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_enh_e4_g04_result_artifact_postgres.py tests/product/test_enh_e4_g02_canonical_execution.py tests/product/test_enh_e4_g03_generic_executor_boundary.py tests/product/test_enh_e4_g03_persistent_stage_execution.py tests/product/test_enh_e4_g03_acceptance_postgres.py tests/product/test_postgres_contract.py` |
| 003 | `E4-G04_01_003_result_artifact_ownership_persistence.md` | `ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g04-trial01-evidence scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_enh_e4_g04_result_artifact_postgres.py tests/product/test_enh_e4_g02_canonical_execution.py tests/product/test_enh_e4_g03_generic_executor_boundary.py tests/product/test_enh_e4_g03_persistent_stage_execution.py tests/product/test_enh_e4_g03_acceptance_postgres.py tests/product/test_postgres_contract.py` |
| 004 | `E4-G04_01_004_typed_reuse_object_key_negative.md` | `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_enh_e4_g03_generic_executor_boundary.py` |
| 005 | `E4-G04_01_005_artifact_store_compensation.md` | `ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g04-trial01-evidence scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_enh_e4_g04_result_artifact_postgres.py tests/product/test_enh_e4_g02_canonical_execution.py tests/product/test_enh_e4_g03_generic_executor_boundary.py tests/product/test_enh_e4_g03_persistent_stage_execution.py tests/product/test_enh_e4_g03_acceptance_postgres.py tests/product/test_postgres_contract.py` |
| 006 | `E4-G04_01_006_artifact_only_family_contract.md` | `ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g04-trial01-evidence scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_enh_e4_g04_result_artifact_postgres.py tests/product/test_enh_e4_g02_canonical_execution.py tests/product/test_enh_e4_g03_generic_executor_boundary.py tests/product/test_enh_e4_g03_persistent_stage_execution.py tests/product/test_enh_e4_g03_acceptance_postgres.py tests/product/test_postgres_contract.py` |
| 007 | `E4-G04_01_007_output_owner_generic_executor_boundary.md` | `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_enh_e4_g03_generic_executor_boundary.py` |
| 008 | `E4-G04_01_008_g02_g03_regression.md` | `ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g04-trial01-evidence scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_enh_e4_g04_result_artifact_postgres.py tests/product/test_enh_e4_g02_canonical_execution.py tests/product/test_enh_e4_g03_generic_executor_boundary.py tests/product/test_enh_e4_g03_persistent_stage_execution.py tests/product/test_enh_e4_g03_acceptance_postgres.py tests/product/test_postgres_contract.py` |
| 009 | `E4-G04_01_009_transition_scope_report_format_audit.md` | `git diff --name-status c23ba9e144d6994a32816efa8e5257fa7c47fddc..3d88781c1b69ba03bb06c0b8f143612b81feb4bf` |

## 7. Reason for Decision
Decision: FAIL. The evidence establishes migration success, ownership persistence, artifact-only contracts, GenericExecutor non-authority, and G02/G03 regression preservation. However, two mandatory Gate contracts are not met: typed Result reuse lacks its required role/context, and compensation’s metadata rollback lacks real PostgreSQL verification. The Gate rules forbid PASS when any mandatory item or AC fails.

## 8. Next Allowed Action
Start a new Coding Trial limited to correcting the item 004 and 005 findings and adding required automated coverage. Do not alter passed-Gate scope, transition-debt state, or this test evidence as a substitute for implementation.

## 9. Supplemental Context
Real PostgreSQL raw evidence: `/tmp/ariadne-g04-trial01-evidence/run-20260809T053910Z.txt` and `/tmp/ariadne-g04-trial01-evidence/run-20260809T053910Z.metadata.txt`. The initial sandbox runner failure is environmental (Docker socket permission) and was resolved by executing the same standardized runner with approved escalation; the final result is therefore not BLOCKED.
