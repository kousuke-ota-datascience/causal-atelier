# 02 Execution Lifecycle Inventory — Architecture Review Prompt

## 1. Task

`ENH-E4 eliminate dual execution` の Architecture Review Phase 02 として、現在のRepositoryに存在する **Execution lifecycle model** を静的コード調査によってInventory化し、相互比較する。

本Phaseの中心目的は、

> 現在のAriadneにおいて「Execution」と呼ばれる処理単位が、identity・persistence・state transition・worker claim・retry/rerun・stage管理の観点で、実際に何種類のlifecycle modelとして実装されているか

をコード上のevidenceによって確定することである。

特に、Phase 01で確認された以下の経路を重点調査する。

```text
Causal Product Execution

Exploratory Family Execution

Predictive Family Execution

Standalone Scientific CLI Execution
```

加えて、現在の標準runtimeからは到達が確認されていないlegacy Executionについても、**比較対象としてコード上のlifecycle modelを調査する**。

ただし、legacy codeの削除可否やTarget Architectureは本Phaseでは決定しない。

このPhaseは **read-only architecture investigation** である。

Production code、test code、configuration、migration、dependency、database、runtime stateを変更してはならない。

唯一許可されるRepositoryへの書き込みは、指定されたresult文書の生成・更新だけである。

---

## 2. Positioning

Phase 01:

```text
Runtime Root
→ Boundary Entry Point
→ Application Service
→ First Execution Boundary
```

Phase 02:

```text
Execution creation
→ identity
→ persistence
→ queue/state
→ claim
→ processing
→ stage execution
→ terminal state
→ cancel/retry/rerun/revise
```

を調査する。

本PhaseはExecution lifecycleの**現状構造を確定するPhase**であり、

以下はまだ行わない。

* canonical Execution modelの決定
* legacy code削除判断
* Product内部のExecution統合判断
* database schema変更案
* API変更案
* worker統合案
* service統合案
* Result ownership再設計
* Artifact ownership再設計
* Lineage architecture再設計
* Gate decomposition
* implementation plan作成

本Phaseのresultは、それらの設計判断を行うためのevidenceとする。

---

## 3. Repository / Investigation Context

対象Repository:

```text
causal-atelier
```

対象branch:

```text
refactor/ariadne_mvp_e4
```

ENH-E4 work directory:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
```

前Phase result:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
architecture_review/
01_runtime_entrypoint_inventory_result.md
```

本Phase result出力先:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
architecture_review/
02_execution_lifecycle_inventory_result.md
```

調査開始時点のcommit SHAを必ず記録すること。

---

## 4. Required Use of Phase 01 Evidence

調査開始時に、

```text
01_runtime_entrypoint_inventory_result.md
```

を読むこと。

特に以下を引き継ぐ。

* Runtime Root ID
* Entry Point ID
* `E4-OBS-001` 〜 `E4-OBS-013`
* `E4-INF-001` 〜 `E4-INF-005`
* `E4-UNK-001` 〜 `E4-UNK-004`

既存IDを変更・再採番してはならない。

ただし、Phase 01 resultに記載された内容を無条件に真と仮定して、Phase 02の詳細調査を省略してはならない。

Lifecycleに関する新しい主張はproduction source / persistence code等から独立してevidenceを取得すること。

---

# 5. Core Investigation Questions

以下の問いへコード上のevidence付きで回答すること。

## Q1. Execution identity

各Execution lifecycleは、何をidentityとして持つか。

例:

```text
execution_id
family_execution_id
batch_key
plan_id
stage_id
base_execution_id
parent_execution_id
revision source
rerun source
```

確認すること:

* ID生成主体
* ID型
* ID namespace
* primary key
* external APIで使用されるID
* workerで使用されるID
* retry/rerun/revise時にidentityが維持されるか、新規生成されるか

---

## Q2. Persistence ownership

各Execution lifecycleはどこへ永続化されるか。

確認すること:

* domain entity
* ORM model
* repository
* UoW access point
* physical table
* related stage table
* related plan table
* state column
* timestamps
* parent/base relation
* retry/revision relation

単にclass名を確認するだけでは不十分。

可能な限り、

```text
Application Service
→ Domain Entity
→ Repository
→ ORM
→ Physical Table
```

を対応付けること。

---

## Q3. State machine

各Execution lifecycleについて、

```text
created
queued
claimed
running
succeeded
failed
cancel requested
cancelled
retry
rerun
revision
```

等のstate transitionを調査する。

コード上に存在する実際のstateのみを記録すること。

存在しないstateを一般論から補完してはならない。

確認すること:

* state enum / literal
* initial state
* transitionを実行するsymbol
* transition条件
* terminal states
* invalid transition validation
* cancellation semantics
* failure semantics

---

## Q4. Worker claim semantics

各worker対象Executionについて確認する。

```text
queue selection
→ claim
→ ownership/lease
→ running transition
→ processing
→ completion/failure
```

特に以下を確認する。

* claim対象repository
* claim query
* ordering
* locking mechanism
* lease / heartbeatの有無
* worker ownership fieldの有無
* state transitionとのatomicity
* commit boundary
* claim失敗時の挙動
* concurrent workerに対する排他方式

実装されていない場合は `NONE_CONFIRMED` とする。

推測してはならない。

---

## Q5. Processing boundary

各Execution lifecycleについて、

> lifecycle orchestrationを所有するcomponent

と、

> scientific computation / stage executionを行うcomponent

を区別する。

特に `GenericExecutor` について、

* Execution identityを所有するか
* lifecycle stateを所有するか
* persistenceを所有するか
* stage sequencingのみを行うか
* scientific runner invocationのみを行うか
* callerごとに責務が異なるか

を調査する。

「複数経路がGenericExecutorを使っている」というだけで「Execution architectureが統一されている」と判定してはならない。

---

## Q6. Stage lifecycle

Execution内部のstageについて調査する。

確認すること:

* stageが永続化されるか
* stage identity
* stage state
* executionとのrelation
* stage開始・成功・失敗の記録
* retry時のstage再利用 / 再生成
* execution-level stateとの同期方法

Causal / Exploratory / Predictiveでstage persistenceの仕組みが異なる場合は明示する。

---

## Q7. Retry / Rerun / Revise semantics

操作名を同義語として扱ってはならない。

各lifecycleについて、存在する操作を個別に調査する。

少なくとも以下を区別する。

```text
retry
rerun
revise
resubmit
requeue
```

各操作について確認すること:

* 同じExecution rowを再利用するか
* 新しいExecutionを生成するか
* IDが変わるか
* input snapshotが変わるか
* planが変わるか
* base/parent relationが保存されるか
* previous Resultへのrelationがあるか
* operation reasonが保存されるか
* failureのみ許可されるか
* completed Executionにも許可されるか

---

## Q8. Cancellation semantics

各lifecycleで、

```text
request cancel
→ state mutation
→ worker observation
→ processing interruption
→ final state
```

を追跡する。

確認すること:

* cancel requestが即時cancelなのか
* cancel_requested等のintermediate stateがあるか
* running scientific computationを実際にinterruptするか
* stage境界でのみ観測するか
* queued execution cancellation
* running execution cancellation
* terminal execution cancellation

---

## Q9. Transaction boundaries

主要なlifecycle transitionについて、

```text
with uow
commit
rollback
repository write
```

等を確認し、

どこまでが同一transactionで行われるかを記録する。

特に、

```text
claim + running transition
execution completion + terminal state
stage completion + execution completion
retry creation + source relation
```

のatomicityを調査する。

本Phaseではtransaction設計の良し悪しを評価しない。

---

## Q10. Result linkage boundary

Result / Artifact lifecycleそのものは後続Phaseで詳細調査する。

ただしExecution lifecycleを理解するため、以下のみ確認する。

* Execution completion時にResult IDを持つか
* Resultを誰が生成するか
* Execution → Result relationをどこで書くか
* Result生成失敗とExecution failureの関係
* Resultが存在しないExecution typeがあるか

ここから先の、

* Result ownership
* Artifact ownership
* Result schema差
* Artifact lifecycle
* lineage generation

は本Phaseでは深掘りしない。

---

# 6. Primary Investigation Targets

少なくとも以下を調査すること。

## 6.1 Causal Product Execution

Phase 01のCausal execution pathを起点に、

```text
HTTP submission
→ ExecutionService
→ Execution entity
→ repository / table
→ worker claim
→ ExecutionProcessor
→ GenericExecutor
→ terminal transition
```

を追跡する。

cancel / retryも含む。

---

## 6.2 Exploratory Family Execution

Phase 01のExploratory pathを起点に、

```text
HTTP submission
→ ExploratoryWorkspaceService
→ family Execution
→ persistence
→ worker claim
→ process_execution
→ GenericExecutor
→ terminal transition
```

を追跡する。

特にCausal Executionとの、

* entity
* repository
* table
* state enum
* claim method
* lifecycle methods

の共通 / 相違を確認する。

---

## 6.3 Predictive Family Execution

Phase 01のPredictive pathを起点に、

```text
plan
→ submit
→ family Execution
→ stage rows
→ worker claim
→ process_execution
→ GenericExecutor
→ terminal transition
```

を追跡する。

特に、

```text
cancel
retry
rerun
revise
```

のsemantic differenceを明示する。

---

## 6.4 Standalone Scientific CLI

CLI pathについて、

```text
command
→ ScientificCoreAdapter
→ scientific operation
→ output
```

を追跡し、

以下を確認する。

* Execution identityを生成するか
* Execution entityを生成するか
* databaseへExecutionを永続化するか
* workerを使用するか
* GenericExecutorを使用するか
* lifecycle stateを保持するか
* Result / ArtifactをProduct persistenceへ書くか

該当しないものは `NONE_CONFIRMED` とする。

CLIをProduct Execution lifecycleと同一視してはならない。

---

## 6.5 Legacy Execution Model

現在の標準runtime reachabilityは本Phaseの判定対象ではない。

Phase 01のclassificationを引き継ぐ。

ただしlegacy source内に存在するExecution lifecycleについて、

```text
creation
identity
persistence
state
worker
retry
failure
completion
result relation
```

を静的に調査する。

目的は、

> legacy codeに存在するExecution conceptが、active Product lifecycleと意味的・構造的にどの程度重複しているか

を後続Architecture Decisionで判断できるevidenceを残すことである。

削除可否は判断しない。

---

# 7. Required Source Scope

Repository全体を検索対象とする。

少なくとも以下を確認すること。

## 7.1 Domain

```text
src/ariadne/product/domain/**
src/ariadne/legacy/**/domain/**
```

特に:

* Execution entity
* family Execution entity
* enums
* state definitions
* transition methods
* validation rules

---

## 7.2 Application

```text
src/ariadne/product/application/**
src/ariadne/legacy/application/**
```

特に:

* submission
* cancellation
* retry
* rerun
* revise
* claim
* processing
* completion
* failure handling

---

## 7.3 Worker / Executor

```text
src/ariadne/interfaces/worker/**
src/ariadne/product/workflow/**
src/ariadne/legacy/workers/**
```

特に:

* worker selection
* claim
* `ExecutionProcessor`
* `GenericExecutor`
* runner registry
* stage execution
* error handling

---

## 7.4 Persistence

```text
src/ariadne/product/persistence/**
```

およびlegacy persistence関連コード。

確認すること:

* ORM classes
* repository implementations
* UoW
* claim queries
* physical table names
* state fields
* relation fields
* transaction handling

---

## 7.5 Migration

migration fileをread-onlyで確認してよい。

目的:

* physical table definition
* column definition
* foreign key
* index
* state persistence structure

migration historyの設計意図を推測してはならない。

migrationは**現存schema structureの補助evidence**としてのみ使用する。

---

## 7.6 Interface

以下を確認する。

```text
src/ariadne/interfaces/web_api/**
src/ariadne/interfaces/cli/**
```

API操作名とapplication lifecycle operationを対応付ける。

---

## 7.7 Tests

test codeはread-only evidenceとして参照してよい。

ただし、

> testが期待しているからproduction semanticsもそうである

と単独で断定してはならない。

優先順位は、

```text
production code / schema
> test evidence
> comments / documentation
```

とする。

testは主に、

* edge case
* intended transition
* invalid transition
* retry semantics

を補助的に確認するために使う。

---

# 8. Lifecycle Unit Definition

本Phaseでは、独立したExecution lifecycle modelを `Lifecycle Unit` と呼ぶ。

Lifecycle Unitは、少なくとも以下のいずれかが独立している場合に候補とする。

* distinct domain entity
* distinct persistent table
* distinct repository
* distinct state machine
* distinct worker claim mechanism
* distinct lifecycle service

単にrunnerが異なるだけの場合は、別Lifecycle Unitと断定してはならない。

逆に、同じ `GenericExecutor` を利用していても、

* identity
* persistence
* state machine
* lifecycle service

が別なら、同一Lifecycle Unitと断定してはならない。

---

# 9. Lifecycle Unit IDs

発見したLifecycle Unitには以下のIDを付ける。

```text
E4-LC-001
E4-LC-002
E4-LC-003
...
```

Phase 01で確認された経路を起点にする場合でも、

実際のコード調査結果に基づいてLifecycle Unitを確定すること。

事前に「3種類である」等と固定してはならない。

---

# 10. Lifecycle Dimension Matrix

各Lifecycle Unitについて最低限以下を埋めること。

| Dimension            | Value |
| -------------------- | ----- |
| Lifecycle Unit ID    |       |
| User-facing concept  |       |
| Domain entity        |       |
| Execution ID         |       |
| Physical table       |       |
| Repository           |       |
| UoW property         |       |
| Submission service   |       |
| Initial state        |       |
| State definition     |       |
| Claim mechanism      |       |
| Processing service   |       |
| GenericExecutor use  |       |
| Stage persistence    |       |
| Cancel support       |       |
| Retry support        |       |
| Rerun support        |       |
| Revise support       |       |
| Parent/base relation |       |
| Result linkage       |       |
| Terminal states      |       |
| Runtime reachability |       |

不明は空欄にせず `UNKNOWN` とする。

存在しないことを十分調査した場合は `NONE_CONFIRMED` とする。

---

# 11. Identity Comparison

Execution identityについて、以下のmatrixを作る。

| Lifecycle Unit | ID Field | ID Generator | Persisted | API-visible | Worker-visible | Parent/Base ID | Evidence |
| -------------- | -------- | ------------ | --------: | ----------: | -------------: | -------------- | -------- |

また、異なるLifecycle Unit間で、

* 同一ID namespaceか
* foreign keyで関連するか
* conversionされるか
* 完全に独立か

を確認する。

「UUIDだから同じidentity model」等の推論は禁止する。

---

# 12. Persistence Comparison

以下を作る。

| Lifecycle Unit | Domain Entity | Repository | ORM | Physical Table | Stage Table | Plan Table | Evidence |
| -------------- | ------------- | ---------- | --- | -------------- | ----------- | ---------- | -------- |

さらに、

```text
same table
different table
shared repository
different repository
shared UoW
different UoW
```

をコード上の事実として整理する。

---

# 13. State Machine Comparison

各Lifecycle Unitについてstate transition表を作る。

例:

| From | Trigger | To | Symbol | Transaction Boundary | Evidence |
| ---- | ------- | -- | ------ | -------------------- | -------- |

状態遷移がmethodとして明示されていない場合は、

repository/application codeによるstate assignmentを追跡する。

推定state machineを書いてよいが、

その場合は必ず `INFERENCE` とし、各edgeのsupporting evidenceを示すこと。

---

# 14. Operation Semantics Matrix

以下を作る。

| Lifecycle Unit | Submit | Claim | Cancel | Retry | Rerun | Revise | Failure Requeue |
| -------------- | ------ | ----- | ------ | ----- | ----- | ------ | --------------- |

各cellは単なるYes/Noではなく、最低限、

```text
same ID
new ID
same row
new row
unsupported
unknown
```

を識別できるようにする。

詳細は個別sectionに記載する。

---

# 15. Retry / Rerun / Revise Detailed Matrix

存在する全操作について、

| Operation | Source Lifecycle | Allowed Source State | New Execution? | New ID? | Copies Inputs? | Base/Parent Relation | State After Operation | Evidence |
| --------- | ---------------- | -------------------- | -------------: | ------: | -------------- | -------------------- | --------------------- | -------- |

を作る。

同一service内に存在する複数操作については必ず比較する。

名称が異なる以上、実装差が存在するかを確認する。

---

# 16. Worker Claim Comparison

以下を作る。

| Lifecycle Unit | Claim Symbol | Selection Rule | Locking | State Mutation | Commit Boundary | Lease/Heartbeat | Evidence |
| -------------- | ------------ | -------------- | ------- | -------------- | --------------- | --------------- | -------- |

特に、

同一worker loopが複数Lifecycle Unitを順番にclaimする場合、

* evaluation order
* starvation possibilityを示すコード構造
* one-loopあたりのclaim数

等の**観測事実**は記録してよい。

ただし性能評価や改善提案は行わない。

---

# 17. GenericExecutor Responsibility Analysis

`GenericExecutor` 自体を独立して調査する。

以下へ回答すること。

| Question                     | Answer | Evidence |
| ---------------------------- | ------ | -------- |
| Generates Execution ID?      |        |          |
| Persists Execution?          |        |          |
| Owns Execution state?        |        |          |
| Claims queued Execution?     |        |          |
| Commits transaction?         |        |          |
| Owns retry semantics?        |        |          |
| Owns cancellation semantics? |        |          |
| Owns stage sequencing?       |        |          |
| Invokes scientific runners?  |        |          |
| Produces execution output?   |        |          |

そのうえで、

```text
Lifecycle Orchestrator
vs
Workflow/Stage Executor
vs
Scientific Runner Dispatcher
```

のどの責務をコード上持っているかを記録する。

分類が推論を含む場合は `INFERENCE` とする。

---

# 18. CLI Comparison

Standalone CLIについて以下を明示する。

| Dimension                    | CLI Behavior | Evidence |
| ---------------------------- | ------------ | -------- |
| Execution ID                 |              |          |
| DB Execution row             |              |          |
| Persistent state machine     |              |          |
| Worker claim                 |              |          |
| GenericExecutor              |              |          |
| ScientificCoreAdapter        |              |          |
| Product Result persistence   |              |          |
| Product Artifact persistence |              |          |
| Retry lifecycle              |              |          |
| Cancel lifecycle             |              |          |

CLIが単なるutilityなのか、Execution architectureの独立経路なのかは本Phaseで設計判断しない。

確認できた構造だけを記録する。

---

# 19. Legacy Lifecycle Comparison

Legacy Executionについて、可能な範囲で同じDimension Matrixを作成する。

ただしRuntime ReachabilityはPhase 01の、

```text
UNREFERENCED_CANDIDATE
```

を変更しない。

新しいrepository-local wiringがPhase 02調査中に偶然見つかった場合のみ、そのevidenceを記録して `Phase 01 discrepancy` として報告する。

Phase 02だけでPhase 01 resultを書き換えてはならない。

---

# 20. Semantic Overlap Analysis

本PhaseではTarget Architectureを決めないが、

Lifecycle Unit間の**観測された重複・差異**は整理すること。

以下のdimensionごとに比較する。

```text
identity
persistence
state machine
claim
processing
stage model
cancel
retry
rerun
revise
result linkage
transaction boundary
```

各比較結果は以下のいずれかで表現する。

### `STRUCTURALLY_SHARED`

同一implementation / entity / repository等を実際に共有する。

### `STRUCTURALLY_DISTINCT`

異なるimplementation / entity / repository等を使用する。

### `SEMANTICALLY_SIMILAR`

目的・操作意味が類似していると複数のFactから合理的に推論できる。

これは必ず `INFERENCE` とする。

### `SEMANTICALLY_DISTINCT`

コード上のprecondition / outcome / state transition等が異なり、同一操作と扱えない。

FactまたはInferenceを明示する。

### `UNKNOWN`

証拠不足。

---

# 21. Critical Distinctions

以下を混同しないこと。

## 21.1 Shared worker process ≠ shared Execution lifecycle

同じworker processで処理されていても、別repository / table / state machineなら区別する。

---

## 21.2 Shared GenericExecutor ≠ shared Execution lifecycle

同じGenericExecutorを使っていても、Execution lifecycle ownershipがcaller側に存在する可能性がある。

---

## 21.3 Same state names ≠ same state machine

`QUEUED`, `RUNNING`, `SUCCEEDED` 等の名前が同じでも、

transition implementationやpersistenceが異なる場合は別物として記録する。

---

## 21.4 Same UUID type ≠ same identity

型や形式だけでidentity semanticsを同一視しない。

---

## 21.5 Similar API operation ≠ same operation semantics

`retry`, `rerun`, `revise` 等はコード上のbehaviorを比較する。

---

## 21.6 Legacy directory ≠ obsolete lifecycle

directory名のみで削除対象と判断しない。

---

# 22. Investigation Method

静的解析のみを使用する。

使用してよいもの:

* `git`
* `git grep`
* `rg`
* `grep`
* `find`
* `sed`
* `cat`
* `head`
* `tail`
* `awk`
* `tree`
* read-only Python AST analysis
* tracked source/config/schema/testの閲覧

必要な追加検索はAgent自身で行ってよい。

---

# 23. Prohibited Operations

以下を行ってはならない。

* production code変更
* test code変更
* configuration変更
* migration変更
* dependency変更
* dependency install
* formatter実行
* auto-fix
* code generation
* database変更
* database reset
* migration実行
* container操作
* application起動
* worker起動
* frontend起動
* test実行
* benchmark実行
* HTTP request
* external API access
* network調査
* source module importによるapplication execution
* architecture変更
* refactoring
* bug fix
* code deletion
* import整理
* documentation修正

唯一許可される書き込み:

```text
02_execution_lifecycle_inventory_result.md
```

および必要なparent directoryのみ。

---

# 24. Do Not Execute Runtime Code

禁止例:

```text
uvicorn ...
python -m ...
docker compose up
ariadne-worker
pytest
alembic upgrade
curl ...
```

Pythonを使用する場合も、application moduleをimportして副作用を起こしてはならない。

静的なtext / AST解析のみに限定する。

Runtime verificationが必要な論点は `Unresolved Items` に残す。

---

# 25. Investigation Procedure

## Step 1. Record Baseline

記録する。

* repository root
* branch
* HEAD
* working tree status
* start time

branchが

```text
refactor/ariadne_mvp_e4
```

でなければ、

```text
BLOCKED_WRONG_BRANCH
```

として停止する。

既存working tree変更を変更・stash・restore・resetしてはならない。

---

## Step 2. Read Phase 01 Result

Phase 01のEntry Point / observation / unresolved itemを確認する。

そこからLifecycle investigationの起点を特定する。

---

## Step 3. Discover Execution Entities

Repository全体から、

```text
Execution
ExecutionStatus
ExecutionState
FamilyExecution
StageExecution
ExecutionPlan
retry
rerun
revise
claim_next
```

等を探索する。

名称に依存しすぎず、Execution相当のpersistent entityも探索する。

---

## Step 4. Build Persistence Map

各entityについて、

```text
Domain
→ Repository interface
→ Repository implementation
→ ORM
→ physical table
```

を追う。

---

## Step 5. Build State Machine

creationからterminal transitionまで追跡する。

state mutationを行う全主要symbolを検索する。

---

## Step 6. Trace Worker Claim

各worker branchについて、

```text
claim
→ state mutation
→ commit
→ process
→ success/failure
```

を追跡する。

---

## Step 7. Trace GenericExecutor Boundary

callerとGenericExecutorの責務境界を確認する。

---

## Step 8. Trace Retry / Rerun / Revise / Cancel

APIからapplication service、entity/repository mutationまで追跡する。

---

## Step 9. Trace CLI Lifecycle Properties

Web/API lifecycleとの差をdimensionごとに確認する。

---

## Step 10. Trace Legacy Lifecycle

active Product pathとは独立した比較対象として調査する。

---

## Step 11. Compare Lifecycle Units

全Lifecycle Unitについてmatrixを作成する。

設計評価ではなく構造比較に限定する。

---

## Step 12. Record Unknowns

解決不能な箇所を推測で埋めない。

---

# 26. Evidence Standard

Architecture上の主要主張には必ず以下を付ける。

```text
<repository-relative-path>:<line or range>
Symbol: <symbol>
Evidence: <what this proves>
```

Lifecycle transitionの場合は、

```text
QUEUED → RUNNING
Evidence:
- path/file.py:100-120
- Symbol: claim_next
- Proves: claim operation changes persisted state from ...
```

のようにtransition単位で記録する。

---

# 27. Persistence Evidence Standard

physical table等を記載する場合、

可能であれば二種類以上のevidenceで確認する。

例:

```text
ORM definition
+
migration definition
```

一致しない場合は必ずdiscrepancyとして報告する。

推測でどちらかを正としない。

---

# 28. Fact / Inference / Unknown

## Fact

production code / schemaから直接確認できる。

```text
FACT
```

---

## Inference

複数Factから合理的に導く。

```text
INFERENCE
```

supporting `E4-OBS-*` を必ず示す。

---

## Unknown

証拠不足。

```text
UNKNOWN
```

「不明」である理由と、追加で必要なevidenceを書く。

---

# 29. Observation ID Continuity

Phase 01では、

```text
E4-OBS-001 ... E4-OBS-013
```

が使用済み。

本Phaseの新規Factは、

```text
E4-OBS-014
```

から開始する。

既存IDを再利用してはならない。

---

# 30. Inference ID Continuity

Phase 01では、

```text
E4-INF-001 ... E4-INF-005
```

が使用済み。

本Phaseの新規Inferenceは、

```text
E4-INF-006
```

から開始する。

---

# 31. Unknown ID Continuity

Phase 01では、

```text
E4-UNK-001 ... E4-UNK-004
```

が使用済み。

本Phaseで新たに発生するUnknownは、

```text
E4-UNK-005
```

から開始する。

Phase 01 unresolved itemが本Phaseの静的調査によって解決した場合、

既存IDを消さず、

```text
RESOLVED_IN_PHASE_02
```

としてevidenceを付ける。

ただしdeployment/runtime evidenceを必要とするものを無理に解決しない。

---

# 32. Required Result Structure

`02_execution_lifecycle_inventory_result.md` を以下の構造で作成する。

```markdown
# 02 Execution Lifecycle Inventory Result

## 1. Metadata

- Prompt:
- Prior phase:
- Repository root:
- Branch:
- HEAD:
- Working tree status:
- Started at:
- Finished at:
- Phase status:

## 2. Executive Summary

### 2.1 Lifecycle Units

| Lifecycle ID | Name | Runtime Reachability | Entity | Table | Lifecycle Owner | Worker Path |
|---|---|---|---|---|---|---|

### 2.2 High-Level Comparison

| Dimension | E4-LC-xxx | E4-LC-xxx | ... |
|---|---|---|---|

## 3. Lifecycle Unit Details

### E4-LC-001 — ...

#### Purpose / User-facing Concept

#### Entry Points

#### Identity

#### Domain Entity

#### Persistence

#### Initial Creation

#### State Machine

#### Worker Claim

#### Processing Boundary

#### GenericExecutor Relationship

#### Stage Lifecycle

#### Cancellation

#### Retry

#### Rerun

#### Revise

#### Failure Handling

#### Terminal Completion

#### Result Linkage Boundary

#### Transaction Boundaries

#### Evidence

#### Unknowns

Repeat for every Lifecycle Unit.

## 4. Identity Comparison Matrix

| Lifecycle Unit | ID | Generator | Table PK | API-visible | Worker-visible | Parent/Base Relation | Evidence |
|---|---|---|---|---|---|---|---|

## 5. Persistence Comparison Matrix

| Lifecycle Unit | Entity | Repository | ORM | Table | Stage Table | Plan Table | UoW |
|---|---|---|---|---|---|---|---|

## 6. State Machine Comparison

### 6.1 <Lifecycle>

| From | Trigger | To | Symbol | Transaction | Evidence |
|---|---|---|---|---|---|

Repeat.

### 6.x Cross-Lifecycle State Matrix

| Semantic State | E4-LC-... | E4-LC-... | Notes |
|---|---|---|---|

## 7. Worker Claim Comparison

| Lifecycle | Claim Symbol | Selection | Locking | State Mutation | Commit | Lease/Heartbeat | Evidence |
|---|---|---|---|---|---|---|---|

## 8. Processing / Executor Responsibility

### 8.1 Lifecycle Orchestrators

| Lifecycle | Lifecycle Owner | Responsibilities | Evidence |
|---|---|---|---|

### 8.2 GenericExecutor

| Responsibility | Present? | Evidence |
|---|---|---|

### 8.3 Scientific Runner Boundary

Describe where lifecycle orchestration stops and scientific execution begins.

## 9. Stage Lifecycle Comparison

| Lifecycle | Persistent Stage? | Stage Entity | Stage Table | State | Retry Behavior | Evidence |
|---|---:|---|---|---|---|---|

## 10. Mutation Semantics

### 10.1 Cancel

| Lifecycle | Supported | Same Row? | State Transition | Worker Handling | Evidence |
|---|---:|---|---|---|---|

### 10.2 Retry

| Lifecycle | Supported | New Execution? | New ID? | Source Relation | Input Copy | Evidence |
|---|---:|---:|---:|---|---|---|

### 10.3 Rerun

same structure.

### 10.4 Revise

same structure.

## 11. Transaction Boundary Comparison

| Lifecycle / Operation | Transaction Start | Writes | Commit | Atomic Scope | Evidence |
|---|---|---|---|---|---|

## 12. Result Linkage Boundary

| Lifecycle | Result Produced | Result ID Relation | Writer | Execution Terminal Coupling | Evidence |
|---|---|---|---|---|---|

Do not expand into full Result/Artifact architecture.

## 13. Standalone CLI Lifecycle Comparison

| Dimension | CLI | Product Persistent Execution Comparison | Evidence |
|---|---|---|---|

## 14. Legacy Execution Lifecycle

Document the legacy model separately.

Do not make deletion recommendations.

## 15. Structural Sharing / Separation Matrix

| Dimension | Lifecycle A | Lifecycle B | Classification | Evidence / Supporting Observations |
|---|---|---|---|---|

Classification:
- STRUCTURALLY_SHARED
- STRUCTURALLY_DISTINCT
- SEMANTICALLY_SIMILAR
- SEMANTICALLY_DISTINCT
- UNKNOWN

## 16. Execution Concept Inventory

Answer explicitly:

### 16.1 Distinct persistent Execution entities confirmed

List them.

### 16.2 Distinct physical Execution tables confirmed

List them.

### 16.3 Distinct state machines confirmed

List them.

### 16.4 Distinct worker claim mechanisms confirmed

List them.

### 16.5 Shared execution infrastructure confirmed

List only genuinely shared components.

### 16.6 Terminology collisions

Record cases where multiple structurally distinct entities are all called
`Execution`, `execution_id`, `retry`, etc.

Do not recommend renaming yet.

## 17. Phase 01 Unknown Carry-forward

| ID | Status | Phase 02 Evidence | Notes |
|---|---|---|---|

## 18. New Unresolved Items

| ID | Question | Confirmed Facts | Why Unresolved | Additional Evidence Needed |
|---|---|---|---|---|

## 19. Facts

Continue numbering from:

- E4-OBS-014
- E4-OBS-015
- ...

Every observation must contain evidence.

## 20. Inferences

Continue numbering from:

- E4-INF-006
- E4-INF-007
- ...

Every inference must reference supporting E4-OBS IDs.

If none:

`NONE`

## 21. Phase Conclusion

State only:

1. number of Lifecycle Units confirmed
2. number of persistent Execution entities confirmed
3. number of physical Execution tables confirmed
4. number of distinct state machines confirmed
5. number of distinct worker claim mechanisms confirmed
6. whether GenericExecutor owns Execution lifecycle or is subordinate to another lifecycle owner
7. whether standalone CLI participates in persistent Product Execution lifecycle
8. whether legacy lifecycle is structurally distinct from active Product lifecycle(s)
9. unresolved item count
10. whether evidence is sufficient to proceed to Result / Artifact ownership investigation

Do not recommend Target Architecture.

## 22. Completion Status

One of:

- COMPLETED
- COMPLETED_WITH_UNKNOWNS
- BLOCKED_WRONG_BRANCH
- BLOCKED
```

---

# 33. Mandatory Explicit Answers

Phase Conclusionとは別に、以下へ必ず一文で回答すること。

## A

```text
Does the active Product runtime have exactly one persistent Execution lifecycle model?
```

回答:

```text
YES
NO
UNKNOWN
```

＋根拠。

---

## B

```text
Do Causal, Exploratory, and Predictive executions persist through the same Execution entity/repository/table?
```

回答:

```text
YES
NO
PARTIALLY
UNKNOWN
```

＋根拠。

---

## C

```text
Do Causal, Exploratory, and Predictive executions share the same state-transition implementation?
```

同様に回答。

---

## D

```text
Do Causal, Exploratory, and Predictive executions share the same worker claim mechanism?
```

同様に回答。

---

## E

```text
Does GenericExecutor own the persistent Execution lifecycle?
```

回答:

```text
YES
NO
PARTIALLY
UNKNOWN
```

＋根拠。

---

## F

```text
Does the standalone CLI create or participate in the persistent Web/API Product Execution lifecycle?
```

回答:

```text
YES
NO
PARTIALLY
UNKNOWN
```

＋根拠。

---

## G

```text
Is the legacy Execution lifecycle structurally identical to any active Product Execution lifecycle?
```

回答:

```text
YES
NO
PARTIALLY
UNKNOWN
```

＋根拠。

`NO` は削除可能性を意味しない。

---

# 34. Prohibited Conclusions

以下は本Phaseでは書いてはならない。

```text
Causal Execution should become canonical.

Family Execution should be removed.

All executions should use one table.

GenericExecutor should own lifecycle.

Legacy Execution should be deleted.

CLI should use ExecutionService.

These services should be merged.

This schema should be migrated.

The architecture is wrong.

This duplication must be eliminated by ...
```

観測された重複を、

```text
STRUCTURALLY_DISTINCT
SEMANTICALLY_SIMILAR
```

と記録することは許可する。

改善策へ進んではならない。

---

# 35. Completeness Criteria

以下をすべて満たすこと。

### C1

Phase 01 resultを読んでいる。

### C2

active Product runtimeの全Execution processing branchを調査している。

### C3

distinct Execution entityを特定している。

### C4

repository / ORM / physical tableまで追跡している。

### C5

各主要Lifecycle Unitのstate machineを追跡している。

### C6

worker claim mechanismを比較している。

### C7

`GenericExecutor` の責務境界を確認している。

### C8

cancel / retry / rerun / reviseを区別している。

### C9

stage lifecycleを比較している。

### C10

主要transaction boundaryを確認している。

### C11

CLIがpersistent Execution lifecycleへ参加するか確認している。

### C12

legacy Execution lifecycleを比較対象として調査している。

### C13

Result linkageはExecution理解に必要な境界までに留めている。

### C14

Fact / Inference / Unknownを分離している。

### C15

新規Observation IDを `E4-OBS-014` 以降としている。

### C16

設計変更提案をしていない。

### C17

runtime executionをしていない。

### C18

指定result以外のRepository fileを変更していない。

---

# 36. Final Self-Check

result生成後、以下のみ実行する。

```text
git status --short
git diff --stat
git diff -- \
docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/architecture_review/02_execution_lifecycle_inventory_result.md
```

期待される新規変更:

```text
02_execution_lifecycle_inventory_result.md
```

既存working tree変更を自分の変更として扱わない。

変更・reset・restoreしてはならない。

---

# 37. Agent Response

作業完了時のchat responseは簡潔に以下を報告する。

```text
02_execution_lifecycle_inventory_result.md を生成しました。

Phase status: <...>
Lifecycle Units: <count>
Persistent Execution entities: <count>
Physical Execution tables: <count>
Distinct state machines: <count>
Unresolved items: <count>

Source/configuration/test/migration codeは変更していません。
```

詳細はresult文書を正本とする。

---

# 38. Stop Condition

以下のいずれかで停止する。

1. `02_execution_lifecycle_inventory_result.md` を生成し、Final Self-Checkを完了した
2. branch不一致
3. static investigationを継続できないblocking issue
4. result以外の変更なしには調査できないことが判明

停止後、以下へ進んではならない。

* runtime verification
* Result / Artifact詳細調査
* Lineage調査
* Phase 03
* Target Architecture決定
* implementation
* refactoring
* deletion
* migration変更
* Gate decomposition

次作業は人間によるresult review後、別promptとして指示される。
