# 06 Target Architecture Decision Record — Architecture Review Prompt

## 1. Task

`ENH-E4 eliminate dual execution` の Architecture Review Phase 06 として、Phase 01〜05で取得したRepository evidenceを統合し、**ENH-E4のTarget Architectureを提案するArchitecture Decision Record** を作成する。

本Phaseは、これまでのInventory Phaseとは異なり、単なる現状観測ではない。

以下を明示的に行う。

```text
Current Architecture Evidence
        ↓
Architectural Problem Definition
        ↓
Candidate Architectures
        ↓
Trade-off Analysis
        ↓
Recommended Target Architecture
        ↓
Architecture Decisions
        ↓
Required Invariants
        ↓
Implementation Implications
        ↓
Gate Decomposition Input
```

ただし、本Phaseではコード・schema・migration・test等を変更してはならない。

本Phaseの成果物は、

> 実装指示書を作る前に、人間がTarget Architectureをレビュー・承認するためのDecision Record

である。

各Architecture Decisionのstatusは原則として、

```text
PROPOSED_FOR_HUMAN_APPROVAL
```

とする。

Agent自身が `ACCEPTED` としてはならない。

---

# 2. Repository / Context

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

Architecture Review evidence:

```text
40_operator_prompts/architecture_review/
01_runtime_entrypoint_inventory_result.md

40_operator_prompts/architecture_review/
02_execution_lifecycle_inventory_result.md

40_operator_prompts/architecture_review/
03_result_artifact_ownership_inventory_result.md

40_operator_prompts/architecture_review/
04_lineage_responsibility_inventory_result.md

40_operator_prompts/architecture_review/
05_legacy_dependency_reachability_matrix_result.md
```

Database reinitialization evidenceも確認すること。

最低限:

```text
40_operator_prompts/database_reinitialization/
99_completion_summary_decision_record.md
```

および、そのdecision recordが参照しているclean rebuild evidence。

本Phase出力先:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
architecture_review/
06_target_architecture_decision_record_result.md
```

調査開始時点のcommit SHAを記録すること。

---

# 3. Positioning

Phase 01〜05は、

```text
What exists?
What is reachable?
What owns lifecycle?
What is duplicated?
What depends on legacy?
```

を確認した。

Phase 06では、

```text
What should remain authoritative?
What should become canonical?
What should cease to be an independent architecture?
What compatibility boundary should remain?
What invariants must the implementation establish?
```

を決定案として提示する。

本Phase終了後、人間がDecision Recordをレビューする。

人間承認前に以下へ進んではならない。

* production code変更
* migration変更
* schema変更
* legacy削除
* implementation
* test変更
* GateごとのCoding Agent実行

---

# 4. Required Evidence Inputs

Phase 01〜05 resultをすべて読むこと。

単にExecutive Summaryだけを読まず、最低限以下を確認する。

```text
Facts
Inferences
Mandatory Explicit Answers
Unresolved Items
Phase Conclusion
```

また、各resultが参照するproduction source evidenceへ必要に応じて戻ること。

Decisionに重大な影響を与える事実は、prior resultだけでなくproduction sourceも再確認してよい。

ただし静的read-only調査に限定する。

---

# 5. Evidence Hierarchy

Decisionの根拠は以下の順に扱う。

```text
1. production source / schema / migration
2. Architecture Review observations
3. active tests
4. repository-managed deployment/configuration
5. documentation / comments
6. inference
```

低いrankの証拠が高いrankの証拠と矛盾する場合、高いrankを優先する。

矛盾自体はDecision Recordへ記録する。

---

# 6. ID Continuity

Phase 01〜05 resultから実際の最大番号を確認する。

```text
E4-OBS-*
E4-INF-*
E4-UNK-*
```

追加調査で新しいFact / Inference / Unknownが生じた場合は、その次の番号から続ける。

Architecture Decision ID:

```text
E4-ADR-001
E4-ADR-002
E4-ADR-003
...
```

Target Architecture Requirement ID:

```text
E4-REQ-001
E4-REQ-002
E4-REQ-003
...
```

Architecture Invariant ID:

```text
E4-INV-001
E4-INV-002
E4-INV-003
...
```

Implementation Constraint ID:

```text
E4-CON-001
E4-CON-002
E4-CON-003
...
```

---

# 7. Decision Status

各 `E4-ADR-*` は以下のstatusのいずれかとする。

## `PROPOSED_FOR_HUMAN_APPROVAL`

evidenceから一つの案を推奨できる。

## `BLOCKED_BY_EVIDENCE`

Target Architectureを決定するには重大なevidence不足がある。

## `DEFERRED`

ENH-E4のscope外であり、今回決める必要がない。

原則として `PROPOSED_FOR_HUMAN_APPROVAL` を目指す。

軽微なUnknownを理由に全DecisionをBLOCKしてはならない。

---

# 8. Architectural Goal

ENH-E4の目的を、Phase 01〜05 evidenceに基づいて具体化する。

抽象的な

```text
remove duplication
clean up legacy
simplify architecture
```

だけでは不十分。

最低限以下の観点からProblem Statementを作る。

```text
Execution identity
Execution lifecycle
persistent state
worker claim
stage lifecycle
Result ownership
Artifact ownership
Lineage representation
retry/rerun/revise semantics
legacy runtime surface
migration/schema ownership
scientific implementation ownership
```

---

# 9. Non-goals

ENH-E4で解決しない事項を明示する。

例えば以下はevidenceに基づきscope判定する。

```text
scientific algorithm redesign
statistical methodology redesign
frontend redesign
performance optimization
generic plugin architecture
new external compatibility framework
historical data migration
```

実際のRepository / project contextを確認して決定する。

---

# 10. Target Architecture Decision Domains

最低限、以下のDecision Domainを全て扱うこと。

---

## D1. Canonical Runtime Architecture

決定すること:

> Ariadneのrepository-managed production runtimeとして、どのarchitecture familyをcanonicalとするか。

確認対象:

```text
Product API
Product worker
Product persistent lifecycle
standalone scientific CLI
legacy API
legacy worker
legacy CLI
```

必ず、

```text
canonical runtime
non-canonical tooling
retired runtime surface
out-of-scope standalone utility
```

を区別する。

---

## D2. Canonical Persistent Execution Model

最重要Decisionの一つ。

少なくとも以下の候補を比較する。

### Candidate A

既存Causal Execution modelをcanonical化し、Family executionをそこへ統合する。

### Candidate B

既存Family Execution modelをcanonical化し、Causal executionをそこへ統合する。

### Candidate C

既存どちらかをそのままcanonicalとせず、新しいunified Execution aggregateへ統合する。

### Candidate D

複数persistent Execution lifecycleを維持し、役割だけ明文化する。

Candidate Dについても比較対象には含める。

ただしENH-E4の目的との整合性を評価する。

比較dimension:

```text
Execution identity
domain entity
table
repository abstraction
state model
worker claim
stage persistence
retry
rerun
revise
cancel
Result ownership
Lineage integration
migration complexity
testability
future extension
```

---

# 11. Canonical Execution Identity

Target Architectureとして、

```text
execution_id
```

が何を一意に識別するかを定義する。

以下を明確化する。

* Causal / Exploratory / Predictiveでnamespaceを共通化するか
* execution type/familyをdiscriminatorとして持つか
* retry時にIDを維持するか
* rerun時に新IDを作るか
* revise時に新IDを作るか
* parent/base relationをどう扱うか

具体的なcolumn名までは必要な範囲でのみ決める。

---

# 12. Execution Type / Family Representation

Target Architectureで、

```text
CAUSAL
EXPLORATORY
PREDICTIVE
```

等のfamily差を、

* separate Execution entity
* discriminator
* plan type
* workflow specification
* runner selection

のどこで表現するかを決定する。

「familyが違うからtableも違う」を無条件に採用してはならない。

逆に、「全部Executionだから完全に同じ」を無条件に採用してもならない。

---

# 13. Canonical State Machine

Target Architectureとして一つのExecution lifecycle contractを定義する。

最低限:

```text
creation
queued
claim
running
success
failure
cancel request
cancel
retry
rerun
revise
```

について、

* 共通state
* operation semantics
* terminal state
* invalid transition

を決定する。

全analysis familyで不要なstateは無理に導入しない。

---

# 14. Worker Claim Architecture

決定する。

* one canonical claim mechanismか
* execution-family-specific claimを許すか
* repository abstraction
* transaction boundary
* locking
* lease/heartbeat

Phase 02で不明な項目が残っている場合も、

Target Architectureとして必要なinvariantは決めてよい。

ただし現状事実とTarget requirementを区別する。

---

# 15. Stage Persistence Architecture

重要Decision。

比較する。

### Option A

全ExecutionでStageExecutionをpersistent first-class entityとする。

### Option B

Stageはworkflow内部のephemeral conceptとし、persistent Executionのみをcanonicalとする。

### Option C

workflow typeによりpersistent / ephemeralを許すが、明確なcontractを設ける。

以下を評価する。

```text
retry granularity
progress visibility
auditability
Result ownership
Lineage
failure recovery
workflow semantics
schema complexity
```

---

# 16. GenericExecutor Responsibility

Target Architectureで `GenericExecutor` が何を所有するかを決定する。

候補責務:

```text
plan validation
stage ordering
binding resolution
runner invocation
stage outcome generation
persistent lifecycle
transaction
retry
claim
Result persistence
```

Phase 02で確認したCurrent responsibilityとTarget responsibilityを分離する。

`GenericExecutor` を単に「共通だからcanonical lifecycle owner」にしてはならない。

---

# 17. Canonical Result Model

少なくとも以下を比較する。

### Candidate A

Causal `product_result` semanticsをcanonicalにする。

### Candidate B

Family `product_family_result` semanticsをcanonicalにする。

### Candidate C

新しいunified Result modelを定義する。

### Candidate D

Execution-level ResultとStage-level Resultを異なるfirst-class conceptとして明示的に残す。

重要:

Candidate Dは、

```text
duplicate Result architecture
```

と、

```text
different semantic aggregate
```

を区別するための候補である。

比較dimension:

```text
identity
execution scope
stage scope
cardinality
payload
API consumption
downstream reuse
retry/rerun
lineage
```

---

# 18. Canonical Artifact Model

決定すること:

* Artifact metadata model
* Resultとのrelation
* Executionとのrelation
* physical Artifact storage ownership
* ArtifactStorePortの位置づけ
* Causal/Family metadata分離を維持するか

physical object storageとmetadata schemaを別々に判断する。

---

# 19. Result / Artifact Ownership Invariant

Target Architectureで、

```text
who creates
who persists
who deletes
who owns physical object
who links lineage
```

を一意に定める。

複数serviceが同じ責務を独立実装する状態を残す場合は、その理由を明示する。

---

# 20. Downstream Reuse Contract

Result / Artifactを後続Execution inputとして利用するcontractを決定する。

最低限:

```text
Result ID
Artifact ID
typed source reference
physical URI
```

のどれをcanonical referenceとするかを検討する。

scientific runner内部の物理formatまでは必要以上に固定しない。

---

# 21. Canonical Lineage Architecture

最重要Decisionの一つ。

少なくとも以下の候補を比較する。

### Candidate A — Derived authoritative

typed persistent relationshipsをauthoritativeとし、Lineageはquery時に導出する。

### Candidate B — Persisted generic authoritative

generic LineageEdgeをauthoritative relationとする。

### Candidate C — Explicit hybrid

typed relationとpersisted generic edgeを異なる責務に限定し、重複semantic edgeを禁止または明示的に同期する。

### Candidate D — Materialized projection

typed relationshipをauthoritativeとし、generic edgeを再構築可能なmaterialized projection/cacheとして扱う。

Candidate名は必要に応じて調整してよい。

比較dimension:

```text
source of truth
information uniqueness
reconstructability
consistency
write complexity
read complexity
closure traversal
cross-model extensibility
retry/revise semantics
schema integrity
auditability
```

---

# 22. Lineage Duplicate Representation Policy

Target Architectureでは必ず、

> 同一semantic relationをtyped FKとgeneric edgeの双方へ独立にwriteしてよいか

を決定する。

許す場合:

* sync invariant
* transaction
* reconciliation
* conflict resolution

をTarget requirementとして定義する。

許さない場合:

* どちらがauthoritativeか
* generic-only relationをどう扱うか

を定義する。

---

# 23. Generic-only Lineage Relations

Phase 04で確認された、

> typed relationから完全には再構築できないgeneric relation

が存在する場合、それを無視してはならない。

各relationについて、

```text
retain as generic relation
promote to typed domain relation
remove from requirement
other explicit representation
```

の候補を比較する。

具体的なrelationごとに判断する。

---

# 24. Legacy Architecture Policy

Phase 05 evidenceに基づき、`ariadne.legacy` のTarget policyを提案する。

少なくとも以下を分離する。

```text
legacy API
legacy CLI
legacy worker
legacy execution/control plane
legacy persistence
legacy migration chain
legacy Result/Artifact
legacy lineage
legacy orchestration
shared scientific implementations
legacy compatibility strings/contracts
```

重要:

```text
ariadne.causal
ariadne.preprocessing
ariadne.shared
```

等、legacyから利用されているshared scientific modulesを、

`ariadne.legacy` と同一視してはならない。

---

# 25. Legacy Policy Candidates

最低限以下を比較する。

### Candidate A

legacy packageをRepositoryに残すが非canonical historical implementationとして隔離する。

### Candidate B

legacy runtime / persistence / orchestration sourceをRepositoryから撤去し、shared scientific modulesだけを維持する。

### Candidate C

legacyをarchive locationへ移し、active source treeから除外する。

### Candidate D

一部legacy componentをProductへ移植してから残りをretireする。

Phase 05のdependency evidenceから最も妥当な案を推奨する。

---

# 26. External Consumer Boundary

Phase 05で外部consumerが静的Repository調査では確認不能な場合、それをTarget Decisionから無視してはならない。

以下のいずれかを推奨する。

```text
A. external compatibility is explicitly not a requirement for ENH-E4

B. external consumer inventory is a prerequisite before legacy removal

C. temporary compatibility window is required
```

どれを選ぶべきか、Repository内のproject context / requirement / development stage evidenceから判断する。

判断材料がない場合のみ、

```text
HUMAN_DECISION_REQUIRED
```

とする。

単にUnknownだから全Target Architectureをblockしてはならない。

---

# 27. Migration / Data Policy

Database reinitialization evidenceを読み、Target Architecture変更時のdata policyを提案する。

候補:

```text
in-place migration
one-time destructive clean rebuild
compatibility migration
dual-read transition
dual-write transition
```

既存データ保持がrequirementとして確認できない場合、それを明示する。

逆に保持不要と証明できない場合は推測しない。

Target Architectureの複雑性に重大な影響を与えるDecisionとして扱う。

---

# 28. Migration Chain Policy

決定対象:

```text
alembic_product.ini / product_migrations
root alembic.ini / legacy migrations
```

Target Architectureで、

* canonical migration chain
* legacy migration historyの扱い
* clean install behavior
* schema bootstrap

を提案する。

migration file削除自体は本Phaseで行わない。

---

# 29. Standalone Scientific CLI Policy

Phase 01/02で確認されたstandalone scientific CLIについて、

> persistent Product Execution lifecycleへ参加しないことが、意図されたtool boundaryなのか、解消すべきsecond execution pathなのか

をArchitecture Decisionとして扱う。

最低限以下を比較する。

### Option A

CLIはlow-level scientific utilityとして明確にExecution architecture外とする。

### Option B

CLIもcanonical Product Execution lifecycle経由へ統合する。

判断基準:

```text
purpose
persistence requirement
auditability
user-facing execution semantics
package contract
test contract
duplication of orchestration
```

---

# 30. Compatibility Terminology

以下のようなlegacy-named Product contractが存在する場合、

```text
legacy-product-snapshot/1
legacy_* names
old table terminology
```

Target Architectureで、

* runtime compatibility requirement
* historical naming only
* rename candidate
* retain until separate migration

のいずれかを提案する。

名称だけでlegacy architecture dependencyとはみなさない。

---

# 31. Architectural Decision Criteria

各Candidateを以下で比較する。

```text
Single Source of Truth
Semantic Coherence
Lifecycle Consistency
Persistence Consistency
Failure / Retry Correctness
Lineage Integrity
Traceability / Auditability
Scientific Capability Preservation
Migration Simplicity
Operational Simplicity
Testability
Future Extensibility
Removal of Duplicate Responsibility
Risk of Hidden Compatibility Break
```

数値scoreを無理につけなくてよい。

以下で評価する。

```text
STRONG
ACCEPTABLE
WEAK
UNACCEPTABLE
UNKNOWN
```

評価理由を必ず記載する。

---

# 32. Minimum Necessary Change Principle

Target Architectureは、

> 二重アーキテクチャを除去するために必要な変更

を中心とする。

以下を理由なく同時に再設計してはならない。

* scientific algorithms
* frontend UX
* unrelated dataset model
* unrelated auth
* unrelated deployment system

ただし、二重architecture解消に不可欠ならscopeに含める。

---

# 33. No Transitional Dual Architecture by Default

Target案として、

```text
old and new both remain authoritative indefinitely
```

を安易に選んではならない。

transition期間だけdual write / dual readが必要なら、

```text
temporary
bounded
exit criteria defined
```

であることを要求する。

永久的な二重管理をTarget Architectureとする場合は、ENH-E4目的と整合する強い理由が必要。

---

# 34. Architecture Invariants

Target Architectureから、実装後に常に成立すべきinvariantを `E4-INV-*` として定義する。

例示:

```text
Exactly one canonical persistent Execution identity exists for user-visible Product executions.

A semantic lineage relation has exactly one authoritative source.

Product runtime does not import retired legacy runtime code.
```

これは例であり、evidenceとDecisionから実際のinvariantを作る。

最低限以下をカバーする。

```text
Execution
State
Worker claim
Result
Artifact
Lineage
Migration
Legacy dependency
```

---

# 35. Target Requirements

各ADRから実装可能なrequirementを `E4-REQ-*` として導出する。

Requirementは、

```text
The system SHALL ...
```

相当の検証可能な形式にする。

抽象的な、

```text
architecture shall be clean
```

は禁止。

例:

```text
All repository-managed Product analysis submissions SHALL create the same canonical Execution entity.
```

実際のDecisionに基づいて作成する。

---

# 36. Implementation Constraints

`E4-CON-*` として、

実装時に破ってはいけない制約を定義する。

例:

```text
Scientific estimators SHALL NOT be reimplemented as part of ENH-E4.

No compatibility dual-write SHALL remain after the final Gate.

Product migration bootstrap SHALL produce the target schema without invoking the legacy migration chain.
```

実際のevidence / Decisionに基づくこと。

---

# 37. Candidate Architecture Diagrams

最低限、

```text
Current Architecture
Recommended Target Architecture
```

をASCII diagramで示す。

CurrentはPhase 01〜05 evidenceから描く。

Targetは推奨Decisionを反映する。

diagramがsource of truthにならないよう、ADR / requirementを正文とする。

---

# 38. Current Architecture Diagram Requirements

最低限以下を示す。

```text
API / UI
Worker
Execution lifecycle(s)
GenericExecutor
Result
Artifact
Lineage
Legacy boundary
Scientific shared modules
```

---

# 39. Target Architecture Diagram Requirements

最低限以下を示す。

```text
canonical runtime entry
canonical Execution
workflow/stage boundary
Result
Artifact
Lineage
scientific runner
legacy/retired boundary
```

---

# 40. Alternative Rejection

推奨しなかった主要Candidateごとに、

```text
Rejected / Not Recommended Because
```

を記録する。

単に、

```text
more complex
```

ではなく、

* どのevidenceと衝突するか
* 何の二重責務が残るか
* 何のmigration burdenが増えるか

を記載する。

---

# 41. Risk Analysis

推奨Target Architectureについて、

| Risk | Cause | Impact | Mitigation / Verification |
| ---- | ----- | ------ | ------------------------- |

を作る。

最低限:

```text
behavior regression
scientific regression
data/schema regression
lineage loss
retry/rerun regression
frontend/API mismatch
legacy external consumer
migration/bootstrap failure
```

を検討する。

存在しないriskを無理に作らない。

---

# 42. Open Decision Handling

重大なDecisionだけが人間判断を必要とする場合、

```text
HUMAN_DECISION_REQUIRED
```

として独立sectionに出す。

必ず以下を含める。

```text
Question
Option A
Option B
Recommended option
Evidence
Consequence if deferred
```

Agentが合理的に推奨できる場合は、単に質問を投げて停止しない。

---

# 43. Traceability

必ず、

```text
Observation / Inference
        ↓
ADR
        ↓
Invariant
        ↓
Requirement
        ↓
Implementation implication
```

を追えるようにする。

Traceability Matrix:

| Evidence | ADR | Invariant | Requirement | Implementation Area |
| -------- | --- | --------- | ----------- | ------------------- |

---

# 44. Implementation Area Classification

各requirementを次の領域へmapする。

```text
Domain
Application
Persistence
Worker
Workflow
Web API
Frontend
Lineage
Migration
Legacy source
Packaging
Deployment
Tests
Documentation
```

これはGate decompositionの入力とする。

まだGate自体は作らない。

---

# 45. Decision Dependency Graph

ADR間の依存関係を記録する。

例:

```text
Execution ADR
    ↓
Result ADR
    ↓
Lineage ADR
    ↓
Migration ADR
```

実際のDecisionに基づいて作る。

循環dependencyがある場合は明示する。

---

# 46. Required Explicit Decision Domains

最低限、個別ADRとして以下を扱うこと。

```text
E4-ADR-xxx Canonical Runtime Boundary

E4-ADR-xxx Canonical Persistent Execution Model

E4-ADR-xxx Execution Type / Family Representation

E4-ADR-xxx Canonical State / Mutation Semantics

E4-ADR-xxx Worker Claim Ownership

E4-ADR-xxx Stage Persistence Model

E4-ADR-xxx GenericExecutor Responsibility

E4-ADR-xxx Result Ownership Model

E4-ADR-xxx Artifact Ownership Model

E4-ADR-xxx Downstream Reuse Contract

E4-ADR-xxx Lineage Source of Truth

E4-ADR-xxx Generic-only Lineage Relations

E4-ADR-xxx Legacy Runtime Policy

E4-ADR-xxx Shared Scientific Capability Boundary

E4-ADR-xxx Migration / Data Reset Policy

E4-ADR-xxx Migration Chain Policy

E4-ADR-xxx Standalone Scientific CLI Policy

E4-ADR-xxx Compatibility Contract Policy
```

必要ならADRを追加してよい。

---

# 47. Legacy Decision Safety Rule

Legacyに関するDecisionでは必ず、

```text
Repository-local evidence
```

と

```text
external consumer assumption
```

を分離する。

例えば、

```text
Repository evidence:
no current Product import/deployment/package entry.

Decision assumption:
external legacy runtime compatibility is not required.
```

のように記載する。

後者が確認できない場合はHuman Decisionとして出す。

---

# 48. Scientific Capability Safety Rule

shared scientific modulesについて、

```text
legacy uses this module
```

という理由で削除対象に含めてはならない。

必ず、

```text
implementation owner
active Product consumer
legacy consumer
```

を区別する。

ENH-E4では原則として、

> execution/persistence architectureの統合

と

> scientific implementationの変更

を分離する。

---

# 49. Migration Safety Rule

data migration / destructive rebuildに関するDecisionは、

database reinitialization evidenceとproject requirementを確認してから行う。

推測で、

```text
existing data can be discarded
```

または

```text
existing data must be preserved
```

と決めてはならない。

---

# 50. Prohibited Operations

禁止:

* production code変更
* test変更
* configuration変更
* migration変更
* dependency変更
* database変更
* container操作
* application起動
* worker起動
* frontend起動
* runtime test
* database test
* migration execution
* refactoring
* deletion

唯一許可される書き込み:

```text
06_target_architecture_decision_record_result.md
```

および必要なparent directoryのみ。

---

# 51. Allowed Investigation

read-onlyで以下を使用してよい。

```text
git
git grep
rg
grep
find
sed
cat
awk
tree
static AST analysis
```

prior evidenceの確認に必要なsource / migration / test / docsを読むことは許可する。

network accessは禁止。

---

# 52. Required Result Structure

`06_target_architecture_decision_record_result.md` は以下の構造とする。

```markdown
# 06 Target Architecture Decision Record

## 1. Metadata

- Prompt:
- Prior phases:
- Repository:
- Branch:
- HEAD:
- Working tree status:
- Started at:
- Finished at:
- Status:

## 2. Executive Decision Summary

### Recommended Target Architecture

### Decisions Requiring Human Approval

### Decisions Blocked by Evidence

## 3. Current Architecture Problem Statement

### 3.1 Runtime

### 3.2 Execution

### 3.3 Result / Artifact

### 3.4 Lineage

### 3.5 Legacy

### 3.6 Migration

## 4. Architectural Goals

## 5. Non-goals

## 6. Decision Criteria

| Criterion | Meaning |
|---|---|

## 7. Candidate Architecture Overview

### Candidate A

### Candidate B

### Candidate C

...

## 8. Candidate Comparison Matrix

| Criterion | Candidate A | Candidate B | Candidate C | Notes |
|---|---|---|---|---|

## 9. Recommended Target Architecture

### 9.1 Runtime

### 9.2 Execution

### 9.3 Stage

### 9.4 Worker

### 9.5 GenericExecutor

### 9.6 Result

### 9.7 Artifact

### 9.8 Downstream Reuse

### 9.9 Lineage

### 9.10 Legacy

### 9.11 Migration

### 9.12 CLI

## 10. Current Architecture Diagram

## 11. Target Architecture Diagram

## 12. Architecture Decisions

### E4-ADR-001 — ...

- Status:
- Context:
- Evidence:
- Decision:
- Alternatives:
- Rationale:
- Consequences:
- Risks:
- Human approval required:
- Derived requirements:

Repeat.

## 13. Architecture Invariants

| ID | Invariant | Derived From |
|---|---|---|

## 14. Target Architecture Requirements

| ID | Requirement | ADR | Verification Concept |
|---|---|---|---|

## 15. Implementation Constraints

| ID | Constraint | Rationale | ADR |
|---|---|---|---|

## 16. Legacy Component Target Classification

| Legacy Component | Proposed Target Status | Reason | Dependency Evidence | Human Approval |
|---|---|---|---|---|

Allowed proposed statuses:

- RETIRE_RUNTIME
- RETIRE_SOURCE
- ARCHIVE_SOURCE
- RETAIN_SHARED_CAPABILITY
- RETAIN_COMPATIBILITY_TEMPORARILY
- REPLACE_BEFORE_RETIRE
- OUT_OF_SCOPE
- HUMAN_DECISION_REQUIRED

This is a proposal, not an executed change.

## 17. Lineage Relation Target Classification

| Relation | Current Representation | Proposed Authority | Secondary Representation | Rationale |
|---|---|---|---|---|

## 18. Execution Mutation Semantics

| Operation | Target Identity Semantics | Result Semantics | Lineage Semantics |
|---|---|---|---|

Cover:
- retry
- rerun
- revise
- cancel

## 19. Data / Migration Policy

### Existing Data Assumption

### Target Bootstrap

### Migration Chain

### Compatibility

## 20. Scientific Capability Preservation

| Capability | Current Owner | Target Owner | Change Allowed? | Evidence |
|---|---|---|---|---|

## 21. Compatibility Boundary

### Repository-local

### External

### Data formats

### API/CLI

## 22. Risks

| Risk | Cause | Impact | Mitigation / Verification |
|---|---|---|---|

## 23. Human Decisions Required

| ID | Question | Options | Recommendation | Evidence | Blocking? |
|---|---|---|---|---|---|

If none:

`NONE`

## 24. ADR Dependency Graph

## 25. Traceability Matrix

| Evidence | ADR | Invariant | Requirement | Implementation Area |
|---|---|---|---|---|

## 26. Implementation Area Impact

| Area | Requirements | Expected Change Type |
|---|---|---|

Do not enumerate exact code edits unless needed to explain architecture.

## 27. Rejected Alternatives

### Alternative ...

- Why considered:
- Why not recommended:
- Evidence:

## 28. Remaining Unknowns

| ID | Impact on Target Architecture | Blocking? | Handling |
|---|---|---|---|

## 29. New Facts

Continue E4-OBS numbering only if additional static investigation produced new facts.

## 30. New Inferences

Continue E4-INF numbering only if needed.

## 31. Decision Quality Check

Explicitly answer:

1. Does the recommended target leave more than one authoritative persistent Product Execution lifecycle?
2. Does it leave more than one authoritative Result ownership model for the same semantic Result?
3. Does it leave more than one authoritative Artifact ownership model for the same semantic Artifact?
4. Can one semantic Lineage relation have two independent authoritative sources?
5. Does active Product runtime depend on retired legacy runtime code?
6. Does the proposed migration/bootstrap require the legacy migration chain?
7. Are shared scientific implementations preserved independently from legacy orchestration?
8. Is any proposed dual-read/dual-write state temporary and bounded?
9. Can each architecture decision be traced to prior evidence?
10. Are unresolved external compatibility assumptions explicit?

Use:

- YES
- NO
- PARTIALLY
- UNKNOWN

and explain.

## 32. Recommendation

State whether the record is:

- READY_FOR_HUMAN_APPROVAL
- NEEDS_ADDITIONAL_EVIDENCE
- BLOCKED

## 33. Completion Status

One of:

- COMPLETED
- COMPLETED_WITH_HUMAN_DECISIONS
- BLOCKED_WRONG_BRANCH
- BLOCKED
```

---

# 53. Mandatory Decision Quality Requirements

The recommendation must satisfy or explicitly justify violation of the following.

## Q1

Target Architecture must identify exactly one canonical repository-managed persistent Execution architecture for user-visible Product analysis.

If not, explain why this does not preserve the ENH-E4 dual architecture.

---

## Q2

Target Architecture must distinguish:

```text
Execution lifecycle
```

from

```text
scientific workflow execution
```

and define ownership of each.

---

## Q3

Target Architecture must define Result semantics independently from current table names.

---

## Q4

Target Architecture must define Artifact metadata ownership independently from physical Artifact storage.

---

## Q5

Target Architecture must define one authority rule for each semantic Lineage relation.

---

## Q6

If generic LineageEdge remains, its role must be one of:

```text
authoritative domain relation
supplementary relation store
materialized projection
explicit generic-only relation store
```

or another precisely defined role.

It may not remain ambiguously authoritative.

---

## Q7

Target Architecture must explicitly determine the fate of active dual Execution persistence.

---

## Q8

Target Architecture must explicitly determine whether persistent StageExecution is part of the canonical model.

---

## Q9

Target Architecture must explicitly determine retry / rerun / revise identity semantics.

---

## Q10

Target Architecture must explicitly separate legacy orchestration from shared scientific implementations.

---

## Q11

Target Architecture must explicitly state the migration/data preservation assumption.

---

## Q12

Target Architecture must not rely on indefinite dual write / dual read as the final state.

---

# 54. Prohibited Conclusions

Do not select architecture based only on:

```text
the newer code looks cleaner

Product is newer

Family supports more features

Causal is simpler

legacy has legacy in the name

this table seems redundant
```

Every material Decision requires evidence and architectural rationale.

---

# 55. Completeness Criteria

### C1

Phase 01〜05 resultsを読んでいる。

### C2

database reinitialization decision evidenceを読んでいる。

### C3

Current Architecture Problemをevidenceベースで定義している。

### C4

複数のCandidate Architectureを比較している。

### C5

canonical Execution modelを提案している。

### C6

Execution identity / state / mutation semanticsを定義している。

### C7

worker claim ownershipを定義している。

### C8

Stage persistence policyを定義している。

### C9

GenericExecutor responsibilityを定義している。

### C10

Result ownershipを定義している。

### C11

Artifact ownershipを定義している。

### C12

downstream reuse contractを定義している。

### C13

Lineage authorityを定義している。

### C14

generic-only lineage relationsを扱っている。

### C15

legacy policyをcomponent単位で提案している。

### C16

shared scientific modulesをlegacy orchestrationから分離している。

### C17

external consumer assumptionを明示している。

### C18

migration/data policyを明示している。

### C19

standalone CLI policyを明示している。

### C20

compatibility terminology/data contractを扱っている。

### C21

ADR / Invariant / Requirementを作成している。

### C22

traceability matrixを作成している。

### C23

rejected alternativesを記録している。

### C24

riskを記録している。

### C25

Human Decisionが必要なら推奨案付きで明示している。

### C26

コード変更をしていない。

### C27

Gate decompositionをまだ行っていない。

---

# 56. Final Self-Check

result生成後、以下のみ実行する。

```text
git status --short

git diff --stat

git diff -- \
docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/architecture_review/06_target_architecture_decision_record_result.md
```

期待される新規変更:

```text
06_target_architecture_decision_record_result.md
```

既存working tree変更を変更・stash・restore・resetしてはならない。

---

# 57. Agent Response

作業完了時のchat responseは簡潔に以下を報告する。

```text
06_target_architecture_decision_record_result.md を生成しました。

Status: <...>
Architecture Decisions: <count>
Target Requirements: <count>
Architecture Invariants: <count>
Human Decisions Required: <count>

Source/configuration/test/migration codeは変更していません。
```

詳細はresult文書を正本とする。

---

# 58. Stop Condition

以下のいずれかで停止する。

1. `06_target_architecture_decision_record_result.md` を生成し、Final Self-Checkを完了した
2. branch不一致
3. Target Architectureに不可欠なevidenceが不足し `BLOCKED` となった

停止後、以下へ進んではならない。

* production implementation
* migration implementation
* legacy deletion
* Gate decomposition
* Coding Agent instruction
* Test Agent instruction

次作業は人間によるTarget Architecture Decision Recordのレビュー後、別promptとして指示される。
