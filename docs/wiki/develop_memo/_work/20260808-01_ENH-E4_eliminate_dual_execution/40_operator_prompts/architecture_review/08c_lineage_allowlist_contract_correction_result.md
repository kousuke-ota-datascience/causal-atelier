# 08c Lineage Allowlist Contract Correction Result

## 1. Metadata

- Prompt: 40_operator_prompts/architecture_review/08c_lineage_allowlist_contract_correction_prompt.md
- Repository: causal-atelier
- Branch: refactor/ariadne_mvp_e4
- HEAD: f361a9ba9fb87598205bfba14052c95f54e432a2
- Working tree before: existing deploy/.nfs000000000076202f00000088 change was preserved
- Started at: 2026-08-09 UTC
- Finished at: 2026-08-09 UTC
- Status: COMPLETED_WITH_NONBLOCKING_UNKNOWNS

## 2. Inputs Reviewed

Phase 04 lineage inventory、Phase 06 approved ADR、Phase 07 Gate decomposition、Phase 08/08b result、formal snapshot 21/30、Document 05 traceabilityを確認した。Architecture Decision、production code、test、migration、configuration、databaseは変更していない。

## 3. Failure Being Corrected

- Gate: E4-G01
- AC: E4-G01-AC-003
- Prior status: FAIL_FIX_IN_GATE
- Root cause: typed structuralとgeneric-onlyのrelation-level allowlistがsnapshotに具体化されておらず、baselineのUSED_INPUT、GENERATED、DERIVED_FROM等がgeneric authoritative relationとして許されるように読めた。

## 4. Approved Lineage Authority Baseline

### Typed structural

Execution→Result、Result→Artifact、Dataset/View→Execution input、Result→Execution input、Result→GraphVersion、Artifact→DatasetVersion、Execution→base/revision ExecutionをTYPED_STRUCTURALとした。これらのgeneric authoritative writeは許可しない。

### Generic-only

Artifact→Artifact stage/process derivation、Result→Result SUMMARIZES、typed equivalentを持たないDOCUMENTS/EVIDENCE_FOR、approved user-authored/manual linksをGENERIC_ONLYとした。

### Projection-only

closure、traversal、exportのsynthetic/derived representationをPROJECTION_ONLYとした。projectionはauthorityではない。

## 5. Formal Relation Allowlist

| Semantic Relation | Source | Target | Authority | Generic Edge Allowed | Evidence |
|---|---|---|---|---|---|
| Execution owns Result | Execution | Result | TYPED_STRUCTURAL | NO | Phase 06 relation classification; E4-REQ-015 |
| Result owns Artifact | Result | Artifact | TYPED_STRUCTURAL | NO | Phase 03/06 ownership classification; E4-REQ-018〜020 |
| Dataset/View is Execution input | DatasetVersion / AnalysisView | Execution | TYPED_STRUCTURAL | NO | Phase 04 typed-derived input evidence; E4-REQ-021 |
| Result is Execution input | Result | Execution | TYPED_STRUCTURAL | NO | Phase 06 Result→Execution input classification; E4-REQ-021 |
| Result produces GraphVersion | Result | GraphVersion | TYPED_STRUCTURAL | NO | Phase 04/06 source_result_id classification; E4-REQ-021 |
| Artifact derives DatasetVersion | Artifact | DatasetVersion | TYPED_STRUCTURAL | NO | Phase 04/06 source_artifact_id classification; E4-REQ-021 |
| Execution is rerun/revised from base | Execution | Execution | TYPED_STRUCTURAL | NO | Phase 06 mutation semantics; E4-REQ-008〜009 |
| Artifact stage/process derivation | Artifact | Artifact | GENERIC_ONLY | YES — AUTHORITY | Phase 04/06 no typed equivalent confirmed |
| Result summarizes Result | Result | Result | GENERIC_ONLY | YES — AUTHORITY | Phase 04/06 SUMMARIZES |
| Result/Artifact documents or evidences another resource | Result / Artifact | Specification / Dataset / View / related resource | GENERIC_ONLY | YES — AUTHORITY | Phase 04/06 DOCUMENTS / EVIDENCE_FOR where no typed structural relation exists |
| User-authored semantic link | approved Product resource | approved Product resource | GENERIC_ONLY | YES — AUTHORITY | Phase 04/06 manual/user-authored relation classification |
| Closure/traversal representation | typed and generic authoritative sources | exported/traversed graph | PROJECTION_ONLY | YES — PROJECTION ONLY | Phase 06 closure/export policy |
| Legacy ArtifactLineage | legacy Artifact | legacy Artifact | OUT_OF_SCOPE | NO Product target write | Phase 05/06 legacy boundary |

USED_INPUT、GENERATED、DERIVED_FROM、REVISED_FROM等のbaseline enum名は、source/target semantic relationを伴わないuniversal generic allowlistではない。structural meaningに該当する場合はTYPED_STRUCTURALとして扱い、generic authorityへ独立writeしない。

## 6. Baseline Relation-type Reconciliation

| Existing Relation Type | Target Interpretation | Authority | Action in Snapshot |
|---|---|---|---|
| USED_INPUT | Dataset/View→ExecutionまたはResult→Executionのstructural input、ただしsemantic source/targetで判定 | TYPED_STRUCTURAL | generic authoritative writeを禁止 |
| GENERATED | Execution→Result、Result→Artifact等のstructural ownership/output | TYPED_STRUCTURAL | generic authoritative writeを禁止 |
| DERIVED_FROM | Execution base/revision等のtyped relation、またはArtifact→Artifact stage derivation | TYPED_STRUCTURALまたはGENERIC_ONLY | source/target semantic allowlistで分岐し、名前だけで判定しない |
| REVISED_FROM | Execution→base/revision Execution | TYPED_STRUCTURAL | generic authoritative writeを禁止 |
| SUPPORTED_BY / EVIDENCE_FOR | typed equivalentがないsupport/evidence relation | GENERIC_ONLY | generic authorityを許可 |
| MOTIVATED | Result→AnalysisSpecification等のmanual/semantic link | GENERIC_ONLY | generic authorityを許可 |
| DOCUMENTS | Result/Artifact→Specification/Dataset/View | GENERIC_ONLY | typed equivalentがない場合のみgeneric authority |
| SUMMARIZES | Result→ResultまたはResult→Artifactのsummary relation | GENERIC_ONLY | generic authorityを許可 |
| SELECTED / REJECTED | approved user-authored semantic link | GENERIC_ONLY | generic authorityを許可 |
| closure/export synthetic relation | projection output | PROJECTION_ONLY | persistence authorityにしない |
| legacy ArtifactLineage | legacy-only artifact relation | OUT_OF_SCOPE | Product targetへ取り込まない |

## 7. Files Changed

| File | Change | Why |
|---|---|---|
| 00_enhance_background/Revised_requirements_definition_documents/21_論理データ設計.md | relation-level allowlist、authority values、direction、generic edge rule | E4-G01-AC-003を独立判定可能にする |
| 00_enhance_background/Revised_requirements_definition_documents/30_詳細設計.md | structural/generic-only writer、closure、export enforcement | allowlistを実行境界へ接続する |
| 00_enhance_background/05_要件・設計整合性およびトレーサビリティ確認.md | AC-003 correction evidence | traceabilityを更新する |
| 40_operator_prompts/architecture_review/08c_lineage_allowlist_contract_correction_result.md | result | correction record |

## 8. 21 Logical Data Contract

### Authority table

Section 12.7にrelation-level tableを追加した。AuthorityはTYPED_STRUCTURAL、GENERIC_ONLY、PROJECTION_ONLY、OUT_OF_SCOPEのいずれかである。

### Cardinality / direction

方向をExecution→Result、Result→Artifact、Dataset/View→Execution等として明示した。structural relationはtyped owner/referenceがauthorityであり、Result/Artifactのsemantic ownershipをgeneric edgeで代替しない。

### Generic edge restrictions

Generic Edge AllowedがNOのrelationはgeneric authoritative writeを拒否または実行しない。YES — AUTHORITYはGENERIC_ONLYのみ、YES — PROJECTION ONLYはclosure/traversal/export representationに限定する。

## 9. 30 Detailed Design Contract

### Structural writer rule

TYPED_STRUCTURAL relationはtyped structural writerがauthorityである。同じsemantic relationのgeneric authoritative writeはrejectまたは未実行とする。

### Generic-only writer rule

GENERIC_ONLY relationはapproved source/target classを検証したgeneric-only writerがauthorityとしてpersistできる。

### Closure

typed structural authorityとgeneric-only authorityを読みprojectionを返す。closureのoverwrite/deduplicationはauthority conflict resolutionではない。

### Export

exportはsynthetic/derived representationを生成できるが、persistence authorityではない。可能な限りTYPED_STRUCTURALまたはGENERIC_ONLYのsource classificationを保持する。

## 10. Traceability Update

### E4-G01-AC-003

21 Section 12.7のallowlistと30 Section 19.1のwriter/closure/export contractで、relation-level classification、authority、generic edge allowed semanticsを独立判定可能にした。

### Related ADR

E4-ADR-008。

### Related INV

E4-INV-011、E4-INV-012、E4-INV-016。

### Related REQ

E4-REQ-021〜025。

## 11. AC-003 Re-evaluation

1. relation-level allowlist present? YES
2. structural authority explicit? YES
3. generic-only authority explicit? YES
4. structural dual-write allowed? NO
5. closure/export authority? NO

E4-G01-AC-003: READY_FOR_INDEPENDENT_REVIEW

## 12. Regression Re-check

| AC | Status | Evidence |
|---|---|---|
| E4-G01-AC-001 | READY_FOR_INDEPENDENT_REVIEW | snapshot 21/30 identity/state/family contract unchanged |
| E4-G01-AC-002 | READY_FOR_INDEPENDENT_REVIEW | Result/Artifact logical contract unchanged |
| E4-G01-AC-004 | READY_FOR_INDEPENDENT_REVIEW | old authority remains Current/Before only |
| E4-G01-AC-005 | READY_FOR_INDEPENDENT_REVIEW | 05 traceability; 35 REQ / 16 INV / 10 CON |

本resultはG01 PASSを宣言しない。

## 13. Identifier / Placeholder Audit

- REQ: 35/35
- ADR: 12/12
- INV: 16/16
- CON: 10/10
- HD: 7/7
- Gate: 8/8
- Placeholder: 0件

## 14. Diff Quality Audit

- unrelated semantic change: NONE
- architecture change: NONE
- unauthorized files: NONE（既存deploy/.nfs000000000076202f00000088の変更は保持）
- mass rewrite: NONE

## 15. Remaining Unknowns

E4-UNK-016〜023のlineage/export/namespace detail、E4-UNK-019のgeneric endpoint validation、E4-UNK-012のArtifact reuse等はimplementation detailとして残る。relation authority classification自体はblocking unknownではない。外部compatibility、legacy cleanup、retentionは後続Gateで扱う。

## 16. Decision

READY_FOR_G01_INDEPENDENT_REVIEW

E4-G01-AC-003のrelation-level allowlist、authority、generic edge semantics、writer boundary、closure/export projectionをformal snapshotへmaterializeした。G01 PASSは宣言していない。

## 17. Completion Status

COMPLETED_WITH_NONBLOCKING_UNKNOWNS
