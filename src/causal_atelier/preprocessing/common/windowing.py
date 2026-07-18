"""Stage-independent windowing and numeric feature utilities."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class CampaignWindow:
    """Analysis week ranges for a single campaign."""

    campaign_id: str
    start_week: int
    end_week: int
    pre_start_week: int
    pre_end_week: int


def select_campaign_window(
    *,
    campaign_descriptions: pd.DataFrame,
    transactions: pd.DataFrame,
    campaign_id: str,
    campaign_id_column: str,
    start_day_column: str,
    end_day_column: str,
    week_column: str,
    transaction_timestamp_column: str,
    pre_weeks: int,
    day_to_week_divisor: int = 7,
) -> CampaignWindow:
    """Select pre-treatment and outcome windows from campaign metadata."""

    first_transaction_date = pd.to_datetime(
        transactions[transaction_timestamp_column],
        unit="s",
    ).min()
    first_transaction_date = first_transaction_date.normalize()

    campaigns = campaign_descriptions.copy()
    campaigns["start_dt"] = pd.to_datetime(
        campaigns[start_day_column],
        unit="D",
        origin="unix",
    )
    campaigns["end_dt"] = pd.to_datetime(
        campaigns[end_day_column],
        unit="D",
        origin="unix",
    )
    campaigns["start_week"] = (
        (campaigns["start_dt"] - first_transaction_date).dt.days // day_to_week_divisor
        + 1
    ).astype(int)
    campaigns["end_week"] = (
        (campaigns["end_dt"] - first_transaction_date).dt.days // day_to_week_divisor
        + 1
    ).astype(int)

    matched = campaigns.loc[campaigns[campaign_id_column].astype(str).eq(str(campaign_id))]
    if matched.empty:
        raise ValueError(f"unknown campaign_id: {campaign_id}")

    campaign = matched.iloc[0]
    min_week = int(transactions[week_column].min())
    max_week = int(transactions[week_column].max())
    start_week = max(int(campaign["start_week"]), min_week)
    end_week = min(int(campaign["end_week"]), max_week)
    pre_end_week = start_week - 1
    pre_start_week = max(min_week, start_week - pre_weeks)

    if pre_start_week > pre_end_week:
        raise ValueError(f"campaign {campaign_id} has no pre-treatment weeks in transactions.")
    if start_week > end_week:
        raise ValueError(f"campaign {campaign_id} has no outcome weeks in transactions.")

    return CampaignWindow(
        campaign_id=str(campaign_id),
        start_week=start_week,
        end_week=end_week,
        pre_start_week=pre_start_week,
        pre_end_week=pre_end_week,
    )


def window_bounds(window: CampaignWindow, name: str) -> tuple[int, int]:
    """Return inclusive bounds for a named window."""

    if name == "pre":
        return window.pre_start_week, window.pre_end_week
    if name == "outcome":
        return window.start_week, window.end_week
    raise ValueError(f"unsupported transaction window: {name}")


def drop_collinear_columns(
    frame: pd.DataFrame,
    *,
    collinearity_threshold: float,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Drop columns that are collinear with earlier columns."""

    if frame.empty:
        return frame, pd.DataFrame(columns=["column", "reason"])

    corr = frame.corr().abs()
    upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
    records = []
    for column in upper.columns:
        correlated_with = upper.index[upper[column] >= collinearity_threshold].tolist()
        if correlated_with:
            records.append(
                {
                    "column": column,
                    "reason": f"collinear_with:{correlated_with[0]}",
                }
            )

    columns_to_drop = [record["column"] for record in records]
    return frame.drop(columns=columns_to_drop), pd.DataFrame(records)


__all__ = [
    "CampaignWindow",
    "drop_collinear_columns",
    "select_campaign_window",
    "window_bounds",
]
