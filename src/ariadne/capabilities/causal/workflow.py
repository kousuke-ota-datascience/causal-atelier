"""Adapter from the existing causal scientific port to Generic Workflow.

This module is intentionally inside the causal capability.  It is the only
place that dispatches causal operations; GenericExecutor remains unaware of
DISCOVERY, IDENTIFICATION, ESTIMATION, REFUTATION, and SENSITIVITY.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ariadne.product.domain.enums import AnalysisFamily, ExecutionOperation
from ariadne.product.domain.execution import Execution
from ariadne.product.domain.execution_plan import (
    ExecutionPlan,
    StageDefinition,
    StageType,
)
from ariadne.product.domain.result import Result
from ariadne.product.ports.scientific_core import (
    DiscoveryInput,
    EstimationInput,
    IdentificationInput,
    RefutationInput,
    ScientificCorePort,
    SensitivityInput,
)
from ariadne.product.workflow.contracts import StageContext, StageRunResult
from ariadne.product.workflow.contracts import PlanningContext
from ariadne.product.workflow.runner_registry import StageRunnerRegistry


_STAGE_TYPES = {
    ExecutionOperation.DISCOVERY: StageType("causal", "discovery", "1"),
    ExecutionOperation.IDENTIFICATION: StageType("causal", "identification", "1"),
    ExecutionOperation.ESTIMATION: StageType("causal", "estimation", "2"),
    ExecutionOperation.REFUTATION: StageType("causal", "refutation", "1"),
    ExecutionOperation.SENSITIVITY: StageType("causal", "sensitivity", "1"),
}


class CausalPlanner:
    """Build a deterministic one-operation plan from the existing Execution.

    Existing product Commands intentionally remain the source of scientific
    snapshot truth during G1.  The adapter adds workflow structure without
    rewriting ``causal-analysis-spec/2`` or its input matrix.
    """

    family = AnalysisFamily.CAUSAL
    spec_versions = frozenset({"causal-analysis-spec/2"})
    planner_id = "causal.compatibility"
    planner_version = "1"

    def build_plan(self, context: PlanningContext) -> ExecutionPlan:
        execution = context.resource_metadata.get("execution")
        if not isinstance(execution, Execution):
            raise ValueError(
                "Causal compatibility planning requires the immutable existing Execution snapshot"
            )
        if context.specification.family_spec_schema_version != "causal-analysis-spec/2":
            raise ValueError("Causal Planner requires causal-analysis-spec/2")
        return self.build_for_execution(execution)

    def build_for_execution(self, execution: Execution) -> ExecutionPlan:
        inputs = {"dataset_path": "dataset-file/1", "output_dir": "directory/1"}
        if execution.operation is not ExecutionOperation.DISCOVERY:
            inputs["graph_path"] = "causal-graph/1"
        if execution.input_result_id is not None:
            inputs["upstream_result"] = "causal-result/1"
            inputs["upstream_execution"] = "causal-execution-snapshot/1"
        stage = StageDefinition(
            stage_key=execution.operation.value.lower(),
            stage_type=_STAGE_TYPES[execution.operation],
            input_contract=inputs,
            output_contract={"scientific_descriptors": "causal-result-descriptors/1"},
            parameters={
                "operation": execution.operation.value,
                "algorithm_or_estimator": execution.algorithm_or_estimator,
                "parameters": execution.parameter_json,
                "random_seed": execution.random_seed,
                "analysis_spec": execution.analysis_spec_json,
            },
            resource_policy={"max_attempts": 1},
        )
        return ExecutionPlan.build(
            project_id=execution.project_id,
            analysis_specification_id=execution.snapshot_hash,
            analysis_family=AnalysisFamily.CAUSAL,
            planner_id=self.planner_id,
            planner_version=self.planner_version,
            stages=(stage,),
        )


@dataclass
class CausalStageRunner:
    operation: ExecutionOperation
    core: ScientificCorePort

    @property
    def stage_type(self) -> StageType:
        return _STAGE_TYPES[self.operation]

    def validate(self, context: StageContext) -> None:
        required = set(context.stage.input_contract)
        missing = sorted(required - set(context.inputs))
        if missing:
            raise ValueError(f"Missing causal Stage inputs: {missing}")
        if context.stage.parameters.get("operation") != self.operation.value:
            raise ValueError("Causal Stage operation does not match its registered Runner")

    def run(self, context: StageContext) -> StageRunResult:
        parameters = context.stage.parameters
        common = {
            "parameters": parameters.get("parameters", {}),
            "random_seed": parameters.get("random_seed"),
            "analysis_spec": parameters["analysis_spec"],
        }
        dataset_path = Path(context.inputs["dataset_path"])
        output_dir = Path(context.inputs["output_dir"])
        descriptors: Any
        if self.operation is ExecutionOperation.DISCOVERY:
            descriptors = self.core.run_discovery(
                DiscoveryInput(
                    dataset_path=dataset_path,
                    algorithm=parameters["algorithm_or_estimator"],
                    **common,
                ),
                output_dir,
            )
        elif self.operation is ExecutionOperation.IDENTIFICATION:
            descriptors = self.core.run_identification(
                IdentificationInput(
                    dataset_path=dataset_path,
                    graph_path=Path(context.inputs["graph_path"]),
                    method=parameters["algorithm_or_estimator"],
                    **common,
                ),
                output_dir,
            )
        elif self.operation is ExecutionOperation.ESTIMATION:
            descriptors = self.core.run_estimation(
                EstimationInput(
                    dataset_path=dataset_path,
                    graph_path=Path(context.inputs["graph_path"]),
                    estimator=parameters["algorithm_or_estimator"],
                    upstream_result=_result_document(context.inputs["upstream_result"]),
                    **common,
                ),
                output_dir,
            )
        elif self.operation is ExecutionOperation.REFUTATION:
            analysis_spec = _inherit_scientific_context(
                parameters["analysis_spec"],
                context.inputs["upstream_execution"].analysis_spec_json,
            )
            descriptors = self.core.run_refutation(
                RefutationInput(
                    dataset_path=dataset_path,
                    graph_path=Path(context.inputs["graph_path"]),
                    base_result={
                        **_result_document(context.inputs["upstream_result"]),
                        **_context(context.inputs["upstream_execution"]),
                    },
                    method=analysis_spec["operation_spec"]["method"],
                    parameters=parameters.get("parameters", {}),
                    random_seed=parameters.get("random_seed"),
                    analysis_spec=analysis_spec,
                ),
                output_dir,
            )
        elif self.operation is ExecutionOperation.SENSITIVITY:
            analysis_spec = _inherit_scientific_context(
                parameters["analysis_spec"],
                context.inputs["upstream_execution"].analysis_spec_json,
            )
            descriptors = self.core.run_sensitivity(
                SensitivityInput(
                    dataset_path=dataset_path,
                    graph_path=Path(context.inputs["graph_path"]),
                    base_result={
                        **_result_document(context.inputs["upstream_result"]),
                        **_context(context.inputs["upstream_execution"]),
                    },
                    dimension=analysis_spec["operation_spec"]["dimension"],
                    parameters=parameters.get("parameters", {}),
                    random_seed=parameters.get("random_seed"),
                    analysis_spec=analysis_spec,
                ),
                output_dir,
            )
        else:  # pragma: no cover - Enum exhaustiveness guard
            raise AssertionError(f"Unsupported causal operation: {self.operation}")
        descriptor_list = list(descriptors)
        if not descriptor_list:
            raise RuntimeError("Scientific Core returned no Results")
        return StageRunResult(output_bindings={"scientific_descriptors": descriptor_list})


def register_causal_runners(registry: StageRunnerRegistry, core: ScientificCorePort) -> None:
    for operation in ExecutionOperation:
        registry.register(CausalStageRunner(operation, core))


def _result_document(result: Result) -> dict[str, Any]:
    return {
        "result_id": result.result_id,
        "result_type": result.result_type.value,
        "scientific_status": result.scientific_status.value,
        "summary": result.summary_json,
        "payload": result.payload_json,
        "diagnostics": result.diagnostics_json,
        "warnings": result.warning_json,
    }


def _context(execution: Execution) -> dict[str, Any]:
    return {
        "causal_question": execution.analysis_spec_json.get("causal_question", {}),
        "causal_design": execution.analysis_spec_json.get("causal_design", {}),
    }


def _inherit_scientific_context(
    current: dict[str, Any], upstream: dict[str, Any]
) -> dict[str, Any]:
    return {
        **current,
        "research_context": current.get("research_context") or upstream.get("research_context", {}),
        "causal_question": current.get("causal_question") or upstream.get("causal_question", {}),
        "causal_design": current.get("causal_design") or upstream.get("causal_design", {}),
    }
