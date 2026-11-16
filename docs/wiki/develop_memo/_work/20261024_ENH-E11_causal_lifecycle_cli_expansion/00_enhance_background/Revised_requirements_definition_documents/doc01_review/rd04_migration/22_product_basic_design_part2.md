# DOC-01 — 22基本設計：RD-04移管原記録（2/2）

**Kind:** FLOW/AUDIT; permanent contracts in stock BD files. **Source HEAD:** `cc846ba070f476c182c63aab037f5f6fc0987135`.

## 22_12_security.md

**Source blob:** `e6f5b04d6416dee7545ec9b2da44dff9143af539`; constraints 5.

## 98. RD-04：要件由来の基本設計制約

**Status:** `RD04_DESIGN_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。旧要件の具体設計制約を担当領域へ移管。実装検証・ADR承認済みを意味しない。

### 98.1. FR-121（SPLIT）

- 元の設計情報を含む要件：全project-scoped routeでpersisted ProjectMembership role（OWNER/EDITOR/VIEWER）に基づくauthorizationをservice action前に検証する
- 改訂後RD／Legacy Trace：Project内操作を所属Roleに応じて認可し権限外の処理を防止する
- ID：`FR-121`; Status：`ACTIVE`; Implementation：`PARTIAL`; [逐条記録](../95_rd04_fr_application_review.md)

### 98.2. FR-124a（SPLIT）

- 元の設計情報を含む要件：Artifact metadata/downloadでProject境界とsafe content dispositionを検証するcurrent contractを維持する
- 改訂後RD／Legacy Trace：成果物の情報・取得をProject境界内で安全に利用できる
- ID：`FR-124a`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [逐条記録](../95_rd04_fr_application_review.md)

### 98.3. FR-124b（SPLIT）

- 元の設計情報を含む要件：legacy/generic routeを含むArtifact downloadでProjectMembership authorizationを一貫適用する
- 改訂後RD／Legacy Trace：旧経路を含む成果物取得に同じProject権限を適用する
- ID：`FR-124b`; Status：`ACTIVE`; Implementation：`PARTIAL`; [逐条記録](../95_rd04_fr_application_review.md)

### 98.4. NFR-008a（SPLIT）

- 元の設計情報を含む要件：current input validation、path traversal防止、secret非露出等のsafeguardを維持する
- 改訂後RD／Legacy Trace：入力検証と危険なパス・秘密情報の保護を維持する
- ID：`NFR-008a`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [逐条記録](../96_rd04_nfr_ar_application_review.md)

### 98.5. AR-020（SPLIT）

- 元の設計情報を含む要件：prediction row / local explanationをpotentially sensitive outputとして扱い、Project roleに応じてdetail exposureを制御する
- 改訂後RD／Legacy Trace：個票予測と局所説明は機微情報になり得るため、利用権限に応じ露出を制限する
- ID：`AR-020`; Status：`ACTIVE`; Implementation：`PARTIAL`; [逐条記録](../96_rd04_nfr_ar_application_review.md)

---

## 22_13_deployment.md

**Source blob:** `e3b5de7f55deb50d23e76a7a5874689224cde72a`; constraints 2.

## 98. RD-04：要件由来の基本設計制約

**Status:** `RD04_DESIGN_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。旧要件の具体設計制約を担当領域へ移管。実装検証・ADR承認済みを意味しない。

### 98.1. NFR-010a（SPLIT）

- 元の設計情報を含む要件：API processとWorker processを分離するcurrent deployment boundaryを維持する
- 改訂後RD／Legacy Trace：分析実行の負荷がAPIの応答性・稼働に不必要な影響を与えない
- ID：`NFR-010a`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [逐条記録](../96_rd04_nfr_ar_application_review.md)

### 98.2. NFR-010b（SPLIT）

- 元の設計情報を含む要件：Worker restart後の明示的resume/recovery semanticsを定義する
- 改訂後RD／Legacy Trace：実行基盤の再起動後に処理状態を復元・回復できる
- ID：`NFR-010b`; Status：`DEFERRED`; Implementation：`PARTIAL`; [逐条記録](../96_rd04_nfr_ar_application_review.md)

---

## 22_14_failure_model.md

**Source blob:** `11de1c496f83f276d33bdafa919e7754839d71b8`; constraints 2.

## 98. RD-04：要件由来の基本設計制約

**Status:** `RD04_DESIGN_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。旧要件の具体設計制約を担当領域へ移管。実装検証・ADR承認済みを意味しない。

### 98.1. FR-128b（SPLIT）

- 元の設計情報を含む要件：size limit、timeout等のoperational resource configurationを一元管理する
- 改訂後RD／Legacy Trace：運用上の処理規模と実行時間の上限を設定・適用できる
- ID：`FR-128b`; Status：`DEFERRED`; Implementation：`NOT_IMPLEMENTED`; [逐条記録](../95_rd04_fr_application_review.md)

### 98.2. NFR-007（SPLIT）

- 元の設計情報を含む要件：Metadata transactionとArtifact writeのcross-store failure compensationを定義する
- 改訂後RD／Legacy Trace：成果物と管理情報の不整合が発生した場合、安全に回復・検知できる
- ID：`NFR-007`; Status：`DEFERRED`; Implementation：`PARTIAL`; [逐条記録](../96_rd04_nfr_ar_application_review.md)

---

## 22_15_schema_dependency.md

**Source blob:** `3574325867fd027fb56dd48a65bff2f72d5aacc5`; constraints 5.

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

---

## 22_16_test_architecture.md

**Source blob:** `6bd70a40733514bc9d3a85741a91f459534269f7`; constraints 2.

## 98. RD-04：要件由来の基本設計制約

**Status:** `RD04_DESIGN_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。旧要件の具体設計制約を担当領域へ移管。実装検証・ADR承認済みを意味しない。

### 98.1. NFR-015（SPLIT）

- 元の設計情報を含む要件：Domain、Planner、Runner、API、Worker、UI、scientific benchmarkを分離testできる
- 改訂後RD／Legacy Trace：Domain・実行・API・UI・科学計算を個別に検証できる
- ID：`NFR-015`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [逐条記録](../96_rd04_nfr_ar_application_review.md)

### 98.2. NFR-024（SPLIT）

- 元の設計情報を含む要件：Navigation descriptor、route、renderer binding、runtime independenceをunit/integration/E2Eで分離検証できる
- 改訂後RD／Legacy Trace：画面構成・URL復元・表示・分析実行独立性を個別に検証できる
- ID：`NFR-024`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [逐条記録](../96_rd04_nfr_ar_application_review.md)

---

## 22_17_stage_contents_e8_effective.md

**Source blob:** `67ca2f2a1ad8025ad226e0fec71a25d6c516a5ac`; constraints 2.

## 98. RD-04：要件由来の基本設計制約

**Status:** `RD04_DESIGN_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。旧要件の具体設計制約を担当領域へ移管。実装検証・ADR承認済みを意味しない。

### 98.1. FR-175（SPLIT）

- 元の設計情報を含む要件：Data Qualityはdedicated backend operationを新設せずread-only availabilityとして扱い、Comparisonの`TIME_TREND`は既存grouping/aggregation semanticsを維持し、Findingsの`CHART`は既存persistent operation/result/artifact semanticsを維持する
- 改訂後RD／Legacy Trace：探索のデータ品質・時間推移・Findingを既存意味で利用できる
- ID：`FR-175`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [逐条記録](../95_rd04_fr_application_review.md)

### 98.2. FR-174（SPLIT）

- 元の設計情報を含む要件：existing Causal / Exploratory / Predictive capabilityを定義済みStage Contentsから操作可能にし、UI再配置だけを理由にanalysis execution semanticsを変更しない
- 改訂後RD／Legacy Trace：既存の因果・探索・予測機能を整理後の画面から利用でき、分析の意味を維持する
- ID：`FR-174`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [逐条記録](../95_rd04_fr_application_review.md)

---

