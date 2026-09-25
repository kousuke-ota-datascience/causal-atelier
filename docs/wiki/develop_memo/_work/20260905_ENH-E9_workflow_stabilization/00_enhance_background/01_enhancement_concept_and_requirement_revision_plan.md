# ENH-E9 Enhancement Concept and Requirement Revision Plan

- Enhancement ID: `ENH-E9`
- Working title: `Post-E8 Workflow Stabilization`
- Status: `DRAFT_NOT_FROZEN / BLOCKED_PREREQUISITE`
- Requirement authority: `docs/wiki/requirement_definition/`

## 1. Objective

ENH-E9はnew analytical capabilityを追加せず、E8後に残ったworkflow usability residualとCausal Diagnostics backend conformance gapを閉じる。

Historical observation inventoryをそのままbacklog化せず、E8 G03 formal PASS baselineに対して再観測してresidual scopeを確定する。

## 2. Required evidence before scope freeze

1. ENH-E8 G03 canonical Independent Verification PASS decision
2. exact accepted PASS SHA
3. historical `Enhance_request.md`
4. historical E9 causal-result backend handoff
5. current frontend/backend implementation at the PASS SHA
6. applicable product/scientific/browser tests
7. current `docs/wiki/requirement_definition/` snapshot

## 3. Requirement handling rule

- New FR/NFR/ARは初期状態では追加しない。
- usability項目は既存Requirement / Basic Designへのconformanceとして成立するかを先に判定する。
- `FR-048`はcurrent snapshotで`IMPLEMENTED`だが、structured diagnostics contractの実装事実を再評価する。
- Requirement truthとimplementation truthが不整合なら、実装へ合わせてRequirementをsilent rewriteしない。
- Requirement semantic deltaが必要な場合はHuman review/approvalを経て `03_requirements_revision.md` と revised snapshotへ反映する。

## 4. Protected constraints

- E8 Stage responsibility / navigation / lineage semanticsを維持する。
- OutcomeはDiscovery → GraphVersion designated outcome → Identification read-only → Estimationの一方向ownershipを維持する。
- Treatment selector ergonomicsをOutcome overrideへ拡張しない。
- Frontendはbackendに存在しないESS/weight/adjusted balanceを推測・生成しない。
- all estimatorへ同一diagnostic setを強制しない。

## 5. Proposed acceptance boundaries

- G01 Context / Data Usability Residual
- G02 Causal Discovery / Graph Interaction Residual
- G03 Identification Input Ergonomics
- G04 Causal Diagnostics Backend Contract Completion
- G05 Integrated Regression Acceptance

Gate scopeはresidual matrix確定後にfreezeする。

## 6. Completion condition for planning

- E8 G03 PASS baselineが固定済み
- residual matrixがevidence-backed
- affected Requirement / Designがtraceable
- Requirement revision要否が明示済み
- G01-G05 semantic claimとdependencyがHuman review可能
- 06/07へ転記すべきprotected invariantとAcceptance Criteria sourceが確定済み
