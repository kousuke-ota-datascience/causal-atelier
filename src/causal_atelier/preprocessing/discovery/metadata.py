"""探索結果の解釈と reporting に使う feature metadata を構築する処理。"""

from __future__ import annotations

import pandas as pd

from .config import FeatureConfig


def build_variable_metadata(
    feature_config: FeatureConfig,
    columns: list[str],
    retained_columns: list[str],
    transform_by_column: dict[str, str],
) -> pd.DataFrame:
    """特徴量設定から variable metadata を作る。

    Args:
        feature_config: Feature-generation configuration.
        columns: Discovery-frame columns before standardization filtering.
        retained_columns: Columns retained after standardization and
            collinearity filtering.
        transform_by_column: Actual transforms applied during preprocessing.

    Returns:
        Variable metadata data frame for reporting and diagnostics.
    """
    retained = set(retained_columns)
    spec_by_name = feature_config.feature_by_name()
    records = []

    for column in columns:
        spec = spec_by_name[column]
        records.append(
            {
                "variable": column,
                "role": spec.role,
                "data_type": spec.data_type,
                "transform": transform_by_column.get(column, spec.transform),
                "background_tier": spec.background_tier,
                "used_in_discovery": spec.used_in_discovery and column in retained,
                "fisherz_caution": spec.fisherz_caution,
                "source_table": spec.source_table,
                "source_column": spec.source_column,
                "window": spec.window,
                "aggregation": spec.aggregation,
            }
        )

    return pd.DataFrame(records)
