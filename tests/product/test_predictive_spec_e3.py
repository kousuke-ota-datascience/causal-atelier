from __future__ import annotations

import pytest

from ariadne.capabilities.predictive.validation import validate_predictive_specification
from ariadne.product.domain.errors import InvalidSchema, PredictiveValidationError


@pytest.mark.requirement("FR-055", "FR-056", "FR-057")
@pytest.mark.parametrize("task_type", ["BINARY_CLASSIFICATION", "REGRESSION"])
def test_predictive_spec_accepts_only_supported_typed_tasks(
    task_type: str, predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    assert validate_predictive_specification(predictive_spec_factory(task_type))["task_type"] == task_type

    with pytest.raises(InvalidSchema, match="BINARY_CLASSIFICATION or REGRESSION"):
        validate_predictive_specification({**predictive_spec_factory(), "task_type": "MULTICLASS"})


@pytest.mark.requirement("FR-056", "FR-057", "FR-065")
def test_predictive_spec_requires_complete_availability_and_task_metric(
    predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    spec = predictive_spec_factory()
    spec["feature_spec"]["availability_cutoff"] = {}
    with pytest.raises(InvalidSchema, match="exactly every feature"):
        validate_predictive_specification(spec)

    mismatch = predictive_spec_factory()
    mismatch["evaluation_spec"]["primary_metric"] = "RMSE"
    with pytest.raises(PredictiveValidationError, match="incompatible") as captured:
        validate_predictive_specification(mismatch)
    assert captured.value.code == "METRIC_TASK_MISMATCH"
