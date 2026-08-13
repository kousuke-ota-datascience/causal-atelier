"""PREPARE, TRAIN, and EVALUATE runners for the Generic Executor."""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from typing import Any

import pandas as pd

from ariadne.capabilities.predictive.metrics import (
    classification_metrics,
    metric_value,
    regression_metrics,
)
from ariadne.capabilities.predictive.modeling import (
    encode_binary_target,
    fit_model,
    predict,
    resolve_model_spec,
)
from ariadne.capabilities.predictive.preprocessing import fit_preprocessor, transform_frame
from ariadne.capabilities.predictive.validation import (
    assert_test_isolation,
    assert_train_only_fit,
    validate_predictive_specification,
)
from ariadne.product.domain.errors import InvalidSchema, PredictiveValidationError
from ariadne.product.domain.execution_plan import StageType
from ariadne.product.domain.schemas import canonical_hash, reject_unknown
from ariadne.product.workflow.contracts import (
    ArtifactDraft,
    ResultDraft,
    StageContext,
    StageRunResult,
)
from ariadne.product.workflow.runner_registry import StageRunnerRegistry


@dataclass
class PredictivePrepareRunner:
    @property
    def stage_type(self) -> StageType:
        return StageType("predictive", "prepare", "1")

    def validate(self, context: StageContext) -> None:
        frame = context.inputs.get("frame")
        manifest = context.inputs.get("partition_manifest")
        if not isinstance(frame, pd.DataFrame) or frame.empty:
            raise PredictiveValidationError(
                "EMPTY_POPULATION", "PREPARE requires a non-empty frame", path="source_population"
            )
        if not isinstance(manifest, dict) or manifest.get("schema_version") != "partition-artifact/1":
            raise InvalidSchema("PREPARE requires partition-artifact/1")
        selection = manifest.get("selection_contract", {})
        if selection.get("TEST", {}).get("selection_allowed") is not False:
            raise PredictiveValidationError(
                "TEST_ISOLATION_VIOLATION",
                "Partition artifact must prohibit TEST selection",
                path="partition_manifest.selection_contract.TEST",
            )
        validate_predictive_specification(context.stage.parameters)

    def run(self, context: StageContext) -> StageRunResult:
        frame: pd.DataFrame = context.inputs["frame"]
        manifest: dict[str, Any] = context.inputs["partition_manifest"]
        spec = context.stage.parameters
        partitions = manifest["partitions"]
        preprocessing = dict(spec["preprocessing_spec"])
        assert_train_only_fit(preprocessing.get("fit_partition", "TRAIN"))
        tuning = _validate_tuning_spec(spec["tuning_spec"])
        assert_test_isolation(tuning["selection_partitions"])
        train_frame = frame.iloc[partitions["TRAIN"]]
        validation_frame = frame.iloc[partitions["VALIDATION"]]
        test_frame = frame.iloc[partitions["TEST"]]
        feature_columns = list(spec["feature_spec"]["feature_columns"])
        target = spec["prediction_question"]["target"]
        fitted = fit_preprocessor(train_frame, feature_columns, preprocessing)
        train_features = transform_frame(train_frame, fitted)
        validation_features = transform_frame(validation_frame, fitted)
        test_features = transform_frame(test_frame, fitted)
        training_bundle = {
            "schema_version": "predictive-training-bundle/1",
            "train": {
                "row_ordinals": partitions["TRAIN"],
                "features": train_features,
                "target": _json_values(train_frame[target].tolist()),
            },
            "validation": {
                "row_ordinals": partitions["VALIDATION"],
                "features": validation_features,
                "target": _json_values(validation_frame[target].tolist()),
            },
            "feature_order": fitted["output_features"],
            "selection_partitions": ["TRAIN", "VALIDATION"],
        }
        evaluation_bundle = {
            "schema_version": "predictive-evaluation-bundle/1",
            "test": {
                "row_ordinals": partitions["TEST"],
                "features": test_features,
                "target": _json_values(test_frame[target].tolist()),
                # These raw TEST columns are deliberately retained separately
                # from model features: subgroup evaluation must not require a
                # subgroup to be a model input.
                "subgroups": {
                    column: _json_values(test_frame[column].tolist())
                    for column in spec["evaluation_spec"].get("subgroups", [])
                },
            },
            "selection_allowed": False,
            "final_evaluation_only": True,
        }
        explanation_dataset = {
            "schema_version": "predictive-explanation-dataset/1",
            "partition": "TEST",
            "row_ordinals": partitions["TEST"],
            "features": test_features,
            "feature_order": fitted["output_features"],
            "selection_allowed": False,
            "explanation_only": True,
            "provenance": {
                "source_snapshot": manifest["source_snapshot"],
                "row_identifier": manifest["row_identifier"],
                "partition": "TEST",
                "specification_hash": manifest["specification_hash"],
            },
            "background_reference": {
                "partition": "TRAIN",
                "role": "PREPROCESSOR_FIT_REFERENCE",
                "sample_count": len(train_frame),
                "row_ordinals_hash": canonical_hash({
                    "row_ordinals": partitions["TRAIN"]
                }),
            },
        }
        explanation_specification = dict(spec["explanation_spec"])
        content = _json_bytes(fitted)
        return StageRunResult(
            output_bindings={
                "training_bundle": training_bundle,
                "evaluation_bundle": evaluation_bundle,
                "fitted_preprocessor": fitted,
                "explanation_dataset": explanation_dataset,
                "explanation_specification": explanation_specification,
                "sampling_definition": dict(
                    explanation_specification.get("sampling", {})
                ),
            },
            artifacts=(ArtifactDraft(
                artifact_type="FITTED_PREPROCESSOR",
                schema_version="fitted-preprocessor/1",
                media_type="application/json",
                content=content,
                metadata={
                    "fit_partition": "TRAIN",
                    "feature_order": fitted["output_features"],
                    "canonical_hash": fitted["canonical_hash"],
                },
            ),),
        )


@dataclass
class PredictiveTrainRunner:
    @property
    def stage_type(self) -> StageType:
        return StageType("predictive", "train", "1")

    def validate(self, context: StageContext) -> None:
        bundle = context.inputs.get("training_bundle")
        preprocessor = context.inputs.get("fitted_preprocessor")
        if not isinstance(bundle, dict) or bundle.get("schema_version") != "predictive-training-bundle/1":
            raise InvalidSchema("TRAIN requires predictive-training-bundle/1")
        if "test" in bundle or "TEST" in bundle.get("selection_partitions", []):
            raise PredictiveValidationError(
                "TEST_ISOLATION_VIOLATION",
                "TRAIN input contract must not contain TEST",
                path="training_bundle",
            )
        if not isinstance(preprocessor, dict) or preprocessor.get("fit_partition") != "TRAIN":
            raise PredictiveValidationError(
                "PREPROCESSING_LEAKAGE_DETECTED",
                "TRAIN requires a TRAIN-fitted preprocessor",
                path="fitted_preprocessor.fit_partition",
            )
        validate_predictive_specification(context.stage.parameters)

    def run(self, context: StageContext) -> StageRunResult:
        bundle: dict[str, Any] = context.inputs["training_bundle"]
        preprocessor: dict[str, Any] = context.inputs["fitted_preprocessor"]
        spec = context.stage.parameters
        task_type = spec["task_type"]
        model_id, parameters = resolve_model_spec(task_type, dict(spec["model_spec"]))
        seed = int(spec["split_spec"]["seed"])
        model = fit_model(
            task_type,
            model_id,
            parameters,
            bundle["train"]["features"],
            bundle["train"]["target"],
            seed=seed,
        )
        model["preprocessor_hash"] = preprocessor["canonical_hash"]
        model["feature_order"] = bundle["feature_order"]
        model["seed"] = seed
        validation_prediction = predict(model, bundle["validation"]["features"])
        if task_type == "BINARY_CLASSIFICATION":
            validation_actual = encode_binary_target(model, bundle["validation"]["target"])
            validation_metrics = classification_metrics(
                validation_actual, validation_prediction
            )
        else:
            validation_metrics = regression_metrics(
                bundle["validation"]["target"], validation_prediction
            )
        primary_name = spec["evaluation_spec"]["primary_metric"]
        primary_value = metric_value(validation_metrics, primary_name)
        warnings: tuple[dict[str, Any], ...] = ()
        status = "TRAINED"
        if primary_value is None:
            status = "TRAINED_WITH_WARNINGS"
            warnings = ({
                "code": "VALIDATION_METRIC_UNAVAILABLE",
                "message": f"{primary_name} is unavailable for the validation population",
            },)
        descriptor = {
            "model_id": model_id,
            "task_type": task_type,
            "parameters": parameters,
            "seed": seed,
            "feature_order": bundle["feature_order"],
            "preprocessor_hash": preprocessor["canonical_hash"],
        }
        result = ResultDraft(
            result_type="TRAINING_RESULT",
            schema_version="predictive-training-result/1",
            analytical_status=status,
            summary={
                "model": descriptor,
                "validation_primary_metric": {
                    "name": primary_name, "value": primary_value,
                },
            },
            payload={
                "model_descriptor": descriptor,
                "selected_hyperparameters": parameters,
                "training_history": {
                    "algorithm": model_id,
                    "iterations": parameters.get("iterations"),
                },
                "validation_metrics": validation_metrics,
            },
            warnings=warnings,
        )
        training_summary = {
            "schema_version": "predictive-training-summary/1",
            "analytical_status": status,
            "model_descriptor": descriptor,
            "selected_hyperparameters": parameters,
            "training_history": {
                "algorithm": model_id,
                "iterations": parameters.get("iterations"),
            },
            "validation_metrics": validation_metrics,
            "validation_primary_metric": {
                "name": primary_name,
                "value": primary_value,
            },
            "warnings": list(warnings),
        }
        return StageRunResult(
            output_bindings={
                "frozen_model": model,
                "training_summary": training_summary,
            },
            results=(result,),
            artifacts=(ArtifactDraft(
                artifact_type="FITTED_MODEL",
                schema_version="fitted-model/1",
                media_type="application/json",
                content=_json_bytes(model),
                metadata={"model_descriptor": descriptor},
            ),),
        )


@dataclass
class PredictiveEvaluateRunner:
    @property
    def stage_type(self) -> StageType:
        return StageType("predictive", "evaluate", "1")

    def validate(self, context: StageContext) -> None:
        model = context.inputs.get("frozen_model")
        bundle = context.inputs.get("evaluation_bundle")
        preprocessor = context.inputs.get("fitted_preprocessor")
        if not isinstance(model, dict) or model.get("schema_version") != "fitted-model/1":
            raise InvalidSchema("EVALUATE requires fitted-model/1")
        if not isinstance(bundle, dict) or bundle.get("schema_version") != "predictive-evaluation-bundle/1":
            raise InvalidSchema("EVALUATE requires predictive-evaluation-bundle/1")
        if bundle.get("selection_allowed") is not False or bundle.get("final_evaluation_only") is not True:
            raise PredictiveValidationError(
                "TEST_ISOLATION_VIOLATION",
                "EVALUATE requires final-evaluation-only TEST data",
                path="evaluation_bundle",
            )
        if (
            not isinstance(preprocessor, dict)
            or preprocessor.get("schema_version") != "fitted-preprocessor/1"
            or preprocessor.get("fit_partition") != "TRAIN"
        ):
            raise PredictiveValidationError(
                "PREPROCESSING_LEAKAGE_DETECTED",
                "EVALUATE requires a TRAIN-fitted preprocessor",
                path="fitted_preprocessor",
            )
        if model.get("preprocessor_hash") != preprocessor.get("canonical_hash"):
            raise PredictiveValidationError(
                "PREPROCESSOR_MODEL_MISMATCH",
                "Frozen model and preprocessor do not match",
                path="fitted_preprocessor",
            )

    def run(self, context: StageContext) -> StageRunResult:
        model: dict[str, Any] = context.inputs["frozen_model"]
        bundle: dict[str, Any] = context.inputs["evaluation_bundle"]
        spec = context.stage.parameters
        test = bundle["test"]
        prediction = predict(model, test["features"])
        warnings: tuple[dict[str, Any], ...] = ()
        if model["task_type"] == "BINARY_CLASSIFICATION":
            actual = encode_binary_target(model, test["target"])
            metrics = classification_metrics(actual, prediction)
            insufficient = set(actual) != {0, 1}
            prediction_rows = [
                {"row_ordinal": row, "actual": y, "probability": probability}
                for row, y, probability in zip(
                    test["row_ordinals"], actual, prediction, strict=True
                )
            ]
            errors = [abs(probability - y) for y, probability in zip(actual, prediction, strict=True)]
        else:
            actual = [float(value) for value in test["target"]]
            metrics = regression_metrics(actual, prediction)
            insufficient = len(actual) < 2
            prediction_rows = [
                {"row_ordinal": row, "actual": y, "prediction": fitted}
                for row, y, fitted in zip(
                    test["row_ordinals"], actual, prediction, strict=True
                )
            ]
            errors = [abs(fitted - y) for y, fitted in zip(actual, prediction, strict=True)]
        subgroup_metrics = _subgroup_metrics(
            task_type=model["task_type"],
            actual=actual,
            prediction=prediction,
            subgroups=test.get("subgroups", {}),
            metrics=[
                spec["evaluation_spec"]["primary_metric"],
                *spec["evaluation_spec"].get("secondary_metrics", []),
            ],
            split_seed=int(spec["split_spec"]["seed"]),
        )
        status = "INSUFFICIENT_TEST_SAMPLE" if insufficient else "EVALUATED"
        if insufficient:
            warnings = ({
                "code": "INSUFFICIENT_TEST_SAMPLE",
                "message": "TEST population cannot support every requested metric",
            },)
        prediction_manifest = {
            "schema_version": "prediction-artifact/1",
            "task_type": model["task_type"],
            "model_id": model["model_id"],
            "final_evaluation_only": True,
            "rows": prediction_rows,
        }
        evaluation = ResultDraft(
            result_type="EVALUATION_RESULT",
            schema_version="predictive-evaluation-result/1",
            analytical_status=status,
            summary={
                "task_type": model["task_type"],
                "sample_count": len(actual),
                "primary_metric": spec["evaluation_spec"]["primary_metric"],
                "primary_metric_value": metric_value(
                    metrics, spec["evaluation_spec"]["primary_metric"]
                ),
            },
            payload={
                "metrics": metrics,
                "evaluation_population": "TEST",
                "sample_count": len(actual),
                "model_descriptor": {
                    "model_id": model["model_id"],
                    "task_type": model["task_type"],
                    "parameters": model["parameters"],
                    "seed": model["seed"],
                },
                "subgroup_metrics": subgroup_metrics,
            },
            diagnostics={
                "selection_allowed": False,
                "final_evaluation_only": True,
            },
            warnings=warnings,
        )
        worst = sorted(
            zip(test["row_ordinals"], errors, strict=True),
            key=lambda item: item[1],
            reverse=True,
        )[:20]
        error_analysis = ResultDraft(
            result_type="ERROR_ANALYSIS_RESULT",
            schema_version="predictive-error-analysis-result/1",
            analytical_status="GENERATED_WITH_WARNINGS" if insufficient else "GENERATED",
            summary={"sample_count": len(actual), "reported_rows": len(worst)},
            payload={
                "largest_absolute_errors": [
                    {"row_ordinal": row, "absolute_error": error}
                    for row, error in worst
                ]
            },
            warnings=warnings,
        )
        return StageRunResult(
            output_bindings={
                "evaluation_summary": {
                    "schema_version": "predictive-evaluation-summary/1",
                    "analytical_status": status,
                    "metrics": metrics,
                    "sample_count": len(actual),
                    "evaluation_population": "TEST",
                    "primary_metric": spec["evaluation_spec"]["primary_metric"],
                    "subgroup_metrics": subgroup_metrics,
                    "warnings": list(warnings),
                }
            },
            results=(evaluation, error_analysis),
            artifacts=(ArtifactDraft(
                artifact_type="PREDICTION",
                schema_version="prediction-artifact/1",
                media_type="application/json",
                content=_json_bytes(prediction_manifest),
                metadata={
                    "sample_count": len(actual),
                    "final_evaluation_only": True,
                    "model_id": model["model_id"],
                },
            ),),
        )


def register_predictive_training_runners(registry: StageRunnerRegistry) -> None:
    registry.register(PredictivePrepareRunner())
    registry.register(PredictiveTrainRunner())
    registry.register(PredictiveEvaluateRunner())


def _validate_tuning_spec(value: dict[str, Any]) -> dict[str, Any]:
    reject_unknown(
        value,
        {"selection_partitions", "candidates", "objective_metric"},
        name="tuning_spec",
    )
    partitions = value.get("selection_partitions", ["TRAIN", "VALIDATION"])
    if not isinstance(partitions, list) or any(
        partition not in {"TRAIN", "VALIDATION", "TEST"} for partition in partitions
    ):
        raise InvalidSchema("tuning_spec.selection_partitions is invalid")
    candidates = value.get("candidates", [])
    if not isinstance(candidates, list) or candidates:
        raise InvalidSchema("Automated tuning candidates are not supported in the G4 minimal registry")
    return {
        "selection_partitions": partitions,
        "candidates": [],
        "objective_metric": value.get("objective_metric"),
    }


def _subgroup_metrics(*, task_type: str, actual: list[Any], prediction: list[float], subgroups: dict[str, list[Any]], metrics: list[str], split_seed: int) -> list[dict[str, Any]]:
    """Evaluate independent TEST-only subgroup slices in a stable record form."""
    records: list[dict[str, Any]] = []
    for column, values in subgroups.items():
        if len(values) != len(actual):
            raise InvalidSchema("evaluation subgroup values must align with TEST rows")
        groups: list[tuple[Any, list[int]]] = []
        for index, value in enumerate(values):
            normalized = _json_values([value])[0]
            for group_value, indices in groups:
                if group_value == normalized:
                    indices.append(index)
                    break
            else:
                groups.append((normalized, [index]))
        for subgroup_value, indices in groups:
            for metric in dict.fromkeys(metrics):
                sliced_actual = [actual[index] for index in indices]
                sliced_prediction = [prediction[index] for index in indices]
                value, warning = _metric_for_slice(task_type, sliced_actual, sliced_prediction, metric)
                warnings: list[dict[str, str]] = [warning] if warning else []
                uncertainty = None
                if len(indices) < 2:
                    warnings.append({"code": "SUBGROUP_SAMPLE_TOO_SMALL", "message": "At least two TEST records are required for bootstrap uncertainty"})
                elif value is not None:
                    uncertainty, bootstrap_warning = _bootstrap_uncertainty(task_type=task_type, actual=sliced_actual, prediction=sliced_prediction, metric=metric, split_seed=split_seed, subgroup_column=column, subgroup_value=subgroup_value)
                    if bootstrap_warning:
                        warnings.append(bootstrap_warning)
                records.append({"subgroup_column": column, "subgroup_value": subgroup_value, "is_null_group": subgroup_value is None, "metric": metric, "sample_count": len(indices), "value": value, "uncertainty": uncertainty, "status": "EVALUATED" if value is not None else "NON_COMPUTABLE", "warnings": warnings})
    return records


def _metric_for_slice(task_type: str, actual: list[Any], prediction: list[float], metric: str) -> tuple[float | None, dict[str, str] | None]:
    try:
        values = classification_metrics(actual, prediction) if task_type == "BINARY_CLASSIFICATION" else regression_metrics(actual, prediction)
        value = metric_value(values, metric)
    except (PredictiveValidationError, ValueError, TypeError):
        value = None
    if value is None:
        return None, {"code": "SUBGROUP_METRIC_NON_COMPUTABLE", "message": f"{metric} is not computable for this TEST subgroup"}
    return value, None


def _bootstrap_uncertainty(*, task_type: str, actual: list[Any], prediction: list[float], metric: str, split_seed: int, subgroup_column: str, subgroup_value: Any) -> tuple[dict[str, Any] | None, dict[str, str] | None]:
    seed = int(canonical_hash({"namespace": "predictive-subgroup-bootstrap/1", "split_seed": split_seed, "subgroup_column": subgroup_column, "subgroup_value": subgroup_value, "metric": metric})[:16], 16)
    generator = random.Random(seed)
    values: list[float] = []
    for _ in range(1000):
        sample = [generator.randrange(len(actual)) for _ in actual]
        estimate, _ = _metric_for_slice(task_type, [actual[index] for index in sample], [prediction[index] for index in sample], metric)
        if estimate is not None:
            values.append(estimate)
    if len(values) < 200:
        return None, {"code": "SUBGROUP_BOOTSTRAP_INSUFFICIENT_VALID_RESAMPLES", "message": "Fewer than 200 valid bootstrap resamples were available"}
    values.sort()
    return {"method": "percentile_bootstrap", "confidence": 0.95, "lower": _percentile(values, 0.025), "upper": _percentile(values, 0.975), "requested_resamples": 1000, "valid_resamples": len(values)}, None


def _percentile(values: list[float], probability: float) -> float:
    position = (len(values) - 1) * probability
    lower = int(position)
    upper = min(lower + 1, len(values) - 1)
    return values[lower] + (values[upper] - values[lower]) * (position - lower)


def _json_values(values: list[Any]) -> list[Any]:
    return [value.item() if hasattr(value, "item") else value for value in values]


def _json_bytes(value: dict[str, Any]) -> bytes:
    canonical_hash(value)
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
