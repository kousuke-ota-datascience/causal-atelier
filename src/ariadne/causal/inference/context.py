"""pipeline mode 間で共有する run-time context。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .config import PipelineConfig
from ariadne.preprocessing.inference.builder import FeatureBuildResult
from ariadne.preprocessing.inference.config import FeatureConfig


@dataclass(frozen=True)
class RunContext:
    """実行可能な analysis mode が必要とする解決済み object 群。

    Attributes:
        config: Resolved pipeline configuration.
        feature_config: Resolved feature construction configuration.
        project_root: Repository root.
        dataset_yaml: Resolved dataset registry YAML path.
        discovery_dir: Resolved causal discovery output directory.
        output_dir: Resolved causal inference output directory.
        preprocessing_result: Household-level features and standardized frame.
    """

    config: PipelineConfig
    feature_config: FeatureConfig
    project_root: Path
    dataset_yaml: Path
    discovery_dir: Path
    output_dir: Path
    preprocessing_result: FeatureBuildResult

    @property
    def inference_frame(self) -> pd.DataFrame:
        """未標準化の数値 analysis frame を返す。

        Returns:
            Data frame on the original scale.
        """
        return self.preprocessing_result.inference_frame

    @property
    def standardized_frame(self) -> pd.DataFrame:
        """edge-weight 推定用の標準化済み frame を返す。

        Returns:
            Z-scored data frame after dropping non-estimable columns.
        """
        return self.preprocessing_result.standardized
