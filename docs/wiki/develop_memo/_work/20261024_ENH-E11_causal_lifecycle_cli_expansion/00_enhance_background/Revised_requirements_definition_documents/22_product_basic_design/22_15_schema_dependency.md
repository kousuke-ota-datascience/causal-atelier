# 22_15_schema_dependency

**Status:** `BD01_E11_BASIC_DESIGN_REVISED / OWNER_POLICY_APPROVED / INDEPENDENT_REVIEW_PENDING`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `87196f2f03a7f3367724bc05fb254d1a4d98109e`.

---

## 18. Schema / Dependency Boundary

- `analysis-specification/1`の既存`analysis_family`を再利用する。
- Navigation Stage fieldをAnalysisSpecificationへ追加しない。
- ExecutionPlan / Execution / StageExecutionへNavigation Stage fieldを追加しない。
- Product Domainはbrowser route/navigation implementationへ依存しない。
- Scientific / ML / visualization libraryはPort / Adapter背後へ隔離する。
- Capability固有Adapterはcanonical runtime lifecycleを制御しない。
- Navigation metadata/stateについてはDB migrationを行わない。
- Reproducibility contractとして`StageAttempt.effective_random_seed: int | null`を追加するDB migrationを行う。
- `Execution.runtime_version_json`へ`ariadne_code_version / python_version / platform_system / platform_release / machine / libraries`を保存する。


## 97. BD-01：E11 version・dependency・migration boundary

- 本文§18の`StageAttempt.effective_random_seed`等のMigrationは既存Product構成に属する設計記録であり、**E11の新Method導入を理由に新DB Migrationを実施する判断ではない**。
- 旧`causal-analysis-spec/2`およびlegacy CLI/Result parserと新E11のversioned local specを別dispatchする。E11 Methodを旧v2でsilent enableしない。
- DEC08のExtras（DoWhy/EconML/Tigramite）・universal`uv.lock`・実効Versionを分離し、R/Q/N/DとMethod41の合致をpreflightで検査する。SDK/Backend objectを永続Domainへ含めない。
- 具体Schema/Port/Env lockのFreezeはIF-01/DD-01/Gate06。 [Environment/Compatibility](22_23_e11_environment_security_compatibility.md)。

## 98. RD-04：要件由来の基本設計制約

**Status:** `RD04_DESIGN_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。旧要件の具体設計制約を担当領域へ移管。実装検証・ADR承認済みを意味しない。

### 98.1. FR-161（SPLIT）

- 元の設計情報を含む要件：LightGBM / SHAP / LIME等のexternal analytical engineはoptional capabilityとして導入し、未導入でもcore startupと既存supported flowを壊さず、unavailable capabilityから別model/methodへsilent fallbackしない
- 改訂後RD／Legacy Trace：追加分析機能が未導入でも基本機能を使え、未対応手法へ勝手に切替えない
- ID：`FR-161`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [逐条記録](../95_rd04_fr_application_review.md)

### 98.2. FR-114a（SPLIT）

- 元の設計情報を含む要件：Idempotency要否をHTTP method/create一般ではなく、retryでduplicate durable side effectを生成し得るCommandかどうかで判定する
- 改訂後RD／Legacy Trace：重複する永続的副作用を生む操作の再試行を安全に処理する
- ID：`FR-114a`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [逐条記録](../95_rd04_fr_application_review.md)

### 98.3. FR-120a（SPLIT）

- 元の設計情報を含む要件：runtime API schemaから生成されるFastAPI OpenAPIをcurrent API contractとして提供する
- 改訂後RD／Legacy Trace：APIの機械可読な仕様を提供し実際の動作と一致させる
- ID：`FR-120a`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [逐条記録](../95_rd04_fr_application_review.md)

### 98.4. NFR-014（SPLIT）

- 元の設計情報を含む要件：`causal-analysis-spec/2`の正規contractおよび保存済みCausal Resultをschema versionに従って読取可能に保つ
- 改訂後RD／Legacy Trace：既存v2の因果分析仕様と保存済み結果を継続して読み取れる
- ID：`NFR-014`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [逐条記録](../96_rd04_nfr_ar_application_review.md)

### 98.5. NFR-028（SPLIT）

- 元の設計情報を含む要件：optional analytical engineのimport/availability failureをcore process startup failureへ伝播させず、capability discovery/selection時に局所化してstable unavailable state/errorとして報告する
- 改訂後RD／Legacy Trace：任意の分析エンジンが利用不能でも基本機能を継続でき、利用不能理由を識別できる
- ID：`NFR-028`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [逐条記録](../96_rd04_nfr_ar_application_review.md)
