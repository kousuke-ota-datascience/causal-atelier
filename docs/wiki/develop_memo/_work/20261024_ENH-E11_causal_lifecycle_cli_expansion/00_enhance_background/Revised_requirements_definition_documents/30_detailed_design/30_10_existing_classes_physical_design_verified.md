# 30.10 — Existing Classes: Physical Design Verified Against Source

**Status:** `SOURCE_VERIFIED_BASELINE / ENH_E11_NO_CODE_CHANGE`  
**Source commit:** `3ba5fe2465ec591f0da7f998c21a5241984b73dc`. This document records existing behavior for six representative classes/ports. It does not approve E11 use of these exact classes or cover all current product classes.

## 1. Scope and source mapping

| Symbol | Source | Source blob | Relation |
|---|---|---|---|
| `PlanValidator` | [src/ariadne/product/workflow/plan_validator.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/src/ariadne/product/workflow/plan_validator.py) | `53aab649a0ed3f0dbec78e5fa98271ff78f5dc12` | workflow plan checks |
| `StageRunnerRegistry` | [src/ariadne/product/workflow/runner_registry.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/src/ariadne/product/workflow/runner_registry.py) | `7ffa673d92818e597c4349737860df0ff75b4f97` | runner resolution |
| `GenericExecutor` / `ExecutionOutcome` | [src/ariadne/product/workflow/executor.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/src/ariadne/product/workflow/executor.py) | `81d91e7de0fc0eb5a582711968b698fa4ac44761` | generic runtime |
| `GraphVersion` | [src/ariadne/product/domain/graph_version.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/src/ariadne/product/domain/graph_version.py) | `37ff76e001c8e269a00127e18d375f1dbc34c0e3` | Product graph authority |
| `ArtifactStorePort` / `StoredArtifact` | [src/ariadne/product/ports/artifact_store.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/src/ariadne/product/ports/artifact_store.py) | `e5bb990f9b69ef68df46a1559560ffb67b64caaf` | Product artifact Port |
| `CliManifest` | [src/ariadne/interfaces/cli/manifest.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/src/ariadne/interfaces/cli/manifest.py) | `97216eca9d777e97f7a5ebd4e248afd31c6b4de0` | existing local manifest |

## 2. `PlanValidator`

**Responsibility:** Verify the structural validity of an `ExecutionPlan` and produce deterministic topological execution order. This is not a causal identification oracle.

| Field | Python type / default | Role |
|---|---|---|
| `runners` | `StageRunnerRegistry`, required | Registered runtime Stage capabilities |
| `max_timeout_seconds` | `int=86400` | Resource policy upper bound |

| Method | Return | Preconditions and operations | Exceptions |
|---|---|---|---|
| `__init__(runners: StageRunnerRegistry, *, max_timeout_seconds: int = 86_400)` | `None` | store dependencies and limit | none specified |
| `validate(plan: ExecutionPlan)` | `tuple[str, ...]` | Validate plan schema/reference, unique Stage key, registered runner, timeout, edge endpoint, binding and schema agreement; perform deterministic topological sort | `InvalidExecutionPlan(code, message)` |
| `_error(code: str, message: str)` | `None` (never returns normally) | raise the above exception | `InvalidExecutionPlan` |

**Negative codes checked by source:** `UNSUPPORTED_PLAN_SCHEMA`, `MISSING_PLAN_REFERENCE`, `DUPLICATE_STAGE_KEY`, `EMPTY_PLAN`, `RUNNER_NOT_REGISTERED`, `RESOURCE_POLICY_EXCEEDED`, `MISSING_DEPENDENCY_NODE`, `DISABLED_DEPENDENCY`, `MISSING_OUTPUT`, `MISSING_INPUT`, `SCHEMA_MISMATCH`, `DUPLICATE_BINDING`, `PLAN_CYCLE`.

**Test obligations:** Graph DAG deterministic order, empty/cycle, type mismatch, disabled dependency, timeout/boundary, missing runner; E11 must not bypass these checks if reusing this component.

## 3. `StageRunnerRegistry`

**Responsibility:** Runtime StageType to concrete StageRunner lookup, not E11 scientific estimator registry unless independently decided.

| Field | Type / default | Invariant |
|---|---|---|
| `_runners` | `dict[StageType, StageRunner]={}` | unique stage_type |

| Method | Return | Behavior / error |
|---|---|---|
| `register(runner: StageRunner)` | `None` | Duplicate type raises `DuplicateRegistration` |
| `resolve(stage_type: StageType)` | `StageRunner` | Missing raises `RunnerNotRegistered` |
| `contains(stage_type: StageType)` | `bool` | Structural membership |
| `capability_fingerprint` (property) | `tuple[str, ...]` | Sorted StageType.key fingerprint |

## 4. `ExecutionOutcome` / `GenericExecutor`

**Responsibility:** Generic synchronous Stage lifecycle; no Browser navigation or scientific Estimand authority.

| Symbol/field | Python type | Invariant |
|---|---|---|
| `ExecutionOutcome.status` | `str` | Overall technical status |
| `ExecutionOutcome.stages` | `tuple[StageExecution, ...]` | Stage snapshots |
| `ExecutionOutcome.results` / `artifacts` | `tuple[Any, ...]` | Stage output collections |
| `ExecutionOutcome.stage_results` | `tuple[tuple[str, StageRunResult], ...]=()` | Identified stage output |
| `GenericExecutor.runners` | `StageRunnerRegistry` | Stage resolution |
| `GenericExecutor.validator` | `PlanValidator` | Refuses invalid plan |
| `GenericExecutor.bindings` | `BindingResolver` | Typed upstream output binding |
| `GenericExecutor.clock` | `Callable[[], datetime]` | Injected UTC clock default |
| `GenericExecutor.compensate` | `Callable[[StageExecution, Exception], None]` | Injected stage compensation default no-op |

```python
def execute(
    self, execution_id: str, plan: ExecutionPlan, *,
    external_inputs: dict[str, dict[str, Any]] | None = None,
    snapshots: dict[str, Any] | None = None,
    worker_id: str = "local-worker",
    cancelled: Callable[[], bool] | None = None,
    stage_executions: tuple[StageExecution, ...] | None = None,
    effective_random_seed: int | None = None,
) -> ExecutionOutcome: ...
```

**Execution sequence:** validate Plan; create/merge StageExecution by stage_key; iterate topological stage keys; skip disabled Stage; resolve input bindings and invoke registry-provided runner; collect results/artifacts and lifecycle state. Existing source owns the exact cancel/compensation semantics; any E11 extension must be reviewed and tested, not inferred from this outline.

**Negative:** Unregistered Stage, mismatched supplied StageExecution, invalid dependency, cancelled Stage and compensating failure. Product lifecycle owner remains outside the local E11 CLI-only design.

## 5. `GraphVersion` (Product Domain)

**Responsibility:** Product-scoped graph provenance, editable DRAFT and immutable FIXED state.

| Field group | Fields and types | Constraints |
|---|---|---|
| Identity | `graph_version_id: str`, `project_id: str`, `name: str` | ID default generated, owner Project |
| Provenance | `source_result_id: str|None`, `parent_graph_version_id: str|None`, `graph_origin: GraphOrigin`, `provenance_json: dict[str,Any]`, `edit_rationale: str|None` | Source/parent match origin rules |
| Graph | `graph_type: GraphType`, `graph_json: dict[str,Any]`, `content_hash: str`, `designated_outcome_node: str|None` | Edit is canonicalized, outcome node must exist |
| Lifecycle | `status: GraphVersionStatus`, `created_by: str`, `created_at: datetime|None` | Initial DRAFT; FIXED not re-edited |

| Method | Return | Behavior / error |
|---|---|---|
| `__post_init__()` | `None` | Checks origin via validate_origin |
| `validate_origin()` | `None` | Invalid origin/link combination raises `ValueError` |
| `apply_edit(graph_json, edit_rationale=None, designated_outcome_node=None, *, update_outcome=False)` | `None` | FIXED raises `GraphAlreadyFixed`; invalid outcome or missing edit reason raises `InvalidAnalysisSpec`; uses `canonical_graph` |
| `fix()` | `None` | FIXED→FIXED raises `InvalidStateTransition` |
| `validate_outcome()` | `None` | Invalid outcome raises `InvalidAnalysisSpec` |

**E11 caution:** This is Product GraphVersion; new local Graph fidelity and versioning cannot claim Product persistence without explicit ADR/Scope change. FCI circle/Temporal oracle behavior is not proven by this class alone.

## 6. `StoredArtifact` / `ArtifactStorePort`

**Responsibility:** Existing Product Artifact Port; exact semantics of `store/retrieve/exists/delete` are API obligations, not proof of E11 atomic multi-file delivery.

| Symbol | Fields / Signature |
|---|---|
| `StoredArtifact` frozen dataclass | `object_key: str`, `content_hash: str`, `size_bytes: int`, `media_type: str` |
| `ArtifactStorePort.store` | `(source_path: Path, object_key: str, media_type: str="application/octet-stream") -> StoredArtifact` |
| `ArtifactStorePort.retrieve` | `(object_key: str, dest_path: Path) -> None` |
| `ArtifactStorePort.exists` | `(object_key: str) -> bool` |
| `ArtifactStorePort.delete` | `(object_key: str) -> None` |

**E11 gap:** Local staging, atomic set commit, relative path sanitation and private CATE export constraints require separate reviewed design; existing Port alone does not guarantee these.

## 7. `CliManifest` (existing v2 local CLI)

**Responsibility:** Legacy manifest serialization; source marks snapshot_schema_version default `causal-analysis-spec/2`.

| Field group | Actual Python fields | Notes |
|---|---|---|
| Identity | `manifest_version: str`, `operation: str`, `algorithm_or_estimator: str` | Required |
| Inputs | `dataset: dict[str,Any]`, `graph: dict[str,Any]|None`, `parameters: dict[str,Any]`, `analysis_spec: dict[str,Any]` | Existing shape |
| Environment | `random_seed: int|None`, `code_version: str`, `runtime_versions: dict[str,str]`, `backend_version: str|None` | Existing provenance |
| Result | `scientific_status: str`, `result_summary: dict[str,Any]`, `artifacts: list[dict[str,Any]]=[]`, `warnings: list[Any]=[]`, `scientific_warnings: list[dict[str,Any]]=[]` | Mutable list within frozen dataclass: do not equate with deep immutability |
| Compat | `snapshot_schema_version: str="causal-analysis-spec/2"`, `analysis_mode: str|None`, `causal_question_hash: str|None`, `graph_origin: str|None`, `upstream_result_reference: str|None`, `identification_status: str|None`, `eligibility_status: str|None` | Legacy contract |

| Method | Return | Behavior |
|---|---|---|
| `to_dict(self)` | `dict[str,Any]` | `dataclasses.asdict(self)` |

**Negative:** E11 typed AR or revised GraphResult must not be shoehorned into v2 manifest without an explicitly versioned reader/writer and regression tests.

## 8. Verification boundary

These entries are source-inspected structural contracts, **not** proof of existing tests, successful E11 migration, scientific benchmark or independent Architecture Review. Each class needs source-linked test references and behavior-level evidence before reusing it as a normalized E11 component.
