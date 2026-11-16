# 23_14_api_causal

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original source section numbering retained; document numbering is by interface responsibility.  
**Source blob:** `131467f02222f105a49e6dfdbcec0f49cadb0f41`.

---

### 5.5 Causal Interface

#### 5.5.1 Graph

Causal analysisはGraph Version / candidate graphを扱う。現行実装のpublic interfaceは次である。

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects/{project_id}/graph-versions` | Graph Version作成。`Idempotency-Key`対応 |
| POST | `/projects/{project_id}/graph-edit-drafts` | candidateを基に編集DRAFT作成。`Idempotency-Key`対応 |
| GET | `/projects/{project_id}/graph-versions` | Project内Graph Version一覧 |
| GET | `/graph-versions/{graph_version_id}` | Graph Version取得 |
| GET | `/projects/{project_id}/graph-versions/{graph_version_id}` | Project境界を検証して取得 |
| PATCH | `/graph-versions/{graph_version_id}` | DRAFT更新 |
| PATCH | `/projects/{project_id}/graph-versions/{graph_version_id}` | Project-scoped DRAFT更新 |
| POST | `/graph-versions/{graph_version_id}/fix` | FIXED化 |
| POST | `/projects/{project_id}/graph-versions/{graph_version_id}/fix` | Project-scoped FIXED化 |
| GET | `/projects/{project_id}/graph-candidates` | Discovery ResultとGraph Versionのcandidate一覧 |
| GET | `/projects/{project_id}/graph-candidates/{candidate_kind}/{candidate_id}` | candidate取得 |
| POST | `/projects/{project_id}/graph-candidate-comparisons/query` | Graph candidate比較 |

Graph Version responseは少なくとも`graph_version_id / project_id / source_result_id / parent_graph_version_id / name / graph_type / graph_origin / provenance / designated_outcome_node / graph / content_hash / edit_rationale / status / created_by / created_at / allowed_actions`を返す。Navigation Stage IDをGraph Version identityへ追加しない。

#### 5.5.2 Causal operation

Runtime causal operation discriminatorは次である。

- `DISCOVERY`
- `IDENTIFICATION`
- `ESTIMATION`
- `REFUTATION`
- `SENSITIVITY`

現行実装の`CausalPlanner`はcanonical `Execution.operation`から**1 runtime Stageだけを持つcompatibility plan**を生成する。

| ExecutionOperation | StageType |
| --- | --- |
| `DISCOVERY` | `causal.discovery.v1` |
| `IDENTIFICATION` | `causal.identification.v1` |
| `ESTIMATION` | `causal.estimation.v2` |
| `REFUTATION` | `causal.refutation.v1` |
| `SENSITIVITY` | `causal.sensitivity.v1` |

したがって、`Identification / Estimation / Effects / Diagnostics`等のNavigation Stageを理由にCausal API/runtimeを単一Plan内の多段Stageへ作り替えない。科学的な前提関係はcanonical Executionの`input_graph_version_id / input_result_id`とResult/Lineageで扱う。


## 98. RD-04：IF契約の要求起源・Trace

**Status:** `RD04_INTERFACE_CONSTRAINT_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。抽象化前のAPI／CLI／Navigationのwire・resource・state契約を失わないための移管記録。現在の実効Implementationを確認したことを意味しない。

### 98.1. FR-051（SPLIT）

- 旧要件に含まれるIF固有情報：同一immutable `dataset_version_id`の先行Exploratory Resultを用いたconfirmatory分析では`EXPLORATORY_REUSE_SAME_DATA` warningとevidence Result IDを保持する
- RDの要求核／Legacy Trace：同一データを探索と確認的分析で再利用する場合、その事実と根拠を警告できる
- `FR-051`；Status=`ACTIVE`；Implementation=`PARTIAL`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.2. AR-004（SPLIT）

- 旧要件に含まれるIF固有情報：同一immutable `dataset_version_id`を探索とconfirmatory analysisで再利用した場合、`EXPLORATORY_REUSE_SAME_DATA` warningとlineage evidenceを保持する
- RDの要求核／Legacy Trace：同一データを探索と確認的分析に再利用した場合、その事実を示し独立検証として扱わない
- `AR-004`；Status=`ACTIVE`；Implementation=`PARTIAL`；[RD-04逐条レビュー](../96_rd04_nfr_ar_application_review.md)
