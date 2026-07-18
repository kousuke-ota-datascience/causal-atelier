"""Deterministic numeric transform registry."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
import pandas as pd


TransformFunction = Callable[[pd.Series], pd.Series]


def identity(series: pd.Series) -> pd.Series:
    """Return the input as float."""

    return pd.to_numeric(series, errors="coerce").astype(float)


def signed_log1p(series: pd.Series) -> pd.Series:
    """Apply sign-preserving log1p."""

    values = pd.to_numeric(series, errors="coerce").astype(float)
    return np.sign(values) * np.log1p(np.abs(values))


def zscore(series: pd.Series) -> pd.Series:
    """Apply z-score scaling."""

    values = pd.to_numeric(series, errors="coerce").astype(float)
    std = values.std()
    if std == 0 or not np.isfinite(std):
        return values * np.nan
    return (values - values.mean()) / std


TRANSFORM_REGISTRY: dict[str, TransformFunction] = {
    "identity": identity,
    "log1p": lambda series: np.log1p(pd.to_numeric(series, errors="coerce").astype(float)),
    "signed_log1p": signed_log1p,
    "zscore": zscore,
}


def get_transform(name: str) -> TransformFunction:
    """Return a transform function or fail fast."""

    try:
        return TRANSFORM_REGISTRY[name]
    except KeyError as exc:
        raise ValueError(f"unsupported transform: {name}") from exc


__all__ = ["TRANSFORM_REGISTRY", "TransformFunction", "get_transform"]
