"""Actual LIME local-only provider adapter."""
from __future__ import annotations
import hashlib
import importlib
import math
from typing import Any
import numpy as np
from ariadne.capabilities.predictive.modeling import predict
from ariadne.product.domain.errors import PredictiveValidationError

def explain_lime_local(model: dict[str, Any], reference_features: list[list[float]], instance: list[float], row_ordinal: int, sampling_seed: int) -> dict[str, Any]:
    if model.get("model_id") not in {"logistic_regression.v1", "linear_regression.v1", "lightgbm_classifier.v1", "lightgbm_regressor.v1"}:
        raise PredictiveValidationError("EXPLANATION_METHOD_NOT_APPLICABLE", "LIME_TABULAR model is unsupported")
    try:
        module = importlib.import_module("lime.lime_tabular")
        version = importlib.metadata.version("lime")
    except (ImportError, importlib.metadata.PackageNotFoundError) as exc:
        raise PredictiveValidationError("EXPLANATION_DEPENDENCY_UNAVAILABLE", "LIME dependency is unavailable") from exc
    names, seed = model["feature_order"], (sampling_seed * 1_000_003 + row_ordinal) % (2**32)
    params = {"num_samples": 2000, "num_features": min(10, len(names)), "feature_selection": "auto", "discretize_continuous": False, "distance_metric": "euclidean", "kernel_width": .75 * math.sqrt(len(names)), "sample_around_instance": False}
    classification = model["task_type"] == "BINARY_CLASSIFICATION"
    # One-hot output columns represent a binary categorical variable, not a
    # continuous quantity.  Tell LIME this explicitly so perturbation samples
    # retain binary feature semantics (the unavoidable cross-category
    # combinations are recorded as a limitation in the canonical result).
    categorical_features = [
        index for index, name in enumerate(names) if "=" in name
    ]
    categorical_names = {
        index: ["0", "1"] for index in categorical_features
    }
    explainer = module.LimeTabularExplainer(np.asarray(reference_features), mode="classification" if classification else "regression", feature_names=names, categorical_features=categorical_features, categorical_names=categorical_names, discretize_continuous=False, sample_around_instance=False, kernel_width=params["kernel_width"], feature_selection="auto", random_state=seed)
    if classification:
        def fn(rows):
            p = np.asarray(predict(model, rows.tolist())); return np.column_stack([1 - p, p])
        result = explainer.explain_instance(np.asarray(instance), fn, labels=(1,), num_features=params["num_features"], num_samples=2000, distance_metric="euclidean")
        contrib, output, scale = result.as_map()[1], float(fn(np.asarray([instance]))[0, 1]), "PROBABILITY"
    else:
        def fn(rows): return np.asarray(predict(model, rows.tolist()))
        result = explainer.explain_instance(np.asarray(instance), fn, num_features=params["num_features"], num_samples=2000, distance_metric="euclidean")
        contrib, output, scale = result.as_map()[1], float(fn(np.asarray([instance]))[0]), "PREDICTION"
    ref = np.asarray(reference_features)
    return {"method": "LIME_TABULAR", "method_version": "1", "provider": {"name": "lime", "version": version}, "row_ordinal": row_ordinal, "effective_seed": seed, "model_output": output, "output_scale": scale, "feature_representation": "PREPROCESSED_FEATURE_SPACE", "feature_order": names, "feature_order_hash": hashlib.sha256("\u001f".join(names).encode("utf-8")).hexdigest(), "categorical_feature_indices": categorical_features, "instance_values": [float(x) for x in instance], "feature_contributions": [{"feature_index": int(i), "feature": names[int(i)], "contribution": float(v)} for i, v in contrib], "reference": {"schema_version": "predictive-explanation-reference/1", "count": len(reference_features), "hash": hashlib.sha256(ref.tobytes()).hexdigest(), "seed": sampling_seed, "partition": "TRAIN"}, "parameters": params, "limitation": "One-hot perturbations can form invalid original-category combinations."}

def reject_lime_global() -> None:
    raise PredictiveValidationError("EXPLANATION_SCOPE_NOT_SUPPORTED", "LIME_TABULAR supports LOCAL explanations only")

def lime_local_contract(model: dict, *, row_ordinal: int, sampling_seed: int, feature_order: list[str]) -> dict:
    """Backward-compatible metadata helper; provider execution uses explain_lime_local."""
    seed = (sampling_seed * 1_000_003 + row_ordinal) % (2**32)
    return {"method": "LIME_TABULAR", "scope": "LOCAL", "row_ordinal": row_ordinal, "effective_seed": seed, "representation": "PREPROCESSED_FEATURE_SPACE", "parameters": {"num_samples": 2000, "num_features": min(10, len(feature_order))}, "feature_order": feature_order}
