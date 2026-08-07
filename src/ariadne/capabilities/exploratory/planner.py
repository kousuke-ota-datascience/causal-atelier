from __future__ import annotations

from typing import Any

from ariadne.product.domain.enums import AnalysisFamily
from ariadne.product.domain.execution_plan import ExecutionPlan, StageDefinition, StageType

_RUNNER_NAMES = {
    "PROFILE": "profile", "DISTRIBUTION": "distribution", "ASSOCIATION": "association",
    "GROUP_SUMMARY": "aggregate", "TIME_TREND": "time_trend", "CHART": "chart",
}


class ExploratoryPlanner:
    family = AnalysisFamily.EXPLORATORY
    spec_versions = frozenset({"exploratory-analysis-spec/1"})
    planner_id = "exploratory.default"
    planner_version = "1"

    def build_for_spec(
        self, *, project_id: str, specification_id: str, family_spec: dict[str, Any]
    ) -> ExecutionPlan:
        operation = family_spec.get("operation")
        if operation not in _RUNNER_NAMES:
            raise ValueError("Unsupported exploratory operation")
        stage = StageDefinition(
            stage_key=_RUNNER_NAMES[operation],
            stage_type=StageType("exploratory", _RUNNER_NAMES[operation], "1"),
            input_contract={"frame": "analysis-frame/1"},
            output_contract={"exploration_result": "exploratory-result/1"},
            parameters=family_spec,
        )
        return ExecutionPlan.build(
            project_id=project_id,
            analysis_specification_id=specification_id,
            analysis_family=self.family,
            planner_id=self.planner_id,
            planner_version=self.planner_version,
            stages=(stage,),
        )
