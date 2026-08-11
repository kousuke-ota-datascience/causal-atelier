# ENH-E5 設計改定

- 文書状態: `DRAFT_FOR_REVIEW`
- Revised effective designs: `21_logical_data_design.md`, `22_product_basic_design.md`, `23_api_interface_design.md`, `30_detailed_design.md`

## 1. Domain / Logical Data設計改定

### 1.1 AnalysisFamily

current codeの`AnalysisFamily`を再利用する。

`AnalysisSpecification`は既に`analysis_family`を保持し、Family-specific schemaをvalidationするため、重複Family discriminatorを追加しない。

### 1.2 Navigation concept

`NavigationStageDescriptor`, `FamilyNavigationDescriptor`, Current Family/StageをDomain Resource外の論理概念として扱う。

Navigation Stageを`AnalysisSpecification`, `ExecutionPlan`, `Execution`, `StageExecution`へ保存しない。

### 1.3 Runtime Stage model

existing`StageType / StageDefinition / ExecutionPlan / StageExecution`はruntime responsibilityとして維持する。

## 2. Product Basic Design改定

### 2.1 Presentation

Family tabs / Family-local Stage sidebar / route/historyはPresentation sectionのsubsectionとして扱う。

### 2.2 Application / Capability

- generic navigation coordinationはApplication
- concrete Stage catalogはCapability ownership

### 2.3 Execution Runtime

Navigation改修を理由にruntime Stage semanticsを変更しない。

Distribution / Metrics / Explainability等の具体例を用い、Navigation StageとExecution Stageが0:N / 1:N / N:1になり得ることを明示する。

## 3. API / Interface設計改定

### 3.1 Existing API preservation

Analysis Specification / Execution / Result interfaceへNavigation Stage required fieldを追加しない。

### 3.2 Navigation metadata interface

read-only descriptor APIをtarget案とする。exact endpoint/schemaはHuman approval後にfreezeする。

Frontend static full catalogとの二重管理は避ける。

### 3.3 Route interface

Family / Stageをdeep-linkableにするtarget routeを設ける。legacy routeをinventoryしてcompatibility mappingする。

## 4. Detailed Design改定

### 4.1 Module responsibility

Navigation descriptor、Capability-owned catalog、Application aggregation、Frontend route/renderer bindingを追加対象とする。

### 4.2 Runtime independence

ExecutionPlan / StageDefinition / StageExecutionへNavigation dependencyを追加しない。

### 4.3 CLI/library independence

backend execution function signatureへNavigation Stage required argumentを追加しない。

## 5. Predictive compatibility design

current Predictive visible controlsとgenerated`predictive-analysis-spec/1` semanticsを実コードから全量inventoryし、Setup/Train/Predict/Metrics/Explainability/Model Managementへ再配置する。

削除・簡略化を禁止する。

## 6. Migration / Deferred design

- DB migration: NONE target
- Result schema redesign: NONE
- Execution runtime redesign: NONE
- external engines: deferred
- new Finding/Evidence entity: deferred

## 7. Execution Agent contract isolation

Planning decisionはfreeze前に06/07/Pxxへ収束させる。

- SINGLE_EXECUTION Coding Agent: 06のみ
- Work Package Agent: assigned Pxxのみ
- Test/Audit Agent: 07のみ

repositoryはimplementation/evidence sourceでありnormative spec authorityではない。
