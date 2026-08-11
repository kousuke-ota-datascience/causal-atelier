"""Execution domain entity."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ariadne.product.domain.enums import AnalysisFamily, ExecutionOperation, ExecutionStatus
from ariadne.product.domain.errors import InvalidStateTransition


CURRENT_SNAPSHOT_SCHEMA_VERSION = "causal-analysis-spec/2"
LEGACY_SNAPSHOT_SCHEMA_VERSION = "legacy-product-snapshot/1"


def _new_id() -> str:
    return str(uuid.uuid4())


@dataclass
class Execution:
    execution_id: str = field(default_factory=_new_id)
    project_id: str = ""
    analysis_family: AnalysisFamily = AnalysisFamily.CAUSAL
    dataset_version_id: str = ""
    input_graph_version_id: str | None = None
    input_result_id: str | None = None
    batch_key: str = field(default_factory=_new_id)
    operation: ExecutionOperation = ExecutionOperation.DISCOVERY
    objective_snapshot: str | None = None
    rationale_snapshot: str | None = None
    analysis_spec_json: dict[str, Any] = field(default_factory=dict)
    algorithm_or_estimator: str = ""
    parameter_json: dict[str, Any] = field(default_factory=dict)
    random_seed: int | None = None
    code_version: str = ""
    runtime_version_json: dict[str, Any] = field(default_factory=dict)
    snapshot_hash: str = ""
    snapshot_schema_version: str = CURRENT_SNAPSHOT_SCHEMA_VERSION
    status: ExecutionStatus = ExecutionStatus.QUEUED
    retry_count: int = 0
    last_error_summary: str | None = None
    requested_by: str = ""
    requested_at: datetime | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    base_execution_id: str | None = None
    revision_kind: str | None = None
    change_reason: str | None = None
    lease_owner: str | None = None
    lease_expires_at: datetime | None = None

    def __post_init__(self) -> None:
        self.validate_input_contract()

    def validate_input_contract(self) -> None:
        """Enforce the operation/input matrix before persistence."""
        if not isinstance(self.analysis_family, AnalysisFamily):
            self.analysis_family = AnalysisFamily(self.analysis_family)
        graph = self.input_graph_version_id is not None
        upstream = self.input_result_id is not None
        current = {
            ExecutionOperation.DISCOVERY: (False, False),
            ExecutionOperation.IDENTIFICATION: (True, False),
            ExecutionOperation.ESTIMATION: (True, True),
            ExecutionOperation.REFUTATION: (True, True),
            ExecutionOperation.SENSITIVITY: (True, True),
        }
        legacy = {
            ExecutionOperation.DISCOVERY: (False, False),
            ExecutionOperation.ESTIMATION: (True, False),
        }
        if self.snapshot_schema_version == CURRENT_SNAPSHOT_SCHEMA_VERSION:
            expected = current[self.operation]
        elif self.snapshot_schema_version == LEGACY_SNAPSHOT_SCHEMA_VERSION:
            expected = legacy.get(self.operation)
            if expected is None:
                raise ValueError(
                    f"Operation {self.operation.value} did not exist in the legacy snapshot contract"
                )
        else:
            raise ValueError("Unsupported snapshot_schema_version")
        if (graph, upstream) != expected:
            raise ValueError(
                f"Invalid inputs for {self.operation.value}: "
                f"graph={graph}, input_result={upstream}"
            )

    def mark_running(self, started_at: datetime) -> None:
        if self.status != ExecutionStatus.QUEUED:
            raise InvalidStateTransition("Execution", self.status, ExecutionStatus.RUNNING)
        self.status = ExecutionStatus.RUNNING
        self.started_at = started_at

    def mark_succeeded(self, finished_at: datetime) -> None:
        if self.status != ExecutionStatus.RUNNING:
            raise InvalidStateTransition("Execution", self.status, ExecutionStatus.SUCCEEDED)
        self.status = ExecutionStatus.SUCCEEDED
        self.finished_at = finished_at

    def mark_failed(self, finished_at: datetime, error_summary: str) -> None:
        if self.status != ExecutionStatus.RUNNING:
            raise InvalidStateTransition("Execution", self.status, ExecutionStatus.FAILED)
        self.status = ExecutionStatus.FAILED
        self.finished_at = finished_at
        self.last_error_summary = error_summary

    def request_cancel(self) -> None:
        if self.status not in (ExecutionStatus.QUEUED, ExecutionStatus.RUNNING):
            raise InvalidStateTransition("Execution", self.status, ExecutionStatus.CANCELLED)
        self.status = ExecutionStatus.CANCELLED

    def increment_retry(self) -> None:
        if self.status != ExecutionStatus.FAILED:
            raise InvalidStateTransition("Execution", self.status, ExecutionStatus.QUEUED)
        self.status = ExecutionStatus.QUEUED
        self.retry_count += 1
        self.started_at = None
        self.finished_at = None
        self.last_error_summary = None

    def set_lease(self, owner: str, expires_at: datetime) -> None:
        if not owner:
            raise ValueError("lease owner is required")
        self.lease_owner = owner
        self.lease_expires_at = expires_at

    def clear_lease(self) -> None:
        self.lease_owner = None
        self.lease_expires_at = None
