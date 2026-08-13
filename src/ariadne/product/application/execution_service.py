"""ExecutionService – submit execution batches and manage lifecycle."""

from __future__ import annotations

import hashlib
import json
import math
import uuid
import platform
from importlib.metadata import PackageNotFoundError, version
from decimal import Decimal
from dataclasses import dataclass, field
from typing import Any

from ariadne.product.domain.enums import AnalysisFamily, ExecutionOperation, GraphVersionStatus
from ariadne.product.domain.analysis_spec import SCHEMA_VERSION
from ariadne.product.domain.errors import (
    EntityNotFound,
    GraphOutcomeMismatch,
    GraphOutcomeRequired,
    InvalidAnalysisSpec,
    ProjectBoundaryViolation,
    ScientificContractViolation,
)
from ariadne.product.domain.execution import Execution
from ariadne.product.domain.enums import StageExecutionStatus
from ariadne.product.domain.execution_plan import ExecutionPlan
from ariadne.product.ports.clock import ClockPort, SystemClock
from ariadne.product.application.scientific_validation_service import ScientificValidationService
from ariadne.product.application.project_policy import require_active_project
from ariadne.product.workflow.stage_materialization import StagePlanMaterializer
from ariadne.product.workflow.canonical_plan_provider import CanonicalPlanProvider


@dataclass
class ExecutionVariantSpec:
    algorithm_or_estimator: str
    parameter_json: dict[str, Any] = field(default_factory=dict)
    random_seed: int | None = None
    analysis_spec_json: dict[str, Any] = field(default_factory=dict)
    objective_snapshot: str | None = None
    rationale_snapshot: str | None = None


@dataclass
class CreateExecutionBatchCommand:
    project_id: str
    dataset_version_id: str
    operation: ExecutionOperation
    variants: list[ExecutionVariantSpec]
    analysis_family: AnalysisFamily = AnalysisFamily.CAUSAL
    input_graph_version_id: str | None = None
    input_result_id: str | None = None
    code_version: str = ""
    runtime_version_json: dict[str, Any] = field(default_factory=dict)
    requested_by: str = "system"
    base_execution_id: str | None = None
    change_reason: str | None = None


@dataclass
class ExecutionBatchResult:
    batch_key: str
    execution_ids: list[str]
    scientific_warnings_by_execution: dict[str, list[dict[str, Any]]] = field(default_factory=dict)


class ExecutionService:
    def __init__(
        self,
        uow_factory: Any,
        clock: ClockPort | None = None,
        plan_provider: Any | None = None,
    ) -> None:
        self._uow_factory = uow_factory
        self._clock = clock or SystemClock()
        self._validation = ScientificValidationService()
        self._plan_provider = plan_provider

    def _plan_for(self, execution: Execution) -> ExecutionPlan:
        if self._plan_provider is not None:
            plan = self._plan_provider(execution)
        else:
            try:
                plan = CanonicalPlanProvider()(execution)
            except Exception as exc:
                raise InvalidAnalysisSpec(
                    "Canonical family workflow plan materialization failed: "
                    f"{execution.analysis_family.value}"
                ) from exc
        if not isinstance(plan, ExecutionPlan):
            raise InvalidAnalysisSpec("Canonical planner returned an invalid ExecutionPlan")
        return plan

    def create_execution_batch(self, command: CreateExecutionBatchCommand) -> ExecutionBatchResult:
        command.runtime_version_json = _runtime_manifest(command.runtime_version_json, command.code_version)
        if not command.variants:
            raise InvalidAnalysisSpec("At least one variant is required")
        if not isinstance(command.analysis_family, AnalysisFamily):
            command.analysis_family = AnalysisFamily(command.analysis_family)
        # DISCOVERY is the common Product submission envelope for the two
        # non-causal families.  Their scientific contract is deliberately kept
        # in ``family_spec``; it must not be validated as a causal question.
        is_causal = command.analysis_family is AnalysisFamily.CAUSAL
        graph_required = command.operation != ExecutionOperation.DISCOVERY
        upstream_required = command.operation in {
            ExecutionOperation.ESTIMATION,
            ExecutionOperation.REFUTATION,
            ExecutionOperation.SENSITIVITY,
        }
        if (command.input_graph_version_id is not None) != graph_required:
            raise InvalidAnalysisSpec("input_graph_version_id does not match operation")
        if (command.input_result_id is not None) != upstream_required:
            raise ScientificContractViolation(
                "UPSTREAM_RESULT_REQUIRED" if upstream_required else "UPSTREAM_RESULT_INCOMPATIBLE",
                "input_result_id does not match operation",
            )
        if command.base_execution_id is None and command.change_reason is not None:
            raise InvalidAnalysisSpec("change_reason requires base_execution_id")

        now = self._clock.now()
        batch_key = str(uuid.uuid4())

        with self._uow_factory() as uow:
            project = uow.projects.get(command.project_id)
            if project is None:
                raise EntityNotFound("Project", command.project_id)
            require_active_project(project)

            base_execution = None
            if command.base_execution_id is not None:
                base_execution = uow.executions.get(command.base_execution_id)
                if base_execution is None:
                    raise EntityNotFound("Execution", command.base_execution_id)
                if base_execution.project_id != command.project_id:
                    raise ProjectBoundaryViolation("Base Execution does not belong to project")
                if base_execution.analysis_family != command.analysis_family:
                    raise InvalidAnalysisSpec("rerun/revise cannot change analysis family")

            dataset_version = uow.dataset_versions.get(command.dataset_version_id)
            if dataset_version is None:
                raise EntityNotFound("DatasetVersion", command.dataset_version_id)
            if dataset_version.project_id != command.project_id:
                raise ProjectBoundaryViolation("DatasetVersion does not belong to project")

            if command.input_graph_version_id is not None:
                gv = uow.graph_versions.get(command.input_graph_version_id)
                if gv is None:
                    raise EntityNotFound("GraphVersion", command.input_graph_version_id)
                if gv.project_id != command.project_id:
                    raise ProjectBoundaryViolation("GraphVersion does not belong to project")
                if gv.status != GraphVersionStatus.FIXED:
                    raise InvalidAnalysisSpec("Operation requires a FIXED GraphVersion")

            graph_content_hash = gv.content_hash if command.input_graph_version_id else None

            executions: list[Execution] = []
            for variant in command.variants:
                analysis_spec = _strip_generated_snapshot_fields(variant.analysis_spec_json)
                dataset_columns = _dataset_columns(dataset_version.schema_json)
                if is_causal and command.operation == ExecutionOperation.DISCOVERY:
                    operation_spec = analysis_spec.get("operation_spec", {})
                    unknown = [
                        item for item in operation_spec.get("feature_columns", [])
                        if item not in dataset_columns
                    ]
                    if unknown:
                        raise InvalidAnalysisSpec(f"Unknown feature columns: {unknown}")
                    outcome = operation_spec.get("designated_outcome_node")
                    if outcome is not None and outcome not in dataset_columns:
                        raise InvalidAnalysisSpec("designated outcome is not in Dataset schema")
                elif is_causal and command.operation in {
                    ExecutionOperation.IDENTIFICATION, ExecutionOperation.ESTIMATION,
                }:
                    if not gv.designated_outcome_node:
                        raise GraphOutcomeRequired("FIXED Graph Version has no designated outcome")
                    if gv.designated_outcome_node not in dataset_columns:
                        raise GraphOutcomeRequired("Graph designated outcome is not in Dataset schema")
                    submitted_outcome = analysis_spec.get("causal_question", {}).get("outcome")
                    if submitted_outcome != gv.designated_outcome_node:
                        raise GraphOutcomeMismatch(
                            "Causal Question outcome does not match Graph designated outcome"
                        )
                warnings = _post_selection_inference_warnings(
                    uow=uow,
                    project_id=command.project_id,
                    dataset_version_id=command.dataset_version_id,
                    operation=command.operation,
                    analysis_mode=analysis_spec.get("analysis_mode"),
                )
                if warnings:
                    analysis_spec["scientific_warnings"] = warnings
                revision_context = None
                if base_execution is not None:
                    revision_context = _build_revision_context(
                        base=base_execution,
                        command=command,
                        variant=variant,
                        analysis_spec=analysis_spec,
                    )
                    analysis_spec["revision_context"] = revision_context
                if is_causal:
                    self._validation.validate_submission(
                        uow=uow,
                        project_id=command.project_id,
                        dataset_version_id=command.dataset_version_id,
                        graph_version_id=command.input_graph_version_id,
                        input_result_id=command.input_result_id,
                        operation=command.operation,
                        analysis_spec=analysis_spec,
                        method=variant.algorithm_or_estimator,
                        parameters=variant.parameter_json,
                    )
                snapshot_hash = _compute_snapshot_hash(
                    objective=variant.objective_snapshot,
                    rationale=variant.rationale_snapshot,
                    dataset_version_id=command.dataset_version_id,
                    dataset_content_hash=dataset_version.content_hash,
                    input_graph_version_id=command.input_graph_version_id,
                    input_graph_content_hash=graph_content_hash,
                    input_result_id=command.input_result_id,
                    operation=command.operation,
                    algorithm_or_estimator=variant.algorithm_or_estimator,
                    parameter_json=variant.parameter_json,
                    random_seed=variant.random_seed,
                    analysis_spec_json=analysis_spec,
                    code_version=command.code_version,
                    runtime_version_json=command.runtime_version_json,
                )
                execution = Execution(
                    project_id=command.project_id,
                    analysis_family=command.analysis_family,
                    dataset_version_id=command.dataset_version_id,
                    input_graph_version_id=command.input_graph_version_id,
                    input_result_id=command.input_result_id,
                    batch_key=batch_key,
                    operation=command.operation,
                    objective_snapshot=variant.objective_snapshot,
                    rationale_snapshot=variant.rationale_snapshot,
                    analysis_spec_json=analysis_spec,
                    algorithm_or_estimator=variant.algorithm_or_estimator,
                    parameter_json=variant.parameter_json,
                    random_seed=variant.random_seed,
                    code_version=command.code_version,
                    runtime_version_json=command.runtime_version_json,
                    snapshot_hash=snapshot_hash,
                    snapshot_schema_version=SCHEMA_VERSION,
                    requested_by=command.requested_by,
                    requested_at=now,
                    base_execution_id=base_execution.execution_id if base_execution else None,
                    revision_kind=revision_context["revision_kind"] if revision_context else None,
                    change_reason=revision_context["change_reason"] if revision_context else None,
                )
                executions.append(execution)

            stages = []
            for execution in executions:
                stages.extend(
                    StagePlanMaterializer.materialize(execution, self._plan_for(execution))
                )
            uow.executions.add_many(executions)
            uow.stage_executions.add_many(stages)
            uow.commit()

        return ExecutionBatchResult(
            batch_key=batch_key,
            execution_ids=[e.execution_id for e in executions],
            scientific_warnings_by_execution={
                e.execution_id: list(e.analysis_spec_json.get("scientific_warnings", []))
                for e in executions
            },
        )

    def create_family_execution(
        self,
        *,
        project_id: str,
        dataset_version_id: str,
        analysis_family: AnalysisFamily,
        family_spec: dict[str, Any],
        requested_by: str,
        analysis_view_id: str | None = None,
        analysis_specification_id: str | None = None,
        execution_plan_id: str | None = None,
        seed: int | None = None,
        code_version: str = "",
        runtime_version_json: dict[str, Any] | None = None,
        base_execution_id: str | None = None,
        change_reason: str | None = None,
    ) -> Execution:
        """Submit a non-causal family through the canonical lifecycle.

        Family-specific identifiers remain immutable input snapshots.  They are
        not a second lifecycle or a persistence authority.
        """
        if analysis_family is AnalysisFamily.CAUSAL:
            raise InvalidAnalysisSpec("create_family_execution is for non-causal families")
        result = self.create_execution_batch(CreateExecutionBatchCommand(
            project_id=project_id,
            dataset_version_id=dataset_version_id,
            operation=ExecutionOperation.DISCOVERY,
            analysis_family=analysis_family,
            variants=[ExecutionVariantSpec(
                algorithm_or_estimator=f"{analysis_family.value.lower()}-workflow",
                random_seed=seed,
                analysis_spec_json={
                    "family_spec": family_spec,
                    "analysis_view_id": analysis_view_id,
                    "analysis_specification_id": analysis_specification_id,
                    "execution_plan_id": execution_plan_id,
                },
            )],
            code_version=code_version,
            runtime_version_json=runtime_version_json or {},
            requested_by=requested_by,
            base_execution_id=base_execution_id,
            change_reason=change_reason,
        ))
        return self.get_execution(result.execution_ids[0])

    def get_execution(self, execution_id: str) -> Execution:
        with self._uow_factory() as uow:
            execution = uow.executions.get(execution_id)
            if execution is None:
                raise EntityNotFound("Execution", execution_id)
            return execution

    def get_prefill(self, execution_id: str) -> dict[str, Any]:
        execution = self.get_execution(execution_id)
        return {
            "operation": execution.operation.value,
            "dataset_version_id": execution.dataset_version_id,
            "input_graph_version_id": execution.input_graph_version_id,
            "input_result_id": execution.input_result_id,
            "objective": execution.objective_snapshot,
            "rationale": execution.rationale_snapshot,
            "analysis_spec": execution.analysis_spec_json,
            "algorithm_or_estimator": execution.algorithm_or_estimator,
            "parameters": execution.parameter_json,
            "random_seed": execution.random_seed,
        }

    def request_cancel(self, execution_id: str) -> None:
        with self._uow_factory() as uow:
            execution = uow.executions.get(execution_id)
            if execution is None:
                raise EntityNotFound("Execution", execution_id)
            project = uow.projects.get(execution.project_id)
            if project is None:
                raise EntityNotFound("Project", execution.project_id)
            require_active_project(project)
            execution.request_cancel()
            uow.executions.update(execution)
            for stage in uow.stage_executions.list_for_execution(execution_id):
                if stage.status not in {
                    StageExecutionStatus.SUCCEEDED,
                    StageExecutionStatus.SKIPPED_DUE_TO_PREREQUISITE,
                    StageExecutionStatus.CANCELLED,
                }:
                    stage.cancel(self._clock.now())
                    uow.stage_executions.update(stage)
            uow.commit()

    def retry_execution(self, execution_id: str) -> None:
        with self._uow_factory() as uow:
            execution = uow.executions.get(execution_id)
            if execution is None:
                raise EntityNotFound("Execution", execution_id)
            project = uow.projects.get(execution.project_id)
            if project is None:
                raise EntityNotFound("Project", execution.project_id)
            require_active_project(project)
            execution.increment_retry()
            uow.executions.update(execution)
            for stage in uow.stage_executions.list_for_execution(execution_id):
                if stage.status is StageExecutionStatus.FAILED:
                    stage.prepare_retry()
                    uow.stage_executions.update(stage)
            uow.commit()


def _compute_snapshot_hash(**kwargs: Any) -> str:
    canonical = canonical_snapshot_json(kwargs).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _strip_generated_snapshot_fields(value: dict[str, Any]) -> dict[str, Any]:
    return {
        key: item for key, item in value.items()
        if key not in {"revision_context", "scientific_warnings"}
    }


def _post_selection_inference_warnings(
    *,
    uow: Any,
    project_id: str,
    dataset_version_id: str,
    operation: ExecutionOperation,
    analysis_mode: Any,
) -> list[dict[str, Any]]:
    if operation != ExecutionOperation.ESTIMATION or analysis_mode != "CONFIRMATORY":
        return []
    source_ids = sorted({
        execution.execution_id
        for execution in uow.executions.list_by_project(project_id)
        if execution.operation == ExecutionOperation.DISCOVERY
        and execution.dataset_version_id == dataset_version_id
    })
    if not source_ids:
        return []
    return [{
        "warning_code": "POST_SELECTION_INFERENCE_RISK",
        "message": (
            "Confirmatory estimation follows graph discovery on the same Dataset Version; "
            "post-selection inference may invalidate nominal uncertainty."
        ),
        "source_discovery_execution_ids": source_ids,
        "dataset_version_id": dataset_version_id,
        "rationale": (
            "A prior DISCOVERY Execution used the same immutable Dataset Version in this Project."
        ),
    }]


def _build_revision_context(
    *,
    base: Execution,
    command: CreateExecutionBatchCommand,
    variant: ExecutionVariantSpec,
    analysis_spec: dict[str, Any],
) -> dict[str, Any]:
    base_conditions = {
        "dataset_version_id": base.dataset_version_id,
        "input_graph_version_id": base.input_graph_version_id,
        "input_result_id": base.input_result_id,
        "operation": base.operation.value,
        "objective": base.objective_snapshot,
        "rationale": base.rationale_snapshot,
        "analysis_spec": _strip_generated_snapshot_fields(base.analysis_spec_json),
        "algorithm_or_estimator": base.algorithm_or_estimator,
        "parameters": base.parameter_json,
        "random_seed": base.random_seed,
        "code_version": base.code_version,
        "runtime_versions": base.runtime_version_json,
    }
    proposed_conditions = {
        "dataset_version_id": command.dataset_version_id,
        "input_graph_version_id": command.input_graph_version_id,
        "input_result_id": command.input_result_id,
        "operation": command.operation.value,
        "objective": variant.objective_snapshot,
        "rationale": variant.rationale_snapshot,
        "analysis_spec": _strip_generated_snapshot_fields(analysis_spec),
        "algorithm_or_estimator": variant.algorithm_or_estimator,
        "parameters": variant.parameter_json,
        "random_seed": variant.random_seed,
        "code_version": command.code_version,
        "runtime_versions": command.runtime_version_json,
    }
    changed = _changed_dimensions(base_conditions, proposed_conditions)
    reason = command.change_reason.strip() if isinstance(command.change_reason, str) else None
    if changed and not reason:
        raise ScientificContractViolation(
            "EXECUTION_CHANGE_REASON_REQUIRED",
            "A changed Execution requires a non-empty change_reason",
        )
    return {
        "base_execution_id": base.execution_id,
        "base_snapshot_hash": base.snapshot_hash,
        "revision_kind": "REVISED" if changed else "RERUN",
        "change_reason": reason if changed else None,
        "changed_dimensions": changed,
    }


def _changed_dimensions(left: Any, right: Any, prefix: str = "") -> list[str]:
    if isinstance(left, dict) and isinstance(right, dict):
        changed: list[str] = []
        for key in sorted(set(left) | set(right)):
            path = f"{prefix}.{key}" if prefix else key
            if key not in left or key not in right:
                changed.append(path)
            else:
                changed.extend(_changed_dimensions(left[key], right[key], path))
        return changed
    return [] if left == right else [prefix]


def canonical_snapshot_json(value: Any) -> str:
    """Serialize snapshot input with deterministic key, NULL, and number rules."""
    return json.dumps(_canonicalize(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _dataset_columns(schema_json: Any) -> set[str]:
    if isinstance(schema_json, dict):
        fields = schema_json.get("fields")
        if isinstance(fields, list):
            return {
                str(item["name"])
                for item in fields
                if isinstance(item, dict) and isinstance(item.get("name"), str)
            }
        return {str(name) for name in schema_json}
    return set()


def _canonicalize(value: Any) -> Any:
    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, int):
        return {"$number": str(value)}
    if isinstance(value, float):
        if not math.isfinite(value):
            raise InvalidAnalysisSpec("Snapshot numbers must be finite")
        number = Decimal(repr(value))
        if number == 0:
            number = Decimal(0)
        return {"$number": format(number.normalize(), "f")}
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise InvalidAnalysisSpec("Snapshot object keys must be strings")
        return {key: _canonicalize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_canonicalize(item) for item in value]
    raise InvalidAnalysisSpec(f"Snapshot contains unsupported value: {type(value).__name__}")


def _runtime_manifest(existing: dict[str, Any], code_version: str) -> dict[str, Any]:
    """Record the actual execution environment without importing optional deps."""
    libraries: dict[str, str] = {}
    for package in ("numpy", "pandas", "scikit-learn", "scipy", "networkx", "pyarrow"):
        try:
            libraries[package] = version(package)
        except PackageNotFoundError:
            continue
    return {
        **existing,
        "ariadne_code_version": code_version,
        "python_version": platform.python_version(),
        "platform_system": platform.system(),
        "platform_release": platform.release(),
        "machine": platform.machine(),
        "libraries": libraries,
    }
