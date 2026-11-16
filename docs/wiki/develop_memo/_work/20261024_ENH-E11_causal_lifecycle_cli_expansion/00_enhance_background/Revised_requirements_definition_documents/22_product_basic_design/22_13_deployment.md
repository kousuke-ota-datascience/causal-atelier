# 22_13_deployment

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `87196f2f03a7f3367724bc05fb254d1a4d98109e`.

---

## 16. Deployment

現行実装ではFastAPI Web API、polling Worker、Product persistence DB、ArtifactStore Port（default LocalArtifactStore）が分離されている。Family / Navigation Stage導入のために別runtime execution serviceを新設しない。


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
