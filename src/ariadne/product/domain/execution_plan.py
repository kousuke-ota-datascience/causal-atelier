"""Immutable generic execution-plan domain objects."""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ariadne.product.domain.enums import AnalysisFamily
from ariadne.product.domain.errors import InvalidExecutionPlan
from ariadne.product.domain.schemas import canonical_hash

PLAN_SCHEMA_VERSION = "execution-plan/1"
_NAME = re.compile(r"^[a-z][a-z0-9_]*$")


@dataclass(frozen=True, order=True)
class StageType:
    namespace: str
    name: str
    version: str

    def __post_init__(self) -> None:
        if not _NAME.fullmatch(self.namespace) or not _NAME.fullmatch(self.name):
            raise InvalidExecutionPlan("INVALID_STAGE_TYPE", "Stage namespace/name must be lower snake case")
        if not self.version.isdigit() or int(self.version) < 1:
            raise InvalidExecutionPlan("INVALID_STAGE_TYPE", "Stage version must be a positive integer string")

    @property
    def key(self) -> str:
        return f"{self.namespace}.{self.name}.v{self.version}"

    def as_dict(self) -> dict[str, str]:
        return {"namespace": self.namespace, "name": self.name, "version": self.version}


@dataclass(frozen=True)
class StageDefinition:
    stage_key: str
    stage_type: StageType
    input_contract: dict[str, str] = field(default_factory=dict)
    output_contract: dict[str, str] = field(default_factory=dict)
    parameters: dict[str, Any] = field(default_factory=dict)
    resource_policy: dict[str, Any] = field(default_factory=dict)
    enabled: bool = True

    def __post_init__(self) -> None:
        if not _NAME.fullmatch(self.stage_key):
            raise InvalidExecutionPlan("INVALID_STAGE_KEY", "stage_key must be lower snake case")

    def as_dict(self) -> dict[str, Any]:
        return {
            "stage_key": self.stage_key,
            "stage_type": self.stage_type.as_dict(),
            "input_contract": self.input_contract,
            "output_contract": self.output_contract,
            "parameters": self.parameters,
            "resource_policy": self.resource_policy,
            "enabled": self.enabled,
        }


@dataclass(frozen=True)
class StageBinding:
    source_stage_key: str
    source_output: str
    target_stage_key: str
    target_input: str

    def as_dict(self) -> dict[str, str]:
        return {
            "source_stage_key": self.source_stage_key,
            "source_output": self.source_output,
            "target_stage_key": self.target_stage_key,
            "target_input": self.target_input,
        }


@dataclass(frozen=True)
class ExecutionPlan:
    execution_plan_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    project_id: str = ""
    analysis_specification_id: str = ""
    analysis_family: AnalysisFamily = AnalysisFamily.EXPLORATORY
    planner_id: str = ""
    planner_version: str = "1"
    stages: tuple[StageDefinition, ...] = ()
    dependencies: tuple[StageBinding, ...] = ()
    plan_schema_version: str = PLAN_SCHEMA_VERSION
    plan_hash: str = ""
    created_at: datetime | None = None

    @classmethod
    def build(cls, **values: Any) -> "ExecutionPlan":
        plan = cls(**values)
        object.__setattr__(plan, "plan_hash", canonical_hash(plan.canonical_payload()))
        return plan

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "plan_schema_version": self.plan_schema_version,
            "project_id": self.project_id,
            "analysis_specification_id": self.analysis_specification_id,
            "analysis_family": self.analysis_family.value,
            "planner_id": self.planner_id,
            "planner_version": self.planner_version,
            "stages": [stage.as_dict() for stage in self.stages],
            "dependencies": [binding.as_dict() for binding in self.dependencies],
        }
