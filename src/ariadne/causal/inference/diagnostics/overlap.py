"""propensity score overlap diagnostic を計算する。"""

from __future__ import annotations

import numpy as np
import pandas as pd


def summarize_propensity_overlap(
    propensity_score: np.ndarray | pd.Series,
    clip: tuple[float, float],
) -> pd.DataFrame:
    """propensity score の overlap を要約する。

    Args:
        propensity_score: Estimated propensity scores.
        clip: Lower and upper clipping bounds.

    Returns:
        One-row data frame containing propensity score quantiles and counts
        outside clipping thresholds.
    """
    values = np.asarray(propensity_score, dtype=float)
    if len(values) == 0:
        return pd.DataFrame(
            columns=[
                "ps_min",
                "ps_p01",
                "ps_p05",
                "ps_median",
                "ps_p95",
                "ps_p99",
                "ps_max",
                "n_ps_below_0_01",
                "n_ps_above_0_99",
            ]
        )
    lower, upper = clip
    return pd.DataFrame(
        [
            {
                "ps_min": float(np.min(values)),
                "ps_p01": float(np.quantile(values, 0.01)),
                "ps_p05": float(np.quantile(values, 0.05)),
                "ps_median": float(np.median(values)),
                "ps_p95": float(np.quantile(values, 0.95)),
                "ps_p99": float(np.quantile(values, 0.99)),
                "ps_max": float(np.max(values)),
                "n_ps_below_0_01": int((values < lower).sum()),
                "n_ps_above_0_99": int((values > upper).sum()),
            }
        ]
    )
