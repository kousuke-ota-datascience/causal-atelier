# E4-G05 Trial 01 — Phase E Final Acceptance / Gate Handoff 実装指示書

推奨ファイル名:

```text
06k01_Ariadne_ENH-E4_G05_PhaseE_実装指示書.md
```

---

## 0. Control Header

* Project: Ariadne / causal-atelier
* Enhancement: ENH-E4 — eliminate dual execution
* Branch: `refactor/ariadne_mvp_e4`
* Gate: `E4-G05`
* Gate name: Product Execution Convergence
* Trial: `01`
* Phase: `E`
* Phase name: Final acceptance / transition-debt closure / Test Agent handoff
* Phase A: `COMPLETE`
* Phase B: `COMPLETE`
* Phase C: `COMPLETE`
* Phase D: `COMPLETE`
* Phase D final implementation checkpoint: `d766b85a22eaff999c3981c7ceb5e675eb8803c7`
* Phase D report commit: `5091ec1ec800c70ed66fd6df48b6e50157c253a3`
* Expected Product migration head: `20260809_product_0010`
* Current Gate status: `NOT_READY_FOR_TEST`
* Target Phase E status: `PHASE_E_COMPLETE`
* Target Gate handoff status: `READY_FOR_TEST`

---

# 1. Purpose

E4-G05 Trial 01を完了させる。

Phase A〜Dでproduction architecture implementationは完了した。

Phase Eの目的は新しいarchitectureを追加することではない。

Phase Eでは以下を行う。

```text
1. Causal / Exploratory / Predictive final Golden Paths
2. G05 acceptance contractの最終横断監査
3. D1/D2/D3 authority shutdownの最終確認
4. passed G02/G03/G04 regression
5. Phase A/B/C/D regression
6. TD-001 / TD-002 / TD-003 の正式closure
7. TD-004 をOPENのままG06へ正式handoff
8. fixed final G05 implementation SHAを確定
9. Phase E checkpoint reportを作成
10. G05 implementation completion reportを作成
11. READY_FOR_TEST を宣言
```

Phase E終了後はIndependent Test Agentへ固定SHAを渡す。

Phase E自身では:

```text
G05 PASS
```

を宣言しない。

Gate PASS / FAILはIndependent Test AgentのTest Item 999で判定する。

---

# 2. Trial Rule

現在は引き続き:

```text
E4-G05 Trial 01
```

である。

Phase E内のimplementation-side acceptance testでFAILを発見してもTrial番号を増やさない。

correct testによるproduction defectの場合:

```text
production remediation
    ↓
same Trial 01
    ↓
re-run acceptance
    ↓
PASSまで修正
```

とする。

Trial 02へ進むのは、

```text
Independent Test Agent
    ↓
E4-G05 Trial 01 FAIL
```

が正式に発生した場合のみ。

---

# 3. Source of Truth

最低限以下を実物参照する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
10_enhance_instruction/G05/
06_Ariadne_ENH-E4_G05_実装指示書.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
10_enhance_instruction/G05/
07_Ariadne_ENH-E4_G05_テスト指示書.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G05/Trial01/
E4-G05_01_PhaseA_implementation_checkpoint_report.md

.../
E4-G05_01_PhaseB_implementation_checkpoint_report.md

.../
E4-G05_01_PhaseC_implementation_checkpoint_report.md

.../
E4-G05_01_PhaseD_implementation_checkpoint_report.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
00_ENH-E4_Current_Architecture_Control_Sheet.md
```

さらにG02/G03/G04のfinal Gate Decision / implementation report / test evidenceをactual repositoryから確認する。

Phase E開始時点でCurrent Architecture Control Sheetは更新しない。

これはG05 final Gate PASS後にoperatorが更新する。

---

# 4. Start-of-Work Verification

最初にactual repository stateを確認する。

```bash
git branch --show-current
git rev-parse HEAD
git status --short
git log -20 --oneline
git diff --check

git merge-base --is-ancestor \
  d766b85a22eaff999c3981c7ceb5e675eb8803c7 HEAD
echo $?
```

Expected:

```text
branch = refactor/ariadne_mvp_e4

Phase D final implementation checkpoint
d766b85a22eaff999c3981c7ceb5e675eb8803c7

is ancestor of HEAD
```

既存documentation-only commitがHEADに存在してもよい。

production/test変更とreport変更を混同しない。

---

# 5. Phase E Primary Gate Question

Phase Eのprimary questionは以下。

> 新しいuser-visible Product analysisをCausal / Exploratory / Predictiveのいずれからsubmitしても、Execution identity / claim / persistent StageExecution / Result / Artifact authorityがcanonical Product aggregate以外へ逃げる経路は残っているか。

Expected answer:

```text
NO
```

さらに:

> canonical pathがfailureした場合、old Family authorityへfallbackできるか。

Expected:

```text
NO
```

---

# 6. Final Target Architecture

G05 final implementationとして以下を固定する。

```text
Product API / auditable Product entry
        ↓
family request adapter
        ↓
canonical Execution Service
        ↓
canonical Execution + persistent StageExecution
        ↓
one canonical claim / lease authority
        ↓
Execution.analysis_family
        ↓
family-specific scientific runner
        ↓
canonical Result / Artifact owner
```

許容:

```text
family-specific DTO/projection
family-specific scientific implementation
bounded historical read-only adapter
low-level scientific CLI outside Product lifecycle
```

禁止:

```text
FamilyExecution new-write authority
FamilyStageExecution new-write authority
FamilyResult new-write authority
FamilyArtifact new-write authority

family-specific Product claimer

canonical failure -> legacy fallback

dual mutation authority

GenericExecutor persistence authority
```

---

# 7. Final Acceptance Matrix

Phase Eでは少なくとも以下をfinal matrixとして埋める。

| Contract                                   | Causal     | Exploratory | Predictive |
| ------------------------------------------ | ---------- | ----------- | ---------- |
| Product submit creates canonical Execution | PASS/FAIL  | PASS/FAIL   | PASS/FAIL  |
| persistent canonical StageExecution        | PASS/FAIL  | PASS/FAIL   | PASS/FAIL  |
| canonical claim authority                  | PASS/FAIL  | PASS/FAIL   | PASS/FAIL  |
| family dispatch after canonical claim      | PASS/FAIL  | PASS/FAIL   | PASS/FAIL  |
| canonical Result owner                     | PASS/FAIL  | PASS/FAIL   | PASS/FAIL  |
| canonical Artifact owner                   | PASS/FAIL  | PASS/FAIL   | PASS/FAIL  |
| old Family Execution write                 | NONE/FOUND | NONE/FOUND  | NONE/FOUND |
| old Family Stage write                     | NONE/FOUND | NONE/FOUND  | NONE/FOUND |
| old Family Result write                    | NONE/FOUND | NONE/FOUND  | NONE/FOUND |
| old Family Artifact write                  | NONE/FOUND | NONE/FOUND  | NONE/FOUND |
| canonical failure fallback                 | NONE/FOUND | NONE/FOUND  | NONE/FOUND |
| lifecycle mutation canonical               | PASS/N/A   | PASS/N/A    | PASS/N/A   |

存在しないfamily-specific surfaceは:

```text
N/A
NOT_EXPOSED
```

とする。

---

# 8. Final Causal Golden Path

actual Causal Product Golden Pathを実行する。

最低限:

```text
Product-facing Causal submission

canonical Execution created

analysis_family = CAUSAL

canonical StageExecution created

canonical claim

family dispatch after claim

scientific execution

canonical Result persisted

canonical Artifact persisted where applicable

terminal lifecycle reached

fresh session reload
```

同じscenario前後で:

```text
FamilyExecution
FamilyStageExecution
FamilyResult
FamilyArtifact
```

のnew-writeがないことを確認する。

---

# 9. Final Exploratory Golden Path

actual Exploratory Product Golden Pathを実行する。

最低限:

```text
Product-facing Exploratory submission

canonical Execution

persistent StageExecution

canonical claim/process

typed canonical Result

canonical Artifact where applicable

canonical read projection

downstream draft/create_analysis_draft behavior where applicable

fresh session reload
```

Phase Bで成立した:

```text
canonical list_results
canonical get_result
canonical create_analysis_draft
```

を維持する。

FamilyResult fallbackは禁止。

---

# 10. Final Predictive Golden Path

Phase Cで成立したPredictive Golden Pathをfinal stateで再確認する。

最低限:

```text
canonical Execution

persistent StageExecution

typed Results

typed Artifacts

input lineage

output lineage

terminal SUCCEEDED
```

Artifact cardinality:

```text
PARTITION_INDEX        exactly 1
FITTED_PREPROCESSOR    exactly 1
FITTED_MODEL           exactly 1
PREDICTION             exactly 1
```

Provenance:

```text
FITTED_PREPROCESSOR
  --DERIVED_FROM-->
PARTITION_INDEX

FITTED_MODEL
  --DERIVED_FROM-->
FITTED_PREPROCESSOR

PREDICTION
  --DERIVED_FROM-->
FITTED_MODEL

PREDICTION
  --EVIDENCE_FOR-->
EVALUATION_RESULT
```

Cartesian-product lineage等のtest-fitting implementationを再導入しない。

---

# 11. Predictive Mutation Final Regression

最低限以下をfinal stateで確認する。

## retry

```text
same canonical Execution ID

same StageExecution IDs

attempt history increment

no destructive legacy Result/Artifact reset
```

## rerun

```text
new canonical Execution ID

base_execution_id = original

revision_kind = RERUN

change_reason = NONE

new StageExecution IDs
```

## revise — changed condition

```text
new canonical Execution ID

base_execution_id = original

revision_kind = REVISED

explicit non-empty user-provided change_reason

changed scientific snapshot truthfully represented
```

## revise — same condition

canonical comparison contractに従い:

```text
RERUN
change_reason = NONE
```

を維持する。

---

# 12. Claim / Process Final Regression

D1で成立した以下を再確認する。

```text
Product worker:
uow.executions.claim_next()
    ↓
ExecutionProcessor
```

旧:

```text
ExploratoryWorkspaceService.claim_next
ExploratoryWorkspaceService.process_execution

PredictiveWorkflowService.claim_next
PredictiveWorkflowService.process_execution
```

がsourceに残る場合でも:

```text
EXPLICIT_REJECT
```

であること。

old Family SELECT FOR UPDATE authorityを再活性化しない。

---

# 13. Lifecycle / DI Final Regression

D2で成立した以下を維持する。

```text
Product mutation requires canonical dependency

canonical dependency missing
    -> explicit failure

NOT:
canonical dependency missing
    -> old Family mutation
```

FastAPI production composition:

```text
Exploratory service -> canonical ExecutionService injected

Predictive service -> canonical ExecutionService injected
```

であること。

---

# 14. Old Family Runtime Negative — Final Gate Evidence

Causal / Exploratory / Predictive final Golden Pathsおよび主要mutationについて:

```text
FamilyExecutionOrm
FamilyStageExecutionOrm
FamilyResultOrm
FamilyArtifactOrm
```

のbefore/after evidenceを取得する。

Required final conclusion:

```text
New Product FamilyExecution writes      = 0
New Product FamilyStageExecution writes = 0
New Product FamilyResult writes         = 0
New Product FamilyArtifact writes       = 0
```

insertだけでなく、可能な範囲で:

```text
UPDATE = 0
DELETE = 0
```

も証明する。

---

# 15. Canonical Failure No-Fallback Final Evidence

最低限以下をfinal regressionする。

```text
canonical submit/domain failure

canonical claim/process failure

canonical lifecycle mutation failure

canonical lookup miss
```

Expected:

```text
canonical error/domain error
    -> stop
```

Forbidden:

```text
-> old Family submit
-> old Family claim
-> old Family process
-> old Family mutation
```

Family 4-table side effect:

```text
NONE
```

---

# 16. Historical Read Compatibility

Phase Dで残したhistorical compatibilityを再確認する。

historical pathが残る場合:

```text
explicit
bounded
read-only
not canonical-miss fallback
not mutation authority
```

であること。

例:

```text
PredictiveSplitService historical partition artifact read
```

等。

historical read supportをPhase Eで新規拡張しない。

---

# 17. GenericExecutor Final Contract

G03/G04 contract:

```text
GenericExecutor
    = planning/order/binding/runner invocation/outcome
```

まで。

以下は持たない。

```text
Execution identity authority
claim/lease authority
persistent StageExecution authority
retry lifecycle authority
Result persistence authority
Artifact persistence authority
```

既存negative testsを維持する。

---

# 18. CLI Final G05 Classification

actual CLIを再inventoryする。

分類:

```text
LOW_LEVEL_SCIENTIFIC

AUDITABLE_PRODUCT

NOT_APPLICABLE
```

LOW_LEVEL_SCIENTIFIC:

```text
persistent Product lifecycleの外
```

でよい。

AUDITABLE_PRODUCT CLIが存在する場合:

```text
canonical Execution submit
```

を使う。

old Family lifecycleへのhidden entryは禁止。

Phase EではCLI source retirementをしない。

G07へ分類結果をhandoffする。

---

# 19. G05 Test Instruction Preflight

Independent Test Agentが実行するG05 Test Itemsを、implementation側でもpreflightする。

Test Item concept:

```text
001 commit/report/scope

002 route-to-canonical authority

003 Causal Golden Path

004 Exploratory Golden Path

005 Predictive Golden Path

006 cross-family authority

007 old-write shutdown negative

008 mutation/read/CLI

009 passed-Gate regression

010 transition/lineage deferral/report-format

999 Gate Decision
```

Phase Eでは:

```text
001〜010がTest Agentへ渡せる証拠状態か
```

を確認する。

ただし:

```text
30_test_report/G05/.../999
```

をCoding Agentが作成してはならない。

Gate DecisionはIndependent Test Agentの責務。

---

# 20. Passed Gate Regression

## G02

最低限:

```text
canonical Execution identity

claim / lease

cancel

retry

rerun

revise

revision comparison
```

## G03

最低限:

```text
persistent StageExecution

retry stable identity

attempt history

GenericExecutor negative
```

## G04

最低限:

```text
Result ownership

Artifact ownership

typed Result/Artifact reuse

Result ↔ Artifact association

physical ArtifactStore boundary

compensation/reconciliation relevant coverage
```

過去Gateのassertionを弱めない。

---

# 21. Phase Regression

最低限以下をfinal bundleへ含める。

```text
Phase A typed Result / Artifact contract

Phase B Exploratory convergence

Phase C Predictive:
    C1 Golden Path
    C2 retry
    C3a rerun
    C3b revise
    C4 authority audit

Phase D:
    D1 claim/process shutdown
    D2 lifecycle/write shutdown
    D3 global authority audit
```

---

# 22. Standard PostgreSQL Verification

real PostgreSQL verification entry pointは唯一:

```bash
scripts/test/run_product_postgres_tests.sh \
  <pytest paths/nodes> [...]
```

である。

禁止:

```text
manual docker
manual DSN
manual psql
manual Alembic
external ad-hoc PostgreSQL pytest
```

Phase E final evidenceでは可能な範囲でまとまったcommandを使う。

ただし既知のfixture isolation requirementがある場合はstandard runnerを複数回使ってよい。

その場合:

```text
why separated
exact command
exit code
pass/fail/skip
```

を記録する。

---

# 23. Acceptance Failure Handling

correct testでFAILした場合:

```text
implementation defect
    -> fix production
    -> add/harden test if needed
    -> rerun
```

Phase Eはacceptance-onlyだからという理由でbroken productionを残さない。

ただし以下をしない。

```text
test assertionを意味なく弱める

legacy behaviorを復活させる

semanticに誤ったprovenanceをtest-fittingする

old Family tableへfallbackさせる
```

---

# 24. Migration Audit

Expected Product migration head:

```text
20260809_product_0010
```

Phase Eでは原則:

```text
new migration = NONE
```

とする。

もしacceptance defect remediationでmigrationが必要になった場合のみ:

```text
revision
down_revision
reason
schema/domain/ORM consistency
```

を証拠化する。

old Family table dropはしない。

---

# 25. TD-001 Closure

TD-001:

```text
G02 -> G05
```

で残したcanonical Execution aggregate convergence debt。

Phase Eで正式にCLOSEする。

Closure evidence最低限:

```text
all family Product submissions
    -> canonical Execution

one canonical claim authority

all Product lifecycle mutations
    -> canonical Execution semantics

no FamilyExecution new-write authority
```

記録:

```text
TD-001: CLOSED at E4-G05 Phase E
Evidence: <tests/reports/commands>
```

---

# 26. TD-002 Closure

TD-002:

```text
G03 -> G05
```

で残したpersistent StageExecution convergence debt。

Phase Eで正式にCLOSEする。

Evidence:

```text
Causal / Exploratory / Predictive
    -> canonical persistent StageExecution

retry
    -> stable StageExecution identity

rerun/revise
    -> new Execution / new StageExecution set

GenericExecutor
    -> non-authoritative
```

記録:

```text
TD-002: CLOSED at E4-G05 Phase E
```

---

# 27. TD-003 Closure

TD-003:

```text
G04 -> G05
```

で残したResult / Artifact ownership convergence debt。

Phase Eで正式にCLOSEする。

Evidence:

```text
all new family Results
    -> canonical Result owner

all new family Artifacts
    -> canonical Artifact owner

no FamilyResult new-write authority

no FamilyArtifact new-write authority

ArtifactStore
    -> physical storage only
```

記録:

```text
TD-003: CLOSED at E4-G05 Phase E
```

---

# 28. TD-004 Handoff — Do NOT Close

TD-004:

```text
G05 -> G06
```

はPhase Eで正式handoffする。

Phase Eでは:

```text
TD-004 = OPEN
Exit Gate = G06
```

を明示する。

handoff内容:

```text
typed structural lineage authority

generic persisted lineage authority

closure/export projection

remaining typed/generic overlap classification
```

をinventoryする。

Phase EでG06 lineage final cutoverを実装しない。

記録:

```text
TD-004: OPEN
Owner / Exit Gate: E4-G06
```

---

# 29. Transition Debt Final State After G05 Implementation

Expected:

```text
TD-001 CLOSED
TD-002 CLOSED
TD-003 CLOSED
TD-004 OPEN  -> G06
TD-005 future
TD-006 future
```

G05 completion reportに明示する。

---

# 30. Fixed Final G05 Implementation SHA

Phase E acceptance test追加やproduction remediationが必要な場合、それらを完了してからfinal implementation commitを作成する。

Suggested commit:

```text
E4-G05 Trial 01 implementation complete
```

このcommitには:

```text
production fixes if any

final G05 acceptance/architecture regression tests

required test hardening
```

を含める。

report/documentation-only changeは含めないことを推奨する。

commit前:

```bash
git status --short
git diff --check
git diff --cached --name-status
```

commit後:

```bash
git rev-parse HEAD
```

このSHAを:

```text
Fixed Final G05 Implementation SHA
```

として固定する。

---

# 31. Fixed SHA Verification

重要:

**final implementation SHAを作った後、その固定SHAの状態でfinal acceptanceを再実行する。**

つまり順序は:

```text
implementation/test modifications complete

        ↓

final implementation commit

        ↓

fixed SHA

        ↓

standard PostgreSQL final verification

unit/boundary final verification

        ↓

all PASS

        ↓

reports
```

reportを書いた後のworking tree状態をテストしただけでは不足。

Independent Test Agentへ渡すfixed implementation SHAそのものを検証する。

---

# 32. Phase E Implementation Checkpoint Report

以下を作成する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G05/Trial01/
E4-G05_01_PhaseE_implementation_checkpoint_report.md
```

Phase Status:

```text
PHASE_E_COMPLETE
```

Gate status:

```text
READY_FOR_TEST
```

まだ:

```text
PASS
```

ではない。

---

# 33. Phase E Checkpoint Report Required Metadata

```text
# E4-G05 Trial 01 Phase E Implementation Checkpoint Report

- Project
- Enhancement
- Gate
- Trial
- Phase
- Phase Status
- Branch

- Phase baseline checkpoint
- Phase D final checkpoint
- Fixed Final G05 Implementation SHA
- Report commit

- Migration head

- Started at
- Finished at

- Gate READY_FOR_TEST
```

Phase baseline:

```text
d766b85a22eaff999c3981c7ceb5e675eb8803c7
```

値がないfieldを削除せず:

```text
N/A
NONE
NOT_RUN
UNKNOWN
```

を使う。

---

# 34. Phase E Checkpoint Report Required Sections

最低限:

```text
## 1. Input

## 2. Phase E Scope Summary

## 3. Final Golden Path Matrix
### Causal
### Exploratory
### Predictive

## 4. Final Product Authority Matrix

## 5. Old Family Runtime Negative Matrix

## 6. Canonical Failure No-Fallback Evidence

## 7. Lifecycle Mutation Final Evidence

## 8. CLI Classification

## 9. GenericExecutor Authority Audit

## 10. Passed Gate Regression
### G02
### G03
### G04

## 11. Earlier G05 Phase Regression
### Phase A
### Phase B
### Phase C
### Phase D

## 12. Transition Debt Closure
### TD-001 CLOSED
### TD-002 CLOSED
### TD-003 CLOSED
### TD-004 OPEN -> G06

## 13. Migration

## 14. Files Changed

## 15. Git Evidence

## 16. Exact Verification Evidence
- complete commands
- exit codes
- pass/fail/skip counts
- raw evidence paths
- tested SHA
- expected
- actual
- Facts
- Interpretation

## 17. Fixed Final G05 Implementation SHA

## 18. Independent Test Agent Handoff

## 19. Gate Status
READY_FOR_TEST

## 20. Design Block
```

---

# 35. G05 Implementation Completion Report

Phase E checkpointとは別にGate-level implementation completion reportを作成する。

Trial-first directory standardを使用する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G05/Trial01/
E4-G05_01_implementation_completion_report.md
```

repositoryの標準Implementation Completion Report template/specificationにfield-by-fieldで従う。

独自の簡略形式に置き換えない。

---

# 36. G05 Completion Report Mandatory Content

最低限以下を含む。

```text
Gate: E4-G05
Trial: 01

Implementation Status:
READY_FOR_TEST

Fixed Final Implementation SHA:
<full SHA>

Migration head:
20260809_product_0010

Phase checkpoints:
A
B
C
D
E

Final authority contract

Causal Golden Path evidence

Exploratory Golden Path evidence

Predictive Golden Path evidence

cross-family authority evidence

old-write shutdown evidence

mutation/read/CLI evidence

passed Gate regression evidence

TD-001 CLOSED
TD-002 CLOSED
TD-003 CLOSED
TD-004 OPEN -> G06

known limitations

explicit out-of-scope

Test Agent handoff
```

---

# 37. Test Agent Handoff Block

Completion reportに明示する。

```text
Independent Test Instruction:

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
10_enhance_instruction/G05/
07_Ariadne_ENH-E4_G05_テスト指示書.md
```

Test target:

```text
Fixed Final G05 Implementation SHA:
<full SHA>
```

Test Agentへ:

```text
branch HEADを漫然とtestする
```

のではなく、fixed implementation refをauditさせる。

report/documentation commitがその後に存在しても、implementation target SHAを曖昧にしない。

---

# 38. Report Commit Procedure

self-referenceを避ける。

Phase E checkpoint reportとG05 completion reportを作成し、最初は:

```text
Report commit: PENDING
```

とする。

両reportをinitial documentation commitへ入れてよい。

Suggested:

```text
E4-G05 Trial 01 Phase E and completion reports
```

取得:

```bash
git rev-parse HEAD
```

このinitial report commit SHAを各reportの:

```text
Report commit
```

へ設定する。

その後metadata correction commit:

```text
E4-G05 Trial 01 report metadata
```

を作成する。

Report commitは:

```text
そのreportを最初に導入したcommit
```

を意味する。

metadata correction commit自身を自己参照しない。

---

# 39. ENH-E4 Implementation Detail Report

repository標準workflow上:

```text
ENH-E4_implementation_report_detail.md
```

等のGate progress/detail report更新が要求されている場合は、actual template / existing G01〜G04/G05 practiceを確認し、Phase E completion時点まで更新する。

推測で新しいreport typeを作らない。

existing reportが存在し、G05 instruction/templateで更新対象なら更新する。

---

# 40. Report Format Compliance

すべてのreportで以下を守る。

```text
required sectionを削除しない

required fieldを統合しない

required fieldを自由作文に置換しない

値なし:
N/A
NONE
NOT_RUN
UNKNOWN
```

Evidence:

```text
exact copy-pastable commands

exit code

passed / failed / skipped

raw evidence

expected

actual

reproduction procedure

Facts

Interpretation
```

Substantive test success does not waive report-format compliance.

---

# 41. READY_FOR_TEST Criteria

以下をすべて満たした場合のみ:

```text
READY_FOR_TEST
```

を宣言する。

```text
[ ] Causal final Golden Path PASS

[ ] Exploratory final Golden Path PASS

[ ] Predictive final Golden Path PASS

[ ] cross-family authority audit PASS

[ ] FamilyExecution new Product writes = 0
[ ] FamilyStageExecution new Product writes = 0
[ ] FamilyResult new Product writes = 0
[ ] FamilyArtifact new Product writes = 0

[ ] canonical failure -> old fallback = NONE

[ ] retry semantics PASS
[ ] rerun semantics PASS
[ ] revise semantics PASS

[ ] historical compatibility bounded read-only

[ ] GenericExecutor non-authoritative

[ ] CLI classification complete

[ ] D1 regression PASS
[ ] D2 regression PASS
[ ] D3 regression PASS

[ ] Phase A regression PASS
[ ] Phase B regression PASS
[ ] Phase C regression PASS
[ ] Phase D regression PASS

[ ] G02 regression PASS
[ ] G03 regression PASS
[ ] G04 regression PASS

[ ] Product migration head verified

[ ] TD-001 CLOSED
[ ] TD-002 CLOSED
[ ] TD-003 CLOSED
[ ] TD-004 OPEN -> G06

[ ] fixed final implementation SHA created

[ ] fixed SHA itself fully verified

[ ] Phase E checkpoint report created

[ ] G05 implementation completion report created

[ ] report-format compliance confirmed

[ ] git diff --check PASS
```

---

# 42. Phase E Completion State

Phase E完了時:

```text
Phase A COMPLETE
Phase B COMPLETE
Phase C COMPLETE
Phase D COMPLETE
Phase E COMPLETE

TD-001 CLOSED
TD-002 CLOSED
TD-003 CLOSED
TD-004 OPEN -> G06

G05 Implementation:
COMPLETE

G05:
READY_FOR_TEST

G05 Gate Decision:
NOT YET DECIDED
```

---

# 43. Do Not Declare G05 PASS

Coding Agentは以下を宣言してはならない。

```text
G05 PASS
Gate Decision PASS
Trial 01 PASS
```

宣言できるのは:

```text
PHASE_E_COMPLETE
READY_FOR_TEST
```

まで。

Independent Test AgentによるTest Item 999のみがGate decisionを行う。

---

# 44. Do Not Enter G06

Phase E完了後、このrunでG06へ進まない。

G06で扱う:

```text
typed structural lineage authority

generic persisted lineage authority

closure/export projection

TD-004 closure

TD-005 establishment
```

をPhase Eで実装しない。

---

# 45. Do Not Enter G07 / G08

Phase Eで以下を先取りしない。

```text
old Family table drop

broad legacy source deletion

legacy migration chain retirement

CLI final retirement/reorganization

clean bootstrap final architecture audit
```

これらはG07 / G08。

---

# 46. Current Architecture Control Sheet

Phase E / READY_FOR_TEST時点ではCoding Agentが:

```text
00_ENH-E4_Current_Architecture_Control_Sheet.md
```

を更新しない。

Current Architecture Control Sheet更新は:

```text
Independent Test Agent G05 PASS
    ↓
operator update
```

の順。

---

# 47. Phase E Stop Reasons NOT Accepted

以下を途中停止理由として認めない。

```text
Golden Pathの1つがFAILした

Family row-count negativeで差分が出た

canonical failure fallbackを発見した

regressionがFAILした

TD closure evidence整理が必要

reportが未作成

report format確認が必要

fixed implementation SHAの再testが必要

completion reportが未作成

Test Agentがまだ実行されていない
```

Phase E scopeのproduction defectは修正し、acceptanceをPASSまで回す。

Test Agent未実行は正常である。

Phase Eの目的はTest Agentへ渡せる状態を作ること。

---

# 48. DESIGN_BLOCKED Condition

`DESIGN_BLOCKED` を許可するのは、

```text
approved G02 / G03 / G04 / G05 architecture

と

required Product scientific/business semantics
```

の間に、既存contractを破壊せずには解消できないsemantic contradictionが発見された場合のみ。

以下はDESIGN_BLOCKEDではない。

```text
test failure

fixture issue

report作業

legacy reference発見

production bug

test追加が必要

TD evidence整理

CLI classification作業
```

---

# 49. Final Stop Condition

このrunの正しい終了条件は:

```text
PHASE_E_COMPLETE
READY_FOR_TEST
```

である。

最後に必ず以下を出力する。

```text
PHASE_E_COMPLETE

Gate: E4-G05
Trial: 01

Fixed Final G05 Implementation SHA:
<full SHA>

Phase E Report Commit:
<full SHA>

G05 Completion Report Commit:
<full SHA or same initial report commit>

Phase E Report:
docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G05/Trial01/E4-G05_01_PhaseE_implementation_checkpoint_report.md

G05 Completion Report:
docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G05/Trial01/E4-G05_01_implementation_completion_report.md

TD-001: CLOSED
TD-002: CLOSED
TD-003: CLOSED
TD-004: OPEN -> E4-G06

Causal Golden Path: PASS
Exploratory Golden Path: PASS
Predictive Golden Path: PASS

Old Family new-write authority: NONE

Canonical failure -> legacy fallback: NONE

Migration head:
20260809_product_0010

Gate status:
READY_FOR_TEST

Independent Test Agent:
NEXT

G05 PASS:
NOT YET DECIDED
```

を報告して停止する。

Independent Test Agentの実行へ勝手に進まないこと。
