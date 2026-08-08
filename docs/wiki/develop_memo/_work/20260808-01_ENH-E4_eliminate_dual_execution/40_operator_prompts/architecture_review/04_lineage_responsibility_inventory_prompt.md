# 04 Lineage Responsibility Inventory — Architecture Review Prompt

## 1. Task

`ENH-E4 eliminate dual execution` の Architecture Review Phase 04 として、現在のRepositoryに存在する **Lineage responsibility / representation / persistence model** を静的コード調査によってInventory化し、相互比較する。

本Phaseの中心目的は、

> 現在のAriadneでは、Execution / Stage / Result / Artifact / Dataset / Graph等のprovenance relationが、どの情報をsourceとして、誰によって生成され、どこへ永続化され、どのread pathでLineageとして提示されているか

をコード上のevidenceによって確定することである。

特に、前Phaseまでに確認された以下の二つを明確に分離して調査する。

```text
Typed relationship / FK
    ↓
query時にLineageとして導出
```

および

```text
application service
    ↓
LineageEdgeOrm
    ↓
persisted generic lineage edge
```

さらに、legacy architectureに存在するlineage modelも比較対象とする。

本Phaseでは、

> derived lineage と persisted lineage のどちらをcanonicalとすべきか

は決定しない。

このPhaseは **read-only architecture investigation** である。

Production code、test code、configuration、migration、dependency、database、runtime stateを変更してはならない。

唯一許可されるRepositoryへの書き込みは、指定されたresult文書の生成・更新だけである。

---

# 2. Positioning

Phase 01:

```text
Runtime Root
→ Execution entry point
```

Phase 02:

```text
Execution identity
→ lifecycle
→ persistence
→ worker
```

Phase 03:

```text
Execution / Stage
→ Result
→ Artifact
→ ownership / reuse / storage
```

Phase 04:

```text
Domain relationships
        │
        ├── derived lineage
        │
        └── persisted lineage
                 ↓
        read / traversal / closure
                 ↓
             API / UI
```

を調査する。

本PhaseではLineageの**現状責務とsource-of-truth構造**を確定する。

以下はまだ行わない。

* canonical lineage model決定
* persisted lineage削除判断
* derived lineageへの統一判断
* LineageEdge table削除判断
* schema migration設計
* Execution / Result / Artifact統合設計
* legacy削除判断
* API redesign
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

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
architecture_review/
03_result_artifact_ownership_inventory_result.md
```

本Phase result出力先:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
architecture_review/
04_lineage_responsibility_inventory_result.md
```

調査開始時点のcommit SHAを必ず記録すること。

---

# 4. Required Use of Prior Evidence

調査開始時にPhase 01〜03 resultをすべて読むこと。

特にPhase 03で確認された以下をinvestigation seedとして使用する。

```text
Causal:
typed FK / relationship に基づくderived lineageが確認されている

Family:
application servicesによるLineageEdgeOrm writeが確認されている

Product closure:
Causal / Family双方をcommon lineage representationへ読み込む

Causal generic persisted-lineage write:
完全なproduction pathは未確認
```

ただし、上記を無条件に結論として採用して調査を省略してはならない。

Phase 04ではlineage production / persistence / read logicそのものをproduction sourceから改めて追跡すること。

---

# 5. ID Continuity

既存resultから以下の最大番号を実際に確認する。

```text
E4-OBS-*
E4-INF-*
E4-UNK-*
```

Phase 04では各最大番号の次から採番する。

番号をprompt記載時点の想定で固定してはならない。

既存IDを変更・再採番してはならない。

Phase 03までのUnknownがPhase 04で解決した場合、

```text
RESOLVED_IN_PHASE_04
```

として既存IDを維持したままevidenceを追記する。

特に、Phase 03の

```text
E4-UNK-013
```

が存在する場合は、

> causal generic-lineage persistence path

を重点調査する。

---

# 6. Core Investigation Questions

最終的に以下へ回答できる状態にすること。

## Q1

現在のRepositoryには、独立したLineage representationが何種類存在するか。

---

## Q2

各Lineage representationは、

```text
derived
persisted
hybrid
legacy
```

のどれに該当するか。

---

## Q3

各Lineage edgeのsource factは何か。

例:

```text
Execution.input_result_id

Result.execution_id

Artifact.result_id

Artifact.execution_id

FamilyResult.execution_id

FamilyResult.stage_execution_id

FamilyArtifact.result_id

GraphVersion.source_result_id

DatasetVersion.source_artifact_id

persisted LineageEdge row

legacy ArtifactLineage
```

実際のコード/schemaに存在するものだけを記録する。

---

## Q4

誰がLineage edgeを生成するか。

```text
ExecutionProcessor
Exploratory service
Predictive service
closure service
repository
worker
API request
migration
legacy service
```

等をproduction codeから確認する。

---

## Q5

誰がLineageを読むか。

```text
API
closure/traversal
UI
export
rerun/revise
downstream execution
comparison
graph/version service
```

等を調査する。

---

## Q6

同じsemantic relationが、

```text
typed relationship
+
persisted generic edge
```

の双方で表現されるケースは存在するか。

---

## Q7

双方が存在する場合、

* deduplicateされるか
* precedenceがあるか
* unionされるか
* conflicting edgesを検出するか
* stale edgeを検出するか

を確認する。

---

## Q8

persisted lineage edgeがなくてもderived lineageを再構築できるrelationは何か。

逆に、

> persisted edgeにしか存在しないrelation

は何か。

---

## Q9

Causal / Exploratory / Predictiveでlineage generation semanticsは同一か。

---

## Q10

retry / rerun / revise / deletionによりLineageがどう変化するか。

---

# 7. Lineage Representation Definition

本Phaseでは、独立したlineage表現方式を `Lineage Representation` と呼ぶ。

以下のいずれかが独立していれば別representation候補とする。

* distinct physical lineage table
* typed relational derivation logic
* distinct graph/closure builder
* legacy lineage entity
* independently maintained lineage metadata

Lineage Representation ID:

```text
E4-LN-001
E4-LN-002
E4-LN-003
...
```

事前に個数を固定してはならない。

---

# 8. Lineage Node Inventory

Lineage graphに登場するnode typeを全てInventory化する。

最低限、存在を検索するもの:

```text
Execution
FamilyExecution
StageExecution
Result
FamilyResult
Artifact
FamilyArtifact
Dataset
DatasetVersion
Graph
GraphVersion
Export
Specification
Draft
Plan
legacy Artifact
legacy StageAttempt
legacy Result
```

実際にlineage graphへ参加するものだけを確定する。

以下を作る。

| Node Type | Persistent Entity | Table | Node ID | Representation(s) | Evidence |
| --------- | ----------------- | ----- | ------- | ----------------- | -------- |

---

# 9. Node Identity / Namespace

特にgeneric persisted lineageが存在する場合、

```text
source_type + source_id
target_type + target_id
```

等のnode identity表現を確認する。

確認すること:

* node type discriminator
* ID type
* UUID namespace
* table-specific uniqueness
* type+IDで一意か
* ID単体を使用する箇所があるか
* causal/familyでcollision可能性を防止する構造があるか

「UUIDだからcollisionしない」という推論は禁止する。

---

# 10. Edge Kind Inventory

全lineage edge kind / relation typeをInventory化する。

例示:

```text
PRODUCED
CONSUMED
DERIVED_FROM
INPUT_TO
OUTPUT_OF
REVISED_FROM
RERUN_OF
SOURCE_RESULT
SOURCE_ARTIFACT
...
```

これは例であり、存在しないkindを補完してはならない。

以下を作る。

| Edge Kind | Source Type(s) | Target Type(s) | Representation | Producer | Evidence |
| --------- | -------------- | -------------- | -------------- | -------- | -------- |

---

# 11. Typed / Derived Lineage

FKやdomain relationshipからquery時に生成されるLineageを調査する。

各derived edgeについて、

```text
typed relation
→ derivation code
→ emitted lineage edge
```

を追跡する。

以下を作る。

| Derived Edge | Source Fact | Derivation Symbol | Emitted Relation | Consumer | Evidence |
| ------------ | ----------- | ----------------- | ---------------- | -------- | -------- |

特に確認する。

* Causal Execution → Result
* Result → Artifact
* input Result → Execution
* Result → GraphVersion
* Artifact → DatasetVersion

および実際に存在するFamily relation。

---

# 12. Persisted Generic Lineage

generic lineage table/entityを特定する。

確認すること:

* ORM
* migration
* physical table
* PK
* source type/id
* target type/id
* edge kind
* metadata/context
* created_at
* unique constraint
* indexes
* FKの有無
* cascade behavior
* repository/service abstraction
* direct ORM usage

以下を作る。

| Property | Value | Evidence |
| -------- | ----- | -------- |

---

# 13. Persisted Edge Producers

`LineageEdgeOrm` 等へwriteするproduction symbolをRepository全体から検索する。

単純なclass reference一覧ではなく、

```text
business operation
→ application service
→ edge construction
→ DB write
→ commit
```

まで追跡する。

以下を作る。

| Producer ID | Lifecycle | Operation | Edge Kind | Source | Target | Transaction | Evidence |
| ----------- | --------- | --------- | --------- | ------ | ------ | ----------- | -------- |

Producer ID:

```text
E4-LP-001
E4-LP-002
...
```

---

# 14. Causal Lineage Write Path

重点調査項目。

Causal executionについて、

```text
submission
processing
Result creation
Artifact creation
retry
rerun
GraphVersion creation
DatasetVersion creation
```

等のbusiness operationからgeneric persisted lineage writeが行われるかを追跡する。

必ず以下を回答する。

```text
Does normal Causal Execution processing write generic persisted lineage edges?
```

回答:

```text
YES
NO_PATH_CONFIRMED
PARTIALLY
UNKNOWN
```

＋evidence。

Phase 03のcausal generic-lineage persistence Unknownを可能な限り解消する。

---

# 15. Exploratory Lineage Write Path

Exploratoryについて、

```text
execution creation
stage processing
Result creation
Artifact creation
downstream specification/draft
```

等からgeneric persisted lineage writeを追跡する。

---

# 16. Predictive Lineage Write Path

Predictiveについて、

```text
execution
stage
Result
Artifact
split
retry
rerun
revise
```

のlineage writeを追跡する。

Phase 03で確認されたretry cleanup / revise relationについて特に確認する。

---

# 17. Persisted Edge Readers

generic lineage tableをreadする全主要production pathを調査する。

以下を作る。

| Reader | Query | Filters | Purpose | Returned Representation | Evidence |
| ------ | ----- | ------- | ------- | ----------------------- | -------- |

特に、

* lineage API
* closure service
* UI-facing service
* export
* retry/revise
* delete cleanup

を調査する。

---

# 18. Derived Edge Readers

typed relationからLineageを構築するread pathについて同様に調査する。

---

# 19. Closure / Traversal Algorithm

Lineage closure / traversal logicを重点調査する。

確認すること:

* BFS / DFS / recursive SQL等
* depth limit
* upstream/downstream direction
* node type filtering
* edge kind filtering
* cycle detection
* deduplication
* deterministic ordering
* pagination
* causal/family union
* persisted/derived union

algorithmの良し悪しは評価しない。

---

# 20. Representation Merge Semantics

derived edgeとpersisted edgeを同一responseへまとめる場合、

merge処理を詳細に追跡する。

以下を確認する。

```text
derived only
persisted only
union
fallback
precedence
deduplication
conflict detection
```

以下を作る。

| Read Path | Derived Used | Persisted Used | Merge Rule | Dedup Key | Conflict Handling | Evidence |
| --------- | -----------: | -------------: | ---------- | --------- | ----------------- | -------- |

---

# 21. Duplicate Semantic Edge Analysis

同じsemantic relationが二つ以上のrepresentationで存在可能か確認する。

例:

```text
Execution → Result

typed FK exists
+
generic LineageEdge exists
```

各caseについて、

| Relation | Typed Relation | Persisted Edge Possible | Both Written? | Dedup? | Evidence |
| -------- | -------------- | ----------------------: | ------------: | -----: | -------- |

を作る。

存在可能性と実際のproduction writeを区別する。

---

# 22. Source-of-Truth Analysis

これは本Phaseの中心項目である。

ただしTarget Architecture判断ではなく、**現在のコードが何をsourceとして扱っているか**を観測する。

各semantic edgeについて、

```text
typed FK required?
persisted edge required?
either is accepted?
persisted edge only?
derived relation only?
```

を調査する。

Classification:

### `TYPED_RELATION_AUTHORITATIVE_IN_CODE`

read pathがtyped relationをsourceとして構築する。

### `PERSISTED_EDGE_AUTHORITATIVE_IN_CODE`

read pathがgeneric edgeをsourceとして使用する。

### `DUAL_SOURCE`

双方を独立にsourceとして使用する。

### `DERIVED_WITH_PERSISTED_SUPPLEMENT`

typed relationを基礎にpersisted relationを追加する。

### `PERSISTED_WITH_DERIVED_SUPPLEMENT`

persisted relationを基礎にderived relationを追加する。

### `UNKNOWN`

静的に決められない。

これは将来のcanonical architecture推奨ではない。

---

# 23. Reconstructability Analysis

persisted lineageを削除する提案は行わない。

しかし、事実として再構築可能性を調査する。

各persisted edge kindについて、

> 同じsemantic relationを他のpersistent typed dataから再構築できるか

を確認する。

Classification:

```text
FULLY_DERIVABLE
PARTIALLY_DERIVABLE
NO_DERIVATION_PATH_CONFIRMED
UNKNOWN
```

以下を作る。

| Persisted Edge Kind | Source Data | Derivable? | Information Lost if Removed? | Evidence |
| ------------------- | ----------- | ---------- | ---------------------------- | -------- |

`Information Lost if Removed?` は現状データモデル上の事実として判断する。

削除提案はしない。

---

# 24. Reverse Reconstructability

逆に、

> typed relationshipsから生成されるLineage edgeがgeneric persisted tableへ完全にmaterializeされているか

を確認する。

以下を作る。

| Derived Relation | Generic Edge Also Written? | Producer | Guaranteed? | Evidence |
| ---------------- | -------------------------: | -------- | ----------: | -------- |

---

# 25. Consistency / Invariant Investigation

dual representation間にconsistency ruleが存在するか確認する。

検索するもの:

```text
validation
assert
consistency
reconcile
repair
rebuild
backfill
sync
duplicate
deduplicate
upsert
unique
```

確認すること:

* write-through guarantee
* reconciliation job
* validation test
* database constraint
* startup repair
* migration backfill
* no explicit mechanism

以下を作る。

| Invariant | Enforcement | Scope | Failure Behavior | Evidence |
| --------- | ----------- | ----- | ---------------- | -------- |

存在しなければ `NONE_CONFIRMED`。

---

# 26. Conflict Semantics

例えば、

```text
typed FK says A → B
persisted edge says A → C
```

のような不整合が存在した場合に、

現在のread pathがどう振る舞うか静的に確認する。

* both returned
* one wins
* deduplicated
* validation error
* undefined
* UNKNOWN

実際のruntime conflictを作って試験してはならない。

---

# 27. Transaction Boundaries

Lineage writeとbusiness entity writeのtransaction couplingを確認する。

特に:

```text
Family Result write + lineage edge write

Artifact write + lineage edge write

retry cleanup + lineage deletion

revise new Execution + REVISED_FROM edge

GraphVersion creation + source Result relation
```

以下を作る。

| Operation | Business Writes | Lineage Writes | Same Transaction? | Physical Store Interaction | Evidence |
| --------- | --------------- | -------------- | ----------------- | -------------------------- | -------- |

---

# 28. Failure Semantics

Lineage writeが失敗した場合、

* business operationもrollbackするか
* Resultは残るか
* Artifactは残るか
* retryされるか
* compensationがあるか

を確認する。

不明なら `UNKNOWN`。

---

# 29. Retry Semantics

Causal / Exploratory / Predictiveについて、

```text
retry
```

が既存lineageを、

* retain
* delete
* overwrite
* recreate
* append

のどれとして扱うか確認する。

---

# 30. Rerun / Revise Semantics

特に、

```text
RERUN_OF
REVISED_FROM
source execution
source result
```

等のrelationがある場合、

* typed relationか
* generic edgeか
* 両方か

を追跡する。

---

# 31. Deletion / Cleanup Semantics

entity削除時にLineageがどうなるか確認する。

* FK cascade
* explicit delete
* orphan possible
* restrictive relation
* cleanup service
* soft delete

特にPhase 03で確認されたPredictive retry cleanupとgeneric lineage edge deletionを追跡する。

---

# 32. Lineage API Investigation

Repository-managed Lineage APIを静的に調査する。

確認すること:

* endpoint
* request parameters
* root node type
* root ID
* direction
* depth
* filters
* response node schema
* response edge schema
* derived/persisted source
* causal/family handling
* not-found behavior

APIの設計評価はしない。

---

# 33. UI Lineage Consumption

Repository-managed frontendがLineage APIを使用している場合、

* root entity
* request
* display node types
* edge kinds
* family-specific branching
* causal-specific branching

を確認する。

UIが共通Lineage representationを利用しているかを観測する。

---

# 34. Export / Closure Consumption

export / closure logicがLineageを利用する場合、

* derived / persistedのどちらを見るか
* Result / Artifact model差を吸収するか
* lineage edgeをexport manifestへ含むか

を調査する。

---

# 35. Causal vs Family Lineage Parity Matrix

以下を必ず作る。

| Semantic Relation    | Causal | Exploratory | Predictive | Same Mechanism? | Evidence |
| -------------------- | ------ | ----------- | ---------- | --------------- | -------- |
| Execution → Result   |        |             |            |                 |          |
| Execution → Artifact |        |             |            |                 |          |
| Stage → Result       |        |             |            |                 |          |
| Stage → Artifact     |        |             |            |                 |          |
| Result → Artifact    |        |             |            |                 |          |
| Input → Execution    |        |             |            |                 |          |
| Rerun source         |        |             |            |                 |          |
| Revision source      |        |             |            |                 |          |

N/Aとなるrelationは明示する。

---

# 36. Legacy Lineage Investigation

legacy architectureについて、少なくとも以下を調査する。

* `ArtifactLineage`
* input/output associations
* producing stage/attempt
* stored object relation
* Result → Artifact relation
* graph traversal/read service
* lineage API

legacy runtime reachabilityの判断はPhase 01を引き継ぐ。

目的はProduct lineageとの構造比較のみ。

---

# 37. Product vs Legacy Comparison

以下を作る。

| Dimension             | Product | Legacy | Classification | Evidence |
| --------------------- | ------- | ------ | -------------- | -------- |
| Node identity         |         |        |                |          |
| Edge persistence      |         |        |                |          |
| Typed relationships   |         |        |                |          |
| Generic lineage table |         |        |                |          |
| Artifact lineage      |         |        |                |          |
| Closure traversal     |         |        |                |          |
| Source of truth       |         |        |                |          |

削除可否は判断しない。

---

# 38. Migration / Schema Investigation

migrationをread-onlyで確認してよい。

確認すること:

* lineage table creation
* columns
* constraints
* indexes
* unique constraints
* FK presence/absence
* later schema changes
* backfill

migration executionは禁止。

migration commentから設計意図を断定しない。

---

# 39. Tests

testはread-only evidenceとして参照してよい。

特に、

* closure expected edges
* duplicate handling
* family lineage
* causal lineage
* retry cleanup
* revise/rerun
* depth traversal

を補助的に確認する。

優先順位:

```text
production implementation / schema
>
tests
>
comments / docs
```

---

# 40. Critical Distinctions

## 40.1 Common API output ≠ common source of truth

同じAPI schemaに変換されていても、元データが別なら区別する。

---

## 40.2 Persisted edge ≠ authoritative edge

tableに保存されているだけでsource of truthと断定しない。

---

## 40.3 Derived edge ≠ ephemeral or secondary

query時生成だから補助情報と断定しない。

---

## 40.4 Same edge kind ≠ same semantics

source/target typeやgeneration timingが違う場合は区別する。

---

## 40.5 Same semantic relation ≠ synchronized representations

typed FKとgeneric edgeの両方が存在しても同期保証を確認する。

---

## 40.6 Generic node ID ≠ typed identity

type discriminatorを含むidentity semanticsを確認する。

---

## 40.7 Closure representation ≠ persistence ownership

closure serviceが共通化されていてもwrite responsibilityは別問題。

---

# 41. Investigation Method

静的解析のみ使用する。

使用可能:

* `git`
* `git grep`
* `rg`
* `grep`
* `find`
* `sed`
* `cat`
* `awk`
* `tree`
* read-only AST analysis
* source / migration / test / documentation閲覧

必要なRepository-local検索はAgent自身で追加してよい。

---

# 42. Prohibited Operations

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
* source application execution
* architecture変更
* refactoring
* deletion
* documentation修正

唯一許可される書き込み:

```text
04_lineage_responsibility_inventory_result.md
```

および必要なparent directoryのみ。

---

# 43. Do Not Execute Runtime Code

禁止例:

```text
pytest
uvicorn ...
python -m ...
docker compose up
alembic ...
curl ...
```

runtime verificationが必要な論点はUnknownとして残す。

---

# 44. Investigation Procedure

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

---

## Step 2. Read Phase 01–03 Results

既存Lifecycle / Result / Artifact IDsとObservation continuityを確認する。

---

## Step 3. Discover All Lineage Representations

Repository全体から、

```text
lineage
Lineage
edge
closure
derived_from
source_result
source_artifact
revised_from
rerun
```

等を探索する。

名称だけに依存しない。

---

## Step 4. Build Node Inventory

Lineageに参加するpersistent entityを確定する。

---

## Step 5. Build Edge Kind Inventory

typed / generic / legacyを分離する。

---

## Step 6. Trace Derived Lineage

source relationshipからresponse edge生成まで追跡する。

---

## Step 7. Trace Persisted Lineage Writers

全production write pathを追跡する。

---

## Step 8. Trace Persisted Lineage Readers

generic lineage table read pathを追跡する。

---

## Step 9. Trace Closure Merge

derived / persisted representationのmerge semanticsを追跡する。

---

## Step 10. Resolve Causal Generic Persistence

Phase 03 Unknownを重点調査する。

---

## Step 11. Compare Causal / Exploratory / Predictive

lineage parity matrixを作成する。

---

## Step 12. Trace Mutation / Cleanup

retry / rerun / revise / deleteを追跡する。

---

## Step 13. Analyze Reconstructability

persisted edgeごとにtyped source dataから再導出可能か確認する。

---

## Step 14. Analyze Consistency Mechanisms

dual representation間のinvariant enforcementを検索する。

---

## Step 15. Compare Legacy

legacy lineageを同dimensionで比較する。

---

## Step 16. Record Unknowns

静的証拠不足を推測で埋めない。

---

# 45. Evidence Standard

主要主張には必ず、

```text
<repository-relative-path>:<line-range>
Symbol: <symbol>
Evidence: <what this proves>
```

を付ける。

lineage edgeについては、

```text
source fact
→ producer / derivation
→ persisted/emitted edge
→ consumer
```

を可能な限りedge単位で証明する。

---

# 46. Fact / Inference / Unknown

## `FACT`

production source / schemaから直接確認。

## `INFERENCE`

複数Factから合理的に導く。

supporting `E4-OBS-*` を必ず列挙。

## `UNKNOWN`

証拠不足。

必要な追加evidenceを明示。

---

# 47. Required Result Structure

`04_lineage_responsibility_inventory_result.md` は以下の構造とする。

```markdown
# 04 Lineage Responsibility Inventory Result

## 1. Metadata

- Prompt:
- Prior phases:
- Repository:
- Branch:
- HEAD:
- Working tree status:
- Started at:
- Finished at:
- Phase status:

## 2. Executive Summary

### 2.1 Lineage Representations

| Lineage ID | Name | Type | Persistence | Primary Producer | Primary Reader |
|---|---|---|---|---|---|

### 2.2 High-Level Responsibility

| Lifecycle | Typed/Derived | Generic Persisted | Read Boundary | Notes |
|---|---|---|---|---|

## 3. Lineage Node Inventory

| Node Type | Entity | Table | ID | Representation | Evidence |
|---|---|---|---|---|---|

## 4. Edge Kind Inventory

| Edge Kind | Source | Target | Representation | Producer | Evidence |
|---|---|---|---|---|---|

## 5. Derived Lineage

### 5.1 Derived Edge Matrix

| Relation | Source Fact | Derivation Symbol | Consumer | Evidence |
|---|---|---|---|---|

### 5.2 Derived Lineage Responsibility

## 6. Persisted Generic Lineage

### 6.1 Schema

### 6.2 Identity / Constraints

### 6.3 Producers

| Producer ID | Lifecycle | Operation | Edge | Transaction | Evidence |
|---|---|---|---|---|---|

### 6.4 Readers

| Reader | Query | Purpose | Evidence |
|---|---|---|---|

## 7. Causal Lineage

### 7.1 Typed Relationships

### 7.2 Generic Writes

### 7.3 Generic Reads

### 7.4 Mutation Semantics

### 7.5 Evidence

## 8. Exploratory Lineage

same structure.

## 9. Predictive Lineage

same structure.

## 10. Closure / Traversal

### 10.1 Algorithm

### 10.2 Derived Sources

### 10.3 Persisted Sources

### 10.4 Merge / Deduplication

| Property | Behavior | Evidence |
|---|---|---|

## 11. Duplicate Semantic Edge Analysis

| Relation | Typed | Persisted | Both Possible | Both Produced | Dedup Rule | Evidence |
|---|---|---|---|---|---|---|

## 12. Current Source-of-Truth Classification

| Semantic Relation | Classification | Actual Read Source | Actual Write Source | Evidence |
|---|---|---|---|---|

Use only:
- TYPED_RELATION_AUTHORITATIVE_IN_CODE
- PERSISTED_EDGE_AUTHORITATIVE_IN_CODE
- DUAL_SOURCE
- DERIVED_WITH_PERSISTED_SUPPLEMENT
- PERSISTED_WITH_DERIVED_SUPPLEMENT
- UNKNOWN

## 13. Reconstructability

| Persisted Edge | Other Persistent Facts | Classification | Information Unique? | Evidence |
|---|---|---|---|---|

## 14. Reverse Reconstructability

| Derived Relation | Persisted Equivalent | Guaranteed Write? | Evidence |
|---|---|---|---|

## 15. Consistency / Invariant Enforcement

| Invariant | Enforcement | Scope | Evidence |
|---|---|---|---|

## 16. Conflict Semantics

| Conflict | Current Behavior | Evidence |
|---|---|---|

## 17. Transaction Boundaries

| Operation | Domain Writes | Lineage Writes | Same Transaction | Evidence |
|---|---|---|---|---|

## 18. Failure Semantics

## 19. Retry / Rerun / Revise

### 19.1 Retry

### 19.2 Rerun

### 19.3 Revise

## 20. Deletion / Cleanup

| Trigger | Lineage Behavior | Mechanism | Evidence |
|---|---|---|---|

## 21. Causal / Family Parity

| Relation | Causal | Exploratory | Predictive | Same Mechanism | Evidence |
|---|---|---|---|---|---|

## 22. Lineage API

### Endpoints

### Input

### Read Sources

### Output

### Traversal

## 23. UI Consumption

## 24. Export / Closure Consumption

## 25. Legacy Lineage

### Representation

### Node Identity

### Edge Identity

### Producers

### Consumers

### Cleanup

## 26. Product / Legacy Comparison

| Dimension | Product | Legacy | Classification | Evidence |
|---|---|---|---|---|

## 27. Lineage Concept Inventory

### 27.1 Distinct lineage representations

### 27.2 Distinct physical lineage tables

### 27.3 Distinct edge-generation mechanisms

### 27.4 Distinct read/traversal mechanisms

### 27.5 Relations represented more than once

### 27.6 Relations represented only by persisted generic lineage

### 27.7 Relations represented only by typed relationships

## 28. Prior Unknown Carry-forward

| ID | Status | Phase 04 Evidence | Notes |
|---|---|---|---|

## 29. New Unresolved Items

| ID | Question | Confirmed Facts | Why Unresolved | Additional Evidence Needed |
|---|---|---|---|---|

## 30. Facts

Continue E4-OBS numbering from actual highest prior ID.

## 31. Inferences

Continue E4-INF numbering from actual highest prior ID.

## 32. Mandatory Explicit Answers

Answer A–L defined by this prompt.

## 33. Phase Conclusion

State only:

1. number of Lineage Representations confirmed
2. number of physical lineage-specific tables confirmed
3. whether active Product uses derived lineage
4. whether active Product uses persisted generic lineage
5. whether Causal writes persisted generic lineage during normal execution
6. whether Family writes persisted generic lineage
7. whether any semantic relation has dual representation
8. whether dual representation has an explicit consistency mechanism
9. whether persisted edges contain relations not reconstructable from typed Product relations
10. whether Product closure/API uses one or multiple lineage sources
11. whether Product and legacy lineage are structurally distinct
12. unresolved item count
13. whether evidence is sufficient to proceed to legacy reachability / target-architecture decision preparation

Do not recommend Target Architecture.

## 34. Completion Status

One of:

- COMPLETED
- COMPLETED_WITH_UNKNOWNS
- BLOCKED_WRONG_BRANCH
- BLOCKED
```

---

# 48. Mandatory Explicit Answers

## A

```text
Does the active Product architecture use typed/derived lineage?
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
Does the active Product architecture use persisted generic lineage edges?
```

同様。

---

## C

```text
Does normal Causal Execution processing write persisted generic lineage edges?
```

回答:

```text
YES
NO_PATH_CONFIRMED
PARTIALLY
UNKNOWN
```

＋evidence。

---

## D

```text
Do Exploratory and Predictive executions write persisted generic lineage edges?
```

Lifecycleごとに回答。

---

## E

```text
Can the same semantic lineage relation exist simultaneously as a typed relation and a persisted generic edge?
```

回答:

```text
YES
NO
PARTIALLY
UNKNOWN
```

＋具体的relation。

---

## F

```text
If both representations exist, is there an explicit synchronization or consistency mechanism?
```

回答:

```text
YES
NO_MECHANISM_CONFIRMED
PARTIALLY
UNKNOWN
```

＋evidence。

---

## G

```text
Does the Product lineage read path combine derived and persisted edges?
```

回答:

```text
YES
NO
PARTIALLY
UNKNOWN
```

＋merge semantics。

---

## H

```text
Are persisted Product lineage edges fully reconstructable from other typed persistent relationships?
```

回答:

```text
YES
NO
PARTIALLY
UNKNOWN
```

＋edge-kind別の根拠。

---

## I

```text
Are all typed/derived Product lineage relations also materialized into persisted generic lineage edges?
```

同様。

---

## J

```text
Do Causal, Exploratory, and Predictive use the same lineage-production mechanism?
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

## K

```text
Does retry/rerun/revise maintain lineage through one common mechanism across active Product lifecycles?
```

同様。

---

## L

```text
Is legacy lineage structurally identical to active Product lineage?
```

回答:

```text
YES
NO
PARTIALLY
UNKNOWN
```

＋evidence。

`NO` はlegacy削除可能性を意味しない。

---

# 49. Prohibited Conclusions

以下を書いてはならない。

```text
Derived lineage should be canonical.

Persisted lineage should be canonical.

LineageEdgeOrm should be removed.

product_lineage_edge should be deleted.

All lineage should be derived from FKs.

All lineage should be persisted.

Causal should write family-style lineage.

Family should stop writing lineage.

The closure service should be simplified.

Legacy ArtifactLineage should be migrated.

This table is redundant and should be deleted.

ENH-E4 should implement ...
```

以下は許可する。

```text
DUAL_SOURCE
NO_MECHANISM_CONFIRMED
FULLY_DERIVABLE
PARTIALLY_DERIVABLE
STRUCTURALLY_DISTINCT
```

ただしevidenceを伴うこと。

---

# 50. Completeness Criteria

### C1

Phase 01〜03 resultを読んでいる。

### C2

全Lineage representationをInventory化している。

### C3

node typeをInventory化している。

### C4

edge kindをInventory化している。

### C5

typed/derived lineage sourceを追跡している。

### C6

generic persisted lineage schemaを確認している。

### C7

全主要production writerを探索している。

### C8

全主要production readerを探索している。

### C9

Causal generic lineage write pathを重点確認している。

### C10

Exploratory / Predictive lineage write pathを確認している。

### C11

closure merge/dedup semanticsを確認している。

### C12

duplicate semantic relationを調査している。

### C13

current source-of-truth behaviorをrelation単位で分類している。

### C14

persisted edge reconstructabilityを調査している。

### C15

reverse reconstructabilityを調査している。

### C16

consistency mechanismを探索している。

### C17

transaction boundaryを確認している。

### C18

retry / rerun / revise / deletion semanticsを確認している。

### C19

Lineage APIを調査している。

### C20

UI / export consumptionを必要範囲で調査している。

### C21

legacy lineageを比較している。

### C22

Fact / Inference / Unknownを分離している。

### C23

prior-phase IDsを実ファイルから継続している。

### C24

Target Architectureを提案していない。

### C25

runtime executionをしていない。

### C26

指定result以外を変更していない。

---

# 51. Final Self-Check

result生成後、以下のみ実行する。

```text
git status --short

git diff --stat

git diff -- \
docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/architecture_review/04_lineage_responsibility_inventory_result.md
```

期待される新規変更:

```text
04_lineage_responsibility_inventory_result.md
```

既存working tree変更を変更・stash・restore・resetしてはならない。

---

# 52. Agent Response

作業完了時のchat responseは簡潔に以下を報告する。

```text
04_lineage_responsibility_inventory_result.md を生成しました。

Phase status: <...>
Lineage representations: <count>
Physical lineage tables: <count>
Persisted edge producers: <count>
Dual-represented semantic relations: <count>
Unresolved items: <count>

Source/configuration/test/migration codeは変更していません。
```

詳細はresult文書を正本とする。

---

# 53. Stop Condition

以下のいずれかで停止する。

1. `04_lineage_responsibility_inventory_result.md` を生成し、Final Self-Checkを完了した
2. branch不一致
3. static investigationを継続できないblocking issue
4. result以外のRepository変更なしには調査不能

停止後、以下へ進んではならない。

* runtime verification
* legacy deletion
* target lineage architecture決定
* Execution統合案作成
* schema migration設計
* Phase 05
* implementation
* refactoring
* deletion
* Gate decomposition

次作業は人間によるresult review後、別promptとして指示される。
