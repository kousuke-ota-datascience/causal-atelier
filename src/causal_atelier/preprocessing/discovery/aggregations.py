"""transaction-level データを探索用の世帯単位特徴量へ集約する処理。"""

from __future__ import annotations

import pandas as pd

from causal_atelier.preprocessing.common import CampaignWindow

from .config import FeatureConfig
from .tables import window_bounds


def aggregate_series(
    transactions: pd.DataFrame,
    *,
    household_column: str,
    source_column: str,
    aggregation: str,
) -> pd.Series:
    """transaction 列を世帯単位へ集約する。

    Args:
        transactions: Window-filtered transaction data.
        household_column: Household identifier column.
        source_column: Source column to aggregate.
        aggregation: Supported aggregation name.

    Returns:
        Household-indexed aggregated series.

    Raises:
        ValueError: If ``aggregation`` is unsupported.
    """
    grouped = transactions.groupby(household_column, observed=True)[source_column]
    if aggregation == "sum":
        return grouped.sum()
    if aggregation == "nunique":
        return grouped.nunique()
    if aggregation == "mean":
        return grouped.mean()
    if aggregation == "count":
        return grouped.count()
    raise ValueError(f"unsupported aggregation: {aggregation}")


def build_transaction_features(
    transactions: pd.DataFrame,
    households: pd.Index,
    window: CampaignWindow,
    feature_config: FeatureConfig,
) -> pd.DataFrame:
    """設定済みの pre-period/outcome transaction features を作る。

    Args:
        transactions: Transaction source table.
        households: Modeling-unit index.
        window: Campaign window defining pre and outcome periods.
        feature_config: Feature-generation configuration.

    Returns:
        Transaction feature frame indexed by household.

    Raises:
        ValueError: If a transaction feature lacks window or aggregation.
    """
    transaction_table = feature_config.tables["transactions"]
    household_column = transaction_table.household_key or feature_config.metadata["entity_id"]
    week_column = transaction_table.week or feature_config.metadata["time_column"]

    frame = pd.DataFrame(index=households)
    for spec in feature_config.features_for_source_table("transactions"):
        if spec.window is None or spec.aggregation is None:
            raise ValueError(f"transaction feature requires window and aggregation: {spec.name}")

        start_week, end_week = window_bounds(window, spec.window)
        window_frame = transactions.loc[
            transactions[week_column].between(start_week, end_week),
            [household_column, spec.source_column],
        ]
        values = aggregate_series(
            window_frame,
            household_column=household_column,
            source_column=spec.source_column,
            aggregation=spec.aggregation,
        )
        fill_value = 0.0 if spec.fill_value is None else spec.fill_value
        frame[spec.name] = values.reindex(households).fillna(fill_value).astype("float64")

    return frame
