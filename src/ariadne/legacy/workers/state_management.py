"""Durable outbox claiming and delivery state management."""

from __future__ import annotations

import platform
from datetime import timedelta
from pathlib import Path
from typing import Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

from ariadne.infrastructure.persistence import Database
from ariadne.infrastructure.persistence import models as m
from ariadne import __version__
from ariadne.application.run_execution import ExecutionService

Dispatch = Callable[[Session, m.OutboxEvent], None]


class OutboxConsumer:
    def __init__(
        self,
        database: Database,
        *,
        worker_id: str,
        lease_seconds: int,
    ) -> None:
        self.database = database
        self.worker_id = worker_id
        self.lease_seconds = lease_seconds

    def consume_one(self, dispatch: Dispatch) -> bool:
        event_id = self._claim_one()
        if event_id is None:
            return False
        with self.database.session() as session:
            event = session.get(m.OutboxEvent, event_id)
            if event is None:
                return False
            try:
                dispatch(session, event)
                event.published_at = m.utcnow()
                event.last_error = None
            except Exception as exc:
                event.last_error = str(exc)[:4000]
                if event.event_type in {
                    "EXECUTE_EXECUTION",
                    "PROFILE_DATASET_TABLE",
                    "EXECUTE_VISUALIZATION_QUERY",
                    "CANCEL_EXECUTION",
                }:
                    event.published_at = m.utcnow()
                else:
                    event.claimed_at = None
                    event.claimed_by = None
                    raise
            event.claimed_at = None
            event.claimed_by = None
            return True

    def _claim_one(self) -> str | None:
        with self.database.session() as session:
            stale_before = m.utcnow() - timedelta(seconds=self.lease_seconds)
            event = session.scalar(
                select(m.OutboxEvent)
                .where(
                    m.OutboxEvent.published_at.is_(None),
                    (m.OutboxEvent.claimed_at.is_(None))
                    | (m.OutboxEvent.claimed_at < stale_before),
                )
                .order_by(m.OutboxEvent.created_at)
                .with_for_update(skip_locked=True)
            )
            if event is None:
                return None
            event.publish_attempts += 1
            event.claimed_at = m.utcnow()
            event.claimed_by = self.worker_id
            return event.id


class ExecutionStateManager:
    def __init__(
        self,
        *,
        worker_id: str,
        lease_seconds: int,
        workspace_root: Path,
    ) -> None:
        self.worker_id = worker_id
        self.lease_seconds = lease_seconds
        self.workspace_root = workspace_root

    def create_attempt(
        self, session: Session, stage: m.StageExecution
    ) -> m.StageAttempt:
        stale_attempts = session.scalars(
            select(m.StageAttempt).where(
                m.StageAttempt.stage_execution_id == stage.id,
                m.StageAttempt.status.in_({"CREATED", "QUEUED", "LEASED", "RUNNING"}),
            )
        ).all()
        for stale in stale_attempts:
            stale.status = "LOST"
            stale.finished_at = m.utcnow()
            stale.error_code = "WORKER_LEASE_LOST"
            stale.error_message = (
                "A replacement worker reclaimed the stage after its lease expired"
            )
        attempt = m.StageAttempt(
            stage_execution_id=stage.id,
            attempt_number=stage.current_attempt_number + 1,
            status="RUNNING",
            worker_id=self.worker_id,
            queued_at=m.utcnow(),
            leased_at=m.utcnow(),
            lease_expires_at=m.utcnow() + timedelta(seconds=self.lease_seconds),
            heartbeat_at=m.utcnow(),
            started_at=m.utcnow(),
            runtime_metadata_json={
                "python": platform.python_version(),
                "platform": platform.platform(),
                "package_version": __version__,
            },
        )
        stage.current_attempt_number = attempt.attempt_number
        stage.status = "RUNNING"
        stage.started_at = m.utcnow()
        session.add(attempt)
        session.flush()
        workspace = self.workspace_root / attempt.id
        workspace.mkdir(parents=True, exist_ok=False)
        attempt.workspace_ref = str(workspace)
        return attempt

    def finish_cancelled(
        self, session: Session, run: m.Execution, service: ExecutionService
    ) -> None:
        run.status = "CANCELLED"
        run.finished_at = m.utcnow()
        for stage in session.scalars(
            select(m.StageExecution).where(m.StageExecution.execution_id == run.id)
        ).all():
            if stage.status not in {"SUCCEEDED", "FAILED", "CANCELLED"}:
                stage.status = "CANCELLED"
                stage.finished_at = m.utcnow()
        service.add_event(run.id, "EXECUTION_CANCELLED", {"best_effort": True})

    def bind_dependency_artifacts(
        self, session: Session, stage: m.StageExecution
    ) -> None:
        dependencies = session.scalars(
            select(m.StageExecutionDependency).where(
                m.StageExecutionDependency.stage_execution_id == stage.id
            )
        ).all()
        for dependency in dependencies:
            upstream = session.get(m.StageExecution, dependency.depends_on_stage_execution_id)
            outputs = session.scalars(
                select(m.StageExecutionArtifactOutput).where(
                    m.StageExecutionArtifactOutput.stage_execution_id == upstream.id
                )
            ).all()
            for output in outputs:
                input_name = f"{upstream.stage_key}.{output.output_name}"[:255]
                if session.get(m.StageExecutionArtifactInput, (stage.id, input_name)) is None:
                    session.add(
                        m.StageExecutionArtifactInput(
                            stage_execution_id=stage.id,
                            input_name=input_name,
                            artifact_id=output.artifact_id,
                        )
                    )


__all__ = ["OutboxConsumer", "ExecutionStateManager"]
