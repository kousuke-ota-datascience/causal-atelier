from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from ariadne.product.domain.enums import ResultType, ScientificStatus
from ariadne.product.ports.scientific_core import (
    IdentificationInput, EstimationInput, RefutationInput, SensitivityInput,
)
from ariadne.scientific.identification.adapter import IdentificationAdapter
from ariadne.scientific.inference.adapter import EstimationAdapter
from ariadne.scientific.refutation.adapter import RefutationAdapter
from ariadne.scientific.sensitivity.adapter import SensitivityAdapter


def analysis_spec(strategy="BACKDOOR", adjustment=None, estimator="ols"):  # type: ignore[no-untyped-def]
    return {
        "schema_version": "causal-analysis-spec/2", "analysis_mode": "EXPLORATORY",
        "research_context": {},
        "causal_question": {"population": "rows", "treatment": "t", "comparator": "0",
                            "outcome": "y", "analysis_unit": "id", "treatment_time": "t0",
                            "outcome_window": "t1", "estimand": "ATE"},
        "causal_design": {"identification_strategy": strategy,
                          "adjustment_set": [] if adjustment is None else adjustment,
                          "assumptions": []},
        "operation_spec": {"estimator": estimator, "inference_options": {}},
        "validation_override": None,
    }


def write_inputs(tmp_path: Path, graph: dict, *, poor_overlap=False):  # type: ignore[no-untyped-def]
    rng = np.random.default_rng(20260806); n = 300
    x = np.linspace(-12, 12, n) if poor_overlap else rng.normal(size=n)
    p = 1 / (1 + np.exp(-(3 * x if poor_overlap else .7 * x)))
    t = rng.binomial(1, p); y = 2 * t + x + rng.normal(size=n)
    frame = pd.DataFrame({"id": range(n), "x": x, "t": t, "y": y, "m": t + rng.normal(size=n)})
    dataset = tmp_path / "data.csv"; frame.to_csv(dataset, index=False)
    graph_path = tmp_path / "graph.json"; graph_path.write_text(json.dumps(graph), encoding="utf-8")
    return dataset, graph_path


BASE_GRAPH = {"graph_type": "DAG", "nodes": ["x", "t", "y", "m"], "edges": [
    {"source": "x", "target": "t", "endpoint_source": "TAIL", "endpoint_target": "ARROW"},
    {"source": "x", "target": "y", "endpoint_source": "TAIL", "endpoint_target": "ARROW"},
    {"source": "t", "target": "y", "endpoint_source": "TAIL", "endpoint_target": "ARROW"},
    {"source": "t", "target": "m", "endpoint_source": "TAIL", "endpoint_target": "ARROW"},
]}


@pytest.mark.scientific_benchmark
@pytest.mark.parametrize(("graph", "adjustment", "expected"), [
    (BASE_GRAPH, ["x"], ScientificStatus.IDENTIFIED),
    (BASE_GRAPH, [], ScientificStatus.NOT_IDENTIFIED),
    (BASE_GRAPH, ["m"], ScientificStatus.NOT_IDENTIFIED),
    ({**BASE_GRAPH, "graph_type": "CPDAG"}, ["x"], ScientificStatus.REQUIRES_REVIEW),
    ({**BASE_GRAPH, "graph_type": "PAG"}, ["x"], ScientificStatus.REQUIRES_REVIEW),
])
def test_deterministic_identification_statuses(tmp_path: Path, graph, adjustment, expected):  # type: ignore[no-untyped-def]
    dataset, graph_path = write_inputs(tmp_path, graph)
    results = IdentificationAdapter().run(IdentificationInput(
        dataset, graph_path, "GRAPHICAL_IDENTIFICATION", {}, 42,
        analysis_spec(adjustment=adjustment),
    ), tmp_path / "out")
    assert results[0].result_type == ResultType.IDENTIFICATION_RESULT
    assert results[0].scientific_status == expected


@pytest.mark.scientific_benchmark
def test_fixed_poor_overlap_is_detected(tmp_path: Path) -> None:
    dataset, graph_path = write_inputs(tmp_path, BASE_GRAPH, poor_overlap=True)
    results = IdentificationAdapter().run(IdentificationInput(
        dataset, graph_path, "GRAPHICAL_IDENTIFICATION", {}, 42,
        analysis_spec(adjustment=["x"]),
    ), tmp_path / "out")
    assert results[1].scientific_status in {ScientificStatus.WARN, ScientificStatus.FAIL}
    assert any(
        check["check_code"] == "LIMITED_OVERLAP" and check["status"] in {"WARN", "FAIL"}
        for check in results[1].payload["checks"]
    )


@pytest.mark.scientific_benchmark
def test_randomized_ate_bias_and_empirical_coverage_gate(tmp_path: Path) -> None:
    graph = {"graph_type": "DAG", "nodes": ["t", "y"], "edges": [
        {"source": "t", "target": "y", "endpoint_source": "TAIL", "endpoint_target": "ARROW"},
    ]}
    graph_path = tmp_path / "rct_graph.json"; graph_path.write_text(json.dumps(graph), encoding="utf-8")
    estimates: list[float] = []; covered = 0; truth = 2.0
    spec = analysis_spec(strategy="RANDOMIZED", adjustment=[], estimator="difference_in_means")
    for seed in range(100, 200):
        rng = np.random.default_rng(seed); n = 500
        treatment = rng.binomial(1, .5, n)
        outcome = truth * treatment + rng.normal(size=n)
        dataset = tmp_path / f"rct-{seed}.csv"
        pd.DataFrame({"t": treatment, "y": outcome}).to_csv(dataset, index=False)
        output = EstimationAdapter().run(EstimationInput(
            dataset, graph_path, "difference_in_means", {}, {}, seed, spec,
        ), tmp_path / f"out-{seed}")
        estimate = float(output.payload["estimate"]); estimates.append(estimate)
        low, high = output.payload["confidence_interval"]
        covered += int(low <= truth <= high)
    standardized_absolute_bias = abs(float(np.mean(estimates)) - truth) / truth
    coverage = covered / len(estimates)
    assert standardized_absolute_bias <= .10
    assert .90 <= coverage <= .98


@pytest.mark.scientific_benchmark
def test_refutation_seed_and_sensitivity_variation_are_reproducible(tmp_path: Path) -> None:
    dataset, graph_path = write_inputs(tmp_path, BASE_GRAPH)
    estimate_spec = analysis_spec(adjustment=["x"], estimator="ipw")
    base = EstimationAdapter().run(EstimationInput(
        dataset, graph_path, "ipw", {}, {}, 42, estimate_spec,
    ), tmp_path / "base")[0]
    base_document = {"payload": base.payload, "causal_question": estimate_spec["causal_question"],
                     "causal_design": estimate_spec["causal_design"]}

    refutation_spec = {**estimate_spec, "operation_spec": {
        "method": "PLACEBO_TREATMENT", "repetitions": 10,
    }}
    input_value = RefutationInput(
        dataset, graph_path, base_document, "PLACEBO_TREATMENT", {}, 42, refutation_spec,
    )
    first = RefutationAdapter().run(input_value, tmp_path / "refute-a")[0]
    second = RefutationAdapter().run(input_value, tmp_path / "refute-b")[0]
    assert first.payload["refutation_estimate"] == second.payload["refutation_estimate"]
    assert "does not prove" in first.payload["interpretation"]

    sensitivity_spec = {**estimate_spec, "operation_spec": {
        "dimension": "PROPENSITY_CLIPPING", "values": [.01, .025, .05],
    }}
    sensitivity = SensitivityAdapter().run(SensitivityInput(
        dataset, graph_path, base_document, "PROPENSITY_CLIPPING", {}, 42,
        sensitivity_spec,
    ), tmp_path / "sensitivity")[0]
    assert sensitivity.payload["effect_range"] is not None
    assert len(sensitivity.payload["variation"]) == 3
