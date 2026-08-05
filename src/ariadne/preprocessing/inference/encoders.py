"""特徴量設定に従って世帯属性を数値化する encoder 群。"""

from __future__ import annotations

from collections.abc import Collection

import numpy as np
import pandas as pd


def encode_ordinal_map(
    series: pd.Series,
    mapping: dict[str, float],
    unknown_value: float | None = None,
) -> pd.Series:
    """順序カテゴリを設定済みの数値 map で encoding する。

    Args:
        series: Input categorical series.
        mapping: Category-to-number mapping.
        unknown_value: Optional fallback for missing or unknown categories. If
            ``None``, the median of configured mapping values is used.

    Returns:
        Numeric encoded series.
    """
    fallback = float(np.median(list(mapping.values()))) if unknown_value is None else unknown_value
    mapped = series.astype("string").map(mapping).astype("float64")
    return mapped.fillna(fallback)


def encode_numeric_extract(
    series: pd.Series,
    unknown_value: float | None = 0.0,
) -> pd.Series:
    """カテゴリ風の series から数値を抽出する。

    Args:
        series: Input series.
        unknown_value: Fallback value for non-numeric entries.

    Returns:
        Numeric series with missing values filled.
    """
    fallback = 0.0 if unknown_value is None else float(unknown_value)
    return pd.to_numeric(series.astype("string"), errors="coerce").fillna(fallback).astype("float64")


def encode_kids_count(
    series: pd.Series,
    unknown_value: float | None = 0.0,
) -> pd.Series:
    """子ども人数カテゴリを数値に変換する。

    Args:
        series: Input category-like kid-count series.
        unknown_value: Fallback value for unknown values.

    Returns:
        Numeric kid-count series.
    """
    return encode_numeric_extract(series, unknown_value=unknown_value)


def encode_binary_with_unknown(
    series: pd.Series,
    positive_values: Collection[str],
) -> pd.DataFrame:
    """カテゴリ series を positive indicator と unknown indicator に変換する。

    Args:
        series: Input categorical series.
        positive_values: Values treated as positive cases.

    Returns:
        A two-column data frame named ``positive`` and ``unknown``.
    """
    as_string = series.astype("string").fillna("Unknown")
    positive = as_string.isin(set(str(value) for value in positive_values)).astype(float)
    unknown = as_string.eq("Unknown").astype(float)
    return pd.DataFrame({"positive": positive, "unknown": unknown}, index=series.index)


def encode_one_hot(
    series: pd.Series,
    prefix: str,
    *,
    include_unknown: bool = True,
    drop_first: bool = True,
) -> pd.DataFrame:
    """カテゴリ series を one-hot encoding する。

    Args:
        series: Input categorical series.
        prefix: Output column prefix.
        include_unknown: Whether missing values should become ``Unknown``.
        drop_first: Whether to drop the first dummy column.

    Returns:
        One-hot encoded data frame.
    """
    values = series.astype("string")
    if include_unknown:
        values = values.fillna("Unknown")
    encoded = pd.get_dummies(values, prefix=prefix, dtype=float)
    if drop_first and len(encoded.columns) > 0:
        encoded = encoded.drop(columns=[encoded.columns[0]])
    return encoded
