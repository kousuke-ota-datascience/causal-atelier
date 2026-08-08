# 01 Runtime Entry Point Inventory Result

## 1. Metadata

- Prompt: `docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/architecture_review/01_runtime_entrypoint_inventory_prompt.md`
- Repository root: `/loc0/bigbrother/repositories/causal-atelier`
- Branch: `refactor/ariadne_mvp_e4`
- HEAD: `bf4cb42843c8ef978c6cfb97581c63ae3a834e76`
- Working tree status at start: ` D deploy/.nfs000000000076202f00000088`; target work directory was untracked. These pre-existing changes were not modified.
- Started at: `2026-08-08T10:39:38Z`
- Finished at: `2026-08-08T10:45:00Z`
- Phase status: `COMPLETED_WITH_UNKNOWNS`

## 2. Executive Inventory

### 2.1 Runtime Roots

| Root ID | Surface | Invocation | Definition / Config | Reachability | Evidence |
|---|---|---|---|---|---|
| E4-ROOT-001 | Product HTTP API | Docker `uvicorn ariadne.interfaces.web_api.app:app --host 0.0.0.0 --port 8000` | `Dockerfile:21-24`; `src/ariadne/interfaces/web_api/app.py:59,62-64` | `ACTIVE_RUNTIME_REACHABLE` | Docker command resolves the product ASGI object; app includes product routers at `app.py:46-50`. |
| E4-ROOT-002 | Product worker | Compose `ariadne-worker` console script | `compose.yaml:44-52`; `pyproject.toml:31-33`; `src/ariadne/interfaces/worker/runner.py:111-121` | `ACTIVE_RUNTIME_REACHABLE` | Compose command resolves the registered worker callable. |
| E4-ROOT-003 | Product CLI | `ariadne-discover`, `ariadne-estimate`, `ariadne-identify`, `ariadne-refute`, `ariadne-sensitivity` | `pyproject.toml:24-30`; respective CLI modules | `ACTIVE_RUNTIME_REACHABLE` | Five console scripts are registered to five `main` callables. |
| E4-ROOT-004 | Frontend static runtime | nginx serves `./frontend` on port 8080 | `compose.yaml:54-63`; `frontend/index.html:1-...`; `frontend/app.js:1` | `ACTIVE_RUNTIME_REACHABLE` | Compose mounts the repository frontend read-only and `app.js` uses `/api/v1`. |
| E4-ROOT-005 | Product migration command | Compose `alembic -c alembic_product.ini upgrade head` | `compose.yaml:18-26` | `TOOLING_ONLY` | Migration is a separate precondition service, not an application Execution boundary. |
| E4-ROOT-006 | Legacy HTTP API candidate | Direct module/app callable exists | `src/ariadne/legacy/interfaces/api/app.py:30-38,212-218` | `UNREFERENCED_CANDIDATE` | No Docker/Compose/console-script reference to this callable was found. |
| E4-ROOT-007 | Legacy worker candidate | Direct module `main` exists | `src/ariadne/legacy/workers/main.py:15-47` | `UNREFERENCED_CANDIDATE` | No current deployment or packaging wiring to this worker was found. |

The Compose database container is infrastructure state, not an application runtime root that accepts an Execution trigger; it is therefore not assigned an application Root ID.

### 2.2 Execution-Relevant Entry Points

| Entry ID | Runtime Root | External Trigger | Boundary Entry Point | First Execution Boundary | Architecture | Reachability |
|---|---|---|---|---|---|---|
| E4-EP-001 | E4-ROOT-001 | HTTP causal discovery/inference request | `POST /api/v1/projects/{project_id}/execution-batches` | `ExecutionService.create_execution_batch` | `PRODUCT` | `ACTIVE_RUNTIME_REACHABLE` |
| E4-EP-002 | E4-ROOT-001 | HTTP cancel for causal Execution | `POST /api/v1/executions/{execution_id}/cancel` | `ExecutionService.request_cancel` | `PRODUCT` | `ACTIVE_RUNTIME_REACHABLE` |
| E4-EP-003 | E4-ROOT-001 | HTTP retry for causal Execution | `POST /api/v1/executions/{execution_id}/retry` | `ExecutionService.retry_execution` | `PRODUCT` | `ACTIVE_RUNTIME_REACHABLE` |
| E4-EP-004 | E4-ROOT-001 | HTTP exploratory analysis submission | `POST /api/v1/projects/{project_id}/exploration/executions` | `ExploratoryWorkspaceService.submit_execution` | `PRODUCT` | `ACTIVE_RUNTIME_REACHABLE` |
| E4-EP-005 | E4-ROOT-001 | HTTP predictive execution submission | `POST /api/v1/projects/{project_id}/executions` | `PredictiveWorkflowService.submit_execution` | `PRODUCT` | `ACTIVE_RUNTIME_REACHABLE` |
| E4-EP-006 | E4-ROOT-001 | HTTP predictive cancel | `POST /api/v1/projects/{project_id}/executions/{execution_id}/cancel` | `PredictiveWorkflowService.cancel` | `PRODUCT` | `ACTIVE_RUNTIME_REACHABLE` |
| E4-EP-007 | E4-ROOT-001 | HTTP predictive retry | `POST /api/v1/projects/{project_id}/executions/{execution_id}/retry` | `PredictiveWorkflowService.retry` | `PRODUCT` | `ACTIVE_RUNTIME_REACHABLE` |
| E4-EP-008 | E4-ROOT-001 | HTTP predictive rerun | `POST /api/v1/projects/{project_id}/executions/{execution_id}/rerun` | `PredictiveWorkflowService.rerun` | `PRODUCT` | `ACTIVE_RUNTIME_REACHABLE` |
| E4-EP-009 | E4-ROOT-001 | HTTP predictive revision | `POST /api/v1/projects/{project_id}/executions/{execution_id}/revise` | `PredictiveWorkflowService.revise` | `PRODUCT` | `ACTIVE_RUNTIME_REACHABLE` |
| E4-EP-010 | E4-ROOT-002 | Worker claims causal `Execution` | `uow.executions.claim_next` branch | `ExecutionProcessor.process` | `PRODUCT` | `ACTIVE_RUNTIME_REACHABLE` |
| E4-EP-011 | E4-ROOT-002 | Worker claims exploratory family Execution | `ExploratoryWorkspaceService.claim_next` branch | `ExploratoryWorkspaceService.process_execution` | `PRODUCT` | `ACTIVE_RUNTIME_REACHABLE` |
| E4-EP-012 | E4-ROOT-002 | Worker claims predictive family Execution | `PredictiveWorkflowService.claim_next` branch | `PredictiveWorkflowService.process_execution` | `PRODUCT` | `ACTIVE_RUNTIME_REACHABLE` |
| E4-EP-013 | E4-ROOT-003 | `ariadne-discover --config ...` | `discovery.main` | `ScientificCoreAdapter.run_discovery` | `SHARED_OR_OTHER` | `ACTIVE_RUNTIME_REACHABLE` |
| E4-EP-014 | E4-ROOT-003 | `ariadne-estimate --config ...` | `estimation.main` | `ScientificCoreAdapter.run_estimation` | `SHARED_OR_OTHER` | `ACTIVE_RUNTIME_REACHABLE` |
| E4-EP-015 | E4-ROOT-003 | `ariadne-identify --config ...` | `identification.main` → `run_stage` | `ScientificCoreAdapter.run_identification` | `SHARED_OR_OTHER` | `ACTIVE_RUNTIME_REACHABLE` |
| E4-EP-016 | E4-ROOT-003 | `ariadne-refute --config ...` | `refutation.main` → `run_stage` | `ScientificCoreAdapter.run_refutation` | `SHARED_OR_OTHER` | `ACTIVE_RUNTIME_REACHABLE` |
| E4-EP-017 | E4-ROOT-003 | `ariadne-sensitivity --config ...` | `sensitivity.main` → `run_stage` | `ScientificCoreAdapter.run_sensitivity` | `SHARED_OR_OTHER` | `ACTIVE_RUNTIME_REACHABLE` |

## 3. Runtime Root Details

### E4-ROOT-001 — Product HTTP API

#### Invocation

`Dockerfile:24` invokes `uvicorn` with `ariadne.interfaces.web_api.app:app`. The packaging script `ariadne-api` is an additional callable at `pyproject.toml:32`, whose handler is `app.main` (`src/ariadne/interfaces/web_api/app.py:62-64`).

#### Registration / Wiring

`app.create_app` imports product routers and includes them under `/api/v1` (`src/ariadne/interfaces/web_api/app.py:10-24,46-50`). Dependency providers construct product application services (`src/ariadne/interfaces/web_api/dependencies.py:15-31,65-118`).

#### Evidence

- `Dockerfile:21-24`, symbol container `CMD`: product ASGI runtime root.
- `src/ariadne/interfaces/web_api/app.py:28-59`, symbols `create_app`, `app`: FastAPI object and router registration.
- `src/ariadne/interfaces/web_api/dependencies.py:65-67,101-118`: product service wiring.

#### Reachability Classification

`ACTIVE_RUNTIME_REACHABLE`.

### E4-ROOT-002 — Product worker

#### Invocation

`compose.yaml:44-52` runs `ariadne-worker`; `pyproject.toml:33` maps it to `ariadne.interfaces.worker.runner:main`. `main` reads product database/artifact configuration and calls `run_worker` (`src/ariadne/interfaces/worker/runner.py:111-121`).

#### Registration / Wiring

`run_worker` constructs product `ExecutionProcessor`, exploratory service, and predictive service (`src/ariadne/interfaces/worker/runner.py:53-62`). Its loop first claims causal executions, then exploratory, then predictive executions (`runner.py:73-103`).

#### Evidence

- `compose.yaml:44-52`, `pyproject.toml:31-33`: deployment-to-console-script wiring.
- `src/ariadne/interfaces/worker/runner.py:32-62,73-103`: worker root and three dispatch branches.

#### Reachability Classification

`ACTIVE_RUNTIME_REACHABLE`.

### E4-ROOT-003 — Product CLI

#### Invocation

Five console scripts are registered in `pyproject.toml:24-30`. Each has an argparse boundary and a `main` callable; identify/refute/sensitivity delegate to `run_stage` (`src/ariadne/interfaces/cli/identification.py:1-5`, `refutation.py:1-5`, `sensitivity.py:1-5`).

#### Registration / Wiring

The direct CLI implementations import product domain validation/contracts and call `ScientificCoreAdapter` (`src/ariadne/interfaces/cli/discovery.py:49-59`, `estimation.py:47-100`, `scientific_stage.py:20-70`). The discovery module explicitly states that it does not create Web/API Execution IDs (`discovery.py:1`).

#### Evidence

- `pyproject.toml:24-30`: all five registered commands.
- `src/ariadne/interfaces/cli/discovery.py:27-34,49-59` and `estimation.py:24-30,47-100`: command parsing and core calls.
- `src/ariadne/interfaces/cli/scientific_stage.py:29-70`: shared identify/refute/sensitivity dispatch.

#### Reachability Classification

`ACTIVE_RUNTIME_REACHABLE` as packaging-defined commands. Whether an operator invokes them is external runtime state and is not established by static code.

### E4-ROOT-004 — Frontend

#### Invocation

Compose runs nginx and mounts `frontend/` read-only (`compose.yaml:54-63`). `frontend/app.js:1,10` establishes the `/api/v1` base and request helper.

#### Registration / Wiring

Execution UI actions issue `POST` requests: exploration at `frontend/app.js:166`, predictive plan/validate/submit at `frontend/app.js:272-283`, and causal batch operations at `frontend/app.js:330,365-372`.

#### Evidence

- `compose.yaml:54-63`: frontend runtime root.
- `frontend/app.js:166,272-283,330,365-372`: UI-to-backend request sites.

#### Reachability Classification

`ACTIVE_RUNTIME_REACHABLE` for the static frontend runtime and its request code. Browser execution itself was not run, per phase prohibition.

### E4-ROOT-005 — Migration

`compose.yaml:18-26` defines a separate product migration command that gates API/worker startup through `depends_on`. It is `TOOLING_ONLY`; no Execution endpoint or worker handler is reached.

### E4-ROOT-006 / E4-ROOT-007 — Legacy candidates

Legacy `create_app` and worker `main` are valid code-level roots (`src/ariadne/legacy/interfaces/api/app.py:30-38,212-218`; `src/ariadne/legacy/workers/main.py:15-47`), but reverse search found no reference from current Dockerfile, Compose, packaging scripts, or non-legacy runtime wiring. They are therefore `UNREFERENCED_CANDIDATE`, not dead-code findings.

## 4. Execution-Relevant Entry Point Details

### E4-EP-001 — Causal execution batch

#### External Trigger

HTTP `POST /api/v1/projects/{project_id}/execution-batches`. The frontend submits DISCOVERY, IDENTIFICATION, ESTIMATION, REFUTATION, and SENSITIVITY variants to this endpoint (`frontend/app.js:330,365-372`).

#### Runtime Root

E4-ROOT-001.

#### Boundary Entry Point

`src/ariadne/interfaces/web_api/routers/executions.py:54-98`, symbol `create_execution_batch`.

#### Static Call Chain

`create_execution_batch` → `ExecutionService.create_execution_batch` (`executions.py:64-85`) → product `Execution` rows are created/queued (`src/ariadne/product/application/execution_service.py:67-89,120-156`). Worker claims them (`src/ariadne/interfaces/worker/runner.py:73-81`) → `ExecutionProcessor.process` (`execution_processor.py:53-64`) → `GenericExecutor.execute` after causal runner registration (`execution_processor.py:180-215`).

#### First Execution Orchestration Boundary

`ExecutionService.create_execution_batch`, followed asynchronously by `ExecutionProcessor._dispatch_generic` / `GenericExecutor.execute`.

#### Architecture Classification

`PRODUCT`.

#### Reachability Classification

`ACTIVE_RUNTIME_REACHABLE`.

#### Evidence

The endpoint is registered by `app.py:46-50`; its dependency is product `ExecutionService` (`dependencies.py:65-67`); worker wiring is product (`runner.py:53-62`).

#### Unknowns

Static code does not establish whether a request is actually sent in a deployed environment.

### E4-EP-002 / E4-EP-003 — Causal cancel/retry

The endpoints are `src/ariadne/interfaces/web_api/routers/executions.py:124-131`. They call `ExecutionService.request_cancel` and `ExecutionService.retry_execution`, respectively. Both are product application boundaries and are `ACTIVE_RUNTIME_REACHABLE` through E4-ROOT-001. The worker later observes cancellation in `execution_processor.py:92-107`; retry creates a new queued execution in the product service implementation. Architecture: `PRODUCT`.

### E4-EP-004 — Exploratory submission

`POST /api/v1/projects/{project_id}/exploration/executions` is registered at `src/ariadne/interfaces/web_api/routers/exploration.py:204-213` and calls `ExploratoryWorkspaceService.submit_execution`. The service creates a queued family Execution (`src/ariadne/product/application/exploratory_service.py:203-265`). Worker dispatch is `runner.py:83-90` → `process_execution` (`exploratory_service.py:326-347`) → `_run_in_memory` → `GenericExecutor` with registered exploratory runners (`exploratory_service.py:477-487`). Architecture: `PRODUCT`; reachability: `ACTIVE_RUNTIME_REACHABLE`.

### E4-EP-005 — Predictive submission

`POST /api/v1/projects/{project_id}/executions` is registered at `src/ariadne/interfaces/web_api/routers/predictive_workflow.py:57-70` and calls `PredictiveWorkflowService.submit_execution`. The service queues a family Execution and stage rows (`src/ariadne/product/application/predictive_workflow_service.py:114-124,191-222`). Worker dispatch is `runner.py:92-100` → `predictive_workflow_service.py:265-288,290-307` → `GenericExecutor.execute` (`predictive_workflow_service.py:335-347`), with predictive runners registered at `:766-772`. Architecture: `PRODUCT`; reachability: `ACTIVE_RUNTIME_REACHABLE`.

### E4-EP-006 through E4-EP-009 — Predictive state mutations

Predictive cancel/retry/rerun/revise endpoints are at `src/ariadne/interfaces/web_api/routers/predictive_workflow.py:108-150`. Each calls a corresponding `PredictiveWorkflowService` method. They are product application boundaries and `ACTIVE_RUNTIME_REACHABLE` through the registered predictive router. Rerun/revise create or derive a queued family Execution in the same service path. Architecture: `PRODUCT`.

### E4-EP-010 — Causal worker execution

The worker claims a product `Execution` at `src/ariadne/interfaces/worker/runner.py:73-81`, then calls `ExecutionProcessor.process`. The processor builds a causal plan and product `GenericExecutor` boundary at `src/ariadne/interfaces/worker/execution_processor.py:180-215`. Architecture: `PRODUCT`; reachability: `ACTIVE_RUNTIME_REACHABLE`.

### E4-EP-011 — Exploratory worker execution

The worker calls `claim_next` and then `process_execution` at `src/ariadne/interfaces/worker/runner.py:83-90`. The service invokes product `GenericExecutor` with exploratory runner registration at `src/ariadne/product/application/exploratory_service.py:326-347,477-487`. Architecture: `PRODUCT`; reachability: `ACTIVE_RUNTIME_REACHABLE`.

### E4-EP-012 — Predictive worker execution

The worker calls `claim_next` and then `process_execution` at `src/ariadne/interfaces/worker/runner.py:92-100`. The service invokes product `GenericExecutor` and registers predictive runners at `src/ariadne/product/application/predictive_workflow_service.py:290-347,766-772`. Architecture: `PRODUCT`; reachability: `ACTIVE_RUNTIME_REACHABLE`.

### E4-EP-013 through E4-EP-017 — Standalone CLI execution paths

The five commands are packaging-reachable. Their call chains are:

- E4-EP-013: `discovery.main` → `ScientificCoreAdapter.run_discovery` (`src/ariadne/interfaces/cli/discovery.py:33-59`).
- E4-EP-014: `estimation.main` → `ScientificCoreAdapter.run_estimation` (`src/ariadne/interfaces/cli/estimation.py:30-57,95-100`).
- E4-EP-015: `identification.main` → `run_stage` → `ScientificCoreAdapter.run_identification` (`src/ariadne/interfaces/cli/identification.py:1-5`; `scientific_stage.py:29-55`).
- E4-EP-016: `refutation.main` → `run_stage` → `ScientificCoreAdapter.run_refutation` (`src/ariadne/interfaces/cli/refutation.py:1-5`; `scientific_stage.py:57-64`).
- E4-EP-017: `sensitivity.main` → `run_stage` → `ScientificCoreAdapter.run_sensitivity` (`src/ariadne/interfaces/cli/sensitivity.py:1-5`; `scientific_stage.py:57-70`).

The CLI imports product domain validation and scientific-core ports, but does not call `ExecutionService`, create Web/API Execution rows, or enter the product workflow `GenericExecutor`. Therefore the first execution implementation is classified `SHARED_OR_OTHER`, not `PRODUCT`; reachability is `ACTIVE_RUNTIME_REACHABLE` as a configured command. The exact operator/deployment invocation remains unknown.

## 5. UI → Backend Execution Paths

| UI Action | Frontend Location | Backend Request | Backend Entry ID | Classification | Evidence |
|---|---|---|---|---|---|
| Exploratory execution submit | `frontend/app.js:166` | `POST /projects/{project_id}/exploration/executions` | E4-EP-004 | `PRODUCT`, `ACTIVE_RUNTIME_REACHABLE` | Request body and endpoint are explicit. |
| Predictive plan creation/validation/submission | `frontend/app.js:272-283` | `POST /projects/{project_id}/execution-plans`, validation, then `POST /projects/{project_id}/executions` | E4-EP-005 | `PRODUCT`, `ACTIVE_RUNTIME_REACHABLE` | Sequential request code is explicit. |
| Causal DISCOVERY batch | `frontend/app.js:330-332` | `POST /projects/{project_id}/execution-batches` | E4-EP-001 | `PRODUCT`, `ACTIVE_RUNTIME_REACHABLE` | Request code is explicit. |
| Causal IDENTIFICATION/ESTIMATION/REFUTATION/SENSITIVITY | `frontend/app.js:365-372` | `POST /projects/{project_id}/execution-batches` | E4-EP-001 | `PRODUCT`, `ACTIVE_RUNTIME_REACHABLE` | Request code is explicit. |

The frontend uses a relative `/api/v1` base (`frontend/app.js:1`); nginx-to-API proxy behavior is deployment configuration outside the frontend file and was not treated as runtime execution evidence beyond the Compose wiring.

## 6. CLI Execution Paths

| CLI Command | Registration | Handler | Entry ID | Architecture | Reachability |
|---|---|---|---|---|---|
| `ariadne-discover` | `pyproject.toml:26` | `discovery.main` | E4-EP-013 | `SHARED_OR_OTHER` | `ACTIVE_RUNTIME_REACHABLE` |
| `ariadne-estimate` | `pyproject.toml:27` | `estimation.main` | E4-EP-014 | `SHARED_OR_OTHER` | `ACTIVE_RUNTIME_REACHABLE` |
| `ariadne-identify` | `pyproject.toml:28` | `identification.main` | E4-EP-015 | `SHARED_OR_OTHER` | `ACTIVE_RUNTIME_REACHABLE` |
| `ariadne-refute` | `pyproject.toml:29` | `refutation.main` | E4-EP-016 | `SHARED_OR_OTHER` | `ACTIVE_RUNTIME_REACHABLE` |
| `ariadne-sensitivity` | `pyproject.toml:30` | `sensitivity.main` | E4-EP-017 | `SHARED_OR_OTHER` | `ACTIVE_RUNTIME_REACHABLE` |

## 7. Worker / Background Execution Paths

| Worker / Task | Process Root | Registration | Handler | Architecture | Reachability |
|---|---|---|---|---|---|
| Causal product Execution | E4-ROOT-002 | `pyproject.toml:33`; `runner.py:73-81` | `ExecutionProcessor.process` | `PRODUCT` | `ACTIVE_RUNTIME_REACHABLE` |
| Exploratory family Execution | E4-ROOT-002 | `runner.py:83-90` | `ExploratoryWorkspaceService.process_execution` | `PRODUCT` | `ACTIVE_RUNTIME_REACHABLE` |
| Predictive family Execution | E4-ROOT-002 | `runner.py:92-100` | `PredictiveWorkflowService.process_execution` | `PRODUCT` | `ACTIVE_RUNTIME_REACHABLE` |
| Legacy outbox worker | E4-ROOT-007 | No current registration found | `legacy.workers.main` → `Worker.run_once` | `LEGACY` | `UNREFERENCED_CANDIDATE` |

## 8. Legacy / Product Runtime Exposure Matrix

| Component / Boundary | Legacy | Product | Runtime Reachability | Entry IDs | Evidence |
|---|---:|---:|---|---|---|
| Product API routers and dependencies |  | Yes | Active | E4-EP-001–009 | `src/ariadne/interfaces/web_api/app.py:10-50`; `dependencies.py:15-31,65-118` |
| Product causal worker/executor |  | Yes | Active | E4-EP-010 | `src/ariadne/interfaces/worker/runner.py:53-62,73-81`; `execution_processor.py:180-215` |
| Product family workers/executors |  | Yes | Active | E4-EP-011–012 | `runner.py:83-103`; product services cited above |
| Product standalone CLI contracts/core |  | Yes | Active command definition | E4-EP-013–017 | CLI source cited above |
| Legacy HTTP API | Yes |  | Unreferenced candidate | None | `src/ariadne/legacy/interfaces/api/app.py:30-38,212-218`; no current deployment/packaging reference found |
| Legacy execution API handlers | Yes |  | Unreferenced candidate | None | `src/ariadne/legacy/interfaces/api/routers/executions.py:104-153`; reverse wiring search found no current root reference |
| Legacy worker | Yes |  | Unreferenced candidate | None | `src/ariadne/legacy/workers/main.py:15-47`; no current registration found |

No `MIXED` path was confirmed. The legacy/product columns describe observed source dependencies and runtime wiring, not lifecycle or deletion recommendations.

## 9. Observed Path Convergence / Divergence

- Causal HTTP operations converge on `ExecutionService.create_execution_batch`, then on the product worker and `ExecutionProcessor`.
- Exploratory and predictive HTTP submissions converge on the product worker process but use distinct family services and family Execution persistence.
- The worker contains three explicit selection branches: causal product Execution, exploratory family Execution, and predictive family Execution (`runner.py:73-103`).
- Exploratory and predictive processing both converge on product `GenericExecutor`, with separate runner registries.
- Standalone CLI commands converge on `ScientificCoreAdapter` but do not converge on the Web/API Execution service or worker path.
- No legacy/product mixed call chain was confirmed from current runtime roots.

## 10. Unreferenced / Non-runtime Candidates

| Component | Classification | Search Performed | Evidence | Limitation |
|---|---|---|---|---|
| `ariadne.legacy.interfaces.api.app:app` | `UNREFERENCED_CANDIDATE` | Dockerfile, Compose, pyproject scripts, source runtime references | `src/ariadne/legacy/interfaces/api/app.py:212-218` | External process managers or commands outside the repository are not observable. |
| `ariadne.legacy.workers.main:main` | `UNREFERENCED_CANDIDATE` | Same reverse search | `src/ariadne/legacy/workers/main.py:26-47` | External invocation cannot be excluded statically. |
| Legacy API execution routes | `UNREFERENCED_CANDIDATE` | Reverse search from current roots and packaging | `src/ariadne/legacy/interfaces/api/routers/executions.py:104-153` | Definition existence is not proof of non-use by external consumers. |
| `src/ariadne/legacy/application/**` execution services | `UNREFERENCED_CANDIDATE` | Source import and runtime wiring search | `src/ariadne/legacy/application/run_execution/services.py:1-16` | Static search cannot establish dynamically constructed imports. |

## 11. Unresolved Items

| ID | Question | Confirmed Facts | Why Unresolved | Additional Evidence Needed |
|---|---|---|---|---|
| E4-UNK-001 | Are the five CLI commands invoked in the standard deployed runtime? | Console scripts and handlers are registered (`pyproject.toml:24-30`). | Static registration does not reveal operator behavior, cron, or external process-manager configuration. | Deployment/process-manager records or operator invocation logs. |
| E4-UNK-002 | Is the legacy API or worker invoked externally? | No repository-local current wiring was found; callables exist. | External commands/configuration are outside repository evidence. | Deployment manifests, process-manager configuration, or runtime process inventory. |
| E4-UNK-003 | Does the frontend actually reach the API through nginx in a running deployment? | Compose mounts frontend and frontend uses relative `/api/v1` requests. | Browser and server runtime were prohibited. | Runtime verification of nginx/API routing. |
| E4-UNK-004 | Are all generic batch operation values reachable from the current UI? | Endpoint accepts operation values and UI submits several values. | Request construction depends on user state and UI interaction. | Browser/runtime trace or externally captured requests. |

## 12. Facts

- E4-OBS-001 — `Dockerfile:24` starts `ariadne.interfaces.web_api.app:app` with uvicorn.
- E4-OBS-002 — `app.py:46-50` registers product routers under `/api/v1`.
- E4-OBS-003 — `pyproject.toml:24-33` registers five product CLI commands, `ariadne-api`, and `ariadne-worker`.
- E4-OBS-004 — `compose.yaml:44-52` starts the worker using `ariadne-worker`.
- E4-OBS-005 — `runner.py:73-103` has explicit causal, exploratory, and predictive worker branches.
- E4-OBS-006 — The causal API endpoint calls product `ExecutionService` (`executions.py:54-98`).
- E4-OBS-007 — Exploratory submission queues a family Execution (`exploratory.py:203-265`).
- E4-OBS-008 — Predictive submission queues a family Execution (`predictive_workflow_service.py:114-222`).
- E4-OBS-009 — Family workers invoke product `GenericExecutor` (`exploratory_service.py:477-487`; `predictive_workflow_service.py:335-347`).
- E4-OBS-010 — CLI handlers call `ScientificCoreAdapter` directly (`discovery.py:49-59`; `estimation.py:47-100`; `scientific_stage.py:49-70`).
- E4-OBS-011 — CLI discovery explicitly says it does not create Web/API Execution IDs (`discovery.py:1`).
- E4-OBS-012 — Legacy API and worker roots exist but have no repository-local current deployment/packaging reference found by reverse search.
- E4-OBS-013 — Frontend request sites map exploratory, predictive, and causal actions to product API paths (`frontend/app.js:166,272-283,330,365-372`).

## 13. Inferences

- E4-INF-001 — Given E4-OBS-001 through E4-OBS-006, the standard containerized HTTP Execution path first enters product application services and then the product worker path.
- E4-INF-002 — Given E4-OBS-004 and E4-OBS-005, the standard Compose worker can reach three distinct product processing branches selected by queue state/type.
- E4-INF-003 — Given E4-OBS-010 and E4-OBS-011, standalone CLI execution is a separate direct scientific-core path rather than the Web/API Execution aggregate path.
- E4-INF-004 — Given E4-OBS-012, legacy roots are not proven active in the repository-defined standard runtime; they remain `UNREFERENCED_CANDIDATE`, not dead code.
- E4-INF-005 — Given E4-OBS-013 and the product router registration, the repository statically maps the principal UI execution actions to product backend boundaries.

## 14. Phase Conclusion

- Confirmed runtime roots: **5 current/standard roots** (E4-ROOT-001 through E4-ROOT-005); **2 legacy code-level candidates**.
- Confirmed Execution-Relevant entry points: **17**.
- Architecture classification counts: `LEGACY 0`, `PRODUCT 12`, `SHARED_OR_OTHER 5`, `MIXED 0`, `UNKNOWN 0`.
- Reachability counts across Execution-Relevant entry points: `ACTIVE_RUNTIME_REACHABLE 17`, `CONDITIONALLY_REACHABLE 0`, `TOOLING_ONLY 0`, `TEST_ONLY 0`, `UNREFERENCED_CANDIDATE 0`, `UNKNOWN 0`.
- Unresolved item count: **4**.
- Evidence sufficiency for next Architecture Review phase: **Yes, with the four unresolved external/runtime questions carried forward.**

No implementation change, deletion recommendation, or target-architecture decision is made here.

## 15. Completion Status

`COMPLETED_WITH_UNKNOWNS`
