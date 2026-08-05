#!/usr/bin/env python3
"""Run the integrated discovery-to-inference experiment with MLflow tracking.

This entrypoint executes the CONFIGURED_FEATURE_BUILD pipeline used by the
Complete Journey experiment. It intentionally does not create an Ariadne
database Execution. The MLflow run ID is used as the CLI pipeline identity
until the application service accepts ExecutionIdentity explicitly.
"""

from __future__ import annotations

import csv
import json
import math
import os
import sys
from argparse import Namespace
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import mlflow
import yaml

from ariadne.application.pipeline.end_to_end import execute
from ariadne.application.pipeline.strategies import format_validation
from ariadne.interfaces.cli.pipeline import parse_args


EXPERIMENT_DIR = Path(__file__).resolve().parent
EXPERIMENT_CONFIG_PATH = EXPERIMENT_DIR / "config.yaml"
DEFAULT_EXPERIMENT_NAME = "004_discovery_inference_integration"


def _read_yaml(path: Path) -> dict[str, Any]:
    """Read a YAML mapping and fail with a useful error for invalid input."""
    if not path.is_file():
        raise FileNotFoundError(f"YAML file does not exist: {path}")

    with path.open("r", encoding="utf-8") as stream:
        document = yaml.safe_load(stream)

    if document is None:
        return {}

    if not isinstance(document, dict):
        raise ValueError(f"Expected a YAML mapping at {path}, got {type(document).__name__}")

    return document


def _resolve_project_root(args: Namespace) -> Path:
    """Resolve the repository root.

    Priority:
      1. --project-root
      2. ARIADNE_PROJECT_ROOT
      3. repository root inferred from this file
      4. current working directory as a final fallback
    """
    if args.project_root is not None:
        candidate = Path(args.project_root).expanduser().resolve()
    elif os.getenv("ARIADNE_PROJECT_ROOT"):
        candidate = Path(os.environ["ARIADNE_PROJECT_ROOT"]).expanduser().resolve()
    else:
        # run.py is normally:
        # <project-root>/experiments/004_discovery_inference_integration/run.py
        candidate = EXPERIMENT_DIR.parents[1].resolve()

    if not (candidate / "pyproject.toml").is_file():
        cwd = Path.cwd().resolve()
        if (cwd / "pyproject.toml").is_file():
            candidate = cwd

    if not (candidate / "pyproject.toml").is_file():
        raise FileNotFoundError(
            "Could not locate the Ariadne repository root. "
            "Specify it with --project-root or ARIADNE_PROJECT_ROOT."
        )

    return candidate


def _resolve_path(project_root: Path, value: str | Path) -> Path:
    """Resolve a project-relative path without requiring it to exist."""
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = project_root / path
    return path.resolve()


def _load_experiment_config() -> dict[str, Any]:
    """Load this experiment's metadata and pipeline reference."""
    config = _read_yaml(EXPERIMENT_CONFIG_PATH)

    experiment = config.get("experiment")
    if experiment is not None and not isinstance(experiment, dict):
        raise ValueError(
            f"'experiment' must be a mapping in {EXPERIMENT_CONFIG_PATH}"
        )

    dataset = config.get("dataset")
    if dataset is not None and not isinstance(dataset, dict):
        raise ValueError(
            f"'dataset' must be a mapping in {EXPERIMENT_CONFIG_PATH}"
        )

    return config


def _configure_pipeline_args(
    args: Namespace,
    project_root: Path,
    experiment_config: Mapping[str, Any],
) -> None:
    """Supply experiment defaults while preserving explicit CLI overrides."""
    if args.pipeline_config is None:
        configured_path = experiment_config.get("pipeline_config")
        if not configured_path:
            raise ValueError(
                f"'pipeline_config' is required in {EXPERIMENT_CONFIG_PATH}"
            )
        args.pipeline_config = _resolve_path(project_root, configured_path)
    else:
        args.pipeline_config = _resolve_path(project_root, args.pipeline_config)

    if not Path(args.pipeline_config).is_file():
        raise FileNotFoundError(
            f"Pipeline configuration does not exist: {args.pipeline_config}"
        )

    args.project_root = project_root


def _mlflow_value(value: Any) -> str | int | float | bool:
    """Convert nested configuration values into MLflow-safe parameter values."""
    if isinstance(value, (str, int, float, bool)):
        return value

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )


def _flatten_mapping(
    document: Mapping[str, Any],
    *,
    prefix: str = "",
) -> dict[str, str | int | float | bool]:
    """Flatten a nested mapping for MLflow parameter logging."""
    flattened: dict[str, str | int | float | bool] = {}

    for key, value in document.items():
        name = f"{prefix}.{key}" if prefix else str(key)

        if isinstance(value, Mapping):
            flattened.update(_flatten_mapping(value, prefix=name))
        else:
            flattened[name] = _mlflow_value(value)

    return flattened


def _log_config(
    project_root: Path,
    experiment_config: Mapping[str, Any],
    pipeline_config_path: Path,
) -> None:
    """Record experiment metadata and the resolved pipeline configuration."""
    experiment_metadata = experiment_config.get("experiment", {})
    dataset_metadata = experiment_config.get("dataset", {})

    tags = {
        "ariadne.execution_origin": "CLI",
        "ariadne.pipeline": DEFAULT_EXPERIMENT_NAME,
        "ariadne.project_root": str(project_root),
        "ariadne.pipeline_config": str(pipeline_config_path),
    }

    if isinstance(experiment_metadata, Mapping):
        if experiment_metadata.get("id") is not None:
            tags["experiment_id"] = str(experiment_metadata["id"])
        if experiment_metadata.get("theme") is not None:
            tags["theme"] = str(experiment_metadata["theme"])

    if isinstance(dataset_metadata, Mapping):
        if dataset_metadata.get("name") is not None:
            tags["dataset"] = str(dataset_metadata["name"])

    mlflow.set_tags(tags)

    pipeline_document = _read_yaml(pipeline_config_path)
    pipeline_params = _flatten_mapping(pipeline_document, prefix="pipeline_config")

    if pipeline_params:
        mlflow.log_params(pipeline_params)

    mlflow.log_artifact(
        str(EXPERIMENT_CONFIG_PATH),
        artifact_path="configuration",
    )
    mlflow.log_artifact(
        str(pipeline_config_path),
        artifact_path="configuration",
    )


def _metric_name(prefix: str, column: str) -> str:
    """Create a stable MLflow metric name."""
    name = f"{prefix}.{column}"
    return name.replace(" ", "_").replace("/", ".")


def _log_numeric_csv_metrics(csv_path: Path, prefix: str) -> None:
    """Log finite numeric cells from a CSV artifact as step metrics.

    Non-numeric values, NaN and infinity are intentionally omitted.
    """
    with csv_path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)

        for step, row in enumerate(reader):
            for column, raw_value in row.items():
                if column is None or raw_value in (None, ""):
                    continue

                try:
                    value = float(raw_value)
                except (TypeError, ValueError):
                    continue

                if not math.isfinite(value):
                    continue

                mlflow.log_metric(
                    _metric_name(prefix, column),
                    value,
                    step=step,
                )


def _log_stage_outputs(stage_result: Any) -> None:
    """Log one pipeline stage's artifacts and numeric CSV outputs."""
    stage_name = str(stage_result.stage)

    metadata = stage_result.metadata or {}
    output_dir_value = metadata.get("output_dir")

    if output_dir_value:
        output_dir = Path(output_dir_value).expanduser().resolve()
        if output_dir.is_dir():
            mlflow.log_artifacts(
                str(output_dir),
                artifact_path=stage_name,
            )

    for artifact_name, artifact_value in (stage_result.artifacts or {}).items():
        artifact_path = Path(artifact_value).expanduser().resolve()

        if not artifact_path.is_file():
            continue

        # Avoid uploading the same files twice when the complete output
        # directory has already been logged above.
        if not output_dir_value:
            mlflow.log_artifact(
                str(artifact_path),
                artifact_path=stage_name,
            )

        if artifact_path.suffix.lower() == ".csv":
            _log_numeric_csv_metrics(
                artifact_path,
                f"{stage_name}.{artifact_name}",
            )


def _print_result(result: Any) -> None:
    """Print the result using the same conventions as ariadne-pipeline."""
    if result.payload is not None:
        print(json.dumps(result.payload, indent=2, ensure_ascii=False))

    if result.validation is not None:
        print(format_validation(result.validation))

    for stage_result in result.stage_results or []:
        print(f"stage: {stage_result.stage}")
        print(f"status: {stage_result.status}")

        for name, path in (stage_result.artifacts or {}).items():
            print(f"artifact.{name}: {path}")


def _run_without_tracking(args: Namespace, project_root: Path) -> int:
    """Execute dry-run or validation without creating an MLflow run."""
    result = execute(args, project_root)
    _print_result(result)
    return 0 if result.status == "ok" else 1


def _run_with_tracking(
    args: Namespace,
    project_root: Path,
    experiment_config: Mapping[str, Any],
) -> int:
    """Execute the analytical pipeline inside one MLflow run."""
    experiment_metadata = experiment_config.get("experiment", {})

    experiment_name = os.getenv(
        "MLFLOW_EXPERIMENT_NAME",
        DEFAULT_EXPERIMENT_NAME,
    )

    if isinstance(experiment_metadata, Mapping):
        experiment_name = str(
            experiment_metadata.get("mlflow_experiment", experiment_name)
        )

    mlflow.set_experiment(experiment_name)

    with mlflow.start_run() as active_run:
        mlflow_run_id = active_run.info.run_id

        # Compatibility bridge for the current planner API.
        #
        # The desired architecture passes an ExecutionIdentity to execute().
        # The checked-in execute() currently accepts only (args, project_root),
        # while PipelinePlanner resolves identity from argparse.Namespace.
        # No Ariadne database Execution is created by this script.
        args.execution_id = mlflow_run_id
        args.run_id = None

        mlflow.set_tags(
            {
                "ariadne.execution_origin": "CLI",
                "ariadne.mlflow_run_id": mlflow_run_id,
            }
        )

        _log_config(
            project_root,
            experiment_config,
            Path(args.pipeline_config),
        )

        try:
            result = execute(args, project_root)
            _print_result(result)

            mlflow.set_tag("ariadne.pipeline_status", str(result.status))

            for stage_result in result.stage_results or []:
                mlflow.set_tag(
                    f"ariadne.stage.{stage_result.stage}.status",
                    str(stage_result.status),
                )
                _log_stage_outputs(stage_result)

            if result.status != "ok":
                mlflow.set_tag("ariadne.failure_kind", "pipeline_result")
                return 1

            return 0

        except Exception as exc:
            mlflow.set_tags(
                {
                    "ariadne.pipeline_status": "failed",
                    "ariadne.failure_kind": type(exc).__name__,
                    "ariadne.failure_message": str(exc)[:1000],
                }
            )
            raise


def main() -> None:
    """Run the integrated discovery-to-inference experiment."""
    args = parse_args()
    project_root = _resolve_project_root(args)
    experiment_config = _load_experiment_config()

    _configure_pipeline_args(
        args,
        project_root,
        experiment_config,
    )

    # The architecture specifies that planning and validation must not create
    # analytical MLflow runs.
    if args.dry_run or args.validate_only:
        exit_code = _run_without_tracking(args, project_root)
    else:
        exit_code = _run_with_tracking(
            args,
            project_root,
            experiment_config,
        )

    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()