# 00_enhance_background — ENH-E6 背景・要件・設計

**Document class:** Authoring Guide  
**Self-containment:** MUST — このREADMEだけでENH-E6の00層artifactの目的・順序・参照規則・architecture review適用・completion conditionを理解できること。

## Canonical filename rule

- filename / directory nameはASCII charactersのみ。
- semantic suffixはtechnical English。
- 日本語はdocument title/bodyで使用可能。

## 1. Purpose

本directoryは、`ANOM-E5-001`をなぜENH-E6として修正するか、正本仕様を変更せず何をimplementation realizationとして成立させるか、どのarchitecture decisionとGate decompositionを採用したか、そのapproval/traceabilityを保存する。

ENH-E6では`docs/wiki/requirement_definition/**`を一切更新しない。03/04の「revision」はENH-localなrealization requirement/design deltaを記録するartifact名であり、canonical requirement/design revisionを意味しない。

## 2. 作成順序

1. `01_enhancement_concept_and_requirement_revision_plan.md` — problem/objective/scope/design impact/Gate proposal。
2. `02_enhancement_concept_approval_record.md` — Human owner approval、conditions、non-approval。
3. `03_requirements_revision.md` — canonical requirement変更なしを明示し、ENH-local realization requirement deltaを固定。
4. `04_design_revision.md` — navigation lifecycle/authority/presentation bindingのdesign delta。
5. `05_requirements_design_consistency_and_traceability_review.md` — requirement -> design -> G01 -> AC traceability。
6. `Revised_requirements_definition_documents/` — canonical requirement/design revisionがないためREADMEで6 standard snapshotsをN/Aと記録し、snapshot本体は生成しない。
7. `80_contract_amendment_log.md` — freeze後contract amendment履歴。現時点NONE。
8. ENH-E6追加artifact: `06_existing_implementation_design_alignment_review.md`, `90_technical_debt_and_future_enhancements.md`。

## 3. External reference rule

source requirement/design、ENH-E5 evidence、code、test、runtime outputはprovenance/fact sourceとして参照できる。ただし本00層artifactの結論・変更内容・判断理由を「参照先を読むこと」だけで省略しない。

## 4. Architecture reviewを先に行う条件 — CONDITIONAL MUST

ENH-E6は以下に該当するため適用必須であり、実施済みとして`40_operator_workflows/architecture_review/`へ記録する。

- runtime/navigation lifecycle change
- authority/ownership consolidation
- legacy analytical path consolidation
- UI/history/presentationを跨ぐcanonical source-of-truth alignment

Architecture Reviewのapproved decisionは01/03/04/05とG01 contractへeffective formで反映する。

## 5. Completion checklist

- [x] problem / target outcomeを本文で説明
- [x] in/out scopeを明示
- [x] canonical requirement/designを変更しないことを明示
- [x] ENH-local requirement/design deltaを具体化
- [x] external referenceをprovenanceに限定
- [x] Architecture Reviewを実施・反映
- [x] Gate decompositionをsemantic boundaryで説明
- [x] Human approval conditionを記録
- [x] unresolved issueとfuture scopeをledger化
- [x] contract amendment ledgerを初期化
