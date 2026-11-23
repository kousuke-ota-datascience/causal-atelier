# 21_23_value_execution_snapshot


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


### Local scientific PrivacyDecision — transient logical value (G01)

The local CLI path uses an immutable **ephemeral value**, not a Product Execution or database entity: `PrivacyDecision = (allowed:bool, run_id:RunId, request_hash:SHA256[JCS(ValidatedStudy)], root_identity:VerifiedRootIdentity, principal_uid:int, classification:AGGREGATE, row_export_requested:false, output_shape:DISCOVER_AGGREGATE_ONLY)`. `VerifiedRootIdentity` captures the verified live root FD identity (device/inode/owner/mode and local filesystem facts), **not a bare user path or persistent authorization credential**. The same `run_id/request_hash` refer to the Study and run-scoped sink; the decision governs an **aggregate-only class**, while the exact staged Graph/diagnostics inventory is checked later. This value is derived by policy evaluation, not caller input; it remains internal/transient and is not a new public Study/Status/Manifest field or Product relational entity. Status/Manifest retain existing outcome and hash semantics.
