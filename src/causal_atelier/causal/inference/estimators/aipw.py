"""AIPW 実装上の注意と互換 wrapper。"""

from __future__ import annotations

import pandas as pd

from .treatment_effect import TreatmentEffectEstimator, TreatmentEffectResult


def estimate_aipw_effect(
    y: pd.Series,
    t: pd.Series,
    x: pd.DataFrame,
    estimand: str,
    propensity_clip: tuple[float, float],
    cross_fitting_folds: int = 0,
) -> TreatmentEffectResult:
    """AIPW score を使って treatment effect を推定する。

    Args:
        y: Outcome values.
        t: Binary treatment indicator.
        x: Adjustment covariates.
        estimand: Target estimand, either ``ATE`` or ``ATT``.
        propensity_clip: Lower and upper clipping bounds for propensity scores.
        cross_fitting_folds: Number of folds used for cross-fitting. If ``0``,
            nuisance models are fit on the full sample.

    Returns:
        Treatment effect result.

    Raises:
        ValueError: If the requested estimand is unsupported or the treatment
            column is not binary.
    """
    frame = pd.concat(
        [
            t.rename("treatment"),
            y.rename("outcome"),
            x.reset_index(drop=True),
        ],
        axis=1,
    )
    estimator = TreatmentEffectEstimator(
        frame,
        treatment="treatment",
        outcome="outcome",
        covariates=list(x.columns),
        estimand=estimand,
        propensity_clip=propensity_clip,
        cross_fitting_folds=cross_fitting_folds,
    )
    return estimator.aipw(estimand)
