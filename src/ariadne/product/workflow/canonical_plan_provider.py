"""Common family-to-plan adapter used by the canonical Execution boundary."""

from __future__ import annotations

from typing import Any

from ariadne.capabilities.causal.workflow import CausalPlanner
from ariadne.capabilities.exploratory.planner import ExploratoryPlanner
from ariadne.capabilities.predictive.planner import PredictivePlanner
from ariadne.product.domain.enums import AnalysisFamily
from ariadne.product.domain.execution import Execution
from ariadne.product.domain.execution_plan import ExecutionPlan


class CanonicalPlanProvider:
    """Materialize one common plan contract while retaining family planners."""

    def __call__(self, execution: Execution) -> ExecutionPlan:
        family_spec: dict[str, Any] = execution.analysis_spec_json.get("family_spec", execution.analysis_spec_json)
        if execution.analysis_family is AnalysisFamily.CAUSAL:
            return CausalPlanner().build_for_execution(execution)
        if execution.analysis_family is AnalysisFamily.EXPLORATORY:
            return ExploratoryPlanner().build_for_spec(
                project_id=execution.project_id,
                specification_id=execution.snapshot_hash,
                family_spec=family_spec,
            )
        if execution.analysis_family is AnalysisFamily.PREDICTIVE:
            return PredictivePlanner().build_full_plan(
                project_id=execution.project_id,
                specification_id=execution.snapshot_hash,
                family_spec=family_spec,
            )
        raise ValueError(f"Unsupported canonical analysis family: {execution.analysis_family}")
