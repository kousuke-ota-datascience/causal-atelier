"""Canonical application boundary for persistent StageExecution lifecycle."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from ariadne.product.domain.enums import ExecutionStatus, StageExecutionStatus
from ariadne.product.domain.errors import EntityNotFound, InvalidStateTransition
from ariadne.product.domain.execution_plan import ExecutionPlan
from ariadne.product.domain.stage_execution import StageExecution
from ariadne.product.workflow.stage_materialization import StagePlanMaterializer


class StageExecutionService:
    def __init__(self, uow_factory: Any, clock: Any) -> None:
        self._uow_factory = uow_factory
        self._clock = clock

    def materialize(self, execution: Any, plan: ExecutionPlan) -> list[StageExecution]:
        stages = StagePlanMaterializer.materialize(execution, plan)
        with self._uow_factory() as uow:
            uow.stage_executions.add_many(stages)
            uow.commit()
        return stages

    def list_for_execution(self, execution_id: str) -> list[StageExecution]:
        with self._uow_factory() as uow:
            return uow.stage_executions.list_for_execution(execution_id)

    def start_attempt(self, stage_execution_id: str, *, owner: str, worker_id: str) -> None:
        at = self._clock.now()
        with self._uow_factory() as uow:
            stage = uow.stage_executions.get(stage_execution_id)
            if stage is None:
                raise EntityNotFound("StageExecution", stage_execution_id)
            uow.stage_executions.start_attempt(stage, owner=owner, worker_id=worker_id, at=at)
            uow.commit()

    def update(self, stage: StageExecution, *, owner: str) -> None:
        with self._uow_factory() as uow:
            uow.stage_executions.update(stage, owner=owner)
            uow.commit()

    def cancel_for_execution(self, execution_id: str, *, owner: str | None = None) -> None:
        at = self._clock.now()
        with self._uow_factory() as uow:
            stages = uow.stage_executions.list_for_execution(execution_id)
            for stage in stages:
                if stage.status not in {
                    StageExecutionStatus.SUCCEEDED,
                    StageExecutionStatus.SKIPPED_DUE_TO_PREREQUISITE,
                    StageExecutionStatus.CANCELLED,
                }:
                    stage.cancel(at)
                    uow.stage_executions.update(stage, owner=owner)
            uow.commit()
