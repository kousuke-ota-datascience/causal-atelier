# E4-G05 Trial 01 — Phase D D2 Legacy Lifecycle / Write Branch Shutdown Implementation Instruction

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Branch: `refactor/ariadne_mvp_e4`
- Gate: `E4-G05`
- Gate name: Product Execution Convergence
- Trial: `01`
- Phase: `D`
- Work package: `D2`
- Work package name: Legacy lifecycle/write branch shutdown + bounded historical read compatibility
- Previous work package: `D1 — PHASE_D_D1_COMPLETE`
- D1 checkpoint: `e831e3f78d4791a2d4a0ef96f6ce80058c376fae`
- Previous Phase C final implementation checkpoint: `9c58bffd5c5fb6be8565a1256222e678fb86c52a`
- Expected Product migration head: `20260809_product_0010`
- Gate READY_FOR_TEST: `NO`

---

# 1. Purpose

E4-G05 Trial 01 Phase Dを継続する。

D1では以下を完了した。

```text
Product worker claim authority
    = canonical uow.executions.claim_next only

Exploratory old claim/process
    = EXPLICIT_REJECT

Predictive old claim/process
    = EXPLICIT_REJECT

Causal family-specific old claim/process
    = NOT_FOUND

canonical failure -> old claim/process fallback
    = NONE
```

D2の目的は、claim/process以外に残るlegacy Product lifecycle/write branchについて、

> **canonical dependencyやProduct compositionの状態に関係なく、新Product mutationからold Family authorityを再活性化できない状態へ固定すること**

である。

対象は主に:

```text
submit
cancel
retry
rerun
revise
Result/Artifact mutating helper
Product service construction / DI
historical legacy read compatibility
```

D2ではlegacy source/tableの削除は行わない。

---

# 2. This Run Scope

このrunでは **D2のみ** を実行する。

Exit condition:

```text
PHASE_D_D2_COMPLETE
```

D3へ進まない。

Phase D全体の:

```text
PHASE_D_COMPLETE
```

ではない。

---

# 3. Source of Truth

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
20_implementation_reports/G05/Trial01/
E4-G05_01_PhaseD__in_progress_06j01.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G05/Trial01/
E4-G05_01_PhaseC_implementation_checkpoint_report.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
00_ENH-E4_Current_Architecture_Control_Sheet.md
```

Current Architecture Control SheetはG05 PASS前なのでCoding Agentが更新しない。

---

# 4. D1 Established State — Preserve

D1 checkpoint:

```text
e831e3f78d4791a2d4a0ef96f6ce80058c376fae
```

で成立した以下を壊さない。

```text
canonical worker sole claim authority

family dispatch after canonical claim

Exploratory claim_next/process_execution explicit reject

Predictive claim_next/process_execution explicit reject

canonical processing failure has no old fallback

GenericExecutor non-authoritative
```

D2でlegacy lifecycle branchを整理するためにD1 rejectを復活させたり、old claimerをdelegate先として利用したりしてはならない。

---

# 5. D2 Primary Architecture Question

D2 completion時、以下の質問への回答がすべて `NO` でなければならない。

```text
Q1:
Exploratory/Predictive Product serviceをcanonical dependencyなしでconstructすると、
old Family submit authorityが復活するか？

Q2:
Product-facing cancel/retry/rerun/reviseを直接呼ぶことで、
FamilyExecution/FamilyStageExecutionをmutationできるか？

Q3:
retry等からFamilyResult/FamilyArtifactをdelete/resetできるか？

Q4:
canonical lookup miss時にold Family lifecycleへsilent fallbackできるか？

Q5:
historical legacy rowを読むためのcompatibility pathが、
new Product mutation authorityとしても使えるか？

Q6:
FastAPI/worker/auditable Product compositionから、
canonical dependencyを外したlegacy mutation serviceを生成できるか？
```

---

# 6. Start-of-Work Verification

最初にactual repository stateを確認する。

```bash
git branch --show-current
git rev-parse HEAD
git status --short
git log -15 --oneline
git diff --check
git merge-base --is-ancestor \
  e831e3f78d4791a2d4a0ef96f6ce80058c376fae HEAD
echo $?
```

Expected:

```text
branch = refactor/ariadne_mvp_e4
D1 checkpoint is ancestor
```

既存documentation/unrelated working-tree changeは:

```text
discardしない
上書きしない
D2 production checkpointへ不用意に混入しない
```

path-specific stagingを使用する。

---

# 7. Mandatory D2 Lifecycle / Composition Inventory

実装前にactual sourceを検索・読解する。

最低限search:

```text
ExploratoryWorkspaceService(
PredictiveWorkflowService(

__init__(
execution_service

submit_execution(
cancel(
retry(
rerun(
revise(
prefill(

FamilyExecutionOrm
FamilyStageExecutionOrm
FamilyResultOrm
FamilyArtifactOrm

session.add(
session.delete(
status =
retry_count
snapshot_json

get_exploratory_workspace_service
get_predictive_workflow_service

Depends(
```

対象:

```text
src/ariadne/product/application/
src/ariadne/interfaces/web_api/
src/ariadne/interfaces/worker/
src/ariadne/interfaces/cli/
tests/product/
```

inventoryを以下の形で作る。

```text
surface
file/method
Product caller
canonical dependency required?
legacy Family read?
legacy Family write?
silent fallback?
historical compatibility purpose?
D2 disposition
```

D2 disposition:

```text
CANONICAL_ONLY
DELEGATE_CANONICAL
EXPLICIT_REJECT
BOUNDED_READ_ONLY
SCIENCE_ONLY
NOT_APPLICABLE
```

---

# 8. Canonical Dependency Must Be Mandatory for Product Mutation

new Product-facing serviceのmutation pathではcanonical lifecycle dependencyを必須にする。

対象例:

```text
ExploratoryWorkspaceService
PredictiveWorkflowService
```

Product mutation surface:

```text
submit
cancel
retry
rerun
revise
```

について、

```text
execution_service is None
    -> silently legacy Family mutation
```

というbranchは禁止する。

Preferred forms:

## Option A — Constructor requirement

Product serviceとして:

```text
execution_service: ExecutionService
```

をmandatory dependencyとし、dependencyなしconstruction自体を拒否する。

## Option B — Explicit Product mutation guard

science/read compatibility上constructor optionalを残す必要がある場合でも:

```text
Product mutation method
    -> canonical dependency required
    -> missing dependency = explicit LegacyProductAuthorityDisabled / configuration error
```

とする。

どちらを採るかはactual source/caller inventoryに基づいて決定する。

**optional dependencyの有無でauthorityが切り替わるdual-mode mutation設計を残さない。**

---

# 9. FastAPI Product Composition Must Be Canonical-Only

actual FastAPI dependency providersを確認する。

最低限:

```text
get_exploratory_workspace_service
get_predictive_workflow_service
```

はcanonical `ExecutionService`を必ず注入すること。

さらにtestで:

```text
dependency provider construction succeeds

injected service Product mutation path
    = canonical

legacy mutation mode
    = unavailable
```

を固定する。

禁止:

```text
environment variable
optional argument default
test-only constructor path
dependency override omission
```

によってproduction Product APIがold Family mutationへ戻ること。

---

# 10. Exploratory Submit Shutdown

Exploratory Product-facing `submit_execution()` をactual sourceで確認する。

D2 completion時:

```text
submit_execution
    -> canonical Execution creation
    -> canonical StageExecution
```

のみ。

旧bodyがsourceに残る場合:

```text
FamilyExecutionOrm(...)
FamilyStageExecutionOrm(...)
session.add(old Family row)
```

へ到達してはならない。

Allowed:

```text
canonical submit adapter

old private implementation source retained but explicit unreachable/reject
science-only plan/spec helper reuse
```

Forbidden:

```text
if execution_service:
    canonical
else:
    old Family submit
```

old submit bodyをsourceに残す場合も直接呼出し可能なpublic Product mutation surfaceとして残さない。

---

# 11. Predictive Submit Shutdown

Predictive Product-facing `submit_execution()` について同様に固定する。

Required:

```text
canonical Execution
canonical StageExecution
Predictive specification/plan/seed snapshot
no FamilyExecution shadow row
no FamilyStageExecution shadow row
```

canonical dependencyなしconstruct時にlegacy Family submitへfallbackしてはならない。

Phase Cで成立したPredictive canonical submission semanticsをそのまま維持する。

---

# 12. Cancel Shutdown / Delegation

family Product serviceにold cancel bodyが残っている場合:

```text
FamilyExecution.status = CANCELLED
FamilyStageExecution.status = ...
```

を独立authorityとして実行させない。

D2 disposition:

```text
DELEGATE_CANONICAL
or
EXPLICIT_REJECT
```

Product-facing APIでcancelが必要ならcanonical delegationを優先する。

Required:

```text
canonical Execution identity
canonical StageExecution cancellation semantics
no Family lifecycle mutation
```

---

# 13. Retry Shutdown / Delegation

old retry bodyに典型的に存在する:

```text
FamilyResult delete
FamilyArtifact delete
Lineage delete
ArtifactStore physical delete
FamilyExecution reset to QUEUED
FamilyStageExecution reset
attempt_history clear
```

をnew Product retryで絶対に実行しない。

Product-facing retryはPhase C/G02/G03で成立済みのcanonical retryのみ。

Required:

```text
same Execution identity
stable StageExecution identities
attempt history preserved
canonical Result/Artifact ownership not destructively reset
```

old retry implementationを直接呼んでもFamily mutationが起きないようにする。

---

# 14. Rerun Shutdown / Delegation

old family rerunが:

```text
old Family base lookup
    -> old submit
```

を行う場合、new Product authorityとして使用禁止。

Product-facing rerunはcanonical:

```text
new Execution
base_execution_id
revision_kind = RERUN
change_reason = NONE
new StageExecution identities
```

へdelegateする。

canonical base missからFamily baseへfallbackしない。

---

# 15. Revise Shutdown / Delegation

old family reviseが:

```text
old Family base lookup
old submit
revision_kind manually forced
```

を行う場合、新Product authorityとして使用禁止。

Product-facing reviseはPhase Cで成立済みcanonical comparison:

```text
changed conditions -> REVISED + explicit change_reason
same conditions    -> RERUN + change_reason NONE
```

を使用する。

service側のlegacy branchでclassificationを偽装しない。

---

# 16. Result / Artifact Mutating Helper Audit

claim/process以外にもold Family outputをmutationするhelperが残っていないか検索する。

対象pattern:

```text
session.add(FamilyResultOrm
session.add(FamilyArtifactOrm

session.delete(FamilyResultOrm / result)
session.delete(FamilyArtifactOrm / artifact)

FamilyResultOrm(...)
FamilyArtifactOrm(...)

ArtifactStore.delete(...)
```

classification:

```text
canonical worker/output path      -> allowed if canonical owner
historical cleanup/admin          -> NOT D2 unless Product-reachable
legacy Product lifecycle helper   -> delegate/reject/unreachable required
science-only transformation       -> allowed
```

new Product mutationからold Result/Artifact write/deleteへ到達しないこと。

---

# 17. Historical Legacy Read Compatibility — Allowed but Bounded

G07前なのでhistorical old Family rowsのread compatibilityを残してよい。

ただし以下を満たす。

```text
read-only
explicit purpose
bounded entry point
no mutation method reuse
no canonical ID miss fallback
authority label is not ambiguous
```

Preferred:

```text
explicit historical/read-only adapter
```

または明確なprivate helper。

Avoid:

```text
get_execution(id):
    canonical lookup
    if missing:
        FamilyExecution lookup
```

このようなsilent dual-readは不可。

historical pathが必要ならcallerが明示的にhistorical mode/adapterを選ぶ。

---

# 18. Historical Read Must Not Enable Mutation

historical rowを取得できるとしても、そのrowを:

```text
cancel
retry
rerun
revise
process
```

へそのまま渡してmutation authorityとして使えないこと。

behavior test例:

```text
historical read succeeds
historical mutation attempt -> explicit reject
Family table unchanged
```

historical read compatibilityが不要なら無理に残さなくてよい。

---

# 19. Direct Legacy Mutation Behavior Tests

sourceにold mutation facade/methodが残る場合、直接呼出しbehaviorを固定する。

対象:

```text
submit
cancel
retry
rerun
revise
```

存在するもののみ。

### EXPLICIT_REJECTの場合

```text
method call
    -> LegacyProductAuthorityDisabled / explicit unsupported error
```

Assert:

```text
FamilyExecution unchanged
FamilyStageExecution unchanged
FamilyResult unchanged
FamilyArtifact unchanged
ArtifactStore destructive action NONE
```

### DELEGATE_CANONICALの場合

Assert:

```text
canonical Execution/StageExecution changed as expected
Family tables unchanged
```

---

# 20. Accidental Legacy Construction Test

D2では特に以下をtestする。

```text
ExploratoryWorkspaceService(...)
PredictiveWorkflowService(...)
```

をcanonical dependencyなしでconstructし、Product mutationを呼ぶ。

Expected:

```text
construction rejected
or
mutation explicitly rejected
```

Forbidden:

```text
old Family mutation succeeds
```

これをarchitecture regression testとして固定する。

---

# 21. User-Visible Product Route Test

FastAPI Product-facing routeについて、最低限actual relevant routesを通し:

```text
submit
cancel/retry/rerun/revise where exposed
```

がcanonical service compositionを使うことを確認する。

全familyで同じmutation routeが存在しない場合は、実在surfaceだけ検証する。

route testで:

```text
Family table row-count unchanged
canonical row changed/created
```

を必要範囲でassertする。

---

# 22. Causal D2 Inventory

Causalについても以下を確認する。

```text
submit authority
cancel/retry/rerun/revise authority if exposed
old FamilyExecution mutation helper
Product DI/composition
```

既にcanonical-onlyなら:

```text
CANONICAL_ONLY
```

としてevidenceを残す。

old mutation branchが存在する場合はExploratory/Predictiveと同じD2 dispositionを適用する。

不存在を推測しない。

---

# 23. D1 Reject Regression

D2変更後も以下を直接回帰する。

```text
Exploratory claim_next -> EXPLICIT_REJECT
Exploratory process_execution -> EXPLICIT_REJECT

Predictive claim_next -> EXPLICIT_REJECT
Predictive process_execution -> EXPLICIT_REJECT
```

D2 refactorのためにD1で閉じたauthorityを再開しない。

---

# 24. Mandatory D2 Automated Tests

推奨:

```text
tests/product/
test_enh_e4_g05_phase_d_d2_legacy_lifecycle_shutdown.py

tests/product/
test_enh_e4_g05_phase_d_d2_legacy_lifecycle_shutdown_postgres.py
```

actual naming/splitはrepository規約に合わせてよい。

最低限cover:

```text
canonical dependency required for Product mutation

Exploratory submit old branch shutdown
Predictive submit old branch shutdown

cancel old branch shutdown/delegation where applicable
retry old branch shutdown/delegation
rerun old branch shutdown/delegation
revise old branch shutdown/delegation

direct legacy mutation cannot write Family tables

historical read-only compatibility if retained

historical row cannot become mutation target

FastAPI composition canonical-only

Causal lifecycle inventory/assertion
```

---

# 25. Mandatory Real PostgreSQL D2 Scenario

standard PostgreSQL runnerでreal DB evidenceを作る。

推奨scenario:

```text
1. clean Product DB
2. migration head
3. seed Project/Dataset/spec context
4. seed optional historical Family trap rows
5. construct normal Product services through production DI
6. execute Product submit/mutations
7. verify canonical rows
8. verify Family trap rows unchanged
9. construct service without canonical lifecycle dependency
10. invoke Product mutation
11. verify explicit reject and Family rows unchanged
12. if historical read retained, read historical row
13. attempt mutation through historical path
14. verify explicit reject / no Family mutation
15. fresh session reload
```

---

# 26. D2 Old-Table Negative

D2で重点的に確認するtable:

```text
FamilyExecutionOrm
FamilyStageExecutionOrm
FamilyResultOrm
FamilyArtifactOrm
```

before/afterを対象operationごとに確認する。

D3でglobal matrixを再度行うため、D2ではlifecycle/write branchに直接関係するoperationへ集中する。

最低限:

```text
submit
cancel
retry
rerun
revise
```

実在するProduct-facing surfaceについて証明する。

---

# 27. No Artifact Physical Delete from Legacy Retry

特にPredictive old retry等にphysical ArtifactStore deleteが残る場合:

```text
canonical Result/Artifact
historical Family Artifact
```

をold retry branchから削除できないことを確認する。

direct legacy retry reject testではArtifactStore spy/fake等を使い:

```text
delete call count = 0
```

をassertすることを推奨する。

---

# 28. D2 Failure Behavior

canonical lifecycle dependencyが:

```text
missing
misconfigured
throws domain error
canonical lookup misses
```

場合でも:

```text
old Family mutation branch
```

へfallbackしてはならない。

Expected:

```text
explicit configuration/domain failure
```

のみ。

最低1つautomated negativeで固定する。

D3ではより広いfailure fallback matrixを実施する。

---

# 29. Phase C Regression

D2はPhase C lifecycle adapterを触る可能性が高いため、最低限以下を回帰する。

```text
Phase C C1 Predictive Golden Path
Phase C C2 retry
Phase C C3a rerun
Phase C C3b revise
Phase C C4 authority audit

Phase B Exploratory canonical projection
```

actual test pathsを使用する。

---

# 30. D1 Regression

D1 dedicated testをstandard runnerへ含める。

```text
tests/product/test_enh_e4_g05_phase_d_d1_legacy_claim_shutdown_postgres.py
```

actual pathが異なる場合は実在pathへ合わせる。

D1 claim/process authority shutdownを壊していないこと。

---

# 31. Relevant G02 / G03 / G04 Regression

D2 mutation branch変更に関連して:

```text
G02 canonical lifecycle
G03 persistent StageExecution / retry attempt
G04 Result/Artifact ownership
```

を回帰する。

特にold retry destructive behaviorを除去するためG03/G04 contractを必ず維持する。

---

# 32. Standard PostgreSQL Verification

real PostgreSQL evidenceは唯一:

```bash
scripts/test/run_product_postgres_tests.sh <pytest paths/nodes> [...]
```

を使用する。

manual:

```text
docker run
manual DSN
manual psql
manual Alembic
external ad-hoc PostgreSQL pytest
```

は禁止。

report/in-progress evidenceにはcopy-pastable complete commandを書く。

`same as previous` 等で省略しない。

---

# 33. Non-PostgreSQL Boundary Tests

以下のようなDBを必要としないcontractはunit/boundary testでも固定する。

```text
constructor dependency guard
direct legacy mutation reject
FastAPI dependency provider wiring
no optional mutation fallback branch
```

exact command / exit code / pass countを記録する。

---

# 34. Migration Policy

Expected Product migration head:

```text
20260809_product_0010
```

D2はcomposition/lifecycle branch shutdownなので:

```text
new migration = NOT REQUIRED by default
```

禁止:

```text
Family table drop
legacy schema rewrite
historical data migration
root legacy migration modification
```

D2でschema migrationが本当に必要になった場合はDESIGN_BLOCKEDではなく、まず既存canonical schemaで表現不能な理由を証拠化する。

---

# 35. D2 Completion Criteria

以下をすべてDONEにする。

```text
[ ] actual Product lifecycle/composition inventory complete

[ ] Product mutation cannot silently run without canonical dependency

[ ] FastAPI Exploratory service composition canonical-only
[ ] FastAPI Predictive service composition canonical-only
[ ] Causal composition/lifecycle inventory complete

[ ] Exploratory old submit write authority shutdown
[ ] Predictive old submit write authority shutdown
[ ] Causal old submit write authority disposition fixed if present

[ ] old cancel mutation authority shutdown/delegated
[ ] old retry mutation authority shutdown/delegated
[ ] old rerun mutation authority shutdown/delegated
[ ] old revise mutation authority shutdown/delegated

[ ] old Result mutating helper Product reachability = NONE
[ ] old Artifact mutating helper Product reachability = NONE
[ ] old retry cannot physically delete Product Artifact

[ ] direct retained legacy mutation = canonical delegate or explicit reject

[ ] historical legacy compatibility, if retained, is bounded read-only
[ ] canonical lookup miss has no historical silent fallback
[ ] historical read object cannot be mutated through Product lifecycle

[ ] missing canonical dependency cannot activate old Family authority
[ ] canonical lifecycle failure cannot activate old Family authority

[ ] lifecycle Product operations produce no new Family writes

[ ] D1 claim/process explicit-reject regression PASS
[ ] D2 unit/boundary tests PASS
[ ] D2 real PostgreSQL tests PASS

[ ] Phase C regression PASS
[ ] Phase B regression PASS
[ ] relevant G02 regression PASS
[ ] relevant G03 regression PASS
[ ] relevant G04 regression PASS

[ ] migration head verified
[ ] git diff --check PASS

[ ] D2 checkpoint commit created
```

---

# 36. D2 Checkpoint Commit

全criteria PASS後、D2 production source/testのみをcheckpoint commitする。

Suggested:

```text
E4-G05 Trial 01 Phase D D2 legacy lifecycle write shutdown
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

D2 checkpointはPhase D final checkpointではない。

---

# 37. D2 In-Progress Record

必要ならexecution evidenceを以下へ記録する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G05/Trial01/
E4-G05_01_PhaseD__in_progress_06j02.md
```

本instruction fileへ実行結果を追記しない。

D2でPhase D final reportはまだ作成しない。

---

# 38. D2 Stop Condition

今回停止してよい条件は:

```text
PHASE_D_D2_COMPLETE
```

のみ。

以下を全て満たす。

```text
D2 completion criteria all DONE
D2 standard PostgreSQL verification PASS
required regression PASS
D2 checkpoint commit created
```

最後に必ず:

```text
PHASE_D_D2_COMPLETE
Checkpoint SHA: <full SHA>

Product mutation requires canonical dependency: PASS

Exploratory submit legacy authority:
<DELEGATE_CANONICAL | EXPLICIT_REJECT | NOT_PRESENT>

Predictive submit legacy authority:
<DELEGATE_CANONICAL | EXPLICIT_REJECT | NOT_PRESENT>

Causal submit legacy authority:
<CANONICAL_ONLY | DELEGATE_CANONICAL | EXPLICIT_REJECT | NOT_PRESENT>

Legacy cancel/retry/rerun/revise:
<summary>

Historical legacy compatibility:
<BOUNDED_READ_ONLY | NOT_RETAINED>

Canonical miss -> old fallback:
NONE

Product lifecycle old Family writes:
NONE

PostgreSQL verification:
PASS
```

を報告して停止する。

---

# 39. D2 Stop Reasons NOT Accepted

以下を途中停止理由として認めない。

```text
optional execution_service branchを発見した

old submit bodyを発見した

old retryがFamily Result/Artifactを削除していた

constructor変更でtest修正が必要

FastAPI dependency testがFAILした

historical compatibility整理が必要

legacy testがold behaviorをassertしている

Phase C regressionがFAILした

D3がまだ残っている

Phase D全体が未完了
```

correct testによるD2 production defectはD2内で修正し、PASSまで再実行する。

DESIGN_BLOCKEDは、passed architectureとactual Product semanticsの間に、canonical delegation / explicit reject / bounded read-only分離では解決不能なsemantic contradictionがある場合のみ。

---

# 40. D3 Preview — Do NOT Execute

D2完了後のD3では以下を扱う。

```text
all-family route/service/worker/CLI reachability audit

global static Product authority map

Causal / Exploratory / Predictive runtime negative matrix

canonical submit/process/mutation failure injection
    -> no old fallback

old Family 4-table before/after
    -> unchanged across new Product Golden Paths

GenericExecutor non-authority final audit

remaining old source classification:
    historical read
    science-only
    explicit reject
    G07 retirement candidate

Phase A/B/C + D1/D2 regression

G02/G03/G04 regression

Phase D final implementation checkpoint

E4-G05_01_PhaseD_implementation_checkpoint_report.md

PHASE_D_COMPLETE
```

D2 runではD3へ進まない。

---

# 41. Forbidden Scope Crossing

D2で行わない。

```text
old Family table drop
broad legacy source deletion
ariadne.legacy retirement
root legacy migration rewrite
historical data rewrite

G06 lineage final authority consolidation

G07 CLI/source retirement finalization

G08 clean bootstrap final audit

TD-001/002/003 final closure
G05 final implementation completion report
READY_FOR_TEST

Current Architecture Control Sheet update
```

---

# 42. Final Instruction

E4-G05 Trial 01 Phase D D2 —

```text
Legacy lifecycle/write branch shutdown
+
bounded historical read compatibility
```

のみを実行し、

```text
PHASE_D_D2_COMPLETE
```

まで完遂せよ。

D2完了後、このrunではD3へ進まないこと。
