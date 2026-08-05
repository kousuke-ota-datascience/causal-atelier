"""propensity score 推定の helper。"""

from __future__ import annotations

import numpy as np


def logistic(values: np.ndarray) -> np.ndarray:
    """数値的に安定な logistic 変換を適用する。

    Args:
        values: Linear predictor values.

    Returns:
        Probabilities in ``(0, 1)`` after clipping the linear predictor.
    """
    clipped = np.clip(values, -35.0, 35.0)
    return 1.0 / (1.0 + np.exp(-clipped))


def fit_logistic_propensity(
    treatment: np.ndarray,
    covariates: np.ndarray,
    *,
    max_iter: int = 100,
    tol: float = 1e-8,
    ridge: float = 1e-6,
) -> tuple[np.ndarray, str]:
    """ridge で安定化した logistic propensity model を Newton 法で推定する。

    Args:
        treatment: Binary treatment indicator.
        covariates: Covariate design matrix without intercept.
        max_iter: Maximum Newton iterations.
        tol: Maximum absolute coefficient update for convergence.
        ridge: Ridge penalty applied to non-intercept coefficients.

    Returns:
        Pair of estimated propensity scores and a notes string.
    """
    x_design = np.column_stack([np.ones(len(treatment)), covariates])
    beta = np.zeros(x_design.shape[1], dtype=float)
    converged = False

    for _ in range(max_iter):
        probability = logistic(x_design @ beta)
        weights = np.clip(probability * (1.0 - probability), 1e-8, None)
        hessian = x_design.T @ (weights[:, None] * x_design)
        penalty = np.eye(x_design.shape[1]) * ridge
        penalty[0, 0] = 0.0
        score = x_design.T @ (treatment - probability) - penalty @ beta
        try:
            delta = np.linalg.solve(hessian + penalty, score)
        except np.linalg.LinAlgError:
            delta = np.linalg.pinv(hessian + penalty) @ score
        beta = beta + delta
        if float(np.max(np.abs(delta))) < tol:
            converged = True
            break

    notes = "" if converged else "propensity_logit_not_converged"
    return logistic(x_design @ beta), notes
