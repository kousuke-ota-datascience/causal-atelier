import json

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
    model["feature_order"] = ["x", "group=A"]
    result = explain_lime_local(model, features[:30], features[35], 35, 17)
    assert result["output_scale"] == "PROBABILITY"
    assert result["feature_contributions"] and result["reference"]["partition"] == "TRAIN"
    assert result["categorical_feature_indices"] == [1]
    assert result["feature_representation"] == "PREPROCESSED_FEATURE_SPACE"


def test_lime_executes_lightgbm_regression_provider() -> None:
    features = [[float(index), float(index % 2)] for index in range(60)]
    target = [2.0 * row[0] - row[1] for row in features]
    model_id, parameters = resolve_model_spec(
        "REGRESSION",
        {"model_id": "lightgbm_regressor.v1", "parameters": {
            "num_boost_round": 8, "min_data_in_leaf": 4,
        }},
    )
    model = fit_model("REGRESSION", model_id, parameters, features, target, seed=3)
    model["feature_order"] = ["x", "group=A"]
    result = explain_lime_local(model, features[:50], features[55], 55, 17)
    assert result["output_scale"] == "PREDICTION"
    assert result["feature_contributions"]


def test_lime_runner_uses_train_reference_and_test_rows(predictive_spec_factory) -> None:
    specification = _spec(predictive_spec_factory, "LIME_TABULAR")
    outcome = _execute(specification)
    explanation = next(item for item in outcome.results if item.result_type == "PREDICTIVE_EXPLANATION_RESULT")
    model_card = next(item for item in outcome.results if item.result_type == "MODEL_CARD_RESULT")
    assert explanation.analytical_status == "GENERATED"
    local = explanation.payload["local_explanation"]
    assert local and local[0]["reference"]["partition"] == "TRAIN"
    provenance = explanation.payload["method_provenance"]
    assert provenance["method_id"] == "LIME_TABULAR"
    assert provenance["method_version"] == "1"
    assert provenance["model_identity"]["model_id"] == "logistic_regression.v1"
    assert provenance["train_reference"]["partition"] == "TRAIN"
    assert provenance["train_reference"]["count"] <= 500
    assert provenance["sampling"] == specification["explanation_spec"]["sampling"]
    assert provenance["provider"]["name"] == "lime"
    assert provenance["output_scale"] == "PROBABILITY"
    assert provenance["test_instances"][0]["row_ordinal"] == local[0]["row_ordinal"]
    assert "features" not in provenance["train_reference"]
    assert model_card.payload["explanation_provenance"] == provenance
    explanation_artifact = next(
        item for item in outcome.artifacts if item.artifact_type == "PREDICTIVE_EXPLANATION"
    )
    model_card_artifact = next(
        item for item in outcome.artifacts if item.artifact_type == "MODEL_CARD"
    )
    assert json.loads(explanation_artifact.content)["method_provenance"] == provenance
    assert json.loads(model_card_artifact.content)["explanation_provenance"] == provenance


def test_lime_train_reference_sampling_is_seeded_without_replacement(
    predictive_spec_factory,
) -> None:
    import pandas as pd

    frame = pd.DataFrame({
        "score": list(range(-600, 600)),
        "converted": [int(score >= 0) for score in range(-600, 600)],
    })
    first = _execute(_spec(predictive_spec_factory, "LIME_TABULAR"), frame)
    second = _execute(_spec(predictive_spec_factory, "LIME_TABULAR"), frame)
    changed_seed = _spec(predictive_spec_factory, "LIME_TABULAR")
    changed_seed["explanation_spec"]["sampling"]["seed"] = 19
    third = _execute(changed_seed, frame)
    first_explanation = next(item for item in first.results if item.result_type == "PREDICTIVE_EXPLANATION_RESULT")
    second_explanation = next(item for item in second.results if item.result_type == "PREDICTIVE_EXPLANATION_RESULT")
    third_explanation = next(item for item in third.results if item.result_type == "PREDICTIVE_EXPLANATION_RESULT")
    first_reference = first_explanation.payload["method_provenance"]["train_reference"]
    second_reference = second_explanation.payload["method_provenance"]["train_reference"]
    third_reference = third_explanation.payload["method_provenance"]["train_reference"]
    assert first_reference == second_reference
    assert first_reference["count"] <= 500
    assert first_reference["hash"] != third_reference["hash"]
    assert third_reference["seed"] == 19
