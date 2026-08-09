# E4-G05 Trial 01 — Phase D D3 Global Authority Audit / Phase D Completion Instruction

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Branch: `refactor/ariadne_mvp_e4`
- Gate: `E4-G05`
- Gate name: Product Execution Convergence
- Trial: `01`
- Phase: `D`
- Work package: `D3`
- Work package name: Global authority reachability / no-fallback / runtime negative audit
- D1 status: `PHASE_D_D1_COMPLETE`
- D1 checkpoint: `e831e3f78d4791a2d4a0ef96f6ce80058c376fae`
- D2 status: `PHASE_D_D2_COMPLETE`
- D2 checkpoint: `ce3a9afd303d408d3b9b36fbb7a91349dbabe514`
- Previous Phase C final implementation checkpoint: `9c58bffd5c5fb6be8565a1256222e678fb86c52a`
- Expected Product migration head: `20260809_product_0010`
- Gate READY_FOR_TEST: `NO`

---

# 1. Purpose

E4-G05 Trial 01 Phase Dを継続する。

D1 / D2で以下を成立させた。

```text
D1:
family-specific old claim/process authority
    -> EXPLICIT_REJECT / NOT_PRESENT

Product worker claim
    -> canonical uow.executions.claim_next only

canonical claim/process failure
    -> old Family authority fallbackなし

D2:
Product mutation requires canonical dependency

legacy submit/mutation branch
    -> canonical delegation or EXPLICIT_REJECT

historical compatibility
    -> bounded read-only only

canonical lookup miss
    -> Family authority fallbackなし

Product lifecycle operation
    -> Family 4-table new writeなし
```

D3の目的は、これらを**局所的なmethod-level修正ではなく、G05 Product architecture全体のauthority invariantとして証明し、Phase Dを閉じること**である。

Phase D completion question:

> Causal / Exploratory / Predictive のnew Product flowについて、submit / claim / process / mutation / Result / Artifact / failure handlingのどこからもold Family authorityへ到達できないことを、static reachabilityとreal PostgreSQL runtime evidenceの両方で証明できるか。

D3完了時のexit condition:

```text
PHASE_D_COMPLETE
```

Phase Eには進まない。

---

# 2. Source of Truth

最低限以下を参照する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
10_enhance_instruction/G05/
06_Ariadne_ENH-E4_G05_実装指示書.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
10_enhance_instruction/G05/
06j01_Ariadne_ENH-E4_G05_PhaseD_実装指示書.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
10_enhance_instruction/G05/
06j02_Ariadne_ENH-E4_G05_PhaseD_D2_実装指示書.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G05/Trial01/
E4-G05_01_PhaseD__in_progress_06j01.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G05/Trial01/
E4-G05_01_PhaseD__in_progress_06j02.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G05/Trial01/
E4-G05_01_PhaseC_implementation_checkpoint_report.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
00_ENH-E4_Current_Architecture_Control_Sheet.md
```

G02/G03/G04 passed contractを変更しない。

Current Architecture Control SheetはG05 PASS前なのでCoding Agentが更新しない。

---

# 3. Phase D Final Boundary

Phase D終了時に許容される状態:

```text
old source may exist

old Family tables may exist

historical explicit read-only compatibility may exist

science-only helper/source may exist
```

しかし以下は禁止。

```text
new Product submit
    -> FamilyExecution write

new Product claim
    -> family-specific FamilyExecution SELECT FOR UPDATE

new Product process
    -> FamilyStage/Result/Artifact persistence

new Product cancel/retry/rerun/revise
    -> Family lifecycle mutation

canonical lookup miss
    -> old Family lookup fallback

canonical failure
    -> old Family authority fallback

auditable Product CLI
    -> hidden old Product lifecycle

GenericExecutor
    -> lifecycle/persistence authority
```

Phase Dはsource deletion Gateではない。

old source/tableのretirementはG07。

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
  ce3a9afd303d408d3b9b36fbb7a91349dbabe514 HEAD
echo $?
```

Expected:

```text
branch = refactor/ariadne_mvp_e4
D2 checkpoint is ancestor
```

既存documentation/unrelated working-tree changes:

```text
discardしない
上書きしない
D3 production checkpointへ不用意に混入しない
```

path-specific stagingを使用する。

actual D3 starting commitをPhase D final reportへ記録する。

---

# 5. D3 Execution Strategy

D3はPhase D final auditである。

以下の順序で実施する。

```text
Step 1  All-family static authority inventory
Step 2  CLI / composition reachability inventory
Step 3  Runtime old-table trap matrix
Step 4  Controlled failure no-fallback matrix
Step 5  GenericExecutor / worker authority negative
Step 6  Phase D + Phase A/B/C + G02/G03/G04 regression
Step 7  Phase D final implementation checkpoint commit
Step 8  Phase D implementation checkpoint report
Step 9  report initial commit / metadata
Step 10 PHASE_D_COMPLETE
```

correct testによるproduction defectを発見した場合はD3 scope内で修正し、再検証する。

途中で単なるinventory resultだけを報告して停止しない。

---

# 6. All-Family Product Authority Matrix — Mandatory

Causal / Exploratory / Predictiveについてactual Product surfaceを再inventoryする。

最低限:

```text
submit
Execution read/list
StageExecution read/list
Result read/list
Artifact read/list
claim
process
cancel
retry
rerun
revise
prefill where present
lineage projection where present
```

各surfaceについて以下を記録する。

```text
family
surface
Product entry point
application/service method
authority repository/service
Family ORM reference?
Family write reachable?
silent fallback?
D1/D2 disposition
D3 final judgment
```

final expected authority matrix:

| Authority | CAUSAL | EXPLORATORY | PREDICTIVE |
|---|---|---|---|
| Execution repository | canonical | canonical | canonical |
| claim / lease | canonical | canonical | canonical |
| StageExecution | canonical | canonical | canonical |
| Result owner | canonical | canonical | canonical |
| Artifact owner | canonical | canonical | canonical |
| lifecycle mutation | canonical | canonical | canonical |
| GenericExecutor authority | NO | NO | NO |
| Family new-write authority | NO | NO | NO |

存在しないfamily surfaceを捏造しない。

```text
NOT_EXPOSED
```

等で明示する。

---

# 7. Static Reachability Audit

最低限以下をsource/searchする。

```text
FamilyExecutionOrm(
FamilyStageExecutionOrm(
FamilyResultOrm(
FamilyArtifactOrm(

session.add(
session.delete(

claim_next(
process_execution(

with_for_update
skip_locked

LegacyProductAuthorityDisabled

ExecutionService(
uow.executions.claim_next

GenericExecutor

get_exploratory_workspace_service
get_predictive_workflow_service

CLI / Typer / argparse / click entry points
```

対象directory:

```text
src/ariadne/interfaces/web_api/
src/ariadne/interfaces/worker/
src/ariadne/interfaces/cli/
src/ariadne/product/application/
src/ariadne/product/persistence/
```

static resultを以下へ分類する。

```text
CANONICAL_PRODUCT
EXPLICIT_REJECT
BOUNDED_HISTORICAL_READ_ONLY
SCIENCE_ONLY
G07_RETIREMENT_CANDIDATE
NOT_PRODUCT_REACHABLE
```

単なるlegacy symbol存在をFAILにしない。

primary question:

```text
new Product route/compositionから
old write/claim authorityへcall graphが存在するか
```

である。

---

# 8. Explicit Product Reachability Graph

Phase D final reportへProduct composition graphを記録する。

最低限:

```text
FastAPI/Product route
    -> dependency/provider
    -> family adapter/service
    -> canonical ExecutionService / UoW
```

worker:

```text
run_worker
    -> SqlUnitOfWork
    -> uow.executions.claim_next
    -> ExecutionProcessor
    -> family dispatch
    -> canonical Result/Artifact persistence
```

CLIが存在する場合は別途記載する。

禁止経路:

```text
Product route
    -> FamilyExecution direct write

worker
    -> family claim_next

canonical failure
    -> old process_execution
```

がないことを明示する。

---

# 9. CLI Boundary Inventory — Mandatory

actual CLI sourceをinventoryする。

存在するCLIを以下へ分類する。

```text
LOW_LEVEL_SCIENTIFIC
AUDITABLE_PRODUCT
NOT_APPLICABLE
```

## LOW_LEVEL_SCIENTIFIC

許容:

```text
local/input-output utility
Product DB persistenceを約束しない
Product Execution auditabilityを約束しない
```

canonical Product lifecycleへ無理に統合しない。

## AUDITABLE_PRODUCT

user-visible Product analysis / Product DB persistence / auditabilityを提供するCLIが存在する場合:

```text
canonical Execution serviceへsubmit
```

すること。

hidden Family lifecycleを作ってはならない。

## Scope limit

Phase Dでは:

```text
classification
reachability
old-authority negative
```

まで。

CLI source retirement/final reorganizationはG07。

存在しないAUDITABLE_PRODUCT CLIを新設しない。

---

# 10. Runtime Old-Family Trap Matrix — Mandatory

D3で最重要のreal PostgreSQL negative evidenceを作る。

旧Family table:

```text
FamilyExecutionOrm
FamilyStageExecutionOrm
FamilyResultOrm
FamilyArtifactOrm
```

について、trap rowsまたはbaseline countsを用意する。

### Required concept

```text
old Family counts BEFORE
        ↓
new Product operations
        ↓
old Family counts AFTER
```

Expected:

```text
AFTER == BEFORE
```

new Product operationによるFamily row:

```text
INSERT = 0
UPDATE = 0
DELETE = 0
```

を証明する。

---

# 11. Runtime Matrix — Causal

actual Causal Product Golden Pathを使う。

最低限:

```text
Product submit
canonical Execution
persistent StageExecution
canonical claim/process
canonical Result/Artifact
terminal Execution
```

Must assert:

```text
FamilyExecution count unchanged
FamilyStageExecution count unchanged
FamilyResult count unchanged
FamilyArtifact count unchanged
```

CausalでFamily tableを使用していない場合でも、全4表のbefore/afterをcross-family trapとして確認してよい。

test fixtureのためにold rowをseedする場合、そのseedをProduct behavior evidenceと混同しない。

---

# 12. Runtime Matrix — Exploratory

actual Exploratory Product pathについて最低限:

```text
submit
canonical read/result projection
downstream draft if relevant
canonical worker execution if supported in current Golden Path
```

および実在するlifecycle mutationを対象にする。

D2でrejectされたold direct methodを別途呼び:

```text
explicit reject
Family counts unchanged
```

も確認する。

---

# 13. Runtime Matrix — Predictive

Phase Cで成立したsurfaceを使用する。

最低限:

```text
submit
worker Golden Path
cancel where practical
retry
rerun
revise
read/result/artifact/prefill
```

すべてを1つの巨大scenarioへ無理に詰め込む必要はない。

複数testに分けてもよい。

ただしPhase D final reportではoperation matrixとして:

```text
operation
canonical effect
Family 4-table before
Family 4-table after
PASS/FAIL
```

を統合して示す。

---

# 14. Old Method Direct Behavior Matrix

sourceに残るold Product mutating facadeをinventoryし:

```text
Exploratory claim/process
Predictive claim/process
legacy submit
legacy cancel/retry/rerun/revise
PredictiveSplit legacy validation/write
その他actual D2 inventoryで見つかったもの
```

直接呼出しtest結果をまとめる。

Expected disposition:

```text
EXPLICIT_REJECT
or
DELEGATE_CANONICAL
or
NOT_PRESENT
```

禁止:

```text
DIRECT_FAMILY_MUTATION
```

D1/D2 testを再利用してよい。

---

# 15. Controlled Failure No-Fallback Matrix

positive Golden PathだけではPhase Dを完了しない。

canonical pathへcontrolled failureを注入する。

最低限、以下のcategoryをcoverする。

```text
A. canonical submit/domain failure
B. canonical claim/process failure
C. canonical lifecycle mutation failure or canonical lookup miss
```

familyごとに全部繰り返す必要はないが、

```text
all three failure categories
+
multiple family coverage
```

を満たすよう設計する。

Expected:

```text
canonical error
    -> canonical failure/domain error
    -> stop
```

Forbidden:

```text
canonical error
    -> Family submit
    -> Family claim
    -> Family process
    -> Family mutation
```

各failure testでFamily table counts unchangedを可能な範囲で直接確認する。

---

# 16. Canonical Lookup Miss Negative

最低限:

```text
unknown canonical execution_id
wrong project
wrong family
unknown canonical Result if exposed
```

について:

```text
EntityNotFound / domain rejection
```

で終了すること。

禁止:

```text
FamilyExecution lookup
FamilyResult lookup
FamilyArtifact lookup
```

へのsilent fallback。

historical bounded adapterは明示的に別surfaceであること。

---

# 17. Historical Compatibility Final Classification

D2で残したhistorical compatibilityをfinal inventoryする。

少なくとも現在把握済みの:

```text
PredictiveSplitService.get_partition_artifact
    -> bounded FamilyArtifact historical read-only
```

について:

```text
read-only
explicit
canonical miss fallbackではない
mutationへ接続しない
```

ことを再確認する。

その他historical compatibilityを発見した場合も同様に分類。

Phase D final reportには:

```text
file/function
historical entity
reason retained
read/write
Product canonical fallback?
G07 retirement candidate?
```

を記録する。

---

# 18. GenericExecutor Final Negative

G03/G04 contractを再確認する。

GenericExecutorは:

```text
plan/order
binding
runner invocation
runner outcome
```

まで。

以下のauthorityを持たない。

```text
Execution identity
claim/lease
persistent StageExecution ownership
retry lifecycle
Result persistence ownership
Artifact persistence ownership
```

static + automated regressionで証明する。

D3修正のためにGenericExecutorへauthorityを移してはいけない。

---

# 19. Canonical Worker Sole Authority Final Check

worker compositionで以下を確認する。

```text
one worker claim authority
    = uow.executions.claim_next

family selection
    = claimed Execution.analysis_family after claim
```

禁止:

```text
family-specific worker queue
family-specific claim fallback
legacy process fallback
```

D1 testをPhase D final bundleで再実行する。

---

# 20. Phase D Dedicated D3 Test

推奨:

```text
tests/product/
test_enh_e4_g05_phase_d_d3_global_authority_audit.py

tests/product/
test_enh_e4_g05_phase_d_d3_global_authority_audit_postgres.py
```

actual split/namingはrepository規約へ合わせてよい。

D3専用testは既存D1/D2/C1-C4 testを重複実装するのではなく、以下のcross-cutting invariantへ集中する。

```text
all-family authority matrix
old-table row-count global negative
failure no-fallback
CLI classification/reachability
historical adapter separation
GenericExecutor non-authority
```

---

# 21. Static Architecture Test — Recommended

fragile grepだけに依存してはならないが、architecture regressionを検出するためのstatic/boundary testを追加してよい。

例:

```text
worker runnerがfamily service .claim_next()を呼ばない

Product DI providerがcanonical ExecutionServiceを注入

known legacy mutating public methods are reject/delegate

auditable Product CLIがFamily ORM mutationをimport/useしない
```

AST/import/source contract等、repositoryに合う方式を選ぶ。

runtime behavior evidenceを必ず併用する。

---

# 22. Phase D Regression Bundle

D3完了前にD1/D2 testをまとめて再実行する。

最低限:

```text
D1 claim/process shutdown

D2 lifecycle/write shutdown

D3 global authority audit
```

actual test pathsを使用する。

---

# 23. Phase C Regression Bundle

最低限:

```text
Predictive C1 Golden Path
Predictive C2 retry
Predictive C3a rerun
Predictive C3b revise
Predictive C4 authority audit

Exploratory Phase B canonical projection
```

を回帰する。

Phase C final reportで成立したauthorityをD3で弱めない。

---

# 24. Phase A Regression

typed Result / Artifact canonical semanticsを維持する。

最低限:

```text
family Result type/status
schema version
Result ↔ Artifact association
repository/PostgreSQL round-trip
```

を関連testで確認する。

---

# 25. G02 / G03 / G04 Regression

Mandatory:

## G02

```text
canonical Execution identity
claim/lease
cancel/retry/rerun/revise lifecycle
```

## G03

```text
persistent StageExecution
stable StageExecution retry identity
attempt history
GenericExecutor negative
```

## G04

```text
canonical Result/Artifact ownership
Artifact physical-store boundary
typed reuse
compensation/reconciliation relevant tests
```

D3はG05 authority auditなので、passed Gate assertionを弱めない。

---

# 26. PostgreSQL Contract Regression

Product PostgreSQL contract testをactual repositoryから特定し実行する。

migration head:

```text
20260809_product_0010
```

を確認する。

D3のためだけにmigrationを追加しない。

---

# 27. Standard PostgreSQL Verification

real PostgreSQL verification entryは唯一:

```bash
scripts/test/run_product_postgres_tests.sh <pytest-path-or-node> [...]
```

を使用する。

D3 final evidenceでは可能な範囲で関連testを1つのbundle commandへまとめる。

ただしG03 fixture等がclean/global-empty DB assumptionを持ち、同一bundleでfalse failureを起こすことが既知の場合:

```text
semanticに必要なisolated standardized runner invocation
```

へ分けてよい。

その場合reportへ:

```text
why separated
exact command
exit code
evidence
```

を記録する。

manual:

```text
docker run
manual DSN
manual psql
manual Alembic
ad-hoc external PostgreSQL pytest
```

は禁止。

---

# 28. Mandatory Runtime Evidence Format

各重要verificationについて以下を残す。

```text
exact copy-pastable command
test target
exit code
passed
failed
skipped
raw evidence path
tested SHA/state
expected
actual
Facts
Interpretation
```

`tests passed` のみでは不足。

`same as previous` 等でcommandを省略しない。

---

# 29. Non-PostgreSQL Regression

以下のboundary/unitを必要範囲で実行する。

```text
D1/D2 explicit reject
FastAPI dependency construction
Product route composition
CLI classification/static boundary
GenericExecutor boundary
worker dispatch
ExecutionService lifecycle
```

exact command / exit code / pass countを記録する。

---

# 30. D3 Defect Handling

D3 testでproduction defectを発見した場合:

```text
Phase D scopeのauthority defect
    -> production fix
    -> test rerun
    -> PASS
```

まで行う。

以下は途中停止理由にならない。

```text
static auditでlegacy pathを発見した
runtime negativeがFAILした
CLI classificationが必要
historical adapterが追加で見つかった
failure injectionがold fallbackを検出した
regressionがFAILした
```

DESIGN_BLOCKEDはapproved architectureでは解決不能なsemantic contradictionのみ。

---

# 31. Phase D Completion Criteria

以下をすべてDONEにする。

```text
[ ] Causal Product authority matrix complete
[ ] Exploratory Product authority matrix complete
[ ] Predictive Product authority matrix complete

[ ] static route/service/worker reachability audit complete

[ ] all Product claim authority = canonical
[ ] family dispatch occurs after canonical claim
[ ] no family-specific Product claimer reachable

[ ] all new Product Execution writes canonical
[ ] all new Product StageExecution writes canonical
[ ] all new Product Result writes canonical
[ ] all new Product Artifact writes canonical

[ ] Product mutation surfaces canonical or explicit reject
[ ] retained old mutating methods canonical delegate or explicit reject

[ ] canonical lookup miss has no old Family fallback
[ ] canonical submit failure has no old fallback
[ ] canonical claim/process failure has no old fallback
[ ] canonical lifecycle failure has no old fallback

[ ] Causal runtime old Family row-count negative PASS
[ ] Exploratory runtime old Family row-count negative PASS
[ ] Predictive runtime old Family row-count negative PASS

[ ] old Family 4-table INSERT/UPDATE/DELETE from new Product path = NONE

[ ] historical compatibility final classification complete
[ ] historical compatibility remains bounded read-only
[ ] historical read cannot become mutation authority

[ ] CLI inventory complete
[ ] LOW_LEVEL_SCIENTIFIC CLI remains outside Product lifecycle where applicable
[ ] AUDITABLE_PRODUCT CLI, if present, uses canonical lifecycle
[ ] no CLI hidden old Product lifecycle

[ ] GenericExecutor remains non-authoritative

[ ] D1 regression PASS
[ ] D2 regression PASS
[ ] D3 dedicated tests PASS

[ ] Phase A regression PASS
[ ] Phase B regression PASS
[ ] Phase C regression PASS

[ ] relevant G02 regression PASS
[ ] relevant G03 regression PASS
[ ] relevant G04 regression PASS
[ ] PostgreSQL contract PASS

[ ] Product migration head verified
[ ] git diff --check PASS

[ ] Phase D final implementation checkpoint commit created
[ ] Phase D implementation checkpoint report created
[ ] report initial commit SHA recorded
```

---

# 32. Phase D Final Implementation Checkpoint Commit

全production/test criteria PASS後、Phase D final implementation checkpoint commitを作成する。

Suggested commit message:

```text
E4-G05 Trial 01 Phase D complete
```

含める:

```text
D3 production corrections if any
D3 automated tests
Phase D final authority audit code/test
```

含めない:

```text
unrelated documentation
Current Architecture Control Sheet update
Phase E work
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

を記録する。

このfull SHAを:

```text
Phase D final implementation checkpoint
```

としてreportへ固定する。

---

# 33. Phase D Implementation Checkpoint Report

D3 execution resultをinstruction fileへ追記しない。

以下を作成する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G05/Trial01/
E4-G05_01_PhaseD_implementation_checkpoint_report.md
```

これはPhase D final checkpoint reportである。

まだGate-level:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G05/
E4-G05_01_implementation_completion_report.md
```

ではない。

Gate-level completion reportはPhase Eで作成する。

---

# 34. Phase D Report Required Metadata

以下を省略しない。

```text
# E4-G05 Trial 01 Phase D Implementation Checkpoint Report

- Project
- Enhancement
- Gate
- Trial
- Phase
- Phase Status: PHASE_D_COMPLETE | DESIGN_BLOCKED
- Branch
- Phase baseline checkpoint
- D1 checkpoint
- D2 checkpoint
- Phase D final implementation checkpoint
- Report commit
- Migration head
- Started at
- Finished at
```

推奨baseline:

```text
Phase baseline checkpoint:
9c58bffd5c5fb6be8565a1256222e678fb86c52a
```

これはPhase C final implementation checkpoint。

値がないfieldを削除しない。

```text
N/A
NONE
NOT_RUN
UNKNOWN
```

を使う。

---

# 35. Phase D Report Required Sections

最低限以下。

```text
## 1. Input

## 2. Phase D Scope Summary

## 3. Internal Checkpoint Ledger
### D1
### D2
### D3

## 4. Final Product Authority Matrix
### Causal
### Exploratory
### Predictive

## 5. Product Reachability Graph
### API / service
### Worker
### CLI

## 6. Files Changed
### Added
### Modified
### Deleted

## 7. Implementation Details

## 8. Automated Test Code Added / Changed

## 9. Old Family Runtime Negative Evidence
### Causal
### Exploratory
### Predictive
### Family 4-table before/after matrix

## 10. Failure No-Fallback Evidence
### submit
### claim/process
### lifecycle mutation / lookup miss

## 11. Retained Legacy Source Classification
### Explicit reject
### Bounded historical read-only
### Science-only
### G07 retirement candidate

## 12. GenericExecutor Authority Audit

## 13. CLI Classification Matrix
- path / command
- classification
- Product persistence?
- canonical lifecycle?
- old authority reachable?
- G07 action

## 14. Migration

## 15. Passed-Gate / Earlier-Phase Regression
### G02
### G03
### G04
### Phase A
### Phase B
### Phase C
### D1
### D2

## 16. Known Limitations / Remaining G05 Work

## 17. Explicit Out-of-Scope Work

## 18. Git Evidence

## 19. Phase Verification Evidence
- exact commands
- exit codes
- pass/fail/skip counts
- raw evidence paths
- tested SHA/state
- expected/actual
- Facts
- Interpretation

## 20. Next-Phase Handoff
- Next phase: Phase E
- Ready for Phase E: YES / NO
- Gate READY_FOR_TEST: NO

## 21. Design Block
```

Substantive test success does not waive report-format compliance.

---

# 36. Report Commit Procedure

self-referential SHA問題を避ける。

1. Phase D final implementation checkpoint commitを作成。
2. reportを作成。
3. 初期値:

```text
Report commit: PENDING
```

4. report initial commit:

Suggested:

```text
E4-G05 Trial 01 Phase D checkpoint report
```

5. SHA取得:

```bash
git rev-parse HEAD
```

6. `Report commit: PENDING` を**initial report commit SHA**へ置換。
7. metadata correction commit:

Suggested:

```text
E4-G05 Trial 01 Phase D report metadata
```

Report commit fieldは:

```text
reportを最初にrepositoryへ導入したcommit
```

を意味する。

metadata correction commit自身を自己参照しない。

---

# 37. Phase D Does NOT Close Transition Debts Yet

D3ではTD-001/TD-002/TD-003の**closure evidence素材**を揃えてよい。

しかし正式closure declarationはPhase E。

Phase D reportには:

```text
TD-001 evidence ready: YES/NO
TD-002 evidence ready: YES/NO
TD-003 evidence ready: YES/NO
```

を補足してよい。

Phase Dで:

```text
TD-001 CLOSED
TD-002 CLOSED
TD-003 CLOSED
```

を最終宣言しない。

---

# 38. TD-004 / Lineage Boundary

G05ではG06 lineage consolidationを先取りしない。

D3でlineage sourceをinventoryする際も:

```text
structural generic duplicate writes
typed/generic authority
closure/export projection
```

のfinal cutoverは行わない。

Phase D reportで必要なら:

```text
remaining lineage-related authority debt
exit Gate = G06
```

として記録する。

TD-004の正式handoff整理はPhase E。

---

# 39. D3 Migration Policy

expected Product head:

```text
20260809_product_0010
```

D3はaudit/shutdown completionなので:

```text
new migration = NOT REQUIRED by default
```

禁止:

```text
Family table drop
legacy schema cleanup
historical application data migration
root migration rewrite
```

schema changeが必要なproduction defectを発見した場合は、まずPhase D authority contract上本当に必要か証明する。

---

# 40. Forbidden Scope Crossing

D3で禁止。

```text
old Family tables drop

broad legacy source deletion

ariadne.legacy retirement

root legacy migration rewrite

historical data rewrite

G06 lineage final authority cutover

G07 legacy/CLI final source retirement

G08 clean bootstrap final audit

TD-001/002/003 final closure

G05 final implementation completion report

READY_FOR_TEST

Current Architecture Control Sheet update
```

---

# 41. Phase D Final Stop Condition

今回停止してよいのは以下のみ。

```text
PHASE_D_COMPLETE
```

以下を全て満たす。

```text
D3 completion criteria all DONE

all-family static authority audit complete

all-family real PostgreSQL old-write negative PASS

controlled failure no-fallback PASS

CLI boundary inventory complete

GenericExecutor non-authority PASS

D1/D2 regression PASS

Phase A/B/C regression PASS

G02/G03/G04 regression PASS

Product PostgreSQL contract PASS

git diff --check PASS

Phase D final implementation checkpoint created

Phase D checkpoint report created

report initial commit SHA recorded
```

最後に必ず:

```text
PHASE_D_COMPLETE

Implementation Checkpoint SHA: <full SHA>

Report Commit SHA: <full SHA>

Report:
docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G05/Trial01/E4-G05_01_PhaseD_implementation_checkpoint_report.md

Causal old Family authority reachable: NO
Exploratory old Family authority reachable: NO
Predictive old Family authority reachable: NO

Canonical failure -> old fallback: NONE

Old Family runtime new-write:
FamilyExecution: 0
FamilyStageExecution: 0
FamilyResult: 0
FamilyArtifact: 0

GenericExecutor authority: NO

CLI boundary: CLASSIFIED

Next Phase: E
Gate READY_FOR_TEST: NO
```

を報告して停止する。

---

# 42. Stop Reasons NOT Accepted

以下を途中停止理由として認めない。

```text
static auditでlegacy referenceを発見した

runtime old-table negativeがFAILした

failure injectionでfallbackを発見した

CLI分類が必要

historical adapterが追加で見つかった

GenericExecutor boundary testが必要

regressionがFAILした

report作成が残っている

report metadata correctionが残っている

Phase Eがまだ残っている

G05全体が未完了
```

これらはD3内で解決・証拠化する対象である。

DESIGN_BLOCKEDは:

```text
approved G02/G03/G04/G05 architecture
vs
actual required Product semantics
```

の間に、canonical delegation / explicit reject / bounded read-only / science-only separationでは解消不能なsemantic contradictionがある場合のみ。

単なるlegacy code量、test failure、fixture問題、report作業はDESIGN_BLOCKEDではない。

---

# 43. Phase E Preview — Do NOT Execute

Phase D完了後のPhase Eでは以下を扱う予定。

```text
Causal / Exploratory / Predictive final Golden Paths

G05 acceptance matrix final verification

TD-001 closure
TD-002 closure
TD-003 closure

TD-004 OPEN / G06 handoff inventory

route-to-authority final before/after matrix

CLI classification final G05 evidence

Phase A/B/C/D evidence aggregation

G02/G03/G04 final regression

fixed final G05 implementation SHA

E4-G05_01_implementation_completion_report.md

ENH-E4_implementation_report_detail.md update

READY_FOR_TEST
```

D3 runではPhase Eへ進まない。

---

# 44. Final Instruction

E4-G05 Trial 01 Phase D D3 —

```text
Global authority reachability
+
failure no-fallback
+
old Family runtime negative
+
Phase D final regression/report
```

を完遂し、

```text
PHASE_D_COMPLETE
```

まで到達せよ。

Phase D完了後、このrunではPhase Eへ進まないこと。
