# 05 Legacy Dependency / Reachability Matrix Result

## 1. Metadata

- Prompt: `05_legacy_dependency_reachability_matrix.md`
- Prior phases: Phase 01–04 result documents.
- Repository: `/loc0/bigbrother/repositories/causal-atelier`
- Branch: `refactor/ariadne_mvp_e4`
- HEAD: `9f2b8d9eae42f2279fb0bf6ce284bacdc7b3e899`
- Working tree at start: existing ` D deploy/.nfs000000000076202f00000088`; Phase 05 prompt untracked.
- Started at: `2026-08-08T11:16:00Z`
- Finished at: `2026-08-08T11:20:00Z`
- Phase status: `COMPLETED_WITH_UNKNOWNS`
- Method: static repository search and source/packaging/migration inspection; no imports were executed and no runtime/database/test command was run.

## 2. Executive Summary

### 2.1 Legacy Components

| ID | Component | Responsibility | Dependency Criticality | Runtime Reachability |
|---|---|---|---|---|
| E4-LG-001 | Legacy API | FastAPI control-plane routes, RBAC, datasets, executions, graphs, visualizations | STANDALONE_RUNTIME_REACHABLE (source root) | STANDALONE_RUNTIME_REACHABLE |
| E4-LG-002 | Legacy CLI | legacy pipeline/discovery/inference CLI handlers | STANDALONE_RUNTIME_REACHABLE (source entry functions) | STANDALONE_RUNTIME_REACHABLE |
| E4-LG-003 | Legacy execution/control plane | execution creation, planning, state, configuration/catalog services | STANDALONE_RUNTIME_REACHABLE (internal legacy root) | MIXED |
| E4-LG-004 | Legacy worker | outbox/claim/execute/materialize/project execution | STANDALONE_RUNTIME_REACHABLE (main symbol) | MIXED |
| E4-LG-005 | Legacy pipeline | planning, validation, stage strategy, manifests, ETL orchestration | SHARED_CAPABILITY_DEPENDENCY / STANDALONE | MIXED |
| E4-LG-006 | Legacy discovery | providers, discovery service, backend, artifact writer | SHARED_CAPABILITY_DEPENDENCY / STANDALONE | MIXED |
| E4-LG-007 | Legacy inference/analysis-ready | graph/effect estimation orchestration and validation | SHARED_CAPABILITY_DEPENDENCY / STANDALONE | MIXED |
| E4-LG-008 | Legacy domain/persistence | legacy ORM metadata and physical schema model | MIGRATION_HISTORY_DEPENDENCY_ONLY | MIGRATION_HISTORY_ONLY |
| E4-LG-009 | Legacy artifact/materialization/projection | StoredObject, Artifact, artifact storage, ETL/materialized views | STANDALONE / MIGRATION_HISTORY | MIXED |
| E4-LG-010 | Legacy lineage | ArtifactLineage production and API read | STANDALONE / MIGRATION_HISTORY | MIXED |
| E4-LG-011 | Legacy infrastructure/contracts | old settings, DB, auth, data-query, tracking, ports | STANDALONE support surface | MIXED |
| E4-LG-012 | Legacy ETL/data catalog | CompleteJourney extraction/transform/load and logical table registry | SHARED_CAPABILITY_DEPENDENCY / STANDALONE | MIXED |

“Runtime reachable” above means a source-level root or callable exists, not that current repository-managed deployment invokes it.

### 2.2 Overall Dependency Summary

| Dependency Category | Count | Major Components |
|---|---:|---|
| Product/shared → legacy production import/call | 0 confirmed | Product/web API architecture checks explicitly exclude it |
| Legacy → shared scientific code | 5 capability families | causal, preprocessing, shared validation/constants, plus old ETL namespace references |
| Product persistence → legacy physical tables | 0 confirmed | Product ORM/migrations target Product tables |
| Product migration chain → legacy migration chain | 0 confirmed | Compose uses `product_migrations` |
| Repository-managed legacy deployment | 0 confirmed | Docker/Compose/package excludes legacy |
| Test/documentation references | several textual/history references | architecture tests, archived legacy tests, old requirements |
| Current package entry points exposing legacy | 0 confirmed | only Product API/worker/CLI scripts |

## 3. Legacy Component Inventory

| Component | Modules | Responsibility | Persistence | Runtime Surface | Evidence |
|---|---|---|---|---|---|
| E4-LG-001 API | `legacy/interfaces/api/**` | FastAPI control plane and routes | legacy DB/session | `app`, `create_app`, `main` | `legacy/interfaces/api/app.py:30-47,152-225` |
| E4-LG-002 CLI | `legacy/interfaces/cli/**` | pipeline/discovery/inference argument adapters | files/legacy services | `main` functions | `legacy/interfaces/cli/pipeline.py:120-184`; discovery/inference main symbols |
| E4-LG-003 execution/control | `legacy/application/run_execution/**`, control/config/data catalog | create/retry/run orchestration | legacy Execution/Stage/Attempt | API and worker consumers | `legacy/application/run_execution/services.py:68-169,773-865` |
| E4-LG-004 worker | `legacy/workers/**` | outbox claim, stage execution, state, materialization/projection | legacy state/events/artifacts | `workers/main.py:26-50` | executor/state/materialization/projection modules |
| E4-LG-005 pipeline | `legacy/application/pipeline/**` | plans, validation, stage strategies, manifests, ETL dispatch | manifest/artifact records | CLI/worker internal | pipeline module imports and `execution.py` |
| E4-LG-006 discovery | `legacy/application/discovery/**` | input providers, algorithms, artifact writer | DiscoveryResult/artifacts | pipeline/CLI/worker | discovery factory/service/adapters |
| E4-LG-007 inference | `legacy/application/analysis_ready.py` and pipeline inference | graph/effect estimation orchestration | EdgeWeight/TreatmentEffect results | worker/API internal | `legacy/application/analysis_ready.py:26-220` |
| E4-LG-008 domain/persistence | `legacy/domain/metadata.py` | SQLAlchemy legacy metadata schema | many legacy tables | legacy services | `metadata.py:98-855,1010-1285` |
| E4-LG-009 artifact/materialization | legacy artifact ports/workers | physical objects and projections | Artifact/StoredObject | worker/API | `legacy/workers/materialization.py`; metadata |
| E4-LG-010 lineage | ArtifactLineage + route/writers | artifact upstream/downstream relations | `artifact_lineage` | legacy artifact route | `metadata.py:829-837`; legacy executor/router |
| E4-LG-011 infrastructure/contracts | old `application.ports`, infrastructure imports | DB/settings/auth/tracking/query/store | legacy DB/config | old API/worker | legacy import sites |
| E4-LG-012 ETL/catalog | `legacy/etl/**`, catalog services | dataset registry and CompleteJourney transformations | legacy dataset/table metadata | pipeline/discovery | legacy ETL imports |

## 4. Product / Shared → Legacy Dependencies

| DEP ID | Source | Target | Type | Runtime Reachability | Evidence |
|---|---|---|---|---|---|
| — | Product application/domain/interfaces | `ariadne.legacy` | NONE_CONFIRMED | not established | `tests/product/test_architecture.py:23-31` statically checks no such imports; repository-wide search found no production import |
| — | Product worker/API | legacy API/worker | NONE_CONFIRMED | not established | `pyproject.toml:19-33`; `compose.yaml:18-47`; Product worker branches are Product services |
| — | Product ORM/migrations | legacy tables | NONE_CONFIRMED | not established | `product_migrations/env.py:1-18`; Product ORM FKs target `product_*` tables |

The result is **NONE_CONFIRMED**, not proof that an external process cannot call a legacy root.

## 5. Legacy → Product / Shared Dependencies

| DEP ID | Source | Target | Type | Purpose | Evidence |
|---|---|---|---|---|---|
| E4-DEP-001 | legacy discovery adapters/providers | `ariadne.causal.discovery.*` | SCIENTIFIC_CAPABILITY | CausalDiscovery/config/diagnostics/reporting | `legacy/application/discovery/adapters/backend.py:7-9`; artifact writer imports |
| E4-DEP-002 | legacy analysis-ready | `ariadne.causal.discovery.algorithms` | SCIENTIFIC_CAPABILITY | discovery computation | `legacy/application/analysis_ready.py:13` |
| E4-DEP-003 | legacy analysis-ready | `ariadne.causal.inference.estimators.*` | SCIENTIFIC_CAPABILITY | edge weight and treatment effect estimation | `legacy/application/analysis_ready.py:14-18` |
| E4-DEP-004 | legacy validation/CLI | `ariadne.preprocessing.*` | SCIENTIFIC_CAPABILITY | feature semantics/builders/config | legacy pipeline/CLI imports |
| E4-DEP-005 | legacy pipeline/ports | `ariadne.shared.*` | SCIENTIFIC_CAPABILITY | validation/constants/identity | `legacy/application/pipeline/strategies.py:8`; CLI imports |
| E4-DEP-006 | legacy source files | old top-level `ariadne.application/domain/infrastructure/interfaces` | IMPORT_NAMESPACE_DEPENDENCY | old control-plane implementation | e.g. `legacy/interfaces/api/app.py:17-22`; `legacy/workers/main.py:9-10` |
| E4-DEP-007 | legacy discovery/ETL | `ariadne.etl.*` | IMPORT_NAMESPACE_DEPENDENCY | data loading and CompleteJourney ETL | `legacy/application/pipeline/etl.py:7-12`; discovery providers |

E4-DEP-001..005 point to shared/product-adjacent scientific or shared modules that are present in the current tree. E4-DEP-006..007 point to namespaces for which matching current top-level paths were not found; source-level dependency is visible, executable resolution is unknown/likely unavailable without an external packaging layout.

## 6. Indirect / Re-export Dependencies

| Source | Bridge | Legacy Target | Consumer | Evidence |
|---|---|---|---|---|
| Product architecture tests | AST/import scanner | `ariadne.legacy` string | test assertion | `tests/product/test_architecture.py:23-31` |
| Product packaging | hatch exclude | `src/ariadne/legacy/**` | wheel build | `pyproject.toml:53-64` |
| Docker build | `.dockerignore` | `src/ariadne/legacy` | build context | `.dockerignore:14-24` |
| Product closure local variable names | variables named `legacy_artifacts`, `legacy_rows` | Product `ArtifactOrm`/`ResultOrm`, not `ariadne.legacy` | closure | `product_closure_service.py:357,703-706` |
| Product snapshot contract | `LEGACY_SNAPSHOT_SCHEMA_VERSION` | legacy-compatible Product snapshot string | Product Execution validation | `product/domain/execution.py:15,63-73`; ORM constraint |
| Retired test archive | excluded test directory and old imports | historical control plane | no default collection | `pyproject.toml:37`; `tests/README.md:8` |

The closure variable names and snapshot schema are compatibility terminology/data contract, not confirmed imports of the legacy package.

## 7. Scientific Capability Matrix

| Capability | Legacy | Product/Shared | Relationship | Criticality | Evidence |
|---|---|---|---|---|---|
| Causal discovery algorithms | legacy discovery adapters call `ariadne.causal.discovery` | Product scientific discovery adapter calls same causal module | SAME_IMPLEMENTATION_SHARED | ACTIVE_PRODUCT_REQUIRED | `legacy/.../backend.py:8`; `scientific/discovery/adapter.py:54` |
| Treatment-effect estimation | legacy analysis-ready imports estimator | Product scientific inference adapter imports same estimator | SAME_IMPLEMENTATION_SHARED | ACTIVE_PRODUCT_REQUIRED | `legacy/application/analysis_ready.py:14-18`; `scientific/inference/adapter.py:129-132` |
| Edge-weight estimation | legacy analysis-ready imports estimator | Product/shared estimator module exists; active adapter relationship not fully traced | SAME_IMPLEMENTATION_SHARED for implementation | SHARED_CAPABILITY_DEPENDENCY | `analysis_ready.py:14`; `causal/inference/estimators/edge_weight.py:65` |
| Feature semantics/preprocessing | legacy pipeline/CLI imports preprocessing | Product scientific/application paths use preprocessing modules | SAME_IMPLEMENTATION_SHARED / PARALLEL orchestration | ACTIVE_PRODUCT_REQUIRED | legacy imports; Product source imports |
| Validation result/severity | legacy pipeline imports shared validation | Product/shared validation uses same module | SAME_IMPLEMENTATION_SHARED | ACTIVE_PRODUCT_REQUIRED | `legacy/application/pipeline/strategies.py:8`; shared module consumers |
| CompleteJourney ETL | legacy pipeline imports old `ariadne.etl` namespace | no current Product equivalent confirmed in inspected Product runtime | LEGACY_ONLY_CONFIRMED at legacy orchestration level | NO_CONSUMER_CONFIRMED in Product | `legacy/application/pipeline/etl.py:7-12`; product runtime search |
| Legacy MLflow/tracking orchestration | legacy worker/CLI | Product current runtime excludes MLflow in package/deployment checks | LEGACY_ONLY_CONFIRMED | STANDALONE_LEGACY_ONLY | legacy executor; `test_architecture.py:47-50` |
| Product workflow orchestration | no legacy implementation used by Product | Product execution/family services | PRODUCT_ONLY_CONFIRMED | ACTIVE_PRODUCT_REQUIRED | Phase 02 evidence and Product sources |

The relationship is about implementation/module dependency, not numerical equivalence. Runtime numerical correctness was not tested.

## 8. Scientific Contract Comparison

| Capability | Input | Output | Algorithm/Library | Configuration | Semantic Differences | Evidence |
|---|---|---|---|---|---|---|
| Discovery | legacy provider/prepared frame/config | legacy DTO/artifacts/results | shared `CausalDiscovery` | legacy config/provider | orchestration/persistence contracts differ from Product adapter | legacy discovery modules; `scientific/discovery/adapter.py` |
| Treatment effect | legacy stage inputs/design | legacy result/artifact rows | shared `TreatmentEffectEstimator` | legacy design/config | legacy stage/result schema vs Product descriptor/Result schema | `analysis_ready.py`; estimator; Product scientific adapter |
| Preprocessing | legacy table/provider/config | prepared frame/features | shared preprocessing plus legacy ETL | config formats differ/unknown | legacy data catalog and Product dataset/view contracts differ | legacy pipeline; Product analysis-frame services |

## 9. Persistence Dependency

### 9.1 Legacy Models

| Model family | Table examples | Product Ref | Legacy Ref | Migration | Evidence |
|---|---|---|---|---|---|
| Legacy execution/stages/attempts | `execution`, `stage_execution`, `stage_attempt` | none confirmed | legacy services/workers | `migrations/**` | `legacy/domain/metadata.py:560-720` |
| Legacy Result families | `discovery_result`, `discovery_algorithm_result`, `edge_weight_result`, `treatment_effect_result` | none confirmed | legacy services | legacy migration chain | `metadata.py:1010-1285` |
| Legacy Artifact/Object | `artifact`, `stored_object`, `artifact_lineage` | none confirmed | legacy API/workers | legacy migration chain | `metadata.py:98-116,789-837` |
| Legacy project/config/data | `project`, `dataset_version`, configuration/table families | no FK from Product ORM confirmed | legacy API/services | legacy migrations | legacy metadata |

Product tables with similar names are separate Product ORM classes and do not establish cross-schema dependency.

### 9.2 Cross-Schema Dependencies

| Source | Target | Mechanism | Evidence |
|---|---|---|---|
| Product ORM | legacy tables | no FK/raw SQL/view/trigger confirmed | Product ORM/migration search |
| Legacy ORM | Product tables | no FK confirmed; legacy source targets unprefixed old tables | `legacy/domain/metadata.py` |
| Product migration | legacy migration | no revision dependency confirmed | `product_migrations/versions/**` and env |
| Product compatibility | legacy snapshot string | JSON/check contract, not physical FK | `product/domain/execution.py:15,63-73`; `orm_models.py:161-165` |

Answer: Product persistence dependence on legacy physical tables is **NO_PATH_CONFIRMED**.

## 10. Migration Dependency

### Product Migration Chain

Current Product migration configuration is `alembic_product.ini` → `product_migrations`; its environment target metadata is `ProductBase.metadata`. Compose migration uses `alembic -c alembic_product.ini upgrade head`. Evidence: `alembic_product.ini:1-2`; `product_migrations/env.py:1-18`; `compose.yaml:18-23`.

### Legacy Migration Chain

Legacy metadata is targeted by root `alembic.ini` → `migrations`; `migrations/env.py` imports `ariadne.infrastructure.persistence.models.Base`. Evidence: `alembic.ini:1-2`; `migrations/env.py:1-18`.

### Cross-chain Dependencies

No Product migration revision imports or depends on the legacy `migrations` revision chain. Historical documentation and archived tests refer to the old chain.

### Clean Product Schema Dependency

Product clean rebuild needs Product migration chain only according to repository configuration; no legacy table FK or Product migration revision dependency was confirmed. This is a static configuration fact, not a claim about external databases.

## 11. Legacy Runtime Roots

| Root | Definition | Repository Invocation | Reachability | Evidence |
|---|---|---|---|---|
| Legacy API | `legacy.interfaces.api.app:main/app` source symbols | no current Docker/Compose/package script | STANDALONE_RUNTIME_REACHABLE source-only | `legacy/interfaces/api/app.py:30-47,212-225` |
| Legacy worker | `legacy.workers.main:main` | no current Docker/Compose/package script | STANDALONE_RUNTIME_REACHABLE source-only | `legacy/workers/main.py:26-50` |
| Legacy pipeline CLI | `legacy.interfaces.cli.pipeline:main` | no current `project.scripts` entry | STANDALONE_RUNTIME_REACHABLE source-only | `legacy/interfaces/cli/pipeline.py:120-184` |
| Legacy discovery CLI | `legacy.interfaces.cli.discovery:main` | no current `project.scripts` entry | STANDALONE_RUNTIME_REACHABLE source-only | discovery module main |
| Legacy inference CLI | `legacy.interfaces.cli.inference:main` | no current `project.scripts` entry | STANDALONE_RUNTIME_REACHABLE source-only | inference module main |

Repository-managed active runtime instead exposes Product API/worker/CLI only: `pyproject.toml:19-33`, `Dockerfile:10-20`, `compose.yaml:18-47`.

## 12. Test Dependencies

| Test Area | Legacy Component | Type | Production Implication | Evidence |
|---|---|---|---|---|
| Product architecture tests | package path/name | static negative assertion | verifies exclusion; does not call legacy | `tests/product/test_architecture.py:23-50` |
| Product causal regression | legacy string absence | static negative assertion | verifies Product source has no legacy import | `tests/product/test_enh_e3_causal_workflow_regression.py:259-262` |
| PostgreSQL contract | legacy-named Product snapshot/table values | DB fixture/data contract | Product compatibility coverage, not legacy module import | `tests/product/test_postgres_contract.py:141-194` |
| Archived control-plane tests | old migration/imports | excluded test history | no default production implication | `tests/README.md:8`; `pyproject.toml:37` |
| Frontend contract | string exclusion list | static contract | verifies no legacy endpoint naming | `tests/product/test_frontend_contract.py:15` |

No active Product test import of `ariadne.legacy` was confirmed. Tests mention legacy strings and old schema names; textual mention is not runtime dependency.

## 13. Tooling Dependencies

No current developer/maintenance script or tool with an executable import of `ariadne.legacy` was confirmed. The repository contains old migration/test references and documentation, but no current tool entry point was found. Legacy source itself has CLI roots; those are categorized as standalone source roots, not current tooling consumers.

## 14. Packaging Dependencies

### Console Scripts

Current scripts are five Product scientific CLIs, `ariadne-api`, and `ariadne-worker`; no legacy API/CLI/worker script is listed. Evidence: `pyproject.toml:19-33`.

### Public Entry Points

No `ariadne.legacy` public entry point or plugin registry was found outside legacy source definitions.

### Package Exposure

Hatch package configuration includes `src/ariadne` but explicitly excludes `src/ariadne/legacy/**`; Docker build context also excludes the directory. Evidence: `pyproject.toml:53-64`; `.dockerignore:14-24`.

## 15. Deployment Dependencies

| Deployment Surface | Legacy Reference | Active Path | Evidence |
|---|---|---|---|
| Docker image | excluded by `.dockerignore` and wheel config | Product source copied | `.dockerignore:14-24`; `Dockerfile:10-20` |
| Compose API | no legacy command | Product uvicorn app | `compose.yaml:25-44` |
| Compose worker | no legacy command | `ariadne-worker` Product runner | `compose.yaml:46-53` |
| Compose migration | no legacy chain | Product Alembic config | `compose.yaml:18-23` |
| Frontend nginx | no legacy API route reference confirmed | Product `/api/v1` paths | deploy/frontend sources |

Repository-managed deployment invokes no legacy root in the inspected configuration.

## 16. Configuration Dependencies

| Config | Product Consumer | Legacy Consumer | Evidence |
|---|---|---|---|
| `ARIADNE_PRODUCT_DATABASE_URL` | Product migration/API/worker | none confirmed | `compose.yaml:21-22` |
| `ARIADNE_ARTIFACT_ROOT` | Product store | legacy has separate settings/store contract | Product dependencies; legacy app |
| `ARIADNE_DATABASE_URL` | no current Compose Product path | old migration/settings | architecture test exclusion; `migrations/env.py` |
| legacy YAML/config files | no Product consumer confirmed | legacy CLI/pipeline | legacy CLI/pipeline modules |
| `legacy-product-snapshot/1` | Product compatibility validation | no legacy module required | `product/domain/execution.py:15,63-73` |

## 17. Interface / Compatibility Contracts

| Contract | Location | Legacy Consumer | Product/Other Consumer | Evidence |
|---|---|---|---|---|
| legacy Product snapshot schema string | Product domain/ORM | name references prior format, consumer not confirmed | Product causal Execution validation | `product/domain/execution.py:63-73`; ORM constraints |
| legacy result/table names in Product tests | test data SQL | historical naming | Product PostgreSQL compatibility tests | `tests/product/test_postgres_contract.py:141-194` |
| old manifest aliases `run_id`/execution ID | legacy pipeline validation | legacy readers | no Product consumer confirmed | `legacy/application/pipeline/validation.py:67-72` |
| Product shared scientific DTOs | `ariadne.causal`/scientific adapters | legacy adapters | Product scientific adapter | dependency IDs E4-DEP-001..005 |

## 18. Compatibility Shims

No explicit module under a current non-legacy `interfaces/legacy_compat` path was found. Compatibility-like items are data/string contracts: Product `legacy-product-snapshot/1`, Product test values, and legacy manifest aliases. They are not confirmed code shims importing `ariadne.legacy`.

## 19. Data Format Compatibility

| Format | Legacy Writer/Reader | Product Writer/Reader | Compatibility |
|---|---|---|---|
| Legacy execution snapshot string | Product ORM/domain validates a legacy-compatible schema label | Product only in inspected path | name/contract compatibility; producer equivalence unknown |
| Legacy manifest aliases | legacy pipeline validation | no Product reader confirmed | legacy-only compatibility |
| Artifact metadata | legacy Artifact/StoredObject | Product Artifact/FamilyArtifact | conceptual overlap, distinct schemas |
| Result JSON | legacy typed Result tables | Product Result JSON payloads | conceptual overlap, no direct conversion path confirmed |
| Product export manifest | no legacy reader confirmed | Product closure/export | Product-only current format |

## 20. Responsibility Overlap

| Responsibility | Legacy | Product/Shared | Relationship | Evidence |
|---|---|---|---|---|
| execution orchestration | legacy control plane/worker | Product Execution/Family services/worker | PARALLEL_IMPLEMENTATIONS | Phase 02; legacy services |
| discovery computation | legacy adapter | Product scientific discovery adapter | SAME_IMPLEMENTATION_SHARED | E4-DEP-001 |
| treatment/edge estimation | legacy analysis-ready | Product scientific inference adapter/shared estimators | SAME_IMPLEMENTATION_SHARED | E4-DEP-002..003 |
| Result persistence | legacy typed tables | Product Result/FamilyResult | PARALLEL_IMPLEMENTATIONS | Phase 03; legacy metadata |
| Artifact storage | legacy StoredObject/ArtifactStore | Product ArtifactStorePort | PARALLEL_INTERFACES | Phase 03; legacy ports |
| lineage | legacy ArtifactLineage | Product typed/generic/closure lineage | PARALLEL_IMPLEMENTATIONS | Phase 04; legacy executor |
| API | legacy control-plane API | Product web API | PARALLEL_IMPLEMENTATIONS | API app roots |
| migration | root legacy chain | Product chain | SEPARATE_CHAINS | migration configs |

## 21. Reachability × Responsibility Matrix

| Legacy Component | Runtime | Product Import | Scientific | Test | Tooling | Migration | Packaging | External |
|---|---|---|---|---|---|---|---|---|
| E4-LG-001 API | standalone source root | no | indirect | no direct | no | legacy schema | excluded | unknown |
| E4-LG-002 CLI | standalone source root | no | shared capability | archived only | no current | no | no script | unknown |
| E4-LG-003 control plane | internal legacy root | no | orchestration | archived/history | no | legacy schema | excluded | unknown |
| E4-LG-004 worker | standalone source root | no | shared/legacy | archived/history | no current | legacy schema | excluded | unknown |
| E4-LG-005 pipeline | internal legacy root | no | shared preprocessing/ETL | archived | no current | legacy | excluded | unknown |
| E4-LG-006 discovery | internal legacy root | no direct Product import | shared causal algorithm | archived | no | legacy result schema | excluded | unknown |
| E4-LG-007 inference | internal legacy root | no direct Product import | shared estimators | archived/history | no | legacy result schema | excluded | unknown |
| E4-LG-008 domain/persistence | migration-only source | no Product FK | no | archived migration tests | Alembic old chain | yes history | excluded | unknown |
| E4-LG-009 artifacts | legacy source | no Product import | no | archived | no current | legacy tables | excluded | unknown |
| E4-LG-010 lineage | legacy source | no Product import | no | archived/history | no | legacy table | excluded | unknown |
| E4-LG-011 infrastructure | legacy source | no | shared old contracts | archived | no current | old chain | excluded | unknown |
| E4-LG-012 ETL/catalog | legacy source | no Product import | preprocessing/data capability | archived | no current | legacy data schema | excluded | unknown |

## 22. Dependency Criticality

| Legacy Component | Classification | Supporting DEP IDs | Evidence |
|---|---|---|---|
| E4-LG-001 | STANDALONE_RUNTIME_REACHABLE | none Product | legacy API root; no current deployment |
| E4-LG-002 | STANDALONE_RUNTIME_REACHABLE | E4-DEP-001,004,005 | legacy CLI roots and shared imports |
| E4-LG-003 | MIXED | E4-DEP-006 | internal old namespace imports |
| E4-LG-004 | MIXED | E4-DEP-006 | worker root plus old namespace imports |
| E4-LG-005 | SHARED_CAPABILITY_DEPENDENCY | E4-DEP-004,005,007 | shared preprocessing/validation; ETL namespace |
| E4-LG-006 | SHARED_CAPABILITY_DEPENDENCY | E4-DEP-001,004 | shared causal discovery |
| E4-LG-007 | SHARED_CAPABILITY_DEPENDENCY | E4-DEP-002,003 | shared causal estimators |
| E4-LG-008 | MIGRATION_HISTORY_DEPENDENCY_ONLY | none | root migration chain only |
| E4-LG-009 | MIXED | E4-DEP-006 | legacy storage plus old infrastructure |
| E4-LG-010 | MIGRATION_HISTORY_DEPENDENCY_ONLY | none | legacy artifact lineage table/API |
| E4-LG-011 | MIXED | E4-DEP-006 | old infrastructure namespace |
| E4-LG-012 | SHARED_CAPABILITY_DEPENDENCY | E4-DEP-004,007 | ETL/preprocessing and old namespace |

## 23. Reverse Blast Radius

| Legacy Component | Direct inbound references | Transitive areas | Evidence |
|---|---|---|---|
| E4-LG-001 API | none confirmed outside legacy | external unknown | repository-wide search; API root |
| E4-LG-002 CLI | none current package scripts | external command users unknown | pyproject scripts |
| E4-LG-003 control plane | legacy API/worker internal | legacy persistence and events | legacy imports |
| E4-LG-004 worker | legacy main/internal | execution, artifacts, lineage, tracking | worker imports |
| E4-LG-005 pipeline | legacy CLI/worker | discovery/ETL/config/artifacts | pipeline imports |
| E4-LG-006 discovery | legacy pipeline/analysis-ready | shared causal algorithms and artifacts | discovery factory/adapters |
| E4-LG-007 inference | legacy worker/analysis-ready | shared estimators and legacy Result tables | analysis-ready |
| E4-LG-008 domain | legacy services/migrations/tests archive | all legacy persistence | metadata/migrations |
| E4-LG-009 artifacts | legacy worker/API | StoredObject and lineage | metadata/worker |
| E4-LG-010 lineage | legacy worker/API/graph route | artifact graph reads | legacy lineage sources |
| E4-LG-011 infrastructure | legacy API/worker | old DB/settings/tracking | legacy import sites |
| E4-LG-012 ETL | legacy pipeline/discovery | dataset providers and preprocessing | ETL imports |

## 24. Repository-Unreferenced Components

| Component | Search performed | Runtime root | Classification | Limitation |
|---|---|---|---|---|
| E4-LG-001 API | non-legacy src/tests/deploy/packaging search | definition only | UNREFERENCED_CANDIDATE for repository-local inbound use | external invocation unknown |
| E4-LG-002 CLI | project scripts/tooling search | definition only | UNREFERENCED_CANDIDATE for repository-local invocation | external command unknown |
| E4-LG-003..012 | non-legacy import/search plus packaging/deploy search | internal references only | no external repository-local consumer confirmed | internal legacy edges are not inbound active Product edges |

This classification is not a deletion recommendation.

## 25. External Consumer Boundary

Repository-local static evidence can establish source definitions, internal imports, package exclusions, migration configuration, and absence of searched incoming references. It cannot establish whether an external process, installed historical wheel, cron, operator script, separate repository, or live database invokes legacy API/CLI/worker or depends on legacy tables.

## 26. Prior Unknown Carry-forward

| ID | Status | Phase 05 evidence | Notes |
|---|---|---|---|
| E4-UNK-001 | remains open | console scripts are Product-only | external CLI/operator invocation unknown |
| E4-UNK-002 | narrowed, not resolved | no repository-managed legacy deployment; legacy roots still exist | external process manager unknown |
| E4-UNK-003 | remains open | no runtime nginx/API verification | runtime prohibited |
| E4-UNK-004 | remains open | static UI mapping only | user-state reachability unknown |
| E4-UNK-005 | remains open | family schema allowance unchanged | design intent unknown |
| E4-UNK-006 | remains open | no runtime lease evidence | worker behavior unknown |
| E4-UNK-007 | remains open | source confirms no Product stage write | external persistence unknown |
| E4-UNK-008 | remains open | legacy retry column/source history not resolved | runtime/history needed |
| E4-UNK-016 | remains open | external generic legacy invocations unknown | Phase 04 carry-forward |

## 27. New Unresolved Items

| ID | Question | Confirmed Facts | Why Unresolved | Additional Evidence Needed |
|---|---|---|---|---|
| E4-UNK-023 | Are legacy source files executable under the current installed namespace? | many legacy files import old top-level namespaces absent from current tree | no import execution allowed; packaging excludes legacy | isolated static/package build or historical layout |
| E4-UNK-024 | Which external operators invoke legacy API/CLI/worker? | source roots exist; no repository-local invocation | external boundary not represented | deployment/process-manager/operator inventory |
| E4-UNK-025 | Are legacy shared-scientific consumers still required outside Product? | legacy and Product adapters share causal modules | external consumers unknown | usage inventory outside repository |
| E4-UNK-026 | Does any deployed database retain legacy tables needed by external clients? | Product migrations have no legacy FK | runtime DB state prohibited | schema inventory/DB owner evidence |
| E4-UNK-027 | Is `legacy-product-snapshot/1` consumed by external or only Product code? | Product validation/constraint references it | external format consumers unknown | contract registry/data samples |
| E4-UNK-028 | Does any current tooling dynamically discover excluded legacy modules? | no static tool reference found | dynamic/plugin configuration not proven absent | process/tool configuration inventory |
| E4-UNK-029 | Are old `ariadne.application` imports a relocation alias outside the repository? | current source tree lacks matching top-level modules | external packaging layout unknown | historical package/build artifacts |

## 28. Facts

- E4-OBS-052: current Product tests assert Product/web code does not import `ariadne.legacy` or old control-plane namespaces.
- E4-OBS-053: current `project.scripts` exposes Product CLI/API/worker entry points only.
- E4-OBS-054: wheel configuration excludes `src/ariadne/legacy/**`.
- E4-OBS-055: `.dockerignore` excludes `src/ariadne/legacy`; Docker/Compose build and run Product API/worker only.
- E4-OBS-056: Product migration environment targets `ProductBase.metadata` and Product migration chain; root legacy migration environment targets a different Base.
- E4-OBS-057: Product ORM/migration searches found no FK/raw SQL/view/trigger dependency on legacy physical tables.
- E4-OBS-058: legacy source roots define API, worker, and CLI main callables but no current repository-managed invocation was found.
- E4-OBS-059: legacy discovery/inference adapters import shared `ariadne.causal`, preprocessing, and shared validation modules.
- E4-OBS-060: Product scientific adapters also import shared causal discovery/inference implementations.
- E4-OBS-061: legacy Result/Artifact/ArtifactLineage models are separate from Product Result/Artifact/LineageEdge models.
- E4-OBS-062: repository tests/docs contain legacy names and archived migration references, but no active Product test imports `ariadne.legacy`.
- E4-OBS-063: current legacy files contain imports to old top-level namespaces for which matching paths are not present in the current source tree.

## 29. Inferences

- E4-INF-026: repository-defined active Product runtime has no confirmed inbound production dependency on `ariadne.legacy`.
- E4-INF-027: shared scientific modules are not legacy-owned exclusively; they are consumed by both Product scientific adapters and legacy adapters.
- E4-INF-028: legacy persistence and Product persistence are separate schema/migration families in current source.
- E4-INF-029: packaging/deployment exclusion reduces repository-managed reachability but cannot prove absence of external consumers.
- E4-INF-030: legacy source has a mixed status: shared scientific capability consumers, standalone old roots, migration/history surfaces, and potentially unresolved old namespace dependencies.
- E4-INF-031: similar names such as `legacy_rows`, `legacy_artifacts`, and `legacy-product-snapshot/1` are compatibility/terminology surfaces rather than confirmed `ariadne.legacy` imports.
- E4-INF-032: removing or changing legacy source could affect shared scientific capability users only if the shared modules themselves are changed; direct Product runtime dependency on legacy package is not confirmed.

## 30. Mandatory Explicit Answers

A–L are answered below with evidence and fact/inference separation.

## 31. Phase Conclusion

1. Legacy Components inventoried: 12.
2. Components with `ACTIVE_PRODUCT_REACHABLE`: 0 confirmed.
3. Components with `STANDALONE_RUNTIME_REACHABLE` source roots: 4 primary roots (API, CLI, worker, internal execution/pipeline roots).
4. Product/shared import dependency on legacy: 0 confirmed.
5. Components containing scientific capabilities: 5 primary units (pipeline, discovery, inference, ETL/catalog, shared scientific consumers).
6. Scientific capabilities used by active Product code: 5 shared capability families confirmed; Product imports shared modules, not legacy package.
7. Product persistence depends on legacy physical tables: NO_PATH_CONFIRMED.
8. Product migration chain depends on legacy migration chain: NO_PATH_CONFIRMED.
9. Repository-managed deployment invokes legacy: 0 confirmed.
10. Installed package entry points expose legacy: 0 confirmed.
11. Repository-unreferenced legacy components: 12 as external inbound candidates; internal legacy edges remain.
12. New unresolved items: 7 (E4-UNK-023..029).
13. Evidence sufficient for Target Architecture Decision preparation: YES as a factual dependency handoff, without keep/delete/migrate/replace classification.

## 32. Completion Status

`COMPLETED_WITH_UNKNOWNS`.

# 52. Mandatory Explicit Answers

## A

**NO_PATH_CONFIRMED.** Active Product source, web API, and worker contain no confirmed `ariadne.legacy` import/call/instantiation; architecture tests enforce this statically. Evidence: E4-OBS-052; `tests/product/test_architecture.py:23-50`.

## B

**NO_PATH_CONFIRMED.** Active Product scientific execution uses `ariadne.causal` and scientific adapters directly/shared, not implementations under `ariadne.legacy`. Evidence: E4-OBS-059..060.

## C

**PARTIALLY.** Legacy-only orchestration/capabilities include legacy control-plane persistence, ArtifactLineage, old MLflow/tracking orchestration, and CompleteJourney legacy orchestration. The underlying causal discovery/estimation implementations are shared, not legacy-only. Evidence: E4-OBS-059..061.

## D

**NO_PATH_CONFIRMED.** Product ORM/migrations target Product tables and Product migration metadata; no legacy table FK/cross-schema SQL/view/trigger was confirmed. Evidence: E4-OBS-056..057.

## E

**NO_PATH_CONFIRMED.** Product uses `product_migrations`; root `migrations` is a separate legacy/history chain and no revision dependency was found.

## F

**NO_PATH_CONFIRMED.** Docker/Compose invokes Product API, Product worker, and `alembic_product.ini`; legacy is excluded from build context.

## G

**NO_PATH_CONFIRMED.** `pyproject.toml` exposes only Product scripts and explicitly excludes the legacy package from wheel output.

## H

**PARTIALLY.** Active Product tests do not import `ariadne.legacy`, but they do contain static exclusion assertions, legacy-named Product compatibility data, and archived legacy tests outside default collection. Evidence: `tests/product/test_architecture.py:23-50`; `tests/product/test_postgres_contract.py:141-194`; `pyproject.toml:37`.

## I

**NO_PATH_CONFIRMED** for current repository tools. Legacy itself has CLI roots, but no non-legacy maintenance/developer tool with an executable legacy import was found.

## J

**PARTIALLY.** No current code shim importing `ariadne.legacy` was confirmed. Product retains legacy-named snapshot/data contracts and tests, which are compatibility surfaces but not module shims.

## K

**YES.** All 12 legacy responsibility units have no confirmed non-legacy repository-local incoming consumer; their internal legacy references and shared scientific outbound dependencies remain. This is not a deletion conclusion.

## L

**NO.** Static repository evidence cannot prove that external processes, installed historical packages, cron jobs, other repositories, operators, or live databases do not invoke legacy roots or depend on legacy tables.

# 53. Prohibited Conclusions

This result does not classify legacy components as keep/delete/migrate/replace, does not assert external consumers are absent, and does not prescribe Target Architecture, migration, or shutdown.

# 54. Completeness Criteria

C1 prior Phase 01–04 results/IDs read: PASS.  
C2 legacy responsibility units: PASS.  
C3 inbound Product/shared references: PASS.  
C4 reverse legacy dependencies: PASS.  
C5 scientific capability matrix: PASS.  
C6 scientific contracts: PASS, static only.  
C7 legacy persistence inventory: PASS.  
C8 Product schema dependency: PASS.  
C9 migration chain comparison: PASS.  
C10 runtime roots: PASS.  
C11 tests/fixtures: PASS.  
C12 tooling: PASS.  
C13 packaging: PASS.  
C14 deployment/configuration: PASS.  
C15 compatibility/data formats: PASS.  
C16 overlap matrix: PASS.  
C17 reachability matrix: PASS.  
C18 criticality classification: PASS.  
C19 reverse blast radius: PASS.  
C20 unreferenced surface: PASS with external limitation.  
C21 prior unknown carry-forward: PASS.  
C22 new unknowns: PASS.  
C23 facts/inferences distinction: PASS.  
C24 mandatory A–L: PASS.  
C25 prohibited conclusions respected: PASS.  
C26 static-only/result-only write: PASS.  
C27 branch and HEAD recorded: PASS.  
C28 no runtime/database/test execution: PASS.

# 55. Final Self-Check

Performed after result generation:

```text
git status --short
git diff --stat
git diff -- docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/architecture_review/05_legacy_dependency_reachability_matrix_result.md
```

Existing `deploy/.nfs000000000076202f00000088` change was preserved.

