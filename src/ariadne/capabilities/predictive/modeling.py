"""Small deterministic library-neutral model registry for ENH-E3 G4."""

from __future__ import annotations

import math
from typing import Any

import numpy as np

from ariadne.product.domain.errors import InvalidSchema, PredictiveValidationError
from ariadne.product.domain.schemas import reject_unknown

MODEL_REGISTRY = (
    {
        "model_id": "logistic_regression.v1",
        "supported_tasks": ["BINARY_CLASSIFICATION"],
        "parameter_schema": {
            "iterations": "integer[1,5000]",
            "learning_rate": "number(0,1]",
            "l2": "number[0,+inf)",
        },
        "deterministic_seed": True,
    },
    {
        "model_id": "linear_regression.v1",
        "supported_tasks": ["REGRESSION"],
        "parameter_schema": {"l2": "number[0,+inf)"},
        "deterministic_seed": True,
    },
)


def resolve_model_spec(task_type: str, spec: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    reject_unknown(spec, {"model_id", "parameters"}, name="model_spec")
    default = (
        "logistic_regression.v1"
        if task_type == "BINARY_CLASSIFICATION"
        else "linear_regression.v1"
    )
    model_id = spec.get("model_id", default)
    entry = next((item for item in MODEL_REGISTRY if item["model_id"] == model_id), None)
    if entry is None:
        raise PredictiveValidationError(
            "MODEL_NOT_REGISTERED", f"Model is not registered: {model_id}", path="model_spec.model_id"
        )
    if task_type not in entry["supported_tasks"]:
        raise PredictiveValidationError(
            "MODEL_TASK_MISMATCH",
            f"Model {model_id} is incompatible with {task_type}",
            path="model_spec.model_id",
        )
    parameters = dict(spec.get("parameters", {}))
    if model_id == "logistic_regression.v1":
        reject_unknown(parameters, {"iterations", "learning_rate", "l2"}, name="model parameters")
        parameters = {
            "iterations": parameters.get("iterations", 500),
            "learning_rate": parameters.get("learning_rate", 0.1),
            "l2": parameters.get("l2", 0.0),
        }
        if (
            isinstance(parameters["iterations"], bool)
            or not isinstance(parameters["iterations"], int)
            or not 1 <= parameters["iterations"] <= 5000
        ):
            raise InvalidSchema("logistic iterations must be an integer in [1, 5000]")
        if not 0 < float(parameters["learning_rate"]) <= 1:
            raise InvalidSchema("logistic learning_rate must be in (0, 1]")
    else:
        reject_unknown(parameters, {"l2"}, name="model parameters")
        parameters = {"l2": parameters.get("l2", 0.0)}
    if float(parameters["l2"]) < 0 or not math.isfinite(float(parameters["l2"])):
        raise InvalidSchema("model l2 must be finite and non-negative")
    return str(model_id), parameters


def fit_model(
    task_type: str,
    model_id: str,
    parameters: dict[str, Any],
    features: list[list[float]],
    target: list[Any],
    *,
    seed: int,
) -> dict[str, Any]:
    del seed  # Registry contract accepts and records seed; selected algorithms are deterministic.
    matrix = _matrix(features)
    if task_type == "BINARY_CLASSIFICATION":
        classes = sorted(set(target), key=str)
        if len(classes) != 2:
            raise PredictiveValidationError(
                "BINARY_TARGET_REQUIRED",
                "Binary training requires two classes",
                path="prediction_question.target",
            )
        encoded = np.asarray([int(value == classes[1]) for value in target], dtype=float)
        weights = np.zeros(matrix.shape[1], dtype=float)
        intercept = 0.0
        learning_rate = float(parameters["learning_rate"])
        l2 = float(parameters["l2"])
        for _ in range(int(parameters["iterations"])):
            logits = np.clip(matrix @ weights + intercept, -35, 35)
            probability = 1 / (1 + np.exp(-logits))
            residual = probability - encoded
            weights -= learning_rate * ((matrix.T @ residual) / len(matrix) + l2 * weights)
            intercept -= learning_rate * float(residual.mean())
        return {
            "schema_version": "fitted-model/1",
            "model_id": model_id,
            "task_type": task_type,
            "parameters": parameters,
            "coefficients": weights.tolist(),
            "intercept": intercept,
            "classes": [_json_scalar(value) for value in classes],
        }
    observed = np.asarray([float(value) for value in target], dtype=float)
    design = np.column_stack([np.ones(len(matrix)), matrix])
    penalty = np.eye(design.shape[1]) * float(parameters["l2"])
    penalty[0, 0] = 0
    coefficients = np.linalg.pinv(design.T @ design + penalty) @ design.T @ observed
    return {
        "schema_version": "fitted-model/1",
        "model_id": model_id,
        "task_type": task_type,
        "parameters": parameters,
        "coefficients": coefficients[1:].tolist(),
        "intercept": float(coefficients[0]),
    }


def predict(model: dict[str, Any], features: list[list[float]]) -> list[float]:
    matrix = _matrix(features)
    weights = np.asarray(model["coefficients"], dtype=float)
    values = matrix @ weights + float(model["intercept"])
    if model["task_type"] == "BINARY_CLASSIFICATION":
        values = 1 / (1 + np.exp(-np.clip(values, -35, 35)))
    return [float(value) for value in values]


def encode_binary_target(model: dict[str, Any], target: list[Any]) -> list[int]:
    classes = model["classes"]
    if any(value not in classes for value in target):
        raise PredictiveValidationError(
            "UNKNOWN_TARGET_CLASS",
            "Evaluation target contains a class absent from TRAIN",
            path="prediction_question.target",
        )
    return [int(value == classes[1]) for value in target]


def _matrix(features: list[list[float]]) -> np.ndarray:
    matrix = np.asarray(features, dtype=float)
    if matrix.ndim != 2 or not len(matrix) or matrix.shape[1] == 0:
        raise PredictiveValidationError(
            "EMPTY_FEATURE_MATRIX", "Model requires a non-empty feature matrix", path="feature_spec"
        )
    if not np.isfinite(matrix).all():
        raise PredictiveValidationError(
            "NON_FINITE_FEATURE", "Feature matrix contains non-finite values", path="feature_spec"
        )
    return matrix


def _json_scalar(value: Any) -> Any:
    return value.item() if hasattr(value, "item") else value
