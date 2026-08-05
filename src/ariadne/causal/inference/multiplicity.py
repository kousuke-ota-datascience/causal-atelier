"""Multiplicity correction helpers."""

from __future__ import annotations

import numpy as np
import pandas as pd


def adjust_p_values(p_values: pd.Series, method: str) -> pd.Series:
    """Adjust p-values with Bonferroni or Benjamini-Hochberg FDR."""

    values = pd.to_numeric(p_values, errors="coerce").to_numpy(dtype=float)
    adjusted = np.full(len(values), np.nan, dtype=float)
    valid = np.isfinite(values)
    if valid.sum() == 0:
        return pd.Series(adjusted, index=p_values.index)
    if method == "bonferroni":
        adjusted[valid] = np.minimum(values[valid] * valid.sum(), 1.0)
    elif method == "bh_fdr":
        order = np.argsort(values[valid])
        sorted_values = values[valid][order]
        ranks = np.arange(1, len(sorted_values) + 1)
        sorted_adjusted = np.minimum.accumulate(
            (sorted_values * len(sorted_values) / ranks)[::-1]
        )[::-1]
        valid_positions = np.flatnonzero(valid)
        adjusted[valid_positions[order]] = np.minimum(sorted_adjusted, 1.0)
    else:
        raise ValueError(f"unsupported p-value adjustment method: {method}")
    return pd.Series(adjusted, index=p_values.index)


__all__ = ["adjust_p_values"]
