import pytest
from ariadne.capabilities.predictive.lime_backend import lime_local_contract, reject_lime_global
from ariadne.product.domain.errors import PredictiveValidationError
from ariadne.capabilities.predictive.modeling import fit_model, resolve_model_spec
from ariadne.capabilities.predictive.lime_backend import explain_lime_local
from test_predictive_explanation_e3 import _execute, _spec


def test_lime_local_contract_and_global_rejection() -> None:
    result = lime_local_contract({"model_id": "linear_regression.v1"}, row_ordinal=9, sampling_seed=17, feature_order=["x", "segment=A"])
    assert result["parameters"]["num_samples"] == 2000 and result["effective_seed"] == 17000060
    with pytest.raises(PredictiveValidationError, match="LOCAL"):
        reject_lime_global()


def test_lime_executes_provider_and_returns_signed_contributions() -> None:
    features = [[float(index), float(index % 2)] for index in range(40)]
    target = [int(index >= 20) for index in range(40)]
    model_id, parameters = resolve_model_spec("BINARY_CLASSIFICATION", {"model_id": "logistic_regression.v1"})
    model = fit_model("BINARY_CLASSIFICATION", model_id, parameters, features, target, seed=3)
    model["feature_order"] = ["x", "group"]
    result = explain_lime_local(model, features[:30], features[35], 35, 17)
    assert result["output_scale"] == "PROBABILITY"
    assert result["feature_contributions"] and result["reference"]["partition"] == "TRAIN"


def test_lime_runner_uses_train_reference_and_test_rows(predictive_spec_factory) -> None:
    outcome = _execute(_spec(predictive_spec_factory, "LIME_TABULAR"))
    explanation = next(item for item in outcome.results if item.result_type == "PREDICTIVE_EXPLANATION_RESULT")
    assert explanation.analytical_status == "GENERATED"
    local = explanation.payload["local_explanation"]
    assert local and local[0]["reference"]["partition"] == "TRAIN"
