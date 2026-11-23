# 21_40_integrity_constraints


---

## 6. 整合性制約

### 6.1 Project境界

- Project-scoped Entityの参照先は原則同一Projectに属する。
- `AnalysisSpecification`のResearchContextVersion / DatasetVersion / AnalysisViewは同一Project。
- `Execution`のDatasetVersion / input GraphVersion / input Result / base Executionは同一Project。
- `Annotation` target、WorkspaceSelection target、WorkspaceAnnotation target、ExportBundle Result、LineageEdge source/targetも同一Project。
- Project境界を越える比較が必要な場合はread-only projectionとして明示し、canonical Entity間FKを暗黙に跨がせない。

### 6.2 Version / 不変性

- DatasetVersionは登録後不変。
- ResearchContextVersion / AnalysisView / AnalysisSpecification / GraphVersionはFIXED後不変。
- ExecutionPlanは生成後不変。
- Executionのinput/snapshot/method/parameterはSubmit後不変。
- Result / Artifact / ExportBundleは生成後不変。
- 変更は新Version / 新Execution / 新Result等として明示する。

### 6.3 Referential / Cardinality制約

- DatasetVersionは1つのSOURCE Artifactを必須参照する。
- AnalysisViewは1つのsource DatasetVersionを必須参照する。
- AnalysisSpecificationはResearchContextVersionとDatasetVersionを必須参照し、AnalysisViewは任意。
- StageExecutionは1つのExecutionに所属する。
- StageAttemptは1つのStageExecutionに所属し、attempt numberはStageExecution内で一意。
- Resultは1つのExecutionに所属する。STAGE_RESULTのみStageExecutionを必須参照する。
- AnnotationはResultまたはGraphVersionのどちらか一方だけを対象とする。
- WorkspaceSelectionはProject/userにつき最大1件。
- ProjectMembershipはProject/userにつき最大1件。
- LineageEdgeのsemantic tupleは重複登録しない。

### 6.4 Operation別入力制約

Canonical Causal Operationの最低参照制約:

| Operation | Dataset | Graph | Input Result |
| --- | --- | --- | --- |
| DISCOVERY | 必須 | 禁止 | 禁止 |
| IDENTIFICATION | 必須 | 必須 | 禁止 |
| ESTIMATION | 必須 | 必須 | Identification Resultを要求。ただし明示されたlegacy snapshot互換を除く |
| REFUTATION | 必須 | 必須 | Treatment Effect等のupstream Resultを必須 |
| SENSITIVITY | 必須 | 必須 | Treatment Effect等のupstream Resultを必須 |

Family固有runtime planでOperation taxonomyが異なる場合も、input ownershipとsnapshotの不変性を維持する。

### 6.5 AnalysisView整合性

- selected / derived columnがsource Dataset schemaに対して解決可能である。
- derived column名を重複させない。
- filter operator/value typeがlogical typeに適合する。
- 非決定的関数、任意code execution、外部I/OをAnalysisView expressionとして許可しない。
- AnalysisViewのDataset compatibilityをWorkspaceSelection変更時にも再検証する。

### 6.7 Artifact ownership

- `artifact_scope = SOURCE`の場合、execution / stage execution / result ownershipを持たない。
- `artifact_scope = EXECUTION_OUTPUT`の場合、Executionを必須参照する。
- stage/result referenceを持つArtifactは、そのExecution/Project ownershipと整合する。
- `object_key`は一意であり、同一physical objectを別のcanonical Artifact identityとして二重管理しない。

### 6.9 ResearchContext relation整合性

- relation targetは同一ProjectのResearchContextVersion。
- self referenceを禁止する。
- relation typeは`REFINES / DERIVED_FROM / SUPERSEDES / RELATED_TO`。
- 特定relationのDAG性を要求する場合は、一般cycle検出を実装するまで「保証済み」と扱わない。

### 6.10 Lineage整合性

- LineageEdgeはsource/target存在確認後に保存する。
- source/targetは同一Project。
- semantic tupleを一意とする。
- direct FK/referenceとLineageEdgeが同じrelationを表す場合、両者の意味が矛盾してはならない。
- lineage queryはcanonical Entity / LineageEdgeをauthorityとし、presentation stateから推測しない。

### 6.11 Navigation / runtime境界

- Navigation Stageを`AnalysisSpecification / ExecutionPlan / Execution / StageExecution`へ追加しない。
- Current Family / Navigation Stageはbrowser route/navigation stateをauthorityとする。
- Navigation catalogはapplication metadataでありscientific schema registryへ登録しない。
- context selection不足をruntime Stage failureとして記録しない。Operation availabilityとして事前に表現する。

### 6.12 Unique / index論理制約

主要unique constraint:

| Entity | Unique key |
| --- | --- |
| DatasetVersion | (`project_id`,`dataset_key`,`version_label`) |
| DatasetVersion | (`project_id`,`dataset_key`,`content_hash`) |
| DatasetVersion | `source_artifact_id` |
| ResearchContextVersion | (`project_id`,`context_key`,`version_number`) |
| AnalysisView | (`project_id`,`view_key`,`version_number`) |
| AnalysisSpecification | (`project_id`,`specification_key`,`version_number`) |
| ExecutionPlan | `plan_hash` |
| StageExecution | (`execution_id`,`stage_key`) |
| StageAttempt | (`stage_execution_id`,`attempt_number`) |
| ProjectMembership | (`project_id`,`user_id`) |
| WorkspaceSelection | (`project_id`,`user_id`) |
| Artifact | `object_key` |
| ExportBundle | `object_key` |
| LineageEdge | (`source_type`,`source_id`,`relation_type`,`target_type`,`target_id`) |

Indexは検索・ownership validation・Lineage traversalに必要なFK/referenceを中心に設計し、logical uniquenessとphysical performance indexを混同しない。

### 6.13 Schema reader contract

Dataset schemaを参照するvalidator / application serviceは、`DatasetVersion.schema_json`からlogical typeを一貫して解決しなければならない。

最低要件:

- column名からlogical typeを取得できる。
- unknown/missing columnをsilent successにしない。
- logical type aliasの正規化規則を一箇所へ集約する。
- filter/type validationとUI schema表示で異なる型解釈を持たない。

**適用する論理データ制約（関連Requirement）**

- **`NFR-011a`**：current request/execution/stage correlation identifiersをlogへ出力する


### Local decision-to-bundle integrity constraint (G01)

A local publication can be sealed only if the supplied PrivacyDecision, actual staged `study.json` decoded by strict schema/JCS, run-scoped sink and publisher, verified root FD, live effective principal and **all staged artifact descriptors** agree. The publisher must recompute its stateless policy on this actual state; `allowed=true` alone is never an authority. A changed run/hash/root/UID, denied policy or restricted-row output in G01 violates integrity and prevents Marker/rename. Decision identity is transient; no extra key is inserted into public Manifest artifacts or Product entity tables. Same physical-file and root identity are verified again at publish; independent Reader validates committed bytes.


### G01 LocalRunManifest typed evidence and lineage joins

The local immutable `ValidatedRunEvidence` value contains validated Study and its semantically identical strict Study-wire projection, full Status-wire snapshot, actual supplied runtime/stochastic snapshots, staged six-field artifact descriptors, optional generated output Graph five-field ContentRef, typed Graph-negative reason tuple and null independent science review ref. Pure `LocalRunManifest.from_run_evidence` checks run_id, strict JCS request hash, matching Method/Estimand/Status science axes, five-field Question/Design/Dataset input-to-lineage equality and G01 input Graph/Identification null. **Generated output Graph Ref** (when positive) is TrustedRoot-relative `runs/{run_id}/graph.json`, whereas staged ArtifactDescriptor key is bundle-relative `graph.json`; prefix stripping and exact SHA/media join are required. Positive inventory is exactly study/status/graph; scientific-negative is exactly study/status/diagnostics with null Graph refs and the closed singleton `SCI_NO_ADMISSIBLE_PAG` in both evidence and Status; technical codes are rejected even if text matches. Pure validation cannot verify actual FD, trusted bytes or P04 science, which belong to P02/P03/P04/P05 and independent Reader. No Effect or invented Science PASS.


### PrivacyDecision equality does not attest origin

The local bundle invariant is `(supplied decision structurally equals Publisher independently derived current policy decision) AND (current authoritative policy result allowed) AND (verified staged data/root/UID/inventory consistent)`. A separately reconstructed but value-identical valid decision is accepted; no object identity or issuer provenance check exists. The word `forged` in security negatives refers only to detectable mismatches or attempts to bypass the trusted re-evaluation, not fully identical values. No marker/rename on a failed conjunct.


### G01 Graph-negative diagnostics consistency integrity

For G01/P1-M06 DISCOVER Graph-negative, a diagnostic Artifact is structurally valid only if its strict decoded internal payload has exactly `run_id` (Status/Manifest equality), `operation=DISCOVER`, `method_id=P1-M06`, and `reason_codes=[SCI_NO_ADMISSIBLE_PAG]` (exact equality with Status.reason_codes and immutable Manifest evidence reason tuple). The physical six-field descriptor hash/size describes actual bytes but alone is insufficient to establish these semantic joins. Reject unknown/missing fields, duplicate JSON keys, inconsistent run/reason, Graph/diagnostics inventory mixing and failed technical runs. Do not infer existence of an admissible scientific negative from the DTO.


### Local GraphProvenance and source/parent reference invariants

A `GraphEvidence` local scientific identity includes its typed provenance value, and JCS semantic `content_hash` covers the entire Graph projection including provenance except the self-digest. The source refs are precisely the immutable `question`, `design`, `dataset` five-field ContentRefs, and for current G01 DISCOVER match the corresponding Study.inputs and Manifest.lineage values. Parent graph reference is nullable and must be null for standalone G01/P1-M06; any non-null successor parent is a genuine previously stored immutable Graph artifact, never an output self-ref or Product Version ID. The referenced ContentRef.sha256 is the **actual full-byte file digest**, not the parent's Graph.content_hash, which must be separately validated from the parent's JCS meaning projection. These are semantic invariants, not a newly persisted entity or approval of editing an existing parent.
