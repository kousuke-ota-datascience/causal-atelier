# E4-G05 Trial 02 R1 Predictive Retry Remediation Report

- Gate: E4-G05
- Trial: 02
- Remediation package: R1
- Status: R1_COMPLETE
- Branch: refactor/ariadne_mvp_e4
- Failed Trial 01 implementation SHA: `ddb009875ef4e649f413cb0bb7f7a85f894e2b14`
- R1 starting commit: `f9c3fafda6b4d4ba77fdacdb192a58b3af07e9d0`
- R1 checkpoint commit: `ad3e3e124ee47f9cbaa2470b25263b7289795262`
- Migration head: `20260809_product_0010`
- Started at: 2026-08-09 UTC
- Finished at: 2026-08-09 UTC
- Report commit: `6269b8031f2cfa8d661cc432e5aea61709e7e4fe`

## 1. Trial 01 Failure Input

Trial 01 Test Agent item 005 は isolated Predictive retry の `claim_next()` が retry target 以外を返したと報告した。

## 2. Reproduction

現行 standard isolated runner では Trial 01 failure は再現しなかった。

## 3. Claim Candidate Evidence

- retry target: retry 後の Predictive canonical Execution
- all eligible candidates: retry target 1件のみ
- requested_at ordering: sole candidate のため target が先頭
- actual claimed ID: retry target

Facts:

- claim 直前 assertion は canonical `QUEUED` 又は lease-expired `RUNNING` を repository と同じ条件で抽出する。
- candidate 集合は retry target だけであり、`claim_next()` は同じ Execution ID を返した。

Interpretation:

- 現在の isolated retry contract では global FIFO claimer と test fixture は整合している。

## 4. Root Cause Classification

Facts:

- Trial 01 Test Agent は isolated retry failure を報告した。
- 現在の standard isolated runner は同じ test を PASS した。
- production source の queue/retry semantics は R1 で変更していない。
- combined regression では先行 test state による queued execution / stage row contamination が観測された。

Interpretation:

- Trial 01 isolated retry failure: `NOT_REPRODUCED`; `ROOT_CAUSE_UNCONFIRMED`。
- combined-run retry/G03 contamination: `TEST_FIXTURE_ISOLATION_DEFECT`。
- isolated failure を combined contamination によって説明したと断定してはならない。
- production queue semantics の変更を要する証拠はない。

## 5. Authoritative Queue / Retry Contract

### G02

`SqlExecutionRepository.claim_next()` は global FIFO canonical queue を claim する。retry priority、family priority、requested_at 操作は導入していない。

### G03

retry は同じ canonical Execution、stable StageExecution identity、append-only attempt history を維持する。

## 6. Fix

### Production

N/A。Production source change は NONE。

### Test

claim 前の eligible candidate set と FIFO order を retry test に assertion として追加した。

### Fixture / Runner

combined-run isolation は後続 Trial 02 work で扱う。

## 7. Files Changed

`tests/product/test_enh_e4_g05_phase_c_retry_postgres.py`（R1 checkpoint）。R1a は documentation/evidence correction only。

## 8. Retry Lifecycle Invariants

- same canonical Execution ID: PASS
- status `FAILED -> QUEUED`: PASS
- retry_count increment: PASS
- persistent StageExecution IDs stable: PASS
- attempt history preserved/appended: PASS
- lease state after retry/claim: PASS
- requested_at manipulation: NONE
- FamilyExecution write: NONE
- FamilyStageExecution write: NONE
- FamilyResult write: NONE
- FamilyArtifact write: NONE

## 9. No-Legacy-Write Evidence

retry test は Family 4 table の before/after count equality を assert する。

## 10. Verification

### V-01 Trial 02 R1 baseline isolated retry reproduction

- Purpose: Trial 01 isolated retry failure の再現確認
- Tested SHA: `f9c3fafda6b4d4ba77fdacdb192a58b3af07e9d0`
- Working tree: MODIFIED — R1 diagnostic 追加前
- Exact command: `ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-r1-baseline scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g05_phase_c_retry_postgres.py`
- Evidence directory: `/tmp/ariadne-g05-t02-r1-baseline`
- Raw evidence: UNKNOWN
- Exit code: 0; Passed: 1; Failed: 0; Skipped: 0
- Expected: Trial 01 failure の再現又は差異の確定
- Actual: 1 passed
- Facts: isolated retry は PASS。
- Interpretation: isolated failure は current runner で NOT_REPRODUCED。

### V-02 Final isolated retry verification

- Purpose: candidate diagnostic を含む retry contract
- Tested SHA: `f9c3fafda6b4d4ba77fdacdb192a58b3af07e9d0`
- Working tree: MODIFIED — R1 diagnostic test changes present
- Exact command: `ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-r1-final scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g05_phase_c_retry_postgres.py`
- Evidence directory: `/tmp/ariadne-g05-t02-r1-final`
- Raw evidence: UNKNOWN
- Exit code: 0; Passed: 1; Failed: 0; Skipped: 0
- Expected: retry target only を claim
- Actual: claimed retry target = PASS
- Facts: candidate assertion と claim assertion が PASS。
- Interpretation: queue-priority change は不要。

### V-03 G02/G03 retry / claim regression

- Purpose: related canonical lifecycle regression
- Tested SHA: `ad3e3e124ee47f9cbaa2470b25263b7289795262`
- Working tree: MODIFIED — documentation only
- Exact command: `scripts/test/run_product_postgres_tests.sh tests/product/test_enh_e4_g05_phase_c_rerun_postgres.py tests/product/test_enh_e4_g05_phase_c_revise_postgres.py tests/product/test_enh_e4_g02_canonical_execution.py tests/product/test_enh_e4_g03_acceptance_postgres.py`
- Evidence directory: NOT_SET
- Raw evidence: UNKNOWN
- Exit code: 1; Passed: 10; Failed: 3; Skipped: 0
- Expected: all PASS
- Actual: G02 PASS; G03 acceptance 3 failures after prior tests created queue/stage state.
- Facts: failures are combined invocation only。
- Interpretation: combined-run fixture isolation remains OPEN; this does not alter V-02 isolated retry result.

### V-04 C3a rerun regression

- Purpose: rerun canonical lifecycle
- Tested SHA: `ad3e3e124ee47f9cbaa2470b25263b7289795262`
- Exact command: V-03 command内の `tests/product/test_enh_e4_g05_phase_c_rerun_postgres.py`
- Evidence directory: NOT_SET; Raw evidence: UNKNOWN
- Exit code: 0 (node); Passed: 1; Failed: 0; Skipped: 0
- Expected/Actual: PASS
- Facts: rerun node PASS。
- Interpretation: R1 does not regress C3a。

### V-05 C3b revise regression

- Purpose: revise canonical lifecycle
- Tested SHA: `ad3e3e124ee47f9cbaa2470b25263b7289795262`
- Exact command: V-03 command内の `tests/product/test_enh_e4_g05_phase_c_revise_postgres.py`
- Evidence directory: NOT_SET; Raw evidence: UNKNOWN
- Exit code: 0 (node); Passed: 1; Failed: 0; Skipped: 0
- Expected/Actual: PASS
- Facts: revise node PASS。
- Interpretation: R1 does not regress C3b。

## 11. Migration

`20260809_product_0010`; migration change NONE。

## 12. Git Evidence

R1 checkpoint: `ad3e3e124ee47f9cbaa2470b25263b7289795262`。

## 13. Remaining Trial 02 Work

OPEN:

- Trial 01 combined regression remaining failures classification/remediation
- G05 Implementation Completion Report format remediation
- full Trial 02 implementation-side acceptance
- READY_FOR_TEST re-establishment

## 14. R1 Decision

R1_COMPLETE。Gate status は `NOT_READY_FOR_TEST`。
