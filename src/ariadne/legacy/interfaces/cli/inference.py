"""因果推論パイプラインの command-line interface。"""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from ariadne.infrastructure.config import load_yaml_mapping

from ariadne.etl.registry import LogicalTableDataLoader
from ariadne.infrastructure.config.datasets import find_project_root

from ariadne.causal.inference.config import (
    load_pipeline_config,
    merge_cli_overrides,
    resolve_project_path,
    write_resolved_configs,
)
from ariadne.causal.inference.constants import (
    DEFAULT_CONFIG_PATH,
    SUPPORTED_ADJUSTMENT_STRATEGIES,
    SUPPORTED_ALGORITHMS,
    SUPPORTED_EFFECT_METHODS,
    SUPPORTED_ESTIMANDS,
    SUPPORTED_MODES,
    SUPPORTED_ROBUST_SE,
)
from ariadne.causal.inference.context import RunContext
from ariadne.causal.inference.modes.registry import MODE_STRATEGY_BY_NAME
from ariadne.preprocessing.inference.builder import FeatureBuilder
from ariadne.preprocessing.inference.config import load_feature_config


def build_parser() -> argparse.ArgumentParser:
    """因果推論 workflow 用の CLI parser を構築する。

    Returns:
        Configured argument parser. Non-``None`` parsed values override the
        YAML configuration.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Estimate causal-discovery edge weights or explicit treatment effects "
            "for completejourney."
        ),
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help=f"Pipeline YAML. Defaults to {DEFAULT_CONFIG_PATH} when present.",
    )
    parser.add_argument("--feature-config", type=Path, default=None)
    parser.add_argument("--mode", choices=SUPPORTED_MODES, default=None)
    parser.add_argument("--project-root", type=Path, default=None)
    parser.add_argument("--dataset-yaml", type=Path, default=None)
    parser.add_argument("--campaign-id", default=None)
    parser.add_argument("--pre-weeks", type=int, default=None)
    parser.add_argument("--collinearity-threshold", type=float, default=None)
    parser.add_argument("--discovery-manifest", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument(
        "--algorithms",
        nargs="+",
        default=None,
        choices=SUPPORTED_ALGORITHMS,
    )
    parser.add_argument(
        "--edge-robust-se",
        choices=SUPPORTED_ROBUST_SE,
        default=None,
        help="Robust SE type for edge-weight regressions.",
    )
    parser.add_argument("--min-samples", type=int, default=None)
    parser.add_argument("--treatment", default=None)
    parser.add_argument("--outcome", default=None)
    parser.add_argument("--estimand", choices=SUPPORTED_ESTIMANDS, default=None)
    parser.add_argument(
        "--adjustment-strategy",
        choices=SUPPORTED_ADJUSTMENT_STRATEGIES,
        default=None,
    )
    parser.add_argument("--covariates", nargs="*", default=None)
    parser.add_argument(
        "--effect-methods",
        nargs="+",
        choices=SUPPORTED_EFFECT_METHODS,
        default=None,
    )
    parser.add_argument(
        "--robust-se",
        choices=SUPPORTED_ROBUST_SE,
        default=None,
        help="Robust SE type for treatment-effect OLS.",
    )
    return parser


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """CLI 引数を解釈する。

    Args:
        argv: Optional command-line arguments. If ``None``, arguments are read
            from ``sys.argv``.

    Returns:
        Parsed command-line namespace.
    """
    return build_parser().parse_args(argv)


def resolve_config_path(path: Path | None, project_root: Path) -> Path | None:
    """指定または既定の pipeline 設定パスを解決する。

    Args:
        path: User-supplied config path.
        project_root: Repository root.

    Returns:
        Existing resolved path, or ``None`` when no config file is available.
    """
    candidate = path if path is not None else DEFAULT_CONFIG_PATH
    resolved = candidate if candidate.is_absolute() else project_root / candidate
    return resolved if resolved.exists() else None


def main(argv: Sequence[str] | None = None) -> None:
    """CLI 引数に基づいて因果推論パイプラインを実行する。

    Args:
        argv: Optional command-line arguments. If ``None``, arguments are read
            from ``sys.argv``.

    Raises:
        ValueError: If the resolved configuration is invalid.
        FileNotFoundError: If required input files do not exist.
    """
    args = parse_args(argv)
    project_root = (
        args.project_root.resolve()
        if args.project_root is not None
        else find_project_root(Path.cwd())
    )
    config_path = resolve_config_path(args.config, project_root)
    config = merge_cli_overrides(load_pipeline_config(config_path), args)

    dataset_yaml = resolve_project_path(config.data.dataset_yaml, project_root)
    discovery_manifest = resolve_project_path(config.data.discovery_manifest, project_root)
    discovery_dir = resolve_discovery_dir_from_manifest(discovery_manifest)
    output_dir = resolve_project_path(config.data.output_dir, project_root)
    feature_config_path = resolve_project_path(config.feature_config_path, project_root)
    feature_config = load_feature_config(feature_config_path)

    data_loader = LogicalTableDataLoader(
        project_root=project_root,
        dataset_yaml=dataset_yaml,
        table_specs=feature_config.tables,
        logger_name="causal_inference_completejourney",
        log_path=Path.cwd() / "causal_inference_completejourney.log",
    )
    tables = data_loader.load_all()

    preprocessing_result = FeatureBuilder(feature_config).build(
        tables=tables,
        campaign_id=config.data.campaign_id,
        pre_weeks=config.data.pre_weeks,
        collinearity_threshold=config.data.collinearity_threshold,
    )
    resolved_config = config.__class__.from_mapping(
        {
            **config.to_dict(),
            "data": {
                **config.data.to_dict(),
                "dataset_yaml": str(dataset_yaml),
                "discovery_manifest": str(discovery_manifest),
                "output_dir": str(output_dir),
            },
            "feature_config_path": str(feature_config_path),
        }
    )

    if config.report.write_config_snapshot:
        write_resolved_configs(
            output_dir=output_dir,
            pipeline_config=resolved_config,
            feature_config_data=feature_config.to_dict(),
        )

    context = RunContext(
        config=resolved_config,
        feature_config=feature_config,
        project_root=project_root,
        dataset_yaml=dataset_yaml,
        discovery_dir=discovery_dir,
        output_dir=output_dir,
        preprocessing_result=preprocessing_result,
    )
    strategy = MODE_STRATEGY_BY_NAME[config.mode]()
    strategy.run(context)


def resolve_discovery_dir_from_manifest(manifest_path: Path) -> Path:
    """Resolve the discovery artifact directory from a stage manifest.

    Args:
        manifest_path: Discovery manifest path.

    Returns:
        Absolute or manifest-declared discovery output directory.

    Raises:
        FileNotFoundError: If the manifest is missing.
        ValueError: If the manifest schema is insufficient.
    """
    if not manifest_path.exists():
        raise FileNotFoundError(f"missing discovery manifest: {manifest_path}")
    manifest = load_yaml_mapping(manifest_path)
    output_dir = manifest.get("resolved_output_dir")
    if output_dir is None:
        raise ValueError(f"discovery manifest is missing resolved_output_dir: {manifest_path}")
    return Path(str(output_dir))
