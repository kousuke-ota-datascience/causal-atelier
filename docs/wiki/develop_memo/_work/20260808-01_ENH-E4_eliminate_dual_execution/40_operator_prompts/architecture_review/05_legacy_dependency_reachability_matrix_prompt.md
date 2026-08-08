# 05 Legacy Dependency / Reachability Matrix — Architecture Review Prompt

## 1. Task

`ENH-E4 eliminate dual execution` の Architecture Review Phase 05 として、現在のRepositoryに存在する `ariadne.legacy` およびlegacy関連componentについて、**dependency / reachability / responsibility matrix** を静的コード調査によって作成する。

本Phaseの中心目的は、

> legacyと名付けられたコードのうち、現在のactive Product runtime、shared scientific capability、test、tooling、migration、packaging等から実際に依存されているものは何か。また、Repository-localな到達経路が確認されないものは何か。

をコード上のevidenceによって確定することである。

本Phaseでは、

```text
legacy directory
=
削除対象
```

とは仮定しない。

また、

```text
runtime reachableでない
=
安全に削除可能
```

とも仮定しない。

以下を分離して調査する。

```text
runtime reachability

import dependency

scientific capability dependency

persistence/schema dependency

test dependency

tooling dependency

packaging dependency

migration/history dependency

documentation/example dependency
```

このPhaseは **read-only architecture investigation** である。

Production code、test code、configuration、migration、dependency、database、runtime stateを変更してはならない。

唯一許可されるRepositoryへの書き込みは、指定されたresult文書の生成・更新だけである。

---

# 2. Positioning

Phase 01では、

```text
standard runtime
→ legacy Execution path
```

についてRepository-localなactive pathが確認されなかった。

Phase 02では、

```text
active Product内部に複数Execution lifecycle
```

が存在することを確認した。

Phase 03では、

```text
Causal Result / Artifact
vs
Family Result / Artifact
```

の構造分離を確認した。

Phase 04では、

```text
Product typed/derived lineage
Product persisted generic lineage
Legacy ArtifactLineage
```

が異なるrepresentation / responsibilityとして存在することを確認した。

Phase 05では、

```text
legacy code/component
       ↑
       │ inbound dependency
       │
Product / shared / interface / test /
tooling / packaging / migration / docs
```

および、

```text
legacy component
       ↓ outbound dependency
Product / shared scientific core /
third-party / persistence
```

を調査する。

目的は、後続のTarget Architecture Decisionに必要な

> keep / migrate / replace / delete

判断の**事実材料**を揃えることである。

本Phase自身は、その判断をしない。

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

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
architecture_review/
04_lineage_responsibility_inventory_result.md
```

本Phase result出力先:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
architecture_review/
05_legacy_dependency_reachability_matrix_result.md
```

調査開始時点のcommit SHAを必ず記録すること。

---

# 4. Required Use of Prior Evidence

Phase 01〜04 resultを調査開始時に読むこと。

特に以下を引き継ぐ。

* active runtime roots
* Execution lifecycle units
* Result / Artifact models
* Lineage representations
* legacy runtime reachability classification
* prior Facts / Inferences / Unknowns
* legacy-related unresolved items

ただしprior resultを理由にsource調査を省略してはならない。

Phase 05では、**dependency directionとresponsibility単位**でlegacyを再調査する。

---

# 5. ID Continuity

以下について、Phase 01〜04 result内の最大番号を実際に確認する。

```text
E4-OBS-*
E4-INF-*
E4-UNK-*
```

Phase 05では最大番号の次から継続する。

既存IDを変更・再採番してはならない。

新規Legacy Component ID:

```text
E4-LG-001
E4-LG-002
...
```

新規Dependency Edge ID:

```text
E4-DEP-001
E4-DEP-002
...
```

---

# 6. Core Investigation Questions

最終的に以下へ回答できる状態にすること。

## Q1

`src/ariadne/legacy/**` には、責務として何が存在するか。

---

## Q2

そのうち現在のProduct/shared production codeからimport / call / instantiateされるcomponentは何か。

---

## Q3

Productから直接参照されていなくても、shared scientific capabilityとしてuniqueな実装を保持しているlegacy componentはあるか。

---

## Q4

legacy配下のscientific algorithm / adapter / runner / transformationが、Product側に

* duplicate
* replacement
* wrapper
* adapter
* no equivalent confirmed

のどれとして存在するか。

---

## Q5

legacy persistence/schemaを現在のProduct runtimeが参照しているか。

---

## Q6

legacy migrationをProduct clean rebuildが必要としているか。

---

## Q7

legacy API / CLI / worker / background processにRepository-localな起動経路は存在するか。

---

## Q8

legacy componentをtestだけが使用しているケースは何か。

---

## Q9

developer tooling / maintenance script / exampleだけがlegacyを使用するケースは何か。

---

## Q10

packaging / console scripts / Docker / Compose / CI / shell scriptがlegacy moduleを参照しているか。

---

## Q11

legacyからProduct/shared codeへの逆依存は何か。

---

## Q12

`ariadne.legacy` 外に、legacy-specific contract / model / naming / compatibility shimが残っているか。

---

# 7. Legacy Component Unit

本Phaseでは、個々のfileではなく**責務単位**を `Legacy Component` としてInventory化する。

例:

```text
legacy API
legacy CLI
legacy execution orchestration
legacy worker
legacy pipeline
legacy discovery
legacy persistence/domain metadata
legacy artifact lineage
legacy scientific runner
legacy materialization
legacy projection
legacy state management
```

実際のRepository構造に従ってcomponentを決定すること。

directoryだけで粗くまとめすぎず、

> dependency / responsibility / replacementを判断できる粒度

にする。

---

# 8. Legacy Component Inventory

以下を作る。

| Component ID | Component | Responsibility | Main Modules | Persistent State | Runtime Surface | Evidence |
| ------------ | --------- | -------------- | ------------ | ---------------- | --------------- | -------- |

Responsibilityはproduction sourceから確認する。

directory名だけで推測しない。

---

# 9. Reachability Classification

各Legacy Componentを以下のいずれかに分類する。

## `ACTIVE_PRODUCT_REACHABLE`

現在のstandard Product runtime rootから到達可能。

---

## `CONDITIONALLY_REACHABLE`

config / registry / parameter等の条件で到達可能。

条件を明記する。

---

## `STANDALONE_RUNTIME_REACHABLE`

Product runtimeとは別だが、Repository-localなCLI / worker / API / executable rootが存在する。

---

## `TEST_ONLY_REACHABLE`

test / fixture / test helperからのみ到達を確認。

---

## `TOOLING_ONLY_REACHABLE`

developer / maintenance toolingからのみ到達。

---

## `MIGRATION_HISTORY_ONLY`

migration/history上は存在するがapplication/runtime dependencyを確認できない。

---

## `DOCUMENTATION_ONLY`

docs/exampleからのみ参照。

---

## `UNREFERENCED_CANDIDATE`

definitionは存在するがRepository-localなincoming referenceを確認できない。

---

## `UNKNOWN`

静的に確定不能。

---

# 10. Dependency Type Classification

Legacyへの各incoming dependencyは以下で分類する。

```text
RUNTIME_IMPORT
RUNTIME_CALL
RUNTIME_REGISTRATION
SCIENTIFIC_CAPABILITY
PERSISTENCE_SCHEMA
MIGRATION
TEST
TOOLING
PACKAGING
DEPLOYMENT
DOCUMENTATION
TYPE_HINT_ONLY
COMPATIBILITY_SHIM
UNKNOWN
```

単なるtext mentionと実際のdependencyを分離する。

---

# 11. Repository-wide Incoming Reference Search

`src/ariadne/legacy` 外のRepository全体からlegacyへの参照を検索する。

最低限:

```text
ariadne.legacy
from .legacy
from ..legacy
import legacy
legacy.
```

に加えて、

legacy symbol名によるindirect import / re-exportも確認する。

対象:

```text
src/
tests/
frontend/
deploy/
scripts/
tools/
docs/
pyproject.toml
Dockerfile*
docker-compose*
compose*
Makefile*
*.sh
CI configuration
migration configuration
```

vendor/cache/generated contentはRepository構造に応じて除外してよいが、除外範囲を記録する。

---

# 12. Re-export / Alias Investigation

以下を重点調査する。

```text
shared module
→ imports legacy symbol
→ re-exports
→ Product imports shared module
```

直接 `ariadne.legacy` の文字列がないProduct dependencyを見逃してはならない。

確認するもの:

* `__init__.py`
* compatibility modules
* aliases
* protocols
* adapters
* factory registrations
* runner registrations
* plugin registries

---

# 13. Product → Legacy Dependency Matrix

必ず以下を作る。

| Dependency ID | Product/Shared Source | Legacy Target | Dependency Type | Runtime Reachability | Evidence |
| ------------- | --------------------- | ------------- | --------------- | -------------------- | -------- |

Productからのdependencyが0件の場合でも、

```text
NONE_CONFIRMED
```

として検索範囲とevidenceを記載する。

---

# 14. Legacy → Product / Shared Dependency Matrix

逆方向も調査する。

| Dependency ID | Legacy Source | Product/Shared Target | Dependency Type | Purpose | Evidence |
| ------------- | ------------- | --------------------- | --------------- | ------- | -------- |

これにより、

> legacy packageが独立したold stackなのか、現在のProduct/shared codeに寄生したcompatibility stackなのか

を後続判断できるようにする。

本Phaseでは評価しない。

---

# 15. Shared Scientific Capability Investigation

最重要項目の一つ。

legacy配下にscientific computation / algorithm / statistical logic / graph operation / causal estimation等が存在する場合、Product側との関係を調査する。

各scientific capabilityについて、

| Capability | Legacy Implementation | Product/Shared Implementation | Relationship | Evidence |
| ---------- | --------------------- | ----------------------------- | ------------ | -------- |

Relationship:

### `SAME_IMPLEMENTATION_SHARED`

実際に同じimplementationを双方が呼ぶ。

### `PRODUCT_WRAP_LEGACY`

Productがlegacy implementationをadapter/wrapper経由で利用。

### `LEGACY_WRAP_SHARED`

legacyがshared/Product implementationを利用。

### `PARALLEL_IMPLEMENTATIONS`

双方に別implementationが存在。

### `LEGACY_ONLY_CONFIRMED`

legacy側のみimplementationを確認。

### `PRODUCT_ONLY_CONFIRMED`

Product側のみ確認。

### `UNKNOWN`

判定不能。

---

# 16. Scientific Semantic Comparison

`PARALLEL_IMPLEMENTATIONS` の場合、単に名前を比較するだけでは不十分。

可能な範囲で、

```text
input contract
output contract
algorithm/library
configuration
statistical semantics
determinism/seed handling
error model
```

を比較する。

ただしscientific correctnessの再検証やruntime numerical testは行わない。

目的は、

> 同じcapabilityの重複実装候補か

を判断できる構造的evidenceを残すこと。

---

# 17. Scientific Dependency Criticality

legacy scientific capabilityがRepository内のどこから使われるか確認する。

Classification:

```text
ACTIVE_PRODUCT_REQUIRED
STANDALONE_LEGACY_ONLY
TEST_REQUIRED
TOOLING_REQUIRED
NO_CONSUMER_CONFIRMED
UNKNOWN
```

これは削除可否の判定ではない。

---

# 18. Legacy Domain / Persistence Inventory

legacy persistent modelについて、

* entity/model
* repository/session
* physical table
* migration family
* active Product reference
* legacy-only reference

を確認する。

以下を作る。

| Legacy Model | Table | Product Reference | Legacy Reference | Migration | Reachability | Evidence |
| ------------ | ----- | ----------------- | ---------------- | --------- | ------------ | -------- |

---

# 19. Product Schema Dependency on Legacy

以下を明示的に調査する。

* Product ORMからlegacy tableへのFK
* Product migrationからlegacy tableへのFK
* legacy ORMからProduct tableへのFK
* raw SQL cross-schema reference
* shared sequence/type
* database view
* trigger
* migration dependency
* foreign-key target strings

回答:

```text
Does active Product persistence depend on legacy physical tables?
```

```text
YES
NO_PATH_CONFIRMED
PARTIALLY
UNKNOWN
```

＋evidence。

---

# 20. Migration Dependency

migration系統を分離して確認する。

最低限:

```text
alembic_product.ini
product_migrations/
legacy migration config
legacy migrations/
```

確認すること:

* Product migration head
* Product migration down_revision chain
* legacy revision ID参照
* cross-directory import
* legacy metadata import
* shared Base/metadata
* bootstrap script
* clean rebuild procedure

Phase 00 / prior database reset evidenceがある場合は参照してよいが、sourceからも確認する。

migrationは実行しない。

---

# 21. Mandatory Migration Answer

```text
Does a clean Product schema definition or migration chain require legacy migrations or legacy ORM metadata?
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

# 22. Legacy Runtime Roots

Phase 01の調査をdependency観点から再確認する。

探索:

* legacy FastAPI app
* router composition
* CLI
* worker main
* module `__main__`
* console script
* shell invocation
* Docker command
* Compose service
* CI job
* Make target

以下を作る。

| Legacy Runtime Root | Definition | Repository-local Invocation | Classification | Evidence |
| ------------------- | ---------- | --------------------------- | -------------- | -------- |

---

# 23. Standalone Runtime Distinction

Repository-localなentry functionが存在することと、

standard deployed runtimeから起動されることを区別する。

例:

```text
worker main exists
≠
deployment invokes worker main
```

---

# 24. Test Dependency

test suite全体からlegacy dependencyをInventory化する。

分類:

```text
LEGACY_BEHAVIOR_TEST
COMPATIBILITY_TEST
SHARED_SCIENTIFIC_TEST
PRODUCT_TEST_USING_LEGACY_FIXTURE
MIGRATION_TEST
OTHER
```

以下を作る。

| Test Area | Legacy Component | Classification | Production Implication | Evidence |
| --------- | ---------------- | -------------- | ---------------------- | -------- |

`Production Implication` は、

```text
NONE_CONFIRMED
SHARED_CONTRACT
COMPATIBILITY_CONTRACT
UNKNOWN
```

等の事実分類に留める。

「testがあるから残すべき」とは書かない。

---

# 25. Fixture / Factory Contamination

Product testsがlegacy fixture / factory / model helperを利用していないか調査する。

これはproduction import dependencyとは別に記録する。

---

# 26. Tooling Dependency

以下を探索する。

* admin script
* migration helper
* seed script
* data converter
* import/export utility
* maintenance command
* benchmark
* local development script
* notebooks if tracked

以下を作る。

| Tool | Legacy Dependency | Purpose | Replacement/Alternative Found | Evidence |
| ---- | ----------------- | ------- | ----------------------------- | -------- |

Replacementがあることは削除判断を意味しない。

---

# 27. Packaging Dependency

確認する。

* `pyproject.toml`
* entry points
* package include/exclude
* console scripts
* optional dependency groups
* module names exposed to users
* installed package surface

以下を回答する。

```text
Is any legacy module directly exposed as an installed CLI or declared public package entry point?
```

```text
YES
NO_PATH_CONFIRMED
UNKNOWN
```

---

# 28. Deployment Dependency

確認する。

* Dockerfile
* Compose
* Kubernetes/manifests if present
* systemd/process definitions if present
* environment variables
* startup commands
* health checks
* worker commands

以下を回答する。

```text
Does repository-managed deployment configuration invoke legacy runtime code?
```

回答:

```text
YES
NO_PATH_CONFIRMED
PARTIALLY
UNKNOWN
```

---

# 29. Configuration Dependency

legacy-specific environment variable / config section / feature flagが存在するか確認する。

以下を作る。

| Config | Consumer | Active Product Consumer? | Legacy Consumer? | Evidence |
| ------ | -------- | -----------------------: | ---------------: | -------- |

unused-looking configurationも削除対象とは断定しない。

---

# 30. Interface / Contract Dependency

`ariadne.legacy` 外に、legacy contractを前提とするものがないか確認する。

例:

* DTO
* enum
* API schema
* error code
* route path
* CLI output
* environment variable
* serialized manifest
* table name
* event payload

以下を作る。

| Contract | Defined In | Legacy Consumer | Product/External Consumer | Evidence |
| -------- | ---------- | --------------- | ------------------------- | -------- |

---

# 31. Compatibility Shim Investigation

legacy→ProductまたはProduct→legacy bridgeを探す。

検索対象:

```text
compat
compatibility
legacy
adapter
bridge
shim
deprecated
alias
wrapper
migration
```

各shimについて、

* source
* target
* direction
* current caller
* purpose

を記録する。

---

# 32. Legacy Data Format Dependency

legacy-specific serialized formatが現在のProduct/toolingから読まれるか確認する。

例:

* JSON manifest
* artifact metadata
* persisted model
* file layout
* export format
* import bundle

存在しない場合 `NONE_CONFIRMED`。

---

# 33. Cross-generation Data Compatibility

以下を調査する。

```text
Can Product code read legacy-generated persistent/file artifacts?

Can legacy code read Product-generated persistent/file artifacts?
```

回答:

```text
YES
NO_PATH_CONFIRMED
PARTIALLY
UNKNOWN
```

static code evidenceのみで判断する。

runtime testは禁止。

---

# 34. External Invocation Boundary

Repository外からlegacy moduleを直接起動している可能性は静的Repository調査だけでは否定できない。

したがって、

```text
Repository-local reference absent
```

と

```text
No external consumer exists
```

を混同しない。

外部consumerについて証拠がなければ、

```text
UNKNOWN_EXTERNAL_CONSUMERS
```

として明示する。

---

# 35. Responsibility Overlap Matrix

legacy componentと現在のProduct componentの責務を比較する。

以下を作る。

| Responsibility | Legacy Component | Product/Shared Component | Structural Relationship | Evidence |
| -------------- | ---------------- | ------------------------ | ----------------------- | -------- |

Structural Relationship:

```text
SHARED_IMPLEMENTATION
PARALLEL_IMPLEMENTATION
LEGACY_WRAPS_PRODUCT
PRODUCT_WRAPS_LEGACY
LEGACY_ONLY
PRODUCT_ONLY
PARTIAL_OVERLAP
UNKNOWN
```

対象最低限:

```text
API
CLI
Execution lifecycle
Worker
Workflow/stage execution
Scientific execution
Result
Artifact
Lineage
Persistence
Discovery
Pipeline
Materialization
Projection
State management
```

---

# 36. Reachability × Responsibility Matrix

各Legacy Componentについて最終的に以下を作る。

| Component | Runtime | Product Import | Scientific Consumer | Test | Tooling | Migration | Packaging | External Unknown |
| --------- | ------- | -------------- | ------------------- | ---- | ------- | --------- | --------- | ---------------- |

値:

```text
YES
NO_PATH_CONFIRMED
PARTIAL
N/A
UNKNOWN
```

---

# 37. Dependency Criticality Classification

各Legacy Componentを、**削除判断ではなくdependency状態**として分類する。

## `ACTIVE_DEPENDENCY`

active Product/runtimeから必要とされるdependencyを確認。

## `SHARED_CAPABILITY_DEPENDENCY`

active codeがlegacy-owned capabilityを利用。

## `COMPATIBILITY_DEPENDENCY`

compatibility bridge/contractから参照。

## `TEST_OR_TOOLING_DEPENDENCY_ONLY`

production dependencyなし、test/tooling依存あり。

## `MIGRATION_HISTORY_DEPENDENCY_ONLY`

migration/historyのみ。

## `REPOSITORY_UNREFERENCED`

Repository-local consumerなし。

## `MIXED`

複数category。

## `UNKNOWN`

静的に分類不能。

---

# 38. No Delete-Candidate Classification

本Phaseでは、

```text
DELETE
SAFE_TO_DELETE
REMOVE
KEEP
MIGRATE
REPLACE
```

という最終分類を使用してはならない。

これは後続Architecture Decisionの責務である。

---

# 39. Reverse Blast Radius Inventory

仮にLegacy Componentが存在しなくなった場合に、

**静的dependencyとして壊れることが確実なRepository-local source** を列挙する。

これは削除シミュレーションではなく、reference graphの逆引きである。

以下を作る。

| Legacy Component | Direct Inbound References | Transitive Repository Areas | Evidence |
| ---------------- | ------------------------- | --------------------------- | -------- |

「壊れるかもしれない」ではなくdirect referenceを基礎に記載する。

---

# 40. Orphan Surface Inventory

Repository-local inbound referenceが確認されないlegacy surfaceを列挙する。

以下を作る。

| Legacy Component | Definition Exists | Inbound Search | Runtime Root | Classification | Limitation |
| ---------------- | ----------------: | -------------- | ------------ | -------------- | ---------- |

必ず `UNREFERENCED_CANDIDATE` / `REPOSITORY_UNREFERENCED` と呼ぶ。

`dead code` と呼んではならない。

---

# 41. Legacy Lineage Follow-up

Phase 04のlegacy unresolved itemについて、dependency調査で追加確認できるものは確認する。

特に、

* ArtifactLineage cleanup caller
* maintenance job
* retention job
* external tool reference

を検索する。

ただしPhase 05の主目的を超える詳細lineage設計へ戻らない。

---

# 42. Prior Unknown Carry-forward

Phase 01〜04のlegacy/dependency関連Unknownを列挙し、

```text
RESOLVED_IN_PHASE_05
REMAINS_OPEN
OUT_OF_SCOPE
```

のいずれかに分類する。

特にRepository外consumerを必要とするUnknownを無理に解決しない。

---

# 43. Investigation Method

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
* read-only Python AST解析
* import graphの静的解析
* source / config / migration / test / docs閲覧

---

# 44. Optional Static Import Graph

必要であればPython ASTを用いて、

```text
module
→ imported module
```

の静的graphを構築してよい。

ただしapplication modulesを実際にimportしてはならない。

AST / text parsingのみとする。

generated graph fileをRepositoryへ保存してはならない。

result文書へ必要なsummaryだけ記載する。

---

# 45. Prohibited Operations

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
* benchmark実行
* HTTP request
* external API
* network調査
* application module import/execution
* refactoring
* deletion
* documentation修正

唯一許可される書き込み:

```text
05_legacy_dependency_reachability_matrix_result.md
```

および必要なparent directoryのみ。

---

# 46. Do Not Execute Runtime Code

禁止例:

```text
pytest
python -m ariadne...
uvicorn ...
docker compose up
alembic ...
curl ...
```

runtime/deployment verificationが必要な事項はUnknownとして残す。

---

# 47. Investigation Procedure

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

## Step 2. Read Phase 01–04 Results

既存facts / IDs / legacy findingsを確認する。

---

## Step 3. Inventory Legacy Components

責務単位でcomponentを確定する。

---

## Step 4. Search Incoming References

Repository全体からlegacyへのdependencyを探す。

---

## Step 5. Resolve Re-exports / Indirect Dependencies

direct string searchで終わらない。

---

## Step 6. Search Reverse Dependencies

legacyからProduct/sharedへのdependencyを調べる。

---

## Step 7. Investigate Scientific Capabilities

legacyとProduct/shared implementationを比較する。

---

## Step 8. Investigate Persistence / Migration

cross-schema / migration dependencyを確認する。

---

## Step 9. Investigate Runtime Roots / Deployment

Repository-local invocationを確認する。

---

## Step 10. Investigate Test / Tooling / Packaging

production dependencyと分離する。

---

## Step 11. Investigate Compatibility Contracts

shim / DTO / serialized format等を確認する。

---

## Step 12. Build Responsibility Overlap Matrix

legacy vs Product/sharedを比較する。

---

## Step 13. Build Reachability Matrix

component単位でdependency状態を整理する。

---

## Step 14. Build Reverse Blast Radius

direct/static dependencyを逆引きする。

---

## Step 15. Carry Forward Unknowns

静的に解決不能なものを残す。

---

# 48. Evidence Standard

主要主張には必ず、

```text
<repository-relative-path>:<line-range>
Symbol: <symbol>
Evidence: <what this proves>
```

を付ける。

dependency edgeについては、

```text
Source
→ import / registration / call
→ Legacy Target
```

を可能な限りedge単位で示す。

---

# 49. Negative Finding Standard

「参照がない」というnegative findingは、単一grepだけで断定してはならない。

最低限、

```text
qualified module search
+
symbol/reference search
+
runtime/config/package search
```

を組み合わせる。

negative findingには、

```text
Search performed:
- ...
- ...
- ...

Result:
NO_PATH_CONFIRMED
```

を記載する。

---

# 50. Fact / Inference / Unknown

## `FACT`

source/config/schema/testから直接確認。

## `INFERENCE`

複数Factから合理的に導く。

supporting `E4-OBS-*` を記載。

## `UNKNOWN`

Repository-local static evidenceでは判定不能。

追加で必要なevidenceを記載。

---

# 51. Required Result Structure

`05_legacy_dependency_reachability_matrix_result.md` は以下の構造とする。

```markdown
# 05 Legacy Dependency / Reachability Matrix Result

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

### 2.1 Legacy Components

| ID | Component | Responsibility | Dependency Criticality | Runtime Reachability |
|---|---|---|---|---|

### 2.2 Overall Dependency Summary

| Dependency Category | Count | Major Components |
|---|---:|---|

## 3. Legacy Component Inventory

| Component | Modules | Responsibility | Persistence | Runtime Surface | Evidence |
|---|---|---|---|---|---|

## 4. Product / Shared → Legacy Dependencies

| DEP ID | Source | Target | Type | Runtime Reachability | Evidence |
|---|---|---|---|---|---|

## 5. Legacy → Product / Shared Dependencies

| DEP ID | Source | Target | Type | Purpose | Evidence |
|---|---|---|---|---|---|

## 6. Indirect / Re-export Dependencies

| Source | Bridge | Legacy Target | Consumer | Evidence |
|---|---|---|---|---|

## 7. Scientific Capability Matrix

| Capability | Legacy | Product/Shared | Relationship | Criticality | Evidence |
|---|---|---|---|---|---|

## 8. Scientific Contract Comparison

For PARALLEL_IMPLEMENTATIONS:

| Capability | Input | Output | Algorithm/Library | Configuration | Semantic Differences | Evidence |
|---|---|---|---|---|---|---|

## 9. Persistence Dependency

### 9.1 Legacy Models

| Model | Table | Product Ref | Legacy Ref | Migration | Evidence |
|---|---|---|---|---|---|

### 9.2 Cross-Schema Dependencies

| Source | Target | Mechanism | Evidence |
|---|---|---|---|

## 10. Migration Dependency

### Product Migration Chain

### Legacy Migration Chain

### Cross-chain Dependencies

### Clean Product Schema Dependency

## 11. Legacy Runtime Roots

| Root | Definition | Repository Invocation | Reachability | Evidence |
|---|---|---|---|---|

## 12. Test Dependencies

| Test Area | Legacy Component | Type | Production Implication | Evidence |
|---|---|---|---|---|

## 13. Tooling Dependencies

| Tool | Legacy Component | Purpose | Alternative Found | Evidence |
|---|---|---|---|---|

## 14. Packaging Dependencies

### Console Scripts

### Public Entry Points

### Package Exposure

## 15. Deployment Dependencies

| Deployment Surface | Legacy Reference | Active Path | Evidence |
|---|---|---|---|

## 16. Configuration Dependencies

| Config | Product Consumer | Legacy Consumer | Evidence |
|---|---|---|---|

## 17. Interface / Compatibility Contracts

| Contract | Location | Legacy Consumer | Product/Other Consumer | Evidence |
|---|---|---|---|---|

## 18. Compatibility Shims

| Shim | Direction | Caller | Purpose | Evidence |
|---|---|---|---|---|

## 19. Data Format Compatibility

| Format | Legacy Writer/Reader | Product Writer/Reader | Compatibility | Evidence |
|---|---|---|---|---|

## 20. Responsibility Overlap

| Responsibility | Legacy | Product/Shared | Relationship | Evidence |
|---|---|---|---|---|

## 21. Reachability × Responsibility Matrix

| Legacy Component | Runtime | Product Import | Scientific | Test | Tooling | Migration | Packaging | External |
|---|---|---|---|---|---|---|---|---|

## 22. Dependency Criticality

| Legacy Component | Classification | Supporting DEP IDs | Evidence |
|---|---|---|---|

Allowed:
- ACTIVE_DEPENDENCY
- SHARED_CAPABILITY_DEPENDENCY
- COMPATIBILITY_DEPENDENCY
- TEST_OR_TOOLING_DEPENDENCY_ONLY
- MIGRATION_HISTORY_DEPENDENCY_ONLY
- REPOSITORY_UNREFERENCED
- MIXED
- UNKNOWN

## 23. Reverse Blast Radius

| Legacy Component | Direct Inbound References | Transitive Areas | Evidence |
|---|---|---|---|

## 24. Repository-Unreferenced Components

| Component | Search Performed | Runtime Root | Classification | Limitation |
|---|---|---|---|---|

## 25. External Consumer Boundary

State explicitly what Repository-local static analysis can and cannot prove.

## 26. Prior Unknown Carry-forward

| ID | Status | Phase 05 Evidence | Notes |
|---|---|---|---|

## 27. New Unresolved Items

| ID | Question | Confirmed Facts | Why Unresolved | Additional Evidence Needed |
|---|---|---|---|---|

## 28. Facts

Continue E4-OBS from actual maximum prior ID.

## 29. Inferences

Continue E4-INF from actual maximum prior ID.

## 30. Mandatory Explicit Answers

Answer A–L defined below.

## 31. Phase Conclusion

State only:

1. number of Legacy Components
2. number with ACTIVE_PRODUCT_REACHABLE status
3. number with STANDALONE_RUNTIME_REACHABLE status
4. number with Product/shared import dependency
5. number containing scientific capabilities
6. number of scientific capabilities used by active Product code
7. whether Product persistence depends on legacy physical tables
8. whether Product migration chain depends on legacy migration chain
9. whether repository-managed deployment invokes legacy
10. whether installed package entry points expose legacy
11. number of Repository-unreferenced legacy components
12. unresolved item count
13. whether evidence is sufficient for Target Architecture Decision preparation

Do not classify components as keep/delete/migrate/replace.

## 32. Completion Status

One of:

- COMPLETED
- COMPLETED_WITH_UNKNOWNS
- BLOCKED_WRONG_BRANCH
- BLOCKED
```

---

# 52. Mandatory Explicit Answers

## A

```text
Does active Product runtime import, instantiate, or call any ariadne.legacy component?
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

## B

```text
Does active Product scientific execution depend on any implementation owned under ariadne.legacy?
```

同様。

---

## C

```text
Are there scientific capabilities implemented only under ariadne.legacy with no Product/shared equivalent confirmed?
```

回答:

```text
YES
NO
PARTIALLY
UNKNOWN
```

capabilityを列挙する。

---

## D

```text
Does active Product persistence depend on legacy physical tables?
```

回答:

```text
YES
NO_PATH_CONFIRMED
PARTIALLY
UNKNOWN
```

---

## E

```text
Does the Product migration chain depend on legacy migrations or legacy ORM metadata?
```

同様。

---

## F

```text
Does repository-managed deployment configuration invoke legacy API, CLI, worker, or application runtime?
```

同様。

---

## G

```text
Is any legacy runtime exposed through a current pyproject/console-script/package entry point?
```

同様。

---

## H

```text
Do Product tests depend on legacy fixtures/helpers/contracts even when production code does not?
```

回答:

```text
YES
NO_PATH_CONFIRMED
PARTIALLY
UNKNOWN
```

---

## I

```text
Do developer or maintenance tools depend on legacy code?
```

同様。

---

## J

```text
Are there compatibility shims outside ariadne.legacy that preserve legacy contracts?
```

回答:

```text
YES
NO_PATH_CONFIRMED
PARTIALLY
UNKNOWN
```

---

## K

```text
Are there legacy components with no Repository-local incoming consumer confirmed?
```

回答:

```text
YES
NO
UNKNOWN
```

該当componentを列挙する。

これは削除可能性を意味しない。

---

## L

```text
Can Repository-local static evidence alone prove that no external consumer invokes legacy entry points?
```

期待される回答形式:

```text
YES
NO
```

＋理由。

外部consumerの証拠なしを不存在証明として扱ってはならない。

---

# 53. Prohibited Conclusions

以下を書いてはならない。

```text
legacy can now be deleted.

legacy is dead code.

remove src/ariadne/legacy.

this component should be migrated.

keep this scientific implementation.

replace legacy worker.

delete legacy migrations.

drop legacy tables.

remove compatibility contracts.

Product is fully independent, therefore deletion is safe.

ENH-E4 should implement ...
```

以下の事実分類は許可する。

```text
NO_PATH_CONFIRMED

REPOSITORY_UNREFERENCED

TEST_OR_TOOLING_DEPENDENCY_ONLY

PARALLEL_IMPLEMENTATIONS

LEGACY_ONLY_CONFIRMED

ACTIVE_DEPENDENCY
```

---

# 54. Completeness Criteria

### C1

Phase 01〜04 resultを読んでいる。

### C2

legacyを責務単位でInventory化している。

### C3

Repository全体からincoming dependencyを探索している。

### C4

indirect/re-export dependencyを調査している。

### C5

legacy→Product/shared reverse dependencyを調査している。

### C6

scientific capabilityをInventory化している。

### C7

Product/shared scientific implementationと比較している。

### C8

legacy persistence/tableをInventory化している。

### C9

cross-schema dependencyを確認している。

### C10

Product migration chainのlegacy dependencyを確認している。

### C11

legacy runtime rootsを調査している。

### C12

deployment invocationを調査している。

### C13

packaging / console scriptsを調査している。

### C14

test dependencyを調査している。

### C15

tooling dependencyを調査している。

### C16

config dependencyを調査している。

### C17

compatibility shim / contractを調査している。

### C18

data-format compatibilityを必要範囲で調査している。

### C19

responsibility overlap matrixを作成している。

### C20

reachability matrixを作成している。

### C21

reverse blast radiusを作成している。

### C22

negative findingに複数検索evidenceを使用している。

### C23

外部consumer不存在を断定していない。

### C24

Fact / Inference / Unknownを分離している。

### C25

prior-phase IDsを実ファイルから継続している。

### C26

keep/delete/migrate/replace判断をしていない。

### C27

runtime executionをしていない。

### C28

指定result以外を変更していない。

---

# 55. Final Self-Check

result生成後、以下のみ実行する。

```text
git status --short

git diff --stat

git diff -- \
docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/architecture_review/05_legacy_dependency_reachability_matrix_result.md
```

期待される新規変更:

```text
05_legacy_dependency_reachability_matrix_result.md
```

既存working tree変更を変更・stash・restore・resetしてはならない。

---

# 56. Agent Response

作業完了時のchat responseは簡潔に以下を報告する。

```text
05_legacy_dependency_reachability_matrix_result.md を生成しました。

Phase status: <...>
Legacy Components: <count>
Active Product dependencies: <count>
Legacy scientific capabilities: <count>
Repository-unreferenced components: <count>
Unresolved items: <count>

Source/configuration/test/migration codeは変更していません。
```

詳細はresult文書を正本とする。

---

# 57. Stop Condition

以下のいずれかで停止する。

1. `05_legacy_dependency_reachability_matrix_result.md` を生成し、Final Self-Checkを完了した
2. branch不一致
3. static investigationを継続できないblocking issue
4. result以外のRepository変更なしには調査不能

停止後、以下へ進んではならない。

* runtime verification
* legacy deletion
* code migration
* Target Architecture決定
* implementation
* refactoring
* schema変更
* migration変更
* Gate decomposition

次作業は人間によるresult review後、別promptとして指示される。
