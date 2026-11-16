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

**適用する論理データ制約（関連Requirement）**

- **`NFR-001b`**：actual scientific library versionとStageAttempt effective seedを含むenvironment再構築metadataを保持する
- **`NFR-013`**：schema versionはversioned Spec/Plan/payload/descriptor等のcontract boundaryで識別し、全persistent Result/Artifact entityへgeneric schema_version fieldを要求しない
- **`AR-019`**：random seedだけでなくsplit indexまたはpartition artifactを保存する
