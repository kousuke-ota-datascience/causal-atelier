"""Predictive split Stage Runner; no model fitting occurs in Gate G3."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import pandas as pd

from ariadne.capabilities.predictive.splitting import build_partitions, comparable_time
from ariadne.capabilities.predictive.validation import validate_predictive_specification
from ariadne.product.domain.execution_plan import StageType
from ariadne.product.domain.schemas import canonical_hash
from ariadne.product.workflow.contracts import ArtifactDraft, StageContext, StageRunResult
from ariadne.product.workflow.runner_registry import StageRunnerRegistry


@dataclass
class PredictiveSplitRunner:
    @property
    def stage_type(self) -> StageType:
        return StageType("predictive", "split", "1")

    def validate(self, context: StageContext) -> None:
        frame = context.inputs.get("frame")
        if not isinstance(frame, pd.DataFrame) or frame.empty:
            raise ValueError("Predictive split requires a non-empty pandas analysis frame")
        validate_predictive_specification(context.stage.parameters)
        spec = context.stage.parameters
        question = spec["prediction_question"]
        feature = spec["feature_spec"]
        split = spec["split_spec"]
        referenced = {
            question["target"], *feature["feature_columns"],
            *([split["group_column"]] if split.get("group_column") else []),
            *([split["time_column"]] if split.get("time_column") else []),
        }
        unknown = sorted(referenced - set(frame.columns))
        if unknown:
            raise ValueError(f"Predictive specification references unknown columns: {unknown}")
        source = context.inputs.get("source_snapshot")
        if not isinstance(source, dict) or not source.get("dataset_version_id"):
            raise ValueError("Predictive split requires an immutable source snapshot")

    def run(self, context: StageContext) -> StageRunResult:
        frame: pd.DataFrame = context.inputs["frame"]
        source: dict[str, Any] = context.inputs["source_snapshot"]
        spec = context.stage.parameters
        question, split = spec["prediction_question"], spec["split_spec"]
        row_ids = list(range(len(frame)))
        strategy = split["strategy"]
        partitions = build_partitions(
            row_ids,
            strategy=strategy,
            train_ratio=float(split.get("train_ratio") or 0),
            validation_ratio=float(split.get("validation_ratio") or 0),
            seed=split["seed"],
            targets=frame[question["target"]].tolist() if strategy == "STRATIFIED" else None,
            groups=frame[split["group_column"]].tolist() if strategy == "GROUP" else None,
            times=frame[split["time_column"]].tolist() if strategy == "TIME_BASED" else None,
            train_cutoff=split.get("train_cutoff"),
            validation_cutoff=split.get("validation_cutoff"),
        )
        manifest: dict[str, Any] = {
            "schema_version": "partition-artifact/1",
            "analysis_family": "PREDICTIVE",
            "task_type": spec["task_type"],
            "strategy": strategy,
            "seed": split["seed"],
            "specification_hash": canonical_hash(spec),
            "source_snapshot": source,
            "row_identifier": {
                "kind": "ANALYSIS_VIEW_ROW_ORDINAL" if source.get("analysis_view_id")
                else "DATASET_ROW_ORDINAL",
                "zero_based": True,
            },
            "partitions": partitions,
            "partition_counts": {name: len(values) for name, values in partitions.items()},
            "selection_contract": {
                "TRAIN": {"fit_allowed": True, "selection_allowed": True},
                "VALIDATION": {"fit_allowed": False, "selection_allowed": True},
                "TEST": {
                    "fit_allowed": False,
                    "selection_allowed": False,
                    "final_evaluation_only": True,
                },
            },
        }
        if strategy == "STRATIFIED":
            manifest["class_distribution"] = {
                partition: _counts(frame.iloc[indices][question["target"]])
                for partition, indices in partitions.items()
            }
        if strategy == "GROUP":
            manifest["group_counts"] = {
                partition: int(frame.iloc[indices][split["group_column"]].nunique())
                for partition, indices in partitions.items()
            }
        if strategy == "TIME_BASED":
            manifest["time_boundaries"] = {
                partition: {
                    "min": _json_value(frame.iloc[indices][split["time_column"]].min()),
                    "max": _json_value(frame.iloc[indices][split["time_column"]].max()),
                }
                for partition, indices in partitions.items()
            }
            _assert_time_boundaries(manifest["time_boundaries"])
        content = json.dumps(
            manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False,
        ).encode("utf-8")
        summary = {key: value for key, value in manifest.items() if key != "partitions"}
        return StageRunResult(
            output_bindings={"partition_manifest": summary},
            artifacts=(ArtifactDraft(
                artifact_type="PARTITION_INDEX",
                schema_version="partition-artifact/1",
                media_type="application/json",
                content=content,
                metadata={
                    "partition_counts": manifest["partition_counts"],
                    "selection_contract": manifest["selection_contract"],
                    "specification_hash": manifest["specification_hash"],
                },
            ),),
        )


def register_predictive_split_runner(registry: StageRunnerRegistry) -> None:
    registry.register(PredictiveSplitRunner())


def _counts(values: pd.Series) -> dict[str, int]:
    return {str(key): int(count) for key, count in values.value_counts(dropna=False).items()}


def _json_value(value: Any) -> Any:
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if hasattr(value, "item"):
        return value.item()
    return value


def _assert_time_boundaries(boundaries: dict[str, dict[str, Any]]) -> None:
    if not (
        comparable_time(boundaries["TRAIN"]["max"])
        < comparable_time(boundaries["VALIDATION"]["min"])
        <= comparable_time(boundaries["VALIDATION"]["max"])
        < comparable_time(boundaries["TEST"]["min"])
    ):
        raise ValueError("TEMPORAL_LEAKAGE_RISK: temporal partitions overlap or are unordered")
