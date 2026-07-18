"""探索特徴量の型変換と数値化処理。"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from .config import FeatureConfig, FeatureSpec


LOG_TRANSFORMS = {"log1p", "signed_log1p"}


def unknown_mask(series: pd.Series, unknown_values: tuple[Any, ...]) -> pd.Series:
    """欠損値または設定上の unknown 値を示す boolean mask を作る。

    Args:
        series: Source values.
        unknown_values: Values that should be treated as unknown. ``None``
            matches missing values.

    Returns:
        Boolean series where missing or unknown values are ``True``.
    """
    mask = series.isna()
    non_null_unknowns = [value for value in unknown_values if value is not None]
    if non_null_unknowns:
        mask = mask | series.astype("string").isin(non_null_unknowns)
    return mask


def apply_feature_transform(
    series: pd.Series,
    spec: FeatureSpec,
    feature_config: FeatureConfig,
) -> pd.Series:
    """allowlist された特徴量変換を適用する。

    Args:
        series: Source or aggregated values.
        spec: Feature specification selecting the transform.
        feature_config: Full feature configuration for mapping lookups.

    Returns:
        Numeric series ready for discovery input.

    Raises:
        ValueError: If a transform is unsupported or receives invalid values.
    """
    transform = spec.transform

    if transform == "identity":
        return pd.to_numeric(series, errors="coerce").astype("float64")

    if transform == "ordered_category_midpoint":
        if spec.mapping is None:
            raise ValueError(f"ordered_category_midpoint requires mapping: {spec.name}")
        mapping = feature_config.categorical_mappings[spec.mapping]
        mapped = series.astype("string").map(mapping.midpoint_map()).astype("float64")
        return mapped.fillna(mapping.median_midpoint())

    if transform == "numeric_category":
        return pd.to_numeric(series.astype("string"), errors="coerce").fillna(0.0).astype("float64")

    if transform == "equals":
        return series.astype("string").fillna("").eq(str(spec.value)).astype("float64")

    if transform == "is_missing_or_unknown":
        values = spec.unknown_values
        if not values and spec.mapping is not None:
            values = feature_config.categorical_mappings[spec.mapping].unknown_values
        return unknown_mask(series, values).astype("float64")

    if transform == "campaign_membership":
        return series.astype("float64")

    values = pd.to_numeric(series, errors="coerce").fillna(0.0).astype("float64")
    if transform == "log1p":
        if (values < 0).any():
            raise ValueError(f"column must be non-negative before log1p: {spec.name}")
        return np.log1p(values)
    if transform == "signed_log1p":
        return np.sign(values) * np.log1p(np.abs(values))

    raise ValueError(f"unsupported transform: {transform}")


def apply_configured_transforms(
    raw_frame: pd.DataFrame,
    feature_config: FeatureConfig,
) -> tuple[pd.DataFrame, dict[str, str]]:
    """探索特徴量に設定された集約後変換を適用する。

    Args:
        raw_frame: Raw household-level discovery feature frame.
        feature_config: Feature-generation configuration.

    Returns:
        Pair of transformed frame and mapping from transformed column name to
        transform name.
    """
    transformed = raw_frame.copy()
    transform_by_column: dict[str, str] = {}
    spec_by_name = feature_config.feature_by_name()

    for column in transformed.columns:
        spec = spec_by_name[column]
        if spec.transform not in LOG_TRANSFORMS:
            continue
        transformed[column] = apply_feature_transform(
            transformed[column],
            spec,
            feature_config,
        )
        transform_by_column[column] = spec.transform

    return transformed, transform_by_column
