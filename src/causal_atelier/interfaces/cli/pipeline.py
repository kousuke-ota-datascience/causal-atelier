"""Thin facade for the integrated discovery-to-inference CLI."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from causal_atelier.shared.constants import SUPPORTED_DISCOVERY_ALGORITHMS

from causal_atelier.application.end_to_end_pipeline import execute
from causal_atelier.application.strategies import format_validation


def build_parser() -> argparse.ArgumentParser:
    """Build the integrated pipeline parser."""

    parser = argparse.ArgumentParser(
        description="Run causal discovery and causal inference as one reproducible pipeline.",
    )
    parser.add_argument("--project-root", type=Path, default=None)
    parser.add_argument("--pipeline-config", type=Path, default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--random-seed", type=int, default=None)
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true")

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
    project_root = (args.project_root or Path.cwd()).resolve()
    result = execute(args, project_root)

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
