from __future__ import annotations

from ariadne.product.domain.enums import AnalysisFamily
from ariadne.product.domain.errors import DuplicateRegistration, InvalidExecutionPlan
from ariadne.product.workflow.contracts import AnalysisPlanner


class PlannerRegistry:
    def __init__(self) -> None:
        self._planners: dict[tuple[AnalysisFamily, str], AnalysisPlanner] = {}

    def register(self, planner: AnalysisPlanner) -> None:
        if not planner.spec_versions:
            raise DuplicateRegistration("Planner must declare at least one schema version")
        for version in planner.spec_versions:
            key = (planner.family, version)
            if key in self._planners:
                raise DuplicateRegistration(
                    f"Planner is already registered for {planner.family.value}/{version}"
                )
        for version in planner.spec_versions:
            self._planners[(planner.family, version)] = planner

    def resolve(self, family: AnalysisFamily, schema_version: str) -> AnalysisPlanner:
        try:
            return self._planners[(family, schema_version)]
        except KeyError as exc:
            raise InvalidExecutionPlan(
                "PLANNER_NOT_REGISTERED",
                f"Planner is not registered for {family.value}/{schema_version}",
            ) from exc
