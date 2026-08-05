from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from ariadne.causal.inference.multiplicity import adjust_p_values
from ariadne.causal.inference.estimators.treatment_effect import TreatmentEffectEstimator
from ariadne.preprocessing.inference.aggregation import AGGREGATION_REGISTRY, get_aggregation
from ariadne.preprocessing.inference.encoding import ENCODING_REGISTRY
from ariadne.preprocessing.inference.transforms import TRANSFORM_REGISTRY


def test_feature_registries_fail_fast() -> None:
    assert {"sum", "mean", "count", "nunique", "max", "min"}.issubset(
        AGGREGATION_REGISTRY
    )
    assert {"identity", "log1p", "signed_log1p", "zscore"}.issubset(
        TRANSFORM_REGISTRY
    )
    assert {"one_hot", "ordinal", "binary"}.issubset(ENCODING_REGISTRY)
    with pytest.raises(ValueError, match="unsupported aggregation"):
        get_aggregation("bad")


def test_estimators_use_explicit_estimand_method_names() -> None:
    frame = pd.DataFrame(
        {
            "treated": [0, 0, 0, 1, 1, 1],
            "outcome": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            "x": [0.0, 1.0, 2.0, 0.0, 1.0, 2.0],
        }
    )
    estimator = TreatmentEffectEstimator(
        frame,
        treatment="treated",
        outcome="outcome",
        covariates=["x"],
        estimand="ATE",
    )

    results = estimator.estimate(["ols_coefficient", "g_computation_ate", "ipw_ate"])

    assert results["method"].tolist() == [
        "ols_coefficient",
        "g_computation_ate",
        "ipw_ate",
    ]
    assert results.loc[0, "estimand"] == "regression_coefficient"
    with pytest.raises(ValueError, match="unsupported when estimand=ATE"):
        estimator.estimate(["ipw_att"])


def test_aipw_cross_fitting_is_executed_when_requested() -> None:
    frame = pd.DataFrame(
        {
            "treated": [0, 1] * 10,
            "outcome": np.linspace(1.0, 20.0, 20),
            "x": np.tile([0.0, 1.0, 2.0, 3.0], 5),
        }
    )
    estimator = TreatmentEffectEstimator(
        frame,
        treatment="treated",
        outcome="outcome",
        covariates=["x"],
        estimand="ATE",
        cross_fitting_folds=2,
    )

    result = estimator.estimate(["aipw_ate"])

    assert result.loc[0, "method"] == "aipw_ate"
    assert "cross_fitted_nuisance_models" in result.loc[0, "notes"]


def test_multiplicity_adjustment_is_monotone() -> None:
    adjusted = adjust_p_values(pd.Series([0.01, 0.02, 0.5]), "bh_fdr")

    assert adjusted.iloc[0] <= adjusted.iloc[1] <= adjusted.iloc[2]


def test_estimators_recover_fixed_seed_synthetic_ate() -> None:
    frame = fixed_seed_constant_effect_dgp()
    estimator = TreatmentEffectEstimator(
        frame,
        treatment="treated",
        outcome="outcome",
        covariates=["x"],
        estimand="ATE",
        cross_fitting_folds=2,
    )

    result = estimator.estimate(["g_computation_ate", "ipw_ate", "aipw_ate"])

    for estimate in result["effect"]:
        assert estimate == pytest.approx(2.0, abs=0.08)


def test_estimators_recover_fixed_seed_synthetic_att() -> None:
    frame = fixed_seed_constant_effect_dgp()
    estimator = TreatmentEffectEstimator(
        frame,
        treatment="treated",
        outcome="outcome",
        covariates=["x"],
        estimand="ATT",
        cross_fitting_folds=2,
    )

    result = estimator.estimate(["g_computation_att", "ipw_att", "aipw_att"])

    for estimate in result["effect"]:
        assert estimate == pytest.approx(2.0, abs=0.08)


def test_extreme_propensity_warning_is_reported() -> None:
    x = np.linspace(-5.0, 5.0, 200)
    treated = (x > 0.0).astype(float)
    frame = pd.DataFrame(
        {
            "treated": treated,
            "outcome": 1.0 + 2.0 * treated + 0.2 * x,
            "x": x,
        }
    )
    estimator = TreatmentEffectEstimator(
        frame,
        treatment="treated",
        outcome="outcome",
        covariates=["x"],
        estimand="ATE",
        propensity_clip=(0.05, 0.95),
    )

    result = estimator.estimate(["ipw_ate"])

    assert "overlap_warning=propensity_outside_[0.05,0.95]" in result.loc[0, "notes"]


def fixed_seed_constant_effect_dgp() -> pd.DataFrame:
    """Generate a fixed-seed DGP with ATE = ATT = 2.0."""

    rng = np.random.default_rng(123)
    n = 5000
    x = rng.normal(size=n)
    propensity = 1.0 / (1.0 + np.exp(-0.5 * x))
    treated = rng.binomial(1, propensity)
    outcome = 1.0 + 2.0 * treated + 0.7 * x + rng.normal(scale=0.2, size=n)
    return pd.DataFrame({"treated": treated, "outcome": outcome, "x": x})
