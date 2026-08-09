"""Stage execution state and append-only attempt history."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ariadne.product.domain.enums import StageExecutionStatus
from ariadne.product.domain.errors import InvalidStateTransition
from ariadne.product.domain.execution_plan import StageType


@dataclass
class StageAttempt:
    attempt_number: int
    worker_id: str
    started_at: datetime
    stage_attempt_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    finished_at: datetime | None = None
    error: dict[str, Any] | None = None


@dataclass
class StageExecution:
    stage_execution_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    execution_id: str = ""
    stage_key: str = ""
    stage_type: StageType = field(default_factory=lambda: StageType("core", "stage", "1"))
    ordinal: int = 0
    dependencies: tuple[str, ...] = ()
    status: StageExecutionStatus = StageExecutionStatus.PENDING
    input_binding: dict[str, Any] = field(default_factory=dict)
    output_binding: dict[str, Any] = field(default_factory=dict)
    attempts: list[StageAttempt] = field(default_factory=list)
    last_error: dict[str, Any] | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None

    def mark_ready(self) -> None:
        self._transition({StageExecutionStatus.PENDING}, StageExecutionStatus.READY)

    def start_attempt(self, worker_id: str, at: datetime) -> StageAttempt:
        self._transition({StageExecutionStatus.READY, StageExecutionStatus.FAILED}, StageExecutionStatus.RUNNING)
        attempt = StageAttempt(
            attempt_number=len(self.attempts) + 1,
            worker_id=worker_id,
            started_at=at,
        )
        self.attempts.append(attempt)
        self.started_at = at
        self.last_error = None
        return attempt

    def succeed(self, outputs: dict[str, Any], at: datetime) -> None:
        self._transition({StageExecutionStatus.RUNNING}, StageExecutionStatus.SUCCEEDED)
        self.output_binding = outputs
        self.finished_at = at
        self.attempts[-1].finished_at = at

    def fail(self, error: dict[str, Any], at: datetime) -> None:
        self._transition({StageExecutionStatus.RUNNING}, StageExecutionStatus.FAILED)
        self.last_error = error
        self.finished_at = at
        self.attempts[-1].finished_at = at
        self.attempts[-1].error = error

    def skip(self, at: datetime) -> None:
        self._transition(
            {StageExecutionStatus.PENDING, StageExecutionStatus.READY},
            StageExecutionStatus.SKIPPED_DUE_TO_PREREQUISITE,
        )
        self.finished_at = at

    def cancel(self, at: datetime, error: dict[str, Any] | None = None) -> None:
        self._transition(
            {StageExecutionStatus.PENDING, StageExecutionStatus.READY,
             StageExecutionStatus.RUNNING},
            StageExecutionStatus.CANCELLED,
        )
        self.last_error = error
        self.finished_at = at
        if self.attempts and self.attempts[-1].finished_at is None:
            self.attempts[-1].finished_at = at

    def _transition(self, allowed: set[StageExecutionStatus], target: StageExecutionStatus) -> None:
        if self.status not in allowed:
            raise InvalidStateTransition("StageExecution", self.status, target)
        self.status = target
