# E4-G05 Trial 02 / R2a — R2 Evidence and Report Completion Instruction

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 — eliminate dual execution
- Branch: `refactor/ariadne_mvp_e4`
- Gate: `E4-G05`
- Trial: `02`
- Remediation package: `R2a`
- Parent remediation: `R2 — Combined regression failure classification and remediation`
- R1 implementation/test checkpoint: `ad3e3e124ee47f9cbaa2470b25263b7289795262`
- R2 checkpoint: `1dd20d2a6b2d7e85c3116e7b019024883e7d9786`
- Target report:
  `docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G05/Trial02/E4-G05_02_R2_combined_regression_remediation_report.md`
- Current R2 state: `TECHNICALLY_COMPLETE / REPORT_INCOMPLETE`
- Current Gate status: `NOT_READY_FOR_TEST`
- Target R2 status: `R2_COMPLETE`
- Expected Product migration head: `20260809_product_0010`

---

# 1. Purpose

E4-G05 Trial 02 / R2を正式に閉じる。

R2ではTrial 01のcombined regression failure 6件について、
runtime/production remediationの要否を分類した。

現時点のtechnical conclusion:

```text
6 / 6 failures classified

remaining unclassified:
0

confirmed production defect:
NONE

runtime acceptance defect currently demonstrated:
NONE

R1 Predictive retry:
PASS

G03 isolated:
PASS

semantic isolated partitions:
PASS
```

しかしR2 reportは、R2 instructionで要求したevidence/report formatを満たしていない。

R2aでは**documentation/evidence correction only**を行い、
R2をformalに `R2_COMPLETE` とする。

---

# 2. Scope

今回実施する。

```text
A. R2 reportのrequired metadata補完

B. Six-Failure Ledgerの証跡詳細化

C.各failureのisolated verification evidence補完

D. Original combined scope evidence補完

E. Corrected standardized partition evidence補完

F. G02 / G03 / G04 regression section補完

G. Phase B / C / D / R1 regression section補完

H. No-Legacy-Authority Regression section追加

I. Exact Verification Evidence section追加

J. R2 checkpointがempty evidence-boundary commitであることを明示

K. R2 Decision = R2_COMPLETE

L. report correction commit
```

今回実施しない。

```text
production source変更
Product test変更
fixture変更
runner変更
migration変更

R3 completion report remediation
READY_FOR_TEST
Independent Test Agent rerun
```

---

# 3. Change Policy

R2aは原則:

```text
report-only
```

変更許可:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G05/Trial02/
E4-G05_02_R2_combined_regression_remediation_report.md
```

必要なら同reportのmetadataのみ。

変更禁止:

```text
src/
tests/
migrations/
scripts/
30_test_report/G05/
```

Trial 01 Test Agent reportsはimmutable input。

---

# 4. Start-of-Work Verification

最初に:

```bash
git branch --show-current
git rev-parse HEAD
git status --short
git log -15 --oneline
git diff --check

git merge-base --is-ancestor \
  1dd20d2a6b2d7e85c3116e7b019024883e7d9786 HEAD
echo $?
```

を実行する。

R2 checkpointがancestorであること。

---

# 5. R2 Checkpoint Classification

R2 checkpoint:

```text
1dd20d2a6b2d7e85c3116e7b019024883e7d9786
```

はproduction/test/fixture変更を伴わないempty checkpointである。

reportへ明示する。

```text
R2 production changes:
NONE

R2 test changes:
NONE

R2 fixture changes:
NONE

R2 checkpoint purpose:
evidence / remediation boundary only
```

empty commit自体を欠陥扱いしない。

---

# 6. Required Metadata

R2 report headerに最低限以下を揃える。

```text
# E4-G05 Trial 02 R2 Combined Regression Remediation Report

- Project
- Enhancement
- Gate
- Trial
- Remediation package
- Status
- Branch

- Trial 01 failed implementation SHA
- R1 checkpoint
- R2 starting commit
- R2 checkpoint commit
- R2 checkpoint type
- Report commit
- Report correction commit

- Migration head

- Started at
- Finished at
```

値が不明な場合:

```text
UNKNOWN
N/A
NONE
NOT_RUN
```

を使う。

fieldを削除しない。

---

# 7. Status

correction完了後:

```text
Status:
R2_COMPLETE
```

とする。

Gateは:

```text
NOT_READY_FOR_TEST
```

のまま。

---

# 8. Six-Failure Ledger — Required Detail

Trial 01の6 failureをtableで完全に記録する。

最低限:

| Failure ID | Test node | Trial 01 result | Failure assertion | Isolated result | Root cause | Final disposition |
|---|---|---|---|---|---|---|

Failure IDs:

```text
F-01
F-02
F-03
F-04
F-05
F-06
```

各行でactual test nodeを完全に書く。

`G03 test` 等の省略だけでは不足。

---

# 9. Final Failure Classification Counts

R2 reportへsummaryを追加する。

例:

```text
Failure classification summary:

IMPLEMENTATION_DEFECT:
0

TEST_FIXTURE_ISOLATION_DEFECT:
5

TEST_CONTRACT_DEFECT:
0

ENVIRONMENT_OR_RUNNER_DEFECT:
0

ALREADY_CLOSED_BY_R1:
1

REPORT_ONLY:
0

Remaining unclassified:
0
```

actual R2 classificationに合わせる。

---

# 10. R1 Closure Mapping

F-01等、R1で閉じたfailureについて:

```text
R1 report
R1 checkpoint
isolated retry result
isolated G03 evidence
```

への対応を明示する。

単に:

```text
closed by R1
```

とだけ書かない。

---

# 11. Isolated Reproduction Matrix

各F-01〜F-06について:

```text
isolated rerun command
exit code
passed / failed / skipped
evidence directory
tested SHA/state
```

をtableまたは個別entryで示す。

R1 evidenceを再利用する場合も:

```text
Evidence source:
E4-G05_02_R1_predictive_retry_remediation_report.md
Verification V-XX
```

まで具体的に記載する。

---

# 12. Original Combined Scope

Trial 01で失敗したoriginal combined invocationを完全形で記載する。

必須:

```text
Purpose

Exact command

ARIADNE_TEST_EVIDENCE_DIR

Tested SHA

Exit code

Passed

Failed

Skipped

Failed nodes

Expected

Actual

Facts

Interpretation
```

Trial 01 Test Agent reportにしかcommandがない場合、
そこからactual commandを正確に転記する。

推測で再構成しない。

---

# 13. Combined Scope Interpretation

original combined invocationについて:

```text
32 passed / 6 failed
```

が何を意味するかFacts / Interpretationを分離する。

例:

```text
Facts:
- all-in-one invocation returned exit 1.
- six nodes failed.
- clean isolated invocations for those contract areas passed.
- preceding tests left queue/stage state used by later tests.

Interpretation:
- the all-in-one invocation is not a valid isolation boundary for all included contracts.
- the failures do not establish six independent production defects.
- semantic partitioning is required for acceptance evidence.
```

actual evidenceに合わせる。

---

# 14. Corrected Standardized Test Partition

R2で採用したcorrected partitionを明示する。

例:

```text
Partition A:
G05 / G02 / G04 convergence contracts

Partition B:
G03 isolated StageExecution contracts

Partition C:
Predictive retry

Partition D:
Predictive rerun

Partition E:
Predictive revise
```

actual実行構成へ合わせる。

各partitionについて:

```text
exact command
evidence dir
tested SHA
exit code
passed
failed
skipped
```

を記録する。

---

# 15. No “Same as Previous” Commands

禁止:

```text
same as previous
same command
V-03内
上記と同じ
関連testを実行
```

各verification entryでcopy-pastable complete commandを書く。

---

# 16. G02 Regression Section

独立sectionを作る。

最低限:

```text
## G02 Regression

Covered contract:
- canonical Execution identity
- canonical claim / lease
- lifecycle where relevant

Exact command:
...

Evidence directory:
...

Tested SHA:
...

Exit code:
...

Passed:
...

Failed:
...

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

# 17. G03 Regression Section

独立isolated evidenceを記載する。

R1bで確認した:

```text
6 passed
0 failed
exit 0
```

をactual command/evidenceとともに記載する。

combined G03 failureとisolated PASSを混同しない。

---

# 18. G04 Regression Section

Result / Artifact authority関連regressionを完全証跡で記載する。

最低限:

```text
Result ownership
Artifact ownership
typed reuse
physical ArtifactStore boundary
```

のcoverageを説明する。

---

# 19. Phase B Regression

Exploratory canonical projectionについて:

```text
canonical list/get results
canonical downstream draft
no FamilyResult authority fallback
```

をどのtestで確認したか記録する。

exact command必須。

---

# 20. Phase C Regression

最低限以下を明示する。

```text
C1 Golden Path
C2 retry
C3a rerun
C3b revise
C4 authority audit
```

それぞれがどのverification/commandに含まれるかを明確にする。

必要なら複数commandでよい。

---

# 21. Phase D Regression

最低限:

```text
D1 claim/process shutdown
D2 lifecycle/write shutdown
D3 global authority audit
```

をどのtestで確認したか記録する。

---

# 22. R1 Regression

R1 final state:

```text
Predictive isolated retry PASS

Trial 01 isolated failure:
NOT_REPRODUCED
ROOT_CAUSE_UNCONFIRMED

Combined contamination:
TEST_FIXTURE_ISOLATION_DEFECT

G03 isolated PASS

C3a PASS

C3b PASS
```

をR2 reportから参照可能にする。

---

# 23. No-Legacy-Authority Regression Section

新規sectionを追加する。

最低限:

```text
## No-Legacy-Authority Regression

FamilyExecution new Product write:
NONE

FamilyStageExecution new Product write:
NONE

FamilyResult new Product write:
NONE

FamilyArtifact new Product write:
NONE

family-specific claim authority:
NONE

canonical failure -> old fallback:
NONE

GenericExecutor authority:
NO
```

これらがどのtest/evidenceで確認されたかを併記する。

---

# 24. Exact Verification Evidence Section

独立した:

```text
## Exact Verification Evidence
```

を設ける。

各entryのrequired fields:

```text
Verification ID
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

# 25. Verification IDs

最低限以下のlogical entryを持つ。

```text
V-01 Original Trial 01 combined scope

V-02 Predictive isolated retry / R1 reference

V-03 Isolated G03

V-04 C3a rerun independent

V-05 C3b revise independent

V-06 G02/G04/G05 convergence partition

V-07 Phase B Exploratory regression

V-08 Phase D authority regression

V-09 Any remaining failure-specific isolated verification
```

actual runsに合わせて増減してよいが、
required contractをすべてcoverする。

---

# 26. Evidence Directory / Raw Evidence

各runner invocationで:

```text
ARIADNE_TEST_EVIDENCE_DIR
```

を記載する。

raw evidence file pathを把握できる場合は記載。

不明なら:

```text
Raw evidence path:
UNKNOWN
```

とする。

field削除禁止。

---

# 27. Tested SHA / State Accuracy

各verification runの実行時点を正確に書く。

例:

```text
Tested HEAD:
<sha>

R1 implementation/test checkpoint:
ad3e3e124ee47f9cbaa2470b25263b7289795262

R2 checkpoint:
1dd20d2a6b2d7e85c3116e7b019024883e7d9786

Production/test delta after R1:
NONE
```

actualに合わせる。

---

# 28. Files Changed Section

R2について明示する。

```text
## Files Changed

### Production
NONE

### Tests
NONE

### Fixtures
NONE

### Migrations
NONE

### Documentation
- E4-G05_02_R2_combined_regression_remediation_report.md
```

R2a correction commit分もdocument-onlyとする。

---

# 29. Migration

```text
Migration head:
20260809_product_0010

New migration in R2:
NONE

New migration in R2a:
NONE
```

を明示する。

---

# 30. Remaining Trial 02 Work

R2 reportには以下をOPENとして残す。

```text
R3:
G05 Implementation Completion Report
template-compliant full regeneration

Final Trial 02 acceptance:
- fixed implementation/test target SHA
- full implementation-side acceptance
- READY_FOR_TEST re-establishment
```

R2aで実行しない。

---

# 31. Report Commit Metadata

既存reportに:

```text
Report commit
```

がある場合はinitial report commit SHAを保持する。

今回のcorrection commitは別field:

```text
R2 report correction commit:
<full SHA>
```

として記載する。

self-referenceを避ける。

---

# 32. Git Verification

R2a作業後:

```bash
git diff --check
git status --short

git diff \
  -- src tests migrations scripts
```

R2a自身によるproduction/test/migration/script差分がないこと。

report file差分のみであることを確認する。

---

# 33. R2 Completion Criteria — Final

以下を全て満たすこと。

```text
[ ] six-failure ledger complete

[ ] 6 / 6 actual failing nodes identified

[ ] classification summary complete

[ ] remaining unclassified = 0

[ ] R1 closure mapping complete

[ ] isolated reproduction matrix complete

[ ] original combined scope exact command recorded

[ ] original combined result:
    exit / passed / failed / skipped recorded

[ ] corrected standardized partition documented

[ ] each partition exact command recorded

[ ] G02 regression evidence complete

[ ] G03 isolated regression evidence complete

[ ] G04 regression evidence complete

[ ] Phase B regression evidence complete

[ ] Phase C regression evidence complete

[ ] Phase D regression evidence complete

[ ] R1 regression evidence complete

[ ] No-Legacy-Authority Regression section complete

[ ] Family 4-table new-write = NONE documented

[ ] canonical failure -> old fallback = NONE documented

[ ] GenericExecutor authority = NO documented

[ ] Exact Verification Evidence section complete

[ ] evidence dirs recorded

[ ] raw evidence paths recorded or UNKNOWN

[ ] tested SHA/state recorded

[ ] Facts / Interpretation separated

[ ] R2 production changes = NONE

[ ] R2 test changes = NONE

[ ] R2 fixture changes = NONE

[ ] R2 checkpoint classified as evidence-boundary empty commit

[ ] migration head = 20260809_product_0010

[ ] R2 Decision = R2_COMPLETE

[ ] Gate = NOT_READY_FOR_TEST

[ ] git diff --check PASS

[ ] R2 report correction commit created
```

---

# 34. Stop Reasons NOT Accepted

以下を途中停止理由として認めない。

```text
evidence commandを調べる必要がある

reportが長くなる

R2は技術的には終わっている

isolated evidenceが別reportにある

same as R1で十分

R3がまだ残っている
```

R2aはreport/evidence completionのための作業である。

最後まで閉じる。

---

# 35. Final Stop Condition

正しい終了条件:

```text
R2_COMPLETE
```

最後に必ず:

```text
E4-G05 Trial 02
R2_COMPLETE

R1 implementation/test checkpoint:
ad3e3e124ee47f9cbaa2470b25263b7289795262

R2 checkpoint:
1dd20d2a6b2d7e85c3116e7b019024883e7d9786

R2 checkpoint type:
EVIDENCE_BOUNDARY_EMPTY_COMMIT

R2 report correction commit:
<full SHA>

Trial 01 failure ledger:
6 / 6 classified

IMPLEMENTATION_DEFECT:
0

TEST_FIXTURE_ISOLATION_DEFECT:
5

ALREADY_CLOSED_BY_R1:
1

Remaining unclassified:
0

Runtime acceptance defect currently demonstrated:
NONE

G02:
PASS

G03 isolated:
PASS

G04:
PASS

Phase B:
PASS

Phase C:
PASS

Phase D:
PASS

R1:
PASS

Family old-authority writes:
NONE

Canonical failure -> old fallback:
NONE

Migration head:
20260809_product_0010

Production/test/fixture changes in R2a:
NONE

Remaining Trial 02:
- R3 G05 completion report format remediation
- final Trial 02 acceptance / READY_FOR_TEST

Gate:
NOT_READY_FOR_TEST
```

を報告して停止する。

R2a完了後、このrunでR3へ進まないこと。
