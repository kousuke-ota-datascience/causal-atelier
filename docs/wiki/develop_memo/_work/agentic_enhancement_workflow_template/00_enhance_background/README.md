# 00_enhance_background — 背景・要件・設計文書の作成ガイド

**Document class:** Authoring Guide  
**Self-containment:** MUST — このREADMEだけで00層の目的・作成順序・各artifactの完成条件が分かること。

## Canonical filename rule

- canonical filename / directory nameはASCII charactersのみを使用する。
- semantic filename suffixはtechnical Englishとする。
- 日本語はdocument title / body textにのみ使用してよい。


## 1. Purpose

このdirectoryには、enhancementを開始する理由、改定対象となる要件・設計、承認、traceability、および開始時点のapproved snapshotを保存する。

00層の各artifactは、**そのartifactの主題について、結論・変更内容・判断理由を本文内で理解できる状態**にする。原典pathはprovenanceとして参照してよいが、「詳細は原典参照」だけで変更内容を省略してはならない。

## 2. 作成順序

1. `01_enhancement_concept_and_requirement_revision_plan.md`
   - problem / objective / scope / target outcome / expected requirement-design impact / initial Gate decompositionを記載する。
2. `02_enhancement_concept_approval_record.md`
   - Human ownerの決定、approved scope、conditions、明示的非承認事項を記録する。
3. `03_requirements_revision.md`
   - requirement deltaをBefore / Afterで記載し、new invariant / removed requirement / acceptance implicationを固定する。
4. `04_design_revision.md`
   - architecture / ownership / runtime / persistence / migration / compatibilityへのeffective design changeを記載する。
5. `05_requirements_design_consistency_and_traceability_review.md`
   - requirement -> design -> Gate -> Acceptance Criterionの対応と未解決事項を確認する。
6. `Revised_requirements_definition_documents/`
   - enhancement開始時点でapprovedとなった要件・設計のsnapshotを保存する。

## 3. External reference rule

外部文書は以下の目的で参照してよい。

- source requirement / designのprovenance
- issue / ADR / code / schema等のfact source
- approval evidence

ただし、現在artifactの結論や変更内容を外部文書へ委譲してはならない。

**NG:** `要件変更は既存設計書を参照。`  
**OK:** `REQ-012をAからBへ変更する。理由は...。Provenance: <path>.`

## 4. Architecture reviewを先に行う条件 — CONDITIONAL MUST

以下の場合は、実装契約を作る前にarchitecture discovery / target decision / Gate decompositionを実施する。

- runtime entrypoint / lifecycle変更
- authority / ownership変更
- persistence / schema / lineage変更
- legacy path除去・統合
- migration strategy変更
- 複数subsystemを跨ぐcanonical source-of-truth変更

architecture reviewの結論は00層の正式な背景・要件・設計へ反映する。Coding / Test Agentへ必要なnormative semanticsは、後続の06 / 07へeffective formで記載する。

## 5. Completion checklist

- [ ] enhancementのproblem / target outcomeが本文だけで理解できる。
- [ ] scope / out-of-scopeが明確である。
- [ ] requirement / design deltaが具体的に書かれている。
- [ ] external referenceはprovenanceであり、normative contentの代替になっていない。
- [ ] Gate decompositionがsemantic acceptance boundaryとして説明できる。
- [ ] unresolved issueとapproval conditionが明示されている。
