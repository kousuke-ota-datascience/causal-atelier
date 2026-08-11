# 03 Result / Artifact Ownership Inventory — Architecture Review Prompt

## 1. Task

`ENH-E4 eliminate dual execution` の Architecture Review Phase 03 として、現在のRepositoryに存在する **Result / Artifact ownership model** を静的コード調査によってInventory化し、相互比較する。

本Phaseの中心目的は、

> active Product runtime に存在する複数のExecution lifecycleが、ResultおよびArtifactをどのentity / repository / table / serviceで所有し、生成・永続化・取得・削除・再利用しているか

をコード上のevidenceによって確定することである。

特に、Phase 02で確認された以下の二系統を重点比較する。

```text
Causal Execution
    ↓
product_result
    ↓
product_artifact
```

および

```text
Exploratory / Predictive Family Execution
    ↓
product_family_stage_execution
    ↓
product_family_result
    ↓
product_family_artifact
```

本Phaseでは、これらが

* 同じ意味モデルの重複実装なのか
* lifecycle上異なる意味を持つ別モデルなのか
* 部分的に共通し、部分的に異なるのか

を判定できるevidenceを集める。

ただし、Target Architectureや統合方法は決定しない。

このPhaseは **read-only architecture investigation** である。

Production code、test code、configuration、migration、dependency、database、runtime stateを変更してはならない。

唯一許可されるRepositoryへの書き込みは、指定されたresult文書の生成・更新だけである。

---

# 2. Positioning

Phase 01では、

```text
Runtime Root
→ Boundary Entry Point
→ First Execution Boundary
```

を確認した。

Phase 02では、

```text
Execution identity
→ persistence
→ lifecycle
→ claim
→ processing
→ stage
→ retry/rerun/revise
```

を確認した。

Phase 03では、

```text
Execution / Stage
    ↓
Result generation
    ↓
Result persistence
    ↓
Artifact generation
    ↓
Artifact persistence / object storage
    ↓
Result / Artifact read path
    ↓
cleanup / replacement / reuse
```

を調査する。

本PhaseはResult / Artifactの**現在のownership構造を確定するPhase**である。

以下はまだ行わない。

* canonical Result modelの決定
* canonical Artifact modelの決定
* table統合判断
* schema migration設計
* API統合設計
* Result ID統一設計
* Artifact ID統一設計
* Execution lifecycle統合
* Lineage architecture決定
* legacy削除判断
* implementation plan
* Gate decomposition

---

# 3. Repository / Investigation Context

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

前Phase results:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
architecture_review/
01_runtime_entrypoint_inventory_result.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
architecture_review/
02_execution_lifecycle_inventory_result.md
```

本Phase result出力先:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
architecture_review/
03_result_artifact_ownership_inventory_result.md
```

調査開始時点のcommit SHAを必ず記録すること。

---

# 4. Required Use of Prior Evidence

調査開始時にPhase 01およびPhase 02 resultを読むこと。

特にPhase 02で確定した、

* Lifecycle Unit IDs
* Execution entity
* physical Execution tables
* stage persistence
* Result linkage
* worker processing boundaries
* unresolved items

を引き継ぐこと。

既存の `E4-LC-*` IDを変更・再採番してはならない。

Observation / Inference / Unknown IDについては、

> Phase 02 result内で実際に使用されている最大番号

を確認し、その次の番号から続けること。

番号を推測してはならない。

例:

```text
max existing observation = E4-OBS-027
→ Phase 03 starts from E4-OBS-028
```

同様に、

```text
E4-INF-*
E4-UNK-*
```

についても既存最大番号から継続する。

---

# 5. Core Investigation Question

最終的に以下へ回答できる状態にすること。

> Causal / Exploratory / Predictive executionが生成するResultおよびArtifactは、同じconceptual ownership modelを異なるtableで実装しているのか、それとも異なるlifecycle semanticsを持つ独立したdomain conceptなのか。

この問いを、

```text
identity
ownership
cardinality
persistence
creation timing
stage association
storage
consumer
downstream reuse
mutation
cleanup
retry/rerun semantics
lineage reference
```

の各dimensionから調査する。

---

# 6. Terminology

## 6.1 Result

本Phaseでは、ExecutionまたはStageの処理結果として永続化されるdomain / persistence objectをResultと呼ぶ。

単なるPython return valueはpersistent Resultと区別する。

---

## 6.2 Artifact

Resultに関連し、

* file
* dataset
* model
* plot
* serialized object
* binary object
* structured data object
* external storage object

等として保存・参照されるものをArtifact候補とする。

コード上の実際の定義に従うこと。

---

## 6.3 Result Owner

Resultのlifecycleを管理する責務を持つcomponent。

少なくとも以下を調査する。

* ID generation
* creation
* persistence
* association
* read
* delete
* replacement
* retry/rerun handling

---

## 6.4 Artifact Owner

Artifact metadataまたはphysical objectのlifecycleを管理するcomponent。

metadata ownershipとphysical object ownershipを区別すること。

---

# 7. Primary Investigation Targets

最低限以下を調査すること。

## 7.1 Causal Result

Phase 02で確認されたCausal lifecycleから、

```text
Execution
→ processing output
→ Result creation
→ Result repository
→ Result ORM
→ product_result
```

を追跡する。

確認すること:

* Result domain entity
* Result ID
* Result kind/type
* Execution relation
* creation owner
* persistence owner
* completionとのtransaction関係
* read API
* update/deleteの有無
* Artifact relation

---

## 7.2 Causal Artifact

```text
Result
→ Artifact metadata
→ Artifact repository / ORM
→ product_artifact
→ physical object/storage
```

を追跡する。

確認すること:

* Artifact ID
* Result relation
* Execution relationの有無
* type/kind
* URI/path/key
* MIME/media type
* metadata
* storage backend
* object creation
* object deletion
* metadata deletion
* physical object deletion
* Result deletion時の挙動

---

## 7.3 Exploratory Family Result

Phase 02のExploratory lifecycleから、

```text
FamilyExecution
→ StageExecution
→ processing output
→ FamilyResult
→ product_family_result
```

を追跡する。

Causal Resultとの構造差を確認する。

---

## 7.4 Predictive Family Result

Predictiveについて同様に調査する。

Exploratoryと同じtable/entityを共有する場合でも、

* Result kind
* Result payload
* stage semantics
* downstream usage
* Artifact creation

が同一か確認する。

同じORMを使っているだけで同じsemantic modelと断定してはならない。

---

## 7.5 Family Artifact

```text
FamilyResult
→ FamilyArtifact
→ product_family_artifact
→ physical object/storage
```

を追跡する。

Causal Artifactとのstorage backend共有有無も確認する。

---

## 7.6 Legacy Result / Artifact

legacy architectureにResult / Artifact相当のmodelが存在する場合は比較対象としてInventory化する。

ただしPhase 01のruntime reachability classificationは変更しない。

目的は、

> active Product Result / Artifactとlegacy Result / Artifactの意味的・構造的重複

を後続Architecture Decisionで判断できるevidenceを残すことである。

削除可否は判断しない。

---

# 8. Result Identity

各Result modelについて確認する。

* ID field
* ID type
* generator
* namespace
* physical primary key
* API-visibleか
* UI-visibleか
* Executionとのforeign key
* Stageとのforeign key
* parent/base/result relation
* retry/rerun間のrelation

以下のmatrixを作成する。

| Result Model | Result ID | Generator | Table | Execution FK | Stage FK | API-visible | Evidence |
| ------------ | --------- | --------- | ----- | ------------ | -------- | ----------- | -------- |

---

# 9. Artifact Identity

各Artifact modelについて、

| Artifact Model | Artifact ID | Generator | Table | Result FK | Execution FK | Storage Locator | Evidence |
| -------------- | ----------- | --------- | ----- | --------- | ------------ | --------------- | -------- |

を作成する。

Artifact metadata IDとphysical storage keyが異なる場合は明確に区別する。

---

# 10. Ownership Chain

各Lifecycle Unitについて、

```text
Execution owner
→ Result owner
→ Artifact metadata owner
→ Artifact physical storage owner
```

を明示する。

以下を作る。

| Lifecycle | Execution Owner | Result Owner | Artifact Metadata Owner | Physical Storage Owner | Evidence |
| --------- | --------------- | ------------ | ----------------------- | ---------------------- | -------- |

「同一service内にある」ことと「同一domain ownership」であることを混同しない。

---

# 11. Cardinality

以下をコード/schemaから確認する。

```text
Execution : Result
Stage : Result
Result : Artifact
Execution : Artifact
```

可能な分類:

```text
1:1
1:N
0..1
0..N
UNKNOWN
```

DB constraint、repository query、service implementation等をevidenceに使う。

単にPython type annotationだけからcardinalityを断定しない。

---

# 12. Creation Timing

各Result / Artifactがいつ生成されるか確認する。

例:

```text
before execution completion
per stage
after all stages
only on success
also on failure
on API request
lazy
eager
```

以下を作る。

| Model | Creation Trigger | Before/After Terminal State | Transaction Coupling | Evidence |
| ----- | ---------------- | --------------------------- | -------------------- | -------- |

---

# 13. Stage Ownership

Phase 02ではCausalとFamily系でstage persistenceに非対称性が確認されている。

本PhaseではResult側からその意味を確認する。

特に、

### Causal

* ResultがExecution単位か
* GenericExecutorのstage outputがどのようにResultへ集約されるか
* individual stage Resultがpersistent conceptとして存在するか

### Family

* ResultがStage単位か
* Execution単位Resultも存在するか
* StageExecutionとResultのcardinality
* final Resultの概念が存在するか

を調査する。

「Causalにpersistent stage tableがない」ことだけからResult semanticsを推測してはならない。

---

# 14. Payload / Semantic Content

Result modelごとに、

* stored fields
* payload structure
* type/kind discriminator
* metrics
* summaries
* data references
* model references
* diagnostics
* error representation

等を確認する。

ただし個々のscientific algorithmの中身までは深掘りしない。

目的は、

> Resultというdomain conceptが何を表現しているか

を比較可能にすることである。

以下を作る。

| Result Model | Semantic Unit | Payload Shape | Kind/Type | Stage-scoped? | Execution-scoped? | Evidence |
| ------------ | ------------- | ------------- | --------- | ------------: | ----------------: | -------- |

---

# 15. Artifact Semantic Content

Artifactについて、

* file-like
* dataset-like
* model-like
* visualization-like
* generic binary
* generic object reference

等、コード上確認できるcategoryを整理する。

Causal / Familyで同じArtifact kind vocabularyを共有しているか確認する。

---

# 16. Physical Storage Investigation

Artifact metadataとphysical objectの保存先を調査する。

確認すること:

* filesystem
* object store
* database blob
* URI
* storage adapter
* path construction
* key generation
* serialization
* content hashing
* deduplication
* write atomicity
* cleanup

存在しない項目は `NONE_CONFIRMED`。

storage backendが共通でもmetadata ownershipが別なら、それを明示する。

---

# 17. Result Read Paths

各Result modelについてconsumerを調査する。

最低限:

* HTTP API
* UI
* downstream application service
* worker
* lineage service
* export/download
* CLI

以下を作る。

| Result Model | Consumer | Read Symbol / Endpoint | Purpose | Evidence |
| ------------ | -------- | ---------------------- | ------- | -------- |

Resultが生成されるだけで読まれていない場合も記録する。

---

# 18. Artifact Read Paths

同様に、

| Artifact Model | Consumer | Endpoint / Symbol | Metadata-only / Physical Data | Evidence |
| -------------- | -------- | ----------------- | ----------------------------- | -------- |

を作る。

---

# 19. UI Exposure

Repository-managed frontendが存在する場合、

Causal / Exploratory / Predictive Resultについて、

* list
* detail
* visualization
* download
* artifact display

等のUI exposureを確認する。

目的は、

> user-visible Result abstractionが共通か、family別に分離しているか

を観測することである。

UI designの評価は行わない。

---

# 20. Downstream Reuse

特に重要。

Result / Artifactが後続Executionのinputとして利用されるか確認する。

以下の経路を検索する。

```text
Result ID
→ input binding
→ source reference
→ plan input
→ downstream execution
```

または、

```text
Artifact ID
→ binding
→ stage input
→ scientific runner
```

確認すること:

* Causal ResultをCausal downstreamで使えるか
* Causal ResultをFamily executionで使えるか
* Family ResultをCausal executionで使えるか
* Family Resultを別Family executionで使えるか
* Artifact IDで参照するか
* Result IDで参照するか
* physical URIで参照するか
* conversion/adaptorが存在するか

静的証拠がなければ `NONE_CONFIRMED` または `UNKNOWN` とする。

---

# 21. Cross-Model Interoperability Matrix

必ず以下を作る。

| Producer        | Consumer Causal | Consumer Exploratory | Consumer Predictive | Evidence |
| --------------- | --------------- | -------------------- | ------------------- | -------- |
| Causal Result   |                 |                      |                     |          |
| Causal Artifact |                 |                      |                     |          |
| Family Result   |                 |                      |                     |          |
| Family Artifact |                 |                      |                     |          |

各cellは、

```text
SUPPORTED
PARTIALLY_SUPPORTED
NO_PATH_CONFIRMED
UNKNOWN
```

のいずれかとする。

`NO_PATH_CONFIRMED` は「設計上禁止」を意味しない。

---

# 22. Retry / Rerun / Revise Result Semantics

Phase 02で確認されたmutation operationについて、

Result / Artifact側の挙動を追跡する。

確認すること:

* existing Resultを残すか
* deleteするか
* overwriteするか
* new Resultを作るか
* source Result relationを保存するか
* old Artifactを残すか
* new Artifactを作るか
* storage objectを再利用するか
* stage Resultを再利用するか

以下を作る。

| Lifecycle | Operation | Existing Result | New Result | Existing Artifact | New Artifact | Relation Preserved | Evidence |
| --------- | --------- | --------------- | ---------- | ----------------- | ------------ | ------------------ | -------- |

---

# 23. Failure Result Semantics

Execution失敗時に、

* Result rowが存在するか
* partial Resultが保存されるか
* completed stage Resultが残るか
* Artifactが残るか
* cleanupされるか
* failure detailsがResultに入るかExecutionに入るか

を確認する。

Causal / Familyで差がある場合は明示する。

---

# 24. Cancellation Result Semantics

cancel時についても同様に調査する。

特に、

```text
queued cancel
running cancel
partial stage completion
```

でResult / Artifactの扱いが異なるか確認する。

---

# 25. Deletion / Cleanup Ownership

Result / Artifactの削除経路を調査する。

検索対象:

```text
delete
remove
cleanup
purge
cascade
orphan
unlink
expire
```

確認すること:

* Execution deletion
* Result deletion
* Artifact metadata deletion
* physical object deletion
* cascade FK
* ORM cascade
* application-managed cleanup
* retry/revise cleanup
* orphan prevention

以下を作る。

| Trigger | Result Metadata | Artifact Metadata | Physical Object | Owner | Evidence |
| ------- | --------------- | ----------------- | --------------- | ----- | -------- |

削除経路が存在しない場合は `NONE_CONFIRMED`。

---

# 26. Transaction Boundaries

主要操作について、

```text
Execution terminal transition
Result write
Artifact metadata write
physical object write
```

のtransaction / atomicityを調査する。

特に、

* DB ResultとExecution completionが同一transactionか
* Artifact metadataとResultが同一transactionか
* physical storage writeとDB commitの順序
* storage write失敗時のrollback
* DB commit失敗時のorphan storage object

を確認する。

実際のコード上確認できる範囲だけ記録する。

atomicityの良し悪しは評価しない。

---

# 27. Result / Artifact Repository Abstraction

以下を比較する。

```text
domain repository interface
SQLAlchemy repository
direct ORM access
service-local persistence
UoW-mediated access
```

特にCausalとFamilyで、

> repository abstraction levelが異なるか

を確認する。

これはstructural factとして記録してよい。

「統一すべき」とは書かない。

---

# 28. Lineage Boundary Investigation

Lineage architecture自体はPhase 04で詳細調査する。

本Phaseでは **Result / Artifact ownershipを理解するために必要な境界だけ** 確認する。

以下を調べる。

* Lineage codeがResult IDを参照するか
* Artifact IDを参照するか
* Execution IDを参照するか
* Family Resultを参照できるか
* Causal Resultを参照できるか
* persisted lineage edgeがどのentity IDsを保持するか
* derived lineage builderがどのrelationshipを読むか

ここでは、

* canonical lineage model
* persisted vs derivedの選択
* lineage再設計

を決定してはならない。

---

# 29. Lineage Compatibility Matrix

以下のみ作成する。

| Entity Type      | Referenced by Derived Lineage | Referenced by Persisted Lineage | Evidence |
| ---------------- | ----------------------------- | ------------------------------- | -------- |
| Causal Execution |                               |                                 |          |
| Causal Result    |                               |                                 |          |
| Causal Artifact  |                               |                                 |          |
| Family Execution |                               |                                 |          |
| Family Stage     |                               |                                 |          |
| Family Result    |                               |                                 |          |
| Family Artifact  |                               |                                 |          |

値:

```text
YES
NO_PATH_CONFIRMED
PARTIAL
UNKNOWN
```

詳細判断はPhase 04へ残す。

---

# 30. Semantic Equivalence Analysis

本Phaseで最も重要な比較の一つ。

Causal ResultとFamily Resultについて、以下をdimensionごとに比較する。

```text
identity
owner
scope
cardinality
creation timing
payload
stage association
consumer
downstream reuse
retry behavior
failure behavior
deletion
lineage participation
```

同様にCausal ArtifactとFamily Artifactを比較する。

Classification:

### `STRUCTURALLY_SHARED`

同一entity / repository / table / implementation等を実際に共有。

### `STRUCTURALLY_DISTINCT`

異なるentity / table / repository等を使用。

### `SEMANTICALLY_EQUIVALENT_CANDIDATE`

構造は別だが、観測された意味・lifecycle・consumerが高い一致を示す。

必ず `INFERENCE` とする。

### `SEMANTICALLY_OVERLAPPING`

一部の責務・意味は共通するが、重要な差異がある。

必ず差異を列挙する。

### `SEMANTICALLY_DISTINCT`

scope / lifecycle / payload / consumer等に明確な意味差がある。

### `UNKNOWN`

証拠不足。

---

# 31. Critical Distinctions

以下を混同しないこと。

## 31.1 Same storage backend ≠ same Artifact model

同じfilesystem/object storeを使っていてもmetadata ownershipが別なら区別する。

---

## 31.2 Same payload format ≠ same Result semantics

同じJSON構造でもowner / scope / lifecycleが異なる可能性がある。

---

## 31.3 Different table ≠ different domain meaning

tableが別というだけでsemantic distinctionを断定しない。

---

## 31.4 Same table ≠ same lifecycle meaning

Exploratory / Predictiveが同じfamily tableを使っていても、service semanticsが異なる可能性がある。

---

## 31.5 Result creation ≠ Result ownership

Resultを組み立てるcomponentとpersistent lifecycleを所有するcomponentを区別する。

---

## 31.6 Artifact metadata ≠ physical Artifact

DB rowとfilesystem/object store objectを区別する。

---

## 31.7 Lineage reference ≠ Result ownership

LineageがResultを参照することとResult lifecycleを所有することは別。

---

# 32. Required Source Scope

Repository全体を対象とする。

最低限以下を確認する。

## 32.1 Product Domain

```text
src/ariadne/product/domain/**
```

Result / Artifact / Execution / Stage関連entity。

---

## 32.2 Product Application

```text
src/ariadne/product/application/**
```

creation / read / mutation / cleanup / downstream reuse。

---

## 32.3 Product Persistence

```text
src/ariadne/product/persistence/**
```

ORM / repository / UoW / table mapping。

---

## 32.4 Workflow / Executor

```text
src/ariadne/product/workflow/**
```

stage outputからResultへの変換境界。

---

## 32.5 Worker

```text
src/ariadne/interfaces/worker/**
```

processing completionとResult persistence。

---

## 32.6 Web API

```text
src/ariadne/interfaces/web_api/**
```

Result / Artifact read endpoint、download、rerun/revise等。

---

## 32.7 Frontend

Repository-managed frontend全体。

Result / Artifact consumerを確認する。

---

## 32.8 Legacy

```text
src/ariadne/legacy/**
```

Result / Artifact相当model。

---

## 32.9 Migration

Productおよびlegacy migrationをread-onlyで確認してよい。

目的は、

* table
* FK
* unique constraint
* cascade
* index

の物理schema確認。

---

## 32.10 Tests

read-onlyで参照してよい。

優先順位:

```text
production implementation / schema
>
test
>
comments / documentation
```

---

# 33. Investigation Method

静的解析のみ使用する。

使用可:

* `git`
* `git grep`
* `rg`
* `grep`
* `find`
* `sed`
* `cat`
* `awk`
* `tree`
* read-only AST解析
* source / schema / test閲覧

必要な検索はAgent自身で追加してよい。

---

# 34. Prohibited Operations

禁止:

* production code変更
* test変更
* configuration変更
* migration変更
* dependency変更
* dependency install
* formatter
* auto-fix
* code generation
* DB変更
* DB reset
* migration execution
* container操作
* application起動
* worker起動
* frontend起動
* test実行
* benchmark
* HTTP request
* external API
* network調査
* application module実行
* architecture変更
* refactoring
* deletion
* documentation修正

唯一許可される書き込み:

```text
03_result_artifact_ownership_inventory_result.md
```

および必要なparent directoryのみ。

---

# 35. Do Not Execute Runtime Code

禁止例:

```text
pytest
uvicorn ...
python -m ...
docker compose up
alembic ...
curl ...
```

Python使用時もapplication moduleをimportして実行してはならない。

runtime verificationが必要な事項はUnknownに残す。

---

# 36. Investigation Procedure

## Step 1. Record Baseline

取得:

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

---

## Step 2. Read Phase 01 / Phase 02 Results

既存Lifecycle UnitおよびID continuityを確認する。

---

## Step 3. Discover Result / Artifact Models

Repository全体から、

```text
Result
Artifact
FamilyResult
FamilyArtifact
result_id
artifact_id
result_uri
artifact_uri
output
materialization
```

等を探索する。

名称だけに依存しない。

---

## Step 4. Build Persistence Map

各modelについて、

```text
Domain
→ Application
→ Repository
→ ORM
→ Physical Table
```

を追跡する。

---

## Step 5. Trace Creation

各Execution lifecycleからResult / Artifact生成まで追跡する。

---

## Step 6. Trace Read Consumers

API / UI / service / worker / lineage / downstream executionを調査する。

---

## Step 7. Trace Storage

Artifact metadataからphysical storageまで追跡する。

---

## Step 8. Trace Mutation Semantics

cancel / retry / rerun / revise / failureに伴うResult / Artifact lifecycleを調べる。

---

## Step 9. Trace Deletion / Cleanup

metadataとphysical objectを分離して追跡する。

---

## Step 10. Trace Downstream Reuse

cross-execution input利用を検索する。

---

## Step 11. Trace Lineage Boundary

Result / Artifact IDsとlineageとの接続だけ確認する。

---

## Step 12. Compare Causal vs Family

semantic equivalence / overlap / distinctionをdimensionごとに整理する。

---

## Step 13. Compare Legacy

legacy modelが存在すれば比較する。

---

## Step 14. Record Unknowns

証拠不足を推測で埋めない。

---

# 37. Evidence Standard

主要主張には、

```text
<repository-relative-path>:<line-range>
Symbol: <symbol>
Evidence: <what this proves>
```

を付ける。

Ownership chainは可能な限りedge単位で証明する。

例:

```text
ExecutionProcessor → Result creation
Evidence: ...

Result creation → Result repository
Evidence: ...

Result repository → product_result
Evidence: ...
```

---

# 38. Physical Schema Evidence

table / FK / cascade等については可能なら、

```text
ORM definition
+
migration definition
```

の二重確認を行う。

不一致があればdiscrepancyとして記録する。

---

# 39. Fact / Inference / Unknown

## `FACT`

直接確認された内容。

## `INFERENCE`

複数Factから導かれる内容。

supporting `E4-OBS-*` を示す。

## `UNKNOWN`

静的証拠不足。

必要な追加evidenceを記載する。

---

# 40. Result / Artifact Model IDs

独立したpersistent Result modelには、

```text
E4-RS-001
E4-RS-002
...
```

を付ける。

独立したpersistent Artifact modelには、

```text
E4-AR-001
E4-AR-002
...
```

を付ける。

既存Lifecycle Unitとのrelationを明示する。

例:

```text
E4-LC-001
→ E4-RS-001
→ E4-AR-001
```

事前にモデル数を仮定しない。

---

# 41. Required Result Structure

`03_result_artifact_ownership_inventory_result.md` は以下の構造とする。

```markdown
# 03 Result / Artifact Ownership Inventory Result

## 1. Metadata

- Prompt:
- Prior phases:
- Repository root:
- Branch:
- HEAD:
- Working tree status:
- Started at:
- Finished at:
- Phase status:

## 2. Executive Summary

### 2.1 Result Models

| Result ID | Name | Lifecycle Units | Entity | Table | Owner |
|---|---|---|---|---|---|

### 2.2 Artifact Models

| Artifact ID | Name | Result Model | Entity | Table | Storage |
|---|---|---|---|---|---|

### 2.3 High-Level Ownership

| Lifecycle | Result Model | Artifact Model | Result Owner | Artifact Owner |
|---|---|---|---|---|

## 3. Result Model Details

### E4-RS-001 — ...

#### Semantic Unit

#### Identity

#### Execution / Stage Relation

#### Creation

#### Persistence

#### Payload

#### Consumers

#### Downstream Reuse

#### Mutation Semantics

#### Deletion

#### Lineage Boundary

#### Evidence

#### Unknowns

Repeat.

## 4. Artifact Model Details

### E4-AR-001 — ...

#### Semantic Unit

#### Identity

#### Result Relation

#### Metadata

#### Physical Storage

#### Creation

#### Read Path

#### Cleanup

#### Downstream Reuse

#### Lineage Boundary

#### Evidence

#### Unknowns

Repeat.

## 5. Ownership Chain Matrix

| Lifecycle | Execution Owner | Result Owner | Artifact Metadata Owner | Physical Storage Owner | Evidence |
|---|---|---|---|---|---|

## 6. Result Identity Matrix

| Result Model | ID | Generator | Table | Execution FK | Stage FK | API-visible | Evidence |
|---|---|---|---|---|---|---|---|

## 7. Artifact Identity Matrix

| Artifact Model | ID | Generator | Table | Result FK | Execution FK | Storage Locator | Evidence |
|---|---|---|---|---|---|---|---|

## 8. Cardinality Matrix

| Lifecycle | Execution:Result | Stage:Result | Result:Artifact | Evidence |
|---|---|---|---|---|

## 9. Result Semantic Comparison

| Dimension | Causal Result | Exploratory Result | Predictive Result | Classification |
|---|---|---|---|---|

## 10. Artifact Semantic Comparison

| Dimension | Causal Artifact | Family Artifact | Classification | Evidence |
|---|---|---|---|---|

## 11. Creation / Completion Coupling

| Model | Creation Trigger | Terminal State Coupling | Transaction | Evidence |
|---|---|---|---|---|

## 12. Stage / Result Ownership

Explain Causal vs Family stage/result relationships.

## 13. Physical Storage Comparison

| Artifact Model | Metadata Store | Physical Store | Key/URI | Writer | Deleter | Evidence |
|---|---|---|---|---|---|---|

## 14. Read / Consumer Matrix

| Model | API | UI | Worker | Service | Lineage | Other |
|---|---|---|---|---|---|---|

## 15. Downstream Reuse

### 15.1 Input Reference Mechanisms

### 15.2 Cross-Model Interoperability

| Producer | Causal | Exploratory | Predictive | Evidence |
|---|---|---|---|---|

## 16. Mutation Semantics

### 16.1 Cancel

### 16.2 Retry

### 16.3 Rerun

### 16.4 Revise

Use detailed matrices.

## 17. Failure / Partial Result Semantics

| Lifecycle | Failure Result | Partial Result | Artifact Retention | Evidence |
|---|---|---|---|---|

## 18. Deletion / Cleanup

| Trigger | Result Metadata | Artifact Metadata | Physical Object | Owner | Evidence |
|---|---|---|---|---|---|

## 19. Transaction Boundaries

| Operation | DB Writes | Storage Writes | Commit Ordering | Atomic Scope | Evidence |
|---|---|---|---|---|---|

## 20. Repository Abstraction Comparison

| Model | Repository Interface | Implementation | Direct ORM? | UoW? | Evidence |
|---|---|---|---:|---:|---|

## 21. Lineage Compatibility Boundary

| Entity Type | Derived Lineage | Persisted Lineage | Evidence |
|---|---|---|---|

Do not decide lineage architecture.

## 22. Legacy Result / Artifact Comparison

If present.

## 23. Structural / Semantic Classification

| Model A | Model B | Dimension | Classification | Evidence |
|---|---|---|---|---|

## 24. Result / Artifact Concept Inventory

### 24.1 Distinct persistent Result entities

### 24.2 Distinct Result tables

### 24.3 Distinct persistent Artifact entities

### 24.4 Distinct Artifact tables

### 24.5 Shared physical storage infrastructure

### 24.6 Shared Result / Artifact abstractions

### 24.7 Terminology collisions

## 25. Prior Unknown Carry-forward

| ID | Status | Phase 03 Evidence | Notes |
|---|---|---|---|

## 26. New Unresolved Items

| ID | Question | Confirmed Facts | Why Unresolved | Additional Evidence Needed |
|---|---|---|---|---|

## 27. Facts

Continue E4-OBS numbering from the highest existing prior-phase ID.

## 28. Inferences

Continue E4-INF numbering from the highest existing prior-phase ID.

## 29. Phase Conclusion

State only:

1. number of persistent Result models
2. number of Result physical tables
3. number of persistent Artifact models
4. number of Artifact physical tables
5. whether Causal and Family Results are structurally shared
6. whether they are semantic-equivalence candidates, overlapping, distinct, or unknown
7. whether Causal and Family Artifacts are structurally shared
8. whether Artifact physical storage is shared
9. whether Result models are cross-lifecycle reusable
10. whether Result/Artifact participation in lineage differs
11. unresolved item count
12. whether evidence is sufficient to proceed to dedicated Lineage investigation

Do not recommend Target Architecture.

## 30. Completion Status

One of:

- COMPLETED
- COMPLETED_WITH_UNKNOWNS
- BLOCKED_WRONG_BRANCH
- BLOCKED
```

---

# 42. Mandatory Explicit Answers

以下へ必ず回答する。

## A

```text
Do Causal and Family executions persist Results through the same entity/repository/table?
```

回答:

```text
YES
NO
PARTIALLY
UNKNOWN
```

＋evidence。

---

## B

```text
Do Causal and Family executions persist Artifacts through the same entity/repository/table?
```

同様。

---

## C

```text
Are Causal Result and Family Result structurally distinct but semantically equivalent candidates?
```

回答:

```text
YES
NO
PARTIALLY
UNKNOWN
```

「YES」は統合すべきという意味ではない。

---

## D

```text
Are Causal Artifact and Family Artifact structurally distinct but semantically equivalent candidates?
```

同様。

---

## E

```text
Is Result ownership execution-scoped, stage-scoped, or both for each active lifecycle?
```

Lifecycleごとに明示する。

---

## F

```text
Do all active Product Result models support the same downstream reuse mechanism?
```

回答:

```text
YES
NO
PARTIALLY
UNKNOWN
```

＋evidence。

---

## G

```text
Do all active Product Artifact models use the same physical storage infrastructure?
```

回答:

```text
YES
NO
PARTIALLY
UNKNOWN
```

＋evidence。

---

## H

```text
Are Result and Artifact persistence coupled atomically with Execution completion?
```

Lifecycleごとに:

```text
YES
NO
PARTIALLY
UNKNOWN
```

＋evidence。

---

## I

```text
Can Causal and Family Result/Artifact entities participate in the same lineage mechanisms?
```

回答:

```text
YES
NO
PARTIALLY
UNKNOWN
```

＋evidence。

詳細なlineage interpretationは行わない。

---

## J

```text
Does retry/rerun/revise preserve, replace, or duplicate existing Results and Artifacts?
```

Lifecycle / operationごとに明示する。

---

# 43. Prohibited Conclusions

本Phaseでは以下を書いてはならない。

```text
product_result should be canonical.

product_family_result should be removed.

The two Result tables should be merged.

The Artifact tables should be merged.

Stage results should move to product_result.

Causal should adopt family Result semantics.

Family should adopt causal Result semantics.

All artifacts should use one repository.

Lineage should be derived only.

Persisted lineage should be removed.

This duplication should be fixed by ...

The schema should be migrated to ...
```

観測された重複について、

```text
STRUCTURALLY_DISTINCT
SEMANTICALLY_OVERLAPPING
SEMANTICALLY_EQUIVALENT_CANDIDATE
```

と分類することは許可する。

---

# 44. Completeness Criteria

以下をすべて満たすこと。

### C1

Phase 01 / 02 resultsを読んでいる。

### C2

active Causal Result lifecycleを調査している。

### C3

active Exploratory Result lifecycleを調査している。

### C4

active Predictive Result lifecycleを調査している。

### C5

Causal / Family Artifact persistenceを調査している。

### C6

Result / Artifact entity → repository → ORM → tableを追跡している。

### C7

physical Artifact storageまで追跡している。

### C8

Execution / Stageとのcardinalityを確認している。

### C9

Result creation timingを確認している。

### C10

Result / Artifact consumerを確認している。

### C11

downstream reuseを調査している。

### C12

cross-model interoperabilityを調査している。

### C13

retry / rerun / revise / cancel / failure時の扱いを調査している。

### C14

deletion / cleanupを調査している。

### C15

主要transaction boundaryを確認している。

### C16

Lineageとの接続境界のみ確認している。

### C17

legacy Result / Artifactが存在する場合は比較している。

### C18

Fact / Inference / Unknownを分離している。

### C19

prior-phase ID numberingを実ファイルから継続している。

### C20

Target Architecture提案をしていない。

### C21

runtime executionをしていない。

### C22

指定result以外のRepository fileを変更していない。

---

# 45. Final Self-Check

result生成後、以下のみ実行する。

```text
git status --short

git diff --stat

git diff -- \
docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/architecture_review/03_result_artifact_ownership_inventory_result.md
```

期待される新規変更:

```text
03_result_artifact_ownership_inventory_result.md
```

既存working tree変更を変更・reset・restoreしてはならない。

---

# 46. Agent Response

作業完了時のchat responseは簡潔に以下を報告する。

```text
03_result_artifact_ownership_inventory_result.md を生成しました。

Phase status: <...>
Persistent Result models: <count>
Result tables: <count>
Persistent Artifact models: <count>
Artifact tables: <count>
Unresolved items: <count>

Source/configuration/test/migration codeは変更していません。
```

詳細はresult文書を正本とする。

---

# 47. Stop Condition

以下のいずれかで停止する。

1. `03_result_artifact_ownership_inventory_result.md` を生成し、Final Self-Checkを完了した
2. branch不一致
3. static investigationを継続できないblocking issue
4. result以外の変更なしでは調査不能

停止後、以下へ進んではならない。

* runtime verification
* Phase 04
* dedicated Lineage architecture analysis
* Target Architecture決定
* implementation
* refactoring
* deletion
* migration変更
* Gate decomposition

次作業は人間によるresult review後、別promptとして指示される。
