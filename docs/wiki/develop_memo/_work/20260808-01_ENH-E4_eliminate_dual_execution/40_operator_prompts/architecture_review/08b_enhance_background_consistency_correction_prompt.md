# 08b Enhance Background Consistency Correction — Operator Prompt

## 1. Task

`ENH-E4 eliminate dual execution` の Architecture Review / Enhance Background materialization補正として、Phase 08でmaterializeされたEnhance背景・要件・設計snapshotについて、**approved ENH-E4 Target Architectureと矛盾するnormative記述のみをin-place修正する**。

本Taskは文書の全面再生成ではない。

目的は、

```text
Phase 08 materialized documents
        ↓
detect normative contradictions
        ↓
minimal in-place correction
        ↓
ENH-E4 target snapshot becomes internally consistent
        ↓
G01 independent review input
```

を成立させることである。

本TaskではArchitecture Decisionを変更しない。

production code、test、migration、configuration、databaseを変更しない。

---

# 2. Background

Phase 08のmaterializationは以下について構造的には完了している。

```text
E4-REQ coverage = 35/35
E4-ADR coverage = 12/12
E4-INV coverage = 16/16
E4-CON coverage = 10/10
HD coverage = 7/7
placeholder = 0
```

しかし独立レビューにより、

> ENH-E3 baselineを全文保持した結果、一部の旧normative clauseとENH-E4 approved target clauseが同一snapshot内で同時に現在形のauthorityとして読める

問題が確認された。

これはArchitecture Reviewのやり直しではなく、

```text
materialization consistency correction
```

である。

---

# 3. Repository / Branch

Repository:

```text
causal-atelier
```

Required branch:

```text
refactor/ariadne_mvp_e4
```

Work directory:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
```

Prompt:

```text
40_operator_prompts/
architecture_review/
08b_enhance_background_consistency_correction_prompt.md
```

Result:

```text
40_operator_prompts/
architecture_review/
08b_enhance_background_consistency_correction_result.md
```

---

# 4. Required Inputs

必ず以下を読むこと。

## 4.1 Architecture Evidence

```text
40_operator_prompts/architecture_review/
01_runtime_entrypoint_inventory_result.md

02_execution_lifecycle_inventory_result.md

03_result_artifact_ownership_inventory_result.md

04_lineage_responsibility_inventory_result.md

05_legacy_dependency_reachability_matrix_result.md

06_target_architecture_decision_record_result.md

07_gate_decomposition_result.md

08_enhance_background_materialization_result.md
```

---

## 4.2 Materialized Documents

```text
00_enhance_background/
01_Enhance構想・要件改定計画.md

00_enhance_background/
02_Enhance構想承認記録.md

00_enhance_background/
03_要件定義書改定.md

00_enhance_background/
04_設計書改定.md

00_enhance_background/
05_要件・設計整合性およびトレーサビリティ確認.md
```

および:

```text
00_enhance_background/
Revised_requirements_definition_documents/
00_プロダクトコンセプトメモ.md

10_要件定義.md

21_論理データ設計.md

22_プロダクト基本設計.md

23_API・インターフェース設計.md

30_詳細設計.md
```

---

## 4.3 Baseline Documents

比較目的でread-only:

```text
docs/wiki/requirement_definition/
00_プロダクトコンセプトメモ.md

10_要件定義.md

21_論理データ設計.md

22_プロダクト基本設計.md

23_API・インターフェース設計.md

30_詳細設計.md
```

baseline originalsは変更してはならない。

---

# 5. Fixed Human Approval

以下は再議論しない。

```text
HD-001
new unified canonical Product Execution aggregate

HD-002
persistent StageExecution for all canonical workflows

HD-003
ExecutionResult / StageResult semantic levels
under one Result ownership contract

HD-004
typed structural lineage + generic-only lineage

HD-005
external legacy compatibility is out of ENH-E4 scope

HD-006
Product-only clean rebuild
no historical application-data migration

HD-007
standalone Product scientific CLI remains
a low-level utility boundary
```

---

# 6. Fixed Architecture

以下はapproved architecture baseline。

```text
E4-ADR-001 ... E4-ADR-012
E4-INV-001 ... E4-INV-016
E4-REQ-001 ... E4-REQ-035
E4-CON-001 ... E4-CON-010
```

以下もfixed Gate decomposition。

```text
E4-G01 ... E4-G08
```

本Taskで新しいADRを作ってはならない。

---

# 7. Primary Correction Principle

Materialized snapshotは、

```text
historical ENH-E3 document
+
ENH-E4 appendix
```

ではなく、

> ENH-E4承認後に適用されるRequirement / Designのcomplete target snapshot

として読めなければならない。

したがって、

```text
old normative clause
```

と

```text
new ENH-E4 normative clause
```

が矛盾する場合、

**両方をそのまま現在有効なMUSTとして残してはならない。**

---

# 8. Minimal-change Rule

ただしbaseline全体を書き直してはならない。

修正対象は、

> approved ENH-E4 targetとsemantic conflictを起こすnormative clause

だけに限定する。

以下は原則変更しない。

* ENH-E4と無関係なfunctional requirements
* scientific requirements
* frontend requirements
* auth requirements
* unrelated API requirements
* unrelated data entities
* stylistic wording
* heading structure
* document ordering
* unrelated terminology

---

# 9. Correction Method

conflicting clauseを発見した場合は以下の順で処理する。

```text
1. locate conflicting normative clause
2. identify related ADR / REQ / INV / CON
3. confirm approved target semantics
4. minimally rewrite the clause
5. preserve unaffected surrounding content
6. verify no contradictory normative clause remains
```

単に末尾へ、

```text
ENH-E4 takes precedence
```

と追記して矛盾本文を放置するだけでは不十分な場合がある。

特に明確なMUST / SHALL / architecture ownershipの矛盾は本文を正規化する。

---

# 10. Mandatory Correction A — Snapshot Status / Precedence

6 snapshot documentsについて、document statusを明確にする。

対象:

```text
Revised_requirements_definition_documents/
00_プロダクトコンセプトメモ.md
10_要件定義.md
21_論理データ設計.md
22_プロダクト基本設計.md
23_API・インターフェース設計.md
30_詳細設計.md
```

冒頭またはdocument metadataとして最低限以下相当を明示する。

```text
Snapshot status:
ENH-E4 approved target requirement/design snapshot.

Baseline:
The corresponding approved pre-ENH-E4 requirement/design document.

Precedence:
Where baseline normative text conflicts with an approved ENH-E4
ADR / requirement / invariant / constraint,
the ENH-E4 target contract is authoritative.

Implementation status:
This document describes the approved target contract.
It does not by itself assert that production implementation is complete.
```

日本語で記載してよい。

---

# 11. ENH-E3 Status Normalization

snapshot内に、

```text
ENH-E3正本
ENH-E3承認済み正本
本書はENH-E3の正本
```

等がdocument-current-statusとして残っている場合、ENH-E4 target snapshotとして正規化する。

historical provenanceとしてENH-E3を記録すること自体は禁止しない。

ただし、

> このsnapshot自体がENH-E3のみの現行正本である

と読めるmetadataを残してはならない。

---

# 12. Mandatory Correction B — GenericExecutor Responsibility

最重要修正。

Approved targetでは、

```text
GenericExecutor
```

はcanonical persistent Execution lifecycle ownerではない。

Target responsibility:

```text
plan validation
stage/workflow sequencing
dependency resolution
binding resolution
scientific runner invocation
in-memory / workflow-level outcome construction
```

相当。

Target responsibilityではないもの:

```text
canonical Execution creation
canonical lifecycle state authority
worker claim authority
lease authority
canonical retry ownership
canonical rerun ownership
canonical revise ownership
canonical cancel state authority
transaction ownership for canonical lifecycle
canonical Result persistence ownership
canonical Artifact metadata persistence ownership
Execution aggregate commit authority
```

Phase 06 / E4-ADR / E4-REQを正本としてexact responsibilityを確認する。

---

# 13. Known GenericExecutor Conflict

最低限以下を検索する。

```text
Generic Executor
GenericExecutor
claim
retry
artifact commit
Artifact commit
Result保存
Result persistence
Execution aggregate
aggregate status
commit
cancel
```

特に:

```text
Revised_requirements_definition_documents/
10_要件定義.md

22_プロダクト基本設計.md

30_詳細設計.md
```

を精査する。

旧ENH-E3 clauseが、

> GenericExecutor自身がcanonical lifecycle / claim / persistenceを所有する

意味になっている場合、ENH-E4 approved responsibilityへ最小修正する。

---

# 14. GenericExecutor Correction Rule

例えば旧記述が、

```text
Generic Executor SHALL claim executions,
commit artifacts/results,
control retry,
and update aggregate status.
```

相当の場合、

単に削除して意味を失わせるのではなく、

```text
Canonical lifecycle/application service owns
claim/state/mutation/persistence.

GenericExecutor receives an already-owned workflow execution context
and performs plan/stage/scientific execution within that boundary.
```

相当のtarget contractへ正規化する。

実際の文言は既存文書のstyleに合わせる。

---

# 15. Mandatory Correction C — Result Semantic Levels

Approved architecture:

```text
ExecutionResult
StageResult
```

はsemantic levelとして区別される。

ただし、

```text
separate Result architectures
```

ではない。

one canonical Result ownership contractの下に存在する。

以下をsnapshot全体で一貫させる。

---

# 16. Result Logical Ownership

最低限、logical contractとして以下を明示する。

```text
Every canonical Result belongs to exactly one canonical Execution.
```

Result semantic levelは、

```text
EXECUTION
STAGE
```

相当の区別を持つ。

具体的enum名はapproved designが固定していなければ新規決定しない。

---

# 17. ExecutionResult Contract

Execution-level Resultについて最低限:

```text
execution ownership:
required

stage ownership:
not applicable / absent / null

semantic meaning:
result representing the Execution-level outcome
```

を明示する。

physical column nullable designまで本Taskで新規決定する必要はない。

ただしlogical relationshipは曖昧にしない。

---

# 18. StageResult Contract

Stage-level Resultについて最低限:

```text
execution ownership:
required

stage ownership:
required

stage ownership consistency:
the referenced StageExecution belongs to the same canonical Execution

semantic meaning:
result produced by a specific persistent StageExecution
```

を明示する。

---

# 19. Result Cardinality

G01 `E4-G01-AC-002` を満たせる粒度でlogical cardinalityを明記する。

Phase 03 / Phase 06 / approved requirementsを確認し、

```text
Execution
StageExecution
ExecutionResult
StageResult
Artifact
```

のownership/cardinalityを記述する。

推測は禁止。

approved evidenceでexact maximum cardinalityを決定できない場合でも、

```text
exactly one parent
zero-or-more children
one-or-more where lifecycle requires it
```

など、evidenceで正当化できるlogical multiplicityは明示する。

---

# 20. Cardinality Evidence Rule

cardinalityを新規創作してはならない。

次を優先する。

```text
1. Phase 06 approved requirement / invariant
2. Phase 03 Result/Artifact ownership inventory
3. current production model where compatible with Target
```

approved contractから判断不能なcardinalityがG01に不可欠な場合:

```text
BLOCKS_G01_CONTRACT
```

として08b resultに記載する。

その場合、推測で埋めない。

---

# 21. Artifact Ownership Correction

Approved architectureでは、

```text
Artifact metadata authority
```

と

```text
physical Artifact storage
```

を分離する。

snapshotで最低限以下を一貫させる。

```text
Artifact metadata has one canonical ownership authority.

ArtifactStorePort / physical object storage
does not define semantic identity.

object_key / URI is not canonical Result/Artifact semantic identity.
```

---

# 22. Artifact Cardinality

Phase 03 / Phase 06 evidenceから確認可能な範囲で、

* Result → Artifact
* Artifact → owner
* StageResult / ExecutionResultとの関係

を明示する。

same physical objectをreuseできる可能性と、

```text
canonical metadata ownership
```

を混同しない。

---

# 23. Mandatory Correction D — Old Execution Authority

snapshot全体を検索し、以下相当の旧architecture記述を確認する。

```text
Causal Execution is separately authoritative

Family Execution is separately authoritative

product_execution and product_family_execution
are both target lifecycle authorities

Exploratory/Predictive use separate lifecycle owner

Causal uses different claim authority as target design
```

Current Architecture説明として存在することは許容する。

しかしTarget / MUST / SHALLとして残してはならない。

---

# 24. Current vs Target Labeling

current architectureを説明するsectionは、

```text
Current / Before / Baseline
```

と明確にlabelする。

target architectureは、

```text
Approved Target / After / ENH-E4
```

と明確にlabelする。

同一paragraph内でcurrentとtargetを混在させない。

---

# 25. Mandatory Correction E — Persistent StageExecution

Approved target:

```text
all canonical workflows
→ persistent StageExecution
```

CausalだけStageExecutionを持たないtarget designが残っていないか確認する。

Current architecture説明として、

```text
Causal currently has in-memory stages
```

と記述するのは許容する。

Targetではpersistent StageExecutionへ収束する。

---

# 26. Mandatory Correction F — Lineage Authority

snapshot内のLineage記述を検索する。

Approved target:

```text
typed structural relation
    = authority

generic persisted lineage
    = approved generic-only relations

closure/export
    = projection / reader, not authority
```

同一semantic structural relationを、

```text
typed relation
+
generic LineageEdge
```

の双方がindependent target authorityとして持つ記述を残してはならない。

---

# 27. Generic-only Lineage

Phase 04 / Phase 06からgeneric-only relation inventoryを確認する。

approved generic-only relationについてはgeneric persisted representationを維持してよい。

typedで再構築可能なstructural relationと混同しない。

---

# 28. Mandatory Correction G — Legacy Boundary

Approved target:

```text
canonical Product runtime
does not depend on retired legacy runtime
```

しかし、

```text
ariadne.causal
ariadne.preprocessing
ariadne.shared
```

等のshared scientific capabilityはlegacy orchestrationと同一視しない。

snapshot内に、

> legacy removal means deleting shared scientific implementation

相当の記述があれば修正する。

---

# 29. Mandatory Correction H — Migration / Bootstrap

Approved target:

```text
empty DB
→ alembic_product.ini
→ product_migrations
→ target Product schema
```

root legacy migration chainはcanonical Product bootstrap requirementではない。

snapshot内に、

```text
Product bootstrap requires root alembic.ini
legacy migrations are prerequisite
```

相当のtarget normative clauseが残っていないか確認する。

historical migration説明は残してよい。

---

# 30. Mandatory Correction I — Standalone CLI

Approved target:

```text
standalone low-level scientific CLI
```

はcanonical persistent Execution lifecycle外のutility boundary。

ただし、

```text
auditable/user-visible Product analysis CLI
```

を提供する場合はcanonical Execution lifecycleへsubmitする。

low-level CLIが第二のpersistent architectureとしてtarget設計に記載されていないことを確認する。

---

# 31. Mandatory Semantic Conflict Scan

既知3件だけを直して終了してはならない。

6 snapshotについてapproved targetとのsemantic contradiction scanを行う。

最低限検索theme:

```text
Execution authority
FamilyExecution
Causal Execution
GenericExecutor
claim
lease
retry
rerun
revise
cancel
StageExecution
Result
Artifact
object_key
LineageEdge
lineage
legacy
migration
alembic
CLI
```

---

# 32. Conflict Classification

検出した候補を以下へ分類する。

```text
TRUE_NORMATIVE_CONFLICT
CURRENT_STATE_DESCRIPTION
HISTORICAL_PROVENANCE
COMPATIBLE_BASELINE
NON_NORMATIVE_REFERENCE
UNKNOWN
```

`TRUE_NORMATIVE_CONFLICT` のみ修正対象。

---

# 33. Historical Preservation Rule

旧ENH-E3設計を完全に消去する必要はない。

必要なら、

```text
Baseline / Before ENH-E4
```

sectionとして歴史的状態を残せる。

ただし、historical textを現行MUSTとして読める状態にはしない。

---

# 34. Standard Enhance Documents

以下5文書は、snapshot修正に伴ってtraceabilityや説明が不整合になる場合のみ最小修正する。

```text
01_Enhance構想・要件改定計画.md
02_Enhance構想承認記録.md
03_要件定義書改定.md
04_設計書改定.md
05_要件・設計整合性およびトレーサビリティ確認.md
```

特に:

```text
05_要件・設計整合性およびトレーサビリティ確認.md
```

は必ず再監査する。

---

# 35. Mandatory Update to Document 05

05へ最低限以下を記録する。

```text
08b consistency correction performed
```

および、

* Snapshot precedence normalized
* GenericExecutor responsibility conflict removed
* Result semantic/cardinality contract normalized
* additional normative conflict scan completed
* no approved ADR changed

を記録する。

---

# 36. G01 AC Re-evaluation

修正後、以下を再評価する。

## E4-G01-AC-001

全familyについて、

```text
family/type
identity
state transition
```

target contractが一意。

## E4-G01-AC-002

```text
ExecutionResult
StageResult
Artifact ownership
logical cardinality
```

が一意。

## E4-G01-AC-003

```text
typed structural lineage
generic-only lineage
```

が一意。

## E4-G01-AC-004

old Causal/Family authorityをtarget authorityとして再定義していない。

## E4-G01-AC-005

```text
REQ = 35
INV = 16
CON = 10
```

missing = 0。

---

# 37. G01 Status Rule

本Task Agentは、

```text
G01 PASS
```

を宣言してはならない。

使用可能status:

```text
READY_FOR_G01_INDEPENDENT_REVIEW
INCOMPLETE
BLOCKED
```

G01 PASS/FAILは次の独立レビューで判定する。

---

# 38. Allowed Writes

変更可能:

```text
00_enhance_background/
01_Enhance構想・要件改定計画.md

02_Enhance構想承認記録.md

03_要件定義書改定.md

04_設計書改定.md

05_要件・設計整合性およびトレーサビリティ確認.md
```

および:

```text
00_enhance_background/
Revised_requirements_definition_documents/
00_プロダクトコンセプトメモ.md

10_要件定義.md

21_論理データ設計.md

22_プロダクト基本設計.md

23_API・インターフェース設計.md

30_詳細設計.md
```

および:

```text
40_operator_prompts/
architecture_review/
08b_enhance_background_consistency_correction_result.md
```

---

# 39. Preferred Write Scope

11 materialized documents全てを変更する義務はない。

**実際に必要なfileだけ修正する。**

変更不要なfileは変更しない。

期待するのは、

```text
smallest sufficient diff
```

である。

---

# 40. Read-only Files

変更禁止:

```text
docs/wiki/requirement_definition/**
```

```text
40_operator_prompts/architecture_review/
01_* ... 08_*
```

08 resultも変更しない。

```text
40_operator_prompts/database_reinitialization/**
```

```text
00_enhance_background/README.md
```

およびsource/test/migration/config/deployment/dependency files。

---

# 41. Prohibited Operations

禁止:

```text
pytest
alembic upgrade
database reset
docker compose
application startup
worker startup
frontend startup
curl
network access
```

production codeをimportして実行してはならない。

static read-only investigationのみ。

---

# 42. Allowed Tools

read-only:

```text
git
git grep
rg
grep
find
sed
cat
awk
diff
static text parsing
Python for text-only static analysis
```

---

# 43. No Architecture Expansion

以下を本Taskで決めてはならない。

* exact new table names
* exact new class names
* library choice
* framework change
* exact SQL schema
* exact migration sequence beyond approved bootstrap contract
* new API endpoint
* new frontend behavior
* scientific algorithm changes

approved semantic contractの文書整合性修正だけを行う。

---

# 44. No Requirement Renumbering

以下IDを変更・renumberしてはならない。

```text
E4-REQ-001 ... E4-REQ-035
E4-ADR-001 ... E4-ADR-012
E4-INV-001 ... E4-INV-016
E4-CON-001 ... E4-CON-010
HD-001 ... HD-007
E4-G01 ... E4-G08
```

---

# 45. No Silent Resolution of Unknowns

approved evidenceで判断不能な問題を推測で埋めない。

分類:

```text
BLOCKS_G01_CONTRACT
DEFERRED_TO_IMPLEMENTATION_GATE
DEFERRED_TO_G08_VERIFICATION
OUT_OF_SCOPE
```

ただし単なるimplementation naming/detailをG01 blockerにしない。

---

# 46. Required Consistency Matrix

08b resultに以下を作る。

| Theme | Conflicting File/Clause | Classification | Approved Authority | Correction |
| ----- | ----------------------- | -------------- | ------------------ | ---------- |

最低限theme:

```text
Snapshot status
GenericExecutor
Execution authority
StageExecution
Result cardinality
Artifact ownership
Lineage authority
Legacy boundary
Migration/bootstrap
CLI boundary
```

conflictがないthemeも、

```text
NO_CONFLICT
```

として記録する。

---

# 47. Required Changed-clause Inventory

実際に修正したnormative clauseについて:

| File | Section | Before Meaning | After Meaning | ADR/REQ |
| ---- | ------- | -------------- | ------------- | ------- |

全文引用は不要。

semantic meaningを短く記録する。

---

# 48. Coverage Re-audit

修正後にidentifier coverageを再確認する。

Expected:

```text
E4-REQ unique IDs = 35
E4-ADR unique IDs = 12
E4-INV unique IDs = 16
E4-CON unique IDs = 10
HD unique IDs = 7
Gate unique IDs = 8
```

missing IDsがあれば完了扱いにしない。

---

# 49. Placeholder Re-audit

allowed materialized documentsについて:

```text
{{...}}
```

が0件であることを再確認する。

---

# 50. Normative Conflict Re-scan

修正後、もう一度全文検索し、

> ENH-E4 approved targetと反対の意味を持つcurrent normative clause

が残っていないか確認する。

単純なkeyword 0件を要求しているわけではない。

Current-state/historical referenceは存在してよい。

判定基準は、

```text
Can a reasonable implementer read this clause
as an active target requirement?
```

である。

YESならconflict。

---

# 51. GenericExecutor Final Check

明示的に回答する。

```text
Does any materialized target document still assign
canonical lifecycle/claim/retry/persistence ownership
to GenericExecutor?
```

Expected:

```text
NO
```

---

# 52. Execution Authority Final Check

明示的に回答する。

```text
Does any materialized target document define
Causal and Family as separate authoritative
persistent Product lifecycle models?
```

Expected:

```text
NO
```

---

# 53. Result Contract Final Check

明示的に回答する。

```text
Is it possible to determine from the target snapshot:

- what an ExecutionResult is
- what a StageResult is
- which parent each belongs to
- whether stage ownership is required
- how Artifact ownership relates to Result
```

Expected:

```text
YES
```

不足ならG01 readyではない。

---

# 54. Lineage Final Check

明示的に回答する。

```text
Can the same structural semantic relation
remain independently authoritative in both
typed relationship and generic lineage edge?
```

Expected target answer:

```text
NO
```

---

# 55. Migration Final Check

明示的に回答する。

```text
Does the target snapshot require root legacy migrations
for canonical Product bootstrap?
```

Expected:

```text
NO
```

---

# 56. CLI Final Check

明示的に回答する。

```text
Does the low-level standalone Product scientific CLI
constitute an alternative persistent lifecycle authority?
```

Expected:

```text
NO
```

---

# 57. Diff Quality Review

修正後:

```text
git diff --stat
```

およびallowed filesのdiffを読む。

以下を確認する。

```text
unrelated rewrite = 0
style-only mass edit = 0
baseline unrelated requirement changes = 0
architecture decision changes = 0
```

---

# 58. Existing Working Tree Changes

開始前の:

```text
git status --short
```

を記録する。

既存変更を、

* reset
* restore
* stash
* delete

してはならない。

自分が作った変更と区別する。

---

# 59. Required Result

生成:

```text
40_operator_prompts/
architecture_review/
08b_enhance_background_consistency_correction_result.md
```

構造:

```markdown
# 08b Enhance Background Consistency Correction Result

## 1. Metadata

- Prompt:
- Repository:
- Branch:
- HEAD:
- Working tree before:
- Started at:
- Finished at:
- Status:

## 2. Inputs Reviewed

## 3. Correction Scope

### Files inspected

### Files changed

### Files unchanged

## 4. Snapshot Status / Precedence Correction

| File | Before | After | Status |
|---|---|---|---|

## 5. Normative Conflict Matrix

| Theme | File / Clause | Classification | Approved Authority | Correction |
|---|---|---|---|---|

## 6. Changed Normative Clauses

| File | Section | Before Meaning | After Meaning | ADR / REQ |
|---|---|---|---|---|

## 7. GenericExecutor Responsibility Audit

### Conflicts Found

### Corrections

### Final Authority

Explicit answer:

`GenericExecutor owns canonical lifecycle/claim/persistence: YES / NO`

Expected: `NO`

## 8. Execution Authority Audit

Explicit answer:

`Separate Causal/Family persistent target authorities remain: YES / NO`

Expected: `NO`

## 9. StageExecution Audit

## 10. Result / Artifact Logical Contract

### ExecutionResult

### StageResult

### Artifact ownership

### Cardinality

### Remaining implementation-only details

## 11. Lineage Authority Audit

### Typed structural

### Generic-only

### Closure/export

### Remaining dual authority

## 12. Legacy Boundary Audit

## 13. Migration / Bootstrap Audit

## 14. CLI Boundary Audit

## 15. Standard Document Consistency

### 01

### 02

### 03

### 04

### 05

## 16. Identifier Coverage

- REQ: <count>/35
- ADR: <count>/12
- INV: <count>/16
- CON: <count>/10
- HD: <count>/7
- Gates: <count>/8

Missing:
<...>

## 17. Placeholder Audit

- occurrences:
- status:

## 18. G01 Contract Re-evaluation

| AC | Evidence | Status |
|---|---|---|

Cover:
- E4-G01-AC-001
- E4-G01-AC-002
- E4-G01-AC-003
- E4-G01-AC-004
- E4-G01-AC-005

Allowed status:
- READY_FOR_INDEPENDENT_REVIEW
- INCOMPLETE
- BLOCKED

Do not use PASS.

## 19. Remaining Unknowns

| ID | Classification | G01 Blocking? | Handling |
|---|---|---|---|

## 20. Diff Quality Audit

- unrelated rewrite:
- architecture decision change:
- baseline unrelated semantic change:
- unauthorized files changed:

## 21. Final Semantic Checks

1. GenericExecutor lifecycle owner?
2. Separate Product Execution authorities?
3. Persistent StageExecution all canonical workflows?
4. ExecutionResult contract explicit?
5. StageResult contract explicit?
6. Artifact semantic ownership explicit?
7. Structural lineage has one authority?
8. Shared scientific capability preserved?
9. Product bootstrap independent of legacy migrations?
10. Low-level CLI outside persistent authority?
11. Current and Target clearly separated?
12. Any active normative ENH-E3 clause contradicts ENH-E4?

Use:
- YES
- NO
- UNKNOWN

Explain when necessary.

## 22. Decision

One of:

- READY_FOR_G01_INDEPENDENT_REVIEW
- INCOMPLETE_CORRECTION
- BLOCKED_G01_CONTRACT
- MATERIALIZATION_INCONSISTENCY
- BLOCKED_WRONG_BRANCH

## 23. Completion Status

One of:

- COMPLETED
- COMPLETED_WITH_NONBLOCKING_UNKNOWNS
- BLOCKED
```

---

# 60. Completion Criteria

`COMPLETED` とするには全て必要。

### C1

6 snapshotのstatus / precedenceがENH-E4 target snapshotとして明確。

### C2

GenericExecutor responsibility conflict = 0。

### C3

separate Causal/Family target lifecycle authority conflict = 0。

### C4

persistent StageExecution target contractが一貫。

### C5

ExecutionResult / StageResult logical ownershipが明示。

### C6

G01に必要なResult/Artifact cardinalityが明示。

### C7

Artifact semantic ownershipとphysical storageが分離。

### C8

structural lineage dual authority conflict = 0。

### C9

legacy runtimeとshared scientific capabilityが分離。

### C10

Product bootstrapがlegacy root migration非依存。

### C11

low-level CLIがalternative persistent lifecycleではない。

### C12

REQ 35/35。

### C13

ADR 12/12。

### C14

INV 16/16。

### C15

CON 10/10。

### C16

HD 7/7。

### C17

Gate 8/8。

### C18

placeholder 0。

### C19

unrelated baseline semantic change = 0。

### C20

approved Architecture Decision change = 0。

### C21

unauthorized file changes = 0。

---

# 61. G01 Readiness Rule

全Completion Criteriaを満たし、G01 AC-001〜005の全てについて文書契約が判定可能なら:

```text
READY_FOR_G01_INDEPENDENT_REVIEW
```

とする。

Agent自身はG01をPASSしてはならない。

---

# 62. Final Self-check

最後に:

```text
git status --short
```

```text
git diff --stat
```

および変更したmaterialized documentsのdiffを確認する。

08b result自身も確認する。

既存working tree変更を変更・reset・restore・stashしてはならない。

---

# 63. Agent Final Response

chat responseは簡潔に以下を報告する。

```text
08b_enhance_background_consistency_correction_result.md
を生成しました。

Status: <...>

Files changed: <count>

Normative conflicts corrected: <count>

REQ coverage: <count>/35
ADR coverage: <count>/12
INV coverage: <count>/16
CON coverage: <count>/10
HD coverage: <count>/7
Gate coverage: <count>/8

G01 contract readiness:
<READY_FOR_G01_INDEPENDENT_REVIEW | INCOMPLETE | BLOCKED>

Production source/test/migration/configurationは変更していません。
```

---

# 64. Stop Condition

以下のいずれかで停止する。

1. consistency correctionと08b result生成完了
2. branch mismatch
3. approved contractだけではG01 logical contractを確定できない
4. baselineとapproved architectureに新たな重大矛盾を発見した

停止後、以下へ進んではならない。

* G01 PASS判定
* G02 implementation
* production code変更
* migration変更
* Coding Agent実行
* Test Agent実行

次作業は独立レビューによるG01判定後、別promptとして指示される。
