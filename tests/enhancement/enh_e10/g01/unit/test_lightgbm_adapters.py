from __future__ import annotations

import pytest

from ariadne.capabilities.predictive.modeling import fit_model, predict, resolve_model_spec
from ariadne.product.domain.errors import PredictiveValidationError


def _classification_data() -> tuple[list[list[float]], list[int]]:
    features = [[float(index), float(index % 3)] for index in range(80)]
    return features, [int(index >= 40) for index in range(80)]


def _regression_data() -> tuple[list[list[float]], list[float]]:
    features = [[float(index), float(index % 5)] for index in range(80)]
    return features, [2.0 * index - 0.5 * (index % 5) for index in range(80)]


def test_lightgbm_binary_fit_predict_is_deterministic_and_returns_probability() -> None:
    features, target = _classification_data()
    model_id, parameters = resolve_model_spec(
        "BINARY_CLASSIFICATION",
        {
            "model_id": "lightgbm_classifier.v1",
            "parameters": {"num_boost_round": 12, "min_data_in_leaf": 5},
        },
    )
    first = fit_model("BINARY_CLASSIFICATION", model_id, parameters, features, target, seed=719)
    second = fit_model("BINARY_CLASSIFICATION", model_id, parameters, features, target, seed=719)

    assert first["booster_model"] == second["booster_model"]
    assert first["classes"] == [0, 1]
    assert first["runtime"] == {
        "objective": "binary",
        "metric": None,
        "device_type": "cpu",
        "deterministic": True,
        "force_col_wise": True,
        "num_threads": 1,
        "seed": 719,
        "verbosity": -1,
        "use_missing": False,
    }
    probabilities = predict(first, features)
    assert len(probabilities) == len(target)
    assert all(0.0 <= probability <= 1.0 for probability in probabilities)


def test_lightgbm_regression_fit_predict_is_deterministic_and_numeric() -> None:
    features, target = _regression_data()
    model_id, parameters = resolve_model_spec(
        "REGRESSION", {"model_id": "lightgbm_regressor.v1"}
    )
    first = fit_model("REGRESSION", model_id, parameters, features, target, seed=941)
    second = fit_model("REGRESSION", model_id, parameters, features, target, seed=941)

    assert first["booster_model"] == second["booster_model"]
    prediction = predict(first, features)
    assert len(prediction) == len(target)
    assert all(isinstance(value, float) for value in prediction)
    assert first["runtime"]["objective"] == "regression"
    assert first["runtime"]["seed"] == 941


@pytest.mark.parametrize(
    "parameters",
    [
        {"num_boost_round": 0},
        {"learning_rate": 1.1},
        {"num_leaves": 257},
        {"max_depth": 0},
        {"min_data_in_leaf": 0},
        {"lambda_l2": -1.0},
        {"unsupported": 1},
    ],
)
def test_lightgbm_rejects_non_contract_parameters(parameters: dict[str, object]) -> None:
    with pytest.raises(PredictiveValidationError) as invalid:
        resolve_model_spec(
            "BINARY_CLASSIFICATION",
            {"model_id": "lightgbm_classifier.v1", "parameters": parameters},
        )
    assert invalid.value.code == "MODEL_PARAMETER_INVALID"


def test_lightgbm_task_mismatch_is_rejected_before_fitting() -> None:
    with pytest.raises(PredictiveValidationError) as mismatch:
        resolve_model_spec(
            "REGRESSION", {"model_id": "lightgbm_classifier.v1"}
        )
    assert mismatch.value.code == "MODEL_TASK_MISMATCH"
