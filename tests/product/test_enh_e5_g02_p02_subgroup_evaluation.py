"""Focused ENH-E5 G02 P02 subgroup-evaluation contracts."""

from __future__ import annotations

import pandas as pd
from pathlib import Path

from ariadne.capabilities.predictive import training_runners
from ariadne.capabilities.predictive.training_runners import PredictivePrepareRunner, _subgroup_metrics
from ariadne.product.domain.execution_plan import StageDefinition, StageType
from ariadne.product.workflow.contracts import StageContext


def test_predictive_setup_surface_and_six_navigation_stages_are_exposed() -> None:
    repository = Path(__file__).parents[2]
    html = (repository / "frontend" / "index.html").read_text(encoding="utf-8")
    predictive = html.split('<section id="predictive"', 1)[1].split('<section id="results"', 1)[0]
    assert all(f'name="{name}"' in predictive for name in (
        "task_type", "target", "feature_columns", "feature_availability", "excluded_columns",
        "split_strategy", "train_ratio", "validation_ratio", "test_ratio", "group_column",
        "time_column", "train_cutoff", "validation_cutoff", "seed", "scale_numeric", "model_id",
        "tuning_selection", "primary_metric", "secondary_metrics", "subgroups", "explanation_method",
        "explanation_sample_size",
    ))
    catalog = (repository / "src/ariadne/product/application/navigation_catalog.py").read_text(encoding="utf-8")
    assert '"setup", "train", "predict", "metrics", "explainability", "model-management"' in catalog


def test_prepare_retains_test_ordinals_and_non_feature_subgroup_columns(
    predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    spec = predictive_spec_factory()
    spec["evaluation_spec"]["subgroups"] = ["region"]
    context = StageContext(
        execution_id="p02", stage=StageDefinition(
            stage_key="prepare", stage_type=StageType("predictive", "prepare", "1"),
            input_contract={}, output_contract={}, parameters=spec,
        ),
        inputs={
            "frame": pd.DataFrame({"score": [1, 2, 3, 4], "converted": [0, 1, 0, 1], "region": ["east", None, "west", "west"]}),
            "partition_manifest": {
                "schema_version": "partition-artifact/1",
                "partitions": {"TRAIN": [0, 1], "VALIDATION": [2], "TEST": [3]},
                "selection_contract": {"TEST": {"selection_allowed": False}},
                "source_snapshot": {}, "row_identifier": "row_ordinal", "specification_hash": "spec",
            },
        },
    )
    bundle = PredictivePrepareRunner().run(context).output_bindings["evaluation_bundle"]
    assert bundle["test"]["row_ordinals"] == [3]
    assert bundle["test"]["subgroups"] == {"region": ["west"]}


def test_subgroup_records_are_test_slices_with_stable_bootstrap_and_null_groups() -> None:
    actual = [0, 1, 0, 1, 0, 1]
    prediction = [0.1, 0.9, 0.2, 0.8, 0.3, 0.7]
    subgroups = {"region": ["east", "east", None, None, "west", "west"]}
    first = _subgroup_metrics(
        task_type="BINARY_CLASSIFICATION", actual=actual, prediction=prediction,
        subgroups=subgroups, metrics=["ROC_AUC", "ACCURACY"], split_seed=17,
    )
    second = _subgroup_metrics(
        task_type="BINARY_CLASSIFICATION", actual=actual, prediction=prediction,
        subgroups=subgroups, metrics=["ROC_AUC", "ACCURACY"], split_seed=17,
    )

    assert first == second
    assert len(first) == 6
    assert all(set(record) == {
        "subgroup_column", "subgroup_value", "is_null_group", "metric", "sample_count",
        "value", "uncertainty", "status", "warnings",
    } for record in first)
    null_records = [record for record in first if record["is_null_group"]]
    assert len(null_records) == 2
    assert all(record["subgroup_value"] is None and record["sample_count"] == 2 for record in null_records)
    assert all(record["uncertainty"] is not None for record in first if record["metric"] == "ROC_AUC")
    accuracy_records = [record for record in first if record["metric"] == "ACCURACY"]
    assert all(record["uncertainty"] is not None for record in accuracy_records)
    assert all(record["uncertainty"]["requested_resamples"] == 1000 for record in accuracy_records)


def test_subgroup_suppresses_uncertainty_for_small_and_noncomputable_slices() -> None:
    records = _subgroup_metrics(
        task_type="BINARY_CLASSIFICATION", actual=[0, 0, 1], prediction=[0.1, 0.2, 0.9],
        subgroups={"non_feature": ["only", "only", "singleton"]}, metrics=["ROC_AUC"], split_seed=17,
    )

    only = next(record for record in records if record["subgroup_value"] == "only")
    singleton = next(record for record in records if record["subgroup_value"] == "singleton")
    assert only["sample_count"] == 2
    assert only["value"] is None and only["uncertainty"] is None
    assert only["status"] == "NON_COMPUTABLE"
    assert singleton["sample_count"] == 1
    assert singleton["uncertainty"] is None
    assert {warning["code"] for warning in singleton["warnings"]} >= {"SUBGROUP_SAMPLE_TOO_SMALL"}


def test_subgroup_suppresses_uncertainty_below_minimum_valid_resamples(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setattr(
        training_runners, "_metric_for_slice", lambda *args: (None, None)
    )
    uncertainty, warning = training_runners._bootstrap_uncertainty(
        task_type="BINARY_CLASSIFICATION", actual=[0, 1], prediction=[0.1, 0.9],
        metric="ROC_AUC", split_seed=17, subgroup_column="region", subgroup_value="east",
    )
    assert uncertainty is None
    assert warning is not None
    assert warning["code"] == "SUBGROUP_BOOTSTRAP_INSUFFICIENT_VALID_RESAMPLES"
