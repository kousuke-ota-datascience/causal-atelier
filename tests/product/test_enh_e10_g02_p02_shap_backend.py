from ariadne.capabilities.predictive.modeling import fit_model, resolve_model_spec
from ariadne.capabilities.predictive.shap_backend import explain_shap_tree


def test_shap_tree_binary_global_local_contract() -> None:
    features = [[float(i), float(i % 3)] for i in range(60)]
    target = [int(i >= 30) for i in range(60)]
    model_id, parameters = resolve_model_spec("BINARY_CLASSIFICATION", {"model_id": "lightgbm_classifier.v1", "parameters": {"num_boost_round": 8, "min_data_in_leaf": 4}})
    model = fit_model("BINARY_CLASSIFICATION", model_id, parameters, features, target, seed=3)
    model["feature_order"] = ["x", "group"]
    result = explain_shap_tree(model, features, list(range(60)), local_size=2)
    assert result["output_scale"] == "LOG_ODDS"
    assert len(result["global"]) == 2 and len(result["local"]) == 2
