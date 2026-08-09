# E4-G05 Trial 02 / R1a — Retry Remediation Report Correction Instruction

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 — eliminate dual execution
- Branch: `refactor/ariadne_mvp_e4`
- Gate: `E4-G05`
- Trial: `02`
- Remediation package: `R1a`
- Parent remediation: `R1 — Predictive retry isolated remediation`
- R1 implementation/test checkpoint: `ad3e3e124ee47f9cbaa2470b25263b7289795262`
- Target report:
  `docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G05/Trial02/E4-G05_02_R1_predictive_retry_remediation_report.md`
- Current Gate status: `NOT_READY_FOR_TEST`
- Target R1 status after this work: `R1_COMPLETE`

---

# 1. Purpose

E4-G05 Trial 02 / R1で実施したPredictive retry isolated remediationについて、
production/test結果そのものは維持しつつ、R1 reportの根因分類とverification evidence形式を修正する。

今回の作業は**documentation/evidence correction only**である。

production source、Product tests、migration、runtime behaviorを変更してはならない。

---

# 2. Current Technical State — Preserve

R1で確認済みの事実:

```text
R1 checkpoint:
ad3e3e124ee47f9cbaa2470b25263b7289795262

Production modification:
NONE

Predictive isolated retry:
PASS

Eligible claim candidate:
retry target only

Actual claimed execution:
retry target

Queue semantics:
preserved

Family old-authority writes:
NONE
```

これらを変更しない。

---

# 3. Correction 1 — Root Cause Classification

現在のR1 reportで、Trial 01 isolated retry failureのroot causeを:

```text
TEST_FIXTURE_ISOLATION_DEFECT
```

と断定している場合、その表現を修正する。

現時点で確定しているのは:

```text
Trial 01 isolated retry failure:
    current standard isolated runnerでは再現しない

Combined-run contamination:
    fixture / test-state interactionの証拠あり
```

である。

したがって、root causeを以下のように分離する。

```text
Trial 01 isolated retry failure:
    NOT_REPRODUCED
    ROOT_CAUSE_UNCONFIRMED

Combined-run retry / G03 contamination:
    TEST_FIXTURE_ISOLATION_DEFECT
```

禁止:

```text
combined-run contaminationの根因を、
isolated retry failureの根因として断定する
```

---

# 4. Required Facts / Interpretation Split

Root Cause sectionでは必ずFactsとInterpretationを分離する。

例:

```text
Facts:
- Trial 01 Test Agent reported an isolated retry failure.
- Current standard isolated runner completes the same retry test with PASS.
- Immediately before claim_next(), the only eligible canonical claim candidate is the retry target.
- claim_next() returns the retry target.
- No production source modification was required.
- Combined regression runs showed state/fixture contamination behavior.

Interpretation:
- The Trial 01 isolated retry failure is not reproducible on the current standard isolated runner.
- Its specific root cause therefore remains unconfirmed.
- Combined-run contamination is independently classified as TEST_FIXTURE_ISOLATION_DEFECT.
- There is currently no evidence requiring a production queue-semantics change.
```

---

# 5. Correction 2 — Verification Evidence Format

R1 reportのVerification sectionを、要約だけではなく、
以下のfieldを各runごとに明示する形式へ修正する。

必須:

```text
Verification ID
Purpose
Tested SHA / repository state
Exact copy-pastable command
Evidence directory
Exit code
Passed
Failed
Skipped
Expected
Actual
Facts
Interpretation
```

値が存在しない場合はfieldを削除せず:

```text
N/A
NONE
UNKNOWN
NOT_RUN
```

を使用する。

---

# 6. Mandatory Verification Entries

最低限、以下を個別entryとして記載する。

## V-01 Trial 02 R1 baseline isolated retry reproduction

```text
Purpose:
Trial 01 isolated retry failureの再現確認
```

exact commandを完全形で記載する。

例:

```bash
ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-r1-baseline \
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g05_phase_c_retry_postgres.py
```

actual実行commandが異なる場合はactualを使用する。

---

## V-02 Final isolated retry verification

```bash
ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-r1-retry \
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g05_phase_c_retry_postgres.py
```

actual commandを記載する。

Required conclusion:

```text
exit 0
1 passed
claimed retry target = PASS
```

---

## V-03 G02/G03 retry / claim regression

actual repositoryで実行したG02/G03 test path/nodeを完全に記載する。

省略禁止:

```text
same as above
related tests
G02/G03 PASS
```

---

## V-04 C3a rerun regression

actual commandを完全形で記載する。

---

## V-05 C3b revise regression

actual commandを完全形で記載する。

---

# 7. Evidence Directory

各standard PostgreSQL runner runについて:

```text
ARIADNE_TEST_EVIDENCE_DIR
```

を明示する。

raw evidence pathが取得できる場合:

```text
Raw evidence:
<path>
```

を記載する。

取得不能なら:

```text
Raw evidence:
UNKNOWN
```

としてfieldを残す。

---

# 8. Tested SHA / State

各verification entryで:

```text
Tested SHA:
<full SHA>
```

を記録する。

R1 checkpoint commit前のworking-tree testだった場合は:

```text
Tested SHA:
<HEAD>

Working tree:
MODIFIED — diagnostic test changes present
```

等、actual stateを明記する。

推測でR1 checkpoint SHAをすべてのrunへ割り当てない。

---

# 9. Preserve Authoritative Queue Semantics

report correctionで以下を明示する。

```text
No retry-priority queue behavior was introduced.

SqlExecutionRepository.claim_next() global queue ordering was not modified.

No requested_at manipulation was introduced to force the retry target to the front.

No Product production source change was required in R1.
```

これをFactsとして記録する。

---

# 10. Preserve Retry Lifecycle Invariants

reportへ以下のverification結果を明示する。

```text
same canonical Execution ID: PASS

status FAILED -> QUEUED: PASS

retry_count increment: PASS

persistent StageExecution IDs stable: PASS

attempt history preserved/appended: PASS

lease state after retry/claim: PASS

FamilyExecution write: NONE
FamilyStageExecution write: NONE
FamilyResult write: NONE
FamilyArtifact write: NONE
```

actual evidenceで未確認の項目は勝手にPASSにせず:

```text
NOT_RUN
UNKNOWN
```

を使用する。

---

# 11. Remaining Trial 02 Work

R1 reportのRemaining Trial 02 Workを明示的に以下とする。

```text
OPEN:
- Trial 01 combined regression remaining failures classification/remediation
- G05 Implementation Completion Report format remediation
- full Trial 02 implementation-side acceptance
- READY_FOR_TEST re-establishment
```

R1aではこれらを実行しない。

---

# 12. R1 Decision

report末尾のR1 Decisionを、correction完了後に:

```text
R1_COMPLETE
```

とする。

ただしGateは:

```text
NOT_READY_FOR_TEST
```

のまま。

---

# 13. Files Allowed to Change

原則として変更許可:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G05/Trial02/
E4-G05_02_R1_predictive_retry_remediation_report.md
```

必要なら同reportのmetadata correctionのみ。

変更禁止:

```text
src/
tests/
migrations/
scripts/
30_test_report/G05/
```

Trial 01 Test Agent reportを変更しない。

---

# 14. Git Verification

作業前:

```bash
git branch --show-current
git rev-parse HEAD
git status --short
git diff --check
```

作業後:

```bash
git diff --check
git status --short
git diff -- \
  docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G05/Trial02/E4-G05_02_R1_predictive_retry_remediation_report.md
```

production/test fileに差分がないことを確認する。

---

# 15. Report Correction Commit

report correctionのみをcommitする。

Suggested commit:

```text
E4-G05 Trial 02 R1 retry report evidence correction
```

commit前:

```bash
git diff --check
git status --short
git diff --cached --name-status
```

commit後:

```bash
git rev-parse HEAD
git status --short
```

correction commit SHAを記録する。

---

# 16. Report Metadata

R1 reportにmetadata fieldがある場合:

```text
Report commit
```

は**report initial commit SHA**を維持する。

今回のcorrection commit SHAでReport commit fieldを上書きしない。

必要なら別field:

```text
Report correction commit:
<full SHA>
```

を追加する。

self-referential commit SHAを要求しない。

---

# 17. Completion Criteria

以下をすべて満たすこと。

```text
[ ] production source unchanged

[ ] Product tests unchanged

[ ] migrations unchanged

[ ] Trial 01 Test Agent reports unchanged

[ ] isolated retry root cause changed to:
    NOT_REPRODUCED / ROOT_CAUSE_UNCONFIRMED

[ ] combined-run contamination separately classified:
    TEST_FIXTURE_ISOLATION_DEFECT

[ ] Facts / Interpretation separated

[ ] baseline isolated retry exact command recorded

[ ] final isolated retry exact command recorded

[ ] G02/G03 exact regression command recorded

[ ] C3a exact regression command recorded

[ ] C3b exact regression command recorded

[ ] exit codes recorded

[ ] pass/fail/skip counts recorded

[ ] evidence dirs/raw evidence recorded

[ ] tested SHA/state recorded

[ ] queue semantics unchanged explicitly documented

[ ] no-legacy-write evidence documented

[ ] Remaining Trial 02 Work remains OPEN

[ ] R1 Decision = R1_COMPLETE

[ ] Gate = NOT_READY_FOR_TEST

[ ] git diff --check PASS

[ ] report correction commit created
```

---

# 18. Stop Reasons NOT Accepted

以下を途中停止理由として認めない。

```text
exact commandを調べる必要がある

evidence directory確認が必要

tested SHA確認が必要

root cause表現の修正が必要

reportが長くなる

R2がまだ残っている
```

今回のscopeはreport/evidence correctionのみなので、最後まで完了する。

---

# 19. Final Stop Condition

正しい終了条件:

```text
R1_COMPLETE
```

最後に必ず以下を報告する。

```text
E4-G05 Trial 02
R1_COMPLETE

R1 implementation/test checkpoint:
ad3e3e124ee47f9cbaa2470b25263b7289795262

Report correction commit:
<full SHA>

Trial 01 isolated retry failure:
NOT_REPRODUCED
ROOT_CAUSE_UNCONFIRMED

Combined-run contamination:
TEST_FIXTURE_ISOLATION_DEFECT

Predictive isolated retry:
PASS

Production source changes in R1a:
NONE

Product test changes in R1a:
NONE

Gate:
NOT_READY_FOR_TEST

Remaining Trial 02:
- combined regression failure classification/remediation
- G05 completion report format remediation
```

を報告して停止する。

R1a完了後、このrunでR2へ進まないこと。
