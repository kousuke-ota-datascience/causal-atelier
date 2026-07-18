"""IPW estimator の単独 wrapper。"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd

from .inference import effective_sample_size, weighted_mean, weighted_variance


def estimate_ipw_effect(
    y: pd.Series,
    t: pd.Series,
    propensity_score: pd.Series,
    estimand: str,
    clip: tuple[float, float],
) -> float:
    """inverse-probability-weighting による treatment effect を推定する。

    Args:
        y: Outcome values.
        t: Binary treatment indicator.
        propensity_score: Estimated propensity scores.
        estimand: Target estimand, either ``ATE`` or ``ATT``.
        clip: Lower and upper clipping bounds for propensity scores.

    Returns:
        IPW point estimate.

    Raises:
        ValueError: If the estimand is unsupported.
    """
    if estimand not in {"ATE", "ATT"}:
        raise ValueError(f"estimand must be ATE or ATT: {estimand}")
    values = y.to_numpy(dtype=float)
    treatment = t.to_numpy(dtype=float)
    ps = np.clip(propensity_score.to_numpy(dtype=float), *clip)
    if estimand == "ATE":
        weights_treated = treatment / ps
        weights_control = (1.0 - treatment) / (1.0 - ps)
    else:
        weights_treated = treatment
        weights_control = (1.0 - treatment) * ps / (1.0 - ps)
    return float(weighted_mean(values, weights_treated) - weighted_mean(values, weights_control))


def estimate_ipw_standard_error(
    y: pd.Series,
    t: pd.Series,
    propensity_score: pd.Series,
    estimand: str,
    clip: tuple[float, float],
) -> float:
    """旧実装互換の IPW standard error 近似を計算する。

    Args:
        y: Outcome values.
        t: Binary treatment indicator.
        propensity_score: Estimated propensity scores.
        estimand: Target estimand, either ``ATE`` or ``ATT``.
        clip: Lower and upper clipping bounds.

    Returns:
        Approximate standard error.
    """
    values = y.to_numpy(dtype=float)
    treatment = t.to_numpy(dtype=float)
    ps = np.clip(propensity_score.to_numpy(dtype=float), *clip)
    if estimand == "ATE":
        weights_treated = treatment / ps
        weights_control = (1.0 - treatment) / (1.0 - ps)
    else:
        weights_treated = treatment
        weights_control = (1.0 - treatment) * ps / (1.0 - ps)
    mean_treated = weighted_mean(values, weights_treated)
    mean_control = weighted_mean(values, weights_control)
    return math.sqrt(
        weighted_variance(values, weights_treated, mean_treated)
        / effective_sample_size(weights_treated)
        + weighted_variance(values, weights_control, mean_control)
        / effective_sample_size(weights_control)
    )
