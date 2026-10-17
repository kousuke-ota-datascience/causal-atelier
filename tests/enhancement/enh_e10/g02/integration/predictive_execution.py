"""Deterministic full-DAG helpers shared only by ENH-E10 G02 integration tests."""

from __future__ import annotations

import pandas as pd

from ariadne.capabilities.predictive import (
    PredictivePlanner,
    register_predictive_explain_runner,
    register_predictive_split_runner,
    register_predictive_training_runners,
)
from ariadne.product.workflow.executor import GenericExecutor
from ariadne.product.workflow.plan_validator import PlanValidator
from ariadne.product.workflow.runner_registry import StageRunnerRegistry


def build_explanation_spec(predictive_spec_factory, method: str) -> dict:  # type: ignore[no-untyped-def,type-arg]
    spec = predictive_spec_factory()
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
    spec["explanation_spec"] = {
        "method": method,
        "dataset": "TEST",
        "sampling": {"strategy": "FIRST_N", "size": 5, "seed": 17},
        "local_explanations": True,
    }
    return spec


def execute_predictive(spec: dict, frame: pd.DataFrame | None = None) -> object:  # type: ignore[type-arg]
    frame = _frame() if frame is None else frame
    registry = _registry()
    plan = PredictivePlanner().build_full_plan(
        project_id="project",
        specification_id="fixed-specification",
        family_spec=spec,
    )
    PlanValidator(registry).validate(plan)
    return GenericExecutor(registry).execute(
        "execution",
        plan,
        external_inputs={
            "split": {
                "frame": frame,
                "source_snapshot": {
                    "schema_version": "predictive-source-snapshot/1",
                    "dataset_version_id": "dataset",
                    "dataset_content_hash": "a" * 64,
                    "analysis_view_id": None,
                    "analysis_view_hash": None,
                    "materialized_hash": "a" * 64,
                },
            },
            "prepare": {"frame": frame},
        },
        snapshots={"versions": {
            "code": "ariadne/0.1.0", "python": "3.12",
            "schemas": ["predictive-analysis-spec/1"],
        }},
    )


def _registry() -> StageRunnerRegistry:
    registry = StageRunnerRegistry()
    register_predictive_split_runner(registry)
    register_predictive_training_runners(registry)
    register_predictive_explain_runner(registry)
    return registry


def _frame() -> pd.DataFrame:
    scores = list(range(-60, 60))
    return pd.DataFrame({
        "score": scores,
        "converted": [int(score >= 0) for score in scores],
    })
