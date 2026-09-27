import pytest
from ariadne.capabilities.predictive.lime_backend import lime_local_contract, reject_lime_global
from ariadne.product.domain.errors import PredictiveValidationError


def test_lime_local_contract_and_global_rejection() -> None:
    result = lime_local_contract({"model_id": "linear_regression.v1"}, row_ordinal=9, sampling_seed=17, feature_order=["x", "segment=A"])
    assert result["parameters"]["num_samples"] == 2000 and result["effective_seed"] == 17000060
    with pytest.raises(PredictiveValidationError, match="LOCAL"):
        reject_lime_global()
