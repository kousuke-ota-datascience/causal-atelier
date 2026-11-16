# 22_14_failure_model

**Status:** `BD01_E11_BASIC_DESIGN_REVISED / OWNER_POLICY_APPROVED / INDEPENDENT_REVIEW_PENDING`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `87196f2f03a7f3367724bc05fb254d1a4d98109e`.

---

## 17. Failure Model

| Failure | 扱い |
| --- | --- |
| Navigation descriptor invalid | startup/query validation error。runtime execution failureへ変換しない |
| Unknown Family / Stage route | explicit 4xx / unsupported state。silent fallbackしない |
| Renderer binding missing | presentation/configuration defectとして検出 |
| Validation rejection | Executionを作成せず4xxまたはREJECTED Command Result |
| Technical runtime stage failure | Stage FAILED、Execution FAILED、既存retry policy |
| Analytical prerequisite unmet | Result/operation availabilityとして表現。Navigation Stage存在自体とは分離 |
| Artifact read integrity failure | `ArtifactHashMismatch`として扱い、破損contentを正常として返さない |
| Client disconnect | server-side Execution継続。cancelは明示Command |


## 97. BD-01：E11 Local失敗の責務分離

| Condition | Architecture response |
|---|---|
| Invalid schema/version/path/hash | 入力・セキュリティのpreflight拒否。科学的非識別と混同しない |
| Graph/Estimand nonidentification / ineligible | 原因・根拠を持つtyped scientific negative。Estimator不呼出し |
| Optional Backend unavailable | 選択MethodをUnavailableにし、他Estimatorへのsilent fallback禁止 |
| Inference unavailable / unsupported | point-onlyの許容をanalysis modeで判定し、無根拠CIは生成しない |
| Adapter execution or artifact readback failure | technical failure、完全公開禁止、staging・manifest commitを安全に回復 |
| Source/Artifact hash collision or mismatch | provenance/consistency error、正本の上書きや黙示再利用を拒否 |

**注意:** 旧Productのretry/idempotency/cross-store compensation方針とLocal Filesystem publicationの実装は分けて定義する。[科学的Gate](22_21_e11_scientific_pipeline.md)／[Artifact publish](22_22_e11_local_result_artifact_lineage.md)。

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
