<!-- ENH-E11 split working copy: not a formal approval. -->
# 21 — history

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [21_logical_data_design.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/21_logical_data_design.md) · blob `72903b9ad48b5b7edabaa7bb1c2cace42aa46ce7`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

---

## 7. CHANGELOG

本章のみEnhancement履歴を扱う。`§1〜§6`は現在有効な論理データ設計であり、過去Enhancementの理解を前提としない。

### 7.1 ENH-E2 Golden Path Logical Model / Migration

ENH-E2ではGolden Path成立に必要な初期正本Entity、ER、Cardinality、state、integrity constraintsを定義した。当時のmigration事項はcurrent normative設計ではなく履歴として本節へ保持する。

- Project statusは既存`ACTIVE / ARCHIVED` modelを利用し、status追加migrationを必要としなかった。
- GraphVersionへ`designated_outcome_node`をnullable fieldとして追加した。
- Batch / Comparison / Lineage View / Graph Candidate / Graph Comparison / Operation Availability等はquery/projection modelとし、それだけを理由に新tableを作成しなかった。
- Dataset、Execution、Result、GraphVersion等のhard-delete抑制とLineage preservationを基本方針とした。

### 7.2 ENH-E3 Versioned Workspace Resource Expansion

Research Context、Analysis View、Analysis Specification、Execution Plan、StageExecution等のversioned/canonical resourceを追加し、Project内の分析Contextとworkflowを明示化した。

この拡張後も、E2で確立した「ER / Cardinality / Entity属性 / 非Entity / 状態 / 整合性制約」という論理設計観点は有効であり、本書では現行Entityへ拡張して復元している。

### 7.3 ENH-E4 Canonical Execution Architecture

- canonical `Execution / StageExecution / StageAttempt / Result / Artifact`をProduct lifecycle authorityとして整理した。
- historical `FamilyExecution / FamilyStageExecution / FamilyResult / FamilyArtifact`をcompatibility read modelへ降格した。
- runtime StageとResult ownershipを明示した。

### 7.4 ENH-E5 Family × Navigation Stage Application Architecture

- `AnalysisFamily`は既存domain discriminatorを再利用した。
- Navigation Stage / descriptor / current navigation stateはpersistent Entityへ追加しなかった。
- Navigation Stageとruntime `StageType / StageExecution`を分離した。

### 7.5 ENH-E5 Phase I Canonical Convergence

- Result / Artifact / Lineageのcanonical authorityを整理した。
- AnalysisView typed filter compatibility、family-specific result/status contract、canonicalization等をcurrent modelへ統合した。

### 7.6 ENH-E7 Analysis Context Logical Projection

Project Management / Analysis Workspace分離に伴い、Analysis Contextを次の4要素からなるapplication-level logical projectionとして明示した。

- Current Project
- Active Research Context
- Dataset Version
- Analysis View

Analysis Context専用persistent aggregateは追加せず、`WorkspaceSelection`と既存Project-scoped Resourceを利用する。Dataset Version変更時に非互換Analysis View selectionを解除し、selection不足時に架空default resourceを生成しない。
