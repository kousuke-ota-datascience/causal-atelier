# 08c Lineage Allowlist Contract Correction — Operator Prompt

## 1. Task

`ENH-E4 eliminate dual execution` の G01 contract reviewで唯一blockingとなった、

```text
E4-G01-AC-003
typed structural / generic-only lineage allowlist is explicitly defined
```

を満たすため、Phase 08bでmaterializeされた正式ENH-E4 target snapshotへ、**approved lineage authority classificationを具体的なrelation-level contractとしてmaterializeする**。

本TaskはArchitecture Decisionの追加・変更ではない。

Phase 06で承認済みのLineage authorityを、G01が独立判定できる粒度まで文書化するだけである。

---

# 2. Current G01 Status

commit `1906758` に対する独立レビュー結果:

```text
E4-G01-AC-001 PASS
E4-G01-AC-002 PASS
E4-G01-AC-003 FAIL
E4-G01-AC-004 PASS
E4-G01-AC-005 PASS
```

G01 overall:

```text
FAIL_FIX_IN_GATE
```

唯一のblocking item:

```text
E4-G01-AC-003
```

本TaskではAC-001 / 002 / 004 / 005の契約を変更してはならない。

---

# 3. Failure Reason

Phase 06ではrelation-levelのauthority classificationが定義されている。

しかし正式snapshotでは、

```text
typedで再構築可能ならtyped authority
typedで表現できなければgeneric-only
```

というpolicyのみがmaterializeされており、

> 具体的にどのsemantic relationがtypedで、どのrelationがgeneric-onlyなのか

を独立Reviewerがsnapshotだけから判定できない。

また、baseline `LineageEdge.relation_type` に広いrelation名が残っているため、

```text
USED_INPUT
GENERATED
DERIVED_FROM
REVISED_FROM
...
```

等がTargetでもgeneric persisted authorityとして許されるように読める余地がある。

これを解消する。

---

# 4. Repository / Branch

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
08c_lineage_allowlist_contract_correction_prompt.md
```

Result:

```text
40_operator_prompts/
architecture_review/
08c_lineage_allowlist_contract_correction_result.md
```

---

# 5. Required Inputs

必ず以下を読む。

## Architecture evidence

```text
40_operator_prompts/architecture_review/
04_lineage_responsibility_inventory_result.md

06_target_architecture_decision_record_result.md

07_gate_decomposition_result.md

08_enhance_background_materialization_result.md

08b_enhance_background_consistency_correction_result.md
```

## Formal target snapshots

```text
00_enhance_background/
Revised_requirements_definition_documents/
21_論理データ設計.md

30_詳細設計.md
```

## Traceability

```text
00_enhance_background/
05_要件・設計整合性およびトレーサビリティ確認.md
```

必要に応じて:

```text
03_要件定義書改定.md
04_設計書改定.md
```

をread-onlyで参照してよい。

---

# 6. Fixed Architecture Decision

Lineage architectureは再議論しない。

Approved target:

```text
typed structural relations
    = authoritative typed persistent relationship

generic-only relations
    = authoritative generic persisted lineage edge

closure / traversal graph
    = projection / reader

export synthetic relation
    = projection / representation

same semantic structural relation
    ≠ independent typed authority + generic authority
```

関連ADR / invariant / requirementはPhase 06を正本として確認する。

---

# 7. Core Invariant

本Task後、以下が文書上明確でなければならない。

```text
For every semantic lineage relation:

exactly one authoritative representation exists.
```

特に、

```text
typed structural relation
```

をgeneric persisted edgeへ独立dual-writeしてはならない。

---

# 8. Mandatory Relation Classification

Phase 04 / Phase 06 evidenceから、少なくとも以下のsemantic relationを分類する。

## Typed structural authority candidates

最低限確認:

```text
Execution → Result

Result → Artifact

Dataset / View → Execution input

Result → Execution input

Result → GraphVersion

Artifact → DatasetVersion

Execution → previous/base/revision Execution
```

実際のrelation direction / semantic nameはPhase 06の記述に合わせる。

---

## Generic-only authority candidates

最低限確認:

```text
Artifact → Artifact
stage / processing derivation

Result → Result
SUMMARIZES

DOCUMENTS

EVIDENCE_FOR / SUPPORTED_BY
where no approved typed structural relation exists

user-authored/manual semantic links
```

relation名はPhase 04 / Phase 06 evidenceに存在するものを使用する。

新しいrelationを創作してはならない。

---

# 9. Evidence-driven Classification Rule

各relationについて以下の順で分類する。

```text
1. Phase 06 approved Lineage Relation Target Classification
2. Phase 04 current representation / reconstructability evidence
3. approved requirement / invariant
```

current generic writerが存在するだけで、

```text
GENERIC_ONLY
```

と判断してはならない。

typed FKから再構築でき、Phase 06でtyped authorityとされたrelationは、

```text
TYPED_STRUCTURAL
```

とする。

---

# 10. Required Authority Values

正式snapshotでは最低限以下の分類語を一貫して使う。

```text
TYPED_STRUCTURAL
GENERIC_ONLY
PROJECTION_ONLY
```

必要なら、

```text
OUT_OF_SCOPE
```

を使用してよい。

別の語を使う場合も意味を完全に定義する。

---

# 11. Required Allowlist Table

`21_論理データ設計.md` に、正式なtarget contractとしてrelation-level tableを追加または既存sectionを補正する。

最低限columns:

| Semantic Relation | Source | Target | Authority | Generic Edge Allowed? | Notes |
| ----------------- | ------ | ------ | --------- | --------------------- | ----- |

例示ではなく、approved evidenceに基づく実relationを記載する。

---

# 12. Generic Edge Allowed Semantics

`Generic Edge Allowed?` は最低限次の意味を持つ。

## `NO`

そのsemantic relationはtyped authority。

generic persisted edgeへ同じsemantic relationを独立authoritative writeしてはならない。

## `YES — AUTHORITY`

そのrelationはgeneric-onlyであり、generic persisted edgeがauthority。

## `YES — PROJECTION ONLY`

Phase 06で明示的に認められている場合のみ使用可能。

原則、closure/exportはedge authorityではなくprojectionなので、generic persisted writeとは区別する。

---

# 13. Structural Relation Rule

以下のようなstructural relationについては、approved evidenceに従いtyped authorityとする。

例:

```text
Execution owns Result
Result owns Artifact
Execution consumes Dataset/View/Result
Execution revision/base relation
```

同じ意味を、

```text
USED_INPUT
GENERATED
DERIVED_FROM
REVISED_FROM
```

等のgeneric edge名でも独立authorityとして書いてよい、というtarget contractにしてはならない。

---

# 14. Generic-only Relation Rule

typed relationshipでは表現されないsemantic relationはgeneric-onlyとして許可してよい。

例:

```text
SUMMARIZES
DOCUMENTS
MOTIVATED
SUPPORTED_BY
EVIDENCE_FOR
manual/user-authored relation
artifact-to-artifact stage derivation
```

ただし実際にPhase 04 / 06 evidenceにあるrelationだけを採用する。

---

# 15. Baseline LineageEdge Relation Types

`21_論理データ設計.md` のbaseline sectionに、

```text
USED_INPUT
GENERATED
DERIVED_FROM
REVISED_FROM
SUPPORTED_BY
MOTIVATED
SELECTED
REJECTED
...
```

等が列挙されている場合、そのsectionを精査する。

以下のどちらかで正規化する。

### Option A

historical/current baseline representationとして明確にlabelする。

### Option B

Target contractとして許可されるgeneric-only relationだけへ絞る。

どちらを選ぶかは既存document structureに対するsmallest sufficient diffで決める。

---

# 16. Prohibited Ambiguity

以下の状態を残してはならない。

```text
LineageEdge.relation_type = arbitrary enum
```

とだけ記述され、

> structural relationもgeneric edgeへ書いてよいのか

が不明。

また、

```text
generic edge may represent any relation
```

相当のTarget contractも禁止。

---

# 17. 30 Detailed Design Update

`30_詳細設計.md` では、generic lineage write pathがrelation allowlistを検証するcontractを具体化する。

最低限:

```text
if relation classified TYPED_STRUCTURAL:
    generic authoritative write is rejected / not performed

if relation classified GENERIC_ONLY:
    generic lineage persistence is allowed

closure/export:
    consume authoritative sources
    do not become authority
```

実装コードやexception classは決めなくてよい。

---

# 18. Writer Responsibility Contract

Target contractとして、

```text
structural relation writer
```

と

```text
generic-only lineage writer
```

を分離する。

具体的service/class名を新規固定する必要はない。

ただし、

> family workflow serviceがstructural relationをgeneric edgeへdual-writeする

ことをTarget responsibilityとして残してはならない。

---

# 19. Closure Contract

Closure / traversalは、

```text
typed structural authoritative relations
+
generic-only authoritative relations
```

を統合して読むprojectionである。

closureが、

```text
third authority
```

になってはならない。

明示する。

---

# 20. Export Contract

Exportでsynthetic/derived relation representationを生成してもよい。

ただし、

```text
export representation
≠ persistence authority
```

を明記する。

可能ならrelation source classification:

```text
TYPED_STRUCTURAL
GENERIC_ONLY
```

を識別可能にするというapproved targetを保持する。

---

# 21. Conflict Resolution

current codeのclosureではexplicit edgeがderived edgeをoverwriteする動作が確認されている。

Target contractではこれをauthority conflict resolution mechanismとして採用してはならない。

理由:

```text
authority must be decided before projection
```

である。

同じsemantic relationがtyped + generic双方にauthoritativeに存在しないtargetを正文とする。

---

# 22. Manual Links

manual/user-authored lineageについては、Phase 04 / 06 evidenceに従いgeneric-only authorityとして扱う。

ただしendpoint/project/type validation等は後続G06 implementation scopeであり、本Taskで実装設計を拡張しない。

G01ではsemantic classificationを確定する。

---

# 23. Relation Naming Rule

current relation enum名とtarget semantic relationが完全に1対1でない場合、

```text
semantic relation
```

をauthority判定の正文とする。

例えば、

```text
GENERATED
```

というgeneric nameが複数semantic relationを曖昧に含むなら、その名前だけでallowlistを作らない。

Source/Target semanticを含めて定義する。

---

# 24. Direction Rule

Relation tableではdirectionを明確にする。

例:

```text
Execution → Result
Result → Artifact
```

のように記載する。

Phase 04 / 06と逆方向にしない。

不明なdirectionを推測しない。

---

# 25. Approved Evidence Must Be Sufficient

本Taskは新規Architecture調査Phaseではない。

Phase 04 / 06にrelation classificationが存在するため、それを正式snapshotへmaterializeする。

もしPhase 06内でも矛盾があり、relation単位のauthorityを一意に確定できない場合だけ:

```text
BLOCKED_G01_LINEAGE_CONTRACT
```

とする。

---

# 26. Allowed Writes

原則変更対象:

```text
00_enhance_background/
Revised_requirements_definition_documents/
21_論理データ設計.md

00_enhance_background/
Revised_requirements_definition_documents/
30_詳細設計.md

00_enhance_background/
05_要件・設計整合性およびトレーサビリティ確認.md
```

必要な場合のみ:

```text
00_enhance_background/
04_設計書改定.md
```

結果:

```text
40_operator_prompts/
architecture_review/
08c_lineage_allowlist_contract_correction_result.md
```

---

# 27. Preferred Write Scope

変更は最小限にする。

期待:

```text
21 = relation allowlist / authority contract
30 = enforcement semantics
05 = traceability / AC-003 evidence update
```

他のsnapshotを理由なく変更しない。

---

# 28. Read-only

以下を変更しない。

```text
docs/wiki/requirement_definition/**
```

```text
40_operator_prompts/architecture_review/
01_* ... 08b_*
```

```text
source code
tests
migrations
configuration
deployment
dependency files
```

---

# 29. No Architecture Change

禁止:

* E4-ADR変更
* E4-REQ変更
* E4-INV変更
* E4-CON変更
* HD変更
* Gate分割変更
* new lineage architecture proposal
* generic graph DB導入
* event sourcing導入
* new lineage framework導入

---

# 30. No Implementation

禁止:

```text
pytest
alembic
database operation
container
application startup
worker
HTTP request
network access
```

static documentation correctionのみ。

---

# 31. AC-003 Exact Re-evaluation

修正後、`E4-G01-AC-003` を明示的に再評価する。

判定質問:

### Q1

Formal target snapshotにrelation-level allowlistが存在するか。

Expected:

```text
YES
```

### Q2

各listed structural relationのauthorityがtypedであると判定できるか。

Expected:

```text
YES
```

### Q3

各listed generic-only relationのauthorityがgeneric persisted lineageであると判定できるか。

Expected:

```text
YES
```

### Q4

structural relationをgeneric edgeへ独立dual-writeしてよいと読めるactive target clauseが残っているか。

Expected:

```text
NO
```

### Q5

closure/exportがauthorityと読めるtarget clauseがあるか。

Expected:

```text
NO
```

---

# 32. Regression Check for Other G01 ACs

AC-003修正によって、既にPASSしている以下を壊してはならない。

```text
E4-G01-AC-001
E4-G01-AC-002
E4-G01-AC-004
E4-G01-AC-005
```

08c resultでre-checkする。

---

# 33. Coverage Must Remain

Expected:

```text
REQ = 35/35
ADR = 12/12
INV = 16/16
CON = 10/10
HD = 7/7
Gate = 8/8
placeholder = 0
```

---

# 34. Required Result

生成:

```text
40_operator_prompts/
architecture_review/
08c_lineage_allowlist_contract_correction_result.md
```

構造:

```markdown
# 08c Lineage Allowlist Contract Correction Result

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

## 3. Failure Being Corrected

- Gate:
- AC:
- Prior status:
- Root cause:

## 4. Approved Lineage Authority Baseline

### Typed structural

### Generic-only

### Projection-only

## 5. Formal Relation Allowlist

| Semantic Relation | Source | Target | Authority | Generic Edge Allowed | Evidence |
|---|---|---|---|---|---|

## 6. Baseline Relation-type Reconciliation

| Existing Relation Type | Target Interpretation | Authority | Action in Snapshot |
|---|---|---|---|

## 7. Files Changed

| File | Change | Why |
|---|---|---|

## 8. 21 Logical Data Contract

### Authority table

### Cardinality / direction

### Generic edge restrictions

## 9. 30 Detailed Design Contract

### Structural writer rule

### Generic-only writer rule

### Closure

### Export

## 10. Traceability Update

### E4-G01-AC-003

### Related ADR

### Related INV

### Related REQ

## 11. AC-003 Re-evaluation

1. relation-level allowlist present?
2. structural authority explicit?
3. generic-only authority explicit?
4. structural dual-write allowed?
5. closure/export authority?

Use YES / NO / UNKNOWN.

## 12. Regression Re-check

| AC | Status | Evidence |
|---|---|---|

Cover:
- E4-G01-AC-001
- E4-G01-AC-002
- E4-G01-AC-004
- E4-G01-AC-005

Do not declare G01 PASS.

## 13. Identifier / Placeholder Audit

- REQ:
- ADR:
- INV:
- CON:
- HD:
- Gate:
- Placeholder:

## 14. Diff Quality Audit

- unrelated semantic change:
- architecture change:
- unauthorized files:
- mass rewrite:

## 15. Remaining Unknowns

## 16. Decision

One of:

- READY_FOR_G01_INDEPENDENT_REVIEW
- INCOMPLETE_LINEAGE_CONTRACT
- BLOCKED_G01_LINEAGE_CONTRACT
- BLOCKED_WRONG_BRANCH

## 17. Completion Status

One of:

- COMPLETED
- COMPLETED_WITH_NONBLOCKING_UNKNOWNS
- BLOCKED
```

---

# 35. Completion Criteria

`COMPLETED` には全て必要。

### C1

Formal relation-level allowlist exists.

### C2

Typed structural relations are explicitly classified.

### C3

Generic-only relations are explicitly classified.

### C4

Generic Edge Allowed status is explicit.

### C5

Structural independent generic dual-write is prohibited.

### C6

Closure is projection-only.

### C7

Export is not persistence authority.

### C8

Baseline broad relation-type list no longer creates target ambiguity.

### C9

21 and 30 are mutually consistent.

### C10

05 traceability points AC-003 to the formal contract.

### C11

AC-001 / 002 / 004 / 005 remain unchanged semantically.

### C12

REQ 35/35.

### C13

ADR 12/12.

### C14

INV 16/16.

### C15

CON 10/10.

### C16

HD 7/7.

### C17

Gate 8/8.

### C18

placeholder 0.

### C19

no unrelated semantic change.

### C20

no unauthorized file change.

---

# 36. Final Self-check

最後に:

```text
git status --short
```

```text
git diff --stat
```

変更したallowed filesについてdiffを読む。

特に、

```text
21_論理データ設計.md
30_詳細設計.md
05_要件・設計整合性およびトレーサビリティ確認.md
```

のsemantic diffを確認する。

---

# 37. Agent Final Response

chat responseは簡潔に:

```text
08c_lineage_allowlist_contract_correction_result.md
を生成しました。

Status: <...>

Files changed: <count>
Typed structural relations classified: <count>
Generic-only relations classified: <count>

E4-G01-AC-003 readiness:
<READY_FOR_INDEPENDENT_REVIEW | INCOMPLETE | BLOCKED>

REQ coverage: <count>/35
ADR coverage: <count>/12
INV coverage: <count>/16
CON coverage: <count>/10

Production source/test/migration/configurationは変更していません。
```

---

# 38. Stop Condition

以下のいずれかで停止する。

1. AC-003 lineage contract correction完了
2. branch mismatch
3. Phase 06 evidenceからrelation authorityを一意に確定不能
4. approved architectureとの新たな重大矛盾を発見

停止後、以下へ進んではならない。

* G01 PASS宣言
* G02 implementation
* production source変更
* migration変更
* Coding Agent実行

次作業は独立Reviewerによるcommit固定のG01再判定とする。
