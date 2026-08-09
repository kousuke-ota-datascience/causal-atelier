# E4-G05 Trial 02 / R1b — Isolated G03 Verification and R1 Final Closure Instruction

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 — eliminate dual execution
- Branch: `refactor/ariadne_mvp_e4`
- Gate: `E4-G05`
- Trial: `02`
- Remediation package: `R1b`
- Parent remediation: `R1 — Predictive retry isolated remediation`
- R1 implementation/test checkpoint: `ad3e3e124ee47f9cbaa2470b25263b7289795262`
- R1 report:
  `docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G05/Trial02/E4-G05_02_R1_predictive_retry_remediation_report.md`
- Current R1 state: `TECHNICALLY_PASS / FORMALLY_INCOMPLETE`
- Current Gate status: `NOT_READY_FOR_TEST`
- Target status: `R1_COMPLETE`

---

# 1. Purpose

E4-G05 Trial 02 / R1を正式に閉じる。

R1aまでに以下は成立している。

```text
Predictive isolated retry:
PASS

Eligible canonical claim candidates:
retry target exactly 1

Actual claimed Execution:
retry target

Production queue semantics:
UNCHANGED

Trial 01 isolated retry failure:
NOT_REPRODUCED
ROOT_CAUSE_UNCONFIRMED

Combined-run contamination:
TEST_FIXTURE_ISOLATION_DEFECT
```

しかしR1 reportにはまだ以下の不足がある。

```text
1. relevant G03 regressionがcombined invocationでは3 FAIL
   → isolated standard runner PASS evidenceが未取得

2. V-04 C3a / V-05 C3b が
   「V-03 command内」のような省略記法
   → independent exact command / exit evidenceとして不十分
```

R1bではこの2点だけを閉じる。

---

# 2. Scope

今回実施する。

```text
A. G03 relevant regressionをstandard PostgreSQL runnerでisolated実行
B. isolated G03結果をR1 reportへ完全記録
C. C3a rerunを独立standard runnerで実行
D. C3b reviseを独立standard runnerで実行
E. V-04 / V-05を完全なevidence entryへ修正
F. R1 completion criteriaを再確認
G. R1 report correction commit
H. R1_COMPLETE
```

今回実施しない。

```text
Trial 02 remaining combined regression remediation
G05 completion report format remediation
full G05 acceptance
READY_FOR_TEST再宣言
Independent Test Agent再実行
production architecture変更
```

---

# 3. Production / Test Change Policy

R1bは原則:

```text
verification + documentation only
```

である。

変更禁止:

```text
src/
migrations/
Product production behavior
queue semantics
retry semantics
claim ordering
```

既存test fileも原則変更しない。

もしisolated G03がFAILした場合のみ、その時点でFAILを正確に分類する。

そのFAILを隠すためにreportだけ修正してはならない。

---

# 4. Start-of-Work Verification

最初にactual repository stateを確認する。

```bash
git branch --show-current
git rev-parse HEAD
git status --short
git log -15 --oneline
git diff --check
git merge-base --is-ancestor \
  ad3e3e124ee47f9cbaa2470b25263b7289795262 HEAD
echo $?
```

Expected:

```text
branch = refactor/ariadne_mvp_e4
R1 checkpoint is ancestor
```

Trial 01 / Trial 02 report commitsがHEAD上に存在してよい。

それらを破棄しない。

---

# 5. Inspect Actual G03 Tests

R1 reportのV-03およびactual repositoryから、
combined invocationでFAILした3件を特定する。

最低限記録:

```text
test file
test node
combined-run failure assertion
combined-run pre-existing DB/test state
```

さらにG03 acceptanceでretry/claimに関連するisolated target setをactual repositoryから確定する。

推測でtest pathを作らない。

---

# 6. Mandatory Isolated G03 Verification

standard PostgreSQL runnerのみを使用する。

形式:

```bash
ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-r1b-g03 \
scripts/test/run_product_postgres_tests.sh \
  <actual G03 relevant test paths/nodes>
```

可能ならcombined runでFAILした3 testだけでなく、
同じfixture/contractに属するG03 relevant setをまとめて実行する。

Required evidence:

```text
Exact command
Evidence directory
Tested SHA
Exit code
Passed
Failed
Skipped
Expected
Actual
Facts
Interpretation
```

---

# 7. G03 Decision

## Case A — isolated G03 PASS

Expected preferred outcome:

```text
exit 0
failed = 0
```

この場合:

```text
Facts:
- combined invocationではG03 3 FAIL
- clean isolated standard runnerではPASS

Interpretation:
- G03 production contract defectの証拠なし
- combined failureはtest-state / fixture isolation interaction
- classification = TEST_FIXTURE_ISOLATION_DEFECT
```

と確定してよい。

## Case B — isolated G03 FAIL

この場合R1を `R1_COMPLETE` にしてはならない。

以下を記録する。

```text
R1b Status:
REMEDIATION_REQUIRED

Failure classification:
<actual classification>
```

production defectなら別micro-remediation instructionが必要。

ただし、このrunで大規模R2へ進まない。

---

# 8. Mandatory C3a Independent Verification

C3a rerun testを独立standard runnerで実行する。

actual test pathを使う。

形式:

```bash
ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-r1b-c3a \
scripts/test/run_product_postgres_tests.sh \
  <actual C3a rerun test path/node>
```

Required:

```text
Exit code: 0
Failed: 0
```

最低限以下を維持。

```text
new Execution ID
base_execution_id
revision_kind = RERUN
change_reason = NONE
new StageExecution IDs
base non-destructive
Family writes = NONE
```

---

# 9. Mandatory C3b Independent Verification

C3b revise testを独立standard runnerで実行する。

形式:

```bash
ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-r1b-c3b \
scripts/test/run_product_postgres_tests.sh \
  <actual C3b revise test path/node>
```

Required:

```text
Exit code: 0
Failed: 0
```

最低限以下を維持。

```text
changed conditions:
REVISED + explicit change_reason

same conditions:
RERUN + change_reason NONE

new canonical Execution
new StageExecution IDs
base non-destructive
Family writes = NONE
```

---

# 10. Why Independent Commands Are Required

以下の記録は禁止。

```text
V-03 command内でPASS
same as V-03
same as previous
combined commandの一部
node result = PASS
```

理由:

```text
process exit code 1のcombined invocation内部で
特定nodeだけPASSしたことは、
独立verification exit 0の証拠ではない
```

R1 reportではV-04 / V-05を独立commandとして記録する。

---

# 11. R1 Report — Add Isolated G03 Entry

R1 reportのVerification sectionに新規entryを追加する。

推奨:

```text
V-06 — Isolated G03 Retry / StageExecution Regression
```

必須field:

```text
Purpose
Tested SHA / state
Exact command
Evidence directory
Raw evidence path
Exit code
Passed
Failed
Skipped
Expected
Actual
Facts
Interpretation
```

---

# 12. R1 Report — Rewrite V-04

V-04 C3aについて、以下のような省略を除去する。

禁止:

```text
Exact command:
V-03 command内の rerun node
```

修正後:

```text
## V-04 — C3a Rerun Regression

Purpose:
...

Tested SHA:
...

Exact command:
```bash
ARIADNE_TEST_EVIDENCE_DIR=... \
scripts/test/run_product_postgres_tests.sh \
  <actual path/node>
```

Evidence directory:
...

Raw evidence:
...

Exit code:
0

Passed:
...

Failed:
0

Skipped:
...

Expected:
...

Actual:
...

Facts:
...

Interpretation:
...
```

---

# 13. R1 Report — Rewrite V-05

V-05 C3bも同様。

完全な独立commandを書く。

```text
Exact command:
<full command>

Exit code:
0

Failed:
0
```

省略禁止。

---

# 14. Tested SHA Accuracy

各runのtested SHAを正確に記録する。

run時点でHEADにreport-only commitsが含まれている場合でも、
production/test checkpointとの関係を明記する。

例:

```text
Tested HEAD:
<full SHA>

R1 production/test checkpoint ancestor:
ad3e3e124ee47f9cbaa2470b25263b7289795262

Production/test delta since R1 checkpoint:
NONE
```

実際にNONEであることをgit diffで確認する。

---

# 15. Verify No Production/Test Delta

R1b終了前に:

```bash
git diff \
  ad3e3e124ee47f9cbaa2470b25263b7289795262..HEAD \
  -- src tests migrations scripts
```

actual path layoutに合わせる。

report-only changes以外の差分が既に存在する場合は、
そのoriginを確認する。

R1b自身がproduction/test deltaを追加しないこと。

---

# 16. R1 Completion Criteria — Final

以下をすべて満たした場合のみ `R1_COMPLETE`。

```text
[ ] Predictive isolated retry PASS

[ ] eligible claim candidate = retry target only

[ ] claimed Execution = retry target

[ ] Trial 01 isolated failure =
    NOT_REPRODUCED / ROOT_CAUSE_UNCONFIRMED

[ ] combined-run contamination =
    TEST_FIXTURE_ISOLATION_DEFECT

[ ] isolated relevant G03 regression PASS

[ ] C3a rerun independent standard runner PASS

[ ] C3b revise independent standard runner PASS

[ ] V-04 exact complete command recorded

[ ] V-05 exact complete command recorded

[ ] isolated G03 exact complete command recorded

[ ] all corresponding exit codes recorded

[ ] pass/fail/skip counts recorded

[ ] evidence directories recorded

[ ] raw evidence paths recorded or UNKNOWN

[ ] tested SHA/state recorded

[ ] Facts / Interpretation separated

[ ] production queue semantics unchanged

[ ] production source changes in R1b = NONE

[ ] Product test changes in R1b = NONE

[ ] migration changes in R1b = NONE

[ ] Family old-authority writes = NONE

[ ] migration head = 20260809_product_0010

[ ] R1 report decision = R1_COMPLETE

[ ] Gate = NOT_READY_FOR_TEST

[ ] git diff --check PASS

[ ] report correction commit created
```

---

# 17. Remaining Trial 02 Work — Preserve OPEN

R1 completion後も以下はOPEN。

```text
R2:
Trial 01 combined regression remaining failures
classification / remediation

R3:
G05 Implementation Completion Report
full template-compliant regeneration

Final Trial 02 acceptance:
fixed implementation SHA
full verification
READY_FOR_TEST
```

R1 reportにこれを明示する。

---

# 18. Report Correction Commit

R1bで変更するのはR1 reportのみを基本とする。

Suggested commit:

```text
E4-G05 Trial 02 R1b isolated G03 evidence and closure
```

commit前:

```bash
git status --short
git diff --check
git diff --cached --name-status
```

commit後:

```bash
git rev-parse HEAD
git status --short
```

R1 reportに既存の:

```text
Report commit
```

fieldがある場合、initial report commit SHAを維持する。

必要なら:

```text
R1a correction commit:
<sha>

R1b correction commit:
<sha>
```

のようなfieldを追加する。

self-referenceしない。

---

# 19. Do Not Alter Trial 01 Test Reports

変更禁止:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
30_test_report/G05/
```

Trial 01 Test Agent evidenceはimmutable inputとして扱う。

---

# 20. Do Not Enter R2

R1bが完了しても、このrunで:

```text
combined 6 failures remediation
completion report regeneration
READY_FOR_TEST
```

へ進まない。

R1を明確に閉じて停止する。

---

# 21. Stop Reasons NOT Accepted

以下を途中停止理由として認めない。

```text
G03 isolated commandを調べる必要がある

C3a/C3bはcombined runでPASSしている

個別実行は冗長

report修正が残っている

evidence path確認が必要

R2がまだ残っている
```

R1b scope内の作業はすべて完了させる。

---

# 22. Final Stop Condition

isolated G03がPASSし、全criteriaを満たした場合:

```text
E4-G05 Trial 02
R1_COMPLETE
```

を宣言する。

最後に必ず:

```text
E4-G05 Trial 02
R1_COMPLETE

R1 implementation/test checkpoint:
ad3e3e124ee47f9cbaa2470b25263b7289795262

R1b report correction commit:
<full SHA>

Predictive isolated retry:
PASS

Trial 01 isolated retry failure:
NOT_REPRODUCED
ROOT_CAUSE_UNCONFIRMED

Combined-run contamination:
TEST_FIXTURE_ISOLATION_DEFECT

Isolated G03 regression:
PASS

C3a rerun independent regression:
PASS

C3b revise independent regression:
PASS

Production source changes in R1b:
NONE

Product test changes in R1b:
NONE

Migration changes in R1b:
NONE

Family old-authority writes:
NONE

Migration head:
20260809_product_0010

Remaining Trial 02:
- R2 combined regression failure classification/remediation
- R3 G05 completion report format remediation
- final Trial 02 acceptance / READY_FOR_TEST

Gate:
NOT_READY_FOR_TEST
```

を報告して停止する。

---

# 23. Failure Stop Condition

isolated G03がFAILした場合のみ:

```text
R1b_REMEDIATION_REQUIRED
```

として停止してよい。

その場合必ず:

```text
exact failing command
exit code
failed nodes
expected
actual
Facts
Interpretation
classification
```

を報告する。

この場合 `R1_COMPLETE` と宣言してはならない。
