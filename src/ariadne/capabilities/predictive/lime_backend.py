"""LIME local-only canonical adapter."""
from __future__ import annotations
import math
from ariadne.product.domain.errors import PredictiveValidationError


def lime_local_contract(model: dict, *, row_ordinal: int, sampling_seed: int, feature_order: list[str]) -> dict:
    if model.get("model_id") not in {"logistic_regression.v1", "linear_regression.v1", "lightgbm_classifier.v1", "lightgbm_regressor.v1"}:
        raise PredictiveValidationError("EXPLANATION_METHOD_NOT_APPLICABLE", "LIME_TABULAR model is unsupported")
    seed = (sampling_seed * 1_000_003 + row_ordinal) % (2**32)
    return {"method": "LIME_TABULAR", "scope": "LOCAL", "row_ordinal": row_ordinal, "effective_seed": seed, "representation": "PREPROCESSED_FEATURE_SPACE", "parameters": {"num_samples": 2000, "num_features": min(10, len(feature_order)), "feature_selection": "auto", "discretize_continuous": False, "distance_metric": "euclidean", "kernel_width": 0.75 * math.sqrt(len(feature_order)), "sample_around_instance": False}, "feature_order": feature_order, "limitation": "One-hot perturbations can form invalid original-category combinations."}


def reject_lime_global() -> None:
    raise PredictiveValidationError("EXPLANATION_SCOPE_NOT_SUPPORTED", "LIME_TABULAR supports LOCAL explanations only")
