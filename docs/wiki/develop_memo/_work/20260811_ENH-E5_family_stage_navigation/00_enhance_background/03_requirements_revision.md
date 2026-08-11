# ENH-E5 要件改定

- 状態: `DRAFT_FOR_REVIEW`
- Revised effective requirement: `Revised_requirements_definition_documents/10_requirements_definition.md`

## 1. 改定の要旨

analytical FamilyとFamily-local Navigation Stageを別dimensionとして要件化し、Navigation Stageをruntime execution contractから分離する。

本文要件はcurrent effective requirementsとして再構成し、Enhancement固有差分はChange Logへ分離する。

## 2. 主要な追加・明確化要件

### 2.1 Navigation

- FR-129〜FR-139: Family / Stage navigation、route、global surface boundary

### 2.2 Navigation / Runtime separation

- FR-140: runtime Stage type/classをNavigationへ流用しない
- FR-141: Navigation:Executionの1:1 mappingを要求しない
- FR-142: CLI/library/backend use caseをNavigation Stageから独立させる
- FR-143: runtimeからUI route/sidebarへの逆依存を禁止する

### 2.3 Capability ownership

- FR-144〜FR-145: Family-specific Stage semanticsはCapabilityが所有する

### 2.4 Family-specific requirements

- FR-146〜FR-148: Exploratory
- FR-149〜FR-152: Predictive
- FR-153〜FR-156: Causal

### 2.5 Compatibility / State

- FR-157〜FR-162: existing Family discriminator再利用、persistent model保護、route compatibility、scope境界

## 3. 科学・分析上の要件改定

- Exploratory associationをcausal conclusionへ昇格しない。
- Predictive explanationをcausal importanceとして扱わない。
- Identification / Estimationを分離する。
- Family-specific result semanticsをgeneric scoreへ平坦化しない。

## 4. 廃止・禁止する前提

- Navigation Stage = Execution Stageという前提
- Stage order = runtime dependency / wizard progressionという前提
- Navigation StageをAnalysisSpecificationへ必須保存する前提
- Family間でStage taxonomyを共通化する前提

## 5. Deferred requirements

- External analytical engine integration
- persistent Finding/Evidence aggregate
- Overview / Flagship
- cross-session last-stage memory

## 6. Acceptanceへの接続

RequirementsはGate freeze前に06/07へ転写・収束する。Execution Agentが本要件定義を直接読んでscopeを補完する運用は行わない。
