from __future__ import annotations

import pytest

from ariadne.capabilities.predictive.validation import validate_predictive_specification
from ariadne.product.domain.errors import InvalidSchema, PredictiveValidationError
from ariadne.product.domain.schemas import canonical_bytes, canonical_hash


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

    pr_auc = predictive_spec_factory()
    pr_auc["evaluation_spec"]["primary_metric"] = "PR_AUC"
    assert (
        validate_predictive_specification(pr_auc)["evaluation_spec"]
        == pr_auc["evaluation_spec"]
    )

    stratified = predictive_spec_factory()
    stratified["split_spec"].update({"strategy": "STRATIFIED", "stratify": True})
    assert validate_predictive_specification(stratified)["split_spec"]["stratify"] is True


@pytest.mark.requirement("FR-055", "FR-056", "FR-057")
def test_predictive_spec_rejects_unknown_missing_duplicate_and_ambiguous_stratify_fields(
    predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    unknown = predictive_spec_factory()
    unknown["prediction_question"]["unknown"] = "not canonical"
    with pytest.raises(InvalidSchema, match="Unknown prediction_question fields"):
        validate_predictive_specification(unknown)

    missing = predictive_spec_factory()
    del missing["prediction_question"]["intended_use"]
    with pytest.raises(InvalidSchema, match="fields are required"):
        validate_predictive_specification(missing)

    duplicate = predictive_spec_factory()
    duplicate["feature_spec"]["feature_columns"] = ["score", "score"]
    with pytest.raises(InvalidSchema, match="unique string array"):
        validate_predictive_specification(duplicate)

    ambiguous = predictive_spec_factory()
    ambiguous["split_spec"]["stratify"] = True
    with pytest.raises(PredictiveValidationError) as captured:
        validate_predictive_specification(ambiguous)
    assert captured.value.code == "STRATIFY_CONTRACT_MISMATCH"
    assert captured.value.path == "split_spec.stratify"


@pytest.mark.requirement("NFR-003")
def test_predictive_spec_canonical_identity_is_independent_of_object_key_order(
    predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    specification = predictive_spec_factory()
    reordered = _reverse_object_key_order(specification)

    validated = validate_predictive_specification(specification)
    reordered_validated = validate_predictive_specification(reordered)

    assert reordered_validated == validated
    assert canonical_bytes(reordered_validated) == canonical_bytes(validated)
    assert canonical_hash(reordered_validated) == canonical_hash(validated)


def _reverse_object_key_order(value):  # type: ignore[no-untyped-def]
    if isinstance(value, dict):
        return {
            key: _reverse_object_key_order(value[key])
            for key in reversed(tuple(value))
        }
    if isinstance(value, list):
        return [_reverse_object_key_order(item) for item in value]
    return value
