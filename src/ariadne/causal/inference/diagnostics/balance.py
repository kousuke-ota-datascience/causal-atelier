"""共変量 balance diagnostic を計算する。"""

from __future__ import annotations

from collections.abc import Sequence
import math

import numpy as np
import pandas as pd

from ..estimators.inference import records_to_frame


def compute_balance_table(
    frame: pd.DataFrame,
    treatment: str,
    covariates: Sequence[str],
    weights: pd.Series | None = None,
) -> pd.DataFrame:
    """共変量 balance diagnostic table を計算する。

    Args:
        frame: Analysis frame.
        treatment: Binary treatment column.
        covariates: Covariates to diagnose.
        weights: Optional observation weights. The current table preserves the
            legacy unweighted standardized mean difference when ``None``.

    Returns:
        Covariate balance table including treated/control means, standard
        deviations, missing rates, and standardized mean differences.

    Raises:
        ValueError: If treatment or covariate columns are invalid.
    """
    if treatment not in frame.columns:
        raise ValueError(f"treatment column is missing: {treatment}")
    missing = [column for column in covariates if column not in frame.columns]
    if missing:
        raise ValueError(f"covariates are missing: {missing}")

    treatment_values = frame[treatment].astype(float)
    records = []
    for column in covariates:
        values = pd.to_numeric(frame[column], errors="coerce")
        if weights is None:
            treated_values = values.loc[treatment_values == 1.0].dropna()
            control_values = values.loc[treatment_values == 0.0].dropna()
            mean_treated = float(treated_values.mean()) if len(treated_values) else np.nan
            mean_control = float(control_values.mean()) if len(control_values) else np.nan
            std_treated = float(treated_values.std(ddof=1)) if len(treated_values) > 1 else np.nan
            std_control = float(control_values.std(ddof=1)) if len(control_values) > 1 else np.nan
        else:
            aligned_weights = weights.reindex(frame.index).astype(float)
            mean_treated = _weighted_mean(values, aligned_weights, treatment_values == 1.0)
            mean_control = _weighted_mean(values, aligned_weights, treatment_values == 0.0)
            std_treated = _weighted_std(values, aligned_weights, treatment_values == 1.0, mean_treated)
            std_control = _weighted_std(values, aligned_weights, treatment_values == 0.0, mean_control)
        pooled_std = math.sqrt((std_treated**2 + std_control**2) / 2.0) if (
            np.isfinite(std_treated) and np.isfinite(std_control)
        ) else np.nan
        smd = (
            (mean_treated - mean_control) / pooled_std
            if np.isfinite(pooled_std) and pooled_std > 0
            else np.nan
        )
        records.append(
            {
                "covariate": column,
                "mean_treated": mean_treated,
                "mean_control": mean_control,
                "std_treated": std_treated,
                "std_control": std_control,
                "standardized_mean_difference": float(smd) if np.isfinite(smd) else np.nan,
                "missing_rate": float(values.isna().mean()),
            }
        )
    return records_to_frame(
        records,
        [
            "covariate",
            "mean_treated",
            "mean_control",
            "std_treated",
            "std_control",
            "standardized_mean_difference",
            "missing_rate",
        ],
    )


def _weighted_mean(values: pd.Series, weights: pd.Series, mask: pd.Series) -> float:
    """mask された subset の重み付き平均を計算する。

    Args:
        values: Values to summarize.
        weights: Observation weights.
        mask: Boolean subset mask.

    Returns:
        Weighted mean or ``nan``.
    """
    subset = values.loc[mask].dropna()
    subset_weights = weights.loc[subset.index]
    denominator = float(subset_weights.sum())
    if denominator <= 0:
        return np.nan
    return float((subset * subset_weights).sum() / denominator)


def _weighted_std(
    values: pd.Series,
    weights: pd.Series,
    mask: pd.Series,
    mean: float,
) -> float:
    """mask された subset の重み付き標準偏差を計算する。

    Args:
        values: Values to summarize.
        weights: Observation weights.
        mask: Boolean subset mask.
        mean: Weighted mean.

    Returns:
        Weighted standard deviation or ``nan``.
    """
    subset = values.loc[mask].dropna()
    subset_weights = weights.loc[subset.index]
    denominator = float(subset_weights.sum())
    if denominator <= 0:
        return np.nan
    return float(np.sqrt(((subset - mean) ** 2 * subset_weights).sum() / denominator))
