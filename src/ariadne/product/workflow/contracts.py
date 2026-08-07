"""Ports shared by planners, runners, and the generic executor."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from ariadne.product.domain.analysis_specification import AnalysisSpecification
from ariadne.product.domain.enums import AnalysisFamily
from ariadne.product.domain.execution_plan import ExecutionPlan, StageDefinition, StageType


@dataclass(frozen=True)
class PlanningContext:
    specification: AnalysisSpecification
    resource_metadata: dict[str, Any] = field(default_factory=dict)
    policy: dict[str, Any] = field(default_factory=dict)


class AnalysisPlanner(Protocol):
    family: AnalysisFamily
    spec_versions: frozenset[str]
    planner_id: str
    planner_version: str

    def build_plan(self, context: PlanningContext) -> ExecutionPlan: ...


@dataclass(frozen=True)
class StageContext:
    execution_id: str
    stage: StageDefinition
    inputs: dict[str, Any]
    snapshots: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ResultDraft:
    result_type: str
    schema_version: str
    analytical_status: str
    summary: dict[str, Any] = field(default_factory=dict)
    payload: dict[str, Any] = field(default_factory=dict)
    diagnostics: dict[str, Any] = field(default_factory=dict)
    warnings: tuple[dict[str, Any], ...] = ()


@dataclass(frozen=True)
class ArtifactDraft:
    artifact_type: str
    schema_version: str
    media_type: str
    content: bytes
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class StageRunResult:
    output_bindings: dict[str, Any]
    results: tuple[ResultDraft, ...] = ()
    artifacts: tuple[ArtifactDraft, ...] = ()
    warnings: tuple[dict[str, Any], ...] = ()
    metrics: dict[str, float] = field(default_factory=dict)


class StageRunner(Protocol):
    stage_type: StageType

    def validate(self, context: StageContext) -> None: ...
    def run(self, context: StageContext) -> StageRunResult: ...
