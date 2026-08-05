"""outcome 変数の分布 diagnostic を計算する。"""

from __future__ import annotations

import numpy as np
import pandas as pd


def summarize_outcome_distribution(
    frame: pd.DataFrame,
    outcome: str,
) -> pd.DataFrame:
    """outcome 変数の分布を要約する。

    Args:
        frame: Analysis frame.
        outcome: Outcome column.

    Returns:
        One-row data frame with descriptive statistics and zero rate.

    Raises:
        ValueError: If the outcome column is missing.
    """
    if outcome not in frame.columns:
        raise ValueError(f"outcome column is missing: {outcome}")
    values = pd.to_numeric(frame[outcome], errors="coerce").dropna()
    if values.empty:
        return pd.DataFrame(
            [
                {
                    "mean": np.nan,
                    "std": np.nan,
                    "min": np.nan,
                    "p25": np.nan,
                    "median": np.nan,
                    "p75": np.nan,
                    "max": np.nan,
                    "zero_rate": np.nan,
                    "skewness": np.nan,
                }
            ]
        )
    return pd.DataFrame(
        [
            {
                "mean": float(values.mean()),
                "std": float(values.std(ddof=1)),
                "min": float(values.min()),
                "p25": float(values.quantile(0.25)),
                "median": float(values.median()),
                "p75": float(values.quantile(0.75)),
                "max": float(values.max()),
                "zero_rate": float((values == 0.0).mean()),
                "skewness": float(values.skew()),
            }
        ]
    )
