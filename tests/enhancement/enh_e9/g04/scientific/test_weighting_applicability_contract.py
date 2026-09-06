"""ENH-E9 G04 P01 diagnostics applicability and estimator-weight contract."""

import numpy as np
import pandas as pd

from ariadne.causal.inference.estimators.treatment_effect import (
    WEIGHT_EXTREME_THRESHOLD,
    TreatmentEffectEstimator,
    WeightingApplicability,
    count_extreme_weights,
)
from ariadne.causal.inference.estimators.inference import weighted_mean
from ariadne.causal.inference.diagnostics.overlap import summarize_propensity_overlap


def _engine() -> TreatmentEffectEstimator:
    frame = pd.DataFrame(
        {
            "treatment": [1.0, 0.0, 1.0, 0.0],
            "outcome": [12.0, 3.0, 10.0, 2.0],
            "x": [0.0, 1.0, 2.0, 3.0],
        }
    )
    return TreatmentEffectEstimator(frame, "treatment", "outcome", ["x"], estimand="ATE")


def _with_fixed_propensity(engine: TreatmentEffectEstimator, propensity: np.ndarray) -> None:
    data = engine.complete_case_data(include_covariates=True)
    engine.propensity_data = lambda: (  # type: ignore[method-assign]
        data,
        data["outcome"].to_numpy(dtype=float),
        data["treatment"].to_numpy(dtype=float),
        propensity,
    )


def test_applicability_values_are_exactly_the_stable_contract() -> None:
    assert [value.value for value in WeightingApplicability] == [
        "ESTIMATOR_WEIGHT",
        "PROPENSITY_COMPONENT",
        "NOT_APPLICABLE",
    ]


def test_ipw_ate_exposes_the_actual_positive_observed_weight_components() -> None:
    engine = _engine()
    propensity = np.array([0.25, 0.20, 0.50, 0.80])
    _with_fixed_propensity(engine, propensity)

    result = engine.ipw("ATE")
    exposed = engine.last_weighting_diagnostics
    expected_treated = np.array([1.0 / 0.25, 1.0 / 0.50])
    expected_control = np.array([1.0 / (1.0 - 0.20), 1.0 / (1.0 - 0.80)])

    assert exposed.applicability is WeightingApplicability.ESTIMATOR_WEIGHT
    assert exposed.estimand == "ATE"
    np.testing.assert_allclose(exposed.treated_weights, expected_treated)
    np.testing.assert_allclose(exposed.control_weights, expected_control)
    expected_effect = weighted_mean(np.array([12.0, 3.0, 10.0, 2.0]), np.array([4.0, 0.0, 2.0, 0.0])) - weighted_mean(np.array([12.0, 3.0, 10.0, 2.0]), np.array([0.0, 1.25, 0.0, 5.0]))
    assert result.effect == expected_effect


def test_ipw_att_exposes_the_actual_positive_observed_weight_components() -> None:
    engine = _engine()
    propensity = np.array([0.25, 0.20, 0.50, 0.80])
    _with_fixed_propensity(engine, propensity)

    engine.ipw("ATT")
    exposed = engine.last_weighting_diagnostics

    assert exposed.applicability is WeightingApplicability.ESTIMATOR_WEIGHT
    assert exposed.estimand == "ATT"
    np.testing.assert_allclose(exposed.treated_weights, np.array([1.0, 1.0]))
    np.testing.assert_allclose(exposed.control_weights, np.array([0.20 / 0.80, 0.80 / 0.20]))


def test_extreme_weight_boundary_and_propensity_overlap_are_independent() -> None:
    assert WEIGHT_EXTREME_THRESHOLD == 10.0
    assert count_extreme_weights(np.array([1.0, 10.0, 10.00001])) == 1
    overlap = summarize_propensity_overlap(np.array([0.001, 0.50, 0.999]), (0.01, 0.99))
    assert int(overlap.loc[0, "n_ps_below_0_01"]) + int(overlap.loc[0, "n_ps_above_0_99"]) == 2
    # Analysis-weight extreme counts neither reuse nor encode propensity clipping counts.
    assert count_extreme_weights(np.array([0.01, 0.99])) == 0


def test_non_weight_estimators_and_aipw_keep_their_distinct_boundaries() -> None:
    engine = _engine()
    engine.diff_in_means()
    assert engine.last_weighting_diagnostics.applicability is WeightingApplicability.NOT_APPLICABLE
    assert engine.last_weighting_diagnostics.treated_weights is None
    assert engine.last_weighting_diagnostics.control_weights is None
    engine.ols()
    assert engine.last_weighting_diagnostics.applicability is WeightingApplicability.NOT_APPLICABLE

    frame = pd.DataFrame(
        {
            "treatment": [0.0, 1.0] * 6,
            "outcome": [1.0, 4.0, 2.0, 5.0, 1.5, 4.5, 2.5, 5.5, 1.2, 4.2, 2.2, 5.2],
            "x": np.linspace(-1.0, 1.0, 12),
        }
    )
    aipw = TreatmentEffectEstimator(frame, "treatment", "outcome", ["x"], estimand="ATE")
    aipw.aipw("ATE")
    exposed = aipw.last_weighting_diagnostics
    assert exposed.applicability is WeightingApplicability.PROPENSITY_COMPONENT
    assert "not a whole-estimator final weight vector" in exposed.definition
    assert exposed.treated_weights is not None
    assert exposed.control_weights is not None


def test_aipw_component_uses_the_cross_fitted_propensity_used_by_the_score() -> None:
    frame = pd.DataFrame(
        {
            "treatment": [0.0, 1.0] * 6,
            "outcome": [1.0, 4.0, 2.0, 5.0, 1.5, 4.5, 2.5, 5.5, 1.2, 4.2, 2.2, 5.2],
            "x": np.linspace(-1.0, 1.0, 12),
        }
    )
    engine = TreatmentEffectEstimator(
        frame, "treatment", "outcome", ["x"], estimand="ATE", cross_fitting_folds=2
    )
    engine.cross_fitted_nuisance = lambda y, t, x: (  # type: ignore[method-assign]
        np.where(t == 1.0, 0.25, 0.80),
        np.zeros(len(y)),
        np.zeros(len(y)),
        "fixture",
    )

    engine.aipw("ATE")

    exposed = engine.last_weighting_diagnostics
    np.testing.assert_allclose(exposed.treated_weights, np.full(6, 4.0))
    np.testing.assert_allclose(exposed.control_weights, np.full(6, 5.0))
