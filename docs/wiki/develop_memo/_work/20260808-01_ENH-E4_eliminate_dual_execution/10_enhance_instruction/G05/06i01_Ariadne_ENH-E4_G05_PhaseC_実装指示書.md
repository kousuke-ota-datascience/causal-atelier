# E4-G05 Trial 01 — Phase C Predictive Convergence Implementation Instruction

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Branch: `refactor/ariadne_mvp_e4`
- Gate: `E4-G05`
- Gate name: Product Execution Convergence
- Trial: `01`
- Phase: `C`
- Phase name: Predictive canonical lifecycle/read convergence
- Previous phase implementation checkpoint: `b77e3febd9c6c48b553bc59cd8e5be29f2aba998`
- Last confirmed documentation normalization commit: `e6c410de6ec4d928c6c3ec8b9647d6ff39a92008`
- Phase A status: `PHASE_A_COMPLETE`
- Phase B status: `PHASE_B_COMPLETE`
- Product migration head at Phase B completion: `20260809_product_0010`

---

# 1. Purpose

E4-G05 Trial 01を継続する。

今回は **Phase C — Predictive convergenceのみを完了すること**。

Phase Cでは、Product-facing Predictive lifecycleをcanonical Product Execution aggregateへ収束させる。

対象:

```text
Predictive submit
Predictive Execution read
Predictive StageExecution read
Predictive Result read
Predictive Artifact read
Predictive lineage read projection
Predictive cancel
Predictive retry
Predictive rerun
Predictive revise
Predictive prefill
Predictive API / DI construction
```

今回のexit conditionは:

```text
PHASE_C_COMPLETE
```

であり、G05全体の:

```text
READY_FOR_TEST
```

ではない。

Phase D / Eへ進まない。

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
06g01_Ariadne_ENH-E4_G05_PhaseA_実装指示書.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
10_enhance_instruction/G05/
06h01_Ariadne_ENH-E4_G05_PhaseB_実装指示書.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G05/Trial01/
E4-G05_01_PhaseA_implementation_checkpoint_report.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G05/Trial01/
E4-G05_01_PhaseB_implementation_checkpoint_report.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
00_ENH-E4_Current_Architecture_Control_Sheet.md
```

Passed G02 / G03 / G04 contractを変更しない。

特に維持する:

```text
G02:
one canonical Execution identity
canonical lifecycle mutation semantics
retry = same Execution identity
rerun/revise = new Execution identity + base relation
changed Execution requires explicit change reason

G03:
persistent canonical StageExecution
stable StageExecution identity
attempt history belongs to StageExecution lifecycle

G04:
canonical Result / Artifact ownership
typed Result / Artifact semantics
artifact_id != object_key
Result ↔ Artifact association
```

---

# 3. Start-of-Work Verification

最初にactual repository stateを確認する。

```bash
git branch --show-current
git rev-parse HEAD
git status --short
git log -10 --oneline
git merge-base --is-ancestor \
  b77e3febd9c6c48b553bc59cd8e5be29f2aba998 HEAD
echo $?
git diff --check
```

Expected branch:

```text
refactor/ariadne_mvp_e4
```

`b77e3febd9c6c48b553bc59cd8e5be29f2aba998` がHEAD ancestryに存在すること。

Phase B reportへの手動metadata修正等、Phase C開始前から存在するworking-tree変更を発見した場合:

```text
discardしない
上書きしない
Phase C production commitへ混入させない
```

path-specific stagingを用いてPhase C変更と分離する。

actual Phase C starting commitをcheckpoint reportへ記録する。

---

# 4. Mandatory Current-State Inventory Before Coding

過去checkpoint narrativeだけを信頼せず、actual sourceを読む。

最低限:

```text
src/ariadne/interfaces/web_api/dependencies.py

src/ariadne/interfaces/web_api/routers/predictive_workflow.py

src/ariadne/product/application/predictive_workflow_service.py

src/ariadne/product/application/execution_service.py

src/ariadne/interfaces/worker/execution_processor.py

src/ariadne/interfaces/worker/runner.py

src/ariadne/product/persistence/orm_models.py

tests/product/
```

を確認する。

以下のsurfaceごとにcurrent authorityを短くinventoryする。

```text
submit
get/list Execution
get StageExecution
get Result
get Artifact
lineage projection
cancel
retry
rerun
revise
prefill
worker claim/process
```

このinventoryはcheckpoint reportのImplementation Detailsへ反映する。

---

# 5. Verified Starting Defect / Inconsistency

Phase C開始前のbranch確認では、少なくとも以下の不整合が存在する。

## 5.1 DI constructor mismatch

`dependencies.py` は概念上:

```python
PredictiveWorkflowService(
    session_factory,
    artifact_store,
    execution_service=ExecutionService(...),
)
```

としてcanonical `ExecutionService`を注入しようとしている。

一方、current `PredictiveWorkflowService.__init__` は概念上:

```python
def __init__(self, session_factory, artifact_store)
```

であり、`execution_service`を受け取らない。

Phase Cではこの不整合を必ず閉じる。

Dependency/providerを生成しただけでTypeErrorになる状態を残してはならない。

## 5.2 Product-facing Predictive authority remains legacy

current sourceでは少なくとも以下が旧Family ORM authorityを直接使用している。

```text
submit_execution
    -> FamilyExecutionOrm / FamilyStageExecutionOrm

list_executions / get_execution
    -> FamilyExecutionOrm

get_stages
    -> FamilyStageExecutionOrm

list_results
    -> FamilyResultOrm

list_artifacts
    -> FamilyArtifactOrm

list_lineage
    -> Family Result / Artifact IDs as owned IDs

cancel
    -> FamilyExecutionOrm / FamilyStageExecutionOrm

retry
    -> FamilyExecutionOrm
    -> FamilyStageExecutionOrm
    -> FamilyResultOrm
    -> FamilyArtifactOrm

rerun / revise / prefill
    -> FamilyExecutionOrm
```

これはPhase CでProduct-facing surfaceについて解消する。

---

# 6. Phase C Architecture Rule

Phase C完了後、新しいuser-visible Predictive Product operationについて:

```text
Execution identity authority
    = canonical Product Execution

Stage lifecycle authority
    = canonical StageExecution

Result ownership/read authority
    = canonical Result

Artifact ownership/read authority
    = canonical Artifact

cancel/retry/rerun/revise lifecycle authority
    = canonical ExecutionService / approved canonical lifecycle contract
```

でなければならない。

family-specific:

```text
Predictive AnalysisSpecification
ExecutionPlan
planner
runner
scientific payload
response DTO / projection
```

は残してよい。

**scientific family semanticsをcanonical authorityと混同しないこと。**

---

# 7. Predictive Service Dependency Boundary

`PredictiveWorkflowService`にcanonical lifecycle dependencyを明示的に持たせる。

Preferred concept:

```text
PredictiveWorkflowService
    ├─ family scientific/session dependencies
    ├─ ArtifactStore where genuinely needed
    └─ ExecutionService / canonical read boundary
```

具体的なconstructor shapeはactual codeに合わせてよい。

ただし:

```text
canonical modeなのにdependency未使用
DIだけexecution_serviceを渡してserviceはlegacy
optional Noneだからsilent legacy fallback
```

という状態は禁止。

必要ならPhase Bと同様に明示的なmode/boundaryを設けてもよいが、新Product-facing APIはcanonical modeを使用すること。

---

# 8. Predictive Submit Convergence

Product-facing endpoint:

```text
POST /projects/{project_id}/executions
```

から作成されるnew Predictive executionをcanonical化する。

Required:

```text
canonical Execution created
analysis_family = PREDICTIVE
persistent canonical StageExecution materialized
canonical execution_id returned
no FamilyExecutionOrm shadow row
no FamilyStageExecutionOrm shadow row
```

既存Predictive validationを失わない。

少なくとも:

```text
project active
AnalysisSpecification fixed / valid
ExecutionPlan belongs to project
ExecutionPlan belongs to submitted specification
plan validation PASS
seed semantics preserved
dataset_version ownership preserved
analysis_view semantics preserved
research_context semantics preserved where applicable
```

を維持する。

---

# 9. Preserve Predictive Scientific Snapshot Semantics

旧Family Execution snapshotで保持していた情報を、canonical Executionのapproved fields / `analysis_spec_json` / parameter/runtime snapshot等へlosslessにmappingする。

少なくとも:

```text
analysis_specification_id
analysis specification hash/version where required
execution_plan_id
execution plan hash/version where required
seed
dataset_version_id
analysis_view_id
research_context context needed by runner
family-specific immutable specification
planner/runner-required metadata
```

をworker/read/mutationで復元可能にする。

禁止:

```text
canonical execution_idだけ作ってPredictive plan/spec contextを失う
legacy FamilyExecutionOrmをsnapshot sidecarとして新規作成する
worker executionのためにold Family rowを必須にする
```

Phase Cで必要なfamily metadataはcanonical Executionから取得可能にする。

---

# 10. Execution Operation Mapping

canonical `ExecutionService.create_execution_batch()` を利用する場合、Predictive familyのoperation mappingをactual approved canonical semanticsに合わせる。

禁止:

```text
Causal用operationを意味もなく流用
validationを通すためだけに虚偽のoperationを設定
family scientific semanticsと矛盾するinput_graph/input_resultを捏造
```

既存`CanonicalPlanProvider` / family runner contractを読み、Predictive用に現在approvedされているmappingを使う。

もしcurrent canonical domainがPredictive submissionをlosslessに表現できないsemantic contradictionを発見した場合のみDESIGN_BLOCKED候補とする。

単なるadapter不足はDESIGN_BLOCKEDではない。

---

# 11. Predictive Execution Read Projection

Product-facing Predictive readはcanonical Executionを読む。

対象:

```text
list_executions if used
get_execution
```

Required isolation:

```text
project_id match
analysis_family == PREDICTIVE
```

responseは既存Predictive-facing shapeを可能な限り維持する。

必要なprojection field例:

```text
execution_id
project_id
analysis_family
dataset_version_id
analysis_view_id
analysis_specification_id
execution_plan_id
snapshot_hash / equivalent canonical snapshot evidence
status
retry_count
base_execution_id
revision_kind
requested_by
requested_at
started_at
finished_at
last_error
```

canonical dataから取得できるものを旧Family rowで補完してはならない。

family-specific fieldはcanonical snapshotからprojectionする。

---

# 12. Predictive StageExecution Read Projection

Product-facing:

```text
GET /projects/{project_id}/executions/{execution_id}/stages
```

はcanonical `StageExecution`を読む。

Assert:

```text
canonical stage_execution_id
execution_id
stage_key
ordinal
status
attempt history / attempt metadata where response contract exposes it
timestamps
last error where exposed
```

旧 `FamilyStageExecutionOrm` をnew executionのread authorityにしない。

---

# 13. Predictive Result Read Projection

Product-facing:

```text
GET /projects/{project_id}/executions/{execution_id}/results
```

はcanonical Resultを読む。

Phase Aで追加したtyped Predictive Result semantics:

```text
SPLIT_RESULT
TRAINING_RESULT
EVALUATION_RESULT
ERROR_ANALYSIS_RESULT
PREDICTIVE_EXPLANATION_RESULT
MODEL_CARD_RESULT
```

およびapproved ScientificStatusをlosslessにprojectionする。

維持対象:

```text
result_id
execution_id
stage_execution_id
result_type
schema_version
analytical/scientific status
summary
payload
diagnostics
warnings
created_at
```

generic `PASS` / `DIAGNOSTICS_RESULT`へ圧縮しない。

---

# 14. Predictive Artifact Read Projection

Product-facing:

```text
GET /projects/{project_id}/executions/{execution_id}/artifacts
```

はcanonical Artifact metadataを読む。

Phase Aで追加したtyped Predictive Artifact semanticsをlosslessにprojectionする。

少なくとも:

```text
artifact_id
execution_id
stage_execution_id
result association if response exposes it
artifact_type
schema/version metadata
object_key
content_hash
media/content metadata
created_at
```

をcanonical authorityから取得する。

禁止:

```text
FamilyArtifactOrm shadow read
artifact_idとobject_keyの混同
```

---

# 15. Predictive Lineage Read Projection

Product-facing:

```text
GET /projects/{project_id}/executions/{execution_id}/lineage
```

をnew canonical executionで壊さない。

Phase CではG06 lineage authority consolidationを実施しない。

Allowed:

```text
canonical Execution / Result / Artifact IDsをowned IDsとして使い、
現在のapproved persisted lineage projectionを読む
```

Required:

```text
new Predictive canonical executionがFamilyResultOrm /
FamilyArtifactOrmの存在をlineage endpointの前提にしない
```

canonical IDsに関連するlineage edgeが存在しなければempty listは許容する。

禁止:

```text
G06 final typed/generic lineage authority cutover
closure/export projection redesign
legacy lineage wholesale deletion
```

---

# 16. Predictive Cancel Delegation

Product-facing:

```text
POST .../executions/{execution_id}/cancel
```

はG02/G03 canonical lifecycle semanticsへdelegateする。

Required:

```text
target = canonical PREDICTIVE Execution
project/family isolation
canonical cancel transition
canonical StageExecution cancellation semantics preserved
no FamilyExecutionOrm mutation
no FamilyStageExecutionOrm mutation
```

responseを返す場合はcancel後のcanonical Executionをprojectionする。

旧Family lifecycle logicをコピーして二重実装しない。

---

# 17. Predictive Retry Delegation

Product-facing:

```text
POST .../executions/{execution_id}/retry
```

はcanonical retry semanticsへdelegateする。

G02/G03 contract:

```text
same Execution identity
stable StageExecution identities
retry/attempt semantics retained
canonical retry_count / attempt history
```

を維持する。

禁止:

```text
Family Result/Artifactを削除してlegacy executionをQUEUEDへ戻す
Family StageExecution attempt historyを初期化する
new Execution IDをretryとして発行する
```

G04 canonical Result / Artifact ownershipを壊さない。

retry時のResult/Artifact扱いは既存canonical contractに従う。

---

# 18. Predictive Rerun Delegation

Product-facing:

```text
POST .../executions/{execution_id}/rerun
```

はcanonical rerun semanticsを使う。

Required:

```text
base canonical Execution is PREDICTIVE
base belongs to project
new canonical Execution ID
base_execution_id = original canonical Execution ID
analysis_family remains PREDICTIVE
unchanged scientific conditions
revision_kind = RERUN
change_reason = NONE
new canonical StageExecution set
```

Predictive:

```text
analysis_specification_id
execution_plan_id
seed
dataset/view context
```

をbase canonical snapshotから再構成する。

旧FamilyExecutionをbase authorityにしない。

---

# 19. Predictive Revise Delegation

Product-facing:

```text
POST .../executions/{execution_id}/revise
```

はcanonical revise semanticsを使う。

Required:

```text
base canonical Execution
new canonical Execution ID
base_execution_id preserved
analysis_family remains PREDICTIVE
changed dimensions represented truthfully
revision_kind = REVISED when conditions changed
explicit non-empty change_reason when changed
new canonical StageExecution set
```

## 19.1 change_reason

current Predictive revise request surfaceに`change_reason`が存在せず、canonical G02 contractがchanged Executionに明示理由を要求する場合:

**reasonを捏造してはならない。**

必要ならminimal API request extensionとして:

```text
change_reason
```

を追加し、API/frontend contract testを更新する。

禁止:

```text
"Predictive revise"
"User requested revise"
```

等をservice側で自動生成してscientific/audit reasonを偽装すること。

同一条件でrevise endpointが呼ばれた場合の扱いはcanonical revision comparison contractに従う。

---

# 20. Predictive Prefill

Product-facing:

```text
GET .../executions/{execution_id}/prefill
```

はcanonical Execution snapshotをsourceにする。

可能な限り既存response:

```text
base_execution_id
analysis_specification_id
execution_plan_id
seed
revision_context
```

を維持する。

旧 `FamilyExecutionOrm.snapshot_json` をnew executionのsourceにしない。

---

# 21. Historical Legacy Compatibility

G07前なのでold Family source/tableを削除する必要はない。

historical pre-G05 rowsについてread-only compatibilityが本当に必要なら残してよい。

ただし新Product operationと明確に分離する。

```text
new canonical execution ID
    -> canonical authority only

historical legacy execution
    -> explicitly bounded read-only compatibility if retained
```

禁止:

```text
canonical lookup miss
    -> FamilyExecutionOrmへsilent fallback
```

同一ID namespaceで曖昧なdual-read authorityを作らない。

---

# 22. Worker Boundary — Phase C Limit

current `PredictiveWorkflowService`内に残るlegacy:

```text
claim_next()
process_execution()
```

等のhard shutdown / retirementはPhase Dで扱う。

Phase Cでは:

```text
new Product-facing submit/read/mutationがこれらをauthorityとして使わない
canonical worker pathからnew Predictive executionが処理可能
```

ことを確認する。

Phase Cのためにlegacy claim/processを全面削除する必要はない。

ただし新しいcanonical Predictive executionを動かすためにold FamilyExecution shadow rowを作ることは禁止。

---

# 23. Canonical Predictive Worker Compatibility

既にG05 partial implementationでcanonical `ExecutionProcessor` family dispatchが存在する場合、そのactual contractを利用する。

Phase Cでは最低限:

```text
canonical PREDICTIVE Execution
    -> canonical claim
    -> persistent canonical StageExecution
    -> Predictive scientific runner
    -> canonical Result / Artifact
```

への必要なsnapshot/plan/spec informationが揃っていることを確認する。

この確認でproduction defectを発見した場合、Predictive canonical lifecycle成立に必要な修正はPhase C scope内。

ただし:

```text
old worker sourceの全面削除
old claim APIの全面retirement
```

はPhase Dへ残す。

---

# 24. No New Legacy Writes

Phase C implementationにより以下のnew writeを追加してはならない。

```text
FamilyExecutionOrm
FamilyStageExecutionOrm
FamilyResultOrm
FamilyArtifactOrm
```

Product-facing Predictive:

```text
submit
read
cancel
retry
rerun
revise
prefill
```

を成立させる目的でshadow rowを作ってはならない。

---

# 25. Mandatory Automated Tests

Phase C専用testを追加する。

Recommended:

```text
tests/product/test_enh_e4_g05_phase_c_predictive_postgres.py
tests/product/test_enh_e4_g05_phase_c_predictive_api.py
```

actual分割は任意。

既存Predictive test setup/helperを再利用してよい。

testをarchitectureに合わせて弱めない。

旧authorityそのものをassertするobsolete testを変更する場合は:

```text
なぜobsoleteか
どのapproved G05 contractへ置換したか
```

をcheckpoint reportに記録する。

---

# 26. Mandatory Test — DI / API Construction

最優先で以下をtestする。

```text
get_predictive_workflow_service()
PredictiveWorkflowService dependency construction
Predictive workflow endpoint dependency resolution
```

Expected:

```text
TypeErrorなし
canonical lifecycle dependencyが実際にserviceへ接続
```

constructor mismatchを未検出のままPhase C完了にしない。

---

# 27. Mandatory Test — Canonical Predictive Submit

real PostgreSQL上でactual Product-facing pathを通す。

最低限:

```text
Project
DatasetVersion
required research/spec context
Predictive AnalysisSpecification
ExecutionPlan
submit endpoint/service
```

を通して:

```text
ExecutionOrm exists
analysis_family == PREDICTIVE

StageExecutionOrm exists
expected stage plan materialized

FamilyExecutionOrm row with new execution_id == NONE
FamilyStageExecutionOrm rows for new execution_id == NONE
```

をassertする。

さらに:

```text
analysis_specification_id
execution_plan_id
seed
dataset/version/view context
```

がcanonical snapshotから復元可能であること。

---

# 28. Mandatory Test — Predictive Reads

same canonical executionについて:

```text
get_execution
get_stages
list_results
list_artifacts
list_lineage
prefill
```

を検証する。

Result / Artifactが実行後に存在するsurfaceでは、Phase A typed semanticsをassertする。

Fresh DB session / UoWを跨いで検証する。

Negative:

```text
different project -> rejected / EntityNotFound
non-PREDICTIVE canonical Execution -> Predictive surfaceから取得不可
unknown canonical ID -> legacy Family fallbackしない
```

---

# 29. Mandatory Test — Cancel

canonical Predictive Executionに対してcancelし:

```text
canonical Execution status transition
canonical StageExecution semantics
same execution_id
no Family row mutation/new write
```

をassertする。

G02/G03既存testと矛盾しないこと。

---

# 30. Mandatory Test — Retry

canonical failed Predictive Executionに対してretryし:

```text
same execution_id
same StageExecution identity set
retry_count / canonical retry semantics
no legacy Result/Artifact destructive reset
no FamilyExecution write
no FamilyStageExecution write
```

をassertする。

必要なfailure seed/setupはcanonical repository/test helperを使う。

---

# 31. Mandatory Test — Rerun

terminal canonical Predictive Executionからrerunし:

```text
new execution_id != base
base_execution_id == base
analysis_family == PREDICTIVE
revision_kind == RERUN
change_reason == NONE
Predictive specification/plan/seed semantics unchanged
new persistent StageExecution set
no Family execution/stage shadow row
```

をassertする。

---

# 32. Mandatory Test — Revise

terminal canonical Predictive Executionからscientific conditionを変更してreviseし:

```text
new execution_id != base
base_execution_id == base
analysis_family == PREDICTIVE
revision_kind == REVISED
change_reason is non-empty and explicit
changed dimensions truthfully reflected
new StageExecution set
no Family shadow write
```

をassertする。

Negative:

```text
changed revise without required change_reason -> rejected
cross-project base -> rejected
cross-family base -> rejected
```

をcanonical contractに応じて検証する。

---

# 33. Mandatory Test — No Shadow Write Matrix

Phase Cのactual Product-facing operations:

```text
submit
get/read
cancel
retry
rerun
revise
prefill
```

の前後で、対象canonical execution ID群について少なくとも:

```text
FamilyExecutionOrm count
FamilyStageExecutionOrm count
FamilyResultOrm count
FamilyArtifactOrm count
```

にnew shadow rowsが生じないことを検証する。

Phase D/Eのglobal old-table unchanged auditとは別に、Phase C自身がlegacy writeを持ち込んでいないことを証明する。

---

# 34. Regression Requirements

Phase Cでは以下を壊さない。

## Phase A

```text
typed Result / Artifact semantics
schema_version preservation
Result ↔ Artifact association
PostgreSQL round-trip
```

## Phase B

```text
Exploratory canonical Result reads
Exploratory downstream draft
no Exploratory shadow write
```

## G02/G03/G04

```text
canonical Execution lifecycle
StageExecution persistence
Result/Artifact ownership
```

既存Predictive scientific testsについても関連範囲を実行する。

特に:

```text
plan validation
seed contract
predictive scientific runner
existing API response contract
```

を不必要に破壊しない。

---

# 35. Standard PostgreSQL Verification

real PostgreSQL verification entryは唯一:

```bash
scripts/test/run_product_postgres_tests.sh <pytest-path-or-node> [...]
```

を使用する。

最低限、actual pathに合わせて以下を含める。

```text
Phase C Predictive canonical lifecycle tests
Phase C DI/API tests where PostgreSQL-backed
Phase A PostgreSQL tests
Phase B PostgreSQL tests
G04 Result/Artifact PostgreSQL regression
Product PostgreSQL contract
relevant G02/G03 lifecycle PostgreSQL regression
```

example shape:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g05_phase_c_predictive_postgres.py \
  tests/product/test_enh_e4_g05_submission_convergence.py \
  tests/product/test_enh_e4_g05_phase_a_postgres.py \
  tests/product/test_enh_e4_g05_phase_b_exploratory_postgres.py \
  <relevant-g02-g03-g04-postgres-tests> \
  <product-postgres-contract-test>
```

実在するpath/nodeへ調整する。

禁止:

```text
manual docker run
manual DSN
manual psql
manual Alembic
manual external pytest against ad-hoc DB
```

test failureがcorrect testによるproduction defectなら修正して再実行する。

---

# 36. Migration Policy

Expected starting Product migration head:

```text
20260809_product_0010
```

Phase Cはprimarily lifecycle/read adapter convergenceなので:

```text
new migration = NOT REQUIRED by default
```

Phase Aでcanonical Predictive typed semanticsは成立済み。

schema changeが必要と判断した場合:

```text
why existing canonical schema cannot represent approved Predictive semantics
why adapter/snapshot mappingでは不十分か
```

を明示する。

minimal corrective Product migrationのみ許可する。

root legacy migrationを変更しない。

---

# 37. Phase C Completion Criteria

以下を全て`DONE`にする。

```text
[ ] actual Predictive authority inventory completed

[ ] PredictiveWorkflowService DI constructor mismatch resolved
[ ] FastAPI dependency construction PASS

[ ] Predictive Product submit creates canonical Execution
[ ] Predictive submit creates canonical StageExecution
[ ] Predictive submit creates no FamilyExecution shadow row
[ ] Predictive submit creates no FamilyStageExecution shadow row
[ ] Predictive spec/plan/seed context preserved canonically

[ ] Predictive get/list Execution reads canonical authority
[ ] Predictive get_stages reads canonical StageExecution
[ ] Predictive list_results reads canonical Result
[ ] Predictive list_artifacts reads canonical Artifact
[ ] Predictive lineage projection works with canonical owned IDs
[ ] Predictive prefill reads canonical snapshot

[ ] Predictive Result typed semantics preserved
[ ] Predictive Artifact typed semantics preserved
[ ] project isolation enforced
[ ] family isolation enforced
[ ] canonical miss does not silently fall back to Family authority

[ ] cancel delegates canonical lifecycle
[ ] retry delegates canonical lifecycle
[ ] retry preserves Execution identity
[ ] retry preserves StageExecution identity contract
[ ] rerun creates new canonical Execution with base relation
[ ] revise creates new canonical Execution with base relation
[ ] changed revise requires explicit change_reason
[ ] rerun/revise remain PREDICTIVE

[ ] Product-facing Phase C operations add no Family shadow writes

[ ] canonical Predictive worker compatibility demonstrated
[ ] Phase A regression PASS
[ ] Phase B regression PASS
[ ] relevant G02/G03/G04 regression PASS
[ ] relevant Predictive scientific/API regression PASS
[ ] standard PostgreSQL runner PASS
[ ] git diff --check PASS

[ ] Phase C implementation checkpoint commit created
[ ] Phase C checkpoint report created
[ ] Phase C report initial commit recorded
```

---

# 38. Phase C Implementation Checkpoint Commit

production source + automated testsが完成し、required verification PASS後にimplementation checkpoint commitを作成する。

Suggested message:

```text
E4-G05 Trial 01 Phase C implementation complete
```

checkpoint commitには原則:

```text
Phase C production source
Phase C tests
minimal corrective migration if required
```

を含める。

Phase C checkpoint reportはこのcommitの**後**に作る。

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
Phase checkpoint implementation commit
```

としてreportへ書く。

---

# 39. Phase C Checkpoint Report

実行結果をinstruction fileへ追記しない。

以下へ出力する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G05/Trial01/
E4-G05_01_PhaseC_implementation_checkpoint_report.md
```

Gate-level final report:

```text
20_implementation_reports/G05/
E4-G05_01_implementation_completion_report.md
```

はまだ作成しない。

---

# 40. Phase C Checkpoint Report Format

以下のfield/sectionを省略しない。

```text
# E4-G05 Trial 01 Phase C Implementation Checkpoint Report

- Project
- Enhancement
- Gate
- Trial
- Phase
- Phase Status: PHASE_C_COMPLETE | DESIGN_BLOCKED
- Branch
- Phase baseline implementation checkpoint
- Phase starting commit
- Phase checkpoint implementation commit
- Report commit
- Migration head
- Started at
- Finished at

## 1. Input
- Phase implementation instruction
- Previous phase checkpoint/report

## 2. Starting Authority Inventory
- submit
- execution read
- stage read
- result read
- artifact read
- lineage read
- cancel/retry/rerun/revise/prefill
- worker claim/process

## 3. Scope Implemented

## 4. Files Changed
### Added
### Modified
### Deleted

## 5. Implementation Details

## 6. Automated Test Code Added / Changed

## 7. Migration

## 8. Changes to Passed Gates / Earlier G05 Phases

## 9. Known Limitations / Remaining G05 Work

## 10. Explicit Out-of-Scope Work

## 11. Git Evidence
- git rev-parse HEAD
- git status --short
- diff stat

## 12. Phase Verification Evidence
- exact commands
- exact complete standardized PostgreSQL runner command
- exit codes
- passed/failed/skipped counts
- raw evidence paths if produced
- tested implementation checkpoint SHA/state
- expected vs actual
- Facts
- Interpretation

## 13. No-Legacy-Write Evidence
- operation matrix
- old Family table before/after evidence
- canonical IDs tested

## 14. Next-Phase Handoff
- Next phase: Phase D
- Ready for Phase D: YES / NO
- Gate READY_FOR_TEST: NO

## 15. Design Block
- Contradiction
- Observed facts
- Impact
- Why permitted implementation choices cannot solve it
- Decision required
```

値がないfieldは削除せず:

```text
N/A
NONE
NOT_RUN
UNKNOWN
```

を使う。

Substantive test success does not waive report-format compliance.

---

# 41. Report Commit Metadata Procedure

Git commit SHAは自分自身のfile contentへ事前記入できないため、以下の手順を使う。

1. Phase C implementation checkpoint commitを先に作る。
2. reportを作成し、その時点では:

```text
Report commit: PENDING
```

とする。
3. reportをcommitする。

Suggested message:

```text
E4-G05 Trial 01 Phase C checkpoint report
```

4. そのreport initial commit SHAを取得する。

```bash
git rev-parse HEAD
```

5. reportの:

```text
Report commit: PENDING
```

を、その**initial report commit SHA**へ置換する。
6. metadata correctionを別commitする。

Suggested message:

```text
E4-G05 Trial 01 Phase C report metadata
```

これにより`Report commit`は「reportを最初にrepositoryへ導入したcommit」を意味する。

report metadata commit自身のSHAを同じfileへ自己参照させる必要はない。

---

# 42. Phase C Does NOT Include

今回進めない。

```text
Phase D:
legacy Predictive claim_next/process_execution hard shutdown
legacy Exploratory worker authority hard shutdown
remaining old lifecycle method reachability audit
global old-write authority shutdown
canonical failure -> no old fallback audit
full runtime negative matrix

Phase E:
Causal/Exploratory/Predictive final Golden Paths
cross-family convergence audit
TD-001 closure
TD-002 closure
TD-003 closure
TD-004 handoff record
G05 final implementation completion report
READY_FOR_TEST
fixed final G05 implementation SHA

G06:
lineage authority final consolidation

G07:
legacy source/table retirement/archive
```

---

# 43. Allowed Stop Conditions

今回turnを終了してよいのは以下のみ。

## PHASE_C_COMPLETE

以下を全て満たす。

```text
all Phase C completion criteria DONE
standard PostgreSQL verification PASS
Phase C implementation checkpoint commit created
Phase C checkpoint report created
report initial commit SHA recorded
```

最後に:

```text
PHASE_C_COMPLETE
Implementation Checkpoint SHA: <full SHA>
Report Commit SHA: <full SHA>
Report: docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G05/Trial01/E4-G05_01_PhaseC_implementation_checkpoint_report.md
```

を報告して停止する。

## DESIGN_BLOCKED

approved G02/G03/G04/G05 contractとactual Predictive scientific semanticsの間に、adapter / canonical snapshot mapping / minimal Product extensionでは解消不能なsemantic contradictionがある場合のみ。

必ず:

```text
exact contradiction
actual source/schema evidence
why permitted implementation choices cannot resolve it
required human architecture decision
```

をreportへ記録する。

---

# 44. Stop Reasons NOT Accepted

以下を理由に途中停止してはならない。

```text
DI constructor mismatchを発見した
Predictive serviceがまだFamily ORMを使っている
canonical submit adapterが必要
response projectionが必要
prefill projectionが必要
change_reason field追加が必要
canonical repository/query追加が必要
testがFAILした
migrationが必要になった
existing Predictive test修正が必要
Phase D/Eが未完了
G05全体が未完了
final implementation reportが未作成
```

これらはPhase C内で解決または明示的に検証する対象である。

---

# 45. Final Instruction

E4-G05 Trial 01 Phase C — Predictive canonical lifecycle/read convergenceを:

```text
PHASE_C_COMPLETE
```

まで完遂せよ。

Phase C完了後、このrunではPhase Dへ進まないこと。
