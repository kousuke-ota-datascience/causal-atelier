"""Library-neutral deterministic predictive metric calculation."""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Any

from ariadne.product.domain.errors import PredictiveValidationError


def regression_metrics(
    actual: Sequence[float], predicted: Sequence[float]
) -> dict[str, Any]:
    _same_nonempty(actual, predicted)
    observed = [_finite(value) for value in actual]
    fitted = [_finite(value) for value in predicted]
    errors = [prediction - value for value, prediction in zip(observed, fitted, strict=True)]
    mae = sum(abs(error) for error in errors) / len(errors)
    mse = sum(error * error for error in errors) / len(errors)
    mean = sum(observed) / len(observed)
    total = sum((value - mean) ** 2 for value in observed)
    ordered = sorted(errors)
    midpoint = len(ordered) // 2
    median = (
        ordered[midpoint]
        if len(ordered) % 2
        else (ordered[midpoint - 1] + ordered[midpoint]) / 2
    )
    return {
        "sample_count": len(observed),
        "mae": mae,
        "rmse": math.sqrt(mse),
        "r2": 1 - sum(error * error for error in errors) / total if total else 0.0,
        "residual_summary": {
            "mean": sum(errors) / len(errors),
            "min": ordered[0],
            "median": median,
            "max": ordered[-1],
        },
    }


def classification_metrics(
    actual: Sequence[int], probability: Sequence[float], *, threshold: float = 0.5
) -> dict[str, Any]:
    _same_nonempty(actual, probability)
    labels_actual = [int(value) for value in actual]
    if set(labels_actual) - {0, 1}:
        raise PredictiveValidationError(
            "BINARY_TARGET_REQUIRED",
            "Classification target must be encoded as 0/1",
            path="prediction_question.target",
        )
    epsilon = 1e-15
    clipped = [min(1 - epsilon, max(epsilon, _finite(value))) for value in probability]
    labels = [int(value >= threshold) for value in clipped]
    tp = sum(y == 1 and p == 1 for y, p in zip(labels_actual, labels, strict=True))
    tn = sum(y == 0 and p == 0 for y, p in zip(labels_actual, labels, strict=True))
    fp = sum(y == 0 and p == 1 for y, p in zip(labels_actual, labels, strict=True))
    fn = sum(y == 1 and p == 0 for y, p in zip(labels_actual, labels, strict=True))
    log_loss = -sum(
        y * math.log(p) + (1 - y) * math.log(1 - p)
        for y, p in zip(labels_actual, clipped, strict=True)
    ) / len(labels_actual)
    brier = sum(
        (p - y) ** 2 for y, p in zip(labels_actual, clipped, strict=True)
    ) / len(labels_actual)
    accuracy = (tp + tn) / len(labels_actual)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    has_both_classes = set(labels_actual) == {0, 1}
    return {
        "sample_count": len(labels_actual),
        "positive_count": sum(labels_actual),
        "negative_count": len(labels_actual) - sum(labels_actual),
        "class_balance": sum(labels_actual) / len(labels_actual),
        "threshold": threshold,
        "roc_auc": _roc_auc(labels_actual, clipped) if has_both_classes else None,
        "pr_auc": _average_precision(labels_actual, clipped) if has_both_classes else None,
        "log_loss": log_loss,
        "brier": brier,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "confusion_matrix": {"tp": tp, "tn": tn, "fp": fp, "fn": fn},
        "calibration": _calibration(labels_actual, clipped),
    }


def metric_value(metrics: dict[str, Any], metric_name: str) -> float | None:
    key = {
        "ROC_AUC": "roc_auc",
        "PR_AUC": "pr_auc",
        "LOG_LOSS": "log_loss",
        "BRIER": "brier",
        "ACCURACY": "accuracy",
        "F1": "f1",
        "MAE": "mae",
        "RMSE": "rmse",
        "R2": "r2",
    }.get(metric_name)
    if key is None:
        raise PredictiveValidationError(
            "UNSUPPORTED_METRIC", f"Unsupported metric: {metric_name}", path="evaluation_spec"
        )
    value = metrics.get(key)
    return float(value) if isinstance(value, (int, float)) else None


def _roc_auc(actual: Sequence[int], scores: Sequence[float]) -> float:
    positives = [score for y, score in zip(actual, scores, strict=True) if y == 1]
    negatives = [score for y, score in zip(actual, scores, strict=True) if y == 0]
    if not positives or not negatives:
        raise PredictiveValidationError(
            "INSUFFICIENT_TEST_CLASS",
            "ROC-AUC requires both classes",
            path="prediction_question.target",
        )
    wins = sum(
        (positive > negative) + 0.5 * (positive == negative)
        for positive in positives
        for negative in negatives
    )
    return wins / (len(positives) * len(negatives))


def _average_precision(actual: Sequence[int], scores: Sequence[float]) -> float:
    ranked = sorted(zip(scores, actual, strict=True), key=lambda item: item[0], reverse=True)
    positive_count = sum(actual)
    found = 0
    total = 0.0
    for rank, (_, label) in enumerate(ranked, start=1):
        if label == 1:
            found += 1
            total += found / rank
    return total / positive_count


def _calibration(actual: Sequence[int], scores: Sequence[float]) -> list[dict[str, Any]]:
    bins: list[dict[str, Any]] = []
    for index in range(10):
        lower, upper = index / 10, (index + 1) / 10
        values = [
            (y, score)
            for y, score in zip(actual, scores, strict=True)
            if lower <= score < upper or (index == 9 and score == 1)
        ]
        if values:
            bins.append({
                "lower": lower,
                "upper": upper,
                "count": len(values),
                "mean_probability": sum(score for _, score in values) / len(values),
                "observed_rate": sum(y for y, _ in values) / len(values),
            })
    return bins


def _same_nonempty(first: Sequence[object], second: Sequence[object]) -> None:
    if not first or len(first) != len(second):
        raise PredictiveValidationError(
            "INVALID_METRIC_INPUT",
            "Metric arrays must be non-empty and equally sized",
            path="evaluation_population",
        )


def _finite(value: Any) -> float:
    converted = float(value)
    if not math.isfinite(converted):
        raise PredictiveValidationError(
            "INVALID_METRIC_INPUT",
            "Metric inputs must be finite",
            path="evaluation_population",
        )
    return converted
