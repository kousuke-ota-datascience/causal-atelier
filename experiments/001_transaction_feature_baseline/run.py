"""Build the baseline discovery feature table without running discovery."""

from __future__ import annotations

from pathlib import Path

from ariadne.causal.discovery.config import load_analysis_config
from ariadne.etl.registry import LogicalTableDataLoader
from ariadne.infrastructure.config.datasets import find_project_root
from ariadne.preprocessing.discovery.builder import CompleteJourneyPreprocessor
from ariadne.preprocessing.discovery.config import load_feature_config


def main() -> None:
    project_root = find_project_root(Path.cwd())
    analysis_config = load_analysis_config(project_root / "configs/causal/discovery.yaml")
    feature_config = load_feature_config(
        project_root / "configs/preprocessing/discovery_features.yaml"
    )
    loader = LogicalTableDataLoader(
        project_root=project_root,
        dataset_yaml=project_root / "configs/etl/completejourney/load.yaml",
        table_specs=feature_config.tables,
        logger_name="experiment_001_transaction_feature_baseline",
    )
    result = CompleteJourneyPreprocessor(
        tables=loader.load_all(),
        campaign_id=analysis_config.run.campaign_id,
        pre_weeks=analysis_config.run.pre_weeks,
        collinearity_threshold=analysis_config.preprocessing.collinearity_threshold,
        feature_config=feature_config,
    ).preprocess()

    output_dir = project_root / "artifacts/experiments/001_transaction_feature_baseline"
    output_dir.mkdir(parents=True, exist_ok=True)
    result.discovery_frame.to_parquet(output_dir / "discovery_features.parquet")
    result.variable_metadata.to_csv(output_dir / "variable_metadata.csv", index=False)


if __name__ == "__main__":
    main()
