from __future__ import annotations

import sys

import pytest

from ariadne.capabilities.predictive import modeling
from ariadne.product.domain.errors import PredictiveValidationError


def test_existing_task_defaults_and_registry_entries_are_preserved() -> None:
    assert modeling.resolve_model_spec("BINARY_CLASSIFICATION", {}) == (
        "logistic_regression.v1",
        {"iterations": 500, "learning_rate": 0.1, "l2": 0.0},
    )
    assert modeling.resolve_model_spec("REGRESSION", {}) == (
        "linear_regression.v1", {"l2": 0.0}
    )
    descriptors = {entry["model_id"]: entry for entry in modeling.model_capabilities()}
    for model_id in ("logistic_regression.v1", "linear_regression.v1"):
        descriptor = descriptors[model_id]
        assert descriptor["task_default"] is True
        assert descriptor["availability"] == {"available": True, "version": None, "reason": None}
        assert descriptor["serializer_id"] == descriptor["loader_id"]
        assert isinstance(descriptor["parameter_schema"]["l2"], dict)


def test_model_selection_error_taxonomy_and_task_compatibility() -> None:
    with pytest.raises(PredictiveValidationError, match="not registered") as missing:
        modeling.resolve_model_spec("REGRESSION", {"model_id": "unknown.v1"})
    assert missing.value.code == "MODEL_NOT_REGISTERED"

    with pytest.raises(PredictiveValidationError, match="incompatible") as incompatible:
        modeling.resolve_model_spec(
            "REGRESSION", {"model_id": "logistic_regression.v1"}
        )
    assert incompatible.value.code == "MODEL_TASK_MISMATCH"


@pytest.mark.parametrize(
    "parameters",
    [
        {"iterations": 0},
        {"learning_rate": "fast"},
        {"l2": -0.1},
        {"unexpected": 1},
    ],
)
def test_invalid_model_parameters_have_a_stable_taxonomy(parameters: dict[str, object]) -> None:
    with pytest.raises(PredictiveValidationError) as invalid:
        modeling.resolve_model_spec(
            "BINARY_CLASSIFICATION",
            {"model_id": "logistic_regression.v1", "parameters": parameters},
        )
    assert invalid.value.code == "MODEL_PARAMETER_INVALID"
    assert invalid.value.path == "model_spec.parameters"


def test_lightgbm_discovery_is_lazy_and_unavailable_models_do_not_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(modeling.importlib_util, "find_spec", lambda _module: None)
    assert "lightgbm" not in sys.modules

    descriptor = next(
        entry for entry in modeling.model_capabilities()
        if entry["model_id"] == "lightgbm_classifier.v1"
    )
    assert descriptor["dependency"] == {
        "extra": "predictive-advanced",
        "distribution": "lightgbm",
        "module": "lightgbm",
        "requirement": ">=4.7.0,<4.8",
    }
    assert descriptor["availability"]["available"] is False

    with pytest.raises(PredictiveValidationError) as unavailable:
        modeling.resolve_model_spec(
            "BINARY_CLASSIFICATION", {"model_id": "lightgbm_classifier.v1"}
        )
    assert unavailable.value.code == "MODEL_DEPENDENCY_UNAVAILABLE"
