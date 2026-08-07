from __future__ import annotations

import pytest

from ariadne.capabilities.predictive import (
    assert_test_isolation,
    assert_train_only_fit,
    build_partitions,
)
from ariadne.product.domain.errors import PredictiveValidationError


@pytest.mark.requirement("FR-058", "FR-059", "NFR-003")
@pytest.mark.parametrize("strategy", ["RANDOM", "STRATIFIED"])
def test_random_and_stratified_partitions_are_deterministic_and_complete(strategy: str) -> None:
    row_ids = list(range(20))
    inputs = {
        "strategy": strategy,
        "train_ratio": 0.6,
        "validation_ratio": 0.2,
        "seed": 41,
        "targets": [index % 2 for index in row_ids] if strategy == "STRATIFIED" else None,
    }
    first = build_partitions(row_ids, **inputs)
    second = build_partitions(row_ids, **inputs)
    assert first == second
    assert set(first["TRAIN"]) | set(first["VALIDATION"]) | set(first["TEST"]) == set(row_ids)


@pytest.mark.requirement("FR-058", "FR-059", "AR-014")
def test_group_split_keeps_entities_in_exactly_one_partition() -> None:
    row_ids = list(range(18))
    groups = [f"entity-{index // 3}" for index in row_ids]
    result = build_partitions(
        row_ids,
        strategy="GROUP",
        train_ratio=0.5,
        validation_ratio=1 / 6,
        seed=9,
        groups=groups,
    )
    memberships = {
        partition: {groups[index] for index in indices}
        for partition, indices in result.items()
    }
    assert not memberships["TRAIN"] & memberships["VALIDATION"]
    assert not memberships["TRAIN"] & memberships["TEST"]
    assert not memberships["VALIDATION"] & memberships["TEST"]


@pytest.mark.requirement("FR-058", "FR-059", "AR-013")
def test_temporal_split_uses_cutoffs_and_has_strict_boundaries() -> None:
    row_ids = list(range(9))
    times = [f"2026-01-{day:02d}" for day in range(1, 10)]
    result = build_partitions(
        row_ids,
        strategy="TIME_BASED",
        train_ratio=0,
        validation_ratio=0,
        seed=1,
        times=times,
        train_cutoff="2026-01-03",
        validation_cutoff="2026-01-06",
    )
    assert result == {
        "TRAIN": [0, 1, 2], "VALIDATION": [3, 4, 5], "TEST": [6, 7, 8],
    }
    with pytest.raises(PredictiveValidationError, match="precede"):
        build_partitions(
            row_ids, strategy="TIME_BASED", train_ratio=0, validation_ratio=0,
            seed=1, times=times, train_cutoff="2026-01-06", validation_cutoff="2026-01-03",
        )


@pytest.mark.requirement("FR-060", "FR-064")
def test_fit_and_selection_contract_isolates_test() -> None:
    assert_train_only_fit("TRAIN")
    assert_test_isolation(["TRAIN", "VALIDATION"])
    with pytest.raises(PredictiveValidationError) as fit_error:
        assert_train_only_fit("VALIDATION")
    assert fit_error.value.code == "PREPROCESSING_LEAKAGE_DETECTED"
    with pytest.raises(PredictiveValidationError) as selection_error:
        assert_test_isolation(["VALIDATION", "TEST"])
    assert selection_error.value.code == "TEST_ISOLATION_VIOLATION"
