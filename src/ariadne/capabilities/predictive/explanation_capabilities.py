"""Provider-neutral explanation capability and provenance contracts."""

from __future__ import annotations

from importlib import metadata as importlib_metadata
from importlib import util as importlib_util
from typing import Any

from ariadne.product.domain.errors import PredictiveValidationError


EXPLANATION_METHODS = (
    {"method_id": "LINEAR_COEFFICIENT_CONTRIBUTION", "version": "1", "supported_models": ("logistic_regression.v1", "linear_regression.v1"), "supports_global": True, "supports_local": True, "dependency": None},
    {"method_id": "SHAP_TREE", "version": "1", "supported_models": ("lightgbm_classifier.v1", "lightgbm_regressor.v1"), "supports_global": True, "supports_local": True, "dependency": {"distribution": "shap", "module": "shap", "requirement": ">=0.52.0,<0.53"}},
    {"method_id": "LIME_TABULAR", "version": "1", "supported_models": ("logistic_regression.v1", "linear_regression.v1", "lightgbm_classifier.v1", "lightgbm_regressor.v1"), "supports_global": False, "supports_local": True, "dependency": {"distribution": "lime", "module": "lime", "requirement": "==0.2.0.1"}},
)


def explanation_capabilities() -> tuple[dict[str, Any], ...]:
    return tuple({**item, "availability": _availability(item["dependency"])} for item in EXPLANATION_METHODS)


def resolve_explanation_method(method_id: str, model_id: str, *, scope: str) -> dict[str, Any]:
    method = next((item for item in EXPLANATION_METHODS if item["method_id"] == method_id), None)
    if method is None:
        raise PredictiveValidationError("EXPLANATION_METHOD_NOT_REGISTERED", f"Explanation method is not registered: {method_id}")
    if model_id not in method["supported_models"]:
        raise PredictiveValidationError("EXPLANATION_METHOD_NOT_APPLICABLE", f"{method_id} is incompatible with {model_id}")
    if scope not in {"GLOBAL", "LOCAL"}:
        raise PredictiveValidationError("EXPLANATION_SCOPE_NOT_SUPPORTED", f"Unsupported explanation scope: {scope}")
    if not method[f"supports_{scope.lower()}"]:
        raise PredictiveValidationError("EXPLANATION_SCOPE_NOT_SUPPORTED", f"{method_id} does not support {scope}")
    availability = _availability(method["dependency"])
    if not availability["available"]:
        raise PredictiveValidationError("EXPLANATION_DEPENDENCY_UNAVAILABLE", availability["reason"])
    return {**method, "availability": availability}


def canonical_explanation_provenance(method: dict[str, Any], *, model: dict[str, Any], feature_order: list[str], sample_identity: dict[str, Any]) -> dict[str, Any]:
    """Canonical public provenance; provider-native objects are intentionally excluded."""
    return {"method": {"id": method["method_id"], "version": method["version"], "availability": method["availability"]}, "model": {"model_id": model["model_id"], "task_type": model["task_type"], "feature_order": feature_order, "preprocessor_hash": model["preprocessor_hash"]}, "sample_identity": sample_identity}


def _availability(dependency: dict[str, str] | None) -> dict[str, Any]:
    if dependency is None:
        return {"available": True, "version": None, "reason": None}
    if importlib_util.find_spec(dependency["module"]) is None:
        return {"available": False, "version": None, "reason": f"Optional dependency {dependency['distribution']} is not installed"}
    try:
        version = importlib_metadata.version(dependency["distribution"])
    except importlib_metadata.PackageNotFoundError:
        return {"available": False, "version": None, "reason": f"Distribution metadata for {dependency['distribution']} is unavailable"}
    return {"available": _version_ok(version, dependency["requirement"]), "version": version, "reason": None if _version_ok(version, dependency["requirement"]) else f"{dependency['distribution']} {version} does not satisfy {dependency['requirement']}"}


def _version_ok(version: str, requirement: str) -> bool:
    if requirement.startswith("=="):
        return version == requirement[2:]
    try:
        major, minor = (int(x) for x in version.split(".")[:2])
    except ValueError:
        return False
    return (major, minor) == (0, 52)
