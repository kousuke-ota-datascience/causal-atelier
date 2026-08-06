from __future__ import annotations

import pytest

from ariadne.product.domain.analysis_spec import validate_analysis_spec
from ariadne.product.domain.enums import (
    ExecutionOperation, GraphOrigin, ResultType, ScientificStatus,
)
from ariadne.product.domain.errors import InvalidAnalysisSpec
from ariadne.product.domain.execution import Execution
from ariadne.product.domain.graph_version import GraphVersion
from ariadne.product.domain.result import Result
from ariadne.product.application.scientific_validation_service import ESTIMATOR_CAPABILITIES


@pytest.mark.requirement("FR-038", "FR-046", "FR-051")
@pytest.mark.parametrize(("operation", "graph", "upstream"), [
    (ExecutionOperation.DISCOVERY, None, None),
    (ExecutionOperation.IDENTIFICATION, "graph", None),
    (ExecutionOperation.ESTIMATION, "graph", "identification"),
    (ExecutionOperation.REFUTATION, "graph", "effect"),
    (ExecutionOperation.SENSITIVITY, "graph", "effect"),
])
def test_operation_input_contract_matrix(operation, graph, upstream):  # type: ignore[no-untyped-def]
    Execution(operation=operation, input_graph_version_id=graph, input_result_id=upstream)
    with pytest.raises(ValueError):
        Execution(operation=operation, input_graph_version_id=None if graph else "graph",
                  input_result_id=upstream)


@pytest.mark.requirement("FR-064", "FR-065")
@pytest.mark.parametrize(("result_type", "status"), [
    (ResultType.DISCOVERY_GRAPH_RESULT, ScientificStatus.GENERATED),
    (ResultType.IDENTIFICATION_RESULT, ScientificStatus.NOT_IDENTIFIED),
    (ResultType.DATA_ELIGIBILITY_RESULT, ScientificStatus.WARN),
    (ResultType.TREATMENT_EFFECT_RESULT, ScientificStatus.ESTIMATED),
    (ResultType.DIAGNOSTICS_RESULT, ScientificStatus.FAIL),
    (ResultType.REFUTATION_RESULT, ScientificStatus.NO_FAILURE_DETECTED),
    (ResultType.SENSITIVITY_RESULT, ScientificStatus.FRAGILE),
])
def test_result_status_contract_matrix(result_type, status):  # type: ignore[no-untyped-def]
    Result(result_type=result_type, scientific_status=status)
    with pytest.raises(InvalidAnalysisSpec):
        Result(result_type=result_type, scientific_status=ScientificStatus.IDENTIFIED
               if result_type != ResultType.IDENTIFICATION_RESULT else ScientificStatus.ESTIMATED)


@pytest.mark.requirement("FR-025", "FR-026", "FR-027")
@pytest.mark.parametrize("value", [
    GraphVersion(graph_origin=GraphOrigin.DISCOVERED, source_result_id="result"),
    GraphVersion(graph_origin=GraphOrigin.CONSTRAINT_ADJUSTED, parent_graph_version_id="parent"),
    GraphVersion(graph_origin=GraphOrigin.USER_DEFINED),
    GraphVersion(graph_origin=GraphOrigin.IMPORTED),
    GraphVersion(graph_origin=GraphOrigin.USER_EDITED, parent_graph_version_id="parent"),
])
def test_graph_origin_contract_matrix(value: GraphVersion) -> None:
    value.validate_origin()


@pytest.mark.requirement("NFR-009", "FR-053")
def test_snapshot_v2_rejects_unknown_fields_and_incomplete_override() -> None:
    value = {
        "schema_version": "causal-analysis-spec/2", "analysis_mode": "EXPLORATORY",
        "research_context": {}, "causal_question": {},
        "causal_design": {"adjustment_set": [], "assumptions": []},
        "operation_spec": {"feature_columns": ["x"], "constraints": {}, "expected_graph_type": None},
        "validation_override": None,
    }
    validate_analysis_spec(ExecutionOperation.DISCOVERY, value)
    with pytest.raises(InvalidAnalysisSpec):
        validate_analysis_spec(ExecutionOperation.DISCOVERY, {**value, "unknown": True})
    with pytest.raises(InvalidAnalysisSpec):
        validate_analysis_spec(ExecutionOperation.DISCOVERY, {
            **value, "validation_override": {"reason": "", "actor": "user", "warning_codes": ["X"]},
        })


@pytest.mark.requirement("FR-054")
def test_estimator_capability_registry_is_complete() -> None:
    required = {
        "estimands", "strategies", "parameters", "treatment_types", "outcome_types",
        "required_adjustment", "uncertainty_support", "overlap_requirement",
        "produced_diagnostics",
    }
    assert ESTIMATOR_CAPABILITIES
    assert all(set(capability) == required for capability in ESTIMATOR_CAPABILITIES.values())
