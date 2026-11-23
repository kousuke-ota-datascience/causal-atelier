# 10_17_fr_api_cli


---

## FR original requirement rows

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| FR-113 | API / CLI | 互換性を管理した版付きAPIを提供できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-114a | API / CLI | 重複する永続的副作用を生む操作の再試行を安全に処理する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-114b | API / CLI | 重複要求と競合要求を識別し、誤った二重処理を防止する | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-115 | API / CLI | 利用側が入力不正・競合・不在・権限不足・処理失敗を判別できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-116 | API / CLI | 既存Executionから再実行用prefillを取得できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-117 | API / CLI | ExportをAPIとUIから同一contractで生成する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-118 | API / CLI | generic Product CLIからFamily別Specificationをsubmitし、Product Execution status/resultを取得できる | SHOULD | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| FR-119 | API / CLI | 履歴を持たないCLIは探索後警告等を独自推測しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-120a | API / CLI | APIの機械可読な仕様を提供し実際の動作と一致させる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-120b | API / CLI | API仕様と公開する入出力例との整合性を検証できる | MUST | DEFERRED | PARTIAL | FUTURE |
| FR-142 | API / CLI | CLI / Python library / backend use case / runtime executorはCurrent Navigation Stageを指定せずanalysis executionを開始できる | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-201 | Local Scientific CLI | 承認された因果分析をProduct Web／DBに依存せずCLIから実行し、科学的負結果・利用不能状態・技術失敗を区別する再現可能な成果物を得られる | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| FR-203 | Legacy Compatibility | 既存Product因果分析と新Local Scientific CLI契約を区別し、旧仕様と既存Review／Override統制を維持できる | MUST | ACTIVE | UNVERIFIED | ENH-E11 |


### Local G01 input, technical outcome and scientific-negative contract (FR-201/203)

The local scientific CLI must validate a versioned Study and its declared Operation/Method/Estimand, preserving strict separation from legacy Product v2. For G01 DISCOVER/P1-M06, Question, Design and Dataset are required input content references; Graph and Identification are not input refs. A successful published result may contain a valid Graph; a legitimately scientific no-Graph outcome must be distinguishable from Backend/schema/I/O failure. **An arbitrary or matching reason string is not sufficient proof of scientific-negative status**: the G01 semantic validator accepts only the registered reserved SCI_NO_ADMISSIBLE_PAG reason code as a structural candidate, and actual scientific publication additionally requires method-specific justification. Unrecognized/technical codes fail closed; unsupported Methods/Operations cannot silently fall back to an alternative. These elaborate FR-201 and FR-203 without changing their required scope or status.


### G01 DISCOVER scientifically negative diagnostic artifact semantic validation

For an actual scientifically justified P1-M06 DISCOVER Graph-negative, `diagnostics.json` MUST be a strict typed **internal** G01 record; it is not sufficient that an arbitrary JSON object matches a stored artifact digest. Its exact required fields are `run_id`, `operation`, `method_id`, `reason_codes`, with `operation="DISCOVER"`, `method_id="P1-M06"`, and `reason_codes=["SCI_NO_ADMISSIBLE_PAG"]`. The diagnostic run must equal Status/Manifest run, and the reason list must exactly equal Status.reason_codes and the Manifest evidence reason tuple. Graph-positive MUST NOT include this diagnostic; technical/backend failure MUST NOT be mislabeled a successful scientific-negative. A schema-valid diagnostic does not itself establish scientific truth; P04 supplies the legitimate scientifically justified negative. This adds no new public E11 wire version or public operation.


### G01 Local Graph scientific provenance contract (FR-186/196 clarification)

For a G01 DISCOVER graph, the pre-existing `e11-local-graph/1` `provenance` object shall carry typed Method ID, effective Backend, CI test, declared scientific assumptions, the genuine source Question/Design/Dataset ContentRefs and a nullable scientific parent Graph ContentRef. The initial standalone G01 DISCOVER graph has no parent, and `version_id`/`parent_version_id` remain null. The sources must match validated Study and Manifest inputs and be checked against actual bytes at a trusted file authority boundary; a claimed hash or arbitrary `provenance={}` is not sufficient. Preserve circle/PAG uncertainty, dual hash domains and separation from Product GraphVersion ownership. This is a constrained value shape for an existing public field, not a new wire version; absence of independently proven assumptions or true FCI correctness is never disguised as scientifically verified.
