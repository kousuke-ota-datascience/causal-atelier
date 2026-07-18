"""線形回帰と標準誤差計算の低レベル utility。"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import pandas as pd

from ..constants import SUPPORTED_ROBUST_SE


@dataclass(frozen=True)
class LinearRegressionFit:
    """線形回帰の推定結果。

    Attributes:
        coefficients: Estimated coefficients including intercept.
        standard_errors: Standard errors corresponding to coefficients.
        fitted: Fitted values.
        residuals: Model residuals.
        rank: Rank of the design matrix.
        condition_number: Condition number of the design matrix.
        r_squared: Coefficient of determination.
        dof: Residual degrees of freedom used for conventional SE.
    """

    coefficients: np.ndarray
    standard_errors: np.ndarray
    fitted: np.ndarray
    residuals: np.ndarray
    rank: int
    condition_number: float
    r_squared: float
    dof: int


def normal_p_value(z_value: float) -> float:
    """正規近似に基づく両側 p 値を計算する。

    Args:
        z_value: Test statistic.

    Returns:
        Two-sided p-value, or ``nan`` for non-finite input.
    """
    if not np.isfinite(z_value):
        return np.nan
    return float(math.erfc(abs(z_value) / math.sqrt(2.0)))


def confidence_interval(
    estimate: float,
    standard_error: float | None,
    *,
    z_value: float = 1.96,
) -> tuple[float | None, float | None]:
    """正規近似に基づく信頼区間を作る。

    Args:
        estimate: Point estimate.
        standard_error: Standard error for the point estimate.
        z_value: Critical value.

    Returns:
        Pair of lower and upper bounds. Bounds are ``None`` when the standard
        error is missing or non-finite.
    """
    if standard_error is None or not np.isfinite(standard_error):
        return None, None
    return float(estimate - z_value * standard_error), float(estimate + z_value * standard_error)


def none_to_nan(value: float | None) -> float:
    """任意の数値を float に変換し、欠損は ``nan`` にする。

    Args:
        value: Optional value.

    Returns:
        ``nan`` if ``value`` is ``None``; otherwise ``float(value)``.
    """
    return np.nan if value is None else float(value)


def numeric_matrix(frame: pd.DataFrame, columns: list[str] | tuple[str, ...]) -> np.ndarray:
    """指定列を数値 matrix に変換する。

    Args:
        frame: Source data frame.
        columns: Columns to select.

    Returns:
        Two-dimensional numeric matrix. Empty column lists return a matrix with
        zero columns and ``len(frame)`` rows.
    """
    if not columns:
        return np.empty((len(frame), 0), dtype=float)
    return frame.loc[:, list(columns)].to_numpy(dtype=float)


def fit_linear_regression(
    y: np.ndarray,
    x: np.ndarray,
    *,
    robust_se: str = "none",
) -> LinearRegressionFit:
    """OLS を推定し、必要に応じて heteroskedasticity-robust SE を計算する。

    Args:
        y: One-dimensional outcome array.
        x: Two-dimensional design matrix without intercept.
        robust_se: Robust standard error type. Supported values are ``none``,
            ``HC0``, ``HC1``, ``HC2``, and ``HC3``.

    Returns:
        Linear regression fit result.

    Raises:
        ValueError: If inputs have incompatible shapes or unsupported robust SE
            type.
    """
    if robust_se not in SUPPORTED_ROBUST_SE:
        raise ValueError(f"robust_se must be one of {SUPPORTED_ROBUST_SE}: {robust_se}")
    y = np.asarray(y, dtype=float)
    x = np.asarray(x, dtype=float)
    if y.ndim != 1:
        raise ValueError("y must be one-dimensional")
    if x.ndim != 2:
        raise ValueError("x must be two-dimensional")
    if len(y) != x.shape[0]:
        raise ValueError("y and x must have the same number of rows")

    x_design = np.column_stack([np.ones(len(y)), x])
    beta, *_ = np.linalg.lstsq(x_design, y, rcond=None)
    fitted = x_design @ beta
    residuals = y - fitted
    rank = int(np.linalg.matrix_rank(x_design))
    dof = int(max(len(y) - x_design.shape[1], 1))
    xtx_inv = np.linalg.pinv(x_design.T @ x_design)

    if robust_se == "none":
        sigma2 = float((residuals @ residuals) / dof)
        covariance = sigma2 * xtx_inv
    else:
        leverage = np.sum((x_design @ xtx_inv) * x_design, axis=1)
        if robust_se == "HC0":
            scaled_residuals = residuals**2
        elif robust_se == "HC1":
            scaled_residuals = residuals**2 * len(y) / dof
        elif robust_se == "HC2":
            scaled_residuals = residuals**2 / np.clip(1.0 - leverage, 1e-12, None)
        else:
            scaled_residuals = residuals**2 / np.clip(1.0 - leverage, 1e-12, None) ** 2
        meat = x_design.T @ (scaled_residuals[:, None] * x_design)
        covariance = xtx_inv @ meat @ xtx_inv

    standard_errors = np.sqrt(np.clip(np.diag(covariance), 0.0, None))
    centered = y - y.mean()
    total_sum_squares = float(centered @ centered)
    residual_sum_squares = float(residuals @ residuals)
    r_squared = (
        1.0 - residual_sum_squares / total_sum_squares
        if total_sum_squares > 0
        else np.nan
    )
    condition_number = (
        float(np.linalg.cond(x_design))
        if x_design.shape[1] > 0 and x_design.shape[0] >= x_design.shape[1]
        else np.inf
    )
    return LinearRegressionFit(
        coefficients=beta,
        standard_errors=standard_errors,
        fitted=fitted,
        residuals=residuals,
        rank=rank,
        condition_number=condition_number,
        r_squared=float(r_squared),
        dof=dof,
    )
