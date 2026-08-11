# E4-G05 Trial 02 / R3 — Implementation Completion Report Regeneration and READY_FOR_TEST Handoff Instruction

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 — eliminate dual execution
- Branch: `refactor/ariadne_mvp_e4`
- Gate: `E4-G05`
- Trial: `02`
- Remediation package: `R3`
- Remediation name: Trial 02 Implementation Completion Report regeneration and final Coding Agent handoff
- Trial 01 failed implementation SHA: `ddb009875ef4e649f413cb0bb7f7a85f894e2b14`
- R1 implementation/test checkpoint: `ad3e3e124ee47f9cbaa2470b25263b7289795262`
- R2 evidence-boundary checkpoint: `1dd20d2a6b2d7e85c3116e7b019024883e7d9786`
- R2 report/evidence correction commit: `9bd7d00dcef1fb6518beb989f9e88c5a6abaaf9d`
- Expected Product migration head: `20260809_product_0010`
- Current Gate status: `NOT_READY_FOR_TEST`
- Target Coding Agent status: `READY_FOR_TEST`
- This instruction MUST NOT declare Gate PASS

---

# 1. Purpose

E4-G05 Trial 02をCoding Agent側で完了し、Independent Test Agentへ再提出できる状態へ戻す。

Trial 01はIndependent Test AgentによりFAILとなった。

Trial 02では以下を実施済み。

```text
R1:
Predictive retry isolated diagnosis/remediation
→ COMPLETE

R1a/R1b:
root-cause/evidence correction
isolated G03 / C3a / C3b verification
→ COMPLETE

R2:
Trial 01 six-failure classification
→ 6 / 6 classified
→ confirmed production defect NONE

R2a:
R2 evidence/report completion
→ COMPLETE
```

R3ではproduction architectureを追加変更しない。

R3の主目的は:

> Trial 02という1 transactionのImplementation Completion Reportを、repositoryの現行v2 template/specificationへ完全準拠させ、fixed implementation/test candidateを明示し、Coding Agent handoffをREADY_FOR_TESTへ戻すこと

である。

---

# 2. Authoritative Template / Specification

必ずrepository上の現行templateを直接読む。

```text
docs/wiki/develop_memo/_work/
agentic_enhancement_workflow_template/
20_implementation_reports/
README.md

docs/wiki/develop_memo/_work/
agentic_enhancement_workflow_template/
20_implementation_reports/
TEMPLATE_implementation_completion_report.md
```

テンプレートを要約して独自formatへ置き換えない。

必須field / sectionを削除・統合・短縮しない。

値が存在しない場合:

```text
N/A
NONE
NOT_RUN
UNKNOWN
```

を使用する。

blankは禁止。

---

# 3. Trial 01 Completion Report Is Historical Evidence

以下はTrial 01のhistorical transaction recordであり、上書きしない。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G05/Trial01/
E4-G05_01_implementation_completion_report.md
```

Trial 01 reportのformat不備はTrial 01 Gate FAIL evidenceの一部として残す。

R3では新規にTrial 02 reportを作成する。

---

# 4. Trial 02 Completion Report Path

新規作成:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G05/Trial02/
E4-G05_02_implementation_completion_report.md
```

Trial 02の唯一のImplementation Completion Reportとする。

R1/R2 remediation reportsはsupplemental evidenceとして参照する。

---

# 5. Fixed Implementation/Test Candidate

最初に以下を検証する。

```bash
git diff \
  ad3e3e124ee47f9cbaa2470b25263b7289795262..HEAD \
  -- src tests migrations scripts
```

actual repository path layoutに合わせる。

期待:

```text
production/test/migration/script delta after R1 checkpoint:
NONE
```

これが成立する場合、Trial 02のfixed implementation/test candidateは:

```text
ad3e3e124ee47f9cbaa2470b25263b7289795262
```

とする。

理由:

```text
- Trial 02で最後にproduction/test stateへ影響したcheckpoint
- R2/R2aはproduction/test/fixture remediation NONE
- 以降はinstruction/report/evidence-only commits
```

重要:

```text
Implementation commit
≠ report commit
≠ report correction commit
≠ evidence-boundary empty commit
```

Report commitをimplementation commitとして使用しない。

---

# 6. If Source/Test Delta Exists After R1 Checkpoint

もし:

```bash
git diff ad3e3e...HEAD -- src tests migrations scripts
```

が非emptyの場合、勝手に`ad3e3e...`をfixed candidateにしてはならない。

差分を分類する。

```text
authorized Trial 02 remediation
unrelated change
unexpected change
```

authorized Trial 02 remediationなら、そのlatest code/test checkpointをfixed candidateとする。

unrelated / unexpectedでcandidateを一意に固定できない場合:

```text
R3_BLOCKED
```

として停止する。

ただしdocs-only差分はcandidate変更理由にならない。

---

# 7. Starting Commit

Trial 02のStarting commitは、Trial 01 FAILを受けてTrial 02 remediationが開始された時点のactual commitをrepository historyから特定する。

推測しない。

reportにはfull SHAで:

```text
Starting commit:
<full SHA>
```

を記載する。

Trial 01 failed implementation SHA:

```text
ddb009875ef4e649f413cb0bb7f7a85f894e2b14
```

とは別fieldとして記録してよい。

---

# 8. 06 Contract

reportの:

```text
06 Contract
```

にはGate authorityであるoriginal G05 coding contractを記載する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
10_enhance_instruction/G05/
06_Ariadne_ENH-E4_G05_実装指示書.md
```

actual path/nameをrepositoryで確認する。

Phase A–Eの06系instructionはImplementation summary / supplemental inputとして列挙してよいが、
06 Contract authorityを置き換えない。

---

# 9. Applicable 08 Remediation

repositoryにformal `08` remediation deltaが存在しない場合:

```text
Applicable 08 Remediation:
NONE
```

とする。

その上でTrial 02 project-specific remediation inputsを別途列挙する。

```text
06k01 — R1 Predictive retry remediation
06k02 — R1a report correction
06k03 — R1b isolated G03 verification
06k04 — R2 combined regression remediation
06k05 — R2a evidence/report correction
06k06 — R3 completion report regeneration
```

actual filenamesを完全に記録する。

formal 08が存在するならactual pathを使用する。

---

# 10. Required Report Header

templateに従い最低限:

```text
# E4-G05 Trial 02 Implementation Completion Report

- Project
- Enhancement
- Gate
- Trial
- Status
- Starting commit
- Implementation commit
- Report commit
- 06 Contract
- Applicable 08 Remediation
- Timestamp
```

を完全に埋める。

追加metadataとして以下を持ってよい。

```text
- Branch
- Trial 01 failed implementation SHA
- R1 checkpoint
- R2 evidence-boundary checkpoint
- R2 report/evidence correction commit
- Migration head
```

Statusは最終handoff時:

```text
READY_FOR_TEST
```

とする。

---

# 11. Implementation Summary — Must Cover Whole Trial 02

Trial 02 transaction全体を説明する。

最低限:

```text
Trial 01 failure input

R1:
Predictive retry isolated re-diagnosis
test diagnostic hardening
production queue semantics unchanged

R1a/R1b:
root cause correction
isolated G03 / C3a / C3b evidence completion

R2:
six-failure ledger
5 TEST_FIXTURE_ISOLATION_DEFECT
1 ALREADY_CLOSED_BY_R1
0 IMPLEMENTATION_DEFECT

R2a:
exact evidence / phase regression / no-legacy-authority evidence completion

R3:
completion report regeneration only
```

Trial 02 production changeがNONEなら明示する。

Trial 02 test changeはactualに基づいて記録する。

---

# 12. Changed Files

templateどおりtableで:

```text
Path | Change | Reason
```

を記録する。

Trial 02全体のtransaction recordとして、
R1で変更されたtest file、
R1/R2 reports、
06k01–06k06 instructions、
Trial 02 completion reportをactual diff/historyから列挙する。

production filesが変更されていなければ:

```text
Production:
NONE
```

と明示する。

ファイル数を推測しない。

---

# 13. Observable Implementation Facts

最低限、以下をFactsとして記録する。

```text
1. Causal / Exploratory / Predictive Product submission authority
   = canonical Execution

2. persistent StageExecution authority
   = canonical Product StageExecution

3. claim / lease authority
   = canonical execution repository

4. Result / Artifact ownership
   = G04 canonical owner

5. FamilyExecution / FamilyStageExecution / FamilyResult / FamilyArtifact
   new Product write authority
   = NONE

6. canonical failure -> old authority fallback
   = NONE

7. GenericExecutor Product lifecycle authority
   = NO

8. Predictive retry:
   same Execution ID
   FAILED -> QUEUED
   retry_count increment
   persistent StageExecution IDs retained
   attempt history retained/appended

9. queue semantics:
   no retry priority introduced

10. R2:
    no confirmed production defect remained
```

事実と解釈を混ぜない。

---

# 14. Schema / Migration / API / Runtime Impact

template sectionを完全に埋める。

最低限:

```text
Schema:
Phase A migration 20260809_product_0010 remains head

New Trial 02 migration:
NONE

Historical application data migration:
NONE

API impact:
family-facing adapters remain allowed
authority is canonical

Runtime impact:
Product worker canonical claim/processor
legacy family mutation/claim/process authority disabled

CLI impact:
auditable Product CLI canonical submit
low-level scientific CLI outside persistent Product lifecycle
```

actual code/report evidenceに合わせる。

G06 lineage final cutoverはここで実施済みと書かない。

---

# 15. Protected Passed-Gate Impact

template tableを埋める。

最低限:

```text
G01
G02
G03
G04
```

各Gateについて:

```text
Touched?
Preserved semantic
Self-check / evidence
```

を記載する。

特に:

```text
G02:
canonical Execution / claim / retry-rerun-revise semantics preserved

G03:
persistent StageExecution / attempt history / GenericExecutor boundary preserved

G04:
Result / Artifact ownership and typed reuse preserved
```

を明示する。

Coding Agent self-checkはGate acceptance evidenceではないことも保持する。

---

# 16. Transition Debt Impact

template tableを完全に埋める。

G05で:

```text
TD-001 CLOSED
TD-002 CLOSED
TD-003 CLOSED
```

を記録する。

さらに:

```text
TD-004 OPEN
Owner / exit Gate: G06
Purpose: lineage authority consolidation
```

を明示する。

G05 completion reportでTD-004をCLOSEDにしない。

TD-005/TD-006はG05で新たに閉じたと書かない。

---

# 17. Coding Agent Self-Checks

template section:

```text
Command | Exit code | Result summary
```

を完全に埋める。

R1/R2で実際に実行済みのself-checkを正確に転記してよい。

必須contract coverage:

```text
Predictive isolated retry

G03 isolated

C3a rerun

C3b revise

G02

G04

Phase B

Phase C

Phase D

No-Legacy-Authority
```

---

# 18. Evidence Reuse Rule

既存R1/R2 reportからevidenceを再利用してよい条件:

```text
[ ] exact command exists

[ ] exit code exists

[ ] pass/fail/skip count exists

[ ] tested SHA/state exists

[ ] evidence directory exists or UNKNOWN is explicit

[ ] candidate source/test state is identical
```

candidate source/test stateが同一であることを:

```bash
git diff <tested-state>..<fixed-candidate> -- src tests migrations scripts
```

等で確認する。

---

# 19. Do Not Re-run Expensive Suites Without Need

R3の目的はreport regenerationである。

以下が成立する場合、R1/R2で既にPASSしたfull PostgreSQL suitesを機械的に再実行する必要はない。

```text
- exact evidence exists
- tested source/test state is fixed candidateと同一
- no production/test/migration delta exists
```

ただし証跡が欠落しているcontractがある場合のみ、そのmissing verificationを実行する。

これは証拠不足を文章でごまかすという意味ではない。

---

# 20. Candidate Integrity Verification

最低限R3で実行する。

```bash
git rev-parse HEAD
git status --short
git diff --check

git diff \
  ad3e3e124ee47f9cbaa2470b25263b7289795262..HEAD \
  -- src tests migrations scripts
```

Expected:

```text
source/test/migration/script delta:
NONE
```

actual path layoutに合わせる。

---

# 21. Migration Head Verification

standard PostgreSQL runner evidenceから:

```text
20260809_product_0010
```

を確認する。

必要なら低コストのstandard runner verificationを1回行う。

manual PostgreSQL / manual Alembicは禁止。

---

# 22. Known Limitations / Unresolved Observations

最低限:

```text
Independent Test Agent verification still required.

TD-004 remains OPEN for G06 lineage authority consolidation.

Historical bounded read-only compatibility may remain until G07 where contract permits.

G06 final lineage authority cutover is not part of G05.

G07 broad legacy retirement is not part of G05.

G08 final clean bootstrap/audit is not part of G05.
```

を記録する。

Trial 01 isolated retry failureは:

```text
NOT_REPRODUCED
ROOT_CAUSE_UNCONFIRMED
```

としてhistorical observationに残してよい。

production defectと書かない。

---

# 23. Handoff to Test Agent

template sectionを完全に埋める。

```text
Tested candidate commit:
ad3e3e124ee47f9cbaa2470b25263b7289795262
```

ただしSection 5/6のcandidate verificationで別SHAが確定した場合はactualを使う。

```text
Required completion report path:
docs/.../G05/Trial02/E4-G05_02_implementation_completion_report.md

Expected next action:
Independent verification under original G05 07 contract
```

Test Agent targetをreport commitにしない。

---

# 24. Test Contract Remains Original G05 07

Independent Test Agentは:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
10_enhance_instruction/G05/
07_Ariadne_ENH-E4_G05_テスト指示書.md
```

をAcceptance Criteria authorityとして使用する。

R1/R2 remediation reportでACを書き換えない。

Trial 01 FAIL reportもhistorical evidenceとして参照可能だが、07をoverrideしない。

---

# 25. Fact / Interpretation Separation

templateのSection 10を省略しない。

## Facts

最低限:

```text
- fixed candidate SHA
- changed files
- migration head
- exact test results
- failure classifications
- no legacy write evidence
- TD status
```

## Interpretation

最低限:

```text
- Coding Agent considers implementation ready for independent verification.
- self-check PASS does not constitute Gate PASS.
- Trial 01 combined failures do not currently demonstrate remaining production defects.
```

とする。

---

# 26. Supplemental Evidence Sections Are Allowed

templateの10 sectionを完全保持した上で、
必要なら以下を追加してよい。

```text
## 11. Trial 02 Remediation Ledger

## 12. Exact Verification Evidence

## 13. No-Legacy-Authority Evidence

## 14. Git / Candidate Integrity Evidence

## 15. Trial 01 FAIL Closure Mapping
```

ただしtemplate sectionを置き換えない。

---

# 27. Trial 02 Remediation Ledger

以下をtableで追跡可能にする。

| Package | Instruction | Result report | Outcome | Code/Test impact |
|---|---|---|---|---|
| R1 | 06k01 | R1 report | COMPLETE | diagnostic test hardening |
| R1a | 06k02 | R1 report correction | COMPLETE | docs only |
| R1b | 06k03 | R1 report correction | COMPLETE | verification/docs |
| R2 | 06k04 | R2 report | COMPLETE | production/test/fixture NONE |
| R2a | 06k05 | R2 report correction | COMPLETE | docs only |
| R3 | 06k06 | Trial02 completion report | READY_FOR_TEST | docs only |

actual historyに合わせる。

---

# 28. Trial 01 FAIL Closure Mapping

Trial 01 Gate FAILの主要2理由を明示する。

```text
A. Predictive retry independent failure
B. mandatory regression 32 passed / 6 failed
C. completion report format noncompliance
```

Trial 02 closure:

```text
A:
NOT_REPRODUCED / ROOT_CAUSE_UNCONFIRMED
isolated candidate/claim PASS

B:
6 / 6 classified
5 TEST_FIXTURE_ISOLATION_DEFECT
1 ALREADY_CLOSED_BY_R1
0 IMPLEMENTATION_DEFECT
remaining unclassified 0

C:
Trial 02 completion report regenerated from current template
```

これはCoding Agent interpretation/closure recordであり、
Gate PASS判定ではない。

---

# 29. No-Legacy-Authority Evidence

Trial 02 reportから独立Test Agentが追跡できるように:

```text
FamilyExecution Product new-write:
NONE

FamilyStageExecution Product new-write:
NONE

FamilyResult Product new-write:
NONE

FamilyArtifact Product new-write:
NONE

family-specific claim authority:
NONE

canonical failure -> old fallback:
NONE

GenericExecutor Product authority:
NO
```

と、それぞれのself-check/evidence sourceを記録する。

---

# 30. Report Format Self-Audit

report作成後、templateとfield-by-fieldで比較する。

最低限checklist:

```text
[ ] title correct

[ ] Project

[ ] Enhancement

[ ] Gate

[ ] Trial

[ ] Status

[ ] Starting commit

[ ] Implementation commit

[ ] Report commit

[ ] 06 Contract

[ ] Applicable 08 Remediation

[ ] Timestamp

[ ] 1. Implementation summary

[ ] 2. Changed files

[ ] 3. Observable implementation facts

[ ] 4. Schema / migration / API / runtime impact

[ ] 5. Protected passed-Gate impact

[ ] 6. Transition Debt impact

[ ] 7. Coding Agent self-checks

[ ] self-check disclaimer retained

[ ] 8. Known limitations / unresolved observations

[ ] 9. Handoff to Test Agent

[ ] 10. Fact / interpretation separation

[ ] no blank fields

[ ] N/A/NONE/NOT_RUN/UNKNOWN used where required

[ ] exact commands copy-pastable

[ ] implementation commit != report commit

[ ] Gate PASS not claimed
```

---

# 31. Report Commit Procedure

新規Trial 02 completion reportの初版では:

```text
Report commit:
PENDING
```

とする。

report作成後にcommit。

Suggested commit:

```text
E4-G05 Trial 02 implementation completion report
```

commit後:

```bash
git rev-parse HEAD
```

でinitial report commit SHAを取得する。

その後report metadataの:

```text
Report commit:
<initial report commit full SHA>
```

へ更新する。

metadata correction commitを作る。

Suggested:

```text
E4-G05 Trial 02 completion report metadata
```

`Report commit` fieldをmetadata correction SHAへ置き換えない。

必要なら:

```text
Report metadata correction commit:
<full SHA>
```

を追加する。

self-referenceを避ける。

---

# 32. Final Git Verification

最終的に:

```bash
git status --short
git diff --check

git diff \
  ad3e3e124ee47f9cbaa2470b25263b7289795262..HEAD \
  -- src tests migrations scripts
```

を確認する。

R3自身によるproduction/test/migration/script delta:

```text
NONE
```

であること。

---

# 33. Current Architecture Control Sheet

R3で更新しない。

理由:

```text
Current Architecture Control Sheet
= final PASS済みverified stateのみをpromotionするcontrol plane
```

G05 Trial 02はまだIndependent Test Agent未実施。

したがって:

```text
G05 PASS前:
update禁止

G05 PASS後:
operatorがCurrent Architecture Control Sheetを更新
```

とする。

---

# 34. READY_FOR_TEST Criteria

以下を全て満たした場合のみ:

```text
READY_FOR_TEST
```

とする。

```text
[ ] R1 COMPLETE

[ ] R2 COMPLETE

[ ] fixed candidate SHA uniquely established

[ ] no unexplained source/test/migration delta after candidate

[ ] migration head = 20260809_product_0010

[ ] Trial 02 completion report created at required path

[ ] template sections 1–10 complete

[ ] no blank required fields

[ ] exact self-check evidence traceable

[ ] G02/G03/G04 protected semantics recorded

[ ] Phase A–E implementation state traceable

[ ] no-legacy-authority evidence traceable

[ ] TD-001 CLOSED

[ ] TD-002 CLOSED

[ ] TD-003 CLOSED

[ ] TD-004 OPEN -> G06

[ ] Trial 01 FAIL closure mapping complete

[ ] report initial commit recorded

[ ] git diff --check PASS

[ ] Coding Agent does not claim Gate PASS
```

---

# 35. Do Not Perform Independent Gate Decision

禁止:

```text
G05 PASS

Gate Decision PASS

verified current architecture promoted

G06 start
```

R3の責務は:

```text
Coding Agent:
READY_FOR_TEST
```

まで。

Independent Test AgentがG05 Trial 02を検証する。

---

# 36. Stop Reasons NOT Accepted

以下を途中停止理由として認めない。

```text
reportが長い

evidenceがR1/R2 reportに分散している

exact commandを転記する必要がある

templateとの比較が必要

report commit metadata correctionが必要

Independent Test Agentがまだなので書けない
```

これらはR3 scopeそのものである。

最後まで完了する。

---

# 37. Failure / Blocked Conditions

以下の場合のみ`READY_FOR_TEST`にしない。

## Candidate inconsistency

```text
unexpected source/test/migration delta exists
```

→ `R3_BLOCKED`

## Missing required evidence

既存R1/R2 evidenceにもなく、必要verificationも実行できない。

→ `R3_BLOCKED`

## Contract contradiction

06 / 07 / passed Gate / actual implementationが解消不能に矛盾する。

→ `DESIGN_BLOCKED`

単なるreport作成量はBLOCKED理由ではない。

---

# 38. Final Stop Condition

正常完了時:

```text
E4-G05 Trial 02
R3_COMPLETE
READY_FOR_TEST
```

最後に必ず以下を報告する。

```text
E4-G05 Trial 02
R3_COMPLETE
READY_FOR_TEST

Trial 01 failed implementation SHA:
ddb009875ef4e649f413cb0bb7f7a85f894e2b14

Fixed Trial 02 implementation/test candidate:
<full SHA>

Expected fixed candidate if source/test state unchanged:
ad3e3e124ee47f9cbaa2470b25263b7289795262

Trial 02 completion report:
docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G05/Trial02/E4-G05_02_implementation_completion_report.md

Report initial commit:
<full SHA>

Report metadata correction commit:
<full SHA or NONE>

Migration head:
20260809_product_0010

R1:
COMPLETE

R2:
COMPLETE

Trial 01 runtime failures:
CLOSED FOR CODING HANDOFF

Implementation defect remaining:
NONE DEMONSTRATED

Family old-authority writes:
NONE

Canonical failure -> old fallback:
NONE

TD-001:
CLOSED

TD-002:
CLOSED

TD-003:
CLOSED

TD-004:
OPEN -> G06

Current Architecture Control Sheet:
NOT UPDATED — WAITING FOR INDEPENDENT G05 PASS

Next action:
Independent Test Agent — E4-G05 Trial 02

Gate:
READY_FOR_TEST
NOT YET PASS
```

を報告して停止する。

このrunでIndependent Test Agentを実行しない。
このrunでG06へ進まない。
