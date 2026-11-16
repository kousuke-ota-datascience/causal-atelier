# 23_51_idempotency_contract


---

## 8. Cross-cutting Contract Policy

### 8.2 Idempotency

Idempotencyはretryでduplicate durable side effectを生成し得るCommandへ適用する。HTTP methodや「create」一般を判定基準にしない。

Scope:

```text
(project_id, command_scope, idempotency_key)
```

Required semantics:

- required key missing → `IDEMPOTENCY_KEY_REQUIRED`
- same key + same canonical semantic request → stored response replay、duplicate durable side effectなし
- same key + different request → HTTP 409 `IDEMPOTENCY_CONFLICT`
- request hashはpath上のsemantic resource identityを含む
- concurrent same-key requestはDB uniqueness/advisory lock等でsingle durable effectへ収束する
- idempotency replay recordは可能な限り対象metadata mutationと同一transactionでcommitする

Current contractでidempotency対象とするCommand:

- DatasetVersion create
- Execution batch create
- GraphVersion create
- GraphEditDraft create
- Result export create
- AnalysisView create
- Exploration execution submit
- Exploratory Result → AnalysisSpecification DRAFT create
- ResearchContext create
- AnalysisSpecification create / revise
- Predictive split-validation（durable Execution/Artifactを生成する場合）
- Predictive Execution submit / rerun / revise
- Annotation / WorkspaceAnnotation create
- Project Export create

対象外:

- pure GET/query/compare/preview/validate
- existing natural plan-hash idempotencyを持つExecutionPlan create
- uniquenessで重複を防ぐexplicit lineage link
- Project create
- cancel/fix/update等のstate-machine Command（別途自然なstate conflictで制御）

#### 8.2.1 Retry-safe Artifact materialization

exactly-once executionは保証しない。successful Stage outputのretry/restartでdurable Artifactを重複materializeしない。

- logical identity/object keyはExecution + Stage + output slot/ordinal + Artifact typeからdeterministically導出する。
- same logical output + same content hashは既存Artifactをreuseする。
- same logical output + different content hashはnondeterministic-output conflictとして失敗させる。
- Result/Artifact bindingはmetadata transactionでatomicに確定する。
- ArtifactStoreとmetadata DBのcross-store compensationはNFR-007に対応する`DEFERRED` scopeである。

**当該Interfaceの追加契約（関連Requirement）**

- **`FR-114a`**：Idempotency要否をHTTP method/create一般ではなく、retryでduplicate durable side effectを生成し得るCommandかどうかで判定する
- **`FR-114b`**：対象Commandで`Idempotency-Key`を必須化し、missing keyを`IDEMPOTENCY_KEY_REQUIRED`、same key/different requestをHTTP 409 `IDEMPOTENCY_CONFLICT`として扱う
 

#### 8.2.2 Research ContextのCurrent implementation差分（PREP-01）

`src/ariadne/interfaces/web_api/routers/workspace_lifecycle.py`（blob `eb90bd940fc7a35b84cda0e3fa58235a738cb0a1`）の`POST /projects/{project_id}/research-contexts`は`Idempotency-Key`を受け取らず、`IdempotencyServiceDep.execute`を呼ばない。呼び先`WorkspaceLifecycleService.create_research_context`（blob `ee84e914f8bc5136b9f9fee7323814a552a5d68a`）はversion番号を計算してcreate/commitする。このSource経路は、上記Required Contractの「ResearchContext create」を満たした実装として数えない。

`CURRENT_GAP`：鍵の欠落／同一鍵再実行／異ペイロード再送を負例検証し、Owner決定した実装Laneへ追跡する。現行APIの観測事実と将来の必須Contractを同一と見なさない。実行テストは`NOT_RUN`。
