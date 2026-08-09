# ENH-E4 E4-G06 P00 Work Package Plan

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Branch: `refactor/ariadne_mvp_e4`
- Gate: `E4-G06`
- Gate Name: Lineage authority consolidation
- Trial: `01`
- Document Type: Gate-local Coding Contract Control Document / Work Package Plan
- File:
  `10_enhance_instruction/G06/06_G06_P00_work_package_plan.md`
- Fixed G06 Baseline:
  `aae491519472f87bfbda88069eb1e65a858a9fcc`
- Previous Gate Fixed Implementation/Test Candidate:
  `ad3e3e124ee47f9cbaa2470b25263b7289795262`
- Product Migration Head:
  `20260809_product_0010`
- Current Transition Debt:
  `E4-TD-004 OPEN -> G06`

---

# 1. Purpose

本書は、E4-G06 `Lineage authority consolidation` を複数のAgent execution Work Packageへ分割し、以下をGate開始前に固定するためのcontrol documentである。

```text
1. G06 Gate contract
2. lineage authority model
3. G06 Acceptance Criteria
4. Work Package decomposition
5. Package dependency
6. Package entry / exit condition
7. instruction / implementation report / test report の配置規則
8. checkpoint commit規則
9. Trial state transition規則
10. Independent Test Agent handoff規則
11. G06 explicit out-of-scope
```

本書自体はproduction implementation instructionではない。

```text
P00
    = G06 execution map / control document

P01-P07
    = Coding Agent execution packages
```

P00でproduction source、test、migrationを変更してはならない。

---

# 2. Why G06 Uses Work Packages

E4-G06は一つのGateであり、Gate自体を分割してはならない。

一方、ENH-E4 G05の実行経験から、Gate全体を一つのCoding Agent instructionとして実行すると、以下の問題が起こりやすい。

```text
- execution scopeが大きくなりすぎる
- agent途中停止時のfailure localizationが困難
- architecture再推論が増える
- checkpointが粗くなる
- regression originの特定が難しくなる
- report correctionとimplementation correctionが混在する
```

したがってG06では、

```text
Gate scope
    !=
Agent execution scope
```

を明示的に採用する。

目的は、

```text
1回のAgent runで最大量を実装すること
```

ではなく、

```text
正しく閉じたGateあたりの総コストを最小化すること
```

である。

---

# 3. Source of Truth / Precedence

G06実装時のsemantic precedenceは以下とする。

```text
1. Passed Gate-local contract + final Gate Decision
2. ENH-E4 Target Architecture ADR / Invariant / Requirement / Constraint
3. G06 Gate-local 06/07 contract
4. Verified current source / Product migration
5. Current Architecture Control Sheet
6. This P00 execution plan
```

本書は上位architecture contractを変更する文書ではない。

本書と上位contractが矛盾した場合、

```text
本書を修正する。
```

上位contractをP00へ合わせて変更してはならない。

主要参照文書:

```text
00_ENH-E4_Current_Architecture_Control_Sheet.md

40_operator_prompts/architecture_review/
06_target_architecture_decision_record_result.md

40_operator_prompts/architecture_review/
07_gate_decomposition_result.md

40_operator_prompts/architecture_review/
08c_lineage_allowlist_contract_correction_result.md
```

---

# 4. Fixed G06 Entry State

G06開始時点のverified architecture:

```text
E4-G01 PASS
E4-G02 PASS
E4-G03 PASS
E4-G04 PASS
E4-G05 PASS

Current Gate:
E4-G06 NEXT

G06 baseline:
aae491519472f87bfbda88069eb1e65a858a9fcc

G05 fixed Implementation/Test Candidate:
ad3e3e124ee47f9cbaa2470b25263b7289795262

Product migration head:
20260809_product_0010

TD-001:
CLOSED

TD-002:
CLOSED

TD-003:
CLOSED

TD-004:
OPEN
Owner / exit Gate:
G06
```

G06ではG02-G05で確立したauthorityを再設計してはならない。

---

# 5. Protected Passed-Gate Architecture

G06全Packageで以下をprotected architectureとして扱う。

## 5.1 Execution

```text
one canonical Product Execution identity

family:
    CAUSAL
    EXPLORATORY
    PREDICTIVE

one shared lifecycle
one canonical claim / lease authority

retry:
    same Execution ID

rerun:
    new Execution ID
    typed source/base relation

revise:
    new Execution ID
    typed source/base relation
```

## 5.2 StageExecution

```text
persistent canonical StageExecution
    = Product stage authority

GenericExecutor
    != Product persistence authority
    != claim authority
    != retry authority
    != lineage authority
```

## 5.3 Result / Artifact

```text
canonical Result
    = Result ownership authority

canonical Artifact metadata
    = Artifact metadata authority

ArtifactStorePort
    = physical object storage boundary

artifact_id
    != object_key
```

## 5.4 Product family convergence

```text
Causal
Exploratory
Predictive

all submit through:
canonical Product Execution architecture
```

禁止:

```text
new FamilyExecution authority
new FamilyStageExecution authority
new FamilyResult authority
new FamilyArtifact authority
canonical failure -> legacy authority fallback
```

---

# 6. G06 Gate Objective

E4-G06の目的は、同一semantic lineage relationについて複数representationが独立authorityとして競合しない状態を成立させることである。

Target:

```text
Lineage Authority
│
├── TYPED_STRUCTURAL
│    └── canonical typed state
│         = sole structural authority
│
├── GENERIC_ONLY
│    └── generic persisted lineage
│         = sole authority for non-reconstructable semantic relation
│
└── PROJECTION_ONLY
     └── closure / traversal / export
          = derived representation only
          != authority
```

E4-G06 exit時には、

```text
one semantic lineage relation
    ->
one authority
```

が成立していなければならない。

---

# 7. Formal Lineage Authority Classes

## 7.1 TYPED_STRUCTURAL

typed canonical stateから再構成できるrelation。

代表例:

```text
Execution -> Result
    ownership / GENERATED

Result -> Artifact
    ownership / GENERATED

DatasetVersion / AnalysisView -> Execution
    input / USED_INPUT

Result -> Execution
    input / USED_INPUT

Result -> GraphVersion
    structural production relation

Artifact -> DatasetVersion
    structural derivation relation

Execution -> Execution
    rerun / revise / base relation
```

これらについて、

```text
generic authoritative persistence
```

を行ってはならない。

---

## 7.2 GENERIC_ONLY

typed canonical equivalentを持たず、generic relationそのものを保存しなければsemantic informationを失うrelation。

代表例:

```text
Artifact -> Artifact
    stage/process DERIVED_FROM

Result -> Result
    SUMMARIZES

Result / Artifact -> related Product resource
    DOCUMENTS
    EVIDENCE_FOR
    SUPPORTED_BY
    where no typed equivalent exists

approved user-authored/manual semantic relation
```

これらは、

```text
generic persisted lineage
    = authority
```

として許可する。

---

## 7.3 PROJECTION_ONLY

以下はauthorityではない。

```text
closure
traversal
synthetic lineage
export lineage representation
```

これらは、

```text
TYPED_STRUCTURAL
+
GENERIC_ONLY
```

を読み取って生成するprojectionである。

---

## 7.4 OUT_OF_SCOPE

```text
legacy ArtifactLineage
legacy family-specific lineage authority retirement
```

はG06で広範削除しない。

最終legacy runtime/source retirement境界はG07で扱う。

---

# 8. Relation Name Is Not Authority

以下のrelation vocabularyが存在しても、

```text
USED_INPUT
GENERATED
DERIVED_FROM
REVISED_FROM
SUPPORTED_BY
EVIDENCE_FOR
MOTIVATED
...
```

relation name単独ではauthority classを決定しない。

authority classificationは必ず、

```text
source semantic type
+
relation semantic
+
target semantic type
```

で行う。

例:

```text
Execution --DERIVED_FROM--> Execution
    = TYPED_STRUCTURAL

Artifact --DERIVED_FROM--> Artifact
    = GENERIC_ONLY
```

したがって、

```text
DERIVED_FROM is allowed
```

というuniversal generic allowlistは禁止する。

---

# 9. G06 Acceptance Criteria

G06は以下5 ACを全て満たす必要がある。

## E4-G06-AC-001

```text
structural relationは
typed authorityから再構築される
```

Verification class:

```text
lineage source audit
```

---

## E4-G06-AC-002

```text
generic-only relationについて
semantic allowlist
endpoint validation
project validation
が存在する
```

Verification class:

```text
persistence / service test
```

---

## E4-G06-AC-003

```text
structural generic dual-writeが
final Product pathに存在しない
```

Verification class:

```text
negative writer audit
```

---

## E4-G06-AC-004

```text
closure / exportは
authority source classを保持し、
自身をauthorityとしてwriteしない
```

Verification class:

```text
API / export test
```

---

## E4-G06-AC-005

```text
retry / rerun / reviseで
typed / generic-only lineageが
target semanticsを維持する
```

Verification class:

```text
mutation lineage regression
```

---

# 10. Execution Hierarchy

G06では以下のtransaction hierarchyを使用する。

```text
Gate
└── Trial
    ├── Work Package
    ├── Implementation Completion
    └── Independent Test
        └── Test Item
```

意味:

```text
Gate
    architecture acceptance unit

Trial
    one implementation -> independent verification transaction

Work Package
    Coding Agent execution unit inside one Trial

Test Item
    Independent Test verification unit inside one Trial
```

重要:

```text
Work Package
    != Gate

Work Package
    != Trial

Coding Agent self-check failure
    != Trial FAIL
```

---

# 11. Trial Rule

Current Trial:

```text
01
```

以下ではTrialを増やさない。

```text
P01 implementation failure
P02 implementation failure
P03 implementation failure
P04 test failure during coding
P05 report correction
P06 regression correction
P07 completion report correction
Coding Agent interruption
self-check failure
package restart
```

Trialを `02` にする唯一の条件:

```text
Independent Test Agent
    ->
E4-G06 Trial 01
    ->
formal FAIL
```

`BLOCKED` はFAILと同義に扱わない。

---

# 12. G06 Work Package Overview

G06 Trial01 Coding executionを以下へ分割する。

```text
P00  Gate contract / work-package freeze
  ↓
P01  Lineage authority policy / allowlist foundation
  ↓
P02  Structural writer cutover
  ↓
P03  Generic-only authority convergence
  ↓
P04  Typed lineage read reconstruction
  ↓
P05  Closure / export projection convergence
  ↓
P06  Mutation lineage + negative authority audit
  ↓
P07  Gate-wide regression / completion / test handoff
  ↓
Independent Test Agent
```

---

# 13. G06-P00 — Work Package Plan

File:

```text
06_G06_P00_work_package_plan.md
```

Purpose:

```text
Gate contract
Work Package boundary
dependency
output structure
checkpoint rules
Trial rules
AC traceability
```

Production change:

```text
NONE
```

Test change:

```text
NONE
```

Migration:

```text
NONE
```

Exit:

```text
P01-P07 execution structureがoperatorにより採用され、
P01 instruction作成へ移行可能
```

---

# 14. G06-P01 — Authority Policy / Allowlist Foundation

Planned instruction:

```text
06_G06_P01_authority_policy_instruction.md
```

Purpose:

```text
semantic source/relation/target
    ->
authority class
```

をcentral Product policyとして確立する。

Primary targets:

```text
TYPED_STRUCTURAL classification
GENERIC_ONLY classification
unknown/unapproved relation rejection
generic writer admission guard
```

Must prove:

```text
same relation name
+
different source/target type
    ->
different authority classification可能
```

Primary AC:

```text
AC-002
```

Secondary support:

```text
AC-003
```

Explicitly out of scope:

```text
workflow structural writer cutover
closure/export redesign
typed read reconstruction
mutation audit
```

Exit:

```text
central lineage authority policy established
generic-only admission semantics verified
checkpoint commit created
package checkpoint report created
```

---

# 15. G06-P02 — Structural Writer Cutover

Planned instruction:

```text
06_G06_P02_structural_writer_cutover_instruction.md
```

Purpose:

```text
TYPED_STRUCTURAL relationの
generic authoritative new-writeを停止する
```

Scope:

```text
Causal
Exploratory
Predictive

canonical Product write paths
```

Required end state:

```text
structural generic NEW WRITE = 0
```

P02はgeneric-only authorityを削除してはならない。

Primary AC:

```text
AC-003
```

Secondary support:

```text
AC-001
```

Exit:

```text
structural duplicate writers removed/disabled
focused negative persistence tests PASS
checkpoint commit created
package checkpoint report created
```

---

# 16. G06-P03 — Generic-only Authority Convergence

Planned instruction:

```text
06_G06_P03_generic_only_convergence_instruction.md
```

Purpose:

```text
P02で不要なgeneric writerを止めた後、
必要なgeneric-only authorityを正式に保全する
```

Scope:

```text
approved GENERIC_ONLY relations

endpoint existence
same-project validation
cross-project rejection
unknown semantic rejection
duplicate/idempotency contract
```

Required end state:

```text
GENERIC_ONLY
    -> persist allowed

TYPED_STRUCTURAL
    -> generic persistence rejected

UNKNOWN
    -> rejected
```

Primary AC:

```text
AC-002
```

Exit:

```text
generic-only persistence semantics verified
checkpoint commit created
package checkpoint report created
```

---

# 17. G06-P04 — Typed Lineage Read Reconstruction

Planned instruction:

```text
06_G06_P04_typed_read_reconstruction_instruction.md
```

Purpose:

```text
structural generic writerを停止しても
Product lineage readが情報欠落しない状態を作る
```

Target:

```text
canonical typed fields / ownership
    ->
structural lineage projection
```

Required proof pattern:

```text
generic structural row:
    absent

lineage read:
    structural relation visible
```

Primary AC:

```text
AC-001
```

Critical invariant:

```text
read correctnessのために
structural generic writeを復活させてはならない
```

Exit:

```text
typed reconstruction verified
checkpoint commit created
package checkpoint report created
```

---

# 18. G06-P05 — Closure / Export Projection Convergence

Planned instruction:

```text
06_G06_P05_projection_convergence_instruction.md
```

Purpose:

```text
closure
traversal
export
```

をlineage authorityから明確に分離する。

Target projection model:

```text
TYPED_STRUCTURAL authority
        +
GENERIC_ONLY authority
        |
        v
closure / traversal / export projection
```

Required:

```text
source class/provenance preserved
projection does not persist itself as authority
synthetic/projected relation distinguished from persisted authority
```

Primary AC:

```text
AC-004
```

Explicitly forbidden:

```text
closureを新authority tableへ昇格
export representationをsource of truth化
graph subsystem broad redesign
```

Exit:

```text
closure/export projection semantics verified
checkpoint commit created
package checkpoint report created
```

---

# 19. G06-P06 — Mutation Lineage / Negative Authority Audit

Planned instruction:

```text
06_G06_P06_mutation_negative_audit_instruction.md
```

Purpose:

```text
retry
rerun
revise
```

後もlineage authority invariantが維持されることを証明する。

Expected:

```text
retry:
    same Execution ID
    structural generic relationを新規authoritative writeしない

rerun:
    new Execution ID
    typed source/base relation

revise:
    new Execution ID
    typed base/revision relation
```

さらにstatic/runtime negative auditで、

```text
structural generic writer resurrection
```

がないことを確認する。

Primary AC:

```text
AC-005
AC-003
```

Exit:

```text
mutation lineage PASS
negative authority audit PASS
checkpoint commit created
package checkpoint report created
```

---

# 20. G06-P07 — Gate-wide Completion / Test Handoff

Planned instruction:

```text
06_G06_P07_gate_completion_instruction.md
```

P07は新しいarchitectureを大きく追加するpackageではない。

Purpose:

```text
P01-P06の成果を
E4-G06 Trial01 implementation candidateとして
一つにfreezeする
```

Required:

```text
all focused G06 tests
required real PostgreSQL verification
G02-G05 protected regression
three-family relevant regression
negative authority audit
mutation regression
report-format audit
fixed Implementation/Test Candidate
Implementation Completion Report
READY_FOR_TEST
```

P07 output:

```text
20_implementation_reports/G06/Trial01/
E4-G06_01_implementation_completion_report.md
```

P07については、

```text
E4-G06_01_P07_implementation_checkpoint_report.md
```

を作成しない。

理由:

```text
P07 transaction result
    =
Trial01 Implementation Completion Report
```

であり、独立Package checkpoint reportとの内容重複が大きいため。

Coding Agent final state:

```text
READY_FOR_TEST
```

禁止:

```text
E4-G06 PASS
TD-004 CLOSED
```

---

# 21. Work Package Dependency Graph

Execution order:

```text
P00
 │
 ▼
P01
Authority Policy
 │
 ▼
P02
Structural Writer Cutover
 │
 ├───────────────┐
 ▼               ▼
P03             P04
Generic-only    Typed Read
Authority       Reconstruction
 │               │
 └───────┬───────┘
         ▼
        P05
Closure / Export Projection
         │
         ▼
        P06
Mutation / Negative Audit
         │
         ▼
        P07
Gate-wide Completion
         │
         ▼
Independent Test Agent
```

Agent executionは原則直列とする。

P03/P04は論理上部分並列化可能だが、checkpoint/failure localizationのため直列executionを推奨する。

---

# 22. Acceptance Criteria Traceability

```text
E4-G06-AC-001
structural relationはtyped authorityから再構築
    <- P02
    <- P04
    <- P07

E4-G06-AC-002
generic-only allowlist + endpoint/project validation
    <- P01
    <- P03
    <- P07

E4-G06-AC-003
structural generic dual-writeなし
    <- P01
    <- P02
    <- P06
    <- P07

E4-G06-AC-004
closure/export source-class preservation
projection-only
    <- P05
    <- P07

E4-G06-AC-005
retry/rerun/revise lineage semantics
    <- P06
    <- P07
```

PxxとIndependent Test Itemは1:1対応を要求しない。

```text
Pxx
    = implementation decomposition

Test Item
    = acceptance verification decomposition
```

である。

---

# 23. Instruction Output Directory Contract

G06 Coding Contract family:

```text
10_enhance_instruction/G06/
├── 06_G06_P00_work_package_plan.md
├── 06_G06_P01_authority_policy_instruction.md
├── 06_G06_P02_structural_writer_cutover_instruction.md
├── 06_G06_P03_generic_only_convergence_instruction.md
├── 06_G06_P04_typed_read_reconstruction_instruction.md
├── 06_G06_P05_projection_convergence_instruction.md
├── 06_G06_P06_mutation_negative_audit_instruction.md
├── 06_G06_P07_gate_completion_instruction.md
└── 07_Ariadne_ENH-E4_G06_テスト指示書.md
```

意味:

```text
06_
    = Coding Contract family

P00-P07
    = Coding Contract internal Work Package sequence

07_
    = Independent Verification Contract
```

`Pxx`をファイル先頭sequenceへ昇格して、

```text
00_G06_P00...
01_G06_P01...
```

としてはならない。

既存ENH-E4 instruction numberingとの整合性を優先する。

---

# 24. Why 10_ Has No Trial Directory

`10_enhance_instruction` はtransaction evidenceではなく契約である。

したがって:

```text
10_enhance_instruction/G06/Trial01/
```

は作らない。

Trial01 contractは、

```text
06_G06_P00-P07
07_Ariadne_ENH-E4_G06_テスト指示書
```

としてfreezeする。

Trial01が正式FAILした場合でも、06/07をTrial02用にコピーして書き換えない。

代わりに:

```text
08_E4-G06_02_Remediation_Instruction.md
```

を追加する。

Gate contractそのものの変更が必要な場合のみ:

```text
09_E4-G06_Gate_Contract_Amendment.md
```

を使用する。

---

# 25. Implementation Report Output Directory Contract

Implementation evidenceはTrial transactionに所属する。

したがって:

```text
20_implementation_reports/
└── G06/
    └── Trial01/
        ├── packages/
        │   ├── E4-G06_01_P01_implementation_checkpoint_report.md
        │   ├── E4-G06_01_P02_implementation_checkpoint_report.md
        │   ├── E4-G06_01_P03_implementation_checkpoint_report.md
        │   ├── E4-G06_01_P04_implementation_checkpoint_report.md
        │   ├── E4-G06_01_P05_implementation_checkpoint_report.md
        │   └── E4-G06_01_P06_implementation_checkpoint_report.md
        │
        └── E4-G06_01_implementation_completion_report.md
```

Work Package reportは、

```text
Gate
└── Trial
    └── Work Package
```

のtransaction recordである。

---

# 26. Package Checkpoint Report Contract

P01-P06の各Packageは、完了時にcheckpoint reportを作成する。

Required fields:

```text
Gate ID
Trial ID
Package ID

Entry SHA
Implementation checkpoint SHA

Package purpose
Scope
Explicit out-of-scope

Changed production files
Changed test files
Migration

Implementation facts
Interpretation
Unknown / Unconfirmed

Exact test commands
Exit codes
passed
failed
skipped

PostgreSQL evidence
Evidence directory

Relevant regressions

Protected Gate impact

Transition Debt impact

Known residual work

Next Package prerequisites

git status --short
```

Package checkpoint reportはPackage完了後、

```text
原則immutable
```

として扱う。

後続Packageで過去Package reportの内容を都合よく書き換えない。

誤記訂正が必要な場合は、訂正内容がGit historyで明確に追跡できるようにする。

---

# 27. No Mutable Gate-wide Implementation Ledger

G06では、

```text
E4-G06_implementation_report_detail.md
```

のような単一mutable cumulative ledgerを必須成果物としない。

理由:

```text
P01終了時点
P02終了時点
P03終了時点
...
```

のtransaction boundaryを独立artifactとして追跡できる方が、failure localizationと監査性に優れるため。

G06における実績集約は、

```text
Package Checkpoint Reports
+
Git history
+
Trial Implementation Completion Report
```

で行う。

この設計は既存templateを盲目的に踏襲するためではなく、G05で得たWork Package運用知見をG06へ適用するためのGate-local decisionである。

後に有効性が確認された場合、workflow templateの次版へbackportする候補とする。

---

# 28. Independent Test Report Output Directory Contract

Independent Test evidenceもTrial transactionに所属する。

```text
30_test_report/
└── G06/
    └── Trial01/
        ├── E4-G06_01_001_<test_item>.md
        ├── E4-G06_01_002_<test_item>.md
        ├── E4-G06_01_003_<test_item>.md
        ├── ...
        └── E4-G06_01_999_gate_decision.md
```

Test Itemのexact decomposition / filenameは、

```text
07_Ariadne_ENH-E4_G06_テスト指示書.md
```

でfreezeする。

P00ではTest Item番号を先取りして固定しない。

---

# 29. Trial 02+ Directory Rule

Trial01がIndependent Test Agentによって正式FAILした場合:

```text
20_implementation_reports/G06/
├── Trial01/
└── Trial02/
```

```text
30_test_report/G06/
├── Trial01/
└── Trial02/
```

を作る。

Trial01 directoryは書き換えない。

Trial02ではP01-P07を機械的に再実行する必要はない。

Trial02 remediationは、

```text
08_E4-G06_02_Remediation_Instruction.md
```

で新たに定義する。

remediation Work Package ID:

```text
R01
R02
R03
...
```

とする。

例:

```text
20_implementation_reports/G06/Trial02/packages/
E4-G06_02_R01_implementation_checkpoint_report.md
E4-G06_02_R02_implementation_checkpoint_report.md
```

`P01-P07` はTrial01 Gate decompositionを示すため、Trial02 remediation packageへ再利用しない。

---

# 30. Completion Report Contract

Trial01 Coding Agent implementation完了時:

```text
20_implementation_reports/G06/Trial01/
E4-G06_01_implementation_completion_report.md
```

を作成する。

このreportが、

```text
one Gate / one Trial implementation transaction
```

をまとめる。

最低限:

```text
Fixed Implementation/Test Candidate SHA

Package completion table:
    P01
    P02
    P03
    P04
    P05
    P06
    P07

all exact verification commands
exit codes
passed / failed / skipped

PostgreSQL evidence

mandatory regressions

migration head

changed files

Transition Debt state

Facts
Interpretation
Unknown / Unconfirmed

READY_FOR_TEST
```

を含む。

Completion Reportは、

```text
Gate PASS authority
```

ではない。

---

# 31. Gate Decision Authority

Gate判定authority:

```text
30_test_report/G06/Trial01/
E4-G06_01_999_gate_decision.md
```

のみ。

Allowed decision:

```text
PASS
FAIL
BLOCKED
```

Coding Agent:

```text
READY_FOR_TEST
```

Independent Test Agent:

```text
PASS / FAIL / BLOCKED
```

を決定する。

---

# 32. Transition Debt Rule

Current debt:

```text
E4-TD-004
    OPEN
    Exit Gate: G06
```

P01-P06では閉じない。

P07 Coding completion時も、

```text
TD-004 CLOSED
```

と宣言してはならない。

P07時点では最大でも:

```text
TD-004:
CLOSURE_CANDIDATE
pending Independent Test Agent verification
```

とする。

正式CLOSEDは:

```text
E4-G06 Independent Test Agent
    ->
PASS
```

後。

---

# 33. Checkpoint Commit Strategy

各Packageを原則以下で閉じる。

```text
Package start
    ↓
focused implementation
    ↓
focused tests
    ↓
required real PostgreSQL verification
    ↓
relevant regression
    ↓
implementation checkpoint commit
    ↓
package checkpoint report
    ↓
report commit
    ↓
next Package
```

重要:

```text
implementation checkpoint SHA
    !=
report-only commit SHA
```

次Packageのproduction baselineとして使用するのは、

```text
latest verified implementation checkpoint
```

である。

report-only commitをtested implementation SHAとして扱ってはならない。

---

# 34. Standard PostgreSQL Verification Rule

real PostgreSQL acceptance evidenceは原則:

```text
scripts/test/run_product_postgres_tests.sh \
  <pytest-path-or-node> \
  [pytest-options]
```

を使用する。

standard acceptance evidenceとして以下を使用しない。

```text
manual docker run
manual container networking
manual DSN
manual psql setup
manual Alembic setup
manual external pytest
```

runner evidenceには最低限:

```text
exact command
exit code
passed
failed
skipped
evidence directory
tested implementation SHA/state
```

を残す。

---

# 35. Test Partition Rule

G05で確認されたglobal state contaminationを考慮し、関連testを必ず一つの巨大pytest invocationへ統合する必要はない。

必要に応じて:

```text
clean semantic partition
    ->
standard PostgreSQL runner
```

を複数回使用する。

ただし:

```text
isolated PASS
    ->
fixture defect確定
```

とはしない。

combined failureが存在する場合、可能な範囲でcontamination originを調査する。

root causeを再現できない場合:

```text
NOT_REPRODUCED
ROOT_CAUSE_UNCONFIRMED
```

を使用できる。

---

# 36. Report Format Is an Acceptance Condition

Package Checkpoint Report、Implementation Completion Report、Test Item、999 Gate Decisionは、それぞれ定義されたrequired fieldを省略しない。

禁止:

```text
same as previous
same command
上記と同じ
related tests
```

値が存在しない場合:

```text
N/A
NONE
NOT_RUN
UNKNOWN
```

を使用する。

必須evidence:

```text
exact copy-pastable command
exit code
passed / failed / skipped
tested SHA/state
evidence directory
expected
actual
reproduction procedure
Facts
Interpretation
Unknown / Unconfirmed
```

---

# 37. Package Completion Is Not Gate Completion

Package complete:

```text
focused implementation complete
focused verification PASS
checkpoint commit created
checkpoint report created
```

Gate implementation complete:

```text
P01-P07 complete
Gate-wide verification complete
fixed candidate created
Implementation Completion Report complete
READY_FOR_TEST
```

Gate PASS:

```text
Independent Test Agent
    ->
999 Gate Decision
    ->
PASS
```

これらを混同してはならない。

---

# 38. G06 Explicitly Out of Scope

G06で以下へ越境しない。

```text
broad legacy source deletion
legacy API/worker全面削除
final CLI retirement
root migration history cleanup
Product-only final clean bootstrap
G08 final architecture audit
scientific algorithm redesign
Execution architecture redesign
StageExecution architecture redesign
Result architecture redesign
Artifact ownership architecture redesign
```

これらはG07/G08境界で扱う。

---

# 39. Legacy Adapter Rule

G06中も以下は残り得る。

```text
family-specific DTO
family-specific URL
bounded read projection
compatibility read adapter
```

それ自体をauthority復活とみなさない。

禁止されるのは:

```text
new-write authority
claim authority
lifecycle authority
Result/Artifact authority
lineage structural authority duplication
canonical failure -> legacy fallback
```

である。

---

# 40. No Test-fitting

testを通す目的でauthority semanticsを歪めてはならない。

禁止例:

```text
specific test resource typeだけallow
test target ID優先
hidden relation special-case
relation-name-only universal allowlist
structural generic writerをreader compatibilityのため復活
retryを特別queue priority化
```

常に:

```text
authoritative contract
    ->
implementation
    ->
test
```

の順序を維持する。

---

# 41. Stop / Escalation Conditions

以下の場合はAgentがarchitectureを推測して補完しない。

```text
formal lineage contractsが
同一semantic relationについて矛盾する

G02-G05 protected semanticsを壊さなければ
G06 packageを実装できない

source/relation/target authority classificationを
formal contractから一意に決定できない

current baselineに
packageと競合する未説明production変更がある
```

その場合:

```text
PACKAGE_BLOCKED
```

として:

```text
Facts
Contradiction
Affected contract
Why local implementation cannot resolve it
Required decision
```

を報告する。

単なるbug、test failure、fixture failure、implementation volumeは`DESIGN_BLOCKED`理由ではない。

---

# 42. Work Package Status Vocabulary

Package:

```text
NOT_STARTED
IN_PROGRESS
COMPLETE
BLOCKED
```

Coding Agent Gate status:

```text
E4-G06 NOT_COMPLETE
READY_FOR_TEST
```

Independent Test:

```text
PASS
FAIL
BLOCKED
```

Package Agentが、

```text
E4-G06 PASS
```

を宣言してはならない。

---

# 43. Planned Artifact Tree — Trial01 PASS Case

Trial01が一回でPASSする場合、最終的な主要artifact treeは以下。

```text
10_enhance_instruction/G06/
├── 06_G06_P00_work_package_plan.md
├── 06_G06_P01_authority_policy_instruction.md
├── 06_G06_P02_structural_writer_cutover_instruction.md
├── 06_G06_P03_generic_only_convergence_instruction.md
├── 06_G06_P04_typed_read_reconstruction_instruction.md
├── 06_G06_P05_projection_convergence_instruction.md
├── 06_G06_P06_mutation_negative_audit_instruction.md
├── 06_G06_P07_gate_completion_instruction.md
└── 07_Ariadne_ENH-E4_G06_テスト指示書.md


20_implementation_reports/G06/
└── Trial01/
    ├── packages/
    │   ├── E4-G06_01_P01_implementation_checkpoint_report.md
    │   ├── E4-G06_01_P02_implementation_checkpoint_report.md
    │   ├── E4-G06_01_P03_implementation_checkpoint_report.md
    │   ├── E4-G06_01_P04_implementation_checkpoint_report.md
    │   ├── E4-G06_01_P05_implementation_checkpoint_report.md
    │   └── E4-G06_01_P06_implementation_checkpoint_report.md
    │
    └── E4-G06_01_implementation_completion_report.md


30_test_report/G06/
└── Trial01/
    ├── E4-G06_01_001_<test_item>.md
    ├── E4-G06_01_002_<test_item>.md
    ├── ...
    └── E4-G06_01_999_gate_decision.md
```

---

# 44. Planned Artifact Tree — Trial01 FAIL Case

Trial01がIndependent TestでFAILした場合:

```text
10_enhance_instruction/G06/
├── 06_G06_P00_work_package_plan.md
├── 06_G06_P01_...
├── ...
├── 06_G06_P07_...
├── 07_Ariadne_ENH-E4_G06_テスト指示書.md
└── 08_E4-G06_02_Remediation_Instruction.md


20_implementation_reports/G06/
├── Trial01/
│   ├── packages/
│   │   └── ...
│   └── E4-G06_01_implementation_completion_report.md
│
└── Trial02/
    ├── packages/
    │   ├── E4-G06_02_R01_implementation_checkpoint_report.md
    │   └── ...
    └── E4-G06_02_implementation_completion_report.md


30_test_report/G06/
├── Trial01/
│   ├── ...
│   └── E4-G06_01_999_gate_decision.md
│
└── Trial02/
    ├── ...
    └── E4-G06_02_999_gate_decision.md
```

Trial01 evidenceをTrial02用に上書きしない。

---

# 45. G06 Exit Condition

E4-G06がPASSできるのは、Independent Test Agentが最低限以下を確認した場合のみ。

```text
1. structural relation is reconstructed from typed authority

2. generic-only relation has explicit semantic admission policy

3. structural generic dual-write does not remain on final Product path

4. closure/export is projection only and preserves authority source class

5. retry/rerun/revise preserve target lineage semantics

6. G02-G05 protected architecture has not regressed

7. TD-004 exit criterion is satisfied

8. required evidence/report format is complete
```

G06 PASS後:

```text
E4-TD-004:
CLOSED

Current next Gate:
E4-G07
```

Control Sheet promotionはIndependent Test PASS後にoperatorが行う。

Coding AgentはControl Sheetをpromotionしない。

---

# 46. P00 Exit Condition

P00 COMPLETE条件:

```text
1. G06 authority model fixed
2. AC-001..005 fixed
3. P01-P07 decomposition fixed
4. Package dependency fixed
5. 10/20/30 output structure fixed
6. checkpoint/report rule fixed
7. Trial transition rule fixed
8. remediation package naming fixed
9. out-of-scope fixed
10. operator approves P01 start
```

P00終了時:

```text
E4-G06:
NOT_COMPLETE

Trial:
01

TD-004:
OPEN

Production change:
NONE

Migration:
NONE
```

---

# 47. Immediate Next Action

P00承認後、次に作成する文書:

```text
10_enhance_instruction/G06/
06_G06_P01_authority_policy_instruction.md
```

P01は、

```text
Lineage authority policy
+
semantic allowlist
+
generic-only admission guard
```

だけに限定する。

P02以降のscopeへ越境しない。
