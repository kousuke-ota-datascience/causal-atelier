from __future__ import annotations

import pytest

from ariadne.capabilities.predictive.metrics import (
    classification_metrics,
    regression_metrics,
)
from ariadne.capabilities.predictive.training_runners import PredictiveEvaluateRunner
from ariadne.product.domain.execution_plan import StageDefinition, StageType
from ariadne.product.workflow.contracts import StageContext


def _context(spec: dict, *, task_type: str, target: list[object]) -> StageContext:  # type: ignore[type-arg]
    classes = [0, 1]
    model = {
        "schema_version": "fitted-model/1",
        "model_id": (
            "logistic_regression.v1"
            if task_type == "BINARY_CLASSIFICATION"
            else "linear_regression.v1"
        ),
        "task_type": task_type,
        "parameters": {},
        "coefficients": [1.0],
        "intercept": 0.0,
        "preprocessor_hash": "preprocessor-hash",
        "feature_order": ["score"],
        "seed": 17,
    }
    if task_type == "BINARY_CLASSIFICATION":
        model["classes"] = classes
    return StageContext(
        execution_id="evaluation",
        stage=StageDefinition(
            stage_key="evaluate",
            stage_type=StageType("predictive", "evaluate", "1"),
            input_contract={
                "frozen_model": "fitted-model/1",
                "evaluation_bundle": "predictive-evaluation-bundle/1",
                "fitted_preprocessor": "fitted-preprocessor/1",
            },
            output_contract={"evaluation_summary": "predictive-evaluation-result/1"},
            parameters=spec,
        ),
        inputs={
            "frozen_model": model,
            "evaluation_bundle": {
                "schema_version": "predictive-evaluation-bundle/1",
                "test": {
                    "row_ordinals": list(range(len(target))),
                    "features": [[-2.0 + index] for index in range(len(target))],
                    "target": target,
                },
                "selection_allowed": False,
                "final_evaluation_only": True,
            },
            "fitted_preprocessor": {
                "schema_version": "fitted-preprocessor/1",
                "fit_partition": "TRAIN",
                "canonical_hash": "preprocessor-hash",
            },
        },
    )


@pytest.mark.requirement("G4-PREDICTIVE-CLASSIFICATION-EVALUATION")
def test_classification_metrics_include_probability_threshold_balance_and_calibration(
    predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    metrics = classification_metrics([0, 0, 1, 1], [0.05, 0.2, 0.8, 0.95])
    assert metrics["roc_auc"] == 1.0
    assert metrics["pr_auc"] == 1.0
    assert metrics["log_loss"] > 0
    assert metrics["brier"] > 0
    assert metrics["threshold"] == 0.5
    assert metrics["class_balance"] == 0.5
    assert metrics["calibration"]
    assert metrics["sample_count"] == 4

    runner = PredictiveEvaluateRunner()
    context = _context(
        predictive_spec_factory(),
        task_type="BINARY_CLASSIFICATION",
        target=[0, 0, 1, 1],
    )
    runner.validate(context)
    outcome = runner.run(context)
    evaluation = next(
        result for result in outcome.results if result.result_type == "EVALUATION_RESULT"
    )
    errors = next(
        result for result in outcome.results
        if result.result_type == "ERROR_ANALYSIS_RESULT"
    )
    assert evaluation.analytical_status == "EVALUATED"
    assert evaluation.payload["evaluation_population"] == "TEST"
    assert evaluation.summary["sample_count"] == 4
    assert evaluation.payload["sample_count"] == 4
    assert evaluation.payload["metrics"]["sample_count"] == 4
    assert errors.analytical_status == "GENERATED"


@pytest.mark.requirement("G4-PREDICTIVE-EVALUATION-STATUS")
def test_one_class_test_population_has_explicit_insufficient_status(
    predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    runner = PredictiveEvaluateRunner()
    context = _context(
        predictive_spec_factory(),
        task_type="BINARY_CLASSIFICATION",
        target=[0, 0, 0],
    )
    runner.validate(context)
    outcome = runner.run(context)
    evaluation = next(
        result for result in outcome.results if result.result_type == "EVALUATION_RESULT"
    )
    assert evaluation.analytical_status == "INSUFFICIENT_TEST_SAMPLE"
    assert evaluation.payload["metrics"]["roc_auc"] is None
    assert evaluation.payload["metrics"]["pr_auc"] is None


@pytest.mark.requirement("G4-PREDICTIVE-REGRESSION-EVALUATION")
def test_regression_metrics_include_residual_summary(predictive_spec_factory) -> None:  # type: ignore[no-untyped-def]
    metrics = regression_metrics([1.0, 2.0, 3.0], [1.5, 2.0, 2.5])
    assert set(metrics) == {"sample_count", "mae", "rmse", "r2", "residual_summary"}
    assert metrics["residual_summary"] == {
        "mean": 0.0,
        "min": -0.5,
        "median": 0.0,
        "max": 0.5,
    }

    runner = PredictiveEvaluateRunner()
    context = _context(
        predictive_spec_factory("REGRESSION"),
        task_type="REGRESSION",
        target=[-2.0, -1.0, 0.0, 1.0],
    )
    runner.validate(context)
    result = runner.run(context).results[0]
    assert result.analytical_status == "EVALUATED"
    assert "residual_summary" in result.payload["metrics"]
