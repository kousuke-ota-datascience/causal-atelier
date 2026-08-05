"""Aggregation registry for feature construction."""

from __future__ import annotations

from collections.abc import Callable

import pandas as pd


AggregationFunction = Callable[[pd.core.groupby.SeriesGroupBy], pd.Series]


AGGREGATION_REGISTRY: dict[str, AggregationFunction] = {
    "sum": lambda grouped: grouped.sum(),
    "mean": lambda grouped: grouped.mean(),
    "count": lambda grouped: grouped.count(),
    "nunique": lambda grouped: grouped.nunique(),
    "max": lambda grouped: grouped.max(),
    "min": lambda grouped: grouped.min(),
}


def get_aggregation(name: str) -> AggregationFunction:
    """Return an aggregation function or fail fast."""

    try:
        return AGGREGATION_REGISTRY[name]
    except KeyError as exc:
        raise ValueError(f"unsupported aggregation: {name}") from exc


__all__ = ["AGGREGATION_REGISTRY", "AggregationFunction", "get_aggregation"]
