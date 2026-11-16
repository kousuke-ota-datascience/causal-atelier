# 23_51_idempotency_contract

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original source section numbering retained; document numbering is by interface responsibility.  
**Source blob:** `131467f02222f105a49e6dfdbcec0f49cadb0f41`.

---

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


## 98. RD-04：IF契約の要求起源・Trace

**Status:** `RD04_INTERFACE_CONSTRAINT_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。抽象化前のAPI／CLI／Navigationのwire・resource・state契約を失わないための移管記録。現在の実効Implementationを確認したことを意味しない。

### 98.1. FR-114a（SPLIT）

- 旧要件に含まれるIF固有情報：Idempotency要否をHTTP method/create一般ではなく、retryでduplicate durable side effectを生成し得るCommandかどうかで判定する
- RDの要求核／Legacy Trace：重複する永続的副作用を生む操作の再試行を安全に処理する
- `FR-114a`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.2. FR-114b（SPLIT）

- 旧要件に含まれるIF固有情報：対象Commandで`Idempotency-Key`を必須化し、missing keyを`IDEMPOTENCY_KEY_REQUIRED`、same key/different requestをHTTP 409 `IDEMPOTENCY_CONFLICT`として扱う
- RDの要求核／Legacy Trace：重複要求と競合要求を識別し、誤った二重処理を防止する
- `FR-114b`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)
