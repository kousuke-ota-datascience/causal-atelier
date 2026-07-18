"""探索特徴量生成で使う source table と campaign window の解決。"""

from __future__ import annotations

import pandas as pd

from causal_atelier.preprocessing.common import (
    CampaignWindow,
    select_campaign_window,
    window_bounds as common_window_bounds,
)

from .config import FeatureConfig


def table_frame(
    tables: dict[str, pd.DataFrame],
    feature_config: FeatureConfig,
    logical_name: str,
) -> pd.DataFrame:
    """logical table name から入力テーブルを取り出す。

    Args:
        tables: logical table name、または旧実装互換の registry entry 名を key
            とする入力テーブル。
        feature_config: 探索用特徴量生成設定。
        logical_name: ``features.yaml`` の logical table key。

    Returns:
        対象テーブルのデータフレーム。
    """
    table = feature_config.tables[logical_name]
    if logical_name in tables:
        return tables[logical_name]
    return tables[table.name]


def build_household_index(
    transactions: pd.DataFrame,
    feature_config: FeatureConfig,
) -> pd.Index:
    """分析単位である世帯 ID の index を作る。

    Args:
        transactions: transaction-level データ。
        feature_config: key column を含む特徴量生成設定。

    Returns:
        transaction 出現順を保った一意な世帯 ID index。
    """
    transaction_table = feature_config.tables["transactions"]
    household_column = transaction_table.household_key or feature_config.metadata["entity_id"]
    return pd.Index(
        transactions[household_column].dropna().unique(),
        name=household_column,
    )


def build_campaign_window(
    *,
    campaign_descriptions: pd.DataFrame,
    transactions: pd.DataFrame,
    campaign_id: str,
    feature_config: FeatureConfig,
    pre_weeks: int,
) -> CampaignWindow:
    """キャンペーンの pre-treatment/outcome 週範囲を求める。

    Args:
        campaign_descriptions: キャンペーン日付テーブル。
        transactions: 週範囲を推定する transaction テーブル。
        campaign_id: 分析対象キャンペーン ID。
        feature_config: table column 設定を含む特徴量生成設定。
        pre_weeks: treatment 前として含める週数。

    Returns:
        transaction データの範囲に丸め込んだ campaign window。

    Raises:
        ValueError: 対象キャンペーンが存在しない、または usable な週範囲がない場合。
    """
    campaign_table = feature_config.tables["campaign_descriptions"]
    transaction_table = feature_config.tables["transactions"]
    campaign_id_column = campaign_table.campaign_id or "campaign_id"
    start_column = campaign_table.start_day or "start_date"
    end_column = campaign_table.end_day or "end_date"
    week_column = transaction_table.week or feature_config.metadata["time_column"]
    timestamp_column = transaction_table.transaction_timestamp or "transaction_timestamp"
    divisor = int(
        feature_config.campaign_window.get("day_to_week", {}).get("divisor", 7)
    )

    return select_campaign_window(
        campaign_descriptions=campaign_descriptions,
        transactions=transactions,
        campaign_id=campaign_id,
        campaign_id_column=campaign_id_column,
        start_day_column=start_column,
        end_day_column=end_column,
        week_column=week_column,
        transaction_timestamp_column=timestamp_column,
        pre_weeks=pre_weeks,
        day_to_week_divisor=divisor,
    )


def window_bounds(window: CampaignWindow, name: str) -> tuple[int, int]:
    """名前付き transaction window の週範囲を返す。

    Args:
        window: pre/outcome の週範囲を持つ campaign window。
        name: ``"pre"`` または ``"outcome"``。

    Returns:
        両端を含む ``(start_week, end_week)``。

    Raises:
        ValueError: 未対応の window 名の場合。
    """
    return common_window_bounds(window, name)
