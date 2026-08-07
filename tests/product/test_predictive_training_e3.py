from __future__ import annotations

import pandas as pd
import pytest

from ariadne.capabilities.predictive import (
    PredictivePlanner,
    register_predictive_split_runner,
    register_predictive_training_runners,
)
from ariadne.product.workflow.executor import GenericExecutor
from ariadne.product.workflow.runner_registry import StageRunnerRegistry


def _registry() -> StageRunnerRegistry:
    registry = StageRunnerRegistry()
    register_predictive_split_runner(registry)
    register_predictive_training_runners(registry)
    return registry


def _frame() -> pd.DataFrame:
    scores = list(range(-60, 60))
    return pd.DataFrame({
        "score": scores,
        "segment": ["A" if index % 3 else "B" for index in range(len(scores))],
        "converted": [int(score >= 0) for score in scores],
    })


def _full_spec(predictive_spec_factory) -> dict:  # type: ignore[no-untyped-def,type-arg]
    spec = predictive_spec_factory()
    spec["feature_spec"] = {
        "feature_columns": ["score", "segment"],
        "availability_cutoff": {
            name: {
                "column": name,
                "available_at": "PREDICTION_TIME",
                "allowed": True,
            }
            for name in ("score", "segment")
        },
        "excluded_columns": ["converted"],
    }
    spec["split_spec"].update({"strategy": "STRATIFIED", "stratify": True})
    spec["preprocessing_spec"] = {
        "fit_partition": "TRAIN",
        "numeric_imputation": "MEAN",
        "scale_numeric": True,
        "categorical_encoding": "ONE_HOT",
    }
    spec["model_spec"] = {
        "model_id": "logistic_regression.v1",
        "parameters": {"iterations": 800, "learning_rate": 0.1, "l2": 0.001},
    }
    spec["tuning_spec"] = {"selection_partitions": ["TRAIN", "VALIDATION"]}
    return spec


def _execute(spec: dict) -> object:  # type: ignore[type-arg]
    plan = PredictivePlanner().build_full_plan(
        project_id="project",
        specification_id="fixed-specification",
        family_spec=spec,
    )
    return GenericExecutor(_registry()).execute(
        "execution",
        plan,
        external_inputs={
            "split": {
                "frame": _frame(),
                "source_snapshot": {
                    "schema_version": "predictive-source-snapshot/1",
                    "dataset_version_id": "dataset",
                    "dataset_content_hash": "a" * 64,
                    "analysis_view_id": None,
                    "analysis_view_hash": None,
                    "materialized_hash": "a" * 64,
                },
            },
            "prepare": {"frame": _frame()},
        },
    )


@pytest.mark.requirement("G4-PREDICTIVE-TRAINING-DAG")
def test_full_predictive_dag_is_deterministic_and_keeps_test_out_of_training(
    predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    spec = _full_spec(predictive_spec_factory)
    first = _execute(spec)
    second = _execute(spec)
    assert first.status == "SUCCEEDED"
    assert [stage.stage_key for stage in first.stages] == [
        "split", "prepare", "train", "evaluate",
    ]
    assert {stage.status.value for stage in first.stages} == {"SUCCEEDED"}

    prepare = next(stage for stage in first.stages if stage.stage_key == "prepare")
    train = next(stage for stage in first.stages if stage.stage_key == "train")
    evaluate = next(stage for stage in first.stages if stage.stage_key == "evaluate")
    assert prepare.output_binding["fitted_preprocessor"]["fit_partition"] == "TRAIN"
    assert prepare.output_binding["evaluation_bundle"]["selection_allowed"] is False
    assert "evaluation_bundle" not in train.input_binding
    assert "test" not in train.input_binding["training_bundle"]
    assert train.input_binding["training_bundle"]["selection_partitions"] == [
        "TRAIN", "VALIDATION",
    ]
    assert evaluate.input_binding["evaluation_bundle"]["final_evaluation_only"] is True

    first_model = next(
        artifact.content for artifact in first.artifacts
        if artifact.artifact_type == "FITTED_MODEL"
    )
    second_model = next(
        artifact.content for artifact in second.artifacts
        if artifact.artifact_type == "FITTED_MODEL"
    )
    assert first_model == second_model
    training = next(result for result in first.results if result.result_type == "TRAINING_RESULT")
    assert training.analytical_status in {"TRAINED", "TRAINED_WITH_WARNINGS"}
    assert training.payload["model_descriptor"]["model_id"] == "logistic_regression.v1"


@pytest.mark.requirement("G4-MINIMAL-MODEL-REGISTRY")
def test_regression_uses_only_registered_deterministic_linear_model(
    predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    spec = predictive_spec_factory("REGRESSION")
    spec["model_spec"] = {
        "model_id": "linear_regression.v1",
        "parameters": {"l2": 0.0},
    }
    spec["tuning_spec"] = {"selection_partitions": ["TRAIN", "VALIDATION"]}
    frame = pd.DataFrame({
        "score": list(range(100)),
        "converted": [3 * value - 2 for value in range(100)],
    })
    plan = PredictivePlanner().build_full_plan(
        project_id="project", specification_id="regression-spec", family_spec=spec
    )
    outcome = GenericExecutor(_registry()).execute(
        "regression-execution",
        plan,
        external_inputs={
            "split": {
                "frame": frame,
                "source_snapshot": {
                    "dataset_version_id": "dataset",
                    "dataset_content_hash": "b" * 64,
                    "materialized_hash": "b" * 64,
                },
            },
            "prepare": {"frame": frame},
        },
    )
    assert outcome.status == "SUCCEEDED"
    training = next(result for result in outcome.results if result.result_type == "TRAINING_RESULT")
    assert training.summary["model"]["model_id"] == "linear_regression.v1"
