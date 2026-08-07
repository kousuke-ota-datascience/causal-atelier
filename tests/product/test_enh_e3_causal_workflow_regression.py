"""G1 regression tests for Generic Workflow and the causal compatibility adapter."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest

from ariadne.capabilities.causal.workflow import CausalPlanner, register_causal_runners
from ariadne.product.domain.enums import (
    AnalysisFamily,
    ExecutionOperation,
    ResultType,
    ScientificStatus,
    StageExecutionStatus,
)
from ariadne.product.domain.execution import Execution
from ariadne.product.domain.execution_plan import (
    ExecutionPlan,
    StageBinding,
    StageDefinition,
    StageType,
)
from ariadne.product.domain.result import Result
from ariadne.product.ports.scientific_core import ScientificResultDescriptor
from ariadne.product.workflow.contracts import ArtifactDraft, StageContext, StageRunResult
from ariadne.product.workflow.executor import GenericExecutor
from ariadne.product.workflow.plan_validator import PlanValidator
from ariadne.product.workflow.planner_registry import PlannerRegistry
from ariadne.product.workflow.runner_registry import StageRunnerRegistry


def _spec(operation: ExecutionOperation) -> dict:  # type: ignore[type-arg]
    operation_specs = {
        ExecutionOperation.DISCOVERY: {"feature_columns": ["x", "t", "y"]},
        ExecutionOperation.IDENTIFICATION: {"allow_partial_identification": False},
        ExecutionOperation.ESTIMATION: {"estimator": "ols", "inference_options": {}},
        ExecutionOperation.REFUTATION: {"method": "PLACEBO_TREATMENT", "repetitions": 10},
        ExecutionOperation.SENSITIVITY: {"dimension": "PROPENSITY_CLIPPING", "values": [.01]},
    }
    return {
        "schema_version": "causal-analysis-spec/2",
        "analysis_mode": "EXPLORATORY",
        "research_context": {},
        "causal_question": {"treatment": "t", "outcome": "y"},
        "causal_design": {"adjustment_set": ["x"], "assumptions": []},
        "operation_spec": operation_specs[operation],
        "validation_override": None,
    }


def _execution(operation: ExecutionOperation) -> Execution:
    has_graph = operation is not ExecutionOperation.DISCOVERY
    has_result = operation in {
        ExecutionOperation.ESTIMATION,
        ExecutionOperation.REFUTATION,
        ExecutionOperation.SENSITIVITY,
    }
    return Execution(
        project_id="project",
        dataset_version_id="dataset",
        input_graph_version_id="graph" if has_graph else None,
        input_result_id="result" if has_result else None,
        operation=operation,
        analysis_spec_json=_spec(operation),
        algorithm_or_estimator={
            ExecutionOperation.DISCOVERY: "pc",
            ExecutionOperation.IDENTIFICATION: "GRAPHICAL_IDENTIFICATION",
            ExecutionOperation.ESTIMATION: "ols",
            ExecutionOperation.REFUTATION: "PLACEBO_TREATMENT",
            ExecutionOperation.SENSITIVITY: "PROPENSITY_CLIPPING",
        }[operation],
        snapshot_hash=f"snapshot-{operation.value}",
    )


class FakeScientificCore:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def run_discovery(self, input_, output_dir):  # type: ignore[no-untyped-def]
        self.calls.append("DISCOVERY")
        return [ScientificResultDescriptor(ResultType.DISCOVERY_GRAPH_RESULT, ScientificStatus.GENERATED)]

    def run_identification(self, input_, output_dir):  # type: ignore[no-untyped-def]
        self.calls.append("IDENTIFICATION")
        return [
            ScientificResultDescriptor(ResultType.IDENTIFICATION_RESULT, ScientificStatus.IDENTIFIED),
            ScientificResultDescriptor(ResultType.DATA_ELIGIBILITY_RESULT, ScientificStatus.PASS),
        ]

    def run_estimation(self, input_, output_dir):  # type: ignore[no-untyped-def]
        self.calls.append("ESTIMATION")
        return [
            ScientificResultDescriptor(ResultType.TREATMENT_EFFECT_RESULT, ScientificStatus.ESTIMATED),
            ScientificResultDescriptor(ResultType.DIAGNOSTICS_RESULT, ScientificStatus.PASS),
        ]

    def run_refutation(self, input_, output_dir):  # type: ignore[no-untyped-def]
        self.calls.append("REFUTATION")
        return [ScientificResultDescriptor(ResultType.REFUTATION_RESULT, ScientificStatus.NO_FAILURE_DETECTED)]

    def run_sensitivity(self, input_, output_dir):  # type: ignore[no-untyped-def]
        self.calls.append("SENSITIVITY")
        return [ScientificResultDescriptor(ResultType.SENSITIVITY_RESULT, ScientificStatus.ROBUST)]


@pytest.mark.requirement("FR-075", "FR-076", "FR-077", "FR-079", "NFR-005")
def test_causal_planner_builds_generic_plans_and_registry_resolves_every_operation() -> None:
    core = FakeScientificCore()
    registry = StageRunnerRegistry()
    register_causal_runners(registry, core)
    planner = CausalPlanner()
    planners = PlannerRegistry()
    planners.register(planner)

    assert registry.capability_fingerprint == (
        "causal.discovery.v1",
        "causal.estimation.v2",
        "causal.identification.v1",
        "causal.refutation.v1",
        "causal.sensitivity.v1",
    )
    for operation in ExecutionOperation:
        execution = _execution(operation)
        plan = planner.build_for_execution(execution)
        assert plan.analysis_family is AnalysisFamily.CAUSAL
        assert plan.plan_schema_version == "execution-plan/1"
        assert plan.plan_hash
        assert registry.resolve(plan.stages[0].stage_type).operation is operation
        assert planners.resolve(AnalysisFamily.CAUSAL, "causal-analysis-spec/2") is planner
        assert PlanValidator(registry).validate(plan) == (operation.value.lower(),)


@pytest.mark.requirement("FR-079", "FR-080", "FR-088", "NFR-014")
@pytest.mark.parametrize("operation", list(ExecutionOperation))
def test_every_existing_causal_operation_runs_through_generic_executor(
    operation: ExecutionOperation, tmp_path: Path,
) -> None:
    core = FakeScientificCore()
    registry = StageRunnerRegistry()
    register_causal_runners(registry, core)
    execution = _execution(operation)
    plan = CausalPlanner().build_for_execution(execution)
    stage_key = plan.stages[0].stage_key
    inputs: dict[str, object] = {"dataset_path": tmp_path / "data.csv", "output_dir": tmp_path}
    (tmp_path / "data.csv").write_text("x,t,y\n0,0,0\n", encoding="utf-8")
    if operation is not ExecutionOperation.DISCOVERY:
        inputs["graph_path"] = tmp_path / "graph.json"
        (tmp_path / "graph.json").write_text("{}", encoding="utf-8")
    if execution.input_result_id:
        inputs["upstream_result"] = Result(
            result_type=ResultType.TREATMENT_EFFECT_RESULT
            if operation in {ExecutionOperation.REFUTATION, ExecutionOperation.SENSITIVITY}
            else ResultType.IDENTIFICATION_RESULT,
            scientific_status=ScientificStatus.ESTIMATED
            if operation in {ExecutionOperation.REFUTATION, ExecutionOperation.SENSITIVITY}
            else ScientificStatus.IDENTIFIED,
        )
        inputs["upstream_execution"] = _execution(
            ExecutionOperation.ESTIMATION
            if operation in {ExecutionOperation.REFUTATION, ExecutionOperation.SENSITIVITY}
            else ExecutionOperation.IDENTIFICATION
        )

    outcome = GenericExecutor(registry).execute(
        execution.execution_id, plan, external_inputs={stage_key: inputs}
    )

    assert outcome.status == "SUCCEEDED"
    assert outcome.stages[0].status is StageExecutionStatus.SUCCEEDED
    descriptors = outcome.stages[0].output_binding["scientific_descriptors"]
    assert descriptors
    assert all(isinstance(item.result_type, ResultType) for item in descriptors)
    assert all(isinstance(item.scientific_status, ScientificStatus) for item in descriptors)
    assert core.calls == [operation.value]


@dataclass
class BindingRunner:
    stage_type: StageType
    output_name: str
    fail_once: bool = False
    calls: int = 0

    def validate(self, context: StageContext) -> None:
        return None

    def run(self, context: StageContext) -> StageRunResult:
        self.calls += 1
        if self.fail_once and self.calls == 1:
            raise OSError("retryable temporary failure")
        value = context.inputs.get("artifact", "artifact-1")
        return StageRunResult(
            output_bindings={self.output_name: value},
            artifacts=(ArtifactDraft("CAUSAL_TEST", "causal-test-artifact/1", "text/plain", b"ok"),),
        )


def _binding_plan(source: StageType, sink: StageType, *, attempts: int = 1) -> ExecutionPlan:
    return ExecutionPlan.build(
        project_id="project",
        analysis_specification_id="causal-spec",
        analysis_family=AnalysisFamily.CAUSAL,
        planner_id="causal.test",
        planner_version="1",
        stages=(
            StageDefinition("source", source, output_contract={"artifact": "causal-artifact/1"}, resource_policy={"max_attempts": attempts}),
            StageDefinition("sink", sink, input_contract={"artifact": "causal-artifact/1"}, output_contract={"consumed": "causal-artifact/1"}),
        ),
        dependencies=(StageBinding("source", "artifact", "sink", "artifact"),),
    )


@pytest.mark.requirement("FR-078", "FR-080", "FR-081", "FR-083", "FR-084")
def test_artifact_binding_attempt_retry_failure_and_cancellation_keep_generic_meaning() -> None:
    source_type = StageType("causal", "test_source", "1")
    sink_type = StageType("causal", "test_sink", "1")
    source = BindingRunner(source_type, "artifact", fail_once=True)
    sink = BindingRunner(sink_type, "consumed")
    registry = StageRunnerRegistry()
    registry.register(source)
    registry.register(sink)
    committed: list[str] = []
    compensated: list[str] = []
    executor = GenericExecutor(
        registry,
        commit=lambda stage, result: committed.append(stage.stage_key),
        compensate=lambda stage, error: compensated.append(stage.stage_key),
        retryable=lambda error: isinstance(error, OSError),
    )
    outcome = executor.execute("execution", _binding_plan(source_type, sink_type, attempts=2))
    assert outcome.status == "SUCCEEDED"
    assert len(outcome.stages[0].attempts) == 2
    assert outcome.stages[1].input_binding == {"artifact": "artifact-1"}
    assert compensated == ["source"]
    assert committed == ["source", "sink"]

    cancelled = executor.execute(
        "cancelled", _binding_plan(source_type, sink_type), cancelled=lambda: True
    )
    assert cancelled.status == "CANCELLED"
    assert all(stage.status is StageExecutionStatus.PENDING for stage in cancelled.stages)

    always_fails = BindingRunner(source_type, "artifact", fail_once=True)
    failing_registry = StageRunnerRegistry()
    failing_registry.register(always_fails)
    failing_registry.register(BindingRunner(sink_type, "consumed"))
    failed = GenericExecutor(failing_registry).execute(
        "failed", _binding_plan(source_type, sink_type)
    )
    assert failed.status == "FAILED"
    assert failed.stages[0].status is StageExecutionStatus.FAILED
    assert failed.stages[1].status is StageExecutionStatus.SKIPPED_DUE_TO_PREREQUISITE


@pytest.mark.requirement("NFR-005", "NFR-018")
def test_generic_workflow_has_no_causal_semantics_or_legacy_dependency() -> None:
    workflow_root = Path(__file__).parents[2] / "src" / "ariadne" / "product" / "workflow"
    source = "\n".join(path.read_text(encoding="utf-8") for path in workflow_root.glob("*.py"))
    assert "ariadne.legacy" not in source
    assert "ExecutionOperation" not in source
    for causal_term in ("DISCOVERY", "IDENTIFICATION", "ESTIMATION", "REFUTATION", "SENSITIVITY"):
        assert causal_term not in source
