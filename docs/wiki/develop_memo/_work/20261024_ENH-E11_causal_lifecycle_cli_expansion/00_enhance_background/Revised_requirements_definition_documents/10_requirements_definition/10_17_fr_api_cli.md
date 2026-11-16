# 10_17_fr_api_cli

**Status:** `RD03_FORMAL_E11_ISSUED / OWNER_SHA_REVIEW_PENDING`; original ID, level and state retained.  
**Source blob:** `40b83f29c67b4a39f6db5393be7534c5e892d656`.

---

## FR original requirement rows

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| FR-113 | API / CLI | HTTP APIをversioned pathとversioned payloadで提供する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-114a | API / CLI | Idempotency要否をHTTP method/create一般ではなく、retryでduplicate durable side effectを生成し得るCommandかどうかで判定する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-114b | API / CLI | 対象Commandで`Idempotency-Key`を必須化し、missing keyを`IDEMPOTENCY_KEY_REQUIRED`、same key/different requestをHTTP 409 `IDEMPOTENCY_CONFLICT`として扱う | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-115 | API / CLI | validation、conflict、not found、forbidden、execution failureをcanonical errorで返す | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-116 | API / CLI | 既存Executionから再実行用prefillを取得できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-117 | API / CLI | ExportをAPIとUIから同一contractで生成する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-118 | API / CLI | generic Product CLIからFamily別Specificationをsubmitし、Product Execution status/resultを取得できる | SHOULD | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| FR-119 | API / CLI | 履歴を持たないCLIは探索後警告等を独自推測しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-120a | API / CLI | runtime API schemaから生成されるFastAPI OpenAPIをcurrent API contractとして提供する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-120b | API / CLI | canonical schema exampleとOpenAPI/exampleをsystematically同期・検証する | MUST | DEFERRED | PARTIAL | FUTURE |
| FR-142 | API / CLI | CLI / Python library / backend use case / runtime executorはCurrent Navigation Stageを指定せずanalysis executionを開始できる | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-201 | Local Scientific CLI | 承認された因果分析をProduct Web／DBに依存せずCLIから実行し、科学的負結果・利用不能状態・技術失敗を区別する再現可能な成果物を得られる | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| FR-203 | Legacy Compatibility | 既存Product因果分析と新Local Scientific CLI契約を区別し、旧仕様と既存Review／Override統制を維持できる | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
