"""Provider-neutral predictive model capabilities and specification validation."""

from __future__ import annotations

import math
import importlib
import json
import platform
from importlib import metadata as importlib_metadata
from importlib import util as importlib_util
from collections.abc import Mapping
from typing import Any

import numpy as np

from ariadne.product.domain.errors import PredictiveValidationError
from ariadne.product.domain.schemas import reject_unknown

_LIGHTGBM_REQUIREMENT = ">=4.7.0,<4.8"


MODEL_REGISTRY = (
    {
        "model_id": "logistic_regression.v1",
        "provider_id": "ariadne.native",
        "supported_tasks": ["BINARY_CLASSIFICATION"],
        "parameter_schema": {
            "iterations": {"type": "integer", "minimum": 1, "maximum": 5000, "default": 500},
            "learning_rate": {"type": "number", "exclusive_minimum": 0, "maximum": 1, "default": 0.1},
            "l2": {"type": "number", "minimum": 0, "default": 0.0},
        },
        "deterministic_seed": True,
        "serializer_id": "ariadne.native-linear-model/1",
        "loader_id": "ariadne.native-linear-model/1",
        "task_default": True,
        "dependency": None,
    },
    {
        "model_id": "linear_regression.v1",
        "provider_id": "ariadne.native",
        "supported_tasks": ["REGRESSION"],
        "parameter_schema": {"l2": {"type": "number", "minimum": 0, "default": 0.0}},
        "deterministic_seed": True,
        "serializer_id": "ariadne.native-linear-model/1",
        "loader_id": "ariadne.native-linear-model/1",
        "task_default": True,
        "dependency": None,
    },
    {
        "model_id": "lightgbm_classifier.v1",
        "provider_id": "lightgbm",
        "supported_tasks": ["BINARY_CLASSIFICATION"],
        "parameter_schema": {
            "num_boost_round": {"type": "integer", "minimum": 1, "maximum": 2000, "default": 100},
            "learning_rate": {"type": "number", "exclusive_minimum": 0, "maximum": 1, "default": 0.1},
            "num_leaves": {"type": "integer", "minimum": 2, "maximum": 256, "default": 31},
            "max_depth": {"type": "integer", "minimum": -1, "maximum": 64, "default": -1},
            "min_data_in_leaf": {"type": "integer", "minimum": 1, "maximum": 10000, "default": 20},
            "lambda_l2": {"type": "number", "minimum": 0, "default": 0.0},
        },
        "deterministic_seed": True,
        "serializer_id": "lightgbm.booster/1",
        "loader_id": "lightgbm.booster/1",
        "task_default": False,
        "dependency": {"extra": "predictive-advanced", "distribution": "lightgbm", "module": "lightgbm", "requirement": _LIGHTGBM_REQUIREMENT},
    },
    {
        "model_id": "lightgbm_regressor.v1",
        "provider_id": "lightgbm",
        "supported_tasks": ["REGRESSION"],
        "parameter_schema": {
            "num_boost_round": {"type": "integer", "minimum": 1, "maximum": 2000, "default": 100},
            "learning_rate": {"type": "number", "exclusive_minimum": 0, "maximum": 1, "default": 0.1},
            "num_leaves": {"type": "integer", "minimum": 2, "maximum": 256, "default": 31},
            "max_depth": {"type": "integer", "minimum": -1, "maximum": 64, "default": -1},
            "min_data_in_leaf": {"type": "integer", "minimum": 1, "maximum": 10000, "default": 20},
            "lambda_l2": {"type": "number", "minimum": 0, "default": 0.0},
        },
        "deterministic_seed": True,
        "serializer_id": "lightgbm.booster/1",
        "loader_id": "lightgbm.booster/1",
        "task_default": False,
        "dependency": {"extra": "predictive-advanced", "distribution": "lightgbm", "module": "lightgbm", "requirement": _LIGHTGBM_REQUIREMENT},
    },
)


def model_capabilities() -> tuple[dict[str, Any], ...]:
    """Return registry descriptors with lazy optional-dependency status.

    This intentionally discovers metadata only; it never imports an optional provider.
    """
    return tuple({**entry, "availability": _availability(entry["dependency"])} for entry in MODEL_REGISTRY)


def _availability(dependency: dict[str, str] | None) -> dict[str, Any]:
    if dependency is None:
        return {"available": True, "version": None, "reason": None}
    if importlib_util.find_spec(dependency["module"]) is None:
        return {
            "available": False,
            "version": None,
            "reason": f"Optional dependency {dependency['distribution']} is not installed; install extra {dependency['extra']}",
        }
    try:
        version = importlib_metadata.version(dependency["distribution"])
    except importlib_metadata.PackageNotFoundError:
        return {"available": False, "version": None, "reason": f"Distribution metadata for {dependency['distribution']} is unavailable"}
    if not _is_lightgbm_version_supported(version):
        return {"available": False, "version": version, "reason": f"{dependency['distribution']} {version} does not satisfy {dependency['requirement']}"}
    return {"available": True, "version": version, "reason": None}


def _is_lightgbm_version_supported(version: str) -> bool:
    """Check the deliberately narrow LightGBM contract without importing LightGBM."""
    parts = version.split(".")
    try:
        major, minor, patch = (int(parts[index]) for index in range(3))
    except (ValueError, IndexError):
        return False
    return (major, minor, patch) >= (4, 7, 0) and (major, minor) < (4, 8)


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
    availability = _availability(entry["dependency"])
    if not availability["available"]:
        raise PredictiveValidationError(
            "MODEL_DEPENDENCY_UNAVAILABLE",
            f"Model {model_id} is unavailable: {availability['reason']}",
            path="model_spec.model_id",
        )
    raw_parameters = spec.get("parameters", {})
    if not isinstance(raw_parameters, Mapping):
        raise _parameter_error("model parameters must be an object")
    parameters = dict(raw_parameters)
    if model_id == "logistic_regression.v1":
        _reject_unknown_model_parameters(parameters, {"iterations", "learning_rate", "l2"})
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
            raise _parameter_error("logistic iterations must be an integer in [1, 5000]")
        if not _finite_in_range(parameters["learning_rate"], lower=0, upper=1, lower_exclusive=True):
            raise _parameter_error("logistic learning_rate must be in (0, 1]")
    elif model_id.startswith("lightgbm_"):
        parameters = _resolve_lightgbm_parameters(parameters)
    else:
        _reject_unknown_model_parameters(parameters, {"l2"})
        parameters = {"l2": parameters.get("l2", 0.0)}
    if "l2" in parameters and not _finite_in_range(parameters["l2"], lower=0):
        raise _parameter_error("model l2 must be finite and non-negative")
    return str(model_id), parameters


def _resolve_lightgbm_parameters(parameters: dict[str, Any]) -> dict[str, Any]:
    _reject_unknown_model_parameters(
        parameters,
        {"num_boost_round", "learning_rate", "num_leaves", "max_depth", "min_data_in_leaf", "lambda_l2"},
    )
    resolved = {
        "num_boost_round": parameters.get("num_boost_round", 100),
        "learning_rate": parameters.get("learning_rate", 0.1),
        "num_leaves": parameters.get("num_leaves", 31),
        "max_depth": parameters.get("max_depth", -1),
        "min_data_in_leaf": parameters.get("min_data_in_leaf", 20),
        "lambda_l2": parameters.get("lambda_l2", 0.0),
    }
    if not _integer_in_range(resolved["num_boost_round"], 1, 2000):
        raise _parameter_error("lightgbm num_boost_round must be an integer in [1, 2000]")
    if not _finite_in_range(resolved["learning_rate"], lower=0, upper=1, lower_exclusive=True):
        raise _parameter_error("lightgbm learning_rate must be in (0, 1]")
    if not _integer_in_range(resolved["num_leaves"], 2, 256):
        raise _parameter_error("lightgbm num_leaves must be an integer in [2, 256]")
    if resolved["max_depth"] != -1 and not _integer_in_range(resolved["max_depth"], 1, 64):
        raise _parameter_error("lightgbm max_depth must be -1 or an integer in [1, 64]")
    if not _integer_in_range(resolved["min_data_in_leaf"], 1, 10000):
        raise _parameter_error("lightgbm min_data_in_leaf must be an integer in [1, 10000]")
    if not _finite_in_range(resolved["lambda_l2"], lower=0):
        raise _parameter_error("lightgbm lambda_l2 must be finite and non-negative")
    return resolved


def _parameter_error(message: str) -> PredictiveValidationError:
    return PredictiveValidationError("MODEL_PARAMETER_INVALID", message, path="model_spec.parameters")


def _reject_unknown_model_parameters(parameters: dict[str, Any], allowed: set[str]) -> None:
    unknown = sorted(set(parameters) - allowed)
    if unknown:
        raise _parameter_error(f"Unknown model parameters: {unknown}")


def _finite_in_range(
    value: Any, *, lower: float, upper: float | None = None, lower_exclusive: bool = False
) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)):
        return False
    return (float(value) > lower if lower_exclusive else float(value) >= lower) and (
        upper is None or float(value) <= upper
    )


def _integer_in_range(value: Any, lower: int, upper: int) -> bool:
    return not isinstance(value, bool) and isinstance(value, int) and lower <= value <= upper


def fit_model(
    task_type: str,
    model_id: str,
    parameters: dict[str, Any],
    features: list[list[float]],
    target: list[Any],
    *,
    seed: int,
) -> dict[str, Any]:
    matrix = _matrix(features)
    if model_id.startswith("lightgbm_"):
        return _fit_lightgbm_model(task_type, model_id, parameters, matrix, target, seed=seed)
    del seed  # Selected native algorithms are deterministic.
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
    # ``fit_model`` returns an in-memory v1-compatible model. Durable artifacts
    # are validated on load, after the runner has bound feature/preprocessor identity.
    if model.get("schema_version") == "fitted-model/2" or {
        "feature_order", "preprocessor_hash"
    }.issubset(model):
        model = load_model_artifact(model)
    matrix = _matrix(features)
    if str(model["model_id"]).startswith("lightgbm_"):
        lightgbm = _load_lightgbm()
        booster = lightgbm.Booster(model_str=str(model["booster_model"]))
        return [float(value) for value in booster.predict(matrix)]
    weights = np.asarray(model["coefficients"], dtype=float)
    values = matrix @ weights + float(model["intercept"])
    if model["task_type"] == "BINARY_CLASSIFICATION":
        values = 1 / (1 + np.exp(-np.clip(values, -35, 35)))
    return [float(value) for value in values]


def serialize_model_artifact(model: dict[str, Any]) -> dict[str, Any]:
    """Produce the durable fitted-model/2 representation without pickle/joblib."""
    serialized = dict(model)
    is_lightgbm = str(model["model_id"]).startswith("lightgbm_")
    serialized.update({
        "schema_version": "fitted-model/2",
        "provider": "lightgbm" if is_lightgbm else "ariadne.native",
        "payload_format": "lightgbm-model-string/1" if is_lightgbm else "ariadne-linear-json/1",
        "library": "lightgbm" if is_lightgbm else "ariadne",
        "library_version": _library_version("lightgbm" if is_lightgbm else "ariadne"),
        "provenance": {
            "python_version": platform.python_version(),
            "ariadne_version": _library_version("ariadne"),
            "lightgbm_version": _library_version("lightgbm") if is_lightgbm else None,
            "determinism": model.get("runtime", {"deterministic": True}),
        },
    })
    return serialized


def load_model_artifact(
    artifact: dict[str, Any] | bytes | str,
    *,
    feature_order: list[str] | None = None,
    preprocessor_hash: str | None = None,
) -> dict[str, Any]:
    """Load v1/v2 JSON model payloads and enforce optional identity expectations."""
    try:
        model = json.loads(artifact) if isinstance(artifact, (bytes, str)) else dict(artifact)
    except (TypeError, ValueError, UnicodeDecodeError) as exc:
        raise PredictiveValidationError("MODEL_ARTIFACT_LOAD_FAILED", "Model artifact is not valid JSON") from exc
    if model.get("schema_version") not in {"fitted-model/1", "fitted-model/2"}:
        raise PredictiveValidationError("MODEL_ARTIFACT_UNSUPPORTED", "Unsupported fitted model schema")
    is_lightgbm = str(model.get("model_id", "")).startswith("lightgbm_")
    if model["schema_version"] == "fitted-model/2":
        required_format = "lightgbm-model-string/1" if is_lightgbm else "ariadne-linear-json/1"
        if model.get("payload_format") != required_format:
            raise PredictiveValidationError("MODEL_ARTIFACT_UNSUPPORTED", "Model payload format does not match provider")
    required = {"model_id", "task_type", "parameters", "preprocessor_hash", "feature_order"}
    if not required.issubset(model):
        raise PredictiveValidationError("MODEL_ARTIFACT_LOAD_FAILED", "Model artifact is missing required identity fields")
    if feature_order is not None and model["feature_order"] != feature_order:
        raise PredictiveValidationError("MODEL_FEATURE_MISMATCH", "Model feature order does not match", path="feature_order")
    if preprocessor_hash is not None and model["preprocessor_hash"] != preprocessor_hash:
        raise PredictiveValidationError("PREPROCESSOR_MODEL_MISMATCH", "Model preprocessor identity does not match", path="preprocessor_hash")
    return model


def _library_version(distribution: str) -> str | None:
    try:
        return importlib_metadata.version(distribution)
    except importlib_metadata.PackageNotFoundError:
        return None


def _fit_lightgbm_model(
    task_type: str,
    model_id: str,
    parameters: dict[str, Any],
    matrix: np.ndarray,
    target: list[Any],
    *,
    seed: int,
) -> dict[str, Any]:
    lightgbm = _load_lightgbm()
    runtime = {
        "objective": "binary" if task_type == "BINARY_CLASSIFICATION" else "regression",
        "metric": None,
        "device_type": "cpu",
        "deterministic": True,
        "force_col_wise": True,
        "num_threads": 1,
        "seed": seed,
        "verbosity": -1,
        "use_missing": False,
    }
    if task_type == "BINARY_CLASSIFICATION":
        classes = sorted(set(target), key=str)
        if len(classes) != 2:
            raise PredictiveValidationError(
                "BINARY_TARGET_REQUIRED",
                "Binary training requires two classes",
                path="prediction_question.target",
            )
        labels = np.asarray([int(value == classes[1]) for value in target], dtype=float)
    else:
        classes = None
        labels = np.asarray([float(value) for value in target], dtype=float)
    train_parameters = {
        "objective": runtime["objective"],
        "metric": "None",
        "device_type": runtime["device_type"],
        "deterministic": runtime["deterministic"],
        "force_col_wise": runtime["force_col_wise"],
        "num_threads": runtime["num_threads"],
        "seed": runtime["seed"],
        "verbosity": runtime["verbosity"],
        "use_missing": runtime["use_missing"],
        "learning_rate": parameters["learning_rate"],
        "num_leaves": parameters["num_leaves"],
        "max_depth": parameters["max_depth"],
        "min_data_in_leaf": parameters["min_data_in_leaf"],
        "lambda_l2": parameters["lambda_l2"],
    }
    booster = lightgbm.train(
        train_parameters,
        lightgbm.Dataset(matrix, label=labels, free_raw_data=False),
        num_boost_round=parameters["num_boost_round"],
    )
    model = {
        "schema_version": "fitted-model/1",
        "model_id": model_id,
        "task_type": task_type,
        "parameters": parameters,
        "runtime": runtime,
        "booster_model": booster.model_to_string(),
    }
    if classes is not None:
        model["classes"] = [_json_scalar(value) for value in classes]
    return model


def _load_lightgbm() -> Any:
    try:
        return importlib.import_module("lightgbm")
    except ImportError as exc:
        raise PredictiveValidationError(
            "MODEL_DEPENDENCY_UNAVAILABLE",
            "LightGBM could not be imported; install extra predictive-advanced",
            path="model_spec.model_id",
        ) from exc


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
