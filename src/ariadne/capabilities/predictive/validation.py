"""Backend-enforced predictive schema, leakage, and split validation."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import math
from typing import Any

from ariadne.product.domain.errors import InvalidSchema, PredictiveValidationError
from ariadne.product.domain.schemas import canonical_bytes, reject_unknown

PREDICTIVE_SCHEMA_VERSION = "predictive-analysis-spec/1"
TASK_TYPES = frozenset({"BINARY_CLASSIFICATION", "REGRESSION"})
SPLIT_STRATEGIES = frozenset({"RANDOM", "STRATIFIED", "GROUP", "TIME_BASED"})

_TOP_LEVEL = {
    "schema_version", "task_type", "prediction_question", "feature_spec", "split_spec",
    "preprocessing_spec", "model_spec", "tuning_spec", "evaluation_spec", "explanation_spec",
}
_QUESTION = {
    "prediction_unit", "target", "prediction_time", "horizon", "intended_use",
    "deployment_population",
}
_FEATURE = {"feature_columns", "availability_cutoff", "excluded_columns"}
_SPLIT = {
    "strategy", "train_ratio", "validation_ratio", "test_ratio", "group_column",
    "time_column", "train_cutoff", "validation_cutoff", "stratify", "seed",
}
_AVAILABILITY = {"column", "available_at", "allowed", "derived_from"}
_AVAILABILITY_REQUIRED = {"column", "available_at", "allowed"}
_CLASSIFICATION_METRICS = {"ROC_AUC", "PR_AUC", "LOG_LOSS", "BRIER", "ACCURACY", "F1"}
_REGRESSION_METRICS = {"MAE", "RMSE", "R2"}


def _object(payload: Mapping[str, Any], name: str) -> dict[str, Any]:
    value = payload.get(name)
    if not isinstance(value, Mapping):
        raise InvalidSchema(f"{name} must be an object")
    return dict(value)


def _required_strings(payload: Mapping[str, Any], fields: set[str], name: str) -> None:
    missing = fields - set(payload)
    if missing:
        raise InvalidSchema(f"{name} fields are required: {sorted(missing)}")
    if any(not isinstance(payload[field], str) or not payload[field].strip() for field in fields):
        raise InvalidSchema(f"{name} fields must be non-empty strings")


def validate_predictive_specification(payload: Mapping[str, Any]) -> dict[str, Any]:
    reject_unknown(payload, _TOP_LEVEL, name="predictive specification")
    missing = _TOP_LEVEL - set(payload)
    if missing:
        raise InvalidSchema(f"Predictive specification fields are required: {sorted(missing)}")
    if payload.get("schema_version") != PREDICTIVE_SCHEMA_VERSION:
        raise InvalidSchema(f"schema_version must be {PREDICTIVE_SCHEMA_VERSION}")
    task_type = payload.get("task_type")
    if task_type not in TASK_TYPES:
        raise InvalidSchema("task_type must be BINARY_CLASSIFICATION or REGRESSION")

    question = _object(payload, "prediction_question")
    reject_unknown(question, _QUESTION, name="prediction_question")
    _required_strings(question, _QUESTION, "prediction_question")

    feature = _object(payload, "feature_spec")
    reject_unknown(feature, _FEATURE, name="feature_spec")
    columns = feature.get("feature_columns")
    if not isinstance(columns, list) or not columns or any(
        not isinstance(column, str) or not column for column in columns
    ) or len(columns) != len(set(columns)):
        raise InvalidSchema("feature_columns must be a non-empty unique string array")
    if question["target"] in columns:
        raise PredictiveValidationError(
            "TARGET_LEAKAGE_DETECTED", "The target cannot be used as a feature",
            path="feature_spec.feature_columns",
        )
    excluded = feature.get("excluded_columns")
    if not isinstance(excluded, list) or any(not isinstance(column, str) or not column for column in excluded):
        raise InvalidSchema("excluded_columns must be a non-empty-string array")
    if len(excluded) != len(set(excluded)) or set(columns) & set(excluded):
        raise InvalidSchema("excluded_columns must be unique and disjoint from feature_columns")
    availability = feature.get("availability_cutoff")
    if not isinstance(availability, Mapping):
        raise InvalidSchema("availability_cutoff must map every feature to an availability value")
    if set(availability) != set(columns):
        raise InvalidSchema("availability_cutoff must contain exactly every feature column")
    for column, descriptor in availability.items():
        if not isinstance(descriptor, Mapping):
            raise InvalidSchema(f"Feature availability for {column!r} must be an object")
        reject_unknown(descriptor, _AVAILABILITY, name=f"availability_cutoff.{column}")
        if not _AVAILABILITY_REQUIRED.issubset(descriptor) or descriptor["column"] != column:
            raise InvalidSchema(f"Feature availability for {column!r} has an invalid shape")
        if not isinstance(descriptor["available_at"], str) or not descriptor["available_at"]:
            raise InvalidSchema(f"Feature availability for {column!r} requires available_at")
        if not isinstance(descriptor["allowed"], bool):
            raise InvalidSchema(f"Feature availability for {column!r} requires boolean allowed")
        derived_from = descriptor.get("derived_from", [])
        if (
            not isinstance(derived_from, list)
            or any(not isinstance(source, str) or not source for source in derived_from)
            or len(derived_from) != len(set(derived_from))
        ):
            raise InvalidSchema(
                f"Feature availability for {column!r} requires a unique string derived_from array"
            )

    split = _object(payload, "split_spec")
    reject_unknown(split, _SPLIT, name="split_spec")
    strategy = split.get("strategy")
    if strategy not in SPLIT_STRATEGIES:
        raise InvalidSchema("split strategy is invalid")
    if strategy == "STRATIFIED" and task_type != "BINARY_CLASSIFICATION":
        raise PredictiveValidationError(
            "SPLIT_TASK_MISMATCH", "Stratified split is only valid for classification",
            path="split_spec.strategy",
        )
    ratios = [split.get(name) for name in ("train_ratio", "validation_ratio", "test_ratio")]
    if strategy != "TIME_BASED":
        if any(
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(float(value))
            or value <= 0
            for value in ratios
        ):
            raise InvalidSchema("train, validation, and test ratios must be positive numbers")
        if abs(sum(float(value) for value in ratios) - 1.0) > 1e-9:
            raise InvalidSchema("split ratios must sum to 1")
    if strategy == "GROUP" and not split.get("group_column"):
        raise InvalidSchema("GROUP split requires group_column")
    if strategy == "TIME_BASED" and (
        not split.get("time_column") or split.get("train_cutoff") is None
        or split.get("validation_cutoff") is None
    ):
        raise InvalidSchema("TIME_BASED split requires time_column and cutoffs")
    if strategy == "TIME_BASED" and not _ordered_cutoffs(
        split["train_cutoff"], split["validation_cutoff"]
    ):
        raise PredictiveValidationError(
            "TEMPORAL_LEAKAGE_RISK", "train_cutoff must precede validation_cutoff",
            path="split_spec.validation_cutoff",
        )
    if isinstance(split.get("seed"), bool) or not isinstance(split.get("seed"), int):
        raise InvalidSchema("split seed must be an integer")
    if not isinstance(split.get("stratify"), bool):
        raise InvalidSchema("split stratify must be a boolean")
    if (strategy == "STRATIFIED") != split["stratify"]:
        raise PredictiveValidationError(
            "STRATIFY_CONTRACT_MISMATCH",
            "stratify must be true exactly when strategy is STRATIFIED",
            path="split_spec.stratify",
        )

    for name in ("preprocessing_spec", "model_spec", "tuning_spec", "evaluation_spec", "explanation_spec"):
        if not isinstance(payload[name], Mapping):
            raise InvalidSchema(f"{name} must be an object")
    evaluation = dict(payload["evaluation_spec"])
    reject_unknown(
        evaluation,
        {"primary_metric", "secondary_metrics", "subgroups"},
        name="evaluation_spec",
    )
    if "primary_metric" not in evaluation or "secondary_metrics" not in evaluation:
        raise InvalidSchema("evaluation_spec requires primary_metric and secondary_metrics")
    primary_metric = evaluation.get("primary_metric")
    allowed_metrics = (
        _CLASSIFICATION_METRICS if task_type == "BINARY_CLASSIFICATION" else _REGRESSION_METRICS
    )
    if primary_metric not in allowed_metrics:
        raise PredictiveValidationError(
            "METRIC_TASK_MISMATCH",
            f"Metric {primary_metric!r} is incompatible with {task_type}",
            path="evaluation_spec.primary_metric",
        )
    secondary = evaluation.get("secondary_metrics", [])
    if (
        not isinstance(secondary, list)
        or any(not isinstance(metric, str) for metric in secondary)
        or len(secondary) != len(set(secondary))
        or set(secondary) - allowed_metrics
    ):
        raise PredictiveValidationError(
            "METRIC_TASK_MISMATCH",
            "secondary_metrics must be unique and compatible with the task",
            path="evaluation_spec.secondary_metrics",
        )
    subgroups = evaluation.get("subgroups", [])
    if not isinstance(subgroups, list) or any(
        not isinstance(column, str) or not column for column in subgroups
    ):
        raise InvalidSchema("evaluation_spec.subgroups must be a string array")
    LeakageValidator().validate(question, feature, split)
    canonical_bytes(payload)
    return dict(payload)


class LeakageValidator:
    _ALLOWED_AVAILABILITY = {
        "BEFORE_PREDICTION_TIME", "AT_PREDICTION_TIME", "PREDICTION_TIME",
    }
    _FORBIDDEN_AVAILABILITY = {
        "AFTER_PREDICTION_TIME", "OUTCOME_WINDOW", "OUTCOME_WINDOW_END", "FUTURE",
    }

    def validate(
        self,
        prediction_question: Mapping[str, Any],
        feature_spec: Mapping[str, Any],
        split_spec: Mapping[str, Any],
    ) -> None:
        target = prediction_question.get("target")
        features = list(feature_spec.get("feature_columns", []))
        if target in features:
            raise PredictiveValidationError(
                "TARGET_LEAKAGE_DETECTED", "The target cannot be used as a feature",
                path="feature_spec.feature_columns",
            )
        availability = feature_spec.get("availability_cutoff", {})
        for index, column in enumerate(features):
            value = availability.get(column)
            if isinstance(value, Mapping):
                if target in value.get("derived_from", []):
                    raise PredictiveValidationError(
                        "TARGET_DERIVATIVE_LEAKAGE_DETECTED",
                        f"Feature {column!r} is derived from the prediction target",
                        path=f"feature_spec.availability_cutoff.{column}.derived_from",
                    )
                allowed = value.get("allowed")
                point = value.get("available_at")
                forbidden = allowed is False or point in self._FORBIDDEN_AVAILABILITY
                if not forbidden and point not in self._ALLOWED_AVAILABILITY:
                    from ariadne.capabilities.predictive.splitting import comparable_time

                    try:
                        available_at = comparable_time(point)
                        prediction_time = comparable_time(prediction_question.get("prediction_time"))
                    except (TypeError, ValueError) as exc:
                        raise InvalidSchema(
                            f"Feature {column!r} has an unsupported availability marker or timestamp"
                        ) from exc
                    if available_at[0] != prediction_time[0]:
                        raise InvalidSchema(
                            f"Feature {column!r} availability and prediction_time are not comparable"
                        )
                    forbidden = available_at > prediction_time
            else:
                forbidden = value in self._FORBIDDEN_AVAILABILITY
            if forbidden:
                raise PredictiveValidationError(
                    "FUTURE_LEAKAGE_DETECTED",
                    f"Feature {column!r} is unavailable at prediction time",
                    path=f"feature_spec.feature_columns[{index}]",
                )
        group_column = split_spec.get("group_column")
        if split_spec.get("strategy") != "GROUP" and group_column:
            raise PredictiveValidationError(
                "GROUP_LEAKAGE_RISK",
                "group_column requires GROUP split so entities cannot cross partitions",
                path="split_spec.group_column",
            )
        if group_column and group_column in features:
            raise PredictiveValidationError(
                "GROUP_KEY_LEAKAGE_DETECTED",
                "The entity grouping key cannot be used as a model feature",
                path="feature_spec.feature_columns",
            )


def validate_partition_isolation(
    train: Sequence[Any],
    validation: Sequence[Any],
    test: Sequence[Any],
    *,
    train_groups: Sequence[Any] | None = None,
    validation_groups: Sequence[Any] | None = None,
    test_groups: Sequence[Any] | None = None,
    population: Sequence[Any] | None = None,
) -> None:
    train_ids, validation_ids, test_ids = set(train), set(validation), set(test)
    if (
        len(train_ids) != len(train)
        or len(validation_ids) != len(validation)
        or len(test_ids) != len(test)
    ):
        raise PredictiveValidationError(
            "SPLIT_DUPLICATE_ROW",
            "A row identifier occurs more than once within a partition",
            path="partitions",
        )
    if train_ids & validation_ids or train_ids & test_ids or validation_ids & test_ids:
        raise PredictiveValidationError(
            "SPLIT_OVERLAP", "Partition row identifiers overlap", path="partitions"
        )
    if population is not None and train_ids | validation_ids | test_ids != set(population):
        raise PredictiveValidationError(
            "SPLIT_POPULATION_MISMATCH",
            "Partition union does not equal the input population",
            path="partitions",
        )
    supplied = (train_groups, validation_groups, test_groups)
    if any(item is not None for item in supplied):
        if any(item is None for item in supplied):
            raise PredictiveValidationError(
                "GROUP_PARTITION_INCOMPLETE",
                "All group partitions are required",
                path="partitions",
            )
        groups = [set(item or ()) for item in supplied]
        if groups[0] & groups[1] or groups[0] & groups[2] or groups[1] & groups[2]:
            raise PredictiveValidationError(
                "GROUP_LEAKAGE_DETECTED", "An entity crosses partitions", path="partitions"
            )


def assert_train_only_fit(fit_partition: str) -> None:
    if fit_partition != "TRAIN":
        raise PredictiveValidationError(
            "PREPROCESSING_LEAKAGE_DETECTED",
            "Preprocessing may only be fitted on TRAIN",
            path="preprocessing_spec.fit_partition",
        )


def assert_test_isolation(used_for_selection: Sequence[str]) -> None:
    if "TEST" in used_for_selection:
        raise PredictiveValidationError(
            "TEST_ISOLATION_VIOLATION",
            "TEST cannot be used for feature, model, or threshold selection",
            path="tuning_spec.selection_partitions",
        )


def _ordered_cutoffs(train_cutoff: Any, validation_cutoff: Any) -> bool:
    from ariadne.capabilities.predictive.splitting import comparable_time

    try:
        return comparable_time(train_cutoff) < comparable_time(validation_cutoff)
    except (TypeError, ValueError) as exc:
        raise InvalidSchema("Temporal cutoffs must be comparable ISO timestamps or numbers") from exc
