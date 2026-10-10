"""Deterministic predictive explanations and model cards for G5."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from ariadne.capabilities.predictive.modeling import predict
from ariadne.capabilities.predictive.validation import (
    validate_predictive_specification,
)
from ariadne.product.domain.errors import InvalidSchema, PredictiveValidationError
from ariadne.product.domain.execution_plan import StageType
from ariadne.product.domain.schemas import canonical_hash
from ariadne.product.workflow.contracts import (
    ArtifactDraft,
    ResultDraft,
    StageContext,
    StageRunResult,
)
from ariadne.product.workflow.runner_registry import StageRunnerRegistry


SUPPORTED_EXPLANATION_METHOD = "LINEAR_COEFFICIENT_CONTRIBUTION"
TERMINOLOGY_LIMITATION = (
    "Predictive Explanation is not a Causal Explanation or Treatment Effect."
)


@dataclass
class PredictiveExplainRunner:
    @property
    def stage_type(self) -> StageType:
        return StageType("predictive", "explain", "1")

    def validate(self, context: StageContext) -> None:
        validate_predictive_specification(context.stage.parameters)
        model = context.inputs.get("frozen_model")
        preprocessor = context.inputs.get("fitted_preprocessor")
        dataset = context.inputs.get("explanation_dataset")
        reference = context.inputs.get("explanation_reference")
        explanation = context.inputs.get("explanation_specification")
        sampling = context.inputs.get("sampling_definition")
        training = context.inputs.get("training_summary")
        evaluation = context.inputs.get("evaluation_summary")
        partition = context.inputs.get("partition_manifest")
        if not isinstance(model, dict) or model.get("schema_version") not in {"fitted-model/1", "fitted-model/2"}:
            raise InvalidSchema("EXPLAIN requires fitted-model/1 or fitted-model/2")
        if (
            not isinstance(preprocessor, dict)
            or preprocessor.get("schema_version") != "fitted-preprocessor/1"
            or preprocessor.get("fit_partition") != "TRAIN"
        ):
            raise InvalidSchema("EXPLAIN requires a TRAIN-fitted preprocessor")
        if model.get("preprocessor_hash") != preprocessor.get("canonical_hash"):
            raise PredictiveValidationError(
                "PREPROCESSOR_MODEL_MISMATCH",
                "Frozen model and preprocessor do not match",
                path="fitted_preprocessor",
            )
        if (
            not isinstance(dataset, dict)
            or dataset.get("schema_version") != "predictive-explanation-dataset/1"
            or dataset.get("partition") != "TEST"
            or dataset.get("selection_allowed") is not False
            or dataset.get("explanation_only") is not True
        ):
            raise PredictiveValidationError(
                "EXPLANATION_DATASET_INVALID",
                "EXPLAIN requires an explicit non-selection TEST dataset",
                path="explanation_dataset",
            )
        if dataset.get("feature_order") != model.get("feature_order"):
            raise PredictiveValidationError(
                "EXPLANATION_FEATURE_MISMATCH",
                "Explanation features do not match the frozen model",
                path="explanation_dataset.feature_order",
            )
        if explanation and explanation.get("method") == "LIME_TABULAR" and (
            not isinstance(reference, dict)
            or reference.get("schema_version") != "predictive-explanation-reference/1"
            or reference.get("partition") != "TRAIN"
        ):
            raise InvalidSchema("EXPLAIN requires a TRAIN explanation reference")
        if not isinstance(explanation, dict) or not explanation:
            raise InvalidSchema("EXPLAIN requires an explicit explanation specification")
        if explanation != context.stage.parameters.get("explanation_spec"):
            raise InvalidSchema("Explanation input differs from the fixed Specification")
        if sampling != explanation.get("sampling"):
            raise InvalidSchema("Sampling input differs from the fixed explanation specification")
        if (
            not isinstance(training, dict)
            or training.get("schema_version") != "predictive-training-summary/1"
        ):
            raise InvalidSchema("EXPLAIN requires predictive-training-summary/1")
        if (
            not isinstance(evaluation, dict)
            or evaluation.get("schema_version") != "predictive-evaluation-summary/1"
        ):
            raise InvalidSchema("EXPLAIN requires predictive-evaluation-summary/1")
        if (
            not isinstance(partition, dict)
            or partition.get("schema_version") != "partition-artifact/1"
        ):
            raise InvalidSchema("EXPLAIN requires partition-artifact/1")

    def run(self, context: StageContext) -> StageRunResult:
        model: dict[str, Any] = context.inputs["frozen_model"]
        preprocessor: dict[str, Any] = context.inputs["fitted_preprocessor"]
        dataset: dict[str, Any] = context.inputs["explanation_dataset"]
        reference: dict[str, Any] | None = context.inputs.get("explanation_reference")
        explanation: dict[str, Any] = context.inputs["explanation_specification"]
        sampling: dict[str, Any] = context.inputs["sampling_definition"]
        training: dict[str, Any] = context.inputs["training_summary"]
        evaluation: dict[str, Any] = context.inputs["evaluation_summary"]
        partition: dict[str, Any] = context.inputs["partition_manifest"]
        spec = context.stage.parameters

        method = explanation["method"]
        warnings: list[dict[str, Any]] = []
        limitations = [
            TERMINOLOGY_LIMITATION,
            "Coefficient contributions depend on the recorded preprocessing and model specification.",
        ]
        output_scale = (
            "LOG_ODDS"
            if model["task_type"] == "BINARY_CLASSIFICATION"
            else "PREDICTION"
        )
        supported = method == SUPPORTED_EXPLANATION_METHOD
        if method == "LIME_TABULAR":
            from ariadne.capabilities.predictive.lime_backend import explain_lime_local, reject_lime_global
            if not explanation["local_explanations"]:
                reject_lime_global()
            global_explanation = None
            assert reference is not None  # validated above for LIME only
            local_explanation = [explain_lime_local(model, reference["features"], row, ordinal, sampling["seed"]) for ordinal, row in zip(dataset["row_ordinals"][:sampling["size"]], dataset["features"][:sampling["size"]], strict=True)]
            if local_explanation:
                output_scale = local_explanation[0]["output_scale"]
            status = "GENERATED"
            supported = False
        elif supported:
            if (
                explanation["local_explanations"]
                and sampling["size"] > len(dataset["row_ordinals"])
            ):
                warnings.append({
                    "code": "EXPLANATION_SAMPLE_TRUNCATED",
                    "message": (
                        "Requested local explanation sample exceeds the TEST "
                        "population; all available TEST rows were used"
                    ),
                })
            global_explanation = _global_explanation(model)
            local_explanation = (
                _local_explanations(model, dataset, sampling)
                if explanation["local_explanations"]
                else []
            )
            status = "GENERATED_WITH_WARNINGS" if warnings else "GENERATED"
        else:
            global_explanation = None
            local_explanation = []
            status = "NOT_APPLICABLE"
            warnings.append({
                "code": "EXPLANATION_METHOD_NOT_APPLICABLE",
                "message": (
                    f"Method {method!r} is not supported for model "
                    f"{model['model_id']!r}; no approximate values were generated"
                ),
            })

        method_provenance = _method_provenance(
            method=method,
            model=model,
            preprocessor=preprocessor,
            dataset=dataset,
            sampling=sampling,
            local_explanation=local_explanation,
            output_scale=output_scale,
            runtime_versions=context.snapshots.get("versions", {}),
        )
        explanation_document = {
            "schema_version": "predictive-explanation-result/1",
            "explanation_method": method,
            "explanation_dataset_provenance": dataset["provenance"],
            "sampling": {
                **sampling,
                "available_sample_count": len(dataset["row_ordinals"]),
                "selected_sample_count": min(
                    sampling["size"], len(dataset["row_ordinals"])
                ),
            },
            "background_reference_data": {
                **dataset["background_reference"],
                "preprocessor_hash": preprocessor["canonical_hash"],
                "feature_schema": preprocessor["columns"],
            },
            "model_output_scale": output_scale,
            "prediction_output_scale": (
                "PROBABILITY"
                if model["task_type"] == "BINARY_CLASSIFICATION"
                else "PREDICTION"
            ),
            "global_explanation": global_explanation,
            "local_explanation": local_explanation,
            "warnings": warnings,
            "limitations": limitations,
        }
        if method_provenance is not None:
            explanation_document["method_provenance"] = method_provenance
        model_card_warnings = [
            *training.get("warnings", []),
            *evaluation.get("warnings", []),
            *warnings,
        ]
        model_card_document = {
            "schema_version": "predictive-model-card-result/1",
            "intended_use": spec["prediction_question"]["intended_use"],
            "deployment_population": spec["prediction_question"][
                "deployment_population"
            ],
            "training_data": {
                "source_snapshot": partition["source_snapshot"],
                "partitions": partition["partition_counts"],
                "training_partition": "TRAIN",
                "analysis_view_id": partition["source_snapshot"].get(
                    "analysis_view_id"
                ),
            },
            "feature_set": {
                "input_features": spec["feature_spec"]["feature_columns"],
                "output_features": preprocessor["output_features"],
                "excluded_columns": spec["feature_spec"]["excluded_columns"],
            },
            "split_strategy": {
                "strategy": partition["strategy"],
                "seed": partition["seed"],
                "partition_counts": partition["partition_counts"],
            },
            "model_descriptor": training["model_descriptor"],
            "model_artifact_provenance": {
                "schema_version": model["schema_version"],
                "provider": model.get("provider", "ariadne.native"),
                "payload_format": model.get("payload_format", "ariadne-linear-json/1"),
                "library": model.get("library", "ariadne"),
                "library_version": model.get("library_version"),
                "provenance": model.get("provenance", {}),
            },
            "selected_hyperparameters": training["selected_hyperparameters"],
            "validation_metrics": training["validation_metrics"],
            "test_metrics": evaluation["metrics"],
            "limitations": [
                TERMINOLOGY_LIMITATION,
                "Recorded performance applies to the immutable TEST population and specification.",
            ],
            "warnings": model_card_warnings,
            "code_runtime_metadata": context.snapshots.get("versions", {}),
        }
        if method_provenance is not None:
            model_card_document["explanation_provenance"] = method_provenance
        explanation_result = ResultDraft(
            result_type="PREDICTIVE_EXPLANATION_RESULT",
            schema_version="predictive-explanation-result/1",
            analytical_status=status,
            summary={
                "method": method,
                "model_id": model["model_id"],
                "model_output_scale": output_scale,
                "sample_count": explanation_document["sampling"][
                    "selected_sample_count"
                ],
            },
            payload=explanation_document,
            diagnostics={
                "predictive_not_causal": True,
                "selection_allowed": False,
            },
            warnings=tuple(warnings),
        )
        model_card_result = ResultDraft(
            result_type="MODEL_CARD_RESULT",
            schema_version="predictive-model-card-result/1",
            analytical_status=(
                "GENERATED_WITH_WARNINGS" if model_card_warnings else "GENERATED"
            ),
            summary={
                "model_id": model["model_id"],
                "task_type": model["task_type"],
                "intended_use": model_card_document["intended_use"],
            },
            payload=model_card_document,
            diagnostics={"predictive_not_causal": True},
            warnings=tuple(model_card_warnings),
        )
        return StageRunResult(
            output_bindings={
                "explanation_summary": {
                    "schema_version": "predictive-explanation-summary/1",
                    "analytical_status": status,
                    "method": method,
                    "sample_count": explanation_document["sampling"][
                        "selected_sample_count"
                    ],
                },
                "model_card": model_card_document,
            },
            results=(explanation_result, model_card_result),
            artifacts=(
                ArtifactDraft(
                    artifact_type="PREDICTIVE_EXPLANATION",
                    schema_version="predictive-explanation-artifact/1",
                    media_type="application/json",
                    content=_json_bytes(explanation_document),
                    metadata={
                        "method": method,
                        "dataset_partition": dataset["partition"],
                        "model_output_scale": output_scale,
                    },
                    result_type="PREDICTIVE_EXPLANATION_RESULT",
                ),
                ArtifactDraft(
                    artifact_type="MODEL_CARD",
                    schema_version="predictive-model-card-artifact/1",
                    media_type="application/json",
                    content=_json_bytes(model_card_document),
                    metadata={
                        "model_id": model["model_id"],
                        "task_type": model["task_type"],
                    },
                    result_type="MODEL_CARD_RESULT",
                ),
            ),
        )


def register_predictive_explain_runner(registry: StageRunnerRegistry) -> None:
    registry.register(PredictiveExplainRunner())


def _global_explanation(model: dict[str, Any]) -> list[dict[str, Any]]:
    feature_order = model["feature_order"]
    coefficients = model["coefficients"]
    if len(feature_order) != len(coefficients):
        raise InvalidSchema("Model coefficient count does not match feature order")
    ranked = sorted(
        zip(feature_order, coefficients, strict=True),
        key=lambda item: (-abs(float(item[1])), item[0]),
    )
    return [
        {
            "rank": rank,
            "feature": feature,
            "coefficient": float(coefficient),
            "absolute_coefficient": abs(float(coefficient)),
        }
        for rank, (feature, coefficient) in enumerate(ranked, start=1)
    ]


def _local_explanations(
    model: dict[str, Any],
    dataset: dict[str, Any],
    sampling: dict[str, Any],
) -> list[dict[str, Any]]:
    size = min(sampling["size"], len(dataset["row_ordinals"]))
    feature_order = model["feature_order"]
    coefficients = [float(value) for value in model["coefficients"]]
    values: list[dict[str, Any]] = []
    for row_ordinal, features in zip(
        dataset["row_ordinals"][:size],
        dataset["features"][:size],
        strict=True,
    ):
        contributions = [
            {
                "feature": feature,
                "transformed_value": float(value),
                "contribution_to_model_output": float(value) * coefficient,
            }
            for feature, value, coefficient in zip(
                feature_order, features, coefficients, strict=True
            )
        ]
        linear_output = float(model["intercept"]) + sum(
            item["contribution_to_model_output"] for item in contributions
        )
        values.append({
            "row_ordinal": row_ordinal,
            "base_value": float(model["intercept"]),
            "linear_output": linear_output,
            "model_output": linear_output,
            "prediction": predict(model, [features])[0],
            "feature_contributions": contributions,
        })
    return values


def _method_provenance(
    *,
    method: str,
    model: dict[str, Any],
    preprocessor: dict[str, Any],
    dataset: dict[str, Any],
    sampling: dict[str, Any],
    local_explanation: list[dict[str, Any]],
    output_scale: str,
    runtime_versions: dict[str, Any],
) -> dict[str, Any] | None:
    """Return additive, public provenance without retaining TRAIN rows.

    LIME is the provider that needs a runtime TRAIN reference.  Its local
    records already carry the provider facts; this projection makes the same
    immutable facts available at result, artifact, and Model Card level.
    """
    if method != "LIME_TABULAR" or not local_explanation:
        return None
    first = local_explanation[0]
    return {
        "method_id": first["method"],
        "method_version": first["method_version"],
        "model_identity": {
            "model_id": model["model_id"],
            "task_type": model["task_type"],
            "model_schema_version": model["schema_version"],
            "preprocessor_hash": model["preprocessor_hash"],
        },
        "preprocessor_identity": {
            "schema_version": preprocessor["schema_version"],
            "canonical_hash": preprocessor["canonical_hash"],
        },
        "feature_representation": {
            "name": first["feature_representation"],
            "feature_order": first["feature_order"],
            "feature_order_hash": first["feature_order_hash"],
            "categorical_feature_indices": first["categorical_feature_indices"],
        },
        "test_instances": [
            {
                "row_ordinal": entry["row_ordinal"],
                "feature_order_hash": entry["feature_order_hash"],
            }
            for entry in local_explanation
        ],
        "train_reference": first["reference"],
        "output_scale": output_scale,
        "sampling": dict(sampling),
        "effective_seeds": [entry["effective_seed"] for entry in local_explanation],
        "parameters": first["parameters"],
        "provider": first["provider"],
        "runtime_versions": runtime_versions,
        "limitations": [
            TERMINOLOGY_LIMITATION,
            first["limitation"],
        ],
    }


def _json_bytes(value: dict[str, Any]) -> bytes:
    canonical_hash(value)
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
