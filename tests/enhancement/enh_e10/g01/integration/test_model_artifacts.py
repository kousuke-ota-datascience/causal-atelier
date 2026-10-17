from __future__ import annotations

import json

import pytest

from ariadne.capabilities.predictive.modeling import (
    fit_model, load_model_artifact, predict, resolve_model_spec, serialize_model_artifact,
)
from ariadne.product.domain.errors import PredictiveValidationError


def _artifact(task: str, model_id: str, seed: int) -> dict:
    features = [[float(index), float(index % 3)] for index in range(60)]
    target = [int(index >= 30) for index in range(60)] if task == "BINARY_CLASSIFICATION" else [float(2 * index) for index in range(60)]
    resolved_id, parameters = resolve_model_spec(task, {"model_id": model_id, "parameters": {"num_boost_round": 8, "min_data_in_leaf": 4}} if model_id.startswith("lightgbm") else {"model_id": model_id})
    model = fit_model(task, resolved_id, parameters, features, target, seed=seed)
    model.update({"feature_order": ["x", "group"], "preprocessor_hash": "a" * 64, "seed": seed})
    return serialize_model_artifact(model)


@pytest.mark.parametrize("task,model_id", [("BINARY_CLASSIFICATION", "lightgbm_classifier.v1"), ("REGRESSION", "lightgbm_regressor.v1")])
def test_lightgbm_artifact_load_has_prediction_parity(task: str, model_id: str) -> None:
    artifact = _artifact(task, model_id, 17)
    restored = load_model_artifact(json.dumps(artifact), feature_order=["x", "group"], preprocessor_hash="a" * 64)
    features = [[1.0, 1.0], [40.0, 1.0]]
    assert predict(artifact, features) == predict(restored, features)
    assert artifact["schema_version"] == "fitted-model/2"
    assert artifact["provenance"]["python_version"]
    assert artifact["provenance"]["lightgbm_version"] == "4.7.0"


def test_model_identity_mismatches_are_rejected() -> None:
    artifact = _artifact("BINARY_CLASSIFICATION", "lightgbm_classifier.v1", 19)
    with pytest.raises(PredictiveValidationError) as feature:
        load_model_artifact(artifact, feature_order=["different"], preprocessor_hash="a" * 64)
    assert feature.value.code == "MODEL_FEATURE_MISMATCH"
    with pytest.raises(PredictiveValidationError) as preprocessor:
        load_model_artifact(artifact, feature_order=["x", "group"], preprocessor_hash="b" * 64)
    assert preprocessor.value.code == "PREPROCESSOR_MODEL_MISMATCH"


def test_legacy_linear_model_remains_readable() -> None:
    legacy = {"schema_version": "fitted-model/1", "model_id": "linear_regression.v1", "task_type": "REGRESSION", "parameters": {"l2": 0.0}, "coefficients": [2.0], "intercept": 1.0, "feature_order": ["x"], "preprocessor_hash": "p"}
    assert predict(load_model_artifact(legacy), [[3.0]]) == [7.0]


def test_in_memory_lightgbm_model_predicts_before_runner_binds_artifact_identity() -> None:
    features = [[float(index)] for index in range(40)]
    target = [int(index >= 20) for index in range(40)]
    model_id, parameters = resolve_model_spec(
        "BINARY_CLASSIFICATION",
        {"model_id": "lightgbm_classifier.v1", "parameters": {"num_boost_round": 4}},
    )
    model = fit_model("BINARY_CLASSIFICATION", model_id, parameters, features, target, seed=7)
    assert len(predict(model, features)) == len(features)
