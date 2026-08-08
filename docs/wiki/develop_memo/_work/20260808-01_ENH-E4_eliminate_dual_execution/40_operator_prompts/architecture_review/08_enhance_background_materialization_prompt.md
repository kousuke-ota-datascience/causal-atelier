# 08 Enhance Background Materialization — Operator Prompt

## 1. Task

`ENH-E4 eliminate dual execution` について、Architecture Review Phase 01〜07、database reinitialization evidence、および人間承認済みArchitecture Decisionを正規入力として使用し、現在skeleton状態である

```text
00_enhance_background/
```

配下のEnhance背景・承認・要件改定・設計改定・traceability文書、および

```text
Revised_requirements_definition_documents/
```

配下の要件・設計snapshotを**具体値へmaterializeする**。

本Taskは、

```text
Architecture Review evidence
        ↓
Human-approved Target Architecture
        ↓
formal Enhance background
        ↓
revised requirement/design snapshot
        ↓
G01 canonical contract review input
```

をRepository上で成立させるためのdocumentation materializationである。

本Taskではproduction code、test code、migration、runtime configuration、database schemaを変更しない。

---

# 2. Purpose

本Task終了後、Repositoryだけを読めば最低限以下を復元できる状態にする。

1. なぜENH-E4を実施するのか
2. Current Architectureの何が問題なのか
3. どのArchitecture Decisionが人間承認されたか
4. どのRequirementが追加・変更されたか
5. Target Architectureは何か
6. Execution / Stage / Result / Artifact / Lineageのauthorityはどうなるか
7. legacy runtimeとshared scientific capabilityをどう区別するか
8. migration/bootstrap policyは何か
9. E4-REQ / E4-ADR / E4-INV / E4-CONがどう対応するか
10. G01〜G08へどう接続されるか

ただしCoding Agent / Test Agentにこれらの背景文書を直接再探索させる運用にはしない。

後続の実行契約は、

```text
10_enhance_instruction/
06_...実装指示書.md
07_...テスト指示書.md
```

へ別途materializeする。

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

本Taskのoperator prompt:

```text
40_operator_prompts/
architecture_review/
08_enhance_background_materialization_prompt.md
```

Result出力先:

```text
40_operator_prompts/
architecture_review/
08_enhance_background_materialization_result.md
```

---

# 4. Required Inputs

必ず以下を読むこと。

## 4.1 Architecture Review

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

40_operator_prompts/architecture_review/
07_gate_decomposition_result.md
```

---

## 4.2 Database Reinitialization Evidence

最低限:

```text
40_operator_prompts/database_reinitialization/
99_completion_summary_decision_record.md
```

および、そのDecision Recordがclean Product bootstrapの根拠として参照しているresult。

---

## 4.3 Enhance Background Schema

```text
00_enhance_background/README.md
```

---

## 4.4 Current Requirement / Design Baseline

以下をsnapshot生成のbaselineとして読むこと。

```text
docs/wiki/requirement_definition/
00_プロダクトコンセプトメモ.md

docs/wiki/requirement_definition/
10_要件定義.md

docs/wiki/requirement_definition/
21_論理データ設計.md

docs/wiki/requirement_definition/
22_プロダクト基本設計.md

docs/wiki/requirement_definition/
23_API・インターフェース設計.md

docs/wiki/requirement_definition/
30_詳細設計.md
```

これらbaseline文書は本Taskでは変更しない。

---

# 5. Human Approval Baseline

以下はproject ownerによって承認済みである。

Phase 07 Human Approval RecordをRepository上のapproval evidenceとして使用する。

## HD-001

```text
new unified canonical Product Execution aggregate
```

Causal / Exploratory / Predictiveを一つのpersistent Execution authorityへ統合する。

## HD-002

```text
persistent StageExecution for all canonical workflows
```

## HD-003

```text
ExecutionResult / StageResult semantic levels
under one Result ownership contract
```

## HD-004

```text
typed structural lineage
+
generic-only lineage
```

## HD-005

```text
external legacy compatibility is out of ENH-E4 scope
```

shared scientific capabilityはlegacy runtimeと区別して保持する。

## HD-006

```text
Product-only clean rebuild
no historical application-data migration
```

canonical bootstrap:

```text
alembic_product.ini
→ product_migrations
```

## HD-007

```text
standalone Product scientific CLI remains
a low-level utility boundary
```

persistent auditabilityを要求するProduct analysisだけcanonical Execution lifecycleへsubmitする。

---

# 6. Approval Metadata Rule

Enhance承認日は、

```text
2026-08-09 JST
```

として記録する。

Repository evidenceに個人名が存在しない限り、個人名を推測してはならない。

その場合:

```text
Approved by: Project owner / human approver
```

とする。

正確なclock timeがRepository evidenceから確認できない場合:

```text
Approved at: 2026-08-09 JST
Exact clock time: NOT_REPOSITORY_EVIDENCED
```

相当の形で記録する。

---

# 7. Fixed Architecture Baseline

Phase 06の以下をapproved baselineとして扱う。

```text
E4-ADR-001 ... E4-ADR-012
E4-INV-001 ... E4-INV-016
E4-REQ-001 ... E4-REQ-035
E4-CON-001 ... E4-CON-010
```

Phase 07の以下もfixed implementation decompositionとして扱う。

```text
E4-G01 ... E4-G08
E4-Gxx-AC-xxx
E4-TD-001 ... E4-TD-006
```

Target Architectureを再設計してはならない。

---

# 8. Phase 07 Transition Debt Normalization

Phase 07内に非semanticな記述不整合があるため、materialization時に以下の解釈を使用する。

Phase 07 Transition Debt Registerをauthorityとする。

```text
E4-TD-001
Actual introduction: G02
Exit: G05

E4-TD-002
Actual introduction: G03
Exit: G05

E4-TD-003
Actual introduction: G04
Exit: G05

E4-TD-004
Actual introduction: G05
Exit: G06

E4-TD-005
Actual introduction: G06
Exit: G07

E4-TD-006
Actual introduction: G07
Exit: G08
```

G01詳細内の、

```text
Transition Debt Introduced:
E4-TD-001〜003
```

は、

```text
G01で契約上定義・予告されるTransition Debt
```

という意味として扱う。

G01はdocumentation/contract Gateであり、production data/schema/runtimeを変更しないため、TD-001〜003のruntime上の実導入Gateとは扱わない。

Phase 07 result自体は変更しない。

このnormalizationを、

```text
05_要件・設計整合性およびトレーサビリティ確認.md
```

および08 resultに記録する。

---

# 9. Phase 06 Typo Normalization

Phase 06 `E4-ADR-003` にあるMarkdown typo、

```text
one globally unique Product `execution_id);
```

は、

```text
one globally unique Product `execution_id`;
```

として解釈する。

Phase 06 result自体は変更しない。

semantic design changeとして扱わない。

---

# 10. Allowed Writes

本Taskで変更してよいのは以下のみ。

## 10.1 Standard Enhance Background Documents

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

---

## 10.2 Revised Snapshot

```text
00_enhance_background/
Revised_requirements_definition_documents/
00_プロダクトコンセプトメモ.md

00_enhance_background/
Revised_requirements_definition_documents/
10_要件定義.md

00_enhance_background/
Revised_requirements_definition_documents/
21_論理データ設計.md

00_enhance_background/
Revised_requirements_definition_documents/
22_プロダクト基本設計.md

00_enhance_background/
Revised_requirements_definition_documents/
23_API・インターフェース設計.md

00_enhance_background/
Revised_requirements_definition_documents/
30_詳細設計.md
```

---

## 10.3 Result

```text
40_operator_prompts/
architecture_review/
08_enhance_background_materialization_result.md
```

---

# 11. Files That Must Not Be Changed

以下はread-only。

```text
docs/wiki/requirement_definition/**
```

```text
40_operator_prompts/architecture_review/
01_* ... 07_*
```

```text
40_operator_prompts/database_reinitialization/**
```

```text
00_enhance_background/README.md
```

```text
00_enhance_background/
Revised_requirements_definition_documents/
README.md
```

さらに、

* source code
* tests
* migrations
* configuration
* dependency files
* deployment files

を変更してはならない。

---

# 12. Materialization Principle

本Taskは新しいArchitectureを考案するTaskではない。

文書内容は次の優先順位から生成する。

```text
1. Human-approved HD-001..007
2. Phase 06 approved Target Architecture
3. Phase 07 Gate decomposition
4. Phase 01..05 observed evidence
5. Database reinitialization evidence
6. Existing requirement/design baseline
```

矛盾がある場合は勝手に補正せず、

```text
MATERIALIZATION_INCONSISTENCY
```

として08 resultに記録する。

ただしSection 8 / 9で明示したnormalizationは既知の非semantic修正として適用する。

---

# 13. No New Architecture Decisions

禁止:

* 新しいExecution architectureの提案
* ADRの追加
* ADRの変更
* Stage persistence方針変更
* Result semantic level変更
* Artifact ownership変更
* Lineage authority変更
* legacy policy変更
* migration policy変更
* CLI policy変更

approved baselineを文章化するだけとする。

---

# 14. Standard Document Template Preservation

`01〜05` は既存templateの必須headingを維持する。

必要であればsubsection / tableを追加してよい。

既存必須headingを削除してはならない。

最終成果物には、

```text
{{...}}
```

形式のmeta-syntax placeholderを残してはならない。

該当情報が本当にない場合は、

```text
NONE
N/A
UNKNOWN
NOT_REPOSITORY_EVIDENCED
```

を使用する。

---

# 15. Document 01 — Enhance構想・要件改定計画

対象:

```text
00_enhance_background/
01_Enhance構想・要件改定計画.md
```

最低限以下をmaterializeする。

## 15.1 Basic Information

```text
Project: Ariadne / causal-atelier
Enhancement ID: ENH-E4
Date: 2026-08-09
```

Author / PlannerはRepository evidenceに個人名がなければrole-basedにする。

---

## 15.2 Background

Phase 01〜05のevidenceから、

* active Product runtime
* multiple Product Execution lifecycles
* Result / Artifact dual ownership
* derived + persisted lineage duality
* legacy runtime dependency boundary

を簡潔に整理する。

ObservationとArchitecture Decisionを混同しない。

---

## 15.3 Current Problems

最低限:

```text
Causal vs Family persistent Execution authority

different state/claim/persistence implementation

persistent stage asymmetry

Result / Artifact ownership duplication

lineage authority ambiguity / dual representation

legacy runtime source remaining beside Product runtime

migration/bootstrap ownership ambiguity historically
```

をevidenceに応じて記載する。

---

## 15.4 Objectives

ENH-E4終了時の状態として、

* one canonical Product Execution authority
* persistent StageExecution
* unified Result/Artifact ownership contract
* one authority per semantic lineage relation
* no active retired legacy runtime dependency
* Product-only bootstrap
* no indefinite transition debt

を記載する。

---

## 15.5 Scope / Out of Scope

Phase 06 Non-goals / Constraintsを反映する。

特にout of scope:

* scientific algorithm redesign
* statistical methodology redesign
* unrelated frontend redesign
* unrelated performance optimization
* historical application-data migration
* external legacy compatibility

---

## 15.6 Completion Criteria

Final completionはG08 PASS。

また、

```text
G05 = Product Execution convergence
G07 = safe boundary before unrelated Enhance work
G08 = ENH-E4 final closure
```

というcheckpoint semanticsを記録する。

---

# 16. Document 02 — Enhance構想承認記録

対象:

```text
00_enhance_background/
02_Enhance構想承認記録.md
```

Decision:

```text
APPROVED
```

としてmaterializeする。

承認対象には最低限:

```text
HD-001 ... HD-007
E4-ADR-001 ... E4-ADR-012
E4-INV-001 ... E4-INV-016
E4-REQ-001 ... E4-REQ-035
E4-CON-001 ... E4-CON-010
E4-G01 ... E4-G08 decomposition
```

を記載する。

---

## 16.1 Conditions

以下を承認条件として含める。

* scientific algorithms are not redesigned by ENH-E4
* shared scientific modules are preserved independently from legacy orchestration
* GenericExecutor does not become lifecycle owner
* structural lineage does not retain indefinite dual authority
* Product bootstrap does not depend on root legacy migrations
* temporary dual-read/write must have bounded exit Gate
* final G08 requires open transition debt = 0

---

## 16.2 Rejected / Not Selected Alternatives

Phase 06のRejected Alternativesを要約する。

少なくとも、

* existing Causal modelをそのまま唯一authorityにする案
* existing Family modelをそのまま唯一authorityにする案
* multiple persistent Execution authoritiesをfinal stateとして維持する案
* ambiguous dual lineage authority
* indefinite compatibility dual-write/read

を「not selected」として記録する。

「過去に正式却下されたrequirement」と混同しない。

---

# 17. Document 03 — 要件定義書改定記録

対象:

```text
00_enhance_background/
03_要件定義書改定.md
```

以下をmaterializeする。

## 17.1 Requirement Documents

最低限:

```text
10_要件定義.md
```

加えてArchitecture requirementを具体化するため改定対象となるdesign documentsを必要に応じてcross-referenceする。

---

## 17.2 Added Requirements

```text
E4-REQ-001 ... E4-REQ-035
```

を全件記録する。

Phase 06の原文semanticを維持する。

短縮によってverification conditionを失わせてはならない。

---

## 17.3 Before / After

主要な差分をconcept単位で記載する。

例:

```text
Before:
Causal / Family separate persistent lifecycle

After:
one canonical persistent Product Execution authority
```

同様に、

* Stage
* Result
* Artifact
* Lineage
* Legacy
* Migration
* CLI

を扱う。

---

## 17.4 Removed Requirements

承認済みevidenceに明示的なremoved requirementが存在しない場合:

```text
NONE
```

とする。

Architecture candidateを採用しなかったことを「既存requirement削除」と誤記しない。

---

## 17.5 Open Requirement Issues

Phase 07 Remaining Unknownsを確認し、

* requirement自体をblockするもの
* implementation detailとして後Gateへ割り当て済みのもの

を分離する。

approved architectureを再openしない。

---

# 18. Document 04 — 設計書改定記録

対象:

```text
00_enhance_background/
04_設計書改定.md
```

Phase 06 ADRを中心にmaterializeする。

主要Design Area:

```text
Runtime boundary

Canonical Execution

Execution identity

State / mutation semantics

Claim / lease ownership

StageExecution

GenericExecutor responsibility

Result ownership

Artifact ownership

Downstream reference

Lineage authority

Legacy boundary

Scientific capability boundary

Migration/bootstrap

Standalone CLI

Compatibility terminology
```

各Areaで、

```text
Before
After
Reason
ADR
Evidence
```

が追跡可能な形にする。

---

## 18.1 Architecture / Data / API Impact

最低限:

### Architecture

one canonical Product lifecycle authority。

### Data

Execution / Stage / Result / Artifact / lineage semanticsとcardinality。

### API

外部API pathのrenameを勝手に決めず、

```text
all user-visible Product analyses must converge to canonical lifecycle
```

というcontractを記録する。

### Worker

one claim/lifecycle authority。

### CLI

low-level scientific utility boundaryはpersistent lifecycle外。

---

## 18.2 Migration / Compatibility

HD-005 / HD-006を正確に記録する。

```text
Product-only clean rebuild
historical application data migration not required
root legacy migration chain not canonical
external legacy runtime compatibility out of scope
```

ただしshared scientific capabilityは保持する。

---

# 19. Document 05 — 要件・設計整合性 / Traceability

対象:

```text
00_enhance_background/
05_要件・設計整合性およびトレーサビリティ確認.md
```

本Taskで最も厳密な文書とする。

---

## 19.1 Requirement → ADR / Design

全:

```text
E4-REQ-001 ... E4-REQ-035
```

について、

* requirement
* ADR
* Invariant
* revised snapshot document
* section
* status

をmapする。

Missing = 0。

---

## 19.2 ADR → Requirement

全:

```text
E4-ADR-001 ... E4-ADR-012
```

に最低1つ以上のRequirementまたは明示的なdesign-only consequenceを対応付ける。

---

## 19.3 Invariant Coverage

全:

```text
E4-INV-001 ... E4-INV-016
```

をsnapshot sectionとGateへmapする。

---

## 19.4 Constraint Coverage

全:

```text
E4-CON-001 ... E4-CON-010
```

を関連Gateとnegative design ruleへmapする。

---

## 19.5 Gate Coverage

最低限:

```text
E4-G01 ... E4-G08
```

について、

* architecture outcome
* primary requirement set
* first-established invariants
* transition debt
* downstream gate

をcross-referenceする。

---

## 19.6 G01 AC Coverage

以下を明示的に判定可能なtraceabilityとする。

```text
E4-G01-AC-001
family/type、identity、state transition target contract

E4-G01-AC-002
ExecutionResult/StageResult + Artifact ownership cardinality

E4-G01-AC-003
typed structural / generic-only lineage allowlist

E4-G01-AC-004
old authority is not redefined as target authority

E4-G01-AC-005
35 REQ / 16 INV / 10 CON traceability complete
```

---

## 19.7 Known Normalizations

以下を記載する。

### Phase 06 typo

semantic correction only。

### Phase 07 Transition Debt introduction wording

Transition Debt Registerをauthorityとして使用。

これはarchitecture changeではない。

---

## 19.8 Traceability Decision

全materialization checkが成立した場合:

```text
CONSISTENT_AND_READY_FOR_G01_INDEPENDENT_REVIEW
```

とする。

G01を自分でPASS判定してはならない。

---

# 20. Snapshot Materialization Principle

対象:

```text
00_enhance_background/
Revised_requirements_definition_documents/
```

snapshotは**差分メモではなく、ENH-E4承認後の要件・設計状態を復元できるcomplete snapshot**とする。

各snapshotについて:

1. 対応する `docs/wiki/requirement_definition/` 文書をbaselineとして読む
2. baseline全文を保持する
3. ENH-E4により変更が必要なsectionだけapproved deltaを統合する
4. unaffected requirement/designを削除・要約しない
5. `{{SNAPSHOT_CONTENT}}` を残さない

---

# 21. Snapshot Baseline Preservation Rule

baselineの無関係な記述を、

* stylistic cleanup
* shortening
* restructuring
* terminology modernization

の目的で変更してはならない。

目的は、

```text
baseline
+
approved ENH-E4 delta
```

のsnapshot作成である。

ENH-E4と無関係な既存requirementの意味を変えてはならない。

---

# 22. Snapshot 00 — プロダクトコンセプトメモ

baseline:

```text
docs/wiki/requirement_definition/
00_プロダクトコンセプトメモ.md
```

ENH-E4によるproduct concept上の意味変更がある場合のみ反映する。

最低限、既存conceptと矛盾しないことを確認する。

新しいproduct visionを創作してはならない。

ENH-E4によるsemantic changeが不要ならbaselineをそのままsnapshot化してよい。

その場合08 resultに:

```text
NO_ENH_E4_SEMANTIC_CHANGE
```

と記録する。

---

# 23. Snapshot 10 — 要件定義

baseline:

```text
docs/wiki/requirement_definition/
10_要件定義.md
```

ここにはapproved Target Requirements:

```text
E4-REQ-001 ... E4-REQ-035
```

を欠落なく統合する。

既存requirement IDをrenumberしてはならない。

ENH-E4 requirementは `E4-REQ-*` identityを保持する。

必要なら、

```text
ENH-E4 Canonical Execution Architecture Requirements
```

相当の明示sectionを追加する。

---

# 24. Snapshot 21 — 論理データ設計

baseline:

```text
docs/wiki/requirement_definition/
21_論理データ設計.md
```

approved target contractを論理データmodelとして反映する。

最低限:

```text
Canonical Execution
Execution family/type discriminator
StageExecution
ExecutionResult
StageResult
Artifact metadata
physical Artifact store boundary
typed structural lineage
generic-only lineage
retry/rerun/revise identity relation
```

を扱う。

---

## 24.1 Cardinality

G01 AC-002を満たせる粒度で、

```text
Execution → StageExecution
Execution → Result
StageExecution → StageResult
Result → Artifact
Execution / Result / Stage ownership
```

のcardinality / ownershipを明示する。

Phase 06がexact cardinalityを定義している箇所はそのまま使用する。

不足部分を勝手に推測しない。

実装時決定事項なら、

```text
IMPLEMENTATION_DETAIL_WITHIN_APPROVED_CONTRACT
```

と明示する。

---

## 24.2 Semantic Identity

physical table nameやcurrent accidental schemaではなく、

```text
semantic authority
```

を正文とする。

既存tableをtarget tableとして無条件に再登録してはならない。

---

# 25. Snapshot 22 — プロダクト基本設計

baseline:

```text
docs/wiki/requirement_definition/
22_プロダクト基本設計.md
```

最低限以下を反映する。

```text
one canonical Product runtime Execution authority

Causal / Exploratory / Predictive as workflow semantics

canonical lifecycle owner

worker claim boundary

persistent StageExecution

GenericExecutor subordinate workflow infrastructure

Result / Artifact ownership

Lineage authority policy

legacy runtime boundary

shared scientific capability boundary

standalone CLI boundary
```

Current / Targetの責務境界が分かるように記載する。

---

# 26. Snapshot 23 — API・インターフェース設計

baseline:

```text
docs/wiki/requirement_definition/
23_API・インターフェース設計.md
```

既存endpointを勝手にrenameしてはならない。

approved contractとして最低限:

* user-visible Product analysis submission must create canonical Execution
* family/type does not create separate lifecycle authority
* retry preserves identity
* rerun creates distinct identity where approved
* revise creates distinct identity where approved
* cancel follows canonical lifecycle contract
* Result/Artifact references use canonical semantic identity
* low-level standalone scientific CLI is not a persistent audit API

を反映する。

既存API compatibility requirementと矛盾が生じた場合は隠さず08 resultへ記載する。

---

# 27. Snapshot 30 — 詳細設計

baseline:

```text
docs/wiki/requirement_definition/
30_詳細設計.md
```

G01 independent reviewが可能な程度に、approved detailed contractを反映する。

最低限:

```text
Execution identity semantics

family discriminator

state / mutation contract

retry identity semantics

rerun identity semantics

revise identity semantics

cancel semantics

claim / lease ownership boundary

StageExecution lifecycle contract

GenericExecutor responsibility exclusions

Result semantic level

Artifact metadata / physical store separation

downstream reference contract

lineage relation classification

generic-only lineage allowlist / registry concept

migration/bootstrap contract

compatibility boundary
```

を記載する。

---

# 28. Lineage Allowlist Rule

G01 AC-003を満たすため、Phase 04 / Phase 06から実際のrelation inventoryを抽出する。

以下を混同しない。

```text
typed structural relation
```

と

```text
generic-only relation
```

各relationについて最低限:

```text
relation semantic
source type
target type
authority
persistence representation
allowed generic-edge status
```

を記録する。

relationを推測で追加しない。

---

# 29. Generic Lineage Rule

Target contractでは、

```text
typed structural relation
```

と同じsemantic relationをgeneric edgeの独立authorityとして残してはならない。

generic edgeは、

```text
typed relationshipでは表現されないapproved generic-only relation
```

に限定する。

closure / exportはprojectionでありauthorityではない。

---

# 30. Execution Mutation Contract

snapshot内で最低限以下を分離する。

## Retry

approved identity semanticsに従う。

## Rerun

retryと同義にしない。

## Revise

rerunと同義にしない。

## Cancel

queued/running behaviorをapproved contract範囲で記述する。

Current behaviorとTarget behaviorを混同しない。

---

# 31. Unknown Handling

Phase 07 Remaining Unknownsを読む。

Unknownを理由にapproved architectureを再設計しない。

分類:

```text
BLOCKS_G01_CONTRACT
DEFERRED_TO_IMPLEMENTATION_GATE
DEFERRED_TO_G08_VERIFICATION
OUT_OF_SCOPE
```

G01 contractを本当に確定できないUnknownだけ、

```text
BLOCKS_G01_CONTRACT
```

とする。

その場合はmaterialization自体は可能な範囲まで行い、08 resultを `BLOCKED_G01_CONTRACT` とする。

---

# 32. No Placeholder Rule

allowed write対象11文書について、最終的に以下形式のplaceholderを残してはならない。

```text
{{...}}
```

検査例:

```text
rg '\{\{[^}]+\}\}' \
  docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/00_enhance_background
```

README内の説明用meta-syntax等はallowed write対象外なので、対象fileを限定して判定すること。

---

# 33. Identifier Completeness Checks

静的checkを行う。

最低限:

## Requirements

```text
E4-REQ-001 ... E4-REQ-035
```

35件すべてが、

* revised requirement/design snapshot
* traceability document

のどこかで正規にmaterializeされていること。

---

## ADRs

```text
E4-ADR-001 ... E4-ADR-012
```

12件すべてtraceable。

---

## Invariants

```text
E4-INV-001 ... E4-INV-016
```

16件すべてtraceable。

---

## Constraints

```text
E4-CON-001 ... E4-CON-010
```

10件すべてtraceable。

---

## Human Decisions

```text
HD-001 ... HD-007
```

7件すべて承認記録へ存在。

---

## Gates

```text
E4-G01 ... E4-G08
```

8件すべてtraceabilityへ存在。

---

# 34. G01 Contract Checks

本materializationが最低限以下を明示しているか確認する。

## G01-AC-001

```text
family/type
identity
state transition
```

が全familyを記述する。

## G01-AC-002

```text
ExecutionResult
StageResult
Artifact ownership
cardinality
```

が明示される。

## G01-AC-003

```text
typed structural
generic-only
```

lineage classificationが明示される。

## G01-AC-004

current old Causal/Family authorityをtarget canonical authorityとして無批判に再登録していない。

## G01-AC-005

```text
REQ 35
INV 16
CON 10
```

のtraceability missing = 0。

本Task Agent自身はG01 PASSを宣言しない。

---

# 35. No Production Change

本Taskでは以下を実行してはならない。

```text
pytest
alembic upgrade
docker compose up
uvicorn
worker startup
frontend startup
curl
runtime integration test
```

また、

* source
* tests
* migrations
* configuration

を変更しない。

documentation-only materializationである。

---

# 36. Baseline / Working Tree

開始時に記録する。

```text
repository root
branch
HEAD
git status --short
start time
```

branchが、

```text
refactor/ariadne_mvp_e4
```

でなければ、

```text
BLOCKED_WRONG_BRANCH
```

として停止する。

既存working tree変更をstash / reset / restoreしてはならない。

---

# 37. Existing Changes

開始前から存在するworking tree変更を記録し、自分の変更と区別する。

本Taskのallowed write以外に新規変更を作ってはならない。

---

# 38. Materialization Consistency Rules

以下を満たす。

## Rule 1

01〜05とsnapshotでTarget Architectureが食い違わない。

## Rule 2

Current Architecture evidenceをTarget requirementとして誤記しない。

## Rule 3

Target Architectureを現在実装済みであるかのように書かない。

必ず、

```text
Current
Approved Target
```

を区別する。

## Rule 4

G01時点ではproduction implementation未着手であることを維持する。

## Rule 5

Final ENH-E4 completionとG01 completionを混同しない。

---

# 39. Snapshot Status Label

各snapshot文書に必要に応じて、冒頭付近に以下相当を記録してよい。

```text
Snapshot status:
Approved target requirement/design snapshot for ENH-E4.

Implementation status:
Not implied by this document.
Implementation progress is tracked by Gate reports.
```

ただし既存文書構造を過度に崩さない。

---

# 40. Traceability Source References

背景文書では必要に応じて以下をpathで参照する。

```text
Architecture Review Phase 01
...
Architecture Review Phase 07

Database reinitialization completion decision record
```

長大なevidence全文を複製しない。

正規evidenceへのpathを示す。

---

# 41. G01 vs Future Implementation Contract

本Taskで作る文書は、

```text
Why
Approved What
Approved Architecture Contract
```

である。

後続の、

```text
10_enhance_instruction/
06_...実装指示書
07_...テスト指示書
```

の役割を侵食しない。

exact file edit instruction、exact test command、implementation sequenceは書かない。

Gate decompositionへのreferenceは記録してよい。

---

# 42. Required Result

以下を生成する。

```text
40_operator_prompts/
architecture_review/
08_enhance_background_materialization_result.md
```

構造:

```markdown
# 08 Enhance Background Materialization Result

## 1. Metadata

- Prompt:
- Repository:
- Branch:
- HEAD before:
- Working tree before:
- Started at:
- Finished at:
- Status:

## 2. Inputs Reviewed

### Architecture Review

### Database Evidence

### Requirement / Design Baseline

### Human Approval

## 3. Files Materialized

| File | Baseline | ENH-E4 Delta | Status |
|---|---|---|---|

## 4. Human Approval Materialization

| HD | Approval Record Location | Status |
|---|---|---|

## 5. Requirement Materialization

- E4-REQ count:
- Missing:
- Duplicate / conflict:

## 6. ADR Materialization

- ADR count:
- Missing:

## 7. Invariant Materialization

- INV count:
- Missing:

## 8. Constraint Materialization

- CON count:
- Missing:

## 9. Gate / Transition Debt Materialization

### Gates

### Transition Debt

### Phase 07 normalization

## 10. Snapshot Summary

### 00 Product Concept

### 10 Requirements

### 21 Logical Data

### 22 Product Basic Design

### 23 API / Interface

### 30 Detailed Design

## 11. G01 Contract Readiness

| AC | Evidence Document / Section | Status |
|---|---|---|

Cover:
- E4-G01-AC-001
- E4-G01-AC-002
- E4-G01-AC-003
- E4-G01-AC-004
- E4-G01-AC-005

Use:
- READY_FOR_INDEPENDENT_REVIEW
- INCOMPLETE
- BLOCKED

Do not use PASS.

## 12. Placeholder Audit

- Target files checked:
- Placeholder occurrences:
- Status:

## 13. Consistency Audit

### Current vs Target separation

### Requirement / Design consistency

### ADR / REQ consistency

### Gate consistency

### Known normalizations

## 14. Remaining Unknowns

| ID | Classification | G01 Blocking? | Handling Gate |
|---|---|---:|---|

## 15. Unauthorized Changes Audit

List changed files.

State whether any non-allowed file changed.

## 16. Materialization Decision

One of:

- READY_FOR_G01_INDEPENDENT_REVIEW
- BLOCKED_G01_CONTRACT
- MATERIALIZATION_INCONSISTENCY
- BLOCKED_WRONG_BRANCH
- BLOCKED

## 17. Completion Status

One of:

- COMPLETED
- COMPLETED_WITH_NONBLOCKING_UNKNOWNS
- BLOCKED
```

---

# 43. Self-Check Commands

materialization後、最低限以下を行う。

```text
git status --short
```

```text
git diff --stat
```

allowed write filesについて:

```text
git diff -- \
docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/00_enhance_background
```

および08 resultを確認する。

---

# 44. Placeholder Check

allowed materialized filesに対して、

```text
{{...}}
```

が0件であることを確認する。

READMEはcheck対象から除外する。

---

# 45. Identifier Count Check

read-only shell / Python text parsingを使用してよい。

期待値:

```text
E4-REQ unique IDs = 35
E4-ADR unique IDs = 12
E4-INV unique IDs = 16
E4-CON unique IDs = 10
HD unique IDs = 7
Gate unique IDs = 8
```

注意:

同じIDが複数文書へtraceability目的で再掲されるため、単純な総出現回数ではなく、

```text
expected identifier set
⊆
materialized identifier set
```

として検査する。

---

# 46. Semantic Spot Checks

最低限以下を人間可読で確認する。

### Check A

Causal / Exploratory / Predictiveが別persistent Execution authorityとしてTargetに残っていない。

### Check B

GenericExecutorがlifecycle ownerとして記載されていない。

### Check C

persistent StageExecutionが全canonical workflowへ適用されている。

### Check D

ExecutionResult / StageResultのsemantic distinctionとone ownership contractが両立している。

### Check E

Artifact metadata authorityとphysical Artifact storeが分離されている。

### Check F

typed structural lineageとgeneric-only lineageのauthorityが曖昧でない。

### Check G

legacy orchestrationとshared scientific capabilityが分離されている。

### Check H

Product bootstrapがlegacy root migrationをrequireしていない。

### Check I

standalone low-level CLIがalternative persistent Execution architectureとして記述されていない。

### Check J

temporary dual authorityがfinal targetとして記述されていない。

---

# 47. Prohibited Behavior

以下をしてはならない。

* Phase 06 ADRを書き換える
* Human approvalを再解釈する
* Phase 07 Gateを再分解する
* requirement IDをrenumberする
* unknownを推測で解決する
* implementation済みでないTargetをCurrent behaviorとして記述する
* current implementationをTarget authorityとして無条件に採用する
* exact production class/table renameを新たに決める
* baseline requirement/designの無関係な箇所をcleanupする
* source requirement_definitionを変更する
* G01 PASSを自己宣言する

---

# 48. Completion Criteria

本Taskを `COMPLETED` または `COMPLETED_WITH_NONBLOCKING_UNKNOWNS` とするには全て必要。

### C1

01〜05 standard documentsがplaceholder-free。

### C2

6 snapshot documentsがplaceholder-free。

### C3

snapshotがcorresponding baseline全文を失っていない。

### C4

approved ENH-E4 deltaが該当snapshotへ統合されている。

### C5

HD-001〜007が承認記録へmaterializeされている。

### C6

E4-ADR-001〜012 coverage missing = 0。

### C7

E4-INV-001〜016 coverage missing = 0。

### C8

E4-REQ-001〜035 coverage missing = 0。

### C9

E4-CON-001〜010 coverage missing = 0。

### C10

E4-G01〜G08がtraceable。

### C11

G01 AC-001〜005がindependent review可能。

### C12

Current / Approved Target / Future Implementationが分離されている。

### C13

Phase 07 Transition Debt normalizationが記録されている。

### C14

source / test / migration / configurationを変更していない。

### C15

allowed write以外の新規変更がない。

---

# 49. Agent Final Response

作業終了時のchat responseは簡潔に以下のみ報告する。

```text
08_enhance_background_materialization_result.md を生成しました。

Status: <...>

Materialized standard documents: <count>/5
Materialized snapshot documents: <count>/6

Requirements covered: <count>/35
ADRs covered: <count>/12
Invariants covered: <count>/16
Constraints covered: <count>/10
Human approvals covered: <count>/7

G01 contract readiness:
<READY_FOR_INDEPENDENT_REVIEW | INCOMPLETE | BLOCKED>

Production source/test/migration/configurationは変更していません。
```

詳細はRepository上のmaterialized documentsと08 resultを正本とする。

---

# 50. Stop Condition

以下のいずれかで停止する。

1. 11文書のmaterializationと08 result生成を完了した
2. branch mismatch
3. approved Architectureとbaseline requirement/designに重大な矛盾を発見した
4. G01 contractを安全にmaterializeできないevidence不足を発見した

停止後、以下へ進んではならない。

* G01 PASS判定
* G02 implementation
* Coding Agent implementation
* migration implementation
* production source変更

次作業は、人間または独立reviewerによるG01 contract review後に別promptとして指示される。
