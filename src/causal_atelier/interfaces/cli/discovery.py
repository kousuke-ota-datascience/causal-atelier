from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from causal_atelier.etl.registry import LogicalTableDataLoader
from causal_atelier.infrastructure.config.datasets import find_project_root

from causal_atelier.causal.discovery.config import (
    load_analysis_config,
    merge_cli_overrides,
    resolve_project_path,
    write_resolved_config,
)
from causal_atelier.causal.discovery.constants import (
    ALLOWED_ALGORITHMS,
    DEFAULT_ALPHA_GRID,
    DEFAULT_ANALYSIS_CONFIG,
    DEFAULT_FEATURE_CONFIG,
    DEFAULT_PC_INDEP_TESTS,
)
from causal_atelier.causal.discovery.algorithms import CausalDiscovery
from causal_atelier.causal.discovery.diagnostics import CausalDiscoveryDiagnostics
from causal_atelier.causal.discovery.reporting import CausalDiscoveryReporter
from causal_atelier.preprocessing.discovery.builder import CompleteJourneyPreprocessor
from causal_atelier.preprocessing.discovery.config import load_feature_config


def build_parser() -> argparse.ArgumentParser:
    """因果探索 workflow 用の CLI parser を構築する。

    Returns:
        YAML analysis 設定を上書きする引数を解釈する parser。
    """
    parser = argparse.ArgumentParser(
        description="Discover causal graph structure in completejourney with causal-learn PC.",
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
    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """CLI 引数を解釈する。

    Args:
        argv: 任意の引数列。``None`` の場合は ``sys.argv`` を読む。

    Returns:
        解釈済み namespace。
    """
    return build_parser().parse_args(argv)


def resolve_config_path(path: Path, project_root: Path) -> Path:
    """設定ファイルパスを project root から解決する。

    Args:
        path: ユーザー指定または既定の設定ファイルパス。
        project_root: project-relative default の基準になる repository root。

    Returns:
        project root 配下に存在する場合はその絶対パス。存在しなければ
        current working directory から解決したパス。
    """
    if path.is_absolute():
        return path
    project_candidate = project_root / path
    if project_candidate.exists():
        return project_candidate
    return path.resolve()


def main(argv: list[str] | None = None) -> None:
    """因果探索 workflow 全体を実行する。

    YAML 設定を読み込み、CLI 上書きを適用し、source table を読み込む。
    その後、世帯単位の探索特徴量を構築し、指定された探索アルゴリズムを実行し、
    再現性用の設定 snapshot と診断・レポートを artifacts に書き出す。

    Args:
        argv: programmatic 実行用の任意の CLI 引数列。
    """
    args = parse_args(argv)
    project_root = (
        args.project_root.resolve()
        if args.project_root is not None
        else find_project_root(Path.cwd())
    )
    if args.dataset_yaml is not None:
        args.dataset_yaml = args.dataset_yaml.resolve()
    if args.output_dir is not None:
        args.output_dir = args.output_dir.resolve()

    analysis_config_path = resolve_config_path(args.analysis_config, project_root)
    feature_config_path = resolve_config_path(args.feature_config, project_root)
    analysis_config = load_analysis_config(analysis_config_path)
    feature_config = load_feature_config(feature_config_path)
    analysis_config = merge_cli_overrides(analysis_config, args)

    dataset_yaml = resolve_project_path(analysis_config.dataset.yaml_path, project_root)
    output_dir = resolve_project_path(analysis_config.run.output_dir, project_root)

    data_loader = LogicalTableDataLoader(
        project_root=project_root,
        dataset_yaml=dataset_yaml,
        table_specs=feature_config.tables,
        logger_name="causal_discovery",
    )
    tables = data_loader.load_all()

    preprocessor = CompleteJourneyPreprocessor(
        tables=tables,
        campaign_id=analysis_config.run.campaign_id,
        pre_weeks=analysis_config.run.pre_weeks,
        collinearity_threshold=analysis_config.preprocessing.collinearity_threshold,
        feature_config=feature_config,
    )
    preprocessing_result = preprocessor.preprocess()

    causal_discovery = CausalDiscovery(
        alpha=analysis_config.discovery.pc.alpha,
        use_background_knowledge=analysis_config.discovery.use_background_knowledge,
        algorithms=analysis_config.discovery.algorithms,
        notears_threshold=analysis_config.discovery.notears.threshold,
        pc_indep_test=analysis_config.discovery.pc.indep_test,
        allowed_pc_indep_tests=analysis_config.discovery.pc.allowed_indep_tests,
        discrete_pc_indep_tests=analysis_config.discovery.pc.discrete_indep_tests,
        alpha_grid=analysis_config.discovery.pc.alpha_grid,
        bootstrap_samples=analysis_config.diagnostics.bootstrap.samples,
        bootstrap_sample_fraction=analysis_config.diagnostics.bootstrap.sample_fraction,
        random_seed=analysis_config.run.random_seed,
        pc_discrete_bins=analysis_config.discovery.pc.discrete_bins,
        feature_config=feature_config,
    )
    discovery_results = causal_discovery.run_all(preprocessing_result.standardized)

    write_resolved_config(
        analysis_config=analysis_config,
        feature_config=feature_config,
        output_dir=output_dir,
    )

    retained_columns = list(preprocessing_result.standardized.columns)
    reporter = CausalDiscoveryReporter(
        reporting_config=analysis_config.reporting,
        diagnostics=CausalDiscoveryDiagnostics(causal_discovery),
    )
    reporter.write_outputs(
        results=discovery_results,
        raw_discovery_frame=preprocessing_result.raw_discovery_frame.loc[:, retained_columns],
        discovery_frame=preprocessing_result.discovery_frame.loc[:, retained_columns],
        standardized_frame=preprocessing_result.standardized,
        variable_metadata=preprocessing_result.variable_metadata,
        output_dir=output_dir,
        collinearity_threshold=analysis_config.preprocessing.collinearity_threshold,
        campaign_id=analysis_config.run.campaign_id,
        pre_weeks=analysis_config.run.pre_weeks,
    )
    summary = pd.DataFrame(
        {
            "algorithm": result.algorithm,
            "status": result.status,
            "edges": len(result.edges),
            "message": result.message,
        }
        for result in discovery_results.values()
    )

    print(f"samples: {len(preprocessing_result.discovery_frame):,}")
    print(f"variables: {len(preprocessing_result.standardized.columns):,}")
    print(f"pc_indep_test: {analysis_config.discovery.pc.indep_test}")
    print(f"bootstrap_samples: {analysis_config.diagnostics.bootstrap.samples:,}")
    print(f"output_dir: {output_dir}")
    print(summary.to_string(index=False))
