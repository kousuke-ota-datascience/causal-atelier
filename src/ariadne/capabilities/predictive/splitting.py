"""Deterministic row/group/time partition construction."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence
from datetime import date, datetime, timezone
from random import Random
from typing import Any

from ariadne.capabilities.predictive.validation import validate_partition_isolation
from ariadne.product.domain.errors import PredictiveValidationError


def build_partitions(
    row_ids: Sequence[Any],
    *,
    strategy: str,
    train_ratio: float,
    validation_ratio: float,
    seed: int,
    targets: Sequence[Any] | None = None,
    groups: Sequence[Any] | None = None,
    times: Sequence[Any] | None = None,
    train_cutoff: Any | None = None,
    validation_cutoff: Any | None = None,
) -> dict[str, list[Any]]:
    if not row_ids:
        raise PredictiveValidationError("EMPTY_POPULATION", "Cannot split an empty population")
    if strategy == "GROUP":
        if groups is None or len(groups) != len(row_ids):
            raise PredictiveValidationError("GROUP_COLUMN_REQUIRED", "GROUP split requires one group per row")
        buckets: dict[Any, list[Any]] = defaultdict(list)
        for row_id, group in zip(row_ids, groups, strict=True):
            buckets[group].append(row_id)
        group_ids = sorted(buckets, key=str)
        Random(seed).shuffle(group_ids)
        split_groups = _slice(group_ids, train_ratio, validation_ratio)
        result = {part: [row for group in values for row in buckets[group]] for part, values in split_groups.items()}
        validate_partition_isolation(
            result["TRAIN"], result["VALIDATION"], result["TEST"],
            train_groups=split_groups["TRAIN"], validation_groups=split_groups["VALIDATION"],
            test_groups=split_groups["TEST"],
            population=row_ids,
        )
        return result
    if strategy == "TIME_BASED":
        if times is None or len(times) != len(row_ids):
            raise PredictiveValidationError("TIME_COLUMN_REQUIRED", "TIME_BASED split requires one time per row")
        if train_cutoff is None or validation_cutoff is None:
            raise PredictiveValidationError(
                "TIME_CUTOFF_REQUIRED", "TIME_BASED split requires train and validation cutoffs"
            )
        lower, upper = comparable_time(train_cutoff), comparable_time(validation_cutoff)
        if lower >= upper:
            raise PredictiveValidationError(
                "TEMPORAL_LEAKAGE_RISK", "train_cutoff must precede validation_cutoff"
            )
        timed_rows = [(comparable_time(value), index, row) for index, (row, value) in enumerate(
            zip(row_ids, times, strict=True)
        )]
        if any(value[0] != lower[0] for value, _, _ in timed_rows):
            raise PredictiveValidationError(
                "TEMPORAL_TYPE_MISMATCH", "Time column and cutoffs must use the same temporal type"
            )
        result = {
            "TRAIN": [row for value, _, row in timed_rows if value <= lower],
            "VALIDATION": [row for value, _, row in timed_rows if lower < value <= upper],
            "TEST": [row for value, _, row in timed_rows if value > upper],
        }
        if any(not result[partition] for partition in result):
            raise PredictiveValidationError(
                "INSUFFICIENT_SPLIT_SAMPLE", "Temporal cutoffs must produce three non-empty partitions"
            )
    elif strategy == "STRATIFIED":
        if targets is None or len(targets) != len(row_ids):
            raise PredictiveValidationError("STRATIFY_TARGET_REQUIRED", "STRATIFIED split requires targets")
        by_class: dict[Any, list[Any]] = defaultdict(list)
        for row, target in zip(row_ids, targets, strict=True):
            by_class[target].append(row)
        if len(by_class) != 2:
            raise PredictiveValidationError("BINARY_TARGET_REQUIRED", "Binary classification requires two classes")
        result = {"TRAIN": [], "VALIDATION": [], "TEST": []}
        for target in sorted(by_class, key=str):
            values = list(by_class[target])
            Random(f"{seed}:{target}").shuffle(values)
            sliced = _slice(values, train_ratio, validation_ratio)
            for part in result:
                result[part].extend(sliced[part])
    else:
        shuffled = list(row_ids)
        Random(seed).shuffle(shuffled)
        result = _slice(shuffled, train_ratio, validation_ratio)
    validate_partition_isolation(
        result["TRAIN"], result["VALIDATION"], result["TEST"], population=row_ids
    )
    return result


def _slice(values: list[Any], train_ratio: float, validation_ratio: float) -> dict[str, list[Any]]:
    train_end = int(len(values) * train_ratio)
    validation_end = train_end + int(len(values) * validation_ratio)
    if train_end == 0 or validation_end == train_end or validation_end >= len(values):
        raise PredictiveValidationError("INSUFFICIENT_SPLIT_SAMPLE", "Every partition must contain rows")
    return {
        "TRAIN": values[:train_end],
        "VALIDATION": values[train_end:validation_end],
        "TEST": values[validation_end:],
    }


def comparable_time(value: Any) -> tuple[int, float]:
    """Normalize numeric or ISO-compatible temporal values without locale inference."""
    if isinstance(value, bool):
        raise TypeError("Boolean is not a temporal value")
    if isinstance(value, (int, float)):
        return (0, float(value))
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, date):
        parsed = datetime.combine(value, datetime.min.time())
    elif isinstance(value, str):
        text = value.strip()
        if not text:
            raise ValueError("Empty temporal value")
        try:
            parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("Temporal strings must use ISO-8601 format") from exc
    else:
        raise TypeError(f"Unsupported temporal value: {type(value).__name__}")
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return (1, parsed.astimezone(timezone.utc).timestamp())
