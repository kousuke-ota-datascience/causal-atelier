# 21_23_value_execution_snapshot

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`; original ID, level and state retained.  
**Source blob:** `72903b9ad48b5b7edabaa7bb1c2cace42aa46ce7`.

---

### 4.7 Execution Snapshot

Execution Snapshotは独立Entityではなく、`Execution`へ固定保存する再現性payloadである。

```json
{
  "snapshot_schema_version": "...",
  "analysis_family": "...",
  "dataset_version_id": "...",
  "input_graph_version_id": null,
  "input_result_id": null,
  "analysis_spec": {},
  "algorithm_or_estimator": "...",
  "parameters": {},
  "random_seed": null,
  "code_version": "...",
  "runtime_versions": {}
}
```

canonical JSONを用いて`snapshot_hash`を計算する。Execution作成後にsnapshotを上書きしない。

### 4.8 Batch View

Batchは独立Entityではない。`Execution.batch_key`が同じExecution集合をquery projectionとして表示する。

```text
Batch View
├─ batch_key
├─ executions[]
├─ operation
├─ parameter differences
├─ scientific result summary
└─ technical status summary
```

`batch_key`はExecution identityでもLineage edgeでもない。


## 98. RD-04：要求の論理データ制約の受入・Trace

**Status:** `DESIGN_CONSTRAINT_MIGRATION / OWNER_CONTENT_REVIEW_PENDING`。以下はRD-04で抽象化した元要件のうち、データ定義・同一性・来歴・正本性に関係する条項を論理設計側に残したもの。原文は出典保証目的で保持する。現行コードで検証済みと主張しない。

### 98.1. NFR-001b（SPLIT）

- 元要件（設計上の拘束を含む）：actual scientific library versionとStageAttempt effective seedを含むenvironment再構築metadataを保持する
- RD改訂後の要求：解析結果を再現するため実効ライブラリ版・乱数条件を取得できる
- Trace：`NFR-001b`; Status=`ACTIVE`; Implementation=`PARTIAL`; [逐条レビュー](../96_rd04_nfr_ar_application_review.md)

### 98.2. NFR-013（SPLIT）

- 元要件（設計上の拘束を含む）：schema versionはversioned Spec/Plan/payload/descriptor等のcontract boundaryで識別し、全persistent Result/Artifact entityへgeneric schema_version fieldを要求しない
- RD改訂後の要求：変化するデータ契約を識別し後方互換を制御できる
- Trace：`NFR-013`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../96_rd04_nfr_ar_application_review.md)

### 98.3. AR-019（SPLIT）

- 元要件（設計上の拘束を含む）：random seedだけでなくsplit indexまたはpartition artifactを保存する
- RD改訂後の要求：分析のデータ分割を再現可能な情報として保持しなければならない
- Trace：`AR-019`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../96_rd04_nfr_ar_application_review.md)
