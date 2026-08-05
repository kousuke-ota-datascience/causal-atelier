"""ExecutionService – submit execution batches and manage lifecycle."""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from typing import Any

from ariadne.product.domain.enums import ExecutionOperation
from ariadne.product.domain.errors import (
    EntityNotFound,
    InvalidAnalysisSpec,
    ProjectBoundaryViolation,
)
from ariadne.product.domain.execution import Execution
from ariadne.product.ports.clock import ClockPort, SystemClock


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

    def create_execution_batch(self, command: CreateExecutionBatchCommand) -> ExecutionBatchResult:
        if not command.variants:
            raise InvalidAnalysisSpec("At least one variant is required")
        if command.operation == ExecutionOperation.ESTIMATION and command.input_graph_version_id is None:
            raise InvalidAnalysisSpec("input_graph_version_id is required for ESTIMATION")
        if command.operation == ExecutionOperation.DISCOVERY and command.input_graph_version_id is not None:
            raise InvalidAnalysisSpec("input_graph_version_id must be None for DISCOVERY")

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

            executions: list[Execution] = []
            for variant in command.variants:
                snapshot_hash = _compute_snapshot_hash(
                    dataset_version_id=command.dataset_version_id,
                    dataset_content_hash=dataset_version.content_hash,
                    input_graph_version_id=command.input_graph_version_id,
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
    canonical = json.dumps(
        {k: kwargs[k] for k in sorted(kwargs)},
        sort_keys=True,
        default=str,
    ).encode()
    return hashlib.sha256(canonical).hexdigest()
