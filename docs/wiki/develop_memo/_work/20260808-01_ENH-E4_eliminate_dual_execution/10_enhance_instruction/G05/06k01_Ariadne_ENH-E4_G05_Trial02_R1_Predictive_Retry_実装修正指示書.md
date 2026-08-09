# E4-G05 Trial 02 / R1 — Predictive Retry Isolated Remediation Instruction

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 — eliminate dual execution
- Branch: `refactor/ariadne_mvp_e4`
- Gate: `E4-G05`
- Trial: `02`
- Remediation package: `R1`
- Remediation name: Predictive retry isolated failure diagnosis and remediation
- Previous Trial: `E4-G05 Trial 01 — FAIL`
- Failed Test Agent target SHA: `ddb009875ef4e649f413cb0bb7f7a85f894e2b14`
- Trial 01 Gate Decision: `FAIL`
- Current Gate status: `NOT_READY_FOR_TEST`
- Target R1 status: `R1_COMPLETE`
- Product migration head expected: `20260809_product_0010`

---

# 1. Purpose

E4-G05 Trial 02を開始する。

R1では、Independent Test AgentがTrial 01で再現した以下のfailureのみを扱う。

```text
tests/product/test_enh_e4_g05_phase_c_retry_postgres.py

Predictive canonical retry
    ↓
same Execution becomes QUEUED
    ↓
SqlExecutionRepository.claim_next(...)
    ↓
expected retry target Execution
    ↓
actual different queued Execution
```

R1の目的は、

> clean PostgreSQL isolated runで、retry直後のcanonical claim candidate集合と実際にclaimされたExecutionを証拠化し、production defect / test-contract defect / fixture-isolation defectを分類した上で、必要な最小修正を行い、isolated retry contractをPASSへ戻すこと

である。

---

# 2. R1 Is NOT a Broad Trial 02 Remediation

今回扱わない。

```text
Trial 01 combined regression 32 passed / 6 failed の全件修正
G05 Implementation Completion Reportの全面再生成
Phase E report-format remediation
G05全体のREADY_FOR_TEST再宣言
Independent Test Agent再実行
TD closure再監査
G06以降
```

これらはR1後の別packageで扱う。

今回の停止条件は:

```text
R1_COMPLETE
```

のみ。

---

# 3. Important Constraint — Do Not Test-Fit claim_next()

現行canonical repositoryの `claim_next()` はglobal queue claimerである。

概念上:

```text
eligible:
    status == QUEUED

    OR

    status == RUNNING
    AND lease_expires_at <= now

order:
    requested_at ASC

lock:
    FOR UPDATE SKIP LOCKED

limit:
    1
```

である。

したがって、R1で以下を勝手に実装してはならない。

```text
retryされたExecutionを常に最優先

retry_count > 0 を優先

PREDICTIVE familyを優先

特定execution_idをclaim_nextへ暗黙注入

testの期待IDになるようrequested_atを書き換える
```

これらはqueue semantics変更である。

既存G02/G03 canonical contractに明示根拠がない限り禁止する。

---

# 4. Known Trial 01 Test Contract

現在のretry testは、retry後に:

```text
claimed = executions.claim_next(...)
assert claimed.execution_id == retry_target_execution_id
```

を要求している。

一方、test seed上で少なくとも以下が作成される。

```text
retry target:
    analysis_family = PREDICTIVE
    initial status = FAILED

causal negative target:
    initial status = FAILED

queued_execution negative target:
    initial status = SUCCEEDED
```

retry後、retry targetはQUEUEDになる。

testの意図上は、この時点でretry targetだけがcanonical claim candidateであるはず。

Independent Test Agentはclean DB isolated runでも別Executionがclaimされたと報告した。

したがって、R1では:

```text
「別candidateが実際に存在するのか」
```

を最初に確定する。

---

# 5. Source of Truth

最初に実物を読む。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
30_test_report/G05/
E4-G05_01_999_gate_decision.md
```

および同directoryの001〜010 reportから、Predictive retry failureを記録したTest Itemを特定する。

さらに:

```text
tests/product/
test_enh_e4_g05_phase_c_retry_postgres.py

src/ariadne/product/persistence/
repositories.py

src/ariadne/product/application/
execution_service.py

src/ariadne/product/application/
predictive_workflow_service.py

scripts/test/
run_product_postgres_tests.sh
```

を読む。

G02/G03でretry / claim contractを固定したtest/reportもactual repositoryから確認する。

推測でqueue semanticsを定義しない。

---

# 6. Start-of-Work Verification

最初に:

```bash
git branch --show-current
git rev-parse HEAD
git status --short
git log -20 --oneline
git diff --check

git merge-base --is-ancestor \
  ddb009875ef4e649f413cb0bb7f7a85f894e2b14 HEAD
echo $?
```

を実行する。

Trial 01 Test Agent report commitsがHEAD上に存在してよい。

それらを削除・改変しない。

Failed tested implementation SHA:

```text
ddb009875ef4e649f413cb0bb7f7a85f894e2b14
```

をR1 baselineとして扱う。

---

# 7. Reproduce Before Modifying Production

production codeを修正する前に、Trial 01 failureをstandard runnerで再現する。

唯一のreal PostgreSQL entry:

```bash
ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-r1-baseline \
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g05_phase_c_retry_postgres.py
```

記録:

```text
exact command
exit code
pass/fail
assertion location
expected execution_id
actual execution_id
raw evidence path
tested HEAD/SHA
```

もしbaselineでPASSした場合でもR1を即完了しない。

Trial 01 Test Agentではclean isolated failureが報告されているため、再現差異を説明する必要がある。

---

# 8. Add Diagnostic Candidate Evidence Before claim_next()

production behaviorを変える前に、retry testまたは専用diagnostic testへcandidate inspectionを追加する。

claim直前にcanonical `executions` tableから最低限以下を取得する。

```text
execution_id
project_id
analysis_family
status
requested_at
started_at
finished_at
retry_count
lease_owner
lease_expires_at
base_execution_id
revision_kind
```

claim eligibilityをrepositoryと同じ条件で分類する。

```text
QUEUED

OR

RUNNING with expired lease
```

さらに:

```text
ordered position by requested_at
```

を記録する。

目的:

```text
claim直前に何件candidateが存在し、
どのexecution_idが最古なのか
```

を証拠化すること。

---

# 9. Mandatory Candidate Origin Trace

retry target以外のcandidateが存在した場合、必ずoriginを追う。

最低限:

```text
candidate execution_id
created by which fixture/test/helper
created at which code location
initial status
when status became eligible
requested_at source
project/family
```

を特定する。

禁止:

```text
「たぶん前テストの残留」
「たぶんmigration seed」
「たぶんfixture」
```

と推測で処理すること。

actual creatorを特定する。

---

# 10. Diagnosis Classification

R1では原因を必ず以下のいずれかへ分類する。

## A. IMPLEMENTATION_DEFECT

例:

```text
claim_next queryがcontractと違う
retry transitionが不正なlease/statusを残す
repositoryが誤ったcandidateを返す
transaction visibility defect
retry処理が別Executionを不当にQUEUED化する
```

→ productionを修正する。

## B. TEST_FIXTURE_ISOLATION_DEFECT

例:

```text
retry test自身またはautouse fixtureが
意図せず別canonical QUEUED Executionを作る
```

→ fixture/test setupを修正する。

production queue semanticsを変えない。

## C. TEST_CONTRACT_DEFECT

例:

```text
複数の正当なQUEUED candidateが存在し、
global FIFO contract上は別Executionのclaimが正しいのに、
testがretry targetの即時claimを不当に要求している
```

→ G02/G03 authoritative contractを確認した上でtestを修正する。

ただし「testが落ちるから」という理由だけでは変更不可。

## D. ENVIRONMENT_OR_RUNNER_DEFECT

例:

```text
standard resetが対象DBをcleanにしていない
wrong DSN/databaseへ接続
runner isolation contract破損
```

→ runner/infrastructureを修正する。

これはproduction implementation FAILとは分類しないが、R1でisolated verification可能な状態まで直す。

## E. DESIGN_BLOCKED

approved queue/retry contractそのものが矛盾しており、
test/production/fixtureの局所修正では解消不能な場合のみ。

---

# 11. Decision Tree

診断後は以下に従う。

```text
candidate = retry target only
AND claim_next returns different execution
    -> IMPLEMENTATION_DEFECT

extra candidate exists
AND extra candidate is unintended fixture/bootstrap contamination
    -> TEST_FIXTURE_ISOLATION_DEFECT or ENVIRONMENT_OR_RUNNER_DEFECT

extra candidate exists
AND extra candidate is legitimate under accepted Product behavior
AND requested_at makes it first
    -> inspect G02/G03 queue contract

        if retry target priority is required
            -> IMPLEMENTATION_DEFECT / missing explicit retry scheduling contract

        if global FIFO is authoritative
            -> TEST_CONTRACT_DEFECT
```

根拠をreportへ書く。

---

# 12. Do Not Change Queue Semantics Without Contract Evidence

特に以下は禁止。

```python
.order_by(
    case((ExecutionOrm.retry_count > 0, 0), else_=1),
    ExecutionOrm.requested_at,
)
```

のようなretry優先化を、既存contract確認なしに入れない。

また:

```text
retry_execution()
    -> requested_at = now - huge_delta
```

等で優先順位を操作しない。

必要ならqueue semantics変更は設計判断として明示しなければならない。

R1のdefaultは:

```text
existing canonical queue contractを維持
```

である。

---

# 13. Retry Lifecycle Invariants — Must Preserve

R1修正後も以下を維持する。

```text
same canonical Execution ID

status:
FAILED -> QUEUED

retry_count:
+1

same persistent StageExecution IDs

failed StageExecution:
-> PENDING / retry-ready canonical state

attempt history:
existing attempt retained

next successful attempt:
append new attempt

canonical Result/Artifact:
destructive legacy resetなし

FamilyExecution:
no write

FamilyStageExecution:
no write

FamilyResult:
no write

FamilyArtifact:
no write
```

---

# 14. Lease Invariants

retry対象Executionについてclaim前後に確認する。

retry直後:

```text
status = QUEUED

lease_owner = NONE
lease_expires_at = NONE
```

またはapproved domain contractに従うretry-ready lease state。

claim後:

```text
status = RUNNING

lease_owner = new worker

lease_expires_at > now
```

stale previous leaseがretry後に残り、candidate selectionを壊していないこと。

---

# 15. requested_at Semantics Audit

`claim_next()` が `requested_at ASC` でqueue orderingしているため、retry時の`requested_at` semanticsを明示的に確認する。

以下のどちらがapproved contractかをG02/G03 source/test/reportから確認する。

```text
A:
retry preserves original requested_at
    -> original queue ageを維持

B:
retry refreshes requested_at
    -> retry request timeを新queue timestampとする
```

現状のactual implementation/domain behaviorを証拠化する。

R1で勝手に変更しない。

もしTest Agent failureの根因がこのsemanticsにある場合のみ、approved contractに合わせて修正する。

---

# 16. Add a Deterministic Retry Queue Test

原因に応じてtestをhardeningする。

最低限、retry直後に:

```text
eligible canonical claim candidates
```

をassertできるようにする。

isolated C2 testの前提が:

```text
retry targetだけがeligible
```

なら、それをclaim前に明示assertする。

そうすることで今後:

```text
unexpected queued contamination
```

と:

```text
claim_next implementation defect
```

を区別できる。

---

# 17. If Multiple Queue Candidates Are Legitimate

authoritative contract上、複数queued executionsが正当なscenarioを別testで持つ。

例:

```text
older normal queued Execution
newer retried Execution
```

またはその逆。

Then assert:

```text
claim_next follows authoritative queue ordering
```

を確認する。

retry isolated testとglobal queue ordering testの責務を混同しない。

---

# 18. No Legacy Authority Regression

R1修正でold Family authorityを復活させてはならない。

retry test前後で:

```text
FamilyExecution
FamilyStageExecution
FamilyResult
FamilyArtifact
```

のcounts/rowsが不変。

禁止:

```text
retry fallback to FamilyExecution

legacy Result/Artifact reset

Family Stage retry

old family-specific claim_next
```

---

# 19. Standard PostgreSQL Verification — Step 1

修正後、まずisolated retryのみ。

```bash
ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-r1-retry \
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g05_phase_c_retry_postgres.py
```

Required:

```text
exit 0
retry test PASS
```

candidate evidenceを残す。

---

# 20. Standard PostgreSQL Verification — Step 2

retry / claim semanticsに直接関連するG02/G03 testをactual repositoryから特定して実行する。

最低限:

```text
canonical claim
lease
retry lifecycle
persistent StageExecution
attempt history
```

をcoverする。

例の形式:

```bash
ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-r1-g02-g03 \
scripts/test/run_product_postgres_tests.sh \
  <actual G02/G03 retry-and-claim test paths/nodes>
```

完全なactual pathを使用する。

---

# 21. Standard PostgreSQL Verification — Step 3

Predictive mutation隣接regressionとして最低限:

```text
C3a rerun
C3b revise
```

を実行する。

理由:

```text
retry remediationがrevision semanticsへ影響していないこと
```

確認のため。

ただしPhase A/B/DやG05全体32+6 bundleはR1ではまだ行わない。

---

# 22. Non-PostgreSQL Tests

production repository/domain変更が入った場合は関連unit/boundary testを実行する。

対象例:

```text
Execution.increment_retry
SqlExecutionRepository.claim_next
lease behavior
retry service delegation
```

actual testを選ぶ。

---

# 23. R1 Completion Criteria

以下をすべてDONEにする。

```text
[ ] Trial 01 retry failure evidence inspected

[ ] isolated failure reproduced OR reproduction difference explained

[ ] claim直前candidate set captured

[ ] actual claimed execution_id captured

[ ] unexpected candidate origin traced if present

[ ] root cause classified:
    IMPLEMENTATION_DEFECT
    TEST_FIXTURE_ISOLATION_DEFECT
    TEST_CONTRACT_DEFECT
    ENVIRONMENT_OR_RUNNER_DEFECT
    or DESIGN_BLOCKED

[ ] G02/G03 retry/queue contract inspected

[ ] no ungrounded retry-priority queue change introduced

[ ] required production/test/fixture fix implemented

[ ] retry same Execution identity preserved

[ ] StageExecution identity preserved

[ ] attempt history append preserved

[ ] retry lease state correct

[ ] requested_at semantics match authoritative contract

[ ] Family 4-table writes = NONE

[ ] isolated retry PostgreSQL PASS

[ ] relevant G02/G03 claim/retry regression PASS

[ ] C3a rerun regression PASS

[ ] C3b revise regression PASS

[ ] migration head verified

[ ] git diff --check PASS

[ ] R1 checkpoint commit created

[ ] R1 remediation report created
```

---

# 24. R1 Checkpoint Commit

criteria PASS後、production/test/fixture修正をcheckpoint commitする。

Suggested:

```text
E4-G05 Trial 02 R1 predictive retry remediation
```

commit前:

```bash
git status --short
git diff --check
git diff --cached --name-status
```

Test Agent Trial 01 reportsを変更・stageしない。

commit後:

```bash
git rev-parse HEAD
git status --short
```

R1 checkpoint SHAを記録する。

---

# 25. R1 Remediation Report

作成:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G05/Trial02/
E4-G05_02_R1_predictive_retry_remediation_report.md
```

最低限metadata:

```text
# E4-G05 Trial 02 R1 Predictive Retry Remediation Report

- Gate
- Trial
- Remediation package
- Status
- Branch
- Failed Trial 01 implementation SHA
- R1 starting commit
- R1 checkpoint commit
- Migration head
- Started at
- Finished at
```

---

# 26. R1 Report Required Sections

```text
## 1. Trial 01 Failure Input

## 2. Reproduction

## 3. Claim Candidate Evidence
- retry target
- all eligible candidates
- requested_at ordering
- actual claimed ID

## 4. Root Cause Classification

## 5. Authoritative Queue / Retry Contract
### G02
### G03

## 6. Fix
### Production
### Test
### Fixture / Runner
Use N/A where not applicable.

## 7. Files Changed

## 8. Retry Lifecycle Invariants

## 9. No-Legacy-Write Evidence

## 10. Verification
For every run:
- exact command
- exit code
- passed/failed/skipped
- raw evidence path
- tested SHA/state
- expected
- actual
- Facts
- Interpretation

## 11. Migration

## 12. Git Evidence

## 13. Remaining Trial 02 Work

## 14. R1 Decision
R1_COMPLETE | DESIGN_BLOCKED
```

---

# 27. Facts vs Interpretation

reportでは必ず分離する。

Example:

```text
Facts:
- claim直前のeligible candidatesは2件だった
- execution A requested_at = ...
- execution B requested_at = ...
- claim_next returned A

Interpretation:
- repositoryはrequested_at ASC contract通り
- retry test fixtureがBだけがeligibleという前提を満たしていなかった
- classification = TEST_FIXTURE_ISOLATION_DEFECT
```

あるいは:

```text
Facts:
- eligible candidateはretry target 1件のみ
- claim_next returned another ID

Interpretation:
- repository/transaction behavior is inconsistent
- classification = IMPLEMENTATION_DEFECT
```

---

# 28. Report Commit Procedure

R1 reportは実装checkpoint commit後に作る。

initially:

```text
Report commit: PENDING
```

report initial commit:

```text
E4-G05 Trial 02 R1 remediation report
```

SHA取得:

```bash
git rev-parse HEAD
```

Report commit fieldをinitial report commit SHAへ更新する。

必要ならmetadata correction commitを作る。

self-referential SHAを要求しない。

---

# 29. R1 Does Not Repair Report-Format Failure

Trial 01のもう一つのFAIL:

```text
E4-G05_01_implementation_completion_report.md
required template fields/sections missing
```

はR1では修正しない。

R1 reportのRemaining Trial 02 Workに:

```text
Report-format remediation remains OPEN
```

と記録する。

またcombined regression 6 failuresのremaining classificationもOPEN。

---

# 30. R1 Exit State

R1成功後のexpected state:

```text
E4-G05 Trial 02

R1 Predictive retry isolated remediation:
    COMPLETE

Predictive isolated retry:
    PASS

Root cause:
    <classification>

Full combined regression remediation:
    OPEN

Completion report format remediation:
    OPEN

G05:
    NOT_READY_FOR_TEST
```

---

# 31. Stop Reasons NOT Accepted

以下を途中停止理由として認めない。

```text
failureを再現した

別queued executionを発見した

fixtureが怪しい

claim_nextがFIFOだった

test expectationが怪しい

G02/G03 contract確認が必要

修正後にretry testがPASSしたがregression未実行

report作成が残っている

combined 6 failuresがまだ残っている
```

最後の項目はR1 scope外なので、R1 completionを妨げない。

ただしR1で要求したretry/G02/G03/C3a/C3b regressionは必須。

---

# 32. DESIGN_BLOCKED

DESIGN_BLOCKEDを許可するのは:

```text
G02/G03 authoritative queue contract自体が相互矛盾し、
retry scheduling semanticsを設計決定なしに確定できない
```

場合のみ。

単なるproduction defect / fixture defect / test defectはDESIGN_BLOCKEDではない。

---

# 33. Final Stop Condition

正しい終了条件:

```text
R1_COMPLETE
```

最後に必ず:

```text
E4-G05 Trial 02
R1_COMPLETE

Root Cause:
<IMPLEMENTATION_DEFECT |
 TEST_FIXTURE_ISOLATION_DEFECT |
 TEST_CONTRACT_DEFECT |
 ENVIRONMENT_OR_RUNNER_DEFECT>

R1 Checkpoint SHA:
<full SHA>

Predictive isolated retry PostgreSQL:
PASS

Eligible candidate set:
<summary>

Claimed retry target:
PASS

G02/G03 retry/claim regression:
PASS

C3a rerun regression:
PASS

C3b revise regression:
PASS

Family old-authority writes:
NONE

Migration head:
20260809_product_0010

Remaining Trial 02:
- combined regression failure classification/remediation
- G05 completion report format remediation

Gate:
NOT_READY_FOR_TEST
```

を報告して停止する。

R1完了後、このrunでR2へ進まないこと。
