"""Library-neutral predictive metric calculation."""

from __future__ import annotations

import math
from collections.abc import Sequence

from ariadne.product.domain.errors import PredictiveValidationError


def regression_metrics(actual: Sequence[float], predicted: Sequence[float]) -> dict[str, float | int]:
    _same_nonempty(actual, predicted)
    errors = [float(p) - float(y) for y, p in zip(actual, predicted, strict=True)]
    mae = sum(abs(error) for error in errors) / len(errors)
    mse = sum(error * error for error in errors) / len(errors)
    mean = sum(float(value) for value in actual) / len(actual)
    total = sum((float(value) - mean) ** 2 for value in actual)
    residual = sum(error * error for error in errors)
    return {"sample_count": len(actual), "mae": mae, "rmse": math.sqrt(mse), "r2": 1 - residual / total if total else 0.0}


def classification_metrics(
    actual: Sequence[int], probability: Sequence[float], *, threshold: float = 0.5
) -> dict[str, float | int | dict[str, int]]:
    _same_nonempty(actual, probability)
    if set(actual) - {0, 1}:
        raise PredictiveValidationError("BINARY_TARGET_REQUIRED", "Classification target must be 0/1")
    epsilon = 1e-15
    clipped = [min(1 - epsilon, max(epsilon, float(value))) for value in probability]
    labels = [int(value >= threshold) for value in clipped]
    tp = sum(y == 1 and p == 1 for y, p in zip(actual, labels, strict=True))
    tn = sum(y == 0 and p == 0 for y, p in zip(actual, labels, strict=True))
    fp = sum(y == 0 and p == 1 for y, p in zip(actual, labels, strict=True))
    fn = sum(y == 1 and p == 0 for y, p in zip(actual, labels, strict=True))
    log_loss = -sum(y * math.log(p) + (1 - y) * math.log(1 - p) for y, p in zip(actual, clipped, strict=True)) / len(actual)
    brier = sum((p - y) ** 2 for y, p in zip(actual, clipped, strict=True)) / len(actual)
    auc = _roc_auc(actual, clipped)
    return {
        "sample_count": len(actual), "positive_count": sum(actual), "threshold": threshold,
        "roc_auc": auc, "log_loss": log_loss, "brier": brier,
        "confusion_matrix": {"tp": tp, "tn": tn, "fp": fp, "fn": fn},
    }


def _roc_auc(actual: Sequence[int], scores: Sequence[float]) -> float:
    positives = [score for y, score in zip(actual, scores, strict=True) if y == 1]
    negatives = [score for y, score in zip(actual, scores, strict=True) if y == 0]
    if not positives or not negatives:
        raise PredictiveValidationError("INSUFFICIENT_TEST_CLASS", "ROC-AUC requires both classes")
    wins = sum((positive > negative) + 0.5 * (positive == negative) for positive in positives for negative in negatives)
    return wins / (len(positives) * len(negatives))


def _same_nonempty(first: Sequence[object], second: Sequence[object]) -> None:
    if not first or len(first) != len(second):
        raise PredictiveValidationError("INVALID_METRIC_INPUT", "Metric arrays must be non-empty and equally sized")
