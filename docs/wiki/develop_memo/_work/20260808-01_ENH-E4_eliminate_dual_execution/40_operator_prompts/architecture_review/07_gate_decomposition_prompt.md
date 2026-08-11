# 07 Gate Decomposition — Architecture Review Prompt

## 1. Task

`ENH-E4 eliminate dual execution` の Architecture Review Phase 07 として、人間承認済みのTarget Architectureを、**安全に実装・独立検証できるImplementation Gateへ分解する**。

本Phaseの目的は、

```text
Approved Architecture Decisions
        ↓
Architecture Invariants
        ↓
Target Requirements
        ↓
Dependency Ordering
        ↓
Implementation Gates
        ↓
Gate Acceptance Criteria
        ↓
Future Coding / Test Contracts
```

を確定することである。

本Phaseではproduction codeを変更しない。

また、Coding Agent向けの具体的な実装指示書やTest Agent向けの具体的なテスト指示書そのものはまだ作成しない。

本Phaseの成果物は、

> 後続の `10_enhance_instruction` におけるGate単位のImplementation Contract / Test Contractを作成するための正規入力

とする。

---

# 2. Human Approval Baseline

Phase 06で提示されたHuman Decisionsについて、project ownerによる承認が完了している。

本Phaseでは以下を **approved architecture baseline** として扱うこと。

## HD-001

Approved:

```text
Candidate C:
new unified canonical Product Execution aggregate
```

Causal / Exploratory / Predictiveを一つのpersistent Execution authorityへ統合する。

---

## HD-002

Approved:

```text
persistent StageExecution for all canonical workflows
```

Causalを含む全canonical ExecutionでStageExecutionをpersistent first-class childとする。

---

## HD-003

Approved:

```text
ExecutionResult / StageResult semantic levels
under one Result ownership contract
```

Result semantic levelは保持する。

ただしResult lifecycle / identity / ownershipを別architectureとして維持してはならない。

---

## HD-004

Approved:

```text
typed structural lineage
+
generic-only lineage
```

explicit hybrid authority modelを採用する。

typed persistent relationshipで表現されるstructural relationはtyped authority。

generic lineageはtypedでは表現されないrelationに限定する。

closure / exportはprojectionでありauthorityではない。

---

## HD-005

Approved:

```text
external legacy compatibility is out of ENH-E4 scope
```

Repository外のlegacy API / CLI / worker consumerへの互換性維持をENH-E4のrequirementとはしない。

したがって、Phase 06で要求されていたlegacy source retirement前のhuman compatibility decisionは本承認によって満たされたものとする。

ただし、

```text
shared scientific capability
```

までlegacy runtimeと一緒に削除してよいことを意味しない。

---

## HD-006

Approved:

```text
Product-only clean rebuild
no historical application-data migration
```

pre-production ENH-E4ではhistorical application data preservationをrequirementとしない。

canonical bootstrapは、

```text
alembic_product.ini
→ product_migrations
```

のみとする。

root legacy migration chainをcanonical bootstrapへ組み込まない。

---

## HD-007

Approved:

```text
standalone Product scientific CLI remains a low-level utility boundary
```

persistent Product auditabilityを約束しないlow-level CLIはcanonical Execution lifecycle外でよい。

ただしuser-visible / auditable Product analysis CLIを将来提供する場合はcanonical Execution serviceへsubmitする。

---

# 3. Approval Traceability Rule

上記承認は、このPhase 07 promptにproject owner approvalとして記録されたものを正規入力とする。

Phase 06 resultの

```text
PROPOSED_FOR_HUMAN_APPROVAL
```

表記を本Taskで編集してはならない。

代わりにPhase 07 resultへ、

```text
Human Approval Record
```

sectionを作成し、

* HD ID
* approved decision
* related ADR
* implementation consequence

を記録すること。

これにより、

```text
Phase 06 proposal
→ human approval
→ Phase 07 gate decomposition
```

をRepository上で追跡可能にする。

---

# 4. Known Phase 06 Typo

Phase 06 `E4-ADR-003` にある、

```text
one globally unique Product `execution_id);
```

はMarkdown typoとして扱う。

semantic meaningは、

```text
one globally unique Product `execution_id`;
```

である。

Target Architecture変更として扱わない。

Phase 06 result自体は変更しない。

---

# 5. Repository / Context

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

必須入力:

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

40_operator_prompts/architecture_review/
06_target_architecture_decision_record_result.md
```

Database evidence:

```text
40_operator_prompts/database_reinitialization/
99_completion_summary_decision_record.md
```

本Phase出力先:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
architecture_review/
07_gate_decomposition_result.md
```

---

# 6. Positioning

Phase 07ではTarget Architectureを再設計しない。

Phase 06 + human approvalをfixed inputとして、

```text
How should the approved architecture be implemented safely?
```

だけを扱う。

本Phaseでは以下を行う。

* implementation dependency分析
* Gate定義
* Gate順序決定
* Gate scope定義
* Gate acceptance criteria定義
* Gate invariant定義
* temporary transition state定義
* requirement coverage確認
* test responsibility concept定義
* rollback / recovery boundary定義
* final convergence criteria定義

以下は行わない。

* architectureの再選択
* Candidate A/B/Dへの変更
* production implementation
* migration implementation
* exact code patch作成
* exact test implementation
* Coding Agent prompt作成
* Test Agent prompt作成
* unrelated refactoring proposal

---

# 7. Fixed Architecture Decisions

以下のADRはHuman ApprovedとしてGate decompositionへ入力する。

```text
E4-ADR-001 Canonical Product runtime
E4-ADR-002 Unified canonical persistent Execution aggregate
E4-ADR-003 Common Execution identity and mutation semantics
E4-ADR-004 Persistent StageExecution
E4-ADR-005 GenericExecutor workflow-infrastructure boundary
E4-ADR-006 Result semantic levels under one ownership contract
E4-ADR-007 One Product Artifact metadata authority
E4-ADR-008 Typed authority + generic-only lineage
E4-ADR-009 Legacy runtime retirement/archive boundary
E4-ADR-010 Product-only migration/bootstrap
E4-ADR-011 Standalone scientific CLI boundary
E4-ADR-012 Compatibility terminology policy
```

Agentはこれらを再投票・再設計してはならない。

実装上の矛盾を発見した場合のみ、

```text
ARCHITECTURE_CONFLICT_DISCOVERED
```

としてevidence付きで報告する。

その場合も勝手にADRを変更してはならない。

---

# 8. Fixed Architecture Invariants

Phase 06の全 `E4-INV-*` を読み、Gateへ割り当てる。

最低限以下を保持する。

```text
E4-INV-001
Every user-visible Product analysis has exactly one canonical persistent Execution identity.

E4-INV-002
Execution family/type changes workflow semantics, not lifecycle authority.

E4-INV-003
Retry preserves execution identity and differs from rerun/revise.

E4-INV-004
Every canonical Execution has auditable claim/state transition.

E4-INV-005
Claim/lease ownership is centralized.

E4-INV-006
Every canonical Execution has persistent StageExecution children.

E4-INV-007
GenericExecutor does not own canonical lifecycle/persistence.

E4-INV-008
Every Result belongs to canonical Execution and declares semantic level.

E4-INV-009
Every Artifact metadata row has one canonical owner.

E4-INV-010
DB metadata / physical object storage compensation is explicit.

E4-INV-011
Each semantic lineage relation has one authority.

E4-INV-012
Closure/export is not a lineage authority.

E4-INV-013
Canonical Product runtime imports no retired legacy runtime.

E4-INV-014
Shared scientific implementations remain independent.

E4-INV-015
Canonical bootstrap does not invoke legacy migrations.

E4-INV-016
No indefinite dual-read/write remains.
```

Phase 06 resultを正本として全文を確認すること。

---

# 9. Fixed Requirements

Phase 06に定義された、

```text
E4-REQ-001
...
E4-REQ-035
```

を全てGateへmapする。

**1件も欠落してはならない。**

各requirementには、

```text
Primary Completion Gate
```

を必ず1つ割り当てる。

必要なら、

```text
Introduced In
Verified Again In
```

を追加してよい。

ただし、

> どのGateがそのRequirementを最終的に成立させる責任を持つか

は一意にする。

---

# 10. Fixed Constraints

Phase 06の、

```text
E4-CON-001
...
E4-CON-010
```

を全Gateへ適用する。

特に以下は重大constraintである。

```text
Do not redesign scientific algorithms.

Do not make GenericExecutor lifecycle owner.

Do not leave Causal / Family persistence as independent final authorities.

Do not use object_key as semantic identity.

Do not dual-author structural lineage indefinitely.

Any transition dual-read/write must be explicitly bounded.

Do not invoke root legacy migrations in Product bootstrap.

Do not remove shared scientific capability with legacy runtime.

Do not rename compatibility contracts without evidence.

Do not expand unrelated feature scope.
```

---

# 11. Gate Definition

本Phaseでいう `Gate` は、

> 一つ以上のArchitecture Invariantを新たに成立させ、その成立を独立したTest/Audit Agentが判定可能なimplementation checkpoint

である。

Gateは単なる、

```text
edit models
edit services
edit tests
```

という作業分類ではない。

Gate完了時に、

```text
What architectural property is now true?
```

へ明確に回答できなければならない。

---

# 12. Gate ID

Gate ID:

```text
E4-G01
E4-G02
E4-G03
...
```

Gate Acceptance Criterion ID:

```text
E4-G01-AC-001
E4-G01-AC-002
...

E4-G02-AC-001
...
```

Gate Risk ID:

```text
E4-G01-RISK-001
...
```

Gate Transition Debt ID:

```text
E4-TD-001
E4-TD-002
...
```

---

# 13. Gate Granularity Rule

Gate数を事前に固定しない。

ただし、本ENH-E4の規模では原則として、

```text
6〜9 implementation gates
```

程度を目安とする。

これを機械的な必須数とはしない。

Gateを増やす/減らす場合は理由を書く。

避けるもの:

### Too Large

```text
E4-G01:
implement entire ENH-E4
```

### Too Small

```text
E4-G01:
add one enum

E4-G02:
add one column
```

Gateはarchitecture checkpoint単位にする。

---

# 14. Dependency-first Decomposition

Gate順序はfile dependencyではなくArchitecture dependencyから決める。

最低限、以下の依存を分析する。

```text
Canonical persistence/domain contract
        ↓
Canonical application lifecycle
        ↓
Canonical worker/claim
        ↓
Family workflow adapters
        ↓
Runtime cutover
```

および、

```text
Canonical Execution/Stage
        ↓
Result/Artifact ownership
        ↓
Lineage authority
```

および、

```text
Canonical runtime cutover
        ↓
Old Product authority retirement
        ↓
Legacy runtime retirement/archive
        ↓
Final clean bootstrap / audit
```

実際のGate分割はAgentがevidenceに基づいて決める。

---

# 15. Preferred Architectural Sequence

以下を**starting hypothesis**として評価する。

そのまま採用する義務はないが、変更する場合はdependency reasonを記載する。

## Candidate Gate Theme 1

```text
Canonical Domain / Persistence Foundation
```

対象候補:

* unified Execution contract
* family discriminator
* persistent StageExecution
* Result semantic levels
* Artifact metadata authority
* repository/UoW interfaces
* Product migration target schema

このGateではruntime routingをまだ全面cutoverしなくてもよい。

---

## Candidate Gate Theme 2

```text
Canonical Lifecycle / Claim / Worker Foundation
```

対象候補:

* state transitions
* retry/rerun/revise identity semantics
* cancel semantics
* attempt history
* canonical claim/lease
* worker ownership
* GenericExecutor responsibility boundary

---

## Candidate Gate Theme 3

```text
Causal Cutover
```

対象候補:

* Causal submission
* persistent StageExecution
* Result/Artifact creation
* worker dispatch
* canonical mutation semantics

Gate終了時にはCausal user-visible analysisについてold Causal lifecycle authorityがruntime authorityでないことを検証する。

---

## Candidate Gate Theme 4

```text
Exploratory / Predictive Cutover
```

対象候補:

* family submission
* family stage adaptation
* Result/Artifact adaptation
* claim path replacement
* retry/rerun/revise normalization

Gate終了時には、Causal / Exploratory / Predictiveの全user-visible Product executionがone canonical persistent authorityへ到達することを検証する。

これはENH-E4の中心convergence checkpoint候補である。

---

## Candidate Gate Theme 5

```text
Lineage Authority Consolidation
```

対象候補:

* typed structural authority
* generic-only allowlist
* duplicate structural generic writes停止
* closure/export projection
* source-class representation
* mutation lineage semantics

---

## Candidate Gate Theme 6

```text
Obsolete Product Authority Retirement
```

対象候補:

* old independent Causal/Family lifecycle paths
* old tables/repositories/services
* transitional readers/writers
* unused family persistence paths
* duplicate Result/Artifact authorities

実際に削除する対象はdependency evidenceによって決める。

単に名前だけで削除しない。

---

## Candidate Gate Theme 7

```text
Legacy Runtime Boundary / Compatibility Cleanup
```

対象候補:

* legacy API/CLI/worker canonical exposure removal
* legacy runtime/archive boundary
* preserve shared scientific modules
* packaging/deployment import audit
* standalone Product CLI contract

Human approval HD-005は取得済みである。

ただしshared scientific codeを削除してはならない。

---

## Candidate Gate Theme 8

```text
Clean Bootstrap / Final Convergence
```

対象候補:

* Product-only clean rebuild
* runtime start
* Causal/Exploratory/Predictive Golden Paths
* retry/rerun/revise/cancel
* Result/Artifact
* Lineage
* import/deployment architecture audit
* zero dual authority verification

---

# 16. Important Ordering Question

以下を明示的に検討する。

```text
Should Result / Artifact ownership consolidation be:
A. part of the persistence foundation,
B. a separate gate before workflow cutover,
C. implemented incrementally inside each family cutover?
```

同様に、

```text
Should Lineage authority consolidation happen:
A. before family cutover,
B. during each family cutover,
C. after all executions use canonical IDs?
```

最も安全でtraceableなorderingを選ぶ。

理由を記載する。

---

# 17. No Hidden Dual Authority

Gate途中ではtemporary coexistenceが必要な場合がある。

ただし、

```text
old implementation exists
```

と

```text
old implementation remains authoritative
```

を区別する。

各Gateについて、

```text
Authority Before Gate
Authority After Gate
```

を必ず記載する。

---

# 18. Transitional Dual Read / Write Rule

Gateで一時的にdual-read / dual-writeを導入する場合、

以下を必ず記録する。

```text
Transition Debt ID
Owner
Reason
Introduced Gate
Allowed Readers
Allowed Writers
Authority
Reconciliation Rule
Exit Gate
Exit Acceptance Criterion
```

以下は禁止。

```text
temporarily use both
```

だけを書いて終了すること。

---

# 19. Transition Debt Register

Resultに以下を作る。

| TD ID | Introduced Gate | Temporary State | Authority | Exit Gate | Exit Criterion |
| ----- | --------------- | --------------- | --------- | --------- | -------------- |

最終Gate終了時:

```text
OPEN TRANSITION DEBT = 0
```

でなければならない。

---

# 20. Gate Independence

各Gateは、

* implementation report
* Test Agent result
* PASS / FAIL / BLOCKED

を独立して持てる粒度とする。

次Gateは原則として前Gate PASS後にのみ開始できる。

例外的な並行Gateを認める場合は、

* shared schema conflictなし
* authority conflictなし
* merge ordering明確

を証明する。

本ENH-E4では安全性を優先し、原則serial Gateを推奨する。

---

# 21. Gate Acceptance Criteria

各Gateには最低限以下の種類のAcceptance Criteriaを含める。

## Structural AC

例:

```text
canonical entity/repository exists
old runtime import absent
typed relation exists
```

---

## Behavioral AC

例:

```text
submission reaches canonical lifecycle
retry preserves ID
family dispatch works
```

---

## Persistence AC

例:

```text
one canonical row created
stage rows persisted
old table not written
```

---

## Negative AC

重要。

例:

```text
no old FamilyExecution write occurs
GenericExecutor does not commit
no structural generic lineage edge is written
```

---

## Regression AC

例:

```text
scientific behavior remains callable
API contract remains valid where in scope
```

---

## Traceability AC

例:

```text
Result / Artifact / Lineage can be traced back to canonical execution_id
```

---

# 22. Acceptance Criteria Quality

Acceptance Criteriaは、

```text
works correctly
architecture is unified
tests pass
```

のような曖昧表現を禁止する。

Test Agentが、

```text
PASS
FAIL
BLOCKED
```

を客観判定できる形式とする。

具体的なtest commandはPhase 07ではまだ書かなくてよい。

ただし、

```text
static architecture test
unit test
integration test
DB inspection
clean bootstrap
concurrency test
API test
```

等のVerification Methodは記載する。

---

# 23. Acceptance Criterion Mapping

各ACに、

```text
Requirement IDs
Invariant IDs
ADR IDs
```

をmapする。

例:

| AC | ADR | INV | REQ | Verification Method |
| -- | --- | --- | --- | ------------------- |

---

# 24. Gate Entry Criteria

各Gateに、

```text
Prerequisite Gates
Required Accepted Decisions
Required Schema State
Required Runtime State
Required Transition Debt State
```

を定義する。

---

# 25. Gate Exit Criteria

各GateのExitは、

```text
all mandatory AC PASS
no blocking defect
no unauthorized architecture deviation
transition debt explicitly registered
implementation report complete
independent test report complete
```

を基本とする。

実際の運用契約は後続文書で定義する。

---

# 26. Gate Failure Semantics

Gate failure時に、

```text
continue anyway
```

を許可してはならない。

Classification:

```text
FAIL_FIX_IN_GATE
BLOCKED_ARCHITECTURE_CONFLICT
BLOCKED_ENVIRONMENT
```

次Gateへ進める条件を明示する。

---

# 27. Schema Change Placement

Targetはclean rebuildを採用している。

したがって、

> historical production data migrationを前提とする複雑なcompatibility migration

をGateへ追加してはならない。

ただしschema change自体はAlembic Product migrationとして管理する。

Gate decompositionで、

* canonical schema introduction
* old Product schema authority retirement
* final clean rebuild

をどのGateへ置くか明確にする。

---

# 28. Old Product Tables

以下のcurrent tables等について、

```text
product_execution
product_family_execution
product_family_stage_execution
product_result
product_family_result
product_artifact
product_family_artifact
product_lineage_edge
```

Target Architectureとの関係をGate decomposition上で整理する。

注意:

このリストの全tableを削除することを要求しているわけではない。

Target semanticsに再利用可能なtableがある可能性もある。

判断基準:

```text
Does it remain an independent authority?
```

であり、

```text
Does the old table name survive?
```

ではない。

---

# 29. Canonical Schema Naming

Phase 07ではfinal table / class nameを必ずしも固定しなくてよい。

ただしGateごとに、

```text
semantic persistence contract
```

は明示する。

Coding Agentがarchitectureを再解釈しなければ実装できないほど曖昧にしてはならない。

必要なら、

```text
schema design decision required inside approved ADR boundary
```

としてGate内deliverableにできる。

しかし新しいADRを勝手に作ることは避ける。

---

# 30. Causal Cutover Rule

Causal cutover Gateでは最低限、

```text
submission
execution identity
stage persistence
worker claim
state
Result
Artifact
cancel
retry
```

をcanonical pathへ接続する。

Gate終了時に、

> Causal submissionはcanonical pathへ行くがretryだけold serviceへ行く

のようなhidden dual lifecycleを許さない。

---

# 31. Exploratory / Predictive Cutover Rule

Exploratory / Predictiveは同じFamily tableを共有していてもservice semanticsが異なるため、両方を独立にAcceptance Criteriaへ含める。

最低限:

```text
submission
stage generation
claim
processing
Result
Artifact
cancel
retry
rerun
revise where supported
```

を確認する。

---

# 32. Convergence Gate

必ずどこか一つのGateを、

```text
Product Execution Convergence Gate
```

として識別する。

そのGate終了時に以下が成立しなければならない。

```text
Causal
Exploratory
Predictive
```

のuser-visible Product analysesが全て、

```text
one canonical Execution identity
one canonical lifecycle authority
one canonical claim authority
one Result/Artifact ownership contract
```

を利用する。

この時点以降、old Causal/Family persistent lifecycleを新規write authorityとして使用してはならない。

---

# 33. Result / Artifact Gate Requirements

Gate decompositionでは最低限以下を完了責任へ割り当てる。

```text
ExecutionResult / StageResult semantic level
canonical Result ID
Result cardinality
Artifact metadata ownership
ArtifactStorePort
artifact-only stage output policy
Result / Artifact downstream reference
object_key non-authority
physical-storage compensation
```

---

# 34. Lineage Gate Requirements

最低限以下を完了責任へ割り当てる。

```text
typed structural authority
generic-only allowlist
endpoint/project validation
uniqueness
delete/retention
closure projection
export relation source class
retry/rerun/revise lineage
structural generic dual-write elimination
```

Lineage Gate終了時、

```text
one semantic relation
→ one authority
```

が成立すること。

---

# 35. Legacy Gate Requirements

HD-005承認済みを入力とし、

legacy runtime retirement/archiveをGateへ配置してよい。

ただし以下を分離する。

```text
legacy API
legacy CLI
legacy worker
legacy orchestration
legacy persistence
legacy ArtifactLineage
historical migrations
shared scientific modules
```

Shared:

```text
ariadne.causal
ariadne.preprocessing
ariadne.shared
```

等をlegacy orchestrationと一緒に除去してはならない。

---

# 36. Legacy Source Deletion

Phase 06では、

```text
ARCHIVE_SOURCE
REPLACE_BEFORE_RETIRE
RETIRE_RUNTIME
```

等が提案されている。

Gate decompositionでは、

* runtime retirement
* source deletion/archive
* replacement dependency

を同義に扱わない。

source removalが不必要なら、ENH-E4の成功条件に無理に含めなくてよい。

重要なのは、

```text
no active duplicate architecture authority
```

である。

---

# 37. CLI Gate Requirements

low-level scientific CLIはpersistent lifecycle外を維持してよい。

Acceptance Criteriaで、

```text
does not silently write canonical/alternative persistent execution lifecycle
```

を確認する。

user-visible/auditable CLIが存在する場合のみcanonical Execution経由を要求する。

---

# 38. Scientific Preservation Gate

各主要cutover Gateで、

```text
shared scientific algorithm implementation
```

が再実装されていないことを確認する。

最低限、

* imports
* adapters
* runner bindings
* scientific unit test surface

を確認対象にする。

Numerical methodology redesignはENH-E4 scope外。

---

# 39. Final Gate

最終Gateは単なるtest rerunではない。

**Architecture Convergence Audit** を含むこと。

最低限:

```text
Product-only clean DB bootstrap

application startup

Causal Golden Path

Exploratory Golden Path

Predictive Golden Path

retry

rerun

revise

cancel

Execution / Stage persistence

Result / Artifact ownership

Lineage closure

no structural lineage dual authority

no old Product lifecycle writes

no canonical runtime import of retired legacy code

shared scientific modules preserved

root legacy migrations not invoked

OPEN TRANSITION DEBT = 0
```

を検証する。

---

# 40. Final Architecture Static Audit

Final Gateへ以下を入れる。

Repository-wide static searchにより、

* old execution repository/service references
* direct family lifecycle persistence
* old runtime registration
* retired legacy imports
* structural generic lineage writers
* forbidden migration references

が残っていないか確認する。

「文字列が0件」でなく、

```text
forbidden runtime authority path = 0
```

を目的とする。

test / historical docs / migration archive等の正当なreferenceは区別する。

---

# 41. Clean Bootstrap Verification

Final Gateでは、

```text
empty database
→ product migrations
→ startup
→ Product Golden Paths
```

を検証する。

root legacy migration chainを実行してはならない。

Phase 07自身では実行しない。

Test Contractで後に実行させるVerification Conceptとして定義する。

---

# 42. Gate Rollback / Recovery

各Gateについて、

```text
If this Gate fails after code changes, what repository/schema state must be restored before retry?
```

を記載する。

clean rebuild前提であっても、

* partially migrated source
* partially switched router
* old/new writer coexistence

を放置して次Gateへ進めない。

具体的Git commandまでは不要。

---

# 43. Gate Scope Boundaries

各Gateに、

```text
In Scope
Explicitly Out of Scope
```

を記載する。

Out of Scopeの例:

```text
unrelated frontend redesign
scientific algorithm rewrite
legacy historical data migration
contract rename unrelated to cutover
performance optimization
```

---

# 44. Expected Change Areas

各Gateについて、

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
Legacy
Packaging
Deployment
Tests
Docs
```

のうち変更対象となる領域を示す。

具体的file listはPhase 07では必須でない。

明確なsource areaが特定できる場合は記載してよい。

---

# 45. Coding Contract Input

各Gateについて、後続Implementation Instructionへ渡す最低inputを作る。

```text
Gate ID
Objective
Prerequisites
In Scope
Out of Scope
ADR
Invariant
Requirements
Expected Architecture After Gate
Acceptance Criteria
Transition Debt
Forbidden Changes
```

---

# 46. Test Contract Input

各Gateについて、後続Test Instructionへ渡す最低inputを作る。

```text
Gate ID
Acceptance Criterion
Verification Method
Required Evidence
Negative Checks
Regression Scope
Environment Assumptions
PASS condition
FAIL condition
BLOCKED condition
```

具体的commandは後続Test Instructionで確定する。

---

# 47. Requirement Coverage Matrix

必ず以下を作る。

| Requirement | Primary Gate | Supporting Gate(s) | Acceptance Criteria |
| ----------- | ------------ | ------------------ | ------------------- |

対象:

```text
E4-REQ-001 ... E4-REQ-035
```

Coverage checks:

```text
Missing requirements = 0
Requirements without primary gate = 0
```

---

# 48. Invariant Coverage Matrix

| Invariant | First Established Gate | Reverified Gate(s) | Acceptance Criteria |
| --------- | ---------------------- | ------------------ | ------------------- |

対象:

```text
E4-INV-001 ... E4-INV-016
```

---

# 49. ADR Coverage Matrix

| ADR | Implementation Gate(s) | Final Verification Gate |
| --- | ---------------------- | ----------------------- |

対象:

```text
E4-ADR-001 ... E4-ADR-012
```

---

# 50. Constraint Coverage Matrix

| Constraint | Gates Where Relevant | Enforcement |
| ---------- | -------------------- | ----------- |

対象:

```text
E4-CON-001 ... E4-CON-010
```

---

# 51. Gate Dependency Graph

ASCIIでGate dependency graphを作成する。

例:

```text
E4-G01
  ↓
E4-G02
  ↓
...
```

並行可能Gateがある場合は分岐を示す。

ただしserial executionを推奨するならその理由を記載する。

---

# 52. Critical Path

Architecture convergenceまでのcritical pathを明示する。

各Gateに時間見積りは不要。

以下を記載する。

```text
Why this Gate blocks the next Gate
```

---

# 53. Authority Transition Table

非常に重要。

以下を作る。

| Gate Boundary | Execution Authority | Result Authority | Artifact Authority | Lineage Authority | Old Authority Still Writable? |
| ------------- | ------------------- | ---------------- | ------------------ | ----------------- | ----------------------------- |

Gateごとにauthorityがどう変わるかを可視化する。

---

# 54. Forbidden Intermediate States

以下のようなintermediate stateを明示的に禁止する。

```text
Both old and new Execution services accept new submissions indefinitely.

Causal uses canonical Execution but old Result authority.

Family uses canonical Execution but old claim service.

GenericExecutor starts committing lifecycle state.

Typed and generic lineage independently write the same structural edge without bounded transition.

Old Product tables remain active new-write authorities after convergence Gate.

Legacy runtime becomes a fallback canonical Product execution path.

Root legacy migrations are required to bootstrap Product target DB.
```

必要なものを追加する。

---

# 55. Gate Naming

Gate名はarchitecture outcomeが分かる名称にする。

Good:

```text
E4-G03 Causal Canonical Execution Cutover
```

Bad:

```text
E4-G03 Backend Changes
```

---

# 56. Decision on Gate Count

Resultで以下を明示する。

```text
Selected gate count:
Why this count:
Why fewer gates are unsafe:
Why more gates add little isolation:
```

---

# 57. Additional Evidence

Gate decompositionに不可欠なfile-level dependencyが不明な場合のみ、read-only source調査を追加してよい。

新しいArchitecture Decisionを探索する目的で調査を広げてはならない。

新しいFactが得られた場合は、既存最大 `E4-OBS-*` の次から採番する。

---

# 58. Architecture Conflict

Approved ADRとproduction realityが実装不能なレベルで矛盾している場合、

```text
ARCHITECTURE_CONFLICT_DISCOVERED
```

とする。

記録:

```text
ADR
Conflicting evidence
Why gate decomposition cannot safely resolve it
Minimal decision that must be revisited
```

軽微なclass/table naming issueをarchitecture conflictとして扱わない。

---

# 59. Prohibited Operations

禁止:

* production code変更
* test code変更
* configuration変更
* migration変更
* dependency変更
* database変更
* database reset
* migration execution
* container操作
* application起動
* worker起動
* frontend起動
* pytest
* runtime integration test
* benchmark
* HTTP request
* external network
* refactoring
* code deletion
* legacy retirement execution

唯一許可されるRepositoryへの書き込み:

```text
07_gate_decomposition_result.md
```

および必要なparent directoryのみ。

---

# 60. Investigation Method

read-onlyで使用可:

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
static AST parsing
```

source / schema / tests / prior resultsを読むことは許可する。

application moduleをimportして実行してはならない。

---

# 61. Evidence Standard

Gate分割の主要判断には、

```text
Source:
- ADR / INV / REQ
- prior Phase evidence
- source path if additionally inspected

Reason:
<why this implementation ordering is required>
```

を記載する。

Gate decompositionはOpinionではなく、dependencyとauthority transitionによって説明する。

---

# 62. Required Result Structure

`07_gate_decomposition_result.md` は以下の構造とする。

```markdown
# 07 Gate Decomposition Result

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

## 2. Human Approval Record

| HD | Approved Decision | ADR | Implementation Consequence |
|---|---|---|---|

State explicitly:

`HD-001 through HD-007 are accepted inputs for this decomposition.`

## 3. Approved Architecture Baseline

### ADRs

### Invariants

### Requirements

### Constraints

## 4. Decomposition Principles

## 5. Selected Gate Count

- Count:
- Why:
- Why fewer:
- Why more:

## 6. Gate Overview

| Gate | Name | Architecture Outcome | Primary ADRs | Prerequisites |
|---|---|---|---|---|

## 7. Gate Dependency Graph

## 8. Authority Transition Table

| Boundary | Execution | Result | Artifact | Lineage | Old Writable Authority |
|---|---|---|---|---|---|

## 9. Transition Debt Register

| TD | Introduced | State | Authority | Exit Gate | Exit Criterion |
|---|---|---|---|---|---|

## 10. Gate Definitions

### E4-G01 — <name>

#### Objective

#### Architecture Before Gate

#### Architecture After Gate

#### Prerequisites

#### In Scope

#### Explicitly Out of Scope

#### ADR Coverage

#### Invariant Coverage

#### Requirement Coverage

#### Constraint Coverage

#### Expected Change Areas

#### Acceptance Criteria

| AC | Criterion | ADR | INV | REQ | Verification Method |
|---|---|---|---|---|---|

#### Negative Acceptance Criteria

#### Transition Debt Introduced

#### Transition Debt Closed

#### Risks

| Risk | Cause | Required Mitigation / Verification |
|---|---|---|

#### Rollback / Recovery Boundary

#### Coding Contract Input

#### Test Contract Input

#### Exit Condition

Repeat for every Gate.

## 11. Product Execution Convergence Gate

Identify exactly one Gate.

Explain why after this Gate:

- Causal
- Exploratory
- Predictive

all use one canonical Product Execution authority.

List evidence expected from Test Agent.

## 12. Result / Artifact Consolidation Strategy

State whether consolidation is:
- foundation-first
- separate pre-cutover gate
- family-by-family

and why.

## 13. Lineage Consolidation Ordering

State when Lineage authority changes relative to Execution cutover and why.

## 14. Old Product Authority Retirement

List current authority surfaces that must cease being active authorities.

Do not assume deletion is necessary.

## 15. Legacy Runtime / Source Boundary

### Retired runtime surfaces

### Preserved shared scientific modules

### Archived/historical surfaces

### Source deletion requirements, if any

## 16. Migration / Bootstrap Placement

### Target schema introduction Gate

### Old schema retirement Gate

### Final clean rebuild Gate

## 17. CLI Boundary

## 18. Scientific Capability Preservation

## 19. Requirement Coverage Matrix

| Requirement | Primary Gate | Supporting Gates | AC |
|---|---|---|---|

Include E4-REQ-001 through E4-REQ-035.

## 20. Invariant Coverage Matrix

| Invariant | First Established | Reverified | AC |
|---|---|---|---|

Include E4-INV-001 through E4-INV-016.

## 21. ADR Coverage Matrix

| ADR | Implementation Gate(s) | Final Verification |
|---|---|---|

Include E4-ADR-001 through E4-ADR-012.

## 22. Constraint Coverage Matrix

| Constraint | Relevant Gates | Enforcement |
|---|---|---|

Include E4-CON-001 through E4-CON-010.

## 23. Forbidden Intermediate States

## 24. Critical Path

| Gate | Why It Blocks Next |
|---|---|

## 25. Parallelism Assessment

State whether any Gates may safely run in parallel.

Default:
`SERIAL`

If parallel:
provide dependency proof.

## 26. Final Gate Architecture Convergence Audit

List all mandatory final checks.

## 27. Remaining Unknowns

| ID | Impact | Blocking? | Assigned Gate / Handling |
|---|---|---|---|

## 28. Architecture Conflicts

If none:

`NONE`

## 29. New Facts

Only if new static evidence was gathered.

## 30. Gate Decomposition Quality Check

Explicitly answer:

1. Does every E4-REQ have exactly one Primary Completion Gate?
2. Does every E4-INV have a first establishment Gate?
3. Does every ADR map to implementation and final verification?
4. Does each Gate have objectively testable ACs?
5. Is exactly one Product Execution Convergence Gate identified?
6. After that Gate, can any old Product lifecycle still accept new writes?
7. Does any Gate leave GenericExecutor as lifecycle owner?
8. Does any final-state structural lineage relation have dual authority?
9. Is every temporary dual-read/write state bounded by a Transition Debt exit Gate?
10. Does the final Gate require OPEN TRANSITION DEBT = 0?
11. Are shared scientific modules explicitly preserved?
12. Is Product bootstrap independent of root legacy migrations?
13. Is historical data migration excluded consistently with HD-006?
14. Is standalone low-level CLI kept distinct without creating another persistent lifecycle?
15. Is implementation sequencing sufficient to create future Coding/Test contracts without architecture reinterpretation?

Answer:
- YES
- NO
- PARTIALLY
- UNKNOWN

with explanation.

## 31. Recommendation

One of:

- READY_FOR_IMPLEMENTATION_CONTRACT_AUTHORING
- NEEDS_ARCHITECTURE_REVISION
- NEEDS_ADDITIONAL_EVIDENCE
- BLOCKED

## 32. Completion Status

One of:

- COMPLETED
- COMPLETED_WITH_NONBLOCKING_UNKNOWNS
- BLOCKED_WRONG_BRANCH
- BLOCKED
```

---

# 63. Mandatory Final Checks

Before marking the Phase complete, calculate and report:

```text
ADR count mapped
Invariant count mapped
Requirement count mapped
Constraint count mapped
Gate count
Acceptance Criterion count
Open Transition Debt after final Gate
```

Expected coverage:

```text
ADR = all Phase 06 ADRs
Invariant = all Phase 06 invariants
Requirement = all E4-REQ-001..035
Constraint = all E4-CON-001..010
Open Transition Debt after final Gate = 0
```

If counts do not match, Phase status cannot be `COMPLETED`.

---

# 64. Gate Acceptance Criterion Minimum

Each Gate must contain at least:

```text
1 structural criterion
1 behavioral criterion where runtime behavior changes
1 persistence criterion where persistence changes
1 negative criterion
1 regression criterion
```

If a category is legitimately N/A, explain why.

---

# 65. Convergence Gate Mandatory ACs

The Product Execution Convergence Gate must include criteria equivalent to:

```text
Causal submission creates canonical Execution.

Exploratory submission creates canonical Execution.

Predictive submission creates canonical Execution.

All three families use the same canonical claim authority.

All three families create persistent StageExecution.

All three families use canonical Result / Artifact ownership.

No old Causal/Family lifecycle accepts new Product writes.

GenericExecutor remains subordinate workflow infrastructure.
```

Exact wording/IDs should be generated in the result.

---

# 66. Lineage Gate Mandatory ACs

Must include criteria equivalent to:

```text
Structural relations are typed-authoritative.

Generic-only relations are explicitly allowed.

Structural generic dual-write is absent in final state.

Closure consumes authoritative sources but is not authority.

Export identifies relation source class.

Retry/rerun/revise preserve target lineage semantics.
```

---

# 67. Legacy Boundary Mandatory ACs

Must include criteria equivalent to:

```text
Canonical Product runtime imports no retired ariadne.legacy runtime module.

Repository-managed deployment does not invoke legacy API/CLI/worker.

Shared scientific modules remain available.

Historical legacy migration chain is not required by Product bootstrap.

Low-level standalone Product CLI does not create an alternative persistent lifecycle.
```

---

# 68. Final Gate Mandatory ACs

Must include:

```text
clean Product bootstrap from empty DB

application startup

Causal Golden Path

Exploratory Golden Path

Predictive Golden Path

retry contract

rerun contract

revise contract

cancel contract

Stage persistence

Result semantic levels

Artifact metadata / store boundary

Lineage authority

no old Product new-write authority

no retired legacy runtime dependency

scientific capability preservation

root legacy migrations not invoked

OPEN TRANSITION DEBT = 0
```

---

# 69. No Implementation Detail Drift

Phase 07 may identify expected architectural change areas.

It must not dictate speculative implementation details such as:

```text
rename class X to Y
move file A to B
use exact SQL snippet
replace library
introduce a new framework
```

unless Phase 06 approved contract logically requires it.

The future Coding Contract will resolve code-level details within these boundaries.

---

# 70. Final Self-Check

result生成後、以下のみ実行する。

```text
git status --short

git diff --stat

git diff -- \
docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/architecture_review/07_gate_decomposition_result.md
```

期待される新規変更:

```text
07_gate_decomposition_result.md
```

既存working tree変更を変更・stash・restore・resetしてはならない。

---

# 71. Agent Response

作業完了時のchat responseは簡潔に以下を報告する。

```text
07_gate_decomposition_result.md を生成しました。

Phase status: <...>
Implementation Gates: <count>
Acceptance Criteria: <count>
Requirements mapped: <count>/35
Invariants mapped: <count>
Transition Debt open after final Gate: <count>
Recommendation: <...>

Source/configuration/test/migration codeは変更していません。
```

詳細はresult文書を正本とする。

---

# 72. Stop Condition

以下のいずれかで停止する。

1. `07_gate_decomposition_result.md` を生成し、Final Self-Checkを完了した
2. branch不一致
3. Approved Architectureとの重大なconflictを確認した
4. safe Gate decompositionに不可欠なevidenceが不足した

停止後、以下へ進んではならない。

* production implementation
* migration implementation
* legacy deletion
* Coding Agent実行
* Test Agent実行
* `10_enhance_instruction` のImplementation Contract作成
* `10_enhance_instruction` のTest Contract作成

次作業は人間によるGate decomposition review後、別promptとして指示される。
