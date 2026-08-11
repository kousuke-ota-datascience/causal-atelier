# 03 Result / Artifact Ownership Inventory Result

## 1. Metadata

- Prompt: `03_result_artifact_ownership_inventory_prompt.md`
- Prior phases: `01_runtime_entrypoint_inventory_result.md`, `02_execution_lifecycle_inventory_result.md`
- Repository: `/loc0/bigbrother/repositories/causal-atelier`
- Branch: `refactor/ariadne_mvp_e4`
- HEAD: `4cec28b2658639cae77e12d64a3c717bb2f885c`
- Start: `2026-08-08T11:06:00Z`; finish: `2026-08-08T11:08:34Z`
- Start status: existing ` D deploy/.nfs000000000076202f00000088`; no result file existed.
- Phase status: `COMPLETED_WITH_UNKNOWNS`
- Method: static source/ORM/migration/prior-result inspection only; no runtime execution.

## 2. Executive Summary

### 2.1 Result Models

| ID | Model | Lifecycle | Entity / table | Owner |
|---|---|---|---|---|
| E4-RS-001 | Causal Product Result | E4-LC-001 | `ResultOrm` / `product_result` | `ExecutionProcessor` + Product UoW |
| E4-RS-002 | Family Product Result | E4-LC-002, E4-LC-003 | `FamilyResultOrm` / `product_family_result` | Exploratory/Predictive services |
| E4-RS-003 | Legacy Discovery Result | E4-LC-005 | `DiscoveryResult` / `discovery_result` | legacy stage pipeline |
| E4-RS-004 | Legacy Discovery Algorithm Result | E4-LC-005 | `DiscoveryAlgorithmResult` / `discovery_algorithm_result` | legacy discovery pipeline |
| E4-RS-005 | Legacy Edge Weight Result | E4-LC-005 | `EdgeWeightResult` / `edge_weight_result` | legacy stage pipeline |
| E4-RS-006 | Legacy Treatment Effect Result | E4-LC-005 | `TreatmentEffectResult` / `treatment_effect_result` | legacy stage pipeline |

### 2.2 Artifact Models

| ID | Model | Entity / table | Storage |
|---|---|---|---|
| E4-AR-001 | Causal Product Artifact | `ArtifactOrm` / `product_artifact` | Product `ArtifactStorePort` |
| E4-AR-002 | Family Product Artifact | `FamilyArtifactOrm` / `product_family_artifact` | Product `ArtifactStorePort` |
| E4-AR-003 | Product Export Bundle | `ExportBundleOrm` / `product_export_bundle` | Product `ArtifactStorePort` |
| E4-AR-004 | Legacy Artifact | `Artifact` + `StoredObject` / `artifact` + `stored_object` | legacy `ArtifactStore` |

### 2.3 High-Level Ownership

| Lifecycle | Result | Artifact metadata | Physical object |
|---|---|---|---|
| Causal | Processor creates; `SqlResultRepository` persists | processor + `SqlArtifactRepository` | `ArtifactStorePort` |
| Exploratory | `ExploratoryService` | same service | `ArtifactStorePort` |
| Predictive | `PredictiveWorkflowService` | workflow/split services | `ArtifactStorePort` |
| CLI | no Product Result confirmed | local manifest/output | CLI/local filesystem |
| Legacy | legacy stage services | legacy artifact/materialization | legacy store + `StoredObject` |

## 3. Result Model Details

### E4-RS-001 — Causal Product Result

- Semantic unit: scientific output belonging to one causal Product Execution.
- Identity: UUID `result_id`, physical PK, API-visible; non-null `execution_id` FK; no stage FK.
- Creation/persistence: `ExecutionProcessor` maps scientific output into Result/Artifact rows and commits them with terminal execution state in the Product UoW.
- Payload: `result_type`, scientific status, summary/payload/diagnostics/warnings JSON, timestamp.
- Consumers: result routes, query/comparison/graph-candidate/closure/export/lineage services, causal UI.
- Reuse: `Execution.input_result_id` and `GraphVersion.source_result_id` explicitly reference it.
- Mutation/deletion: no Result update/delete port found; causal retry has no confirmed Result/Artifact cleanup or replacement path. FKs are restrictive.
- Lineage: closure derives Execution→Result and Result→Artifact; causal typed FKs are confirmed, processor-owned generic lineage writes are not.
- Evidence: `src/ariadne/product/domain/result.py:19-73` (`Result`); `src/ariadne/product/persistence/orm_models.py:171-202` (`ResultOrm`); `src/ariadne/product/persistence/repositories.py:395-421`; `src/ariadne/interfaces/worker/execution_processor.py:133-178`; `product_migrations/versions/20260805_product_0001_baseline.py:88-143`.

### E4-RS-002 — Family Product Result

- Semantic unit: analytical output belonging to a family execution and family stage execution.
- Identity: UUID `result_id`, PK/API-visible; non-null family `execution_id` and `stage_execution_id`.
- Creation/persistence: Exploratory and Predictive services persist `FamilyResultOrm` rows in their session transactions. The shared table does not make their payload semantics identical; `analysis_family`, `result_type`, and schema version remain discriminators.
- Payload: family, type, schema version, analytical status, summary/payload/diagnostics/warnings JSON.
- Consumers: exploration/predictive routes and Product closure; export and lineage read paths.
- Reuse: family draft/specification/lineage paths; no direct family-result FK into causal `input_result_id`.
- Mutation: predictive retry removes owned family Result/Artifact/lineage rows and physical keys; predictive rerun/revise creates a new execution and retains source rows. Exploratory retry/rerun/revise methods were not found.
- Important distinction: predictive split validation creates a family Artifact with `result_id=None`, so not every family stage output has a Result.
- Evidence: `src/ariadne/product/persistence/orm_models.py:429-540`; `product_migrations/versions/20260807_product_0004_enh_e3_workspace.py:108-148`; `src/ariadne/product/application/exploratory_service.py:370-417,445-470,528-545`; `src/ariadne/product/application/predictive_workflow_service.py:403-451,612-716`; `src/ariadne/product/application/predictive_split_service.py:198-224,273-287`.

### E4-RS-003..006 — Legacy Result Models

`DiscoveryResult` is stage-scoped and unique per stage; `DiscoveryAlgorithmResult` is a per-algorithm child with edge/graph/diagnostic Artifact FKs; `EdgeWeightResult` and `TreatmentEffectResult` are typed stage results with input/configuration and result/report Artifact FKs. Evidence: `src/ariadne/legacy/domain/metadata.py:1010-1068,1190-1285`.

## 4. Artifact Model Details

### E4-AR-001 — Causal Product Artifact

UUID `artifact_id`; nullable `execution_id` and `result_id`; `artifact_type`, unique `object_key`, hash, media type, size, metadata; table `product_artifact`. Processor stores physical bytes first, persists metadata second, and deletes the key on DB failure. Read retrieves through the store and verifies SHA-256. Evidence: `src/ariadne/product/domain/artifact.py:18-29`; `src/ariadne/product/persistence/orm_models.py:69-91`; `src/ariadne/adapters/local_artifact_store.py:10-64`.

### E4-AR-002 — Family Product Artifact

UUID `artifact_id`; non-null family execution/stage FKs and nullable Result FK; family, schema version, type, object key, hash, media type, size, metadata; table `product_family_artifact`. Exploratory/Predictive/split services use the same Product store and compensate failed commits by deleting newly stored keys. Evidence: `orm_models.py:518-540`; `exploratory_service.py:370-417`; `predictive_workflow_service.py:403-451`; `predictive_split_service.py:198-224`.

### E4-AR-003 — Product Export Bundle

Separate `ExportBundleOrm`/ `product_export_bundle` with export UUID, JSON Result ID list, object key/hash/media/size and manifest summary; no execution FK. Product closure exposes it in an artifact-like export response, but it is not a Result-owned Artifact. Evidence: `src/ariadne/product/persistence/orm_models.py` (`ExportBundleOrm`); `src/ariadne/product/application/product_closure_service.py:614-631,689-706,831-850`.

### E4-AR-004 — Legacy Artifact

Legacy `Artifact` has UUID `id`, kind/name/status, `stored_object_id`, producing `StageAttempt`, schema/hash/metadata and `deleted_at`. `StoredObject` carries backend/bucket/object key/version/checksum/status. Stage input/output, ManifestRecord, and ArtifactLineage provide associations. Evidence: `src/ariadne/legacy/domain/metadata.py:98-116,720-855`.

## 5. Ownership Chain Matrix

| Lifecycle | Execution | Result | Artifact metadata | Physical storage |
|---|---|---|---|---|
| Causal | `ExecutionProcessor` | processor + SQL Result repo | processor + SQL Artifact repo | `ArtifactStorePort` |
| Exploratory | `ExploratoryService` | same service | same service | `ArtifactStorePort` |
| Predictive | workflow/split services | workflow service | workflow/split services | `ArtifactStorePort` |
| Legacy | legacy execution/stage pipeline | stage-specific services | legacy materialization/services | legacy `ArtifactStore` + `StoredObject` |

Evidence: `src/ariadne/product/persistence/repositories.py:395-446`; service ranges above; legacy ranges above.

## 6. Result Identity Matrix

| Model | ID/generator | Table | Execution FK | Stage FK | API |
|---|---|---|---|---|---|
| E4-RS-001 | UUID `result_id` | `product_result` | yes, causal | no | yes |
| E4-RS-002 | UUID `result_id` | `product_family_result` | yes, family | yes, family stage | yes |
| E4-RS-003 | UUID `id`/legacy `new_id` | `discovery_result` | indirect | yes | legacy |
| E4-RS-004 | UUID `id` | `discovery_algorithm_result` | parent indirect | no direct | legacy |
| E4-RS-005 | UUID `id` | `edge_weight_result` | indirect | yes | legacy |
| E4-RS-006 | UUID `id` | `treatment_effect_result` | indirect | yes | legacy |

## 7. Artifact Identity Matrix

| Model | ID/generator | Table | Result FK | Execution FK | locator |
|---|---|---|---|---|---|
| E4-AR-001 | UUID `artifact_id` | `product_artifact` | nullable | nullable | `object_key` |
| E4-AR-002 | UUID `artifact_id` | `product_family_artifact` | nullable | non-null | `object_key` |
| E4-AR-003 | UUID `export_id` | `product_export_bundle` | JSON list, no FK | no | `object_key` |
| E4-AR-004 | UUID `id` | `artifact` | result-specific FKs | stage-attempt path | `stored_object_id` |

## 8. Cardinality Matrix

| Lifecycle | Execution:Result | Stage:Result | Result:Artifact | Execution:Artifact |
|---|---|---|---|---|
| Causal | 1:N | N/A persistent stage result | 0:N | 0:N |
| Family | 1:N | 1:N schema-allowed | 0:N | 0:N |
| Legacy | 1:N through stage graph | Discovery 1:1; algorithm child 1:N | 0:N | 0:N through stage/attempt |

Exact business cardinality by result type is not established; these are schema/service bounds.

## 9. Result Semantic Comparison

Causal and Family Results are both execution-produced JSON-backed scientific/analytical outputs with type/status/timestamp, so they are structurally analogous. Causal is execution-scoped and has typed input/result graph references; Family is mandatory stage-scoped and has family/schema discriminators. Legacy is more stage-specific and normalized around configuration and Artifact FKs. These facts support partial overlap, not interchangeability.

## 10. Artifact Semantic Comparison

Causal and Family Artifacts both persist object metadata (type, key, hash, media, size, JSON metadata) and use the Product store contract. Family additionally requires execution/stage and supports Result-null outputs; legacy has status, stage-attempt ownership, StoredObject indirection, and explicit artifact lineage. Shared storage protocol is not shared semantic ownership.

## 11. Creation / Completion Coupling

| Model | Trigger | Coupling |
|---|---|---|
| Causal Result/Artifact | processor output | DB metadata and terminal execution in one Product UoW; physical store compensated, not DB-atomic |
| Exploratory family | stage output | service session transaction plus physical compensation |
| Predictive family | workflow output/split validation | service session transaction plus physical compensation |
| Export bundle | export API request | independent metadata transaction plus physical compensation |

## 12. Stage / Result Ownership

Causal has no persistent generic stage Result; Result is Execution-scoped. Family Result is both Execution- and Stage-scoped. Predictive split proves family Artifact can exist without a Result. This is a confirmed structural difference, not a conclusion based solely on naming.

## 13. Physical Storage Comparison

Product causal/family/export paths use `ArtifactStorePort`; default `LocalArtifactStore` copies files under `ARIADNE_ARTIFACT_ROOT` or `.ariadne/objects` and computes SHA-256. Legacy uses a separate `ArtifactStore` and `StoredObject` metadata. The deployed backend and garbage-collection policy are unknown.

## 14. Read / Consumer Matrix

| Resource | Metadata/read path | Physical/read consumers |
|---|---|---|
| Causal Result | result routes, query, comparison, closure | causal UI, graph candidate, export, lineage |
| Family Result | exploration/predictive routes, closure | family UI, export, lineage |
| Product Artifact | ArtifactService/closure | download, dataset/analysis-frame paths, export |
| Export Bundle | closure export/detail | export/download |
| Legacy Artifact | legacy execution/dataset/visualization APIs | materialization/projection/legacy APIs |

## 15. Downstream Reuse

### 15.1 Input Reference Mechanisms

- Causal Result: direct `Execution.input_result_id` and `GraphVersion.source_result_id`.
- Family Result: family draft/specification and generic lineage paths; no direct causal Result FK.
- Causal Artifact: `DatasetVersion.source_artifact_id` targets `product_artifact`.
- Family Artifact: family service/download/split paths; no confirmed generic DatasetVersion FK.
- Export Bundle: JSON list of Result IDs; packaged read output, not typed execution input.

### 15.2 Cross-Model Interoperability

| Source → target | Status |
|---|---|
| Causal Result → causal Execution/GraphVersion | confirmed typed FKs |
| Family Result → family draft/lineage | confirmed |
| Family Result → causal `input_result_id` | not confirmed |
| Product causal/family Artifact → closure download/export | confirmed |
| Family Artifact → Product DatasetVersion source | not confirmed |

## 16. Mutation Semantics

### 16.1 Cancel

Predictive cancel changes execution state; complete Result/Artifact deletion effect is not confirmed. Causal/Exploratory cancel paths were not found.

### 16.2 Retry

Predictive retry deletes owned family Results, Artifacts, lineage, and physical keys before rerun. Causal retry exists but no corresponding cleanup/replacement path was found. Exploratory retry was not found.

### 16.3 Rerun

Predictive rerun creates a new execution and retains source rows. Causal rerun is new-execution behavior in Phase 02; no in-place Result replacement found. Exploratory rerun not confirmed.

### 16.4 Revise

Predictive revise creates a new execution with revision context and closure `REVISED_FROM`; source outputs remain. Causal/Exploratory revise not confirmed.

## 17. Failure / Partial Result Semantics

Technical failures do not automatically become Product Results under the product error contract. Known physical objects are deleted on failed metadata commit. Predictive split can intentionally persist an Artifact without a Result. Complete partial-result behavior for failed executions remains unknown.

## 18. Deletion / Cleanup

- Product Result/Artifact general delete: no path found; restrictive FKs.
- Causal/family failed commit: physical-key compensation confirmed.
- Predictive retry: row, lineage, and physical-key cleanup confirmed at `predictive_workflow_service.py:630-676`.
- Export: failed-commit cleanup confirmed; general garbage collection unknown.
- Legacy: `deleted_at` fields exist; full retention/physical cleanup workflow not traced.

## 19. Transaction Boundaries

DB writes are local transactions. Physical storage is a separate resource: store first, commit metadata, compensate on exception. This is not atomic across DB and object storage. Predictive retry crash-window behavior is not established.

## 20. Repository Abstraction Comparison

Product Result/Artifact ports and SQL implementations are confirmed for causal models. Family services mostly persist family ORM rows directly. Product physical storage is shared by port. Legacy uses separate repository/service and store abstractions. Abstraction reuse is partial and asymmetric.

## 21. Lineage Compatibility Boundary

Product closure reads both causal and family tables and emits common Result/Artifact lineage nodes. Family services explicitly write `LineageEdgeOrm`; causal typed FKs and closure-derived edges are confirmed, but processor-owned generic writes are not. Shared read representation therefore does not prove shared creation semantics.

## 22. Legacy Result / Artifact Comparison

Legacy has four stage-specific Result tables/classes and an Artifact/StoredObject composition tied to attempts and explicit artifact lineage. Product has generic causal Result, family stage Result, separate Product Artifact tables, and a Product store contract. Conceptual overlap exists; schema, owner, and lifecycle semantics are distinct.

## 23. Structural / Semantic Classification

| Comparison | Classification |
|---|---|
| Causal vs Family Result | structurally distinct, partially semantically analogous |
| Causal vs Family Artifact | structurally distinct, partially semantically analogous |
| Exploratory vs Predictive Result | shared persistence structure; semantic equivalence not proven |
| Product vs Legacy | structurally/operationally distinct with conceptual overlap |
| Product closure | common read/lineage boundary, not common persistence owner |

## 24. Result / Artifact Concept Inventory

### 24.1 Distinct persistent Result entities

6: E4-RS-001 through E4-RS-006.

### 24.2 Distinct Result tables

6: `product_result`, `product_family_result`, `discovery_result`, `discovery_algorithm_result`, `edge_weight_result`, `treatment_effect_result`.

### 24.3 Distinct persistent Artifact entities

4: E4-AR-001 through E4-AR-004; E4-AR-003 is export-bundle-like, not Result-owned.

### 24.4 Distinct Artifact tables

5 if export and legacy storage metadata are counted: `product_artifact`, `product_family_artifact`, `product_export_bundle`, `artifact`, `stored_object`.

### 24.5 Shared physical storage infrastructure

Product models share `ArtifactStorePort`; legacy uses a separate abstraction. Deployment-level backend sharing is unknown.

### 24.6 Shared Result / Artifact abstractions

Product closure shares a read representation; generic repositories are confirmed only for causal models. Product store port is shared.

### 24.7 Terminology collisions

“Result”, “Artifact”, “stage”, “lineage”, and “export” occur across Product and legacy but point to different tables and ownership edges. Export is artifact-like at API level but a separate ORM.

## 25. Prior Unknown Carry-forward

Phase 02 unknowns remain where this phase could not resolve them: CLI/Product boundary, full legacy reachability, production object-store backend, and runtime retry/crash behavior. Prior lifecycle IDs and conclusions are unchanged.

## 26. New Unresolved Items

- E4-UNK-009: causal retry behavior with existing Result/Artifact rows.
- E4-UNK-010: exact family Result business cardinality per stage/type.
- E4-UNK-011: cancellation cleanup of already-written family objects.
- E4-UNK-012: complete downstream reuse matrix for family Artifacts.
- E4-UNK-013: full causal generic-lineage persistence path.
- E4-UNK-014: Product production backend and garbage collection.
- E4-UNK-015: legacy deletion/retention and physical cleanup.

## 27. Facts

- E4-OBS-033: Causal and Family Result entities/tables and execution FKs differ.
- E4-OBS-034: causal Result has no stage FK; family Result has mandatory execution and stage FKs.
- E4-OBS-035: Causal and Family Artifact tables differ; family Result FK is nullable.
- E4-OBS-036: Product causal/family/export use `ArtifactStorePort`; default is local filesystem plus SHA-256.
- E4-OBS-037: causal Result/Artifact have SQL repository ports; family services directly persist ORM rows.
- E4-OBS-038: predictive retry removes owned family output rows/lineage/physical keys; causal equivalent not found.
- E4-OBS-039: Product closure reads both Product families into common Result/Artifact lineage representation.
- E4-OBS-040: legacy has four Result tables and separate Artifact/StoredObject models.
- E4-OBS-041: export bundles persist Result ID lists and object metadata separately.

## 28. Inferences

- E4-INF-013: Causal and Family Results are structural analogues with partial semantic overlap, not proven one model.
- E4-INF-014: Family Artifact ownership is broader than Result ownership because artifact-only stage output exists.
- E4-INF-015: Shared store protocol does not imply shared metadata ownership.
- E4-INF-016: Predictive retry has family-output replacement semantics; causal retry is underspecified.
- E4-INF-017: Product closure is a compatibility/read boundary, not proof of common creation ownership.
- E4-INF-018: Legacy overlaps conceptually but remains a separate persistence/lifecycle model.

## 29. Phase Conclusion

Active Product contains two Result/Artifact ownership families. Causal outputs are execution-scoped in `product_result`/`product_artifact`; Exploratory/Predictive outputs share family tables but are stage-owned and support Artifact-only outputs. They share output-field patterns, closure views, and a physical store port, but differ in FK topology, stage semantics, repository use, lineage writing, and retry cleanup. Legacy adds stage-specific Results and a separate artifact/object-store model. This is sufficient ownership evidence; it does not decide canonicalization, integration, migration, deletion, or legacy removal.

## 30. Completion Status

`COMPLETED_WITH_UNKNOWNS`. Required ownership, identity, persistence, storage, consumers, reuse, mutation, cleanup, transaction, lineage-boundary, and legacy inventories are present. No production/test/configuration/runtime state was modified.

# 42. Mandatory Explicit Answers

## A

No. Causal uses `product_result`/`product_artifact`; Family uses `product_family_result`/`product_family_artifact`.

## B

No at metadata level. They share Product `ArtifactStorePort`, not an entity/table/ownership model.

## C

Yes, as structural/semantic overlap candidates only: both are typed, JSON-backed execution outputs. Stage ownership and input references differ.

## D

Yes, as overlap candidates only: both are hashed object metadata, but family requires execution/stage and supports Result-null artifacts.

## E

Causal Result is execution-scoped; causal Artifact is Result- or execution-associated. Family Result is execution+stage scoped; Family Artifact is execution+stage scoped and may lack Result. Legacy is stage/attempt oriented.

## F

No. Causal has direct typed Result reuse; Family uses family draft/specification/lineage paths and no confirmed causal Result FK.

## G

No at metadata level; Product storage protocol is shared. Actual deployed backend is unknown. Legacy store is separate.

## H

Partially. Product DB writes are coupled to terminal state per service/UoW, with physical-store compensation; DB and physical store are not one atomic transaction. Export is independent.

## I

No proof of identical mechanisms. Closure provides a common read representation; Family writes generic lineage, while causal typed FKs/derived edges are confirmed.

## J

Causal retry behavior unresolved; Predictive retry deletes owned family outputs and physical keys; Predictive rerun/revise creates new executions and retains source rows; Exploratory equivalents are not confirmed.

# 43. Prohibited Conclusions

This inventory does not choose a canonical model, recommend table merging, define migration/deletion, decide legacy removal, or prescribe Execution/Lineage architecture.

# 44. Completeness Criteria

C1 prior phases/IDs carried forward: PASS.  
C2 causal Result: PASS.  
C3 causal Artifact: PASS.  
C4 Exploratory Result: PASS.  
C5 Predictive Result: PASS.  
C6 Family Artifact: PASS.  
C7 identity matrices: PASS.  
C8 cardinality: PASS with unknowns.  
C9 creation/coupling: PASS.  
C10 stage ownership: PASS.  
C11 semantic payload: PASS.  
C12 physical storage: PASS.  
C13 consumers: PASS.  
C14 downstream reuse: PASS with unknowns.  
C15 mutation: PASS with gaps recorded.  
C16 failure/partial: PASS.  
C17 cleanup: PASS with GC unknown.  
C18 transactions: PASS.  
C19 repositories: PASS.  
C20 lineage: PASS.  
C21 legacy: PASS.  
C22 facts/inferences/unknowns and A–J: PASS.

# 45. Final Self-Check

Performed after generation:

```text
git status --short
git diff --stat
git diff -- docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/architecture_review/03_result_artifact_ownership_inventory_result.md
```

Existing `deploy/.nfs000000000076202f00000088` change was preserved.

