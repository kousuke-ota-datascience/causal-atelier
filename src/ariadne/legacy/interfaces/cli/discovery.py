"""Thin CLI adapter for causal discovery.

Responsibilities:
- Build the argument parser and parse CLI arguments.
- Convert parsed arguments to a DiscoveryRequest.
- Obtain a DiscoveryApplicationService from the composition root.
- Execute the service.
- Print a summary to stdout.
- Return an exit code.

This module must NOT import pandas, LogicalTableDataLoader,
CompleteJourneyPreprocessor, or CausalDiscoveryReporter directly.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ariadne.application.discovery.dto import DiscoveryExecutionResult
from ariadne.application.discovery.factory import (
    build_discovery_application_service,
    build_discovery_request,
)
from ariadne.causal.discovery.constants import (
    ALLOWED_ALGORITHMS,
    DEFAULT_ALPHA_GRID,
    DEFAULT_ANALYSIS_CONFIG,
    DEFAULT_FEATURE_CONFIG,
    DEFAULT_PC_INDEP_TESTS,
)
from ariadne.infrastructure.config.datasets import find_project_root


def build_parser() -> argparse.ArgumentParser:
    """因果探索 workflow 用の CLI parser を構築する。

    Returns:
        YAML analysis 設定を上書きする引数を解釈する parser。
    """
    parser = argparse.ArgumentParser(
        description=(
            "Discover causal graph structure with causal-learn algorithms. "
            "Supports completejourney and single_table input providers."
        ),
    )
    parser.add_argument("--project-root", type=Path, default=None)
    parser.add_argument(
        "--analysis-config",
        type=Path,
        default=DEFAULT_ANALYSIS_CONFIG,
        help=f"Analysis YAML. Defaults to {DEFAULT_ANALYSIS_CONFIG}.",
    )
    parser.add_argument(
        "--feature-config",
        type=Path,
        default=DEFAULT_FEATURE_CONFIG,
        help=f"Feature YAML. Defaults to {DEFAULT_FEATURE_CONFIG}.",
    )
    parser.add_argument("--dataset-yaml", type=Path, default=None)
    parser.add_argument("--campaign-id", default=None)
    parser.add_argument("--pre-weeks", type=int, default=None)
    parser.add_argument("--alpha", type=float, default=None)
    parser.add_argument(
        "--pc-indep-test",
        choices=DEFAULT_PC_INDEP_TESTS,
        default=None,
        help="Conditional-independence test for PC. fisherz is a linear-Gaussian approximation; gsq/chisq discretize continuous variables first.",
    )
    parser.add_argument(
        "--alpha-grid",
        nargs="+",
        type=float,
        default=None,
        help=f"Alpha values for PC sensitivity analysis. YAML default is {list(DEFAULT_ALPHA_GRID)}.",
    )
    parser.add_argument("--bootstrap-samples", type=int, default=None)
    parser.add_argument("--bootstrap-sample-fraction", type=float, default=None)
    parser.add_argument("--random-seed", type=int, default=None)
    parser.add_argument("--pc-discrete-bins", type=int, default=None)
    parser.add_argument("--collinearity-threshold", type=float, default=None)
    parser.add_argument(
        "--no-background-knowledge",
        action="store_true",
        default=None,
        help="Run PC without temporal tier constraints.",
    )
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument(
        "--algorithms",
        nargs="+",
        default=None,
        choices=ALLOWED_ALGORITHMS,
    )
    parser.add_argument("--notears-threshold", type=float, default=None)
    parser.add_argument(
        "--input-provider",
        default=None,
        help=(
            "Input provider type. Defaults to 'completejourney'. "
            "Use 'single_table' for a single analysis-ready CSV/Parquet file."
        ),
    )
    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """CLI 引数を解釈する。

    Args:
        argv: 任意の引数列。``None`` の場合は ``sys.argv`` を読む。

    Returns:
        解釈済み namespace。
    """
    return build_parser().parse_args(argv)


def print_discovery_summary(result: DiscoveryExecutionResult) -> None:
    """Discovery 実行結果のサマリーを stdout に出力する。

    Args:
        result: DiscoveryApplicationService.execute() の返り値。
    """
    import pandas as pd

    print(f"samples: {result.sample_count:,}")
    print(f"variables: {result.variable_count:,}")
    print(f"pc_indep_test: {result.analysis_config.discovery.pc.indep_test}")
    print(f"bootstrap_samples: {result.analysis_config.diagnostics.bootstrap.samples:,}")
    print(f"output_dir: {result.output_dir}")

    summary = pd.DataFrame(
        {
            "algorithm": r.algorithm,
            "status": r.status,
            "edges": len(r.edges),
            "message": r.message,
        }
        for r in result.algorithm_results.values()
    )
    print(summary.to_string(index=False))


def main(argv: list[str] | None = None) -> int:
    """因果探索 workflow 全体を実行する。

    Args:
        argv: programmatic 実行用の任意の CLI 引数列。

    Returns:
        Exit code (0 on success).
    """
    args = parse_args(argv)
    project_root = (
        args.project_root.resolve()
        if args.project_root is not None
        else find_project_root(Path.cwd())
    )
    request = build_discovery_request(args, project_root)
    service = build_discovery_application_service(project_root)
    result = service.execute(request)
    print_discovery_summary(result)
    return 0

