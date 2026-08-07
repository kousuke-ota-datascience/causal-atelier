from __future__ import annotations

import pytest

from ariadne.capabilities.predictive.validation import (
    LeakageValidator,
    validate_partition_isolation,
    validate_predictive_specification,
)
from ariadne.product.domain.errors import PredictiveValidationError


@pytest.mark.requirement("FR-059")
def test_target_and_future_feature_leakage_are_rejected(
    predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    target = predictive_spec_factory()
    target["feature_spec"]["feature_columns"] = ["converted"]
    target["feature_spec"]["availability_cutoff"] = {
        "converted": {
            "column": "converted", "available_at": "PREDICTION_TIME", "allowed": True,
        },
    }
    with pytest.raises(PredictiveValidationError) as target_error:
        validate_predictive_specification(target)
    assert target_error.value.code == "TARGET_LEAKAGE_DETECTED"

    future = predictive_spec_factory()
    future["feature_spec"]["availability_cutoff"]["score"] = {
        "column": "score", "available_at": "OUTCOME_WINDOW_END", "allowed": False,
    }
    with pytest.raises(PredictiveValidationError) as future_error:
        validate_predictive_specification(future)
    assert future_error.value.code == "FUTURE_LEAKAGE_DETECTED"

    timestamp_future = predictive_spec_factory()
    timestamp_future["feature_spec"]["availability_cutoff"]["score"] = {
        "column": "score", "available_at": "2026-01-02T00:00:00Z", "allowed": True,
    }
    with pytest.raises(PredictiveValidationError) as timestamp_error:
        validate_predictive_specification(timestamp_future)
    assert timestamp_error.value.code == "FUTURE_LEAKAGE_DETECTED"

    derivative = predictive_spec_factory()
    derivative["feature_spec"]["availability_cutoff"]["score"]["derived_from"] = [
        "converted"
    ]
    with pytest.raises(PredictiveValidationError) as derivative_error:
        validate_predictive_specification(derivative)
    assert derivative_error.value.code == "TARGET_DERIVATIVE_LEAKAGE_DETECTED"
    assert derivative_error.value.path.endswith("score.derived_from")


@pytest.mark.requirement("FR-059", "AR-014")
def test_group_key_feature_and_partition_overlap_are_rejected() -> None:
    validator = LeakageValidator()
    with pytest.raises(PredictiveValidationError) as group_error:
        validator.validate(
            {"target": "y"},
            {
                "feature_columns": ["entity_id"],
                "availability_cutoff": {"entity_id": {
                    "column": "entity_id", "available_at": "PREDICTION_TIME", "allowed": True,
                }},
            },
            {"strategy": "GROUP", "group_column": "entity_id"},
        )
    assert group_error.value.code == "GROUP_KEY_LEAKAGE_DETECTED"

    with pytest.raises(PredictiveValidationError) as overlap_error:
        validate_partition_isolation([1, 2], [2, 3], [4], population=[1, 2, 3, 4])
    assert overlap_error.value.code == "SPLIT_OVERLAP"
    with pytest.raises(PredictiveValidationError) as population_error:
        validate_partition_isolation([1], [2], [3], population=[1, 2, 3, 4])
    assert population_error.value.code == "SPLIT_POPULATION_MISMATCH"

    with pytest.raises(PredictiveValidationError) as group_partition_error:
        validate_partition_isolation(
            [1],
            [2],
            [3],
            train_groups=["entity-1"],
            validation_groups=["entity-1"],
            test_groups=["entity-2"],
            population=[1, 2, 3],
        )
    assert group_partition_error.value.code == "GROUP_LEAKAGE_DETECTED"
    assert group_partition_error.value.path == "partitions"


@pytest.mark.requirement("FR-059", "AR-014")
def test_group_column_requires_group_strategy(predictive_spec_factory) -> None:  # type: ignore[no-untyped-def]
    spec = predictive_spec_factory()
    spec["split_spec"]["group_column"] = "entity_id"
    with pytest.raises(PredictiveValidationError) as captured:
        validate_predictive_specification(spec)
    assert captured.value.code == "GROUP_LEAKAGE_RISK"
    assert captured.value.path == "split_spec.group_column"
