# Ariadne ENH-E4 E4-G05 実装指示書

* Project: Ariadne / causal-atelier
* Enhancement: ENH-E4 eliminate dual execution
* Branch: `refactor/ariadne_mvp_e4`
* Gate: `E4-G05`
* Gate name: Product Execution Convergence
* Trial: `01`
* Expected starting repository ref: `d2b0f311fda209608629114aaae9a1ea142bdd2d` またはその後のdocumentation-only descendant
* G04 tested implementation: `9c9db4454e0f08c4d46cb002f723ca6827917564`
* Expected starting Product migration head: `20260809_product_0009`
* G01/G02/G03/G04: `PASS`
* Standard Test PostgreSQL Infrastructure: mandatory
* Trial ID format: 2-digit zero-padded decimal (`01`–`99`)
* Test Item ID format: 3-digit zero-padded decimal (`001`–`998`; `000` reserved; `999` Gate Decision)

---

# 1. Source of Truth

本書は **E4-G05 Trial 01 Coding Agentが従うGate-local implementation contract** である。

G05はENH-E4における **唯一の Product Execution Convergence Gate** である。

正本:

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
30_test_report/G04/
E4-G04_02_999_gate_decision.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G04/
E4-G04_02_implementation_completion_report.md
```

Current Architecture Control SheetがG04 PASS反映前のsnapshotである場合は、**G04 final Gate Decisionを優先**する。

本書とcurrent sourceの間に、実装選択では解消できないsemantic contradictionがある場合のみ `DESIGN_BLOCKED` とする。

---

# 2. Transition Debt Interpretation

Phase 07文書にはTD-004の導入Gateについて局所的な記述差があるが、Global Transition Debt Registerおよびproject handoffに従い、G05では以下を採用する。

```text
G05 closes:
    E4-TD-001
    E4-TD-002
    E4-TD-003

G05 records:
    E4-TD-004 OPEN until G06
    Authority: structural lineage generic duplicate writes
```

G05でG06 lineage consolidationを先取りしない。

この既知文書差は `DESIGN_BLOCKED` 理由ではない。

---

# 3. Report Format Is a Completion Contract

Coding Agentは開始時に必ず以下を実物参照する。

```text
docs/wiki/develop_memo/_work/
agentic_enhancement_workflow_template_complete/
20_implementation_reports/
README.md

docs/wiki/develop_memo/_work/
agentic_enhancement_workflow_template_complete/
20_implementation_reports/
TEMPLATE_implementation_completion_report.md

docs/wiki/develop_memo/_work/
agentic_enhancement_workflow_template_complete/
20_implementation_reports/
TEMPLATE_implementation_report_detail.md
```

Implementation Completion Reportはtemplate/specificationへfield-by-field準拠する。

禁止:

```text
required section省略
required field省略
required sectionの独自merge
required fieldをprose summaryで代替
独自short format
空欄
Gate PASS/FAIL/BLOCKEDをCoding Agentが判定
```

値がない場合は:

```text
N/A
NONE
NOT_RUN
UNKNOWN
```

を使いfieldを残す。

**Substantive implementation/test success does not waive report-format compliance.**

format不適合のまま `READY_FOR_TEST` としてはならない。

---

# 4. Start-of-Work Verification

最初に実行し、Completion Reportへ記録する。

```bash
git branch --show-current
git rev-parse HEAD
git rev-parse d2b0f311fda209608629114aaae9a1ea142bdd2d^{commit}
git status --short
git log --oneline -15
```

Expected branch:

```text
refactor/ariadne_mvp_e4
```

Expected Product migration head:

```text
20260809_product_0009
```

`d2b0f311...` 後にControl Sheet更新等のdocumentation-only commitが存在することは許容する。

source/test/migration/configが変わっている場合はdiffを読み、G05 baselineへ与える影響をreportへ記録する。

既知unrelated artifact:

```text
deploy/.nfs000000000076202f00000088
```

はstage / restore / delete / recreateしない。

---

# 5. Protected Architecture Before G05

G05は新しいcanonical contractを発明するGateではない。G02〜G04で成立した以下を保全する。

## 5.1 G02

```text
one canonical Execution identity
analysis_family = CAUSAL | EXPLORATORY | PREDICTIVE
shared lifecycle
one claim/lease authority
atomic claim
owner-checked mutation
retry = same Execution ID
rerun/revise = new Execution ID + typed relation
cancel = terminal transition
```

## 5.2 G03

```text
persistent StageExecution for all canonical families
stable StageExecution identity across retry
persistent attempt history
queryable stage/input/output/timestamps
Execution claim/lease controls stage mutation
GenericExecutor:
    plan/order/binding/runner outcome only
    no lifecycle/persistence/retry authority
```

## 5.3 G04

```text
explicit Result level:
    EXECUTION_RESULT
    STAGE_RESULT

one canonical Result/Artifact ownership boundary
Artifact ID = semantic identity
object_key = physical locator
ArtifactStorePort = physical storage only
DB/store compensation/reconciliation explicit
typed downstream reuse
artifact-only output explicit in workflow contract
```

G05はこれらを変更せず、**全user-visible Product pathをこのauthorityへ収束**させる。

---

# 6. Current Dual-Lifecycle Evidence to Eliminate

Coding Agentはactual sourceを再inventoryする。

baselineでは少なくとも以下が存在する。

## 6.1 Canonical common submission capability

`src/ariadne/product/application/execution_service.py`

```text
CreateExecutionBatchCommand.analysis_family
ExecutionService.create_execution_batch()
CanonicalPlanProvider
StagePlanMaterializer
uow.executions
uow.stage_executions
```

が存在する。

## 6.2 Exploratory old lifecycle

`src/ariadne/product/application/exploratory_service.py`

baselineでは:

```text
submit_execution()
    -> FamilyExecutionOrm
    -> FamilyStageExecutionOrm
    -> direct Session commit

claim_next()
    -> FamilyExecutionOrm SELECT ... FOR UPDATE SKIP LOCKED

process_execution()
    -> FamilyResultOrm
    -> FamilyArtifactOrm
    -> family stage/execution state update
```

が残っている。

## 6.3 Predictive old lifecycle

`src/ariadne/product/application/predictive_workflow_service.py`

baselineでは:

```text
submit_execution()
    -> FamilyExecutionOrm
    -> FamilyStageExecutionOrm

claim_next()
    -> FamilyExecutionOrm family=PREDICTIVE

process_execution()
    -> old family lifecycle/output persistence
```

が残っている。

## 6.4 Canonical worker

`src/ariadne/interfaces/worker/execution_processor.py`

はcanonical repositoriesを使用するが、baselineのscientific dispatchはCausal中心である。

G05ではworker lifecycle authorityをfamily-neutralに収束させる。

---

# 7. Gate Objective

E4-G05 Objective:

> Causal / Exploratory / Predictiveの全てをcanonical Execution authorityへcutoverする。

Architecture after G05:

```text
Product API / auditable Product CLI
                │
                v
       family request adapter
                │
                v
      Canonical Execution Service
                │
                v
       canonical Execution UoW
       ├─ Execution
       └─ persistent StageExecution
                │
                v
       one canonical claim/lease
                │
                v
       canonical worker/orchestrator
                │
                v
      family scientific adapter
      ├─ Causal
      ├─ Exploratory
      └─ Predictive
                │
                v
       detached runner outcome
                │
                v
 canonical Result/Artifact owner
                │
                v
 Product metadata + ArtifactStorePort
```

Old Causal/Family Product lifecycle:

```text
new Product write authority = NONE
```

Source files/tablesはG07まで残ってよいが、new Product writes must not reach them.

---

# 8. Core Convergence Principle

G05の意味は:

```text
one lifecycle authority
```

であり:

```text
one scientific workflow
one universal request DTO
one payload schema
```

ではない。

Allowed:

```text
CausalSubmissionAdapter
ExploratorySubmissionAdapter
PredictiveSubmissionAdapter
family-specific planner
family-specific runner registry
family-specific scientific payload
family-specific read projection
```

Forbidden:

```text
family-specific Execution table write authority
family-specific claim authority
family-specific StageExecution persistence authority
family-specific Result/Artifact metadata owner
```

---

# 9. Family Submission Adapter Contract

全user-visible Product submissionは最終的に:

```text
canonical Execution
+
persistent canonical StageExecution children
```

を作成する。

Family adapterはexisting request/specificationをcanonical submissionへ変換し、実在するfamily semanticsを保持する。

Examples of semantics that may need preservation:

```text
analysis_family
dataset version
analysis view
research context
analysis specification
execution plan
seed/randomness
immutable specification snapshot/hash
plan snapshot/hash
runtime/code/schema versions
revision/rerun context
family-specific parameters
```

存在しないfieldを推測して追加しない。

禁止:

```text
Exploratory/Predictiveを
semanticに偽ったCausal DISCOVERYとして登録
```

canonical Executionのfieldだけでは既存family semanticsを正しく表現できない場合:

1. ADRのfamily discriminator / workflow-specific specification contractに従うminimal typed extensionを行う。
2. schema changeが本当に必要ならProduct migrationを追加する。
3. 新しいsemantic human decisionが必要なら `DESIGN_BLOCKED`。

**One authority does not require one command class.**

Family-specific request/validation DTOは保持してよい。

---

# 10. Route-to-Authority Inventory

Coding前にcurrent Product surfacesをinventoryする。

最低限:

```text
Causal submit
Exploratory submit
Predictive submit

execution get/list
cancel
retry
rerun
revise

worker entrypoint
claim
processing

Result list/get/write
Artifact list/get/write

Product/auditable CLI if any
low-level scientific CLI
```

各surfaceについて:

```text
Route / command
Current service
Current write authority
Target canonical authority
Post-G05 read projection
```

をCompletion Reportへ記載する。

Existing URL / response schemaを維持してよい。

ただしhandlerはcanonical authorityへdelegateする。

Public/Product routeから:

```text
FamilyExecutionOrm
FamilyStageExecutionOrm
FamilyResultOrm
FamilyArtifactOrm
```

へnew writeしてはならない。

---

# 11. Canonical Claim / Worker Contract

G05 exit時:

```text
all families
    -> canonical Execution repository/service claim
```

family-specific `claim_next()` が独立Product authorityとして動作してはならない。

正しい順序:

```text
canonical claim
    ↓
Execution.analysis_family
    ↓
family adapter/runner selection
    ↓
persistent StageExecution orchestration
    ↓
scientific execution
```

`ExecutionProcessor`をfamily-neutral化してよい。別common orchestratorでもよい。

ただし:

```text
claim authority
StageExecution persistence
Result/Artifact ownership
Execution terminalization
```

は一つでなければならない。

Family-specific processor classが残る場合もscientific adapterでありpersistent lifecycle ownerではない。

G02 lease contractを維持する。

---

# 12. Scientific Adapter Contract

G05ではscientific behaviorを変更しない。

```text
Causal scientific runners
Exploratory scientific runners
Predictive scientific runners
```

を保持する。

old family service内で:

```text
planning/science
+
Session lifecycle/ORM persistence/claim
```

が混在している場合、science/planning側をadapterとして再利用/抽出し、ORM lifecycle write authorityを停止する。

Family adapter / GenericExecutorからcanonical ownerへ渡すものは:

```text
detached result descriptors
artifact descriptors
stage output bindings
failure classification
scientific diagnostics
```

等。

ORM rowをcanonical outcome contractにしない。

---

# 13. Result / Artifact Convergence

G04 contractを全family new-writeへ適用する。

All new Result:

```text
canonical Result owner
explicit Result level
canonical Execution ID
StageResult -> canonical StageExecution ID
```

All new execution-output Artifact metadata:

```text
canonical Artifact owner
artifact_id semantic identity
object_key physical locator
ArtifactStorePort physical bytes
```

禁止:

```text
canonical Result/Artifact
+
FamilyResultOrm/FamilyArtifactOrm
```

のsame-request dual-write。

TD-003はG05で閉じる。

historical old rowのread-only compatibilityはG07まで許容され得るが、new G05 outputのreadはcanonical ownerから行う。

---

# 14. Lifecycle Mutation Convergence

family-facing endpoints/servicesが:

```text
cancel
retry
rerun
revise
```

を提供する場合、G02 canonical semanticsへdelegateする。

Retry:

```text
same Execution ID
same StageExecution identity
append attempt history
```

Rerun/revise:

```text
new canonical Execution ID
typed base/source relation
same analysis_family
```

Cancel:

```text
canonical terminal Execution
canonical StageExecution cancellation semantics
```

old FamilyExecution state mutationを行わない。

---

# 15. Query / Read Projection

G05はwrite convergence Gateだが、new canonical executionをexisting user-visible family APIが読めなければGolden Pathは成立しない。

family-specific response modelを維持する場合:

```text
Canonical Execution -> family response projection
Canonical Result    -> family result projection
```

を用いる。

禁止:

```text
new canonical write
then
family endpoint only queries FamilyExecutionOrm
and returns not found
```

historical old-row read compatibilityが必要ならread-only adapterとして明示する。

---

# 16. Old Write Authority Shutdown

G05 PASSの核心。

G07前なのでsource/table削除は要求しない。

```text
FamilyExecutionOrm
FamilyStageExecutionOrm
FamilyResultOrm
FamilyArtifactOrm
old service files
```

は残ってよい。

しかしProduct runtimeからnew-write可能な:

```text
submit
claim
process persistence
cancel/retry/rerun/revise
Result/Artifact create/delete
```

がold authorityへ到達してはならない。

Allowed strategies:

```text
A. old method delegates canonical service
B. method is removed from Product routing and read-only split
C. old mutating method explicitly rejects non-canonical writes
D. family service split into science/read projection and canonical lifecycle adapter
```

static grepだけでなくreal PostgreSQLで:

```text
old family table row counts before
    ↓
new Causal/Exploratory/Predictive Product Golden Paths
    ↓
old family table row counts after
```

が増えないことをtestする。

canonical failure時にold authorityへfallbackしてはならない。

---

# 17. CLI Boundary

Target ADR-011をG05でuser-visible write boundaryへ反映する。

## Low-level scientific CLI

以下はcanonical Executionへ統合しなくてよい。

```text
explicitly low-level scientific utility
local input/output
Product DB persistence/auditabilityを約束しない
```

## Auditable Product CLI

CLIが:

```text
user-visible Product analysis
Product DB persistence
auditability
```

を提供するならcanonical Execution serviceへsubmitする。

CLIからhidden old Product lifecycleを作らない。

CLI source retirement/final classificationはG07 scope。

---

# 18. Lineage Boundary / TD-004

G05はlineage consolidation Gateではない。

禁止:

```text
generic-only allowlist final cutover
structural generic writer全削除
closure/export redesign
lineage source-class finalization
```

ただしold Family lifecycleをlineageを書くためだけに残してはならない。

必要なlineage compatibility writeはcanonical IDsを使う。

Completion Reportでremaining structural generic duplicate writesを:

```text
file/function
relation kind
reason deferred
exit Gate G06
```

としてinventoryし、TD-004へhandoffする。

新しいduplicate writerを増やさない。

---

# 19. Recovery / Rollback Contract

G05 cutover後のfailure recoveryはcanonical lifecycleのみ。

```text
incomplete canonical Execution
    -> retry/requeue
    -> fail terminally
    -> cancel
```

禁止:

```text
"Predictive canonical processing failed"
    -> FamilyExecutionOrmへfallback
```

old write authorityをrollback strategyとして復活させない。

---

# 20. Product Migration Policy

Expected starting Product head:

```text
20260809_product_0009
```

G05 default:

```text
new Product migration = NOT REQUIRED
```

空migrationをGate番号のためだけに追加しない。

canonical Executionがrequired family semanticsを表現するためschema extensionが実証的に必要な場合のみProduct migrationを追加する。

root legacy migrationは変更しない。

G05でold family tablesをdropしない。

historical application-data migrationを行わない。

---

# 21. Required Automated Test Coverage

Coding AgentはAC-001〜005をdirectly proveするautomated testsを実装する。

Recommended logical split:

```text
tests/product/test_enh_e4_g05_submission_convergence.py
tests/product/test_enh_e4_g05_family_golden_paths_postgres.py
tests/product/test_enh_e4_g05_old_write_negative.py
tests/product/test_enh_e4_g05_cli_boundary.py
```

actual splitは任意。

---

# 22. E4-G05-AC-001 — Causal Golden Path

real PostgreSQLで:

```text
Product submit
-> canonical Execution family=CAUSAL
-> persistent StageExecution
-> canonical claim
-> scientific adapter
-> canonical Result/Artifact
-> terminal canonical Execution
```

を検証する。

Must assert:

```text
one execution_id
fresh UoW/session reload
no old family lifecycle/output row created
G02/G03/G04 contract preserved
```

---

# 23. E4-G05-AC-002 — Exploratory Golden Path

real PostgreSQLでuser-visible Product Exploratory submission pathを通す。

Must prove:

```text
returned ID == canonical execution_id
analysis_family == EXPLORATORY
persistent canonical stages
canonical claim authority
family scientific semantics/snapshot preserved
canonical Result/Artifact if produced
terminal canonical state
fresh Session reload
family-facing read surface sees new canonical data
```

Mandatory negative:

```text
no new FamilyExecutionOrm
no new FamilyStageExecutionOrm
no new FamilyResultOrm
no new FamilyArtifactOrm
```

---

# 24. E4-G05-AC-003 — Predictive Golden Path

real PostgreSQLでuser-visible Product Predictive submission pathを通す。

Must prove:

```text
returned ID == canonical execution_id
analysis_family == PREDICTIVE
persistent canonical stages
canonical claim authority
specification/plan/seed/snapshot semantics preserved
canonical Result/Artifact if produced
terminal canonical state
fresh Session reload
family-facing read surface sees new canonical data
```

Mandatory old-family negativeも行う。

---

# 25. E4-G05-AC-004 — Cross-Family Authority

| Authority | CAUSAL | EXPLORATORY | PREDICTIVE |
|---|---|---|---|
| Execution repository | same canonical | same canonical | same canonical |
| claim/lease | same authority | same authority | same authority |
| StageExecution | canonical | canonical | canonical |
| Result owner | canonical G04 | canonical G04 | canonical G04 |
| Artifact owner | canonical G04 | canonical G04 | canonical G04 |
| GenericExecutor lifecycle authority | NO | NO | NO |

をautomated evidenceで証明する。

canonical claimerがall familiesを同じrepository contractで扱えることをreal PostgreSQLで証明する。

---

# 26. E4-G05-AC-005 — Old-Write Negative

Positive Golden Pathだけでは不足。

## Static

Product route/service/worker graphをinventoryし:

```text
FamilyExecutionOrm new-write
FamilyStageExecutionOrm new-write
FamilyResultOrm new-write
FamilyArtifactOrm new-write
family-specific SELECT FOR UPDATE claim
```

がnew Product write routeからreachableでないこと。

## Runtime PostgreSQL

public/application G05 paths実行後:

```text
old family lifecycle/output table counts unchanged
```

を検証。

## Old methods

old mutating methodがsourceに残る場合:

```text
delegate canonical
or
explicit reject
```

をbehavior test。

## No fallback

canonical failure injection時にold write authorityへfallbackしない。

## GenericExecutor

G03/G04 negative contractを維持。

---

# 27. Mutation / Read / CLI Coverage

Exposed family mutation APIについて:

```text
cancel
retry
rerun
revise
```

のcanonical delegationをtestする。

最低限、G05前に存在したExploratory/Predictive mutation surfaceをinventoryし、実在するものを検証する。

new canonical family execution/resultがexisting supported family read surfaceから読めること。

CLIはactual inventoryを作成し:

```text
LOW_LEVEL_SCIENTIFIC
AUDITABLE_PRODUCT
```

を分類する。

存在しないcategoryを捏造しない。

---

# 28. Passed-Gate Regression

Mandatory:

```text
G02 Execution lifecycle/claim
G03 StageExecution/GenericExecutor
G04 Result/Artifact ownership/compensation/typed reuse
PostgreSQL contract
```

required affected files/nodesを実行する。

過去assertionを弱めない。

---

# 29. Standard PostgreSQL Verification

real PostgreSQL testは唯一:

```bash
scripts/test/run_product_postgres_tests.sh <pytest-path-or-node> [pytest-options]
```

Example:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g05_submission_convergence.py \
  tests/product/test_enh_e4_g05_family_golden_paths_postgres.py \
  tests/product/test_enh_e4_g05_old_write_negative.py \
  tests/product/test_enh_e4_g02_canonical_execution.py \
  tests/product/test_enh_e4_g03_acceptance_postgres.py \
  tests/product/test_enh_e4_g04_result_artifact_postgres.py \
  tests/product/test_postgres_contract.py
```

禁止:

```text
manual docker run
manual network probing
manual DSN
manual psql reset
manual alembic
manual external PostgreSQL pytest
```

---

# 30. Route-to-Authority Matrix — Mandatory Report Output

Completion Reportへimplementation前後を記録する。

| Product Surface | Before G05 | After G05 |
|---|---|---|
| Causal submit | actual | canonical |
| Exploratory submit | actual | canonical |
| Predictive submit | actual | canonical |
| Causal claim/process | actual | canonical |
| Exploratory claim/process | actual | canonical |
| Predictive claim/process | actual | canonical |
| Result write | actual | canonical G04 |
| Artifact metadata write | actual | canonical G04 |
| cancel/retry/rerun/revise | actual | canonical |
| Product/auditable CLI | actual | canonical or NONE |
| low-level scientific CLI | utility | utility |

After欄にold family write authorityが残っていてはならない。

---

# 31. Transition Debt Exit Contract

## TD-001 CLOSE

```text
no old Causal/Family new Execution write
all user-visible submission -> canonical Execution
```

## TD-002 CLOSE

```text
all new Product families -> persistent canonical StageExecution
no old/ephemeral persistent lifecycle for new writes
```

## TD-003 CLOSE

```text
all new Product outputs -> canonical Result/Artifact owner
no Family Result/Artifact new write
```

## TD-004 G06 handoff

Remaining structural generic duplicate writersをexact inventoryする。

none observedなら`NONE observed`と書き、事実を捏造しない。

---

# 32. Allowed Change Areas

必要な範囲:

```text
src/ariadne/product/application/execution_service.py
src/ariadne/product/application/exploratory_service.py
src/ariadne/product/application/predictive_workflow_service.py
src/ariadne/product/workflow/
src/ariadne/product/domain/
src/ariadne/product/ports/
src/ariadne/product/persistence/

src/ariadne/interfaces/web_api/routers/
src/ariadne/interfaces/web_api/schemas/
src/ariadne/interfaces/worker/
src/ariadne/interfaces/cli/
    only G05 Product/auditable boundary

src/ariadne/capabilities/
    wiring/adapters only; no scientific redesign

product_migrations/
    only if demonstrably required

tests/product/

20_implementation_reports/G05/
ENH-E4_implementation_report_detail.md
```

---

# 33. Forbidden Change Areas

```text
scientific algorithms/statistics
root legacy migration chain
legacy source broad deletion
ariadne.legacy retirement work
lineage authority final consolidation
closure/export redesign
frontend UX
auth
unrelated dataset ingestion
deployment topology
standard PostgreSQL infrastructure
passed Gate instruction/report artifacts
Current Architecture Control Sheet
    # update only after final G05 PASS by operator
```

---

# 34. Acceptance Criteria

## E4-G05-AC-001
Causal submissionがcanonical Executionを生成する。

## E4-G05-AC-002
Exploratory submissionがcanonical Executionを生成する。

## E4-G05-AC-003
Predictive submissionがcanonical Executionを生成する。

## E4-G05-AC-004
三familyが同じclaim authority、persistent StageExecution、Result/Artifact ownerを使う。

## E4-G05-AC-005
old Causal/Family lifecycleが新規Product writeを受け付けず、GenericExecutorがlifecycle ownerでない。

---

# 35. Negative Acceptance Criteria

Any is defect:

```text
Exploratory submit creates FamilyExecutionOrm
Predictive submit creates FamilyExecutionOrm
Product claim reads FamilyExecutionOrm as authority
new Product stage writes FamilyStageExecutionOrm
new output writes FamilyResultOrm / FamilyArtifactOrm
new canonical output is mirrored to old tables
family-specific old claimer remains active
canonical worker cannot dispatch a family
family read surface cannot see newly canonical data
family semantics are falsified into causal-only semantics
GenericExecutor gains lifecycle/output authority
object_key becomes semantic input identity
old authority used as failure fallback
low-level CLI forced into Product lifecycle unnecessarily
auditable Product CLI creates hidden lifecycle
G06 lineage final cutover performed
legacy source broadly deleted
historical migration introduced
```

---

# 36. Implementation Completion Conditions

`READY_FOR_TEST` only if:

1. Causal submit canonical.
2. Exploratory submit canonical.
3. Predictive submit canonical.
4. all new family submissions have persistent canonical stages.
5. one claim/lease authority handles all families.
6. family dispatch happens after canonical claim.
7. scientific family semantics preserved.
8. all new Results use canonical G04 owner.
9. all new Artifacts use canonical G04 owner.
10. ArtifactStore remains physical-only.
11. supported family read surfaces see new canonical writes.
12. family mutation surfaces use canonical lifecycle.
13. no new FamilyExecution write from Product path.
14. no new FamilyStage write.
15. no new FamilyResult write.
16. no new FamilyArtifact write.
17. old write methods delegate or reject.
18. real PostgreSQL row-count negative exists.
19. no old-authority fallback.
20. GenericExecutor remains non-authoritative.
21. CLI boundary is explicit.
22. TD-001 closed.
23. TD-002 closed.
24. TD-003 closed.
25. TD-004 state/inventory recorded.
26. no G06/G07/G08 crossing.
27. G02 regression passes.
28. G03 regression passes.
29. G04 regression passes.
30. standardized PostgreSQL verification passes.
31. migration head recorded accurately.
32. fixed implementation commit exists.
33. Completion Report template-compliant.
34. exact self-check commands/exit/evidence recorded.
35. enhancement-wide ledger updated.
36. unrelated artifact untouched.

---

# 37. Required Outputs

Implementation commit containing:

```text
production source
automated tests
Product migration only if required
```

Completion Report:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G05/
E4-G05_01_implementation_completion_report.md
```

Status only:

```text
READY_FOR_TEST
DESIGN_BLOCKED
```

Mandatory supplemental content without removing template fields:

```text
actual baseline SHA
implementation SHA
migration head
route-to-authority before/after matrix
Causal adapter
Exploratory adapter
Predictive adapter
canonical worker dispatch
old claim/write method disposition
read projection compatibility
mutation convergence
CLI classification matrix
old table runtime negative evidence
TD-001/002/003 closure evidence
TD-004 inventory/status
AC -> exact pytest node mapping
G02/G03/G04 regression
known limitations
working-tree integrity
```

Update:

```text
20_implementation_reports/
ENH-E4_implementation_report_detail.md
```

without erasing prior history.

---

# 38. Self-check Evidence

Each executed command must record:

```text
exact copy-pastable command
test target
exit code
passed/failed/skipped
raw evidence path
tested SHA/state
```

`tests passed` only is insufficient.

---

# 39. Stop Conditions

## READY_FOR_TEST

After all completion conditions:

```text
fix implementation SHA
create template-compliant report
handoff to Test Agent
STOP
```

Do not:

```text
declare G05 PASS
start G06
update Control Sheet
delete legacy source
```

## DESIGN_BLOCKED

Only if existing approved architecture cannot represent required existing family semantics without a new human decision.

Simple test failure/environment failure is not DESIGN_BLOCKED.

---

# 40. Primary Risk Focus

PASS architecture:

```text
ALL THREE USER-VISIBLE FAMILIES
          │
          v
ONE canonical submission authority
          │
          v
ONE canonical Execution identity
          │
          v
ONE claim/lease authority
          │
          v
persistent canonical StageExecution
          │
          v
family science only
          │
          v
ONE canonical Result/Artifact owner
```

FAIL architecture:

```text
API canonical / worker old
submit canonical / Result old
Exploratory canonical / Predictive old
canonical + old dual-write
failure -> old fallback
```

G05 exit時、**new Product write authorityは一つでなければならない。**
