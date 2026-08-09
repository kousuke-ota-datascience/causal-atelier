"""Canonical, persistence-neutral materialization of workflow stage skeletons."""

from __future__ import annotations

from ariadne.product.domain.errors import InvalidExecutionPlan
from ariadne.product.domain.execution import Execution
from ariadne.product.domain.execution_plan import ExecutionPlan
from ariadne.product.domain.stage_execution import StageExecution


class StagePlanMaterializer:
    """Build stable StageExecution identities from one family workflow plan."""

    @staticmethod
    def materialize(execution: Execution, plan: ExecutionPlan) -> list[StageExecution]:
        if not plan.stages:
            raise InvalidExecutionPlan("EMPTY_STAGE_PLAN", "Canonical execution requires a stage")
        if plan.analysis_family != execution.analysis_family:
            raise InvalidExecutionPlan("FAMILY_MISMATCH", "Execution and plan families differ")
        definitions = {stage.stage_key: stage for stage in plan.stages}
        if len(definitions) != len(plan.stages):
            raise InvalidExecutionPlan("DUPLICATE_STAGE", "Stage keys must be unique")
        dependencies: dict[str, list[str]] = {key: [] for key in definitions}
        for binding in plan.dependencies:
            if binding.source_stage_key not in definitions or binding.target_stage_key not in definitions:
                raise InvalidExecutionPlan("UNKNOWN_STAGE_DEPENDENCY", "Dependency references an unknown stage")
            if binding.source_stage_key not in dependencies[binding.target_stage_key]:
                dependencies[binding.target_stage_key].append(binding.source_stage_key)

        order: list[str] = []
        remaining = set(definitions)
        while remaining:
            ready = sorted(
                key for key in remaining
                if all(parent in order for parent in dependencies[key])
            )
            if not ready:
                raise InvalidExecutionPlan("PLAN_CYCLE", "Stage dependencies contain a cycle")
            order.extend(ready)
            remaining.difference_update(ready)

        return [StageExecution(
            execution_id=execution.execution_id,
            stage_key=key,
            stage_type=definitions[key].stage_type,
            ordinal=ordinal,
            dependencies=tuple(dependencies[key]),
        ) for ordinal, key in enumerate(order)]
