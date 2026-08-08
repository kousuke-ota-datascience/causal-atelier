# 04 Lineage Responsibility Inventory Result

## 1. Metadata

- Prompt: `04_lineage_responsibility_inventory_prompt.md`
- Prior phases: Phase 01, Phase 02, Phase 03 result documents.
- Repository: `/loc0/bigbrother/repositories/causal-atelier`
- Branch: `refactor/ariadne_mvp_e4`
- HEAD: `1e94134fd117b2a5d7438d03c4acc88bbcf36905`
- Working tree at start: existing ` D deploy/.nfs000000000076202f00000088`; Phase 04 prompt untracked.
- Started at: `2026-08-08T11:10:00Z`
- Finished at: `2026-08-08T11:13:00Z`
- Phase status: `COMPLETED_WITH_UNKNOWNS`
- Method: static production source, ORM, migration, legacy source, and prior-result inspection; no runtime execution.

## 2. Executive Summary

### 2.1 Lineage Representations

| Lineage ID | Name | Type | Persistence | Primary Producer | Primary Reader |
|---|---|---|---|---|---|
| E4-LN-001 | Product typed/derived lineage | derived | typed FKs/domain relations; emitted in memory | `LineageQueryService`, Product closure | Results router, closure |
| E4-LN-002 | Product generic persisted lineage | persisted | `product_lineage_edge` | Exploratory/Predictive/split/closure services | closure, predictive lineage API, export |
| E4-LN-003 | Product closure graph | hybrid | in-memory union of derived and persisted sources | `ProductClosureService.project_lineage` | project/result lineage API, export |
| E4-LN-004 | Product export synthetic lineage | derived supplement | embedded JSON in export manifest | `_synthetic_export_lineage` | export consumer |
| E4-LN-005 | Legacy artifact lineage | persisted | `artifact_lineage` | legacy executor/causal graph API | legacy artifact-lineage API |

### 2.2 High-Level Responsibility

| Lifecycle | Typed/Derived | Generic Persisted | Read Boundary | Notes |
|---|---|---|---|---|
| Causal | YES | NO_PATH_CONFIRMED for normal processing | `LineageQueryService`, closure | typed FKs and query derivation |
| Exploratory | PARTIAL | YES | closure | service writes input/output edges |
| Predictive | PARTIAL | YES | predictive service + closure | service writes workflow/stage/result/artifact edges |
| CLI | no Product lineage confirmed | no Product edge confirmed | local manifest only | separate direct scientific path |
| Legacy | typed stage/result relations plus artifact graph | separate legacy table | legacy artifact-lineage API | not Product lineage |

The repository therefore contains a derived Product representation, a persisted generic Product representation, a hybrid closure representation, an export-embedded representation, and a separate legacy representation. These are inventory findings, not target-architecture decisions.

## 3. Lineage Node Inventory

| Node Type | Entity | Table | ID | Representation | Evidence |
|---|---|---|---|---|---|
| Project | `ProjectOrm` | `product_project` | `project_id` | closure/persisted scope | `product_closure_service.py:286-296` |
| Execution | `ExecutionOrm` | `product_execution` | `execution_id` | typed + closure/persisted | `orm_models.py:118-168` |
| Family Execution | `FamilyExecutionOrm` | `product_family_execution` | `execution_id` | closure/persisted as Execution | `product_closure_service.py:329-337` |
| Family Stage Execution | `FamilyStageExecutionOrm` | `product_family_stage_execution` | `stage_execution_id` | persisted FK; not a closure node in current builder | `orm_models.py:474-493` |
| Result | `ResultOrm` / `FamilyResultOrm` | `product_result` / `product_family_result` | `result_id` | typed + closure/persisted | `product_closure_service.py:350-356` |
| Artifact | `ArtifactOrm` / `FamilyArtifactOrm` | Product artifact tables | `artifact_id` | typed + closure/persisted | `product_closure_service.py:358-364` |
| DatasetVersion | `DatasetVersionOrm` | `product_dataset_version` | `dataset_version_id` | typed + closure | `orm_models.py:93-116`; closure |
| GraphVersion | `GraphVersionOrm` | `product_graph_version` | `graph_version_id` | typed + closure | `orm_models.py:206-238` |
| AnalysisView | `AnalysisViewOrm` | Product analysis view table | `analysis_view_id` | closure/persisted input edges | `exploratory_service.py:273-278` |
| AnalysisSpecification | `AnalysisSpecificationOrm` | Product specification table | `analysis_specification_id` | closure/persisted input edges | `product_closure_service.py:318-324` |
| ResearchContextVersion | Product ORM | Product context table | context ID | closure/persisted input edges | `predictive_workflow_service.py:229-257` |
| Annotation | `WorkspaceAnnotationOrm` / legacy annotation | Product annotation tables | annotation ID | closure/persisted | `product_closure_service.py:375-383,497-505` |
| Legacy Artifact | legacy `Artifact` | `artifact` | `id` | legacy persisted | `legacy/domain/metadata.py:789-855` |
| Legacy StageAttempt | legacy stage model | `stage_attempt` | `id` | typed legacy ownership | `legacy/domain/metadata.py:720-785` |

Generic node identity is `source_type + source_id` or `target_type + target_id`; the ORM does not use FKs to each typed target. Closure nodes use `(node_type, entity_id)`; the causal lineage service separately de-duplicates nodes by entity ID only. No source-wide UUID namespace invariant was found.

## 4. Edge Kind Inventory

| Edge Kind | Source → Target | Representation | Producer | Evidence |
|---|---|---|---|---|
| USED_INPUT | DatasetVersion/AnalysisView/Specification/Context → Execution or AnalysisView | typed-derived and persisted | closure derivation; family services | closure; `exploratory_service.py:273-278`; `predictive_workflow_service.py:229-252` |
| GENERATED | Execution → Result/Artifact; Result → Artifact | typed-derived and persisted | family services; closure | `exploratory_service.py:366-400`; `predictive_workflow_service.py:395-447` |
| DERIVED_FROM | Result → GraphVersion; Execution → Execution; Artifact → Artifact | typed-derived, persisted, or closure | closure; predictive service | closure: `348-371`; predictive: `474-479` |
| REVISED_FROM | Execution → Execution; GraphVersion → GraphVersion | typed-derived/closure and persisted for predictive revise | closure; predictive submit | closure; `predictive_workflow_service.py:252-257` |
| SUPPORTED_BY | Result/Context → Annotation or specification | closure/persisted | closure/annotation service | `product_closure_service.py:321,356,375-383,497-505` |
| MOTIVATED | Result → AnalysisSpecification | persisted | Exploratory draft flow | `exploratory_service.py:445-470` |
| EVIDENCE_FOR | Artifact → Result | persisted | Predictive workflow | `predictive_workflow_service.py:456-469` |
| DOCUMENTS | Result → Specification/Dataset/View | persisted | Predictive model card | `predictive_workflow_service.py:809-827` |
| SUMMARIZES | Result → Artifact/Result | persisted | Predictive model card | `predictive_workflow_service.py:827-850` |
| USED_GRAPH | legacy Artifact → legacy Artifact | legacy persisted | legacy executor/graph API | `legacy/workers/executor.py:671-679`; `legacy/interfaces/api/routers/causal_graphs.py:261` |
| PACKAGES | legacy Artifact → legacy Artifact | legacy persisted | legacy executor | `legacy/workers/executor.py:725-735` |
| DERIVED_FROM (legacy) | legacy Artifact → legacy Artifact | legacy persisted | legacy executor | same evidence |

The exact relation vocabulary is not identical across Product closure, family services, and legacy.

## 5. Derived Lineage

### 5.1 Derived Edge Matrix

| Relation | Source fact | Derivation symbol | Consumer | Evidence |
|---|---|---|---|---|
| Execution → Result | Result.execution_id | `LineageQueryService.add_result_chain`; closure `edge` | Result lineage/API, closure | `lineage_query_service.py:109-130`; closure `350-356` |
| Result → Artifact | Artifact.result_id/execution_id | `add_artifacts`; closure artifact loop | Result lineage/API, closure | `lineage_query_service.py:51-70`; closure `358-364` |
| DatasetVersion → Execution | Execution.dataset_version_id | `add_dataset`; closure | lineage/API, closure | `lineage_query_service.py:79-101`; closure `329-343` |
| Artifact → DatasetVersion | DatasetVersion.source_artifact_id | `add_dataset` | causal lineage/API | `lineage_query_service.py:91-101` |
| Result → Execution | Execution.input_result_id | `add_result_chain` | causal lineage/API, closure | `lineage_query_service.py:158-163`; closure `342-343` |
| Result → GraphVersion | GraphVersion.source_result_id | `add_graph_chain`; closure | causal lineage/API, closure | `lineage_query_service.py:175-188`; closure `368-369` |
| GraphVersion → Execution | Execution.input_graph_version_id | `add_graph_chain` | causal lineage/API, closure | `lineage_query_service.py:163-188`; closure `340-341` |
| Execution → Execution | revision context/base ID | revision handling | causal lineage/API, closure | `lineage_query_service.py:134-145`; closure `344-349` |
| DatasetVersion → AnalysisView | AnalysisView.source_dataset_version_id | closure | project lineage | closure `300-309` |
| GraphVersion → GraphVersion | parent_graph_version_id | closure | project lineage | closure `370-371` |
| Result/GraphVersion → Annotation | annotation target FKs | closure | project lineage | closure `375-383` |

### 5.2 Derived Lineage Responsibility

Typed/derived lineage is generated by read services, not by a generic lineage repository. Causal `LineageQueryService` traverses only Product causal UoW relationships. Product closure independently reconstructs a project-wide graph from both causal and family ORM rows. These two derived readers are not the same traversal implementation.

## 6. Persisted Generic Lineage

### 6.1 Schema

`LineageEdgeOrm` maps to `product_lineage_edge`. Columns are UUID-like `lineage_edge_id`, project FK, source/target type and ID strings, relation type, evidence JSON, creator, and timestamp. Migration creates the table and a project index. There are no source/target FKs.

Evidence: `src/ariadne/product/persistence/orm_models.py:542-557`; `product_migrations/versions/20260807_product_0004_enh_e3_workspace.py:151-164`.

### 6.2 Identity / Constraints

The unique key is `(source_type, source_id, relation_type, target_type, target_id)`; no project_id is included in that unique constraint. The domain `LineageEdge` validates same-project source/target and non-empty references, while closure API calls `_assert_resource_project`. No cascade behavior for target entities exists; only the project FK is restrictive. Evidence: `domain/lineage.py:23-39`; ORM/migration above.

### 6.3 Producers

| Producer ID | Lifecycle | Operation | Edge | Transaction | Evidence |
|---|---|---|---|---|---|
| E4-LP-001 | Exploratory | view/submit/process/draft | USED_INPUT, GENERATED, MOTIVATED | same service session commit | `exploratory_service.py:159-161,273-278,366-400,445-470,534-545` |
| E4-LP-002 | Predictive | submit/process/model-card | USED_INPUT, GENERATED, DERIVED_FROM, EVIDENCE_FOR, DOCUMENTS, SUMMARIZES | same workflow session commit | `predictive_workflow_service.py:229-257,395-484,775-850,1076-1094` |
| E4-LP-003 | Predictive split | split validation | USED_INPUT, GENERATED | split session commit | `predictive_split_service.py:198-227,262-287` |
| E4-LP-004 | Product closure API | manual lineage link | caller-supplied relation | direct service session commit | `product_closure_service.py:432-467` |
| E4-LP-005 | Product closure annotation | selected/rejected annotation | decision relation | same annotation session commit | `product_closure_service.py:497-505` |

No `LineageEdgeOrm` write was found in `ExecutionProcessor`, causal `ExecutionService`, graph-version creation, or Product causal Result/Artifact persistence.

### 6.4 Readers

| Reader | Query | Purpose | Evidence |
|---|---|---|---|
| Product closure | select all project edges | union into project graph | `product_closure_service.py:383-391` |
| Product closure result | same project edge list, then connected traversal | result subgraph | `product_closure_service.py:395-410` |
| Predictive service | edges with source/target IDs in owned execution/result/artifact IDs | execution lineage endpoint | `predictive_workflow_service.py:593-610` |
| Predictive retry | edges touching owned result/artifact IDs | cleanup | `predictive_workflow_service.py:639-650` |
| Export | project edges filtered to selected result IDs | manifest lineage references | `product_closure_service.py:583-607` |

## 7. Causal Lineage

### 7.1 Typed Relationships

Causal typed relationships are Result.execution_id, Execution.input_result_id, Execution.input_graph_version_id, GraphVersion.source_result_id, DatasetVersion.source_artifact_id, and Artifact.result_id/execution_id. They are converted to edges by `LineageQueryService` and Product closure.

### 7.2 Generic Writes

**NO_PATH_CONFIRMED** for normal Causal Execution processing. Static search found no `LineageEdgeOrm` construction in `ExecutionProcessor`, causal execution service, Result repository, Artifact repository, or graph-version service. The generic table can nevertheless receive API-supplied links.

This resolves Phase 03 `E4-UNK-013` as `RESOLVED_IN_PHASE_04` for the normal causal-processing question; it does not prove that no external caller ever writes a causal edge.

### 7.3 Generic Reads

Causal generic edges are read by Product closure and export when present. The dedicated `LineageQueryService` does not query `product_lineage_edge`; it derives from causal UoW repositories.

### 7.4 Mutation Semantics

Causal retry mutates execution state but no generic lineage cleanup/write path is confirmed. Causal revision lineage is derived from `revision_context.base_execution_id` in the dedicated and closure readers; a normal causal processor generic edge is not confirmed.

### 7.5 Evidence

`src/ariadne/interfaces/worker/execution_processor.py:109-178`; `src/ariadne/product/application/execution_service.py:89-213,246-270,317-365`; `src/ariadne/product/application/graph_version_service.py:80-125`; `src/ariadne/product/application/lineage_query_service.py:109-188`.

## 8. Exploratory Lineage

Exploratory submission writes DatasetVersion/AnalysisView→Execution edges. Successful processing writes Execution→Result and Result→Artifact. Analysis-view fixing and analysis-draft creation add further edges, including MOTIVATED. All writes call `_add_lineage`, construct `LineageEdgeOrm`, and commit in the surrounding session. Exploratory has no independent typed-generic synchronization mechanism. Evidence: `exploratory_service.py:159-161,273-278,366-400,445-470,534-545`.

## 9. Predictive Lineage

Predictive submission writes input and revision/derived edges. Processing writes Execution→Result, Result/Execution→Artifact, Artifact→Result evidence, cross-stage Artifact→Artifact derivation, and model-card relations. Split validation writes input and generated-artifact edges. `list_lineage` reads persisted rows. Retry deletes edges touching owned output IDs; rerun/revise creates new persisted input/revision edges. Evidence: `predictive_workflow_service.py:229-257,395-484,593-676,678-718,775-850,1076-1094`; `predictive_split_service.py:198-227,262-287`.

## 10. Closure / Traversal

### 10.1 Algorithm

Product closure builds dictionaries of nodes and edges by scanning project resources. `result_lineage` computes connected closure by repeated edge scans until no new IDs are added. It has no explicit depth limit or cycle check in this method. Dedicated causal `LineageQueryService` uses recursive functions with depth 32, visited/processing sets, edge de-duplication, project-boundary checks, and cycle errors.

### 10.2 Derived Sources

Closure derives edges from typed Product columns and service-owned resource relations: datasets/views/specifications/contexts, execution inputs, result execution IDs, artifact result/execution IDs, graph source/parent IDs, annotations, and revision context.

### 10.3 Persisted Sources

Closure reads all `LineageEdgeOrm` rows for the project. Predictive service reads persisted edges only for an execution-owned ID set. Export reads persisted rows related to selected results and adds synthetic derived references.

### 10.4 Merge / Deduplication

Closure edge key is `(source_type, source_id, relation, target_type, target_id)`; derived edges are inserted first, explicit persisted edges later, so an identical explicit key overwrites the derived dictionary value and marks `explicit=true`. This is a deterministic overwrite, not a documented conflict detector. Nodes use `(node_type, entity_id)`. Export does not show a general edge deduplication step for synthetic plus explicit lists.

Evidence: `product_closure_service.py:273-296,350-391,583-607`.

## 11. Duplicate Semantic Edge Analysis

| Relation | Typed | Persisted | Both possible | Both produced | Dedup/conflict |
|---|---|---|---|---|---|
| Execution → Result | yes | yes for Family; manual possible | yes | Family yes; causal generic no path | closure key overwrite |
| Result → Artifact | yes | yes for Family; manual possible | yes | Family yes; causal generic no path | closure key overwrite |
| Dataset/View → Execution | yes | yes for Family | yes | Family yes | closure key overwrite |
| Result → GraphVersion | yes | generic possible | yes | typed confirmed; generic normal producer no | no explicit conflict check |
| Execution → Execution revise | derived from revision context | yes Predictive | yes | Predictive yes | closure key overwrite |
| Artifact → Artifact | no Product FK equivalent for stage chain | yes Predictive | no typed duplicate confirmed | Predictive yes | unique tuple |
| Annotation decision → Annotation | target relation derived | yes on selected/rejected | yes | closure and annotation service | closure key overwrite |

“Both possible” is not the same as “both written by the same operation.” Causal normal execution does not establish the latter.

## 12. Current Source-of-Truth Classification

| Semantic relation | Classification | Actual read source | Actual write source |
|---|---|---|---|
| Causal input Result → Execution | TYPED_RELATION_AUTHORITATIVE_IN_CODE | causal UoW/closure | causal Execution FK |
| Causal Result → Artifact | TYPED_RELATION_AUTHORITATIVE_IN_CODE | causal UoW/closure | artifact/result FKs |
| Causal Result → GraphVersion | TYPED_RELATION_AUTHORITATIVE_IN_CODE | graph/result FKs | graph service |
| Family input/output edges | DUAL_SOURCE | closure can derive and read explicit | family services write explicit; closure derives |
| Predictive stage artifact chain | PERSISTED_EDGE_AUTHORITATIVE_IN_CODE | predictive list/closure | predictive service |
| Manual cross-resource links | PERSISTED_EDGE_AUTHORITATIVE_IN_CODE | closure/export | closure API |
| Legacy Artifact lineage | PERSISTED_EDGE_AUTHORITATIVE_IN_CODE | legacy artifact endpoint | legacy executor/API |

These classifications describe current code paths, not architectural authority recommendations.

## 13. Reconstructability

| Persisted edge | Other facts | Classification | Unique information? |
|---|---|---|---|
| Family Execution→Result | family Result.execution_id | DERIVED_WITH_PERSISTED_SUPPLEMENT | edge itself reconstructable; evidence/stage context may not be identical |
| Family Result→Artifact | FamilyArtifact.result_id | DERIVED_WITH_PERSISTED_SUPPLEMENT | edge reconstructable; evidence hash/context may be richer |
| Predictive Artifact→Artifact | no equivalent typed FK for stage chain | PERSISTED_EDGE_AUTHORITATIVE_IN_CODE | yes, source-stage relationship |
| Predictive Result→Result SUMMARIZES | result payload/type alone | PERSISTED_EDGE_AUTHORITATIVE_IN_CODE | relation not typed |
| Manual MOTIVATED/DOCUMENTS/SUPPORTED_BY | generic edge payload | PERSISTED_EDGE_AUTHORITATIVE_IN_CODE | yes |
| Causal normal typed edges | typed FK fields | TYPED_RELATION_AUTHORITATIVE_IN_CODE | generic edge not required |

## 14. Reverse Reconstructability

| Derived relation | Persisted equivalent | Guaranteed write? |
|---|---|---|
| Causal Execution→Result | generic edge | no |
| Causal Result→Artifact | generic edge | no |
| Causal Result→GraphVersion | generic edge | no |
| Family Execution→Result | generic edge | yes for normal family processing, but not every closure-derived edge |
| Family Result→Artifact | generic edge | yes when service creates Result-linked artifact |
| Dataset/AnalysisView→Family Execution | generic edge | yes in inspected submit paths |
| Closure revision edge | generic edge | Predictive yes; Causal generic no |
| Dedicated causal traversal edges | persisted generic table | no |

## 15. Consistency / Invariant Enforcement

| Invariant | Enforcement | Scope |
|---|---|---|
| source/target same Product project | domain validation and closure resource checks | generic API/domain |
| non-empty/non-self edge | domain/API validation | generic API |
| generic edge tuple uniqueness | DB unique constraint | Product table |
| Product resource existence | closure `_assert_resource_project` for manual links | manual API |
| typed FK existence | DB FKs with restrictive deletes | causal/family typed relations |
| generic edge target existence | no DB FK; only producer/API checks | not globally enforced |
| traversal project boundary | dedicated causal service checks; closure role/project scope | readers |
| cycle/depth | causal service; closure connected scan has no equivalent explicit cycle check | readers |

No invariant compares a typed relation against a persisted generic edge or detects stale/duplicate semantic relations across representations.

## 16. Conflict Semantics

- Identical generic edge insertion: DB uniqueness causes `IntegrityError`; manual API rolls back and re-reads an existing row.
- Derived vs explicit same key in closure: explicit row overwrites dictionary value and is marked explicit.
- Different evidence for same semantic tuple: no conflict report found.
- Persisted edge referring to missing typed resource: generic table has no target FK; stale reference detection is not confirmed.
- Cross-project manual link: rejected by project checks/domain validation.

## 17. Transaction Boundaries

| Operation | Domain writes | Lineage writes | Same transaction |
|---|---|---|---|
| Causal submit/process | execution/result/artifact | no normal generic write confirmed | typed metadata in UoW |
| Exploratory submit/process | family execution/stage/result/artifact | `LineageEdgeOrm` | yes, service session |
| Predictive submit/process | family execution/stage/result/artifact | `LineageEdgeOrm` | yes, service session |
| Predictive retry | rows/stages/output cleanup | edge deletion | metadata same commit; physical cleanup after |
| Predictive rerun/revise | new execution/plan | new input/revision edges | separate operation sessions |
| Manual lineage link | none beyond edge | one generic row | direct session commit |
| Closure read/export | no domain mutation except export metadata | read/synthetic manifest | export transaction separate |

## 18. Failure Semantics

Family lineage writes are inside the same DB transaction as the associated service operation; a failed commit rolls back metadata and physical artifact compensation where applicable. Causal typed relations are committed with the relevant Product UoW. Generic persisted edges have no independent retry/outbox mechanism found. A persisted generic edge can therefore be absent even when a typed relation exists, by design of the current code paths; stale generic edges are not globally reconciled.

## 19. Retry / Rerun / Revise

### 19.1 Retry

Predictive retry deletes edges touching owned Result/Artifact IDs with the owned output rows, then deletes physical keys. Causal retry does not show generic-edge cleanup; Exploratory retry not confirmed.

### 19.2 Rerun

Predictive rerun creates a new execution and new persisted input edges; source edges remain. Causal rerun is typed/derived through new execution context; no generic write confirmed.

### 19.3 Revise

Predictive revise writes a persisted REVISED_FROM/DERIVED_FROM edge. Causal dedicated/closure readers derive revision from `revision_context`; generic write not confirmed. No Exploratory revise path found.

## 20. Deletion / Cleanup

| Trigger | Lineage behavior | Mechanism |
|---|---|---|
| Predictive retry | delete owned generic edges | explicit query/delete |
| Predictive source rerun/revise | source lineage retained | new execution |
| Product project/resource deletion | no lineage-specific cascade path confirmed | project FK restrictive |
| Manual edge duplicate | retain existing row | unique constraint + re-read |
| Legacy artifact lifecycle | ArtifactLineage rows not shown deleted by API | legacy cleanup unresolved |

## 21. Causal / Family Parity

| Relation | Causal | Exploratory | Predictive | Same mechanism |
|---|---|---|---|---|
| input dataset/view | typed/derived | persisted + closure-derived | persisted + closure-derived | no |
| Execution→Result | typed/derived | persisted + derived | persisted + derived | no |
| Result→Artifact | typed/derived | persisted + derived | persisted + derived | no |
| stage chain | no persistent Product stage lineage confirmed | limited family stage ownership | persisted Artifact→Artifact | no |
| revise | derived revision context | not confirmed | persisted revision edge | no |
| retry cleanup | no generic cleanup path | not confirmed | explicit cleanup | no |

## 22. Lineage API

### Endpoints

Product causal Result lineage: `GET /results/{result_id}/lineage`. Product closure: project lineage, result lineage, and POST lineage-links. Predictive execution lineage: `GET /projects/{project_id}/executions/{execution_id}/lineage`. Legacy artifact lineage: `GET /artifacts/{artifact_id}/lineage`.

### Input

Result ID for dedicated causal lineage; project/user scope and result ID for closure; caller-supplied source/target types/IDs/relation/evidence for manual links; execution ID for predictive lineage.

### Read Sources

Dedicated causal endpoint reads typed UoW repositories. Closure reads typed Product tables plus `product_lineage_edge`. Predictive endpoint reads `product_lineage_edge`. Legacy reads `artifact_lineage`.

### Output

Dedicated API emits nodes and undirected-shaped `from_id/to_id` edge pairs with relation inferred from node types. Closure emits typed source/target IDs, relation, explicit flag, and evidence. Predictive emits persisted edge rows.

### Traversal

Dedicated causal traversal recursively follows upstream result/graph/revision relationships with depth/cycle checks. Closure result traversal repeatedly expands connected IDs over the full project edge list. No pagination was found in the inspected paths.

## 23. UI Consumption

The frontend requests predictive execution lineage and causal result lineage through Product routes; Product closure APIs provide project/result lineage and downloads/exports. UI-facing code receives representations from different service boundaries; a common UI response does not prove a common source of truth.

Evidence: `frontend/app.js` predictive execution detail requests; `src/ariadne/interfaces/web_api/routers/results.py:141-180`; `routers/product_closure.py:138-158`.

## 24. Export / Closure Consumption

Product export gathers selected causal/family artifacts, selected explicit generic edges, and synthetic derived references from Result execution/dataset/context/view/specification fields. The manifest stores lineage references as JSON inside ExportBundle metadata/physical object. This is a snapshot, not a live lineage query.

Evidence: `product_closure_service.py:570-631,853-880`.

## 25. Legacy Lineage

### Representation

Legacy uses `ArtifactLineage`, a persisted pair table with downstream/upstream Artifact IDs and `relationship_type`. It is distinct from Product `LineageEdgeOrm`.

### Node Identity

Legacy uses Artifact UUID `id`; edge identity is the pair plus relationship type. No generic node-type discriminator is present.

### Edge Identity

Composite primary key: downstream artifact, upstream artifact, relationship type. Evidence: `legacy/domain/metadata.py:829-837`.

### Producers

Legacy executor writes DERIVED_FROM, USED_GRAPH, and PACKAGES edges; legacy causal-graph API writes artifact lineage. Evidence: `legacy/workers/executor.py:671-679,725-735`; `legacy/interfaces/api/routers/causal_graphs.py:261`.

### Consumers

Legacy execution router queries upstream/downstream ArtifactLineage rows and returns relationship type and artifact details. Evidence: `legacy/interfaces/api/routers/executions.py:283-325`.

### Cleanup

No complete lineage deletion/retention path was confirmed; legacy Artifact has `deleted_at`, but edge cleanup semantics remain unresolved.

## 26. Product / Legacy Comparison

| Dimension | Product | Legacy | Classification |
|---|---|---|---|
| Generic lineage | `product_lineage_edge`, typed node IDs | no generic node-type table | structurally distinct |
| Artifact lineage | Result/Execution FKs plus generic edges | `artifact_lineage` pair table | partially analogous |
| Producers | Product family/closure services | legacy executor/API | distinct |
| Readers | closure, Product APIs, predictive API | legacy artifact API | distinct |
| Identity | type+ID generic edge | Artifact ID pair | distinct namespace rules |
| Cleanup | predictive retry cleanup confirmed | full cleanup unknown | not at parity |
| Transaction | service/session commits | legacy worker/API sessions | lifecycle-specific |

## 27. Lineage Concept Inventory

### 27.1 Distinct lineage representations

5: E4-LN-001 through E4-LN-005.

### 27.2 Distinct physical lineage tables

2: Product `product_lineage_edge`; legacy `artifact_lineage`. Export lineage is embedded JSON, not a separate lineage table.

### 27.3 Distinct edge-generation mechanisms

At least 6: typed-FK readers, closure derivation, Exploratory writer, Predictive writer, closure/manual writer, legacy ArtifactLineage writers.

### 27.4 Distinct read/traversal mechanisms

At least 5: causal `LineageQueryService`, Product closure traversal, Predictive persisted-edge reader, export snapshot builder, legacy artifact-lineage reader.

### 27.5 Relations represented more than once

Execution→Result, Result→Artifact, input Dataset/View→Execution, revision, and annotation-related relations can occur in typed-derived and persisted/closure representations.

### 27.6 Relations represented only by persisted generic lineage

Predictive stage Artifact→Artifact DERIVED_FROM, Result→Result SUMMARIZES, Result→Artifact DOCUMENTS/SUMMARIZES/EVIDENCE_FOR, and manual MOTIVATED/SELECTED/REJECTED links have no equivalent typed FK confirmed.

### 27.7 Relations represented only by typed relationships

Causal normal input Result→Execution, Result→GraphVersion, Artifact→DatasetVersion, and causal revision context are typed/derived in the inspected normal paths; generic materialization is not guaranteed.

## 28. Prior Unknown Carry-forward

| ID | Status | Phase 04 evidence | Notes |
|---|---|---|---|
| E4-UNK-013 | RESOLVED_IN_PHASE_04 | no generic writer in causal processor/service/repositories; generic API writer is separate | normal causal processing: NO_PATH_CONFIRMED |
| E4-UNK-009 | remains open | retry cleanup search confirms predictive only | causal retry result/edge behavior unresolved |
| E4-UNK-012 | remains open | family writers/readers identified | full artifact reuse outside inspected paths unresolved |
| E4-UNK-015 | remains open | legacy reader/writers found | deletion/retention not complete |
| E4-UNK-014 | remains open | no runtime backend/GC evidence | deployment state prohibited |

## 29. New Unresolved Items

| ID | Question | Confirmed facts | Why unresolved | Additional evidence |
|---|---|---|---|---|
| E4-UNK-016 | Can external/manual generic edges use causal IDs in production? | closure API accepts generic resource types and IDs | no runtime caller/config evidence | route invocation/runtime audit |
| E4-UNK-017 | Are all closure derived edges intentionally duplicated by family writers? | same keys can be derived and persisted | no explicit semantic policy | design/history or tests |
| E4-UNK-018 | Is explicit-over-derived overwrite intended precedence? | dict assignment gives explicit overwrite | no stated policy/conflict test | design source/tests |
| E4-UNK-019 | Are generic Product edges validated against all typed resources after creation? | no target FKs; producer checks vary | no reconciliation job found | full worker/job inventory/runtime |
| E4-UNK-020 | Does legacy delete ArtifactLineage rows on artifact cleanup? | deleted_at exists; API read exists | full delete path not found | legacy retention/job source |
| E4-UNK-021 | Does dedicated causal lineage intentionally exclude generic family/closure edges? | dedicated service uses causal UoW only | ownership boundary not documented in source | API contract/history |
| E4-UNK-022 | Are Product export synthetic edges deduplicated against explicit references? | both lists are assembled | no general dedup step found | export tests/runtime |

## 30. Facts

- E4-OBS-042: Product has typed/derived lineage logic in dedicated causal and closure readers.
- E4-OBS-043: Product has `LineageEdgeOrm` / `product_lineage_edge` with type+ID endpoints and tuple uniqueness.
- E4-OBS-044: Exploratory writes generic edges for inputs, outputs, and draft motivation.
- E4-OBS-045: Predictive writes generic input/output/revision/stage/model-card/split edges.
- E4-OBS-046: Product closure reads both typed-derived resources and all project generic edges.
- E4-OBS-047: Closure dedup key is typed endpoint/relation tuple; later explicit edge overwrites earlier derived value.
- E4-OBS-048: Normal Causal processor/result/artifact paths contain no confirmed generic edge write.
- E4-OBS-049: Predictive retry deletes generic edges touching owned Result/Artifact IDs.
- E4-OBS-050: Legacy uses separate `artifact_lineage` with artifact-pair identity.
- E4-OBS-051: Product export includes explicit lineage references plus synthetic derived references.

## 31. Inferences

- E4-INF-019: Active Product uses multiple lineage production/read mechanisms rather than one shared writer.
- E4-INF-020: Product closure is hybrid because it combines typed-derived and persisted generic edges.
- E4-INF-021: Family lineage is more generic-edge-driven than causal lineage in normal processing.
- E4-INF-022: Generic persisted lineage carries relations not recoverable from the typed Product schema.
- E4-INF-023: Same semantic edge can be represented twice, but current code has overwrite/dedup behavior rather than cross-source consistency validation.
- E4-INF-024: Product and legacy lineage are conceptually overlapping but structurally distinct.
- E4-INF-025: Export lineage is a snapshot representation and can have different duplicate/consistency behavior from live closure.

## 32. Mandatory Explicit Answers

A–L are answered below with evidence and fact/inference distinctions.

## 33. Phase Conclusion

1. Confirmed Lineage Representations: 5.
2. Physical lineage-specific tables: 2.
3. Active Product uses derived lineage: YES.
4. Active Product uses persisted generic lineage: YES.
5. Normal Causal processing writes persisted generic lineage: NO_PATH_CONFIRMED.
6. Family writes persisted generic lineage: YES for Exploratory and Predictive paths inspected.
7. Some semantic relations have dual representation: YES.
8. Explicit cross-representation consistency mechanism: NO_MECHANISM_CONFIRMED; closure has deterministic key overwrite.
9. Persisted edges not reconstructable from typed relations: YES, including Predictive stage Artifact chain and model-card/manual relations.
10. Product closure/API uses multiple sources: YES.
11. Product and legacy lineage are structurally distinct: YES.
12. New unresolved items: 7 (E4-UNK-016..022); E4-UNK-013 resolved.
13. Evidence is sufficient to proceed to legacy reachability and target-architecture decision preparation: YES as an evidence handoff, without deciding target architecture.

## 34. Completion Status

`COMPLETED_WITH_UNKNOWNS`.

# 48. Mandatory Explicit Answers

## A

**YES.** Active Product has typed/derived lineage through Result/Execution/Artifact/Graph/Dataset FKs and reader derivation. Evidence: E4-OBS-042; `lineage_query_service.py:51-188`, closure `300-371`.

## B

**YES.** `LineageEdgeOrm` and Product family/closure writers persist generic edges. Evidence: E4-OBS-043..045.

## C

**NO_PATH_CONFIRMED** for normal Causal Execution processing. No `LineageEdgeOrm` write was found in `ExecutionProcessor`, causal execution service, or causal repositories. Manual closure API can write caller-supplied edges, which is a separate path.

## D

**YES for Exploratory and Predictive.** Exploratory writes input/output/motivation edges; Predictive writes input/output/revision/stage/model-card edges; split writes input/generated edges. Evidence: E4-OBS-044..045.

## E

**YES, partially.** Execution→Result, Result→Artifact, and input edges can be both typed-derived and persisted for Family paths; Causal normal processing produces typed edges without guaranteed generic materialization. Evidence: E4-OBS-046..048.

## F

**NO_MECHANISM_CONFIRMED.** DB tuple uniqueness and closure key overwrite exist, but no validator/reconciler compares typed and generic edges or reports conflicting evidence. Evidence: E4-OBS-047; Section 15–16.

## G

**YES, partially.** Product closure combines derived and persisted edges; dedicated causal lineage combines only typed sources, predictive execution lineage reads persisted edges, and export combines explicit plus synthetic references. There is no single merge rule across all APIs.

## H

**PARTIALLY.** Family Execution→Result and Result→Artifact edges are often reconstructable from FKs, but Predictive stage Artifact→Artifact and model-card/manual relations are not. Evidence: Sections 13–14.

## I

**NO.** Typed/derived relations are not all materialized as generic edges; normal Causal edges are the clearest counterexample. Family materializes many but not every closure-derived relation.

## J

**NO.** Causal uses typed/derived reader logic; Exploratory/Predictive use service-owned generic writers; closure uses a hybrid builder; legacy uses a separate artifact-pair writer.

## K

**NO.** Predictive retry deletes persisted output edges; predictive rerun/revise writes new edges; causal retry/revision is primarily typed/derived; Exploratory equivalents are incomplete/not confirmed. No common mechanism is established.

## L

**NO.** Legacy uses `artifact_lineage` with Artifact-pair identity and separate writers/readers, unlike Product `product_lineage_edge` and typed Product closure. This does not imply legacy deletion.

# 49. Prohibited Conclusions

This inventory does not select a canonical lineage source, recommend deleting generic/typed/legacy lineage, prescribe migration, or define target API/Execution architecture.

# 50. Completeness Criteria

C1 prior Phase 01–03 results/IDs read: PASS.  
C2 all Product lineage representations: PASS.  
C3 node inventory: PASS.  
C4 edge inventory: PASS.  
C5 derived sources/writers/readers: PASS.  
C6 generic schema/constraints: PASS.  
C7 generic producers: PASS.  
C8 Causal generic path: PASS; normal path NO_PATH_CONFIRMED.  
C9 Exploratory/ Predictive writers: PASS.  
C10 closure/traversal: PASS.  
C11 merge/dedup/conflict: PASS.  
C12 source-of-truth classification: PASS.  
C13 reconstructability: PASS with unknowns.  
C14 reverse reconstructability: PASS.  
C15 consistency/invariants: PASS.  
C16 transaction/failure: PASS.  
C17 retry/rerun/revise: PASS with lifecycle gaps.  
C18 cleanup: PASS with unknowns.  
C19 API/UI/export: PASS.  
C20 legacy comparison: PASS.  
C21 prior unknown carry-forward: PASS.  
C22 new unknowns: PASS.  
C23 facts/inferences distinction: PASS.  
C24 mandatory A–L: PASS.  
C25 prohibited conclusions respected: PASS.  
C26 static-only investigation and result-only write: PASS.

# 51. Final Self-Check

Performed after result generation:

```text
git status --short
git diff --stat
git diff -- docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/architecture_review/04_lineage_responsibility_inventory_result.md
```

Existing `deploy/.nfs000000000076202f00000088` change was preserved.

