from __future__ import annotations

import pandas as pd
import pytest

from ariadne.capabilities.predictive.metrics import (
    classification_metrics,
    regression_metrics,
)
from ariadne.capabilities.predictive.modeling import fit_model, predict
from ariadne.capabilities.predictive.preprocessing import (
    fit_preprocessor,
    transform_frame,
)
from ariadne.capabilities.predictive.validation import (
    assert_test_isolation,
    validate_predictive_specification,
)
from ariadne.product.domain.errors import PredictiveValidationError


@pytest.mark.requirement("G4-SCIENTIFIC-BENCHMARK-TRAIN-ONLY-FIT")
def test_preprocessor_fits_train_only_and_only_transforms_untouched_test() -> None:
    train = pd.DataFrame({"score": [0.0, 2.0]})
    untouched_test = pd.DataFrame({"score": [100.0]})
    fitted = fit_preprocessor(
        train,
        ["score"],
        {
            "fit_partition": "TRAIN",
            "numeric_imputation": "MEAN",
            "scale_numeric": True,
            "categorical_encoding": "ONE_HOT",
        },
    )

    assert fitted["fit_partition"] == "TRAIN"
    assert fitted["columns"][0]["mean"] == 1.0
    assert fitted["columns"][0]["scale"] == 1.0
    fitted_hash = fitted["canonical_hash"]
    assert transform_frame(untouched_test, fitted) == [[99.0]]
    assert fitted["canonical_hash"] == fitted_hash


@pytest.mark.requirement("G4-SCIENTIFIC-BENCHMARK-TEST-ISOLATION")
def test_test_partition_is_rejected_from_model_selection() -> None:
    assert_test_isolation(["TRAIN", "VALIDATION"])
    with pytest.raises(PredictiveValidationError) as captured:
        assert_test_isolation(["TRAIN", "VALIDATION", "TEST"])
    assert captured.value.code == "TEST_ISOLATION_VIOLATION"
    assert captured.value.path == "tuning_spec.selection_partitions"


@pytest.mark.requirement("G4-SCIENTIFIC-BENCHMARK-DELIBERATE-LEAKAGE")
def test_predictive_contract_rejects_deliberate_target_leakage() -> None:
    leaking_specification = _binary_specification(feature_columns=["converted"])
    with pytest.raises(PredictiveValidationError) as captured:
        validate_predictive_specification(leaking_specification)
    assert captured.value.code == "TARGET_LEAKAGE_DETECTED"
    assert captured.value.path == "feature_spec.feature_columns"


@pytest.mark.requirement("G4-SCIENTIFIC-BENCHMARK-CLASSIFICATION")
def test_logistic_registry_model_recovers_deterministic_separable_signal() -> None:
    features = [[value / 50] for value in range(-200, 200)]
    target = [int(row[0] >= 0) for row in features]
    parameters = {"iterations": 1500, "learning_rate": 0.2, "l2": 0.001}
    first = fit_model(
        "BINARY_CLASSIFICATION",
        "logistic_regression.v1",
        parameters,
        features,
        target,
        seed=29,
    )
    second = fit_model(
        "BINARY_CLASSIFICATION",
        "logistic_regression.v1",
        parameters,
        features,
        target,
        seed=29,
    )
    assert first == second
    metrics = classification_metrics(target, predict(first, features))
    assert metrics["roc_auc"] > 0.99
    assert metrics["pr_auc"] > 0.99
    assert metrics["log_loss"] < 0.25
    assert metrics["brier"] < 0.08


@pytest.mark.requirement("G4-SCIENTIFIC-BENCHMARK-REGRESSION")
def test_linear_registry_model_recovers_exact_affine_signal() -> None:
    features = [[float(value)] for value in range(-100, 101)]
    target = [3.5 * row[0] - 2.25 for row in features]
    model = fit_model(
        "REGRESSION",
        "linear_regression.v1",
        {"l2": 0.0},
        features,
        target,
        seed=29,
    )
    metrics = regression_metrics(target, predict(model, features))
    assert metrics["mae"] < 1e-10
    assert metrics["rmse"] < 1e-10
    assert metrics["r2"] > 0.999999999999


def _binary_specification(*, feature_columns: list[str]) -> dict[str, object]:
    return {
        "schema_version": "predictive-analysis-spec/1",
        "task_type": "BINARY_CLASSIFICATION",
        "prediction_question": {
            "prediction_unit": "customer",
            "target": "converted",
            "prediction_time": "2026-01-01T00:00:00Z",
            "horizon": "30 days",
            "intended_use": "prioritize outreach",
            "deployment_population": "eligible customers",
        },
        "feature_spec": {
            "feature_columns": feature_columns,
            "availability_cutoff": {
                column: {
                    "column": column,
                    "available_at": "PREDICTION_TIME",
                    "allowed": True,
                }
                for column in feature_columns
            },
            "excluded_columns": ["customer_id"],
        },
        "split_spec": {
            "strategy": "RANDOM",
            "train_ratio": 0.6,
            "validation_ratio": 0.2,
            "test_ratio": 0.2,
            "group_column": None,
            "time_column": None,
            "train_cutoff": None,
            "validation_cutoff": None,
            "stratify": False,
            "seed": 29,
        },
        "preprocessing_spec": {"fit_partition": "TRAIN"},
        "model_spec": {},
        "tuning_spec": {"selection_partitions": ["TRAIN", "VALIDATION"]},
        "evaluation_spec": {
            "primary_metric": "ROC_AUC",
            "secondary_metrics": ["PR_AUC", "LOG_LOSS", "BRIER"],
            "subgroups": [],
        },
        "explanation_spec": {},
    }
