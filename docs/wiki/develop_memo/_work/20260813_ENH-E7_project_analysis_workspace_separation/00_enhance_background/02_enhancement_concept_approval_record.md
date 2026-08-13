# ENH-E7 Enhancement構想承認記録

**文書種別:** Planning / Decision Artifact  
**Status:** APPROVED_FOR_PLANNING_ONLY  
**実装承認:** NOT GRANTED

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
Coding implementation: NOT YET AUTHORIZED
Gate 06 / 07 freeze: NOT YET AUTHORIZED
```

## 3. 実装承認前の条件

- Architecture Reviewをlocal source factで確認する。
- Requirement / Design revisionをreviewする。
- G01 06/07/Pxxをreviewし、execution用Statusへ明示的に変更する。
- local Git remote aliasとE7 baseline full SHAを解決する。
- Agent Execution Readiness preflightをPASSさせる。

## 4. 根拠

- `provenance/01_ENH-E7_IA_handoff.md`
- `provenance/02_ENH-E6_workflow_revision_findings.md`
- `01_enhancement_concept_and_requirement_revision_plan.md`
