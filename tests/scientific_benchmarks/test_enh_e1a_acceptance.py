from __future__ import annotations

import copy
import json
import math
import time
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import statsmodels.api as sm

from ariadne.product.domain.enums import ScientificStatus
from ariadne.product.ports.scientific_core import (
    EstimationInput,
    IdentificationInput,
    RefutationInput,
    SensitivityInput,
)
from ariadne.scientific.benchmark_report import (
    REQUIRED_SCENARIO_FIELDS,
    SCENARIO_MANIFEST,
    evaluate_gate,
    package_versions,
    write_report,
)
from ariadne.scientific.identification.adapter import IdentificationAdapter
from ariadne.scientific.inference.adapter import EstimationAdapter
from ariadne.scientific.refutation.adapter import RefutationAdapter
from ariadne.scientific.sensitivity.adapter import SensitivityAdapter


pytestmark = pytest.mark.scientific_benchmark
RECORDED: list[dict] = []
EDGE = lambda source, target: {  # noqa: E731
    "source": source,
    "target": target,
    "endpoint_source": "TAIL",
    "endpoint_target": "ARROW",
}
BASE_GRAPH = {
    "graph_type": "DAG",
    "nodes": ["id", "x", "z", "t", "y", "m"],
    "edges": [EDGE("x", "t"), EDGE("x", "y"), EDGE("t", "y"), EDGE("t", "m")],
}


def _spec(
    *, strategy: str = "BACKDOOR", adjustment: list[str] | None = None,
    estimator: str = "ols", estimand: str = "ATE", operation_spec: dict | None = None,
) -> dict:
    return {
        "schema_version": "causal-analysis-spec/2",
        "analysis_mode": "EXPLORATORY",
        "research_context": {},
        "causal_question": {
            "population": "rows", "treatment": "t", "comparator": "0",
            "outcome": "y", "analysis_unit": "id", "treatment_time": "t0",
            "outcome_window": "t1", "estimand": estimand,
        },
        "causal_design": {
            "identification_strategy": strategy,
            "adjustment_set": adjustment or [], "assumptions": [],
        },
        "operation_spec": operation_spec or {"estimator": estimator, "inference_options": {}},
        "validation_override": None,
    }


def _write(tmp_path: Path, frame: pd.DataFrame, graph: dict) -> tuple[Path, Path]:
    dataset = tmp_path / "data.csv"
    graph_path = tmp_path / "graph.json"
    frame.to_csv(dataset, index=False)
    graph_path.write_text(json.dumps(graph), encoding="utf-8")
    return dataset, graph_path


def _frame(seed: int = 20260806, *, n: int = 400, poor_overlap: bool = False) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    x = np.linspace(-12, 12, n) if poor_overlap else rng.normal(size=n)
    z = rng.normal(size=n)
    linear = 3 * x if poor_overlap else 0.8 * x
    t = rng.binomial(1, 1 / (1 + np.exp(-linear)))
    y = 2 * t + 0.8 * x - 0.3 * z + rng.normal(size=n)
    return pd.DataFrame({"id": range(n), "x": x, "z": z, "t": t, "y": y, "m": t + rng.normal(size=n)})


def _identify(tmp_path: Path, frame: pd.DataFrame, graph: dict, adjustment: list[str]):
    dataset, graph_path = _write(tmp_path, frame, graph)
    return IdentificationAdapter().run(IdentificationInput(
        dataset, graph_path, "GRAPHICAL_IDENTIFICATION", {}, 42,
        _spec(adjustment=adjustment),
    ), tmp_path / "identify"), dataset, graph_path


def _record(
    scenario_id: str,
    *,
    started: float,
    expected_status: str | None,
    actual_status: str | None,
    seed: int | None,
    truth: float | None = None,
    estimate: float | None = None,
    bias: float | None = None,
    rmse: float | None = None,
    coverage: float | None = None,
    seeds: list[int] | None = None,
    metrics: dict | None = None,
) -> None:
    RECORDED.append({
        "scenario_id": scenario_id,
        "scenario": SCENARIO_MANIFEST[scenario_id],
        "dgp_version": "enh-e1a-v1",
        "seed": seed,
        "ground_truth": truth,
        "estimate": estimate,
        "bias": bias,
        "rmse": rmse,
        "ci_coverage": coverage,
        "expected_status": expected_status,
        "actual_status": actual_status,
        "runtime_seconds": time.perf_counter() - started,
        "package_versions": package_versions(),
        "seeds": seeds or ([] if seed is None else [seed]),
        "metrics": metrics or {},
    })


def test_sb_e1a_001_randomized_ate(tmp_path: Path) -> None:
    started = time.perf_counter()
    graph = {"graph_type": "DAG", "nodes": ["t", "y"], "edges": [EDGE("t", "y")]}
    graph_path = tmp_path / "graph.json"
    graph_path.write_text(json.dumps(graph), encoding="utf-8")
    truth, estimates, covered = 2.0, [], 0
    seeds = list(range(100, 200))
    for seed in seeds:
        rng = np.random.default_rng(seed)
        treatment = rng.binomial(1, 0.5, 500)
        dataset = tmp_path / f"rct-{seed}.csv"
        pd.DataFrame({"t": treatment, "y": truth * treatment + rng.normal(size=500)}).to_csv(dataset, index=False)
        output = EstimationAdapter().run(EstimationInput(
            dataset, graph_path, "difference_in_means", {}, {}, seed,
            _spec(strategy="RANDOMIZED", estimator="difference_in_means"),
        ), tmp_path / f"out-{seed}")[0]
        value = float(output.payload["estimate"])
        estimates.append(value)
        low, high = output.payload["confidence_interval"]
        covered += int(low <= truth <= high)
    mean = float(np.mean(estimates))
    bias = mean - truth
    rmse = float(np.sqrt(np.mean((np.asarray(estimates) - truth) ** 2)))
    coverage = covered / len(seeds)
    standardized = abs(bias) / abs(truth)
    assert standardized <= 0.10 and 0.90 <= coverage <= 0.98
    _record("SB-E1A-001", started=started, expected_status="ESTIMATED", actual_status="ESTIMATED",
            seed=seeds[0], truth=truth, estimate=mean, bias=bias, rmse=rmse, coverage=coverage,
            seeds=seeds, metrics={"standardized_absolute_bias": standardized})


def test_sb_e1a_002_observed_confounding(tmp_path: Path) -> None:
    started = time.perf_counter()
    results, dataset, graph = _identify(tmp_path, _frame(), BASE_GRAPH, ["x"])
    effect = EstimationAdapter().run(EstimationInput(
        dataset, graph, "ols", {}, {}, 42, _spec(adjustment=["x"], estimator="ols"),
    ), tmp_path / "estimate")[0]
    estimate = float(effect.payload["estimate"])
    assert results[0].scientific_status is ScientificStatus.IDENTIFIED
    _record("SB-E1A-002", started=started, expected_status="IDENTIFIED", actual_status=results[0].scientific_status.value,
            seed=42, truth=2.0, estimate=estimate, bias=estimate - 2.0)


def test_sb_e1a_003_missing_confounder(tmp_path: Path) -> None:
    started = time.perf_counter()
    results, _, _ = _identify(tmp_path, _frame(), BASE_GRAPH, [])
    assert results[0].scientific_status is ScientificStatus.NOT_IDENTIFIED
    _record("SB-E1A-003", started=started, expected_status="NOT_IDENTIFIED", actual_status=results[0].scientific_status.value, seed=42)


def test_sb_e1a_004_collider_adjustment(tmp_path: Path) -> None:
    started = time.perf_counter()
    frame = _frame()
    frame["u1"], frame["u2"] = frame["x"], frame["z"]
    frame["c"] = frame["u1"] + frame["u2"]
    frame["d"] = frame["c"] + 0.1
    graph = {"graph_type": "DAG", "nodes": ["id", "t", "u1", "c", "d", "u2", "y"], "edges": [
        EDGE("u1", "t"), EDGE("u1", "c"), EDGE("u2", "c"), EDGE("c", "d"), EDGE("u2", "y"),
    ]}
    results, _, _ = _identify(tmp_path, frame, graph, ["d"])
    codes = {item["code"] for item in results[0].payload["non_identification_reasons"]}
    assert results[0].scientific_status is ScientificStatus.NOT_IDENTIFIED and "COLLIDER_ADJUSTMENT" in codes
    _record("SB-E1A-004", started=started, expected_status="NOT_IDENTIFIED", actual_status=results[0].scientific_status.value, seed=42,
            metrics={"reason_codes": sorted(codes)})


def test_sb_e1a_005_post_treatment_adjustment(tmp_path: Path) -> None:
    started = time.perf_counter()
    results, _, _ = _identify(tmp_path, _frame(), BASE_GRAPH, ["m"])
    assert results[0].scientific_status is ScientificStatus.NOT_IDENTIFIED
    _record("SB-E1A-005", started=started, expected_status="NOT_IDENTIFIED", actual_status=results[0].scientific_status.value, seed=42)


def test_sb_e1a_006_poor_overlap(tmp_path: Path) -> None:
    started = time.perf_counter()
    results, _, _ = _identify(tmp_path, _frame(poor_overlap=True), BASE_GRAPH, ["x"])
    status = results[1].scientific_status.value
    assert status in {"WARN", "FAIL"}
    _record("SB-E1A-006", started=started, expected_status=status, actual_status=status, seed=42)


def _base_ipw(tmp_path: Path):
    frame = _frame()
    dataset, graph = _write(tmp_path, frame, BASE_GRAPH)
    spec = _spec(adjustment=["x"], estimator="ipw")
    effect = EstimationAdapter().run(EstimationInput(
        dataset, graph, "ipw", {}, {}, 42, spec,
    ), tmp_path / "base")[0]
    base = {"payload": effect.payload, "causal_question": spec["causal_question"], "causal_design": spec["causal_design"]}
    return dataset, graph, spec, effect, base


def test_sb_e1a_007_placebo(tmp_path: Path) -> None:
    started = time.perf_counter()
    dataset, graph, spec, _, base = _base_ipw(tmp_path)
    refute_spec = {**spec, "operation_spec": {"method": "PLACEBO_TREATMENT", "repetitions": 20}}
    result = RefutationAdapter().run(RefutationInput(
        dataset, graph, base, "PLACEBO_TREATMENT", {}, 42, refute_spec,
    ), tmp_path / "placebo")[0]
    assert result.scientific_status is ScientificStatus.NO_FAILURE_DETECTED
    _record("SB-E1A-007", started=started, expected_status="NO_FAILURE_DETECTED", actual_status=result.scientific_status.value,
            seed=42, truth=0.0, estimate=float(result.payload["refutation_estimate"]), bias=float(result.payload["refutation_estimate"]))


def test_sb_e1a_008_adjustment_variation(tmp_path: Path) -> None:
    started = time.perf_counter()
    dataset, graph, spec, _, base = _base_ipw(tmp_path)
    sensitivity_spec = {**spec, "operation_spec": {"dimension": "ADJUSTMENT_SET", "adjustment_sets": [["x"], ["x", "z"]]}}
    result = SensitivityAdapter().run(SensitivityInput(
        dataset, graph, base, "ADJUSTMENT_SET", {}, 42, sensitivity_spec,
    ), tmp_path / "adjustment")[0]
    assert len(result.payload["variation"]) == 2
    _record("SB-E1A-008", started=started, expected_status="ROBUST", actual_status=result.scientific_status.value, seed=42,
            metrics={"effect_range": result.payload["effect_range"]})


def test_sb_e1a_009_propensity_clipping(tmp_path: Path) -> None:
    started = time.perf_counter()
    dataset, graph, spec, _, base = _base_ipw(tmp_path)
    sensitivity_spec = {**spec, "operation_spec": {"dimension": "PROPENSITY_CLIPPING", "values": [0.01, 0.025, 0.05]}}
    result = SensitivityAdapter().run(SensitivityInput(
        dataset, graph, base, "PROPENSITY_CLIPPING", {}, 42, sensitivity_spec,
    ), tmp_path / "clipping")[0]
    assert len(result.payload["variation"]) == 3
    _record("SB-E1A-009", started=started, expected_status="ROBUST", actual_status=result.scientific_status.value, seed=42,
            metrics={"effect_range": result.payload["effect_range"]})


def test_sb_e1a_010_unresolved_cpdag_pag(tmp_path: Path) -> None:
    started = time.perf_counter()
    statuses = []
    for graph_type in ("CPDAG", "PAG"):
        case = tmp_path / graph_type
        case.mkdir()
        graph = {**BASE_GRAPH, "graph_type": graph_type}
        results, _, _ = _identify(case, _frame(), graph, ["x"])
        statuses.append(results[0].scientific_status.value)
    assert statuses == ["REQUIRES_REVIEW", "REQUIRES_REVIEW"]
    _record("SB-E1A-010", started=started, expected_status="REQUIRES_REVIEW", actual_status="REQUIRES_REVIEW", seed=42,
            metrics={"graph_statuses": {"CPDAG": statuses[0], "PAG": statuses[1]}})


def test_sb_e1a_011_semi_synthetic_ate_att(tmp_path: Path) -> None:
    started = time.perf_counter()
    raw = sm.datasets.longley.load_pandas().exog[["GNPDEFL", "GNP"]].to_numpy(dtype=float)
    fixed = np.tile((raw - raw.mean(axis=0)) / raw.std(axis=0), (30, 1))
    graph = {"graph_type": "DAG", "nodes": ["x1", "x2", "t", "y"], "edges": [
        EDGE("x1", "t"), EDGE("x2", "t"), EDGE("x1", "y"), EDGE("x2", "y"), EDGE("t", "y"),
    ]}
    graph_path = tmp_path / "graph.json"
    graph_path.write_text(json.dumps(graph), encoding="utf-8")
    truth, seeds, estimates, covered = 2.0, list(range(30)), [], 0
    per_estimand: dict[str, list[float]] = {"ATE": [], "ATT": []}
    for seed in seeds:
        rng = np.random.default_rng(seed)
        propensity = 1 / (1 + np.exp(-(0.8 * fixed[:, 0] - 0.5 * fixed[:, 1])))
        treatment = rng.binomial(1, propensity)
        outcome = truth * treatment + 0.7 * fixed[:, 0] - 0.4 * fixed[:, 1] + rng.normal(size=len(fixed))
        dataset = tmp_path / f"semi-{seed}.csv"
        pd.DataFrame({"x1": fixed[:, 0], "x2": fixed[:, 1], "t": treatment, "y": outcome}).to_csv(dataset, index=False)
        for estimand in ("ATE", "ATT"):
            output = EstimationAdapter().run(EstimationInput(
                dataset, graph_path, "ols", {}, {}, seed,
                _spec(adjustment=["x1", "x2"], estimator="ols", estimand=estimand),
            ), tmp_path / f"semi-{seed}-{estimand}")[0]
            value = float(output.payload["estimate"])
            estimates.append(value)
            per_estimand[estimand].append(value)
            low, high = output.payload["confidence_interval"]
            covered += int(low <= truth <= high)
    mean, coverage = float(np.mean(estimates)), covered / len(estimates)
    bias = mean - truth
    rmse = float(np.sqrt(np.mean((np.asarray(estimates) - truth) ** 2)))
    standardized = abs(bias) / truth
    assert standardized <= 0.10 and 0.90 <= coverage <= 0.98
    _record("SB-E1A-011", started=started, expected_status="ESTIMATED", actual_status="ESTIMATED",
            seed=seeds[0], truth=truth, estimate=mean, bias=bias, rmse=rmse, coverage=coverage,
            seeds=seeds, metrics={
                "standardized_absolute_bias": standardized,
                "ate_mean": float(np.mean(per_estimand["ATE"])),
                "att_mean": float(np.mean(per_estimand["ATT"])),
                "fixture": "statsmodels.datasets.longley",
            })


def test_zz_manifest_artifact_and_gate_are_complete(project_root: Path) -> None:
    assert len(RECORDED) == 11
    assert {item["scenario_id"] for item in RECORDED} == set(SCENARIO_MANIFEST)
    assert all(REQUIRED_SCENARIO_FIELDS <= set(item) for item in RECORDED)
    report = write_report(
        RECORDED,
        project_root / "test-results/scientific_benchmarks/ariadne_ENH-E1a.json",
    )
    assert report["gate_result"] == "PASS", report["checks"]
    assert all(item["package_versions"]["statsmodels"] != "NOT_INSTALLED" for item in RECORDED)


def test_zzz_gate_fails_at_threshold_violation() -> None:
    violating = copy.deepcopy(RECORDED)
    target = next(item for item in violating if item["scenario_id"] == "SB-E1A-001")
    target["metrics"]["standardized_absolute_bias"] = 0.1000001
    assert evaluate_gate(violating)["gate_result"] == "FAIL"
