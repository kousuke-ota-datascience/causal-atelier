"""分析単位へ集約するための設定駆動 aggregation helper。"""

from __future__ import annotations

import pandas as pd

from .config import MetricSpec
from .aggregation import get_aggregation


def aggregate_metrics(
    frame: pd.DataFrame,
    group_by: list[str],
    metrics: dict[str, MetricSpec],
    prefix: str,
) -> pd.DataFrame:
    """raw row を分析単位の特徴量列へ集約する。

    Args:
        frame: Source data frame after filtering.
        group_by: Columns used as aggregation keys.
        metrics: Metric specifications keyed by output metric names.
        prefix: Prefix added to output feature columns.

    Returns:
        Aggregated data frame keyed by ``group_by``.

    Raises:
        ValueError: If an aggregation method is unknown.
        KeyError: If a configured input column does not exist.
    """
    grouped = frame.groupby(group_by, observed=True)
    output = pd.DataFrame(index=grouped.size().index)
    for name, metric in metrics.items():
        column_name = f"{prefix}_{name}"
        if metric.agg == "count_rows":
            output[column_name] = grouped.size()
            continue
        if metric.column is None:
            raise ValueError(f"{metric.agg} requires a source column for {column_name}")
        if metric.column not in frame.columns:
            raise KeyError(f"missing aggregation column: {metric.column}")
        series_grouped = grouped[metric.column]
        output[column_name] = get_aggregation(metric.agg)(series_grouped)
    return output.reset_index()
