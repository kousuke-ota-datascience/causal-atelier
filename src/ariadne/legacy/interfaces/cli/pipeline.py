"""Thin facade for the integrated discovery-to-inference CLI."""

from __future__ import annotations

import argparse
import json
import logging
import warnings
from collections.abc import Sequence
from pathlib import Path

from ariadne.shared.constants import SUPPORTED_DISCOVERY_ALGORITHMS
from ariadne.shared.identity import cli_identity

from ariadne.application.pipeline.end_to_end import execute
from ariadne.application.pipeline.strategies import format_validation

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Build the integrated pipeline parser."""

    parser = argparse.ArgumentParser(
        description="Run causal discovery and causal inference as one reproducible pipeline.",
    )
    parser.add_argument("--project-root", type=Path, default=None)
    parser.add_argument("--pipeline-config", type=Path, default=None)
    parser.add_argument(
        "--run-label",
        default=None,
        help=(
            "Human-readable label written to the reproducibility manifest. "
            "This is NOT an Ariadne execution_id; CLI runs do not create Ariadne Executions."
        ),
    )
    parser.add_argument(
        "--run-id",
        default=None,
        help="Deprecated alias for --run-label. Will be removed in a future version.",
    )
    parser.add_argument("--random-seed", type=int, default=None)
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true")

    # MLflow tracking options
    parser.add_argument(
        "--mlflow-tracking-uri",
        default=None,
        help="MLflow tracking server URI. Overrides MLFLOW_TRACKING_URI env var.",
    )
    parser.add_argument(
        "--mlflow-experiment",
        default=None,
        help="MLflow experiment name. Overrides MLFLOW_EXPERIMENT_NAME env var.",
    )
    parser.add_argument(
        "--mlflow-run-name",
        default=None,
        help="Human-readable name for the MLflow Run.",
    )
    parser.add_argument(
        "--resume-mlflow-run-id",
        default=None,
        help="Resume an existing MLflow Run by ID instead of creating a new one.",
    )
    parser.add_argument(
        "--disable-mlflow",
        action="store_true",
        default=False,
        help="Disable MLflow tracking. A Null Tracker is used; no pseudo-IDs are generated.",
    )

    parser.add_argument("--dataset-yaml", type=Path, default=None)
    parser.add_argument("--campaign-id", default=None)
    parser.add_argument("--pre-weeks", type=int, default=None)
    parser.add_argument("--collinearity-threshold", type=float, default=None)

    parser.add_argument("--discovery-analysis-config", type=Path, default=None)
    parser.add_argument("--discovery-feature-config", type=Path, default=None)
    parser.add_argument("--discovery-output-dir", type=Path, default=None)
    parser.add_argument(
        "--discovery-algorithms",
        nargs="+",
        choices=SUPPORTED_DISCOVERY_ALGORITHMS,
        default=None,
        help="Discovery algorithms to run. Choices: %(choices)s.",
    )
    parser.add_argument("--discovery-alpha", type=float, default=None)
    parser.add_argument("--discovery-alpha-grid", nargs="+", type=float, default=None)
    parser.add_argument("--discovery-pc-indep-test", default=None)
    parser.add_argument("--discovery-bootstrap-samples", type=int, default=None)
    parser.add_argument("--discovery-bootstrap-sample-fraction", type=float, default=None)
    parser.add_argument("--discovery-random-seed", type=int, default=None)
    parser.add_argument("--discovery-no-background-knowledge", action="store_true", default=False)
    parser.add_argument("--discovery-notears-threshold", type=float, default=None)

    parser.add_argument("--inference-config", type=Path, default=None)
    parser.add_argument("--inference-feature-config", type=Path, default=None)
    parser.add_argument("--inference-output-dir", type=Path, default=None)
    parser.add_argument("--inference-mode", choices=("edge_weight", "treatment_effect"), default=None)
    parser.add_argument("--inference-treatment", default=None)
    parser.add_argument("--inference-outcome", default=None)
    parser.add_argument("--inference-estimand", choices=("ATE", "ATT"), default=None)
    parser.add_argument("--inference-effect-methods", nargs="+", default=None)
    parser.add_argument("--inference-adjustment-strategy", default=None)
    parser.add_argument("--inference-covariates", nargs="+", default=None)
    parser.add_argument("--inference-robust-se", default=None)
    parser.add_argument("--inference-min-samples", type=int, default=None)
    parser.add_argument("--inference-edge-robust-se", default=None)
    return parser


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse integrated CLI arguments."""

    return build_parser().parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    """Run the selected pipeline command strategy."""

    args = parse_args(argv)

    # Warn about deprecated --run-id
    if args.run_id is not None:
        warnings.warn(
            "--run-id is deprecated and will be removed in a future release. "
            "Use --run-label for a human-readable label, or --resume-mlflow-run-id "
            "to resume an MLflow Run.",
            DeprecationWarning,
            stacklevel=2,
        )
        if args.run_label is None:
            args.run_label = args.run_id

    # Bootstrap MLflow tracking for CLI runs
    mlflow_run_id: str | None = None
    tracker = None

    if not args.disable_mlflow and not args.dry_run and not args.validate_only:
        try:
            from ariadne.infrastructure.tracking.settings import TrackingSettings
            from ariadne.infrastructure.tracking.mlflow_tracker import MlflowTracker
            from ariadne.infrastructure.tracking.exceptions import TrackingError

            ts = TrackingSettings.from_env(
                tracking_uri=args.mlflow_tracking_uri,
                experiment_name=args.mlflow_experiment,
            )
            if ts.enabled:
                tracker = MlflowTracker(ts)
                if args.resume_mlflow_run_id:
                    mlflow_run_id = args.resume_mlflow_run_id
                    logger.info("Resuming MLflow Run: %s", mlflow_run_id)
                else:
                    ref = tracker.create_or_resume_run(
                        experiment_name=ts.experiment_name,
                        tags={
                            "ariadne.execution_origin": "CLI",
                        },
                        run_name=args.mlflow_run_name or args.run_label,
                        execution_id=args.run_label or "cli",
                    )
                    mlflow_run_id = ref.run_id
                    logger.info("MLflow Run started: %s", mlflow_run_id)
        except Exception as exc:
            logger.warning("MLflow bootstrap failed, continuing without tracking: %s", exc)
            tracker = None
            mlflow_run_id = None

    identity = cli_identity(mlflow_run_id=mlflow_run_id)
    project_root = (args.project_root or Path.cwd()).resolve()

    result = execute(args, project_root)

    # Terminate MLflow Run based on result status
    if tracker is not None and mlflow_run_id is not None:
        try:
            from ariadne.infrastructure.tracking.exceptions import TrackingError
            mlflow_terminal = "FINISHED" if result.status == "ok" else "FAILED"
            tracker.terminate_run(mlflow_run_id, mlflow_terminal)
        except Exception as exc:
            logger.warning("Failed to terminate MLflow Run %s: %s", mlflow_run_id, exc)

    if result.payload is not None:
        print(json.dumps(result.payload, indent=2, ensure_ascii=False))
    if result.validation is not None:
        print(format_validation(result.validation))
    if result.stage_results is not None:
        for stage_result in result.stage_results:
            print(f"stage: {stage_result.stage}")
            print(f"status: {stage_result.status}")
            for name, path in stage_result.artifacts.items():
                print(f"artifact.{name}: {path}")
    if result.status != "ok":
        raise SystemExit(1)


__all__ = ["build_parser", "main", "parse_args"]
