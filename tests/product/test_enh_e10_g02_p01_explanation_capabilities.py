from __future__ import annotations

import pytest

from ariadne.capabilities.predictive.explanation_capabilities import explanation_capabilities, resolve_explanation_method
from ariadne.product.domain.errors import PredictiveValidationError


def test_capability_matrix_preserves_coefficient_and_declares_advanced_methods() -> None:
    methods = {item["method_id"]: item for item in explanation_capabilities()}
    assert methods["LINEAR_COEFFICIENT_CONTRIBUTION"]["supports_global"] is True
    assert methods["SHAP_TREE"]["supported_models"] == ("lightgbm_classifier.v1", "lightgbm_regressor.v1")
    assert methods["LIME_TABULAR"]["supports_global"] is False


@pytest.mark.parametrize("method,model,scope,code", [("UNKNOWN", "linear_regression.v1", "LOCAL", "EXPLANATION_METHOD_NOT_REGISTERED"), ("SHAP_TREE", "linear_regression.v1", "LOCAL", "EXPLANATION_METHOD_NOT_APPLICABLE"), ("LIME_TABULAR", "linear_regression.v1", "GLOBAL", "EXPLANATION_SCOPE_NOT_SUPPORTED")])
def test_negative_capability_boundaries(method: str, model: str, scope: str, code: str) -> None:
    with pytest.raises(PredictiveValidationError) as error:
        resolve_explanation_method(method, model, scope=scope)
    assert error.value.code == code
