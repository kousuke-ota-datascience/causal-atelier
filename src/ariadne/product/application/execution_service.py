"""ExecutionService – submit execution batches and manage lifecycle."""

from __future__ import annotations

import hashlib
import json
import math
import uuid
from decimal import Decimal
from dataclasses import dataclass, field
from typing import Any

from ariadne.product.domain.enums import ExecutionOperation, GraphVersionStatus
from ariadne.product.domain.analysis_spec import SCHEMA_VERSION
from ariadne.product.domain.errors import (
    EntityNotFound,
    InvalidAnalysisSpec,
    ProjectBoundaryViolation,
    ScientificContractViolation,
)
from ariadne.product.domain.execution import Execution
from ariadne.product.ports.clock import ClockPort, SystemClock
from ariadne.product.application.scientific_validation_service import ScientificValidationService


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
    input_graph_version_id: str | None = None
    input_result_id: str | None = None
    code_version: str = ""
    runtime_version_json: dict[str, Any] = field(default_factory=dict)
    requested_by: str = "system"


@dataclass
class ExecutionBatchResult:
    batch_key: str
    execution_ids: list[str]


class ExecutionService:
    def __init__(self, uow_factory: Any, clock: ClockPort | None = None) -> None:
        self._uow_factory = uow_factory
        self._clock = clock or SystemClock()
        self._validation = ScientificValidationService()

    def create_execution_batch(self, command: CreateExecutionBatchCommand) -> ExecutionBatchResult:
        if not command.variants:
            raise InvalidAnalysisSpec("At least one variant is required")
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

        now = self._clock.now()
        batch_key = str(uuid.uuid4())

        with self._uow_factory() as uow:
            project = uow.projects.get(command.project_id)
            if project is None:
                raise EntityNotFound("Project", command.project_id)

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
                self._validation.validate_submission(
                    uow=uow,
                    project_id=command.project_id,
                    dataset_version_id=command.dataset_version_id,
                    graph_version_id=command.input_graph_version_id,
                    input_result_id=command.input_result_id,
                    operation=command.operation,
                    analysis_spec=variant.analysis_spec_json,
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
                    analysis_spec_json=variant.analysis_spec_json,
                    code_version=command.code_version,
                    runtime_version_json=command.runtime_version_json,
                )
                execution = Execution(
                    project_id=command.project_id,
                    dataset_version_id=command.dataset_version_id,
                    input_graph_version_id=command.input_graph_version_id,
                    input_result_id=command.input_result_id,
                    batch_key=batch_key,
                    operation=command.operation,
                    objective_snapshot=variant.objective_snapshot,
                    rationale_snapshot=variant.rationale_snapshot,
                    analysis_spec_json=variant.analysis_spec_json,
                    algorithm_or_estimator=variant.algorithm_or_estimator,
                    parameter_json=variant.parameter_json,
                    random_seed=variant.random_seed,
                    code_version=command.code_version,
                    runtime_version_json=command.runtime_version_json,
                    snapshot_hash=snapshot_hash,
                    snapshot_schema_version=SCHEMA_VERSION,
                    requested_by=command.requested_by,
                    requested_at=now,
                )
                executions.append(execution)

            uow.executions.add_many(executions)
            uow.commit()

        return ExecutionBatchResult(
            batch_key=batch_key,
            execution_ids=[e.execution_id for e in executions],
        )

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
            execution.request_cancel()
            uow.executions.update(execution)
            uow.commit()

    def retry_execution(self, execution_id: str) -> None:
        with self._uow_factory() as uow:
            execution = uow.executions.get(execution_id)
            if execution is None:
                raise EntityNotFound("Execution", execution_id)
            execution.increment_retry()
            uow.executions.update(execution)
            uow.commit()


def _compute_snapshot_hash(**kwargs: Any) -> str:
    canonical = canonical_snapshot_json(kwargs).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def canonical_snapshot_json(value: Any) -> str:
    """Serialize snapshot input with deterministic key, NULL, and number rules."""
    return json.dumps(_canonicalize(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


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
