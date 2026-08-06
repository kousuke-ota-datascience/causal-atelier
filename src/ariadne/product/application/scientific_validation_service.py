"""Cross-entity ENH-E1 validation gates."""

from __future__ import annotations

from typing import Any

from ariadne.product.domain.analysis_spec import causal_question_hash, validate_analysis_spec
from ariadne.product.domain.enums import (
    ExecutionOperation, ResultType, ScientificStatus,
)
from ariadne.product.domain.errors import (
    InvalidAnalysisSpec, ProjectBoundaryViolation, ScientificContractViolation,
)


ESTIMATOR_CAPABILITIES: dict[str, dict[str, Any]] = {
    "difference_in_means": {
        "estimands": {"ATE", "ATT"}, "strategies": {"RANDOMIZED"}, "parameters": set(),
        "treatment_types": {"BINARY"}, "outcome_types": {"CONTINUOUS"},
        "required_adjustment": "NONE", "uncertainty_support": True,
        "overlap_requirement": "TREATMENT_ARMS",
        "produced_diagnostics": {"SAMPLE_SIZE", "TREATMENT_ARM_COUNTS"},
    },
    "diff_in_means": {
        "estimands": {"ATE", "ATT"}, "strategies": {"RANDOMIZED"}, "parameters": set(),
        "treatment_types": {"BINARY"}, "outcome_types": {"CONTINUOUS"},
        "required_adjustment": "NONE", "uncertainty_support": True,
        "overlap_requirement": "TREATMENT_ARMS",
        "produced_diagnostics": {"SAMPLE_SIZE", "TREATMENT_ARM_COUNTS"},
    },
    "ols": {
        "estimands": {"ATE", "ATT"}, "strategies": {"RANDOMIZED", "BACKDOOR"},
        "parameters": {"robust_se"},
        "treatment_types": {"BINARY"}, "outcome_types": {"CONTINUOUS"},
        "required_adjustment": "IDENTIFICATION_RESULT", "uncertainty_support": True,
        "overlap_requirement": "TREATMENT_ARMS",
        "produced_diagnostics": {"SAMPLE_SIZE", "BALANCE", "DESIGN"},
    },
    "outcome_regression": {
        "estimands": {"ATE", "ATT"}, "strategies": {"RANDOMIZED", "BACKDOOR"},
        "parameters": {"robust_se"},
        "treatment_types": {"BINARY"}, "outcome_types": {"CONTINUOUS"},
        "required_adjustment": "IDENTIFICATION_RESULT", "uncertainty_support": True,
        "overlap_requirement": "TREATMENT_ARMS",
        "produced_diagnostics": {"SAMPLE_SIZE", "BALANCE", "DESIGN"},
    },
    "ipw": {
        "estimands": {"ATE", "ATT"}, "strategies": {"RANDOMIZED", "BACKDOOR"},
        "parameters": {"propensity_clip"},
        "treatment_types": {"BINARY"}, "outcome_types": {"CONTINUOUS"},
        "required_adjustment": "IDENTIFICATION_RESULT", "uncertainty_support": True,
        "overlap_requirement": "PROPENSITY_SCORE",
        "produced_diagnostics": {"SAMPLE_SIZE", "BALANCE", "DESIGN", "OVERLAP"},
    },
    "aipw": {
        "estimands": {"ATE", "ATT"}, "strategies": {"RANDOMIZED", "BACKDOOR"},
        "parameters": {"robust_se", "propensity_clip", "cross_fitting_folds"},
        "treatment_types": {"BINARY"}, "outcome_types": {"CONTINUOUS"},
        "required_adjustment": "IDENTIFICATION_RESULT", "uncertainty_support": True,
        "overlap_requirement": "PROPENSITY_SCORE",
        "produced_diagnostics": {"SAMPLE_SIZE", "BALANCE", "DESIGN", "OVERLAP"},
    },
}


class ScientificValidationService:
    def validate_submission(
        self,
        *,
        uow: Any,
        project_id: str,
        dataset_version_id: str,
        graph_version_id: str | None,
        input_result_id: str | None,
        operation: ExecutionOperation,
        analysis_spec: dict[str, Any],
        method: str,
        parameters: dict[str, Any],
    ) -> None:
        validate_analysis_spec(operation, analysis_spec)
        if operation in {ExecutionOperation.DISCOVERY, ExecutionOperation.IDENTIFICATION}:
            if input_result_id is not None:
                raise InvalidAnalysisSpec("input_result_id is forbidden for this operation")
            return
        if input_result_id is None:
            raise ScientificContractViolation("UPSTREAM_RESULT_REQUIRED", "input_result_id is required")
        upstream = uow.results.get(input_result_id)
        if upstream is None:
            raise InvalidAnalysisSpec("upstream Result does not exist")
        upstream_execution = uow.executions.get(upstream.execution_id)
        if upstream_execution is None:
            raise InvalidAnalysisSpec("upstream Execution does not exist")
        if upstream_execution.project_id != project_id:
            raise ProjectBoundaryViolation("Upstream Result does not belong to project")
        if upstream_execution.dataset_version_id != dataset_version_id:
            raise InvalidAnalysisSpec("upstream Result uses a different Dataset Version")
        if upstream_execution.input_graph_version_id != graph_version_id:
            raise InvalidAnalysisSpec("upstream Result uses a different Graph Version")

        expected = (
            ResultType.IDENTIFICATION_RESULT
            if operation == ExecutionOperation.ESTIMATION
            else ResultType.TREATMENT_EFFECT_RESULT
        )
        if upstream.result_type != expected:
            raise ScientificContractViolation(
                "UPSTREAM_RESULT_INCOMPATIBLE", f"{operation.value} requires {expected.value}"
            )

        if operation == ExecutionOperation.ESTIMATION:
            self._validate_estimation(
                uow=uow,
                upstream=upstream,
                upstream_execution=upstream_execution,
                analysis_spec=analysis_spec,
                method=method,
                parameters=parameters,
            )

    def _validate_estimation(
        self,
        *,
        uow: Any,
        upstream: Any,
        upstream_execution: Any,
        analysis_spec: dict[str, Any],
        method: str,
        parameters: dict[str, Any],
    ) -> None:
        if causal_question_hash(upstream_execution.analysis_spec_json) != causal_question_hash(analysis_spec):
            raise InvalidAnalysisSpec("causal question does not match Identification Result")
        if upstream.scientific_status == ScientificStatus.NOT_IDENTIFIED:
            raise ScientificContractViolation(
                "IDENTIFICATION_NOT_ACCEPTABLE", "Identification Result is NOT_IDENTIFIED"
            )
        if upstream.scientific_status not in {
            ScientificStatus.IDENTIFIED, ScientificStatus.REQUIRES_REVIEW,
        }:
            raise ScientificContractViolation(
                "IDENTIFICATION_NOT_ACCEPTABLE", "Identification Result is not acceptable"
            )
        siblings = uow.results.list_by_execution(upstream.execution_id)
        eligibility = next(
            (item for item in siblings if item.result_type == ResultType.DATA_ELIGIBILITY_RESULT),
            None,
        )
        if eligibility is None:
            raise InvalidAnalysisSpec("Data Eligibility Result is required")
        if eligibility.scientific_status == ScientificStatus.FAIL:
            raise ScientificContractViolation("DATA_ELIGIBILITY_FAILED", "Data Eligibility failed")
        override = analysis_spec.get("validation_override")
        if eligibility.scientific_status == ScientificStatus.WARN and override is None:
            raise ScientificContractViolation(
                "OVERRIDE_REASON_REQUIRED", "validation_override is required for Eligibility WARN"
            )
        if upstream.scientific_status == ScientificStatus.REQUIRES_REVIEW and override is None:
            raise ScientificContractViolation(
                "OVERRIDE_REASON_REQUIRED", "validation_override is required for REQUIRES_REVIEW"
            )

        name = method.lower()
        capability = ESTIMATOR_CAPABILITIES.get(name)
        if capability is None:
            raise InvalidAnalysisSpec(f"Unsupported estimator: {method}")
        question = analysis_spec["causal_question"]
        design = upstream_execution.analysis_spec_json["causal_design"]
        if question["estimand"] not in capability["estimands"]:
            raise InvalidAnalysisSpec("Estimator is incompatible with estimand")
        if design["identification_strategy"] not in capability["strategies"]:
            raise InvalidAnalysisSpec("Estimator is incompatible with identification strategy")
        unknown = set(parameters) - capability["parameters"]
        if unknown:
            raise InvalidAnalysisSpec(f"Unsupported estimator parameters: {sorted(unknown)}")
