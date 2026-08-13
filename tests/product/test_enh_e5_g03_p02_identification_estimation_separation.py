"""Focused ENH-E5 G03 P02 identification/estimation boundary checks."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from ariadne.product.application.comparison_query_service import _build_comparison
from ariadne.product.domain.enums import AnalysisFamily, ExecutionOperation, ResultType, ScientificStatus
from ariadne.product.domain.errors import ScientificContractViolation


def _effect_result(result_id: str) -> SimpleNamespace:
    return SimpleNamespace(
        result_id=result_id,
        result_type=ResultType.TREATMENT_EFFECT_RESULT,
        scientific_status=ScientificStatus.ESTIMATED,
        summary_json={},
        warning_json=[],
    )


def _effect_execution(treatment: str, *, population: str = "all rows") -> SimpleNamespace:
    return SimpleNamespace(
        execution_id=f"execution-{treatment}",
        operation=ExecutionOperation.ESTIMATION,
        analysis_family=AnalysisFamily.CAUSAL,
        algorithm_or_estimator="ols",
        parameter_json={}, random_seed=42, dataset_version_id="dataset", input_graph_version_id="graph",
        analysis_spec_json={"causal_question": {
            "treatment": treatment, "outcome": "outcome", "estimand": "ATE", "population": population,
        }},
    )


def test_causal_effect_comparison_requires_the_exact_semantic_key() -> None:
    with pytest.raises(ScientificContractViolation) as captured:
        _build_comparison(
            [_effect_result("left"), _effect_result("right")],
            [_effect_execution("coupon"), _effect_execution("email")],
        )

    assert captured.value.code == "CAUSAL_COMPARISON_INCOMPATIBLE"
    assert "treatment/exposure" in str(captured.value)


def test_compatible_causal_effect_comparison_remains_available() -> None:
    comparison = _build_comparison(
        [_effect_result("left"), _effect_result("right")],
        [_effect_execution("coupon"), _effect_execution("coupon")],
    )

    assert comparison.operation == "ESTIMATION"
    assert comparison.warnings == []


def test_frontend_separates_identification_inputs_from_estimation_tuning() -> None:
    html = (Path(__file__).parents[2] / "frontend" / "index.html").read_text(encoding="utf-8")

    identification = html.split('<fieldset id="identification-inputs">', 1)[1].split('</fieldset>', 1)[0]
    estimation = html.split('<fieldset id="estimation-inputs">', 1)[1].split('</fieldset>', 1)[0]
    assert 'name="assumptions"' in identification
    assert 'id="run-identification"' in identification
    assert 'name="estimators"' not in identification
    assert 'name="identification_result_id"' in estimation
    assert 'name="estimators"' in estimation
