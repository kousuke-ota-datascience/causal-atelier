"""G3 Predictive planner limited to deterministic partition construction."""

from __future__ import annotations

from typing import Any

from ariadne.product.domain.analysis_specification import PREDICTIVE_SCHEMA_VERSION
from ariadne.product.domain.enums import AnalysisFamily, VersionedResourceStatus
from ariadne.product.domain.errors import InvalidExecutionPlan
from ariadne.product.domain.execution_plan import ExecutionPlan, StageDefinition, StageType
from ariadne.product.workflow.contracts import PlanningContext


class PredictivePlanner:
    family = AnalysisFamily.PREDICTIVE
    spec_versions = frozenset({PREDICTIVE_SCHEMA_VERSION})
    planner_id = "predictive.split"
    planner_version = "1"

    def build_plan(self, context: PlanningContext) -> ExecutionPlan:
        specification = context.specification
        if specification.status is not VersionedResourceStatus.FIXED:
            raise InvalidExecutionPlan("SPEC_NOT_FIXED", "Specification must be FIXED")
        return self.build_for_spec(
            project_id=specification.project_id,
            specification_id=specification.analysis_specification_id,
            family_spec=specification.family_spec,
        )

    def build_for_spec(
        self,
        *,
        project_id: str,
        specification_id: str,
        family_spec: dict[str, Any],
    ) -> ExecutionPlan:
        stage = StageDefinition(
            stage_key="split",
            stage_type=StageType("predictive", "split", "1"),
            input_contract={
                "frame": "analysis-frame/1",
                "source_snapshot": "predictive-source-snapshot/1",
            },
            output_contract={"partition_manifest": "partition-artifact/1"},
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
