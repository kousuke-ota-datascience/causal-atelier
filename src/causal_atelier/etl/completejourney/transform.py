"""Normalize extracted Complete Journey tables before persistence."""

from __future__ import annotations

from collections.abc import Mapping

import pandas as pd


def normalize_tables(tables: Mapping[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Return table copies with normalized string column names."""

    normalized: dict[str, pd.DataFrame] = {}
    for name, table in tables.items():
        frame = table.copy()
        frame.columns = [str(column) for column in frame.columns]
        normalized[str(name)] = frame
    return normalized


__all__ = ["normalize_tables"]
