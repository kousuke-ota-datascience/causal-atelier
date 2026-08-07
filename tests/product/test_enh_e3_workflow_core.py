"""Direct G1 contract tests for the family-neutral workflow core."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from ariadne.product.domain.enums import AnalysisFamily
from ariadne.product.domain.errors import (
    DuplicateRegistration,
    InvalidExecutionPlan,
    InvalidSchema,
    UnsupportedSchemaVersion,
)
from ariadne.product.domain.execution_plan import (
    ExecutionPlan,
    StageBinding,
    StageDefinition,
    StageType,
)
from ariadne.product.domain.schemas import SchemaRegistry, canonical_hash, reject_unknown
from ariadne.product.workflow.contracts import StageContext, StageRunResult
from ariadne.product.workflow.plan_validator import PlanValidator
from ariadne.product.workflow.runner_registry import StageRunnerRegistry


@dataclass
class Runner:
    stage_type: StageType

    def validate(self, context: StageContext) -> None:
        return None

    def run(self, context: StageContext) -> StageRunResult:
        return StageRunResult({})


def _plan(
    stages: tuple[StageDefinition, ...], dependencies: tuple[StageBinding, ...] = ()
) -> ExecutionPlan:
    return ExecutionPlan.build(
        project_id="project",
        analysis_specification_id="specification",
        analysis_family=AnalysisFamily.CAUSAL,
        planner_id="test",
        planner_version="1",
        stages=stages,
        dependencies=dependencies,
    )


@pytest.mark.requirement("FR-077", "FR-079", "FR-085")
def test_registry_rejects_duplicate_and_validator_rejects_missing_runner() -> None:
    stage_type = StageType("core", "registered", "1")
    registry = StageRunnerRegistry()
    registry.register(Runner(stage_type))
    with pytest.raises(DuplicateRegistration):
        registry.register(Runner(stage_type))
    missing = StageDefinition("missing", StageType("core", "missing", "1"))
    with pytest.raises(InvalidExecutionPlan) as caught:
        PlanValidator(registry).validate(_plan((missing,)))
    assert caught.value.code == "RUNNER_NOT_REGISTERED"


@pytest.mark.requirement("FR-078", "FR-084", "FR-085")
@pytest.mark.parametrize(
    ("dependencies", "expected_code"),
    [
        ((StageBinding("first", "value", "second", "value"), StageBinding("second", "value", "first", "value")), "PLAN_CYCLE"),
        ((StageBinding("first", "value", "second", "value"),), "SCHEMA_MISMATCH"),
    ],
)
def test_plan_validator_rejects_cycles_and_schema_mismatch(
    dependencies: tuple[StageBinding, ...], expected_code: str,
) -> None:
    first_type = StageType("core", "first", "1")
    second_type = StageType("core", "second", "1")
    registry = StageRunnerRegistry()
    registry.register(Runner(first_type))
    registry.register(Runner(second_type))
    first = StageDefinition(
        "first", first_type,
        input_contract={"value": "schema/a"}, output_contract={"value": "schema/a"},
    )
    second = StageDefinition(
        "second", second_type,
        input_contract={"value": "schema/b" if expected_code == "SCHEMA_MISMATCH" else "schema/a"},
        output_contract={"value": "schema/a"},
    )
    with pytest.raises(InvalidExecutionPlan) as caught:
        PlanValidator(registry).validate(_plan((first, second), dependencies))
    assert caught.value.code == expected_code


@pytest.mark.requirement("FR-076", "FR-087", "NFR-003", "NFR-013")
def test_schema_registry_and_plan_hash_are_deterministic_and_strict() -> None:
    registry = SchemaRegistry()

    def validate(payload):  # type: ignore[no-untyped-def]
        reject_unknown(payload, {"schema_version", "value"}, name="test")
        if payload.get("schema_version") != "test/1":
            raise InvalidSchema("wrong schema version")
        return payload

    registry.register("test/1", validate)
    first = {"schema_version": "test/1", "value": {"b": 2.0, "a": -0.0}}
    second = {"value": {"a": 0, "b": 2}, "schema_version": "test/1"}
    assert registry.hash("test/1", first) == registry.hash("test/1", second)
    assert canonical_hash(first) == canonical_hash(second)
    with pytest.raises(InvalidSchema):
        registry.validate("test/1", {**first, "unknown": True})
    with pytest.raises(InvalidSchema):
        registry.hash("test/1", {"schema_version": "test/1", "value": float("nan")})
    with pytest.raises(UnsupportedSchemaVersion):
        registry.validate("test/2", first)

    stage = StageDefinition("only", StageType("core", "only", "1"))
    assert _plan((stage,)).plan_hash == _plan((stage,)).plan_hash
