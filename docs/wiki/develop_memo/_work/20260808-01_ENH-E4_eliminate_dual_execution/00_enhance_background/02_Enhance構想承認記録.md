# Ariadne / ENH-E4 Enhance構想承認記録

## 1. 対象計画
- Enhancement ID: ENH-E4
- Target Plan: `00_enhance_background/01_Enhance構想・要件改定計画.md`

## 2. 承認情報
- Decision: APPROVED
- Approved by: project owner（Phase 07 Human Approval Record）
- Approved at: 2026-08-08（Repository記録上のPhase 07 baseline）

## 3. 承認対象
HD-001 unified canonical Product Execution aggregate、HD-002 all canonical workflowsのpersistent StageExecution、HD-003 ExecutionResult/StageResult under one Result ownership contract、HD-004 typed structural lineage + generic-only lineage、HD-005 Product-only runtime boundaryとexternal legacy compatibilityの明示、HD-006 Product-only clean rebuild / historical application-data migration不要（pre-production context）、HD-007 standalone low-level CLI utility boundaryを承認する。

Architecture baselineはE4-ADR-001〜012、E4-INV-001〜016、E4-REQ-001〜035、E4-CON-001〜010、E4-G01〜G08とする。

## 4. 条件・留保
- scientific algorithmsはENH-E4で再設計しない。
- shared scientific modulesはlegacy orchestrationと独立して保持する。
- GenericExecutorはlifecycle ownerにしない。
- structural lineageはindefinite dual authorityにしない。
- Product bootstrapはroot legacy migrationsに依存しない。
- temporary dual-read/writeにはbounded exit Gateを持たせる。
- G08ではopen transition debt = 0とする。
- external consumerの不存在はRepository evidenceでは証明されていないため、legacy source/data removalは別のcompatibility decisionに従う。

## 5. 却下事項
採用しなかったarchitecture candidateとして、既存Causal modelのみを唯一authorityにする案、既存Family modelのみを唯一authorityにする案、複数persistent Execution authorityをfinal stateに残す案、ambiguous dual lineage authority、indefinite compatibility dual-write/readを記録する。これは既存requirementの正式な削除ではない。

## 6. 備考
Phase 06 ADRは提案から承認済みbaselineへ昇格しているが、承認記録は実装認可ではない。本TaskもG01 PASS、coding、migration、data destructionを認可しない。
+### Identifier coverage register

- ADR: E4-ADR-001, E4-ADR-002, E4-ADR-003, E4-ADR-004, E4-ADR-005, E4-ADR-006, E4-ADR-007, E4-ADR-008, E4-ADR-009, E4-ADR-010, E4-ADR-011, E4-ADR-012
- Invariant: E4-INV-001, E4-INV-002, E4-INV-003, E4-INV-004, E4-INV-005, E4-INV-006, E4-INV-007, E4-INV-008, E4-INV-009, E4-INV-010, E4-INV-011, E4-INV-012, E4-INV-013, E4-INV-014, E4-INV-015, E4-INV-016
- Constraint: E4-CON-001, E4-CON-002, E4-CON-003, E4-CON-004, E4-CON-005, E4-CON-006, E4-CON-007, E4-CON-008, E4-CON-009, E4-CON-010
- Gates: E4-G01, E4-G02, E4-G03, E4-G04, E4-G05, E4-G06, E4-G07, E4-G08
