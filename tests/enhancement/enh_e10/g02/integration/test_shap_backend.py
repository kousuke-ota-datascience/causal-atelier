from __future__ import annotations

import json

import pandas as pd
import pytest

from ariadne.capabilities.predictive.modeling import fit_model, resolve_model_spec
from ariadne.capabilities.predictive.shap_backend import explain_shap_tree
from .predictive_execution import execute_predictive


def test_shap_tree_binary_global_local_contract() -> None:
    features = [[float(i), float(i % 3)] for i in range(60)]
    target = [int(i >= 30) for i in range(60)]
    model_id, parameters = resolve_model_spec("BINARY_CLASSIFICATION", {"model_id": "lightgbm_classifier.v1", "parameters": {"num_boost_round": 8, "min_data_in_leaf": 4}})
    model = fit_model("BINARY_CLASSIFICATION", model_id, parameters, features, target, seed=3)
    model["feature_order"] = ["x", "group"]
    result = explain_shap_tree(model, features, list(range(60)), local_size=2)
    assert result["output_scale"] == "LOG_ODDS"
    assert len(result["global"]) == 2 and len(result["local"]) == 2


def _shap_spec(predictive_spec_factory, task_type: str) -> dict:  # type: ignore[no-untyped-def,type-arg]
    specification = predictive_spec_factory(task_type)
    specification["preprocessing_spec"] = {
        "fit_partition": "TRAIN",
        "numeric_imputation": "MEAN",
        "scale_numeric": True,
        "categorical_encoding": "ONE_HOT",
    }
    specification["model_spec"] = {
        "model_id": (
            "lightgbm_classifier.v1"
            if task_type == "BINARY_CLASSIFICATION"
            else "lightgbm_regressor.v1"
        ),
        "parameters": {"num_boost_round": 8, "min_data_in_leaf": 4},
    }
    specification["tuning_spec"] = {"selection_partitions": ["TRAIN", "VALIDATION"]}
    specification["explanation_spec"] = {
        "method": "SHAP_TREE",
        "dataset": "TEST",
        "sampling": {"strategy": "FIRST_N", "size": 3, "seed": 17},
        "local_explanations": True,
    }
    return specification


@pytest.mark.parametrize(
    ("task_type", "expected_scale"),
    [("BINARY_CLASSIFICATION", "LOG_ODDS"), ("REGRESSION", "PREDICTION")],
)
def test_shap_tree_full_dag_persists_canonical_provenance(
    predictive_spec_factory, task_type: str, expected_scale: str,
) -> None:  # type: ignore[no-untyped-def]
    frame = pd.DataFrame({
        "score": list(range(-60, 60)),
        "converted": (
            [int(value >= 0) for value in range(-60, 60)]
            if task_type == "BINARY_CLASSIFICATION"
            else [float(3 * value - 2) for value in range(-60, 60)]
        ),
    })
    outcome = execute_predictive(_shap_spec(predictive_spec_factory, task_type), frame)
    assert outcome.status == "SUCCEEDED"
    assert [stage.stage_key for stage in outcome.stages] == [
        "split", "prepare", "train", "evaluate", "explain",
    ]
    assert {stage.status.value for stage in outcome.stages} == {"SUCCEEDED"}

    results = {item.result_type: item for item in outcome.results}
    explanation = results["PREDICTIVE_EXPLANATION_RESULT"]
    model_card = results["MODEL_CARD_RESULT"]
    assert explanation.analytical_status == "GENERATED"
    assert explanation.payload["model_output_scale"] == expected_scale
    assert explanation.payload["prediction_output_scale"] == (
        "PROBABILITY" if task_type == "BINARY_CLASSIFICATION" else "PREDICTION"
    )
    assert explanation.payload["global_explanation"]
    assert explanation.payload["local_explanation"]
    assert all(
        item["feature"] == "score"
        for item in explanation.payload["global_explanation"]
    )
    local = explanation.payload["local_explanation"]
    provenance = explanation.payload["method_provenance"]
    assert [item["row_ordinal"] for item in local] == [
        item["row_ordinal"] for item in provenance["test_instances"]
    ]
    for item in local:
        assert item["model_output"] == pytest.approx(
            item["base_value"] + sum(
                contribution["contribution"]
                for contribution in item["feature_contributions"]
            ),
            abs=1e-6,
            rel=1e-5,
        )
    assert provenance["method_id"] == "SHAP_TREE"
    assert provenance["method_version"] == "1"
    assert provenance["provider"]["name"] == "shap"
    assert provenance["background"]["kind"] == "TREE_PATH_DEPENDENT"
    assert provenance["global_explanation_identity"]["test_sample_count"] == 24
    assert provenance["sampling"] == {"strategy": "FIRST_N", "size": 3, "seed": 17}
    assert "train_reference" not in provenance
    assert model_card.payload["explanation_provenance"] == provenance
    artifacts = {item.artifact_type: item for item in outcome.artifacts}
    assert json.loads(artifacts["PREDICTIVE_EXPLANATION"].content)["method_provenance"] == provenance
    assert json.loads(artifacts["MODEL_CARD"].content)["explanation_provenance"] == provenance
    assert (
        "Predictive Explanation is not a Causal Explanation or Treatment Effect."
        in explanation.payload["limitations"]
    )
    train = next(stage for stage in outcome.stages if stage.stage_key == "train")
    assert "test" not in train.input_binding["training_bundle"]
