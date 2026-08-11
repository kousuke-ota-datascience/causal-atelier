# ENH-E5 Enhancement Concept Approval Record

- 状態: `PENDING_HUMAN_APPROVAL`
- Planning pin: `46122c68333df03680b97c253a7b5d32bf9393e7`

## 1. Approval対象

- Familyをglobal analytical contextとする。
- Navigation StageをFamily-local work/view contextとする。
- concrete Stage definitionsをCapability ownershipとする。
- Navigation StageとExecution Stageを別conceptとする。
- Predictive existing settingsを100%保持する。
- External analytical enginesをscope外とする。

## 2. Architecture approval対象

### 2.1 既存AnalysisFamilyの再利用

current `AnalysisSpecification`等が使用する`AnalysisFamily`をFamily identityとして再利用する。

### 2.2 Navigation descriptor

Navigation metadata用の独立descriptor/value modelを設け、runtime StageType/StageDefinitionを再利用しない。

### 2.3 Navigation metadata delivery

backend read-only descriptor APIをcanonical catalog sourceとする案をtarget designとする。ただしendpoint/path/schema exactnessはHuman approval + current API convention照合後にfreezeする。

### 2.4 URL state

Current Family/StageをURLから復元する案をtargetとし、DB navigation-state persistenceは導入しない。

## 3. Explicitly not approved / out of scope

- runtime execution lifecycle redesign
- DB navigation state
- LightGBM / DoWhy / EconML
- Overview/Flagship実装
- new Finding/Evidence persistence hierarchy

## 4. Approval status

| Item | Status | Owner / Note |
| --- | --- | --- |
| Product concept | PENDING | Human |
| Requirements | PENDING | Human |
| Architecture | PENDING | Human |
| API exactness | PENDING | Architecture review |
| Gate decomposition | PENDING | Human |
| Coding start | BLOCKED | approval + preflight + freeze required |
