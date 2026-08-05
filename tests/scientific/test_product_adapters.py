from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from ariadne.product.domain.enums import ScientificStatus
from ariadne.product.ports.scientific_core import DiscoveryInput, EstimationInput
from ariadne.scientific.discovery.adapter import DiscoveryAdapter
from ariadne.scientific.inference.adapter import EstimationAdapter


@pytest.fixture
def synthetic(tmp_path: Path):
    rng=np.random.default_rng(20260805);n=300
    x=rng.normal(size=n);t=rng.binomial(1,1/(1+np.exp(-.6*x)));y=2*t+.8*x+rng.normal(scale=.5,size=n)
    path=tmp_path/"sales.csv";pd.DataFrame({"x":x,"treatment":t,"sales":y,"unused":rng.normal(size=n)}).to_csv(path,index=False)
    graph={"graph_type":"DAG","nodes":["x","treatment","sales"],"edges":[
        {"source":"x","target":"treatment","endpoint_source":"TAIL","endpoint_target":"ARROW"},
        {"source":"x","target":"sales","endpoint_source":"TAIL","endpoint_target":"ARROW"},
        {"source":"treatment","target":"sales","endpoint_source":"TAIL","endpoint_target":"ARROW"},
    ]};graph_path=tmp_path/"graph.json";graph_path.write_text(json.dumps(graph),encoding="utf-8")
    return path,graph_path


@pytest.mark.parametrize("algorithm", ["pc", "ges"])
def test_pc_and_ges_run_without_database_and_preserve_graph_semantics(synthetic, tmp_path, algorithm):  # type: ignore[no-untyped-def]
    dataset,_=synthetic
    output=DiscoveryAdapter().run(DiscoveryInput(
        dataset_path=dataset,algorithm=algorithm,parameters={"alpha":.05} if algorithm=="pc" else {},
        random_seed=42,analysis_spec={"feature_columns":["x","treatment","sales"],"constraints":{}},
    ),tmp_path/algorithm)
    assert output.scientific_status is ScientificStatus.VALID
    assert output.graph_type=="CPDAG"
    assert output.graph_json["nodes"]==["sales","treatment","x"]
    assert all(set(edge)>= {"endpoint_source","endpoint_target"} for edge in output.graph_json["edges"])


@pytest.mark.parametrize("estimator,tolerance", [
    ("difference_in_means", .7), ("ols", .25), ("ipw", .4), ("aipw", .3),
])
def test_estimators_use_explicit_adjustment_and_recover_ate(synthetic,tmp_path,estimator,tolerance):  # type: ignore[no-untyped-def]
    dataset,graph=synthetic
    output=EstimationAdapter().run(EstimationInput(
        dataset_path=dataset,graph_path=graph,estimator=estimator,parameters={},random_seed=42,
        analysis_spec={"treatment":"treatment","outcome":"sales","estimand":"ATE",
                       "target_population":None,"adjustment_set":["x"],"assumptions":[],"inference_options":{}},
    ),tmp_path/estimator)
    assert output.scientific_status is ScientificStatus.VALID
    assert output.payload["adjustment_set"]==["x"]
    assert abs(output.payload["estimate"]-2)<tolerance
    assert output.payload["confidence_interval"] is not None
    assert "sample_size" in output.diagnostics and "balance" in output.diagnostics


def test_small_sample_is_scientific_result_not_exception(synthetic,tmp_path):  # type: ignore[no-untyped-def]
    dataset,graph=synthetic;small=tmp_path/"small.csv";pd.read_csv(dataset).head(8).to_csv(small,index=False)
    output=EstimationAdapter().run(EstimationInput(
        dataset_path=small,graph_path=graph,estimator="ols",analysis_spec={
            "treatment":"treatment","outcome":"sales","estimand":"ATT","target_population":None,
            "adjustment_set":["x"],"assumptions":[],"inference_options":{}},
    ),tmp_path/"small")
    assert output.scientific_status is ScientificStatus.INSUFFICIENT_SAMPLE


def test_missing_treatment_to_outcome_path_is_not_identified(synthetic, tmp_path):  # type: ignore[no-untyped-def]
    dataset, graph = synthetic
    graph_document = json.loads(graph.read_text(encoding="utf-8"))
    graph_document["edges"] = graph_document["edges"][:2]
    no_path = tmp_path / "no_path.json"
    no_path.write_text(json.dumps(graph_document), encoding="utf-8")
    output = EstimationAdapter().run(EstimationInput(
        dataset_path=dataset, graph_path=no_path, estimator="ols", parameters={},
        analysis_spec={"treatment":"treatment","outcome":"sales","estimand":"ATE",
                       "target_population":None,"adjustment_set":["x"],"assumptions":[],"inference_options":{}},
    ), tmp_path / "not-identified")
    assert output.scientific_status is ScientificStatus.NOT_IDENTIFIED


def test_extreme_propensity_is_insufficient_overlap(synthetic, tmp_path):  # type: ignore[no-untyped-def]
    dataset, graph = synthetic
    frame = pd.read_csv(dataset)
    frame["x"] = np.linspace(-20, 20, len(frame))
    frame["treatment"] = (frame["x"] > 0).astype(int)
    separated = tmp_path / "separated.csv"
    frame.to_csv(separated, index=False)
    output = EstimationAdapter().run(EstimationInput(
        dataset_path=separated, graph_path=graph, estimator="ipw", parameters={},
        analysis_spec={"treatment":"treatment","outcome":"sales","estimand":"ATE",
                       "target_population":None,"adjustment_set":["x"],"assumptions":[],"inference_options":{}},
    ), tmp_path / "overlap")
    assert output.scientific_status is ScientificStatus.INSUFFICIENT_OVERLAP


def test_non_estimable_aipw_uncertainty_is_unreliable(tmp_path: Path) -> None:
    rng = np.random.default_rng(7)
    columns = [f"x{index}" for index in range(5)]
    frame = pd.DataFrame(rng.normal(size=(30, 5)), columns=columns)
    frame["treatment"] = [1] * 5 + [0] * 25
    frame["sales"] = rng.normal(size=30)
    dataset = tmp_path / "unreliable.csv"
    frame.to_csv(dataset, index=False)
    graph_document = {
        "graph_type": "DAG", "nodes": [*columns, "treatment", "sales"],
        "edges": [{"source":"treatment","target":"sales",
                   "endpoint_source":"TAIL","endpoint_target":"ARROW"}],
    }
    graph = tmp_path / "unreliable_graph.json"
    graph.write_text(json.dumps(graph_document), encoding="utf-8")
    output = EstimationAdapter().run(EstimationInput(
        dataset_path=dataset, graph_path=graph, estimator="aipw", parameters={},
        analysis_spec={"treatment":"treatment","outcome":"sales","estimand":"ATE",
                       "target_population":None,"adjustment_set":columns,"assumptions":[],"inference_options":{}},
    ), tmp_path / "unreliable")
    assert output.scientific_status is ScientificStatus.ESTIMATION_UNRELIABLE
