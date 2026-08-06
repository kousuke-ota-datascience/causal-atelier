from __future__ import annotations

from dataclasses import dataclass

import pytest

from ariadne.product.application.scientific_validation_service import ScientificValidationService
from ariadne.product.domain.enums import ExecutionOperation, ResultType, ScientificStatus
from ariadne.product.domain.errors import ScientificContractViolation
from ariadne.product.domain.execution import Execution
from ariadne.product.domain.result import Result


def _spec(
    *,
    estimand: str = "ATE",
    strategy: str = "BACKDOOR",
    adjustment: list[str] | None = None,
) -> dict:
    return {
        "schema_version": "causal-analysis-spec/2",
        "analysis_mode": "EXPLORATORY",
        "research_context": {},
        "causal_question": {
            "population": "rows",
            "treatment": "treatment",
            "comparator": "untreated",
            "outcome": "outcome",
            "analysis_unit": "row",
            "treatment_time": "t0",
            "outcome_window": "t1",
            "estimand": estimand,
        },
        "causal_design": {
            "identification_strategy": strategy,
            "adjustment_set": adjustment if adjustment is not None else ["x"],
            "assumptions": [],
        },
        "operation_spec": {"estimator": "placeholder", "inference_options": {}},
        "validation_override": None,
    }


class _Results:
    def __init__(self, upstream: Result, eligibility: Result) -> None:
        self._upstream = upstream
        self._eligibility = eligibility

    def get(self, result_id: str):  # type: ignore[no-untyped-def]
        return self._upstream if result_id == self._upstream.result_id else None

    def list_by_execution(self, execution_id: str):  # type: ignore[no-untyped-def]
        return [self._upstream, self._eligibility]


class _Executions:
    def __init__(self, execution: Execution) -> None:
        self._execution = execution

    def get(self, execution_id: str):  # type: ignore[no-untyped-def]
        return self._execution if execution_id == self._execution.execution_id else None


@dataclass
class _Uow:
    results: _Results
    executions: _Executions


def _uow(
    *,
    estimand: str = "ATE",
    strategy: str = "BACKDOOR",
    adjustment: list[str] | None = None,
    treatment_type: str = "BINARY",
    outcome_type: str = "CONTINUOUS",
    checks: list[dict] | None = None,
) -> tuple[_Uow, dict, Result]:
    spec = _spec(estimand=estimand, strategy=strategy, adjustment=adjustment)
    execution = Execution(
        project_id="project",
        dataset_version_id="dataset",
        input_graph_version_id="graph",
        operation=ExecutionOperation.IDENTIFICATION,
        analysis_spec_json=spec,
    )
    upstream = Result(
        execution_id=execution.execution_id,
        result_type=ResultType.IDENTIFICATION_RESULT,
        scientific_status=ScientificStatus.IDENTIFIED,
        payload_json={
            "strategy": strategy,
            "estimand": estimand,
            "selected_adjustment_set": spec["causal_design"]["adjustment_set"],
        },
    )
    eligibility = Result(
        execution_id=execution.execution_id,
        result_type=ResultType.DATA_ELIGIBILITY_RESULT,
        scientific_status=ScientificStatus.PASS,
        payload_json={
            "status": "PASS",
            "inferred_types": {
                "treatment": {"type": treatment_type, "evidence": {}},
                "outcome": {"type": outcome_type, "evidence": {}},
            },
            "checks": checks if checks is not None else [
                {"check_code": "LIMITED_OVERLAP", "status": "PASS", "evidence": {}},
                {"check_code": "TREATMENT_PREVALENCE", "status": "PASS", "evidence": {}},
            ],
        },
    )
    return _Uow(_Results(upstream, eligibility), _Executions(execution)), spec, upstream


def _validate(
    uow: _Uow,
    spec: dict,
    upstream: Result,
    *,
    estimator: str,
    parameters: dict | None = None,
) -> None:
    ScientificValidationService().validate_submission(
        uow=uow,
        project_id="project",
        dataset_version_id="dataset",
        graph_version_id="graph",
        input_result_id=upstream.result_id,
        operation=ExecutionOperation.ESTIMATION,
        analysis_spec={
            **spec,
            "operation_spec": {"estimator": estimator, "inference_options": {}},
        },
        method=estimator,
        parameters=parameters or {},
    )


@pytest.mark.requirement("FR-054")
def test_compatible_estimators_can_reuse_one_identification_result() -> None:
    uow, spec, upstream = _uow()
    _validate(uow, spec, upstream, estimator="ols")
    _validate(uow, spec, upstream, estimator="ipw", parameters={"propensity_clip": [0.01, 0.99]})


@pytest.mark.requirement("FR-054")
@pytest.mark.parametrize(
    ("uow_kwargs", "estimator", "parameters", "expected_code"),
    [
        ({"estimand": "ATT", "strategy": "RANDOMIZED", "adjustment": []}, "difference_in_means", {}, "ESTIMATOR_ESTIMAND_INCOMPATIBLE"),
        ({"treatment_type": "UNSUPPORTED"}, "ols", {}, "ESTIMATOR_TREATMENT_TYPE_INCOMPATIBLE"),
        ({"outcome_type": "BINARY"}, "ols", {}, "ESTIMATOR_OUTCOME_TYPE_INCOMPATIBLE"),
        ({"strategy": "BACKDOOR"}, "difference_in_means", {}, "ESTIMATOR_IDENTIFICATION_STRATEGY_INCOMPATIBLE"),
        ({}, "unknown", {}, "ESTIMATOR_UNSUPPORTED"),
        ({}, "ols", {"unknown": True}, "ESTIMATOR_PARAMETER_UNSUPPORTED"),
    ],
)
def test_incompatible_estimator_contract_is_rejected_at_submission(
    uow_kwargs: dict,
    estimator: str,
    parameters: dict,
    expected_code: str,
) -> None:
    uow, spec, upstream = _uow(**uow_kwargs)
    with pytest.raises(ScientificContractViolation) as caught:
        _validate(uow, spec, upstream, estimator=estimator, parameters=parameters)
    assert caught.value.code == expected_code


@pytest.mark.requirement("FR-054")
def test_estimator_adjustment_and_overlap_prerequisites_are_enforced() -> None:
    uow, spec, upstream = _uow(strategy="RANDOMIZED", adjustment=["x"])
    with pytest.raises(ScientificContractViolation) as adjustment_error:
        _validate(uow, spec, upstream, estimator="difference_in_means")
    assert adjustment_error.value.code == "ESTIMATOR_ADJUSTMENT_INCOMPATIBLE"

    uow, spec, upstream = _uow(checks=[
        {"check_code": "TREATMENT_PREVALENCE", "status": "PASS", "evidence": {}},
    ])
    with pytest.raises(ScientificContractViolation) as diagnostics_error:
        _validate(uow, spec, upstream, estimator="ipw")
    assert diagnostics_error.value.code == "ESTIMATOR_DIAGNOSTIC_PREREQUISITE_MISSING"
