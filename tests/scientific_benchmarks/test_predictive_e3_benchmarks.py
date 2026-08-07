from __future__ import annotations

import pytest

from ariadne.capabilities.predictive.metrics import (
    classification_metrics,
    regression_metrics,
)
from ariadne.capabilities.predictive.modeling import fit_model, predict


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
