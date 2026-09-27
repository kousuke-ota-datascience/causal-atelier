"""Canonical SHAP Tree backend for G02 P02."""
from __future__ import annotations
import importlib
from typing import Any
import numpy as np
from ariadne.product.domain.errors import PredictiveValidationError


def explain_shap_tree(model: dict[str, Any], features: list[list[float]], row_ordinals: list[int], *, local_size: int) -> dict[str, Any]:
    if model.get("model_id") not in {"lightgbm_classifier.v1", "lightgbm_regressor.v1"}:
        raise PredictiveValidationError("EXPLANATION_METHOD_NOT_APPLICABLE", "SHAP_TREE requires a LightGBM model")
    try:
        shap = importlib.import_module("shap")
        lightgbm = importlib.import_module("lightgbm")
    except ImportError as exc:
        raise PredictiveValidationError("EXPLANATION_DEPENDENCY_UNAVAILABLE", "SHAP_TREE dependency is unavailable") from exc
    matrix = np.asarray(features, dtype=float)
    explainer = shap.TreeExplainer(lightgbm.Booster(model_str=model["booster_model"]), feature_perturbation="tree_path_dependent", model_output="raw")
    values = np.asarray(explainer.shap_values(matrix))
    if values.ndim == 3:
        values = values[:, :, -1]
    if values.shape != matrix.shape:
        raise PredictiveValidationError("EXPLANATION_COMPUTATION_FAILED", "Unexpected SHAP value shape")
    expected = float(np.asarray(explainer.expected_value).reshape(-1)[-1])
    raw = matrix.shape[0] and np.asarray(explainer.model.predict(matrix, output="raw"), dtype=float)
    if not np.allclose(expected + values.sum(axis=1), raw, atol=1e-6, rtol=1e-5):
        raise PredictiveValidationError("EXPLANATION_COMPUTATION_FAILED", "SHAP additivity check failed")
    names = model["feature_order"]
    global_values = [{"feature": name, "mean_absolute_contribution": float(np.abs(values[:, i]).mean()), "signed_mean_contribution": float(values[:, i].mean())} for i, name in enumerate(names)]
    local = [{"row_ordinal": row, "base_value": expected, "model_output": float(raw[i]), "feature_contributions": [{"feature": name, "contribution": float(values[i, j])} for j, name in enumerate(names)]} for i, row in enumerate(row_ordinals[:local_size])]
    return {"method": "SHAP_TREE", "output_scale": "LOG_ODDS" if model["task_type"] == "BINARY_CLASSIFICATION" else "PREDICTION", "background": {"kind": "TREE_PATH_DEPENDENT"}, "global": global_values, "local": local}
