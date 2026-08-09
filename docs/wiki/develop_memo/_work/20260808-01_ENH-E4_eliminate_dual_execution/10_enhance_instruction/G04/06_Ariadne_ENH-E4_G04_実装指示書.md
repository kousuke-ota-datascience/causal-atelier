# Ariadne ENH-E4 E4-G04 実装指示書

* Project: Ariadne / causal-atelier
* Enhancement: ENH-E4 eliminate dual execution
* Branch: `refactor/ariadne_mvp_e4`
* Gate: `E4-G04`
* Gate name: Result / Artifact ownership boundary
* Trial: `01`
* Baseline ref: `14bc705` — G03 PASS後のCurrent Architecture Control Sheet追加commit
* Baseline full SHA: **作業開始時に `git rev-parse 14bc705^{commit}` で確定してreportへ記録する**
* Expected starting Product migration head: `20260809_product_0008`
* Expected next Product migration revision: `20260809_product_0009`（actual headを開始時に再確認する）
* G02 status: `PASS`
* G03 status: `PASS`
* Test PostgreSQL Infrastructure: `PASS_READY_FOR_G03` をG04以降も標準基盤として継続使用
* Trial ID format: 2-digit zero-padded decimal (`01`–`99`)
* Test Item ID format: 3-digit zero-padded decimal (`001`–`998`; `000` reserved; `999` Gate Decision)

---

# 1. Source of Truth

本書は **E4-G04 Trial 01 Coding Agentが従うGate-local implementation contract** である。

Coding Agentは、本書に明示された範囲だけを実装し、本書にないarchitecture decisionを独自に拡張しない。

G04で参照してよい正本は以下。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
00_ENH-E4_Current_Architecture_Control_Sheet.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/architecture_review/
06_target_architecture_decision_record_result.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/architecture_review/
07_gate_decomposition_result.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
30_test_report/G03/
E4-G03_02_999_gate_decision.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G03/
E4-G03_02_implementation_completion_report.md
```

実装事実についてはbaseline/current branch上のactual source、Product migration、automated testsを使用する。

本書とcurrent sourceの間に、単なる実装選択では解消できないsemantic contradictionがある場合は、勝手に要件を弱めず `DESIGN_BLOCKED` とする。

---

# 2. Report Format Is Part of the Contract

G03 Trial 01で発生したreport format逸脱をG04以降で再発させない。

## 2.1 Implementation Completion Report specification

Coding Agentは以下を**必ず実物参照**する。

```text
docs/wiki/develop_memo/_work/
agentic_enhancement_workflow_template_complete/
20_implementation_reports/
README.md

docs/wiki/develop_memo/_work/
agentic_enhancement_workflow_template_complete/
20_implementation_reports/
TEMPLATE_implementation_completion_report.md
```

enhancement-wide detail ledgerを更新する場合:

```text
docs/wiki/develop_memo/_work/
agentic_enhancement_workflow_template_complete/
20_implementation_reports/
TEMPLATE_implementation_report_detail.md
```

も参照する。

## 2.2 Strict compliance

Implementation Completion Reportはrepository-defined template/specificationへ準拠しなければならない。

Coding Agentは以下をしてはならない。

```text
required sectionを省略する
required sectionを勝手にmergeする
required fieldをprose summaryで代替する
独自の短縮report formatを採用する
required fieldを空欄にする
Gate PASS/FAIL/BLOCKEDをCoding Agent自身が判定する
```

値が存在しない場合もfieldを削除せず、仕様に従い:

```text
N/A
NONE
NOT_RUN
UNKNOWN
```

を使用する。

## 2.3 Completion condition

`READY_FOR_TEST` を宣言する前に、Coding Agentはreport template/specificationと**field-by-field compliance check**を行う。

**Substantive implementation/test success does not waive report-format compliance.**

Report format不適合のまま `READY_FOR_TEST` としてはならない。

---

# 3. Coding Agent Role

Coding Agentの責務:

1. branch / starting commit / migration head / G03 PASS stateを確認する。
2. current Result / Artifact implementationをactual sourceで再確認する。
3. G02/G03 passed contractを保全する。
4. G04 scopeだけを実装する。
5. explicit `ExecutionResult` / `StageResult` semantic level contractを導入する。
6. Result identity / ownership / cardinality contractをpersistentに実装する。
7. Product Artifact metadata ownership authorityを一つのcanonical service/repository contractへ集約する。
8. physical bytesを`ArtifactStorePort`の背後に維持する。
9. metadata transactionとphysical storeの非atomic性に対するcompensation/reconciliation semanticsを実装する。
10. `object_key`をsemantic Result/Artifact identityとして使用できないcontractを実装する。
11. downstream reuseをtyped Product IDsへ限定するG04 contractを実装する。
12. Artifact-only outputの許可/拒否をfamily workflow contractとして明示する。
13. E4-G04-AC-001〜005を直接検証するautomated test codeを追加する。
14. Product migrationを追加する。
15. standardized Test PostgreSQL infrastructureでself-checkを行う。
16. implementation commitを固定する。
17. Gate-local Implementation Completion Reportをtemplate準拠で作成する。
18. enhancement-wide implementation detail ledgerを更新する。
19. `READY_FOR_TEST` または `DESIGN_BLOCKED` で停止する。

Coding AgentはGate Decisionを行わない。

---

# 4. Prohibited Work

## 4.1 G05 scope — Product Execution Convergence

G04では以下を完了させない。

```text
Causal / Exploratory / Predictive全submission pathのcanonical cutover
old Causal/Family execution new-write pathの全面停止
old family result/artifact pathの全面削除
TD-001 closure
TD-002 closure
TD-003 closure
Product API / worker / CLIの全route convergence
```

G05が唯一のProduct Execution Convergence Gateである。

## 4.2 G06 scope — Lineage

禁止:

```text
lineage authority final cutover
structural generic dual-write全面除去
closure/export redesign
generic-only relation allowlist最終化
lineage source-class final convergence
```

G04でtyped Result/Artifact ownership FKを追加することは許可されるが、それを理由にG06 lineage writer/read projectionを先取りしない。

## 4.3 G07/G08 scope

禁止:

```text
legacy runtime/source deletion
legacy CLI retirement
root migration deletion
final clean bootstrap
final architecture audit
open transition debt全閉鎖
```

## 4.4 Scientific scope

禁止:

```text
scientific algorithm redesign
scientific payload semantics redesign
estimator/discovery/preprocessing変更
family outputの科学的意味の統一
```

Result ownershipを統一するためにscientific payloadを一つの形へ潰してはならない。

## 4.5 GenericExecutor

GenericExecutorへ以下を戻してはならない。

```text
Result persistence
Artifact metadata persistence
ArtifactStore write coordination
DB/UoW commit
canonical retry policy
claim / lease
lineage persistence
```

G03 passed contractを保全する。

## 4.6 Migration / infrastructure

禁止:

```text
root legacy migration chain変更
root legacy migrationをG04 verificationで実行
G02型manual PostgreSQL verification再導入
compose.test.yaml / Dockerfile.test等の標準基盤再設計
development DB reset
```

## 4.7 Unrelated working-tree artifact

既知のunrelated artifact:

```text
deploy/.nfs000000000076202f00000088
```

は:

```text
stageしない
restoreしない
deleteしない
recreateしない
implementation commitへ含めない
```

---

# 5. Baseline / Current State

## 5.1 Gate state

開始時:

```text
E4-G01 = PASS
E4-G02 = PASS
E4-G03 = PASS
E4-G04 = NOT_STARTED
```

G04実装開始後:

```text
E4-G04 = IN_PROGRESS
```

## 5.2 Baseline ref

Expected baseline:

```text
14bc705
```

開始時に:

```bash
git branch --show-current
git rev-parse HEAD
git rev-parse 14bc705^{commit}
git status --short
git log --oneline -12
```

を実行する。

branchが:

```text
refactor/ariadne_mvp_e4
```

以外なら作業しない。

`14bc705`以降にproduction/test/migration changeがある場合はdiffを確認し、G04開始点として妥当かreportへ記録する。

## 5.3 Current migration

Expected:

```text
20260809_product_0008
```

G04ではResult/Artifact persistent contractにschema changeが必要なため、**Product migration追加はMUST**。

Baseline上のexpected next revision:

```text
20260809_product_0009
```

actual headが異なる場合、そのactual headのdirect childとして作成する。

## 5.4 Current Result facts

baselineではcanonical Product domain `Result` は概ね:

```text
result_id
execution_id
result_type
scientific_status
summary_json
payload_json
diagnostics_json
warning_json
created_at
```

を持つ。

不足しているG04 semantics:

```text
explicit Result semantic level
canonical StageExecution association
level/cardinality validation
cross-family canonical Result persistence
```

current persistenceには少なくとも:

```text
product_result
product_family_result
```

が別authorityとして存在する。

`product_result`はexecution-scoped。

`product_family_result`はexecution + stage scopedであり、別table / repository styleを持つ。

## 5.5 Current Artifact facts

canonical Product `Artifact` は概ね:

```text
artifact_id
project_id
execution_id?      # current domainではoptional
result_id?
artifact_type
object_key
content_hash
media_type
size_bytes
metadata_json
created_at
```

current persistenceには:

```text
product_artifact
product_family_artifact
```

が存在する。

family artifactは:

```text
execution_id
stage_execution_id
result_id optional
```

を持ち、Resultなしでも存在可能。

## 5.6 Current physical store

`ArtifactStorePort`は既にshared physical storage boundaryとして存在する。

current `ArtifactService.read_verified()`は:

```text
artifact_id
  ↓ metadata repository
object_key
  ↓ ArtifactStorePort.retrieve()
bytes
  ↓ sha256 verify
```

という方向で読み出す。

G04はこのstorage abstractionを維持し、metadata authorityとphysical storageを混同しない。

## 5.7 Current canonical repository surface

canonical Product ports/UoWには既に:

```text
ResultRepository
ArtifactRepository
UnitOfWork.results
UnitOfWork.artifacts
```

が存在する。

G04ではこれらをcanonical Result/Artifact ownership semanticsへ拡張することを優先し、family別second canonical repositoryを新設しない。

---

# 6. Gate Objective

E4-G04 Objective:

> `ExecutionResult` / `StageResult` semantic levelと、一つのProduct Artifact metadata ownership boundaryを成立させる。

Architecture After Gate:

```text
Canonical Execution
    │
    ├─ persistent StageExecution
    │
    ├─ Result ownership contract
    │    ├─ ExecutionResult
    │    └─ StageResult
    │
    └─ Artifact metadata ownership contract
         ├─ mandatory canonical output ownership
         ├─ optional StageExecution association
         ├─ optional Result association
         ├─ artifact_id = semantic identity
         └─ object_key = physical locator only
                  │
                  v
            ArtifactStorePort
```

Application authority:

```text
canonical output ownership/application service
    ├─ validates Result level/cardinality
    ├─ validates Execution/Stage ownership
    ├─ creates/persists Result metadata
    ├─ stores Artifact bytes via ArtifactStorePort
    ├─ persists Artifact metadata
    ├─ links Result / Stage / Execution
    └─ compensates/reconciles partial physical/DB failure
```

GenericExecutorはこのauthorityを持たない。

---

# 7. Canonical Result Contract

## 7.1 Explicit semantic level

Resultにはscientific `result_type`とは独立したsemantic levelを導入する。

Required logical values:

```text
EXECUTION_RESULT
STAGE_RESULT
```

Domain enum/class namingはrepository conventionに合わせてよいが、persistent serialized contractはこの二つを明確に区別できなければならない。

禁止:

```text
result_typeから暗黙推定する
stage_execution_id nullableだけで意味を推測する
CausalだからExecutionResult、FamilyだからStageResultとfamilyだけで暗黙決定する
```

## 7.2 Minimum Result ownership fields

canonical Result logical contract:

```text
result_id
execution_id
result_level
stage_execution_id optional/conditional
result_type
scientific/analytical status
summary/payload/diagnostics/warnings
created_at
```

existing family `schema_version`等、現在保持しているsemantically relevant informationをG04統合で失ってはならない。

必要ならcanonical fieldまたは明示的metadataとして保持する。

## 7.3 Ownership invariants

Every canonical Result:

```text
execution_id != NULL
```

`EXECUTION_RESULT`:

```text
stage_execution_id MUST be NULL
```

`STAGE_RESULT`:

```text
stage_execution_id MUST NOT be NULL
```

さらにStageResultのstageは:

```text
StageExecution.execution_id == Result.execution_id
```

でなければならない。

wrong-execution StageExecution linkをservice/database contractのどちらか一方だけに依存せず、可能な限りdomain/service + persistence testで拒否する。

## 7.4 Stable semantic identity

Result identity:

```text
result_id
```

のみをsemantic Product Result IDとする。

以下をResult identityとして使用しない。

```text
object_key
content_hash
stage_key
payload hash
family Result table row locator
```

## 7.5 Result level != scientific result type

例:

```text
result_level = EXECUTION_RESULT
result_type  = TREATMENT_EFFECT_RESULT

result_level = STAGE_RESULT
result_type  = <family/scientific result kind>
```

semantic levelとscientific kindを一つのenumへ潰さない。

## 7.6 Cardinality contract

E4-REQ-017のため、cardinalityは明示contractを持つ。

最低限、family/workflow output contractが以下を決定できること。

```text
which stage/output may emit:
    zero Result
    one Result
    multiple Results

allowed Result level
required / optional Result
allowed Result types
artifact-only output allowed?
```

Coding Agentはcurrent Causal / Exploratory / Predictive workflow definitionsをinventoryし、暗黙の`if family == ...`散在ではなく、共通contract/registry/typed specificationへ表現する。

**具体的なscientific payloadを変更してcardinalityを揃えてはならない。**

## 7.7 Artifact-only semantics

Artifactだけを生成しResultを生成しないstageは、family/output contractが明示的に:

```text
artifact_only_allowed = true
```

相当を宣言した場合のみ許可する。

Resultが必須のoutput contractではArtifact-onlyを拒否する。

「ResultがたまたまNoneだったのでArtifactだけ残った」という状態を許可しない。

---

# 8. Canonical Artifact Metadata Contract

## 8.1 One metadata ownership authority

G04以降のcanonical output pathでは、Result/Artifact metadataをcreate/persist/link/deleteするapplication ownership boundaryを一つにする。

禁止:

```text
Causal用canonical Artifact writer
Exploratory用canonical Artifact writer
Predictive用canonical Artifact writer
```

という三authority化。

family adapterはoutput descriptorを生成できるが、persistent ownershipは共通service/repository境界へ渡す。

## 8.2 Minimum output Artifact fields

canonical execution-output Artifact metadata logical contract:

```text
artifact_id
project_id
execution_id
stage_execution_id optional
result_id optional
artifact_type / artifact kind
schema/version where applicable
object_key
content_hash
media_type
size_bytes
metadata_json
created_at
```

## 8.3 Semantic identity vs locator

```text
artifact_id = semantic Product Artifact identity
object_key  = physical ArtifactStore locator
content_hash = integrity snapshot
```

これらを混同しない。

`object_key`がuniqueであることは許可されるが、semantic identityにはならない。

## 8.4 Ownership validation

execution-owned output Artifactはcanonical Executionへtyped associationを持つ。

If `stage_execution_id` exists:

```text
StageExecution.execution_id == Artifact.execution_id
```

If `result_id` exists:

```text
Result.execution_id == Artifact.execution_id
```

StageResultへlinkする場合は、ResultのstageとArtifactのstageが矛盾しないこと。

If `result_id` is NULL:

```text
family/output contract must explicitly allow artifact-only output
```

## 8.5 Existing non-execution source artifacts

Current `product_artifact` is also used by Product resources such as DatasetVersion source references.

G04はscientific execution output ownershipを統一するGateであり、unrelated dataset ingestion semanticsを壊してはならない。

Therefore:

1. **Execution-output Artifact**は上記canonical ownership contractを満たす。
2. existing pre-analysis/source Artifactが同一metadata authority/tableを共有する場合、その既存typed ownershipを暗黙にexecution outputへ偽装しない。
3. nullable `execution_id`だけで「何でもあり」にしない。
4. 必要なら明示的artifact ownership role/scopeを導入し、execution-outputとsource/input resourceを区別する。
5. この区別を行うためにDatasetVersion/ingestionの意味を再設計してはならない。
6. Target ADR-007とexisting source-artifact semanticsを両立できない実証的矛盾を発見した場合は `DESIGN_BLOCKED` とし、勝手にsource artifactを削除/移行しない。

この互換境界はE4-CON-010を守るためのものであり、execution-output ownershipを弱めるための抜け道ではない。

---

# 9. Canonical Output Ownership Service

## 9.1 Required boundary

G04では、Result/Artifact persistent ownershipを一つのapplication boundaryへ集約する。

Exact class nameは任意。

例:

```text
OutputOwnershipService
ResultArtifactService
ExecutionOutputService
```

等。

重要なのはclass名ではなくauthority。

## 9.2 Responsibilities

このservice/aggregate boundaryだけがcanonical outputについて:

```text
Result level/cardinality validation
Execution/Stage ownership validation
Result metadata creation
Artifact bytes store orchestration
Artifact metadata creation
Result↔Artifact link
Artifact-only validation
metadata commit
physical compensation
delete/reconciliation operation
```

を所有する。

## 9.3 Forbidden owners

以下はcanonical Result/Artifact ownershipを持たない。

```text
GenericExecutor
scientific runner
family-specific persistence adapter
CLI direct DB writer
ArtifactStorePort
lineage writer
```

ArtifactStorePortはbytesをstore/retrieve/deleteするphysical portであり、Product ownershipを判断しない。

## 9.4 UoW

canonical metadata persistenceはProduct UoW:

```text
uow.results
uow.artifacts
```

または同等のcanonical repositoriesを使う。

family-specific second UoWを作らない。

---

# 10. Physical ArtifactStore Compensation Contract

DB transactionとArtifactStoreは同一transactionではない。

G04ではこの非atomicityを隠さず、明示的compensation/reconciliation contractを実装する。

## 10.1 Create/write minimum sequence

推奨logical sequence:

```text
validate Result/Artifact ownership and output contract
        ↓
prepare Result / Artifact semantic IDs
        ↓
write physical artifact bytes via ArtifactStorePort
        ↓
collect object_key/hash/size/media metadata
        ↓
persist Result + Artifact metadata in one Product UoW
        ↓
commit
```

Exact internal orderingは、以下のfailure invariantsを満たす限り変更可能。

## 10.2 Store failure before metadata commit

If physical store write fails:

```text
no committed Artifact metadata for failed object
no committed Result metadata that falsely claims complete output
already-written sibling objects are compensating-deleted where this operation is atomic-as-a-group
UoW rolls back
failure is surfaced
```

Resultがphysical Artifactに依存しない独立科学Resultである場合の扱いはoutput contractで明示する。事故的partial successを許可しない。

## 10.3 DB commit failure after physical store success

If physical write succeeds but DB commit fails:

```text
stored physical object(s) are compensating-deleted
metadata transaction remains uncommitted/rolled back
failure is surfaced
```

## 10.4 Partial multi-artifact write

N個のArtifactを一操作で所有する場合、途中store failure時:

```text
written subset is known
cleanup targets are deterministic
metadata cannot claim unwritten members
```

## 10.5 Compensation failure

physical delete/cleanup itselfが失敗した場合:

```text
silently success扱いしない
orphan locator/object_keyをstructuredに保持/返却できる
reconciliation対象を人間/サービスが再試行可能
```

最低限:

```text
object_key
artifact semantic ID if allocated
content hash if known
operation/execution context
```

を再調停可能にする。

必ずしも新しいdistributed transaction infrastructureを導入する必要はない。

## 10.6 Delete semantics

canonical ownership serviceがmetadata deleteを扱う場合:

```text
physical delete
metadata delete
failure compensation/reconciliation
```

のorderとfailure contractを明示しtestする。

G04ではlegacy retention policy全体を再設計しない。

---

# 11. Typed Downstream Reuse Contract

## 11.1 Result reuse

Result reuseは:

```text
Result ID
+
typed role/context
```

を使用する。

禁止:

```text
object_keyをinput_result_id相当として渡す
payload hashをResult identityとして渡す
family Result rowをuntyped stringでCausalへ渡す
```

## 11.2 Artifact reuse

Artifact reuseは:

```text
Artifact ID
+
metadata lookup
+
hash/integrity validation where required
```

を使用する。

physical `object_key`はrepository/application境界の内部locatorである。

## 11.3 Existing typed resources

以下は既存typed domain referencesとして維持する。

```text
DatasetVersion ID
GraphVersion ID
Result ID
Artifact ID
```

## 11.4 Scope boundary

G04はtyped reuse contractを成立させる。

全UI/API/worker routeをG04でcutoverする必要はない。G05 convergence scopeである。

しかしG04で新設するcanonical API/serviceはobject_keyをsemantic downstream inputとして受け付けてはならない。

---

# 12. G03 Stage Output Boundary

G03 passed contractを利用し、G04ではpersistent StageExecutionからcanonical output ownerへ接続する。

Required logical flow:

```text
StageExecution / canonical orchestration
        ↓
detached runner outcome / output descriptors
        ↓
canonical output ownership service
        ├─ Result?
        └─ Artifact(s)?
        ↓
persistent metadata + ArtifactStore
```

GenericExecutorはdetached outcomeまで。

G04 serviceはStageExecution ownershipをvalidateする。

Stage `output_binding`はG03 orchestration metadataであり、G04 Result/Artifact metadata authorityの代替ではない。

---

# 13. Transition Debt

## 13.1 Existing

Keep OPEN:

```text
E4-TD-001
old Causal/Family new Execution writes
Exit: G05

E4-TD-002
old stage persistence / ephemeral behavior
Exit: G05
```

## 13.2 Introduce in G04

```text
E4-TD-003
Introduced: G04
State: OPEN until G05
Temporary authority:
    old Causal/Family Result/Artifact metadata ownership paths that still exist
    only because Product path convergence is deferred to G05
Exit criterion:
    all new Product outputs use canonical Result/Artifact ownership boundary
    and old metadata owners accept no new Product writes
```

## 13.3 Critical interpretation

`TD-003`は**same request dual-writeの許可ではない**。

禁止:

```text
one output request
  ├─ canonical Result/Artifact table write
  └─ old family Result/Artifact table write
```

を恒常的transition mechanismにすること。

G04では:

```text
canonical G04 path → canonical owner only
old non-converged path → bounded old owner, tracked as TD-003
```

というwrite-boundary separationを使う。

G05でold new-write authorityを停止しTD-001〜003を閉じる。

---

# 14. Product Migration Contract

## 14.1 Product migration MUST

Expected:

```text
previous head: 20260809_product_0008
new head:      20260809_product_0009
```

actual headを確認してdirect childを作成する。

## 14.2 Required schema outcome

migration後、canonical Result persistenceは少なくとも:

```text
explicit result_level
canonical execution FK
conditional StageExecution association
level/stage consistency support
stable result_id
required scientific payload/status preservation
query indexes / constraints
```

を持つ。

canonical execution-output Artifact metadataは少なくとも:

```text
artifact_id semantic identity
canonical execution association
optional stage association
optional result association
object_key physical locator
hash/media/size/metadata
ownership consistency
artifact-only semantics support
```

を持つ。

## 14.3 Physical schema choice

Coding Agentはcurrent repository conventionに合わせ、以下のいずれかのminimal designを採用してよい。

```text
A. existing canonical product_result/product_artifactを
   explicit level/stage/ownership contractへevolveする

B. explicit canonical Result/Artifact persistenceを新設し、
   current tablesをTD-003 transitional boundaryへ置く
```

ただし:

```text
current Causal tableをsemantic変更なしでそのままcanonicalと宣言
current Family tableをsemantic変更なしでそのままcanonicalと宣言
ExecutionResult/StageResultを区別しないone-row semantics
```

は禁止。

選択したphysical designと理由をImplementation Completion Reportに記録する。

## 14.4 No historical backfill requirement

pre-production clean rebuild policyのため、old family rowsからcanonical rowへのhistorical data migrationはG04必須ではない。

必要性がないのにdual-read/backfill infrastructureを追加しない。

## 14.5 Product only

verification:

```text
alembic -c alembic_product.ini upgrade head
```

をrepository-managed PostgreSQL runner経由で使用する。

root legacy chainは使用しない。

---

# 15. Required Automated Test Coverage

Coding AgentはE4-G04 ACを直接証明するautomated test codeを実装する。

Test Agentが後から「source inspectionでたぶん正しい」と補完する前提は禁止。

Recommended files:

```text
tests/product/test_enh_e4_g04_result_artifact_contract.py
tests/product/test_enh_e4_g04_result_artifact_postgres.py
tests/product/test_enh_e4_g04_artifact_compensation.py
tests/product/test_enh_e4_g04_typed_reuse.py
```

実際のsplitは任意。

## 15.1 AC-001 — Result level / cardinality

Must prove:

```text
ExecutionResult persists with explicit EXECUTION_RESULT
StageResult persists with explicit STAGE_RESULT
ExecutionResult rejects stage_execution_id
StageResult requires stage_execution_id
StageResult stage belongs to same execution
result_level and result_type are distinct
family/workflow cardinality contract is explicit
```

少なくともpersistent schema/domain validationをreal PostgreSQLで1系統以上検証する。

## 15.2 AC-002 — typed canonical Execution ownership

Must prove real PostgreSQL round-trip:

```text
Result.execution_id -> canonical product Execution
StageResult.stage_execution_id -> canonical persistent StageExecution
Artifact.execution_id -> same canonical Execution
Artifact.stage_execution_id optional but if present same Execution
Artifact.result_id optional but if present same Execution
```

wrong execution/stage/result ownershipをnegative testする。

Causal/Exploratory/Predictiveでcanonical output contractが表現可能であることをtestする。

G05 route convergenceまでは要求しない。

## 15.3 AC-003 — store/metadata compensation

Must behavior-test:

```text
store failure before metadata commit
DB commit failure after store success
partial multi-artifact store failure
compensation cleanup
compensation cleanup failure/reconciliation visibility
```

metadata durabilityを確認するケースはreal PostgreSQLを使う。

physical storeはtest double / deterministic local storeを使用してfailure injectionしてよい。

## 15.4 AC-004 — object_key cannot be semantic identity

Must negative-test:

```text
downstream Result reuse API does not accept object_key as Result ID
Artifact semantic lookup uses artifact_id
object_key-only reference cannot satisfy ownership
hash alone cannot satisfy semantic identity
```

existing `input_result_id` / typed domain pathsがResult ID contractを維持することを確認する。

## 15.5 AC-005 — Artifact-only family contract

Must prove:

```text
every canonical family/workflow output contract has explicit decision
```

and at least:

```text
one allowed artifact-only case succeeds if current workflow supports it
one disallowed artifact-only case is rejected
```

もしcurrent workflowsをinventoryした結果artifact-only allowed caseが本当に存在しないなら、推測で作らず全contractがexplicitly falseであることを証明し、Gate ACの「許可/拒否が決定される」を満たす。

## 15.6 Report mapping

Implementation Completion Reportに:

```text
AC-001 -> exact pytest nodes
AC-002 -> exact pytest nodes
AC-003 -> exact pytest nodes
AC-004 -> exact pytest nodes
AC-005 -> exact pytest nodes
```

を記載する。

---

# 16. Passed-Gate Regression

G04はResult/Artifact integrationのためExecution/Stage近傍へ変更が及び得る。

Mandatory:

```text
G02 canonical Execution regression
G03 persistent StageExecution regression
G03 GenericExecutor non-authority regression
PostgreSQL contract
```

少なくとも:

```text
tests/product/test_enh_e4_g02_canonical_execution.py
tests/product/test_enh_e4_g03_*.py
tests/product/test_postgres_contract.py
```

からactual affected required nodesを実行する。

G04 testを通すためG02/G03 assertionを弱めてはならない。

---

# 17. Standardized Test PostgreSQL Infrastructure

real PostgreSQLを必要とするG04 self-checkは唯一:

```bash
scripts/test/run_product_postgres_tests.sh <pytest-path-or-node> [pytest-options]
```

を使用する。

Example:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g04_result_artifact_postgres.py \
  tests/product/test_enh_e4_g04_artifact_compensation.py \
  tests/product/test_postgres_contract.py \
  tests/product/test_enh_e4_g02_canonical_execution.py \
  tests/product/test_enh_e4_g03_acceptance_postgres.py
```

actual test pathsに合わせる。

禁止:

```text
manual docker run
Docker network IP調査
127.0.0.1 / 172.17.0.1 workaround
manual DSN export
manual psql reset
manual alembic
manual pytest against hand-wired PostgreSQL
```

Agent環境からDockerへアクセス不能ならenvironment limitationとして記録し、product FAIL扱いしない。

ただしrequired automated test code自体は省略しない。

---

# 18. Allowed Change Areas

G04に必要な範囲:

```text
src/ariadne/product/domain/result.py
src/ariadne/product/domain/artifact.py
src/ariadne/product/domain/enums.py

src/ariadne/product/application/
    result/output/artifact ownership services as needed

src/ariadne/product/ports/repositories.py
src/ariadne/product/ports/unit_of_work.py
src/ariadne/product/ports/artifact_store.py
    only contract-preserving extensions if needed

src/ariadne/product/persistence/orm_models.py
src/ariadne/product/persistence/repositories.py
src/ariadne/product/persistence/unit_of_work.py

src/ariadne/product/workflow/
    output contract/specification only as needed

family workflow adapters
    only output ownership/cardinality descriptor boundary

product_migrations/

tests/product/

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G04/

20_implementation_reports/
ENH-E4_implementation_report_detail.md
```

必要なfileだけ変更する。

---

# 19. Forbidden Change Areas

原則変更禁止:

```text
legacy runtime roots
root legacy migrations
shared scientific algorithms
frontend
auth
unrelated dataset ingestion semantics
lineage writers/readers/closure final authority
CLI architecture
deployment production topology
G03 PostgreSQL test infrastructure
passed G02/G03 instruction/report artifacts
00 Current Architecture Control Sheet
    # G04 PASS後に別工程で更新する。Coding Agentが先に更新しない。
```

---

# 20. Acceptance Criteria

## E4-G04-AC-001

> Resultは`ExecutionResult` / `StageResult` levelを明示する。

PASS requires:

```text
persistent explicit level
level/stage validation
explicit cardinality contract
no semantic inference solely from family/table name
```

## E4-G04-AC-002

> Result/Artifactはcanonical Executionへtyped associationを持つ。

PASS requires:

```text
canonical Execution ownership
StageResult typed StageExecution ownership
Artifact optional Stage/Result links are ownership-consistent
query/reload proves typed association
```

## E4-G04-AC-003

> metadata commitとphysical store failureのcompensationが検証可能である。

PASS requires executable failure-injection evidence.

## E4-G04-AC-004

> `object_key`単体でdownstream ownershipやResult identityを表せない。

PASS requires typed Result/Artifact ID contract and negative object-key test.

## E4-G04-AC-005

> Artifact-only outputの許可/拒否がfamily contractで決定される。

PASS requires explicit family/workflow contract and validation test.

---

# 21. Negative Acceptance Criteria

Any is defect:

```text
Result levelが暗黙
StageResultがstageなしでpersist可能
ExecutionResultがstageへattachされる
StageResult stageとResult executionが不一致
Artifact result/stageとArtifact executionが不一致
object_keyをResult IDとして使える
object_key-only downstream ownershipが成立する
content_hashだけでProduct identityが成立する
GenericExecutorがResult/Artifact metadata persistする
family別canonical metadata ownerを新設する
Artifact-only behaviorがNone accidental pathに依存する
store failureでcommitted orphan metadataが残る
DB failureでcleanupされないobjectが成功扱いされる
compensation failureをsilent successにする
same outputをold+canonical metadataへindefinite dual-writeする
scientific payloadを統一のため再設計する
G05 convergenceを先取りする
G06 lineage cutoverを先取りする
root legacy migrationを変更する
```

---

# 22. Implementation Completion Conditions

`READY_FOR_TEST` only if:

1. explicit Result level implemented.
2. Result level/stage ownership validation implemented.
3. Result cardinality/output contract explicit.
4. one canonical output metadata ownership service/repository boundary exists.
5. Artifact semantic identity distinct from object_key.
6. canonical execution-output Artifact ownership implemented.
7. optional stage/result Artifact links validate ownership consistency.
8. ArtifactStorePort remains physical-only.
9. physical-store/DB compensation implemented.
10. compensation failure is observable/reconcilable.
11. typed downstream Result/Artifact reuse contract implemented.
12. Artifact-only output decision explicit for family/workflow contracts.
13. AC-001〜005 each have automated test nodes.
14. required real PostgreSQL tests exist.
15. G02 regression preserved.
16. G03 regression preserved.
17. GenericExecutor remains non-authority.
18. Product migration added and head verified.
19. TD-001 remains OPEN.
20. TD-002 remains OPEN.
21. TD-003 is recorded OPEN until G05.
22. no G05+ scope crossing.
23. implementation commit fixed.
24. Implementation Completion Report created.
25. enhancement-wide detail ledger updated.
26. **Implementation Completion Report is field-by-field compliant with repository template/specification.**
27. required fields are not omitted/merged/abbreviated.
28. exact self-check commands/results are recorded where performed.
29. unrelated working-tree artifact untouched.

Coding Agent self-check success is not Gate PASS.

---

# 23. Required Outputs

## 23.1 Implementation commit

Create one fixed G04 implementation commit containing:

```text
production source
automated test source
Product migration
```

and no unrelated artifact.

## 23.2 Gate-local Implementation Completion Report

Create:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G04/
E4-G04_01_implementation_completion_report.md
```

The report MUST use the repository template/specification.

Before completion, compare the generated report **line-by-line/field-by-field** against:

```text
agentic_enhancement_workflow_template_complete/
20_implementation_reports/
README.md

agentic_enhancement_workflow_template_complete/
20_implementation_reports/
TEMPLATE_implementation_completion_report.md
```

Status:

```text
READY_FOR_TEST
DESIGN_BLOCKED
```

only.

## 23.3 Mandatory G04 supplemental report content

Template fields must remain intact.

Within them/supplemental section additionally include:

```text
chosen physical Result persistence design
chosen physical Artifact metadata design
Result level serialization values
level/cardinality rule
source/input Artifact compatibility handling
canonical output ownership service
ArtifactStore compensation sequence
compensation failure/reconciliation semantics
typed downstream reuse types
Artifact-only family contract mapping
AC -> exact pytest node mapping
Product migration previous/new head
TD-001/002/003 states
G02/G03 regression commands/results
```

## 23.4 Enhancement-wide detail ledger

Update:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/
ENH-E4_implementation_report_detail.md
```

using repository detail-report specification.

Do not erase prior FAIL/PASS trial history.

---

# 24. Self-check Evidence

Coding Agentが実行したself-checkはGate evidenceではないが、reportへactual command/resultを記録する。

Minimum expected:

```text
pure unit/domain tests
G04 contract tests
standardized PostgreSQL G04 tests
G02/G03 relevant regression
```

For every executed command:

```text
exact command
exit code
passed/failed/skipped count where available
evidence path
tested implementation state/SHA
```

を記録する。

実行していない場合は実行したように書かない。

---

# 25. Git Integrity

Before commit:

```bash
git status --short
git diff --check
git diff --cached --name-status
```

After implementation commit:

```bash
git rev-parse HEAD
git status --short
```

Report commitを分ける場合:

```text
implementation commit
report commit
```

を明確に区別する。

---

# 26. Stop Conditions

## READY_FOR_TEST

全Implementation Completion Conditionsを満たす。

Then:

```text
implementation/test/migration commit固定
template-compliant completion report作成
Test Agentへhandoff
STOP
```

Coding Agentは:

```text
Gate PASSを宣言しない
G05を開始しない
Current Architecture Control Sheetを更新しない
```

## DESIGN_BLOCKED

以下のようなsemantic contradictionのみ。

```text
ADR-006/007とcurrent mandatory source-artifact semanticsが
implementation choiceでは解消不能

Result level/cardinalityを決めるために
新しいscientific semanticsのhuman decisionが必要

compensation contractに
06/ADRでは決められないownership decisionが必要
```

Report templateに従い:

```text
Contradiction
Observed facts
Impact
Minimal choices
Decision required
```

を記載して停止する。

単なるtest failure/environment failureは自動的にDESIGN_BLOCKEDではない。

---

# 27. Primary Risk Focus

G04は「result_level columnを追加した」「artifact tableにstage_idを足した」だけでは完了しない。

必要なauthority graphは:

```text
Canonical Execution / StageExecution
          │
          v
Canonical Result/Artifact Ownership Service
     ├─ explicit Result level
     ├─ explicit cardinality
     ├─ typed ownership validation
     ├─ semantic Product IDs
     └─ compensation/reconciliation
          │
          v
metadata repositories / Product UoW
          │
          └─────────────┐
                        v
                 ArtifactStorePort
                 physical bytes only
```

次の状態はG04未達:

```text
product_result exists
but Family still needs a different canonical Result owner

or

Artifact has an ID
but downstream still treats object_key as identity

or

DB/store failure can leave an untracked orphan

or

Artifact-only output is accidental None behavior

or

GenericExecutor now persists output metadata
```

同時に、G04でold family pathsを全面cutoverしてG05を先取りすることも誤り。

**G04はcanonical ownership contractを成立させるGate、G05は全Product pathをそのcontractへ収束させるGateである。**
