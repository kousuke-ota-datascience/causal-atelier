"""ENH-E9 G04 P03 before/after balance applicability contract checks."""

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from ariadne.causal.inference.estimators.treatment_effect import TreatmentEffectEstimator
from ariadne.product.ports.scientific_core import EstimationInput
from ariadne.scientific.inference.adapter import EstimationAdapter


def _write_graph(path: Path) -> Path:
    path.write_text(json.dumps({
        "graph_type": "DAG", "nodes": ["x", "treatment", "outcome"],
        "edges": [
            {"source": "x", "target": "treatment", "endpoint_source": "TAIL", "endpoint_target": "ARROW"},
            {"source": "x", "target": "outcome", "endpoint_source": "TAIL", "endpoint_target": "ARROW"},
            {"source": "treatment", "target": "outcome", "endpoint_source": "TAIL", "endpoint_target": "ARROW"},
        ],
    }), encoding="utf-8")
    return path


def _spec(estimand: str) -> dict[str, object]:
    return {
        "causal_question": {"treatment": "treatment", "outcome": "outcome", "estimand": estimand},
        "causal_design": {"adjustment_set": ["x"]},
        "operation_spec": {"inference_options": {}},
    }


def _expected_balance(values: np.ndarray, treatment: np.ndarray, weights: np.ndarray | None) -> dict[str, float | str]:
    treated = values[treatment == 1.0]
    control = values[treatment == 0.0]
    if weights is None:
        treated_mean, control_mean = float(np.mean(treated)), float(np.mean(control))
        treated_std, control_std = float(np.std(treated, ddof=1)), float(np.std(control, ddof=1))
    else:
        treated_weights, control_weights = weights[treatment == 1.0], weights[treatment == 0.0]
        treated_mean = float(np.sum(treated * treated_weights) / np.sum(treated_weights))
        control_mean = float(np.sum(control * control_weights) / np.sum(control_weights))
        treated_std = float(np.sqrt(np.sum((treated - treated_mean) ** 2 * treated_weights) / np.sum(treated_weights)))
        control_std = float(np.sqrt(np.sum((control - control_mean) ** 2 * control_weights) / np.sum(control_weights)))
    pooled = math.sqrt((treated_std**2 + control_std**2) / 2.0)
    return {
        "covariate": "x",
        "mean_treated": treated_mean,
        "mean_control": control_mean,
        "std_treated": treated_std,
        "std_control": control_std,
        "standardized_mean_difference": (treated_mean - control_mean) / pooled,
        "missing_rate": 0.0,
    }


def _assert_balance_row(actual: dict[str, object], expected: dict[str, float | str]) -> None:
    assert actual["covariate"] == expected["covariate"]
    for field in (
        "mean_treated",
        "mean_control",
        "std_treated",
        "std_control",
        "standardized_mean_difference",
        "missing_rate",
    ):
        assert actual[field] == pytest.approx(expected[field])


@pytest.mark.parametrize("estimand", ["ATE", "ATT"])
def test_ipw_persists_unweighted_before_and_actual_weighted_after_balance(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, estimand: str
) -> None:
    treatment = np.array([1.0] * 12 + [0.0] * 12)
    x = np.array([float(value) for value in range(12)] + [float(value) for value in range(3, 15)])
    propensity = np.array([0.20, 0.25, 0.30, 0.35] * 3 + [0.60, 0.65, 0.70, 0.75] * 3)
    frame = pd.DataFrame({"treatment": treatment, "outcome": 2.0 * treatment + x, "x": x})
    dataset = tmp_path / "dataset.csv"
    frame.to_csv(dataset, index=False)

    def fixed_propensity(self: TreatmentEffectEstimator):
        data = self.complete_case_data(include_covariates=True)
        self.last_propensity_score = np.full(len(data), 0.5)
        return data, data["outcome"].to_numpy(float), data["treatment"].to_numpy(float), propensity

    monkeypatch.setattr(TreatmentEffectEstimator, "propensity_data", fixed_propensity)
    result = EstimationAdapter().run(
        EstimationInput(dataset, _write_graph(tmp_path / "graph.json"), "ipw", analysis_spec=_spec(estimand)),
        tmp_path / estimand.lower(),
    )
    balance = result.diagnostics["balance"]
    if estimand == "ATE":
        weights = np.where(treatment == 1.0, 1.0 / propensity, 1.0 / (1.0 - propensity))
    else:
        weights = np.where(treatment == 1.0, 1.0, propensity / (1.0 - propensity))

    assert balance["after_applicability"] == "ESTIMATOR_WEIGHT"
    _assert_balance_row(balance["before"][0], _expected_balance(x, treatment, None))
    _assert_balance_row(balance["after"][0], _expected_balance(x, treatment, weights))
    assert balance["before"] != balance["after"]
    json.dumps(result.diagnostics, allow_nan=False)


@pytest.mark.parametrize(
    ("estimator", "expected_applicability"),
    [("ols", "NOT_APPLICABLE"), ("difference_in_means", "NOT_APPLICABLE"), ("aipw", "PROPENSITY_COMPONENT")],
)
def test_non_ipw_estimators_keep_after_null_and_persist_applicability(
    tmp_path: Path, estimator: str, expected_applicability: str
) -> None:
    treatment = np.array([0.0, 1.0] * 12)
    x = np.linspace(-1.0, 1.0, 24)
    frame = pd.DataFrame({"treatment": treatment, "outcome": 2.0 * treatment + x, "x": x})
    dataset = tmp_path / "dataset.csv"
    frame.to_csv(dataset, index=False)
    result = EstimationAdapter().run(
        EstimationInput(dataset, _write_graph(tmp_path / "graph.json"), estimator, analysis_spec=_spec("ATE")),
        tmp_path / estimator,
    )

    assert result.diagnostics["balance"]["after_applicability"] == expected_applicability
    assert result.diagnostics["balance"]["after"] is None
    assert result.diagnostics["weighting"]["applicability"] == expected_applicability
    assert result.diagnostics["weighting"]["effective_sample_size"] == {"treated": None, "control": None}
    assert result.diagnostics["weighting"]["treated"] is None
    assert result.diagnostics["weighting"]["control"] is None
    json.dumps(result.diagnostics, allow_nan=False)
