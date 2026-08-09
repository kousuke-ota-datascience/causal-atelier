# E4-G05 Trial 01 — Phase D Legacy Authority Shutdown Implementation Instruction

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Branch: `refactor/ariadne_mvp_e4`
- Gate: `E4-G05`
- Gate name: Product Execution Convergence
- Trial: `01`
- Phase: `D`
- Phase name: Global legacy Product authority shutdown
- Previous phase: `Phase C — PHASE_C_COMPLETE`
- Previous phase final implementation checkpoint: `9c58bffd5c5fb6be8565a1256222e678fb86c52a`
- Previous phase report commit: `2ee00aa30572a1f7771488eb3953dcd5d0e7b65a`
- Expected Product migration head: `20260809_product_0010`
- Gate READY_FOR_TEST: `NO`

---

# 1. Purpose

E4-G05 Trial 01を継続する。

Phase A / B / Cでnew Product-facing family flowはcanonical Product aggregateへ収束した。

Phase Dの目的は、source上に残存するold Family lifecycle / output authorityについて、

> **new Product runtimeからwrite/claim/process authorityとして到達できない状態をarchitectureとして固定すること**

である。

Phase Dではlegacy source/tableの全面削除を行わない。

G07前なので以下は残ってよい。

```text
FamilyExecutionOrm
FamilyStageExecutionOrm
FamilyResultOrm
FamilyArtifactOrm
legacy family service source
historical read-only compatibility source
```

しかし、new Product runtimeから以下へ到達してはならない。

```text
old submit write
family-specific claim
old process persistence
old cancel/retry/rerun/revise mutation
old Result/Artifact create/delete
canonical failure -> old authority fallback
```

---

# 2. Execution Strategy — Do NOT Attempt Phase D in One Run

これまでのG05 execution historyを踏まえ、Phase Dを一回のCoding Agent runで完遂しようとしない。

Phase D内部を以下の3 work packageへ分割する。

```text
D1  Legacy claim/process authority shutdown
    - family-specific old claim_next/process_execution disposition
    - canonical worker is sole Product claimer/processor
    - direct old mutation behavior = delegate or explicit reject
    - checkpoint commit

D2  Legacy lifecycle/write branch shutdown
    - Product composition cannot enter legacy submit/mutation branches
    - old mutating methods delegate canonical or explicitly reject
    - historical reads, if retained, are read-only and bounded
    - checkpoint commit

D3  Global authority reachability / no-fallback / runtime negative audit
    - all-family static route/service/worker inventory
    - failure injection no-fallback
    - old Family table runtime row-count negative
    - GenericExecutor remains non-authoritative
    - Phase D regression
    - Phase D final checkpoint report
    - PHASE_D_COMPLETE
```

**この初回runではD1だけを実行すること。**

初回runのexit condition:

```text
PHASE_D_D1_COMPLETE
```

Phase D全体の:

```text
PHASE_D_COMPLETE
```

ではない。

D1完了後、このrunではD2へ進まないこと。

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
20_implementation_reports/G05/Trial01/
E4-G05_01_PhaseC_implementation_checkpoint_report.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
00_ENH-E4_Current_Architecture_Control_Sheet.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
30_test_report/G04/
E4-G04_02_999_gate_decision.md
```

Current Architecture Control SheetはG05 PASS前なのでCoding Agentが更新しない。

---

# 4. Approved G05 Authority Contract

G05 exit時のProduct authorityは以下のみ。

```text
Product API / auditable Product entry
        ↓
family request adapter
        ↓
canonical Execution Service
        ↓
canonical Execution UoW
        ├─ Execution
        └─ persistent StageExecution
        ↓
one canonical claim / lease authority
        ↓
Execution.analysis_family
        ↓
family scientific adapter / runner
        ↓
canonical Result / Artifact owner
```

family-specific scientific implementationは残してよい。

family-specific lifecycle authorityは残してはならない。

---

# 5. Phase C Established State — Preserve

Phase C final checkpointで少なくともPredictiveについて以下が成立済み。

```text
submit                    canonical
Execution read/list       canonical
StageExecution read       canonical
Result/Artifact read      canonical
lineage/prefill           canonical-owned IDs / snapshot
cancel/retry              canonical lifecycle
rerun/revise              canonical base Execution
worker                     canonical claim + ExecutionProcessor
```

Phase C reportではlegacy branches/sourceが残る一方、injected canonical Product modeからはunreachableと整理されている。

Phase Dではこの「現在はunreachable」を、

```text
accidental configurationで再到達できない
direct old mutating methodが独立authorityとして動作しない
worker/product wiringからfamily-specific claimerへ戻れない
```

状態へ強化する。

Phase Cのcanonical behaviorを巻き戻さない。

---

# 6. Verified Current D1 Risk

current sourceには少なくともold family-specific lifecycle methodが残存している。

Exploratory側には概念上:

```text
claim_next()
    -> FamilyExecutionOrm
    -> SELECT ... FOR UPDATE SKIP LOCKED
    -> FamilyStageExecutionOrm mutation

process_execution()
    -> FamilyExecutionOrm
    -> FamilyStageExecutionOrm
    -> FamilyResultOrm
    -> FamilyArtifactOrm
```

が残っている。

Predictive側にも概念上:

```text
claim_next()
    -> FamilyExecutionOrm
    -> SELECT ... FOR UPDATE SKIP LOCKED

process_execution()
    -> FamilyExecutionOrm
    -> old Family Stage/Result/Artifact persistence
```

が残っている。

一方、current Product worker runnerは:

```text
uow.executions.claim_next(...)
    -> ExecutionProcessor.process(...)
```

というcanonical claim pathを使用している。

D1ではこの状態を「worker wiringがたまたまcanonical」から、

> **old family-specific claim/process methodはProduct authorityとして実行不能**

へ固定する。

---

# 7. D1 Scope

D1の対象は**claim/process authorityのみ**。

対象候補:

```text
ExploratoryWorkspaceService.claim_next
ExploratoryWorkspaceService.process_execution

PredictiveWorkflowService.claim_next
PredictiveWorkflowService.process_execution

その他actual inventoryで見つかる
family-specific Product claim/process method
```

Causalについてもactual sourceをinventoryする。

存在しないold Causal claimerを捏造しない。

存在する場合のみD1対象に含める。

---

# 8. D1 Does NOT Include

今回D1で進めない。

```text
legacy submit branch full shutdown                  # D2
legacy cancel/retry/rerun/revise branch full audit  # D2
historical read compatibility final split           # D2
global failure fallback matrix                      # D3
all-family old-table Golden Path matrix             # D3
CLI final classification/completion                 # D3/Phase E as applicable
TD-001/002/003 final closure                        # Phase E
G05 final completion report                         # Phase E
READY_FOR_TEST                                      # Phase E
G06 lineage authority final consolidation
G07 legacy source/table retirement
G08 final bootstrap audit
```

ただしD1のclaim/process shutdownを成立させるために必要なminimal refactorは許可する。

---

# 9. Start-of-Work Verification

最初にactual repository stateを確認する。

```bash
git branch --show-current
git rev-parse HEAD
git status --short
git log -12 --oneline
git diff --check
git merge-base --is-ancestor   9c58bffd5c5fb6be8565a1256222e678fb86c52a HEAD
echo $?
```

Expected:

```text
branch = refactor/ariadne_mvp_e4
Phase C final implementation checkpoint is ancestor
```

Phase C report metadata correction等の既存documentation変更がworking treeにある場合:

```text
discardしない
上書きしない
D1 production checkpointへ不用意に混入しない
```

path-specific stagingを使用する。

actual D1 starting commitをin-progress/checkpoint recordに記録する。

---

# 10. Mandatory D1 Authority Inventory Before Coding

actual sourceを検索する。

最低限以下をinventoryする。

```text
claim_next(
process_execution(
SELECT ... FOR UPDATE
skip_locked
FamilyExecutionOrm
FamilyStageExecutionOrm
FamilyResultOrm
FamilyArtifactOrm
ExecutionProcessor
run_worker
GenericExecutor
```

対象directory:

```text
src/ariadne/product/application/
src/ariadne/interfaces/worker/
src/ariadne/interfaces/web_api/
src/ariadne/interfaces/cli/
tests/product/
```

inventory output concept:

```text
method/function
file
family
current caller(s)
direct Product reachability
old table write/claim capability
D1 disposition
```

D1 dispositionは以下のいずれか。

```text
DELEGATE_CANONICAL
EXPLICIT_REJECT
REMOVE_PRODUCT_ROUTING
SCIENCE_ONLY_EXTRACTED
READ_ONLY_NOT_D1
NOT_APPLICABLE
```

source fileの存在だけでauthorityと判定しない。

**call graph / composition / direct invocation behaviorまで見ること。**

---

# 11. Allowed D1 Disposition

old family-specific claim/process methodが残る場合、以下のいずれかへ収束させる。

## A. Explicit Reject

最も単純で安全な場合:

```text
old claim_next()
    -> explicit exception / unsupported legacy Product mutation

old process_execution()
    -> explicit exception / unsupported legacy Product mutation
```

要件:

```text
Family tableをSELECT FOR UPDATEしない
Family statusを変えない
Family Result/Artifactを書かない
canonical failure fallbackに使えない
behavior testがある
```

## B. Delegate Canonical

既存public/internal caller compatibility上methodを残す必要があり、意味が明確にcanonicalへ委譲可能な場合:

```text
old facade
    -> canonical claim/service
```

要件:

```text
FamilyExecutionOrmをauthorityとして読まない
canonical Execution IDを返す
canonical lease semantics
family filterが必要ならcanonical Execution.analysis_familyに対するadapter
```

ただしworker全体としてfamily-specific claimerを複数持つarchitectureへ戻してはならない。

## C. Remove Product Routing

method自体を残してもよいが、Product composition/rootから完全に切り離す。

ただし:

```text
直接呼べばold writeできる
```

状態が「Product service public API」として残るなら不十分。

新Product authorityの誤使用を防ぐため、public mutating surfaceならdelegate/rejectを優先する。

---

# 12. Preferred D1 Direction

current workerは既にcanonical:

```text
uow.executions.claim_next(...)
    -> ExecutionProcessor
    -> family dispatch
```

である。

したがって、old family-specific `claim_next/process_execution` がnew Product runtimeで不要なら、

```text
explicit reject
or
internal science-only codeへ分離しold lifecycle methodを非authoritative化
```

を優先する。

D1のためだけに複数のfamily-specific canonical claimer wrapperを増やさない。

---

# 13. Scientific Code Preservation

old `process_execution()` 内に、

```text
scientific runner construction
frame loading
family plan/spec reconstruction
science-only transformation
```

と、

```text
Family ORM lifecycle
Family output persistence
claim/lease
```

が混在している場合:

**science側を失ってはならない。**

必要なら:

```text
science/planning/helper
    -> reusable adapter

old lifecycle persistence shell
    -> reject / unreachable
```

に分離する。

Phase C canonical `ExecutionProcessor` が既に同じscienceを使っている場合、重複抽出を増やさない。

scientific algorithm/statistics自体を変更しない。

---

# 14. Canonical Worker Must Remain Sole Product Claimer

D1完了後、Product workerのclaimは一つだけ。

```text
run_worker()
    ↓
SqlUnitOfWork
    ↓
uow.executions.claim_next()
    ↓
canonical Execution
    ↓
ExecutionProcessor
```

family dispatchはclaim**後**。

禁止:

```text
try canonical claim
if none:
    exploratory.claim_next()

try canonical claim
if none:
    predictive.claim_next()

family別worker loop
    -> FamilyExecutionOrm claim

canonical worker error
    -> old family process_execution fallback
```

---

# 15. GenericExecutor Boundary

`GenericExecutor`はscientific stage executorとして再利用してよい。

しかしD1でも:

```text
Execution identity owner
claim owner
lease owner
persistent StageExecution owner
Result/Artifact owner
```

になってはならない。

D1 testでは既存G03/G04 negative contractを維持する。

---

# 16. Direct Old-Method Behavior Test

old mutating `claim_next/process_execution` がsourceに残る場合、そのmethod自体のbehavior testを必須とする。

### Explicit rejectの場合

seedとしてold Family rowを用意しても:

```text
method invocation
    -> explicit rejection
```

となり、

```text
FamilyExecution status unchanged
FamilyStageExecution unchanged
FamilyResult count unchanged
FamilyArtifact count unchanged
```

をassertする。

### Canonical delegateの場合

```text
method invocation
    -> canonical repository/service
```

であることをassertし:

```text
Family table mutation = NONE
canonical identity/lease used
```

を証明する。

---

# 17. Old Family SELECT FOR UPDATE Negative

static inventoryだけでなく、D1 completion時にはnew Product claim pathから:

```text
FamilyExecutionOrm
SELECT FOR UPDATE SKIP LOCKED
```

へ到達しないことを証明する。

可能ならautomated architecture/boundary testで:

```text
worker runner source/composition
family service claim method behavior
```

を固定する。

fragileな文字列grepだけを唯一の証拠にせず、static evidence + behavior testを組み合わせる。

---

# 18. Causal Inventory

D1は三familyのauthority GateなのでCausalも確認する。

最低限actual sourceから:

```text
Causal Product submission/worker
old Causal-specific claim source
old FamilyExecution-based claim path
```

の有無を確認する。

結果は:

```text
FOUND -> D1 disposition required
NOT_FOUND -> evidence with searched locations
```

とする。

不存在を推測で宣言しない。

---

# 19. Mandatory D1 Automated Tests

推奨logical test:

```text
tests/product/
test_enh_e4_g05_phase_d_d1_legacy_claim_shutdown.py

tests/product/
test_enh_e4_g05_phase_d_d1_legacy_claim_shutdown_postgres.py
```

actual split/namingはrepository規約に合わせてよい。

最低限cover:

```text
canonical worker sole claim path

Exploratory old claim disposition
Exploratory old process disposition

Predictive old claim disposition
Predictive old process disposition

Causal old claim disposition if present

direct old method cannot mutate Family authority

no canonical failure fallback into old claim/process
```

---

# 20. Mandatory Real PostgreSQL D1 Test

standard PostgreSQL runnerのみを使う。

scenario例:

```text
1. clean Product DB
2. Product migrations head
3. canonical queued executions for relevant families
4. optional old Family queued rows as trap fixtures
5. canonical worker/claim path execute
6. verify canonical Execution claimed/processed
7. verify old Family trap rows untouched
8. directly invoke retained old claim/process method
9. verify reject/delegate behavior
10. fresh session reload
```

old Family trap rowをseedする場合、そのfixture作成自体をProduct runtime behaviorと混同しない。

---

# 21. D1 Canonical Failure Negative

少なくとも1つ、canonical claim/process側へcontrolled failureを入れる。

Expected:

```text
canonical failure
    -> canonical error/retry/failure handling
```

Forbidden:

```text
canonical failure
    -> FamilyExecutionOrm claim/process
```

D1ではglobal failure matrix全部を行う必要はない。

claim/process authorityに限定してno fallbackを証明する。

---

# 22. Phase C Regression Required in D1

D1はPhase C worker pathを触る可能性があるため、最低限以下を回帰する。

```text
Predictive C1 Golden Path
Predictive C2 retry
Predictive C3a rerun
Predictive C3b revise
Predictive C4 authority audit
Exploratory Phase B canonical projection
```

実在するactual test pathを使用する。

特にC1 canonical worker Golden Pathは必須。

---

# 23. Relevant G02/G03/G04 Regression

D1がclaim/process boundaryへ触れるため最低限:

```text
G02 canonical claim/lifecycle
G03 persistent StageExecution / attempt history
G04 Result/Artifact ownership
```

の関連testを実行する。

過去assertionを弱めない。

---

# 24. Standard PostgreSQL Verification

real PostgreSQL entry pointは唯一:

```bash
scripts/test/run_product_postgres_tests.sh <pytest paths/nodes> [...]
```

を使用する。

manual:

```text
docker run
manual DSN
psql
manual Alembic
ad-hoc external PostgreSQL pytest
```

は禁止。

D1 completion evidenceには完全なcopy-pastable commandを書く。

`same as previous` 等の省略は禁止。

---

# 25. Migration Policy

Expected Product head:

```text
20260809_product_0010
```

D1はauthority/wiring shutdownなので:

```text
new migration = NOT REQUIRED by default
```

old Family tableをdropしない。

root legacy migrationを変更しない。

historical application-data migrationを行わない。

D1のためだけの空migrationを作らない。

---

# 26. D1 Completion Criteria

以下を全てDONEにする。

```text
[ ] actual claim/process authority inventory completed

[ ] Product worker uses canonical uow.executions.claim_next only

[ ] family dispatch happens after canonical claim

[ ] Exploratory old claim_next disposition fixed
[ ] Exploratory old process_execution disposition fixed

[ ] Predictive old claim_next disposition fixed
[ ] Predictive old process_execution disposition fixed

[ ] Causal old claim/process inventory completed
[ ] Causal old method disposition fixed if present

[ ] retained old mutating method = canonical delegate or explicit reject

[ ] direct old method cannot independently mutate Family lifecycle/output

[ ] Product worker cannot fall back to family-specific claimer

[ ] canonical claim/process failure cannot fall back to old Family authority

[ ] old Family SELECT FOR UPDATE is unreachable from new Product claim path

[ ] GenericExecutor remains non-authoritative

[ ] D1 behavior/unit tests PASS
[ ] D1 real PostgreSQL tests PASS

[ ] Phase C worker/authority regression PASS
[ ] relevant G02 regression PASS
[ ] relevant G03 regression PASS
[ ] relevant G04 regression PASS

[ ] Product migration head verified
[ ] git diff --check PASS

[ ] D1 checkpoint commit created
```

---

# 27. D1 Checkpoint Commit

全criteria PASS後、D1 production source/testのみをcheckpoint commitする。

Suggested message:

```text
E4-G05 Trial 01 Phase D D1 legacy claim process shutdown
```

commit前:

```bash
git status --short
git diff --check
git diff --cached --name-status
```

documentation/unrelated changesを不用意にstageしない。

commit後:

```bash
git rev-parse HEAD
git status --short
```

を記録する。

D1 checkpointはPhase D final implementation checkpointではない。

---

# 28. D1 In-Progress / Checkpoint Record

必要ならD1のexecution evidenceは以下へ記録する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G05/Trial01/
E4-G05_01_PhaseD__in_progress_06j01.md
```

instruction fileへexecution resultを追記しない。

Phase D final reportはD3で別途:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G05/Trial01/
E4-G05_01_PhaseD_implementation_checkpoint_report.md
```

として作成する。

---

# 29. D1 Stop Condition

今回停止してよい条件は以下のみ。

```text
PHASE_D_D1_COMPLETE
```

以下を全て満たすこと。

```text
D1 completion criteria all DONE
standard PostgreSQL D1 verification PASS
required regression PASS
D1 checkpoint commit created
```

最後に必ず:

```text
PHASE_D_D1_COMPLETE
Checkpoint SHA: <full SHA>
Canonical worker sole claim authority: PASS
Exploratory old claim/process: <DELEGATE_CANONICAL | EXPLICIT_REJECT | NOT_PRESENT>
Predictive old claim/process: <DELEGATE_CANONICAL | EXPLICIT_REJECT | NOT_PRESENT>
Causal old claim/process: <DELEGATE_CANONICAL | EXPLICIT_REJECT | NOT_PRESENT>
Canonical failure -> old fallback: NONE
PostgreSQL verification: PASS
```

を報告して停止する。

---

# 30. D1 Stop Reasons NOT Accepted

以下を途中停止理由として認めない。

```text
old claim_nextを発見した
old process_executionを発見した
Family ORM writeが残っていた
direct behavior test追加が必要
canonical worker testがFAILした
old method rejectへ変更が必要
science helper extractionが必要
G02/G03/G04 regressionが未実行
D2/D3がまだ残っている
Phase D全体が未完了
```

これらはD1内で解決する対象である。

DESIGN_BLOCKEDは、passed G02/G03/G04/G05 contractとexisting scientific semanticsの間に、delegate/reject/science extractionでは解消不能なsemantic contradictionがある場合のみ。

単なるlegacy code量、test failure、refactor必要性はDESIGN_BLOCKEDではない。

---

# 31. D2 Contract Preview — Do NOT Execute in This Run

D1完了後のD2は以下を扱う予定。

```text
Product composition / DI audit
    -> canonical dependency injection mandatory

legacy submit branches
    -> delegate canonical or explicit reject

legacy cancel/retry/rerun/revise branches
    -> delegate canonical or explicit reject

old Result/Artifact mutating helpers
    -> no new Product write authority

historical read compatibility
    -> explicit bounded read-only if retained

accidental service construction without canonical dependency
    -> cannot silently activate legacy Product lifecycle
```

D1 runではD2へ進まない。

---

# 32. D3 Contract Preview — Do NOT Execute in This Run

D3ではPhase D全体を最終監査する。

```text
all-family route/service/worker graph
static reachability audit
new Product failure injection no-fallback

real PostgreSQL:
old family table counts before
    ↓
Causal / Exploratory / Predictive Product operations
    ↓
old family table counts after
unchanged

GenericExecutor non-authority
Product/auditable CLI old-authority reachability inventory
Phase A/B/C + G02/G03/G04 regression
Phase D final implementation checkpoint
Phase D checkpoint report
PHASE_D_COMPLETE
```

Phase EのTD closure / G05 final Completion Report / READY_FOR_TESTは行わない。

---

# 33. Phase D Final Boundary

Phase D終了時に目指す状態:

```text
old source may exist
old tables may exist
historical reads may exist

BUT

new Product submit
new Product claim
new Product process
new Product mutation
new Product Result/Artifact persistence
canonical failure recovery

cannot use old Family authority
```

Phase Dは**source deletion Gateではない**。

G07のretirement作業を先取りしない。

---

# 34. Forbidden Scope Crossing

Phase Dで禁止:

```text
old Family tables drop
broad legacy source deletion
ariadne.legacy retirement
root legacy migration rewrite
historical application data migration

G06 lineage final authority consolidation
generic-only lineage allowlist cutover
closure/export redesign

G07 CLI/source retirement finalization

G08 final clean bootstrap audit

Current Architecture Control Sheet update
    # operator updates only after final Gate PASS
```

---

# 35. Final Instruction for This Run

E4-G05 Trial 01 Phase Dの**D1 — Legacy claim/process authority shutdownのみ**を実行し、

```text
PHASE_D_D1_COMPLETE
```

まで完遂せよ。

D1完了後、このrunではD2へ進まないこと。
