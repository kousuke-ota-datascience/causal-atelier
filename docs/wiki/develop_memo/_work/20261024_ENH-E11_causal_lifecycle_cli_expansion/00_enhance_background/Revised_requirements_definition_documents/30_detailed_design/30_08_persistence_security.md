<!-- ENH-E11 split working copy: not a formal approval. -->
# 30 — persistence security

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [30_detailed_design.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/30_detailed_design.md) · blob `04d83541e55ab0364500afb4b92ef55c10785a0c`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

---

## 20. Persistence / transaction / idempotency

### 20.1 Persistence rule

Project Management / Analysis Workspace分離やStage presentation再編に伴う新DB migrationを要求しない。

current persistent entitiesとrelationをauthorityとする。

- Project
- Research Context Version
- Dataset / Dataset Version
- Analysis View
- Analysis Specification
- Execution / StageExecution / StageAttempt
- Result
- Artifact
- Lineage
- Annotation
- Workspace Selection等のselection state

Navigation state / Analysis Context composite / presentation grouping / current Stage presentation stateを新しいpersistent aggregateにしない。

### 20.2 Transaction boundary

Application commandはUnit of Workでdomain mutationとpersistenceを一貫させる。external scientific executionはtransactionを不必要に長時間保持しない。

### 20.3 Command idempotency

Idempotency keyを全POSTへ一律要求せず、duplicate durable side effectを作り得るcommandを対象とする。

logical scope:

```text
(project_id, command_scope, idempotency_key)
```

behavior:

```text
same scope/key + same semantic request
  → stored result/response replay
  → duplicate side effectなし

same scope/key + different semantic request
  → conflict
```

path上のsemantic resource IDもrequest hash inputへ含める。

browser route/history/presentation stateはidempotent command hashのsemantic inputに含めない。

### 20.4 Artifact materialization

retryでduplicate artifactを生成しない。Artifactのcontent identity / lineage / idempotency contractを用いてsingle durable outcomeへ収束させる。

---

## 21. Security / authorization

### 21.1 Project boundary

すべてのProject-scoped resource read/writeはactorのProject accessを検証する。

URLの`project_id`だけを信頼せず、resourceが同じProjectに所属することを検証する。

### 21.2 Navigation and authorization

route visibilityやdisabled controlをauthorization enforcementの代替にしない。

Project/Context/Data/Result/Analysis API commandはserver-side authorizationを実施する。

### 21.3 Cross-project prohibition

- Research Context restore
- Dataset Version restore
- Analysis View restore
- deep-linked resource resolve
- Result / Lineage traversal

でProject境界外resourceを採用しない。

---

## 22. Failure / error handling

### 22.1 Route failure

invalid routeはexplicit navigation errorとして扱い、無関係なdefaultへsilent redirectしない。

### 22.2 Context failure

selection restore失敗はunselected stateへ落とし、架空defaultを作らない。

### 22.3 API failure

loading/error stateとlast known current routeを分離する。API failureだけを理由にrouteを別Family/Stageへ書き換えない。

### 22.4 Runtime failure

runtime failureはExecution/StageExecution/Result scientific status contractで表現し、Navigation Stage自体をruntime statusとして更新しない。

### 22.5 Feature selector failure

Predictive feature selectorでDataset Version/schemaを取得できない場合はselectorをunavailable/errorとして表示し、架空column optionやstale selectionをscientific inputとして確定しない。

Dataset Version変更によりselected featureが無効になった場合は、無効featureをsilent保持しない。clearまたはvalid intersectionへのreconcileを行う場合、利用者に変更を示す。

---
