"""入力テーブルの列検証ユーティリティ。"""

from __future__ import annotations

from collections.abc import Collection

import pandas as pd


def validate_required_columns(
    frame: pd.DataFrame,
    required_columns: Collection[str],
    table_name: str,
) -> None:
    """読み込んだテーブルが必須列を含むことを検証する。

    Args:
        frame: 検証対象のデータフレーム。
        required_columns: 必須列名。
        table_name: エラーメッセージで使う論理テーブル名。

    Raises:
        ValueError: 必須列が不足している場合。
    """
    missing = sorted(set(required_columns).difference(frame.columns))
    if missing:
        raise ValueError(f"{table_name} is missing required columns: {missing}")
