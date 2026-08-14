# ENH-E7 Enhancement構想承認記録

**文書種別:** Planning / Decision Artifact  
**Status:** APPROVED_FOR_PLANNING_ONLY  
**実装承認:** G01 PACKAGE EXECUTION GRANTED SUBJECT TO DERIVED PREFLIGHT READINESS

## 1. Planning baselineとして承認済みの事項

- Project ManagementとAnalysis WorkspaceをTop-levelで分離する。
- Project ManagementはProject resourceを管理する。
- Analysis Workspaceは選択済みProject / Research Context / Dataset Version / Analysis Viewをanalysis contextとして利用する。
- ENH-E6で導入したAnalysis Family / Stage navigationを維持する。
- 既存analysis機能は移設後も操作可能でなければならず、backend execution redesignは行わない。
- semantic contractを変えないvisual tuningは、実ブラウザ操作後のfollow-upで実施してよい。

## 2. 承認状態

HumanはENH-E7 Enhancement Planおよびworkflow artifact一式の作成を指示した。

```text
Concept / planning continuation: APPROVED
Coding implementation: G01 AUTHORIZED PACKAGE-BY-PACKAGE SUBJECT TO PREFLIGHT PASS
Gate G01 06 / 07 freeze: APPROVED / FROZEN
```

## 3. G01実装承認条件の状態

- Architecture Review: APPROVED
- G01 06/07: FROZEN
- Work Package eligibility: dependency evidenceからpreflightが導出（declared status literalはcontrolに使用しない）
- local remote: `causal-atelier`
- baseline: `1beea1c9eb3ffa5d01f7c266b826e52136d01e8f`
- **各packageの実行直前条件:** actual local repositoryでAgent Execution Readiness preflightがPASSすること

preflightがFAIL/BLOCKEDの場合、この承認を使ってexecutionを強行してはならない。

## 4. 根拠

- `provenance/01_ENH-E7_IA_handoff.md`
- `provenance/02_ENH-E6_workflow_revision_findings.md`
- `01_enhancement_concept_and_requirement_revision_plan.md`
