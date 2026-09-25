"""ENH-E9 G04 P02 persistence checks for actual IPW arm weights."""

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from ariadne.causal.inference.estimators.treatment_effect import TreatmentEffectEstimator
from ariadne.product.domain.enums import ResultType
from ariadne.product.ports.scientific_core import EstimationInput
from ariadne.scientific.inference.adapter import EstimationAdapter


def _graph(path: Path) -> Path:
    graph = {
        "graph_type": "DAG",
        "nodes": ["x", "treatment", "outcome"],
        "edges": [
            {"source": "x", "target": "treatment", "endpoint_source": "TAIL", "endpoint_target": "ARROW"},
            {"source": "x", "target": "outcome", "endpoint_source": "TAIL", "endpoint_target": "ARROW"},
            {"source": "treatment", "target": "outcome", "endpoint_source": "TAIL", "endpoint_target": "ARROW"},
        ],
    }
    path.write_text(json.dumps(graph), encoding="utf-8")
    return path


def _spec(estimand: str) -> dict[str, object]:
    return {
        "causal_question": {"treatment": "treatment", "outcome": "outcome", "estimand": estimand},
        "causal_design": {"adjustment_set": ["x"]},
        "operation_spec": {"inference_options": {}},
    }


def _expected_stats(weights: np.ndarray) -> dict[str, float | int | str]:
    quantiles = np.quantile(weights, [0.50, 0.95, 0.99], method="linear")
    return {
        "count": len(weights),
        "min": float(np.min(weights)),
        "mean": float(np.mean(weights)),
        "p50": float(quantiles[0]),
        "p95": float(quantiles[1]),
        "p99": float(quantiles[2]),
        "max": float(np.max(weights)),
        "extreme_count": int(np.sum(weights > 10.0)),
        "extreme_rule": "weight > 10.0",
    }


@pytest.mark.parametrize("estimand", ["ATE", "ATT"])
def test_ipw_persists_actual_arm_weight_statistics_and_ess(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, estimand: str
) -> None:
    treatment = np.array([1.0] * 12 + [0.0] * 12)
    propensity = np.array([0.1, 0.09999] + [0.5] * 10 + [0.9, 0.90001] + [0.5] * 10)
    frame = pd.DataFrame({"treatment": treatment, "outcome": np.arange(24, dtype=float), "x": np.linspace(-1.0, 1.0, 24)})
    dataset = tmp_path / "dataset.csv"
    frame.to_csv(dataset, index=False)

    def fixed_propensity(self: TreatmentEffectEstimator):
        data = self.complete_case_data(include_covariates=True)
        self.last_propensity_score = np.full(len(data), 0.5)
        return data, data["outcome"].to_numpy(float), data["treatment"].to_numpy(float), propensity

    monkeypatch.setattr(TreatmentEffectEstimator, "propensity_data", fixed_propensity)
    output_dir = tmp_path / estimand.lower()
    results = EstimationAdapter().run(
        EstimationInput(dataset, _graph(tmp_path / "graph.json"), "ipw", parameters={}, analysis_spec=_spec(estimand)),
        output_dir,
    )
    diagnostics_result = next(item for item in results if item.result_type is ResultType.DIAGNOSTICS_RESULT)
    weighting = diagnostics_result.payload["weighting"]

    if estimand == "ATE":
        expected_treated = 1.0 / propensity[treatment == 1.0]
        expected_control = 1.0 / (1.0 - propensity[treatment == 0.0])
    else:
        expected_treated = np.ones(int(np.sum(treatment == 1.0)))
        expected_control = propensity[treatment == 0.0] / (1.0 - propensity[treatment == 0.0])
    expected_ess = lambda values: float(np.sum(values) ** 2 / np.sum(values**2))

    assert weighting["applicability"] == "ESTIMATOR_WEIGHT"
    assert weighting["estimand"] == estimand
    assert weighting["definition"] == (
        "arm-specific IPW analysis weights computed from clipped propensity scores; "
        "weighted means normalize by each arm's weight sum"
    )
    assert weighting["treated"] == _expected_stats(expected_treated)
    assert weighting["control"] == _expected_stats(expected_control)
    assert weighting["effective_sample_size"] == {
        "treated": expected_ess(expected_treated),
        "control": expected_ess(expected_control),
    }
    persisted = json.loads((output_dir / "ipw_diagnostics.json").read_text(encoding="utf-8"))
    assert persisted["weighting"] == weighting
