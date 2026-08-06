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
        "estimands": {"ATE"}, "strategies": {"RANDOMIZED"}, "parameters": set(),
        "treatment_types": {"BINARY"}, "outcome_types": {"CONTINUOUS"},
        "required_adjustment": "NONE", "uncertainty_support": True,
        "overlap_requirement": "TREATMENT_ARMS",
        "produced_diagnostics": {"SAMPLE_SIZE", "TREATMENT_ARM_COUNTS"},
    },
    "diff_in_means": {
        "estimands": {"ATE"}, "strategies": {"RANDOMIZED"}, "parameters": set(),
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

        question = analysis_spec["causal_question"]
        design = upstream_execution.analysis_spec_json["causal_design"]
        validate_estimator_compatibility(
            method=method,
            parameters=parameters,
            estimand=question["estimand"],
            strategy=design["identification_strategy"],
            submitted_adjustment=analysis_spec["causal_design"].get("adjustment_set", []),
            identified_adjustment=upstream.payload_json.get("selected_adjustment_set", []),
            eligibility_payload=eligibility.payload_json,
        )


def validate_estimator_compatibility(
    *,
    method: str,
    parameters: dict[str, Any],
    estimand: str,
    strategy: str,
    submitted_adjustment: list[str],
    identified_adjustment: list[str],
    eligibility_payload: dict[str, Any],
) -> None:
    """Validate the complete FR-054 contract using persisted scientific evidence."""
    capability = ESTIMATOR_CAPABILITIES.get(method.lower())
    if capability is None:
        raise ScientificContractViolation(
            "ESTIMATOR_UNSUPPORTED", f"Unsupported estimator: {method}"
        )
    if estimand not in capability["estimands"]:
        raise ScientificContractViolation(
            "ESTIMATOR_ESTIMAND_INCOMPATIBLE",
            f"{method} does not support estimand {estimand}",
        )

    inferred = eligibility_payload.get("inferred_types")
    if not isinstance(inferred, dict):
        raise ScientificContractViolation(
            "DATA_ELIGIBILITY_TYPE_EVIDENCE_MISSING",
            "Data Eligibility Result has no normalized inferred types",
        )
    treatment = inferred.get("treatment")
    outcome = inferred.get("outcome")
    treatment_type = treatment.get("type") if isinstance(treatment, dict) else None
    outcome_type = outcome.get("type") if isinstance(outcome, dict) else None
    if treatment_type not in capability["treatment_types"]:
        raise ScientificContractViolation(
            "ESTIMATOR_TREATMENT_TYPE_INCOMPATIBLE",
            f"{method} does not support treatment type {treatment_type or 'UNKNOWN'}",
        )
    if outcome_type not in capability["outcome_types"]:
        raise ScientificContractViolation(
            "ESTIMATOR_OUTCOME_TYPE_INCOMPATIBLE",
            f"{method} does not support outcome type {outcome_type or 'UNKNOWN'}",
        )
    if strategy not in capability["strategies"]:
        raise ScientificContractViolation(
            "ESTIMATOR_IDENTIFICATION_STRATEGY_INCOMPATIBLE",
            f"{method} does not support identification strategy {strategy}",
        )

    unknown = set(parameters) - capability["parameters"]
    if unknown:
        raise ScientificContractViolation(
            "ESTIMATOR_PARAMETER_UNSUPPORTED",
            f"Unsupported estimator parameters: {sorted(unknown)}",
        )
    _validate_parameter_values(method, parameters)

    if submitted_adjustment != identified_adjustment:
        raise ScientificContractViolation(
            "ESTIMATOR_ADJUSTMENT_INCOMPATIBLE",
            "Submitted adjustment set does not match the Identification Result",
        )
    if capability["required_adjustment"] == "NONE" and identified_adjustment:
        raise ScientificContractViolation(
            "ESTIMATOR_ADJUSTMENT_INCOMPATIBLE",
            f"{method} does not consume an adjustment set",
        )

    if capability["overlap_requirement"] == "PROPENSITY_SCORE":
        checks = eligibility_payload.get("checks")
        overlap = next(
            (
                item for item in checks
                if isinstance(item, dict) and item.get("check_code") == "LIMITED_OVERLAP"
            ),
            None,
        ) if isinstance(checks, list) else None
        if overlap is None or overlap.get("status") not in {"PASS", "WARN"}:
            raise ScientificContractViolation(
                "ESTIMATOR_DIAGNOSTIC_PREREQUISITE_MISSING",
                f"{method} requires an estimable propensity overlap diagnostic",
            )


def _validate_parameter_values(method: str, parameters: dict[str, Any]) -> None:
    robust_se = parameters.get("robust_se")
    if robust_se is not None and robust_se not in {"HC0", "HC1", "HC2", "HC3"}:
        raise ScientificContractViolation(
            "ESTIMATOR_PARAMETER_UNSUPPORTED", "robust_se must be HC0, HC1, HC2, or HC3"
        )
    clip = parameters.get("propensity_clip")
    if clip is not None and (
        not isinstance(clip, (list, tuple))
        or len(clip) != 2
        or not all(isinstance(value, (int, float)) for value in clip)
        or not 0 < float(clip[0]) < float(clip[1]) < 1
    ):
        raise ScientificContractViolation(
            "ESTIMATOR_PARAMETER_UNSUPPORTED",
            "propensity_clip must be [lower, upper] with 0 < lower < upper < 1",
        )
    folds = parameters.get("cross_fitting_folds")
    if folds is not None and (
        not isinstance(folds, int) or isinstance(folds, bool) or folds == 1 or folds < 0
    ):
        raise ScientificContractViolation(
            "ESTIMATOR_PARAMETER_UNSUPPORTED",
            "cross_fitting_folds must be zero or at least two",
        )
