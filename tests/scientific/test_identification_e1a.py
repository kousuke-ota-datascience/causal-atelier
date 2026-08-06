from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from ariadne.product.domain.enums import ResultType, ScientificStatus
from ariadne.product.ports.scientific_core import IdentificationInput
from ariadne.scientific.identification.adapter import IdentificationAdapter


def _edge(source: str, target: str) -> dict[str, str]:
    return {
        "source": source,
        "target": target,
        "endpoint_source": "TAIL",
        "endpoint_target": "ARROW",
    }


def _spec(*, strategy: str = "BACKDOOR", adjustment: list[str] | None = None) -> dict:
    return {
        "schema_version": "causal-analysis-spec/2",
        "analysis_mode": "EXPLORATORY",
        "research_context": {},
        "causal_question": {
            "population": "rows",
            "treatment": "treatment",
            "comparator": "untreated",
            "outcome": "outcome",
            "analysis_unit": "row",
            "treatment_time": "t0",
            "outcome_window": "t1",
            "estimand": "ATE",
        },
        "causal_design": {
            "identification_strategy": strategy,
            "adjustment_set": adjustment or [],
            "assumptions": ["declared design assumptions"],
        },
        "operation_spec": {"allow_partial_identification": False},
        "validation_override": None,
    }


def _run(
    tmp_path: Path,
    frame: pd.DataFrame,
    *,
    nodes: list[str],
    edges: list[dict[str, str]],
    graph_type: str = "DAG",
    strategy: str = "BACKDOOR",
    adjustment: list[str] | None = None,
):
    dataset = tmp_path / "data.csv"
    frame.to_csv(dataset, index=False)
    graph = tmp_path / "graph.json"
    graph.write_text(
        json.dumps({"graph_type": graph_type, "nodes": nodes, "edges": edges}),
        encoding="utf-8",
    )
    results = IdentificationAdapter().run(
        IdentificationInput(
            dataset_path=dataset,
            graph_path=graph,
            method="GRAPHICAL_IDENTIFICATION",
            analysis_spec=_spec(strategy=strategy, adjustment=adjustment),
        ),
        tmp_path / "out",
    )
    identification = next(r for r in results if r.result_type is ResultType.IDENTIFICATION_RESULT)
    eligibility = next(r for r in results if r.result_type is ResultType.DATA_ELIGIBILITY_RESULT)
    return identification, eligibility


def _base_frame(n: int = 120) -> pd.DataFrame:
    return pd.DataFrame({
        "row": range(n),
        "x": [float(i % 7) for i in range(n)],
        "treatment": [i % 2 for i in range(n)],
        "outcome": [1.5 + i % 11 for i in range(n)],
    })


@pytest.mark.requirement("FR-050", "FR-054", "FR-064", "FR-065")
@pytest.mark.parametrize(
    ("column", "values", "expected_treatment", "expected_outcome"),
    [
        ("treatment", ["control", "treated"] * 60, "UNSUPPORTED", "CONTINUOUS"),
        ("outcome", ["low", "high"] * 60, "BINARY", "UNSUPPORTED"),
    ],
)
def test_eligibility_type_failure_is_a_saved_scientific_result(
    tmp_path: Path,
    column: str,
    values: list[str],
    expected_treatment: str,
    expected_outcome: str,
) -> None:
    frame = _base_frame()
    frame[column] = values
    _, eligibility = _run(
        tmp_path,
        frame,
        nodes=["x", "treatment", "outcome"],
        edges=[_edge("x", "treatment"), _edge("x", "outcome"), _edge("treatment", "outcome")],
        adjustment=["x"],
    )

    assert eligibility.scientific_status is ScientificStatus.FAIL
    assert eligibility.payload["inferred_types"]["treatment"]["type"] == expected_treatment
    assert eligibility.payload["inferred_types"]["outcome"]["type"] == expected_outcome
    checks = {item["check_code"]: item for item in eligibility.payload["checks"]}
    assert checks["TYPE_COMPATIBILITY"]["status"] == "FAIL"
    assert checks["TREATMENT_PREVALENCE"]["status"] == "SKIPPED_DUE_TO_PREREQUISITE"
    assert checks["LIMITED_OVERLAP"]["status"] == "SKIPPED_DUE_TO_PREREQUISITE"


@pytest.mark.requirement("FR-050", "FR-064", "FR-065")
def test_missing_required_column_records_explicit_prerequisite_skips(tmp_path: Path) -> None:
    frame = _base_frame().drop(columns="outcome")
    identification, eligibility = _run(
        tmp_path,
        frame,
        nodes=["x", "treatment", "outcome"],
        edges=[_edge("x", "treatment"), _edge("x", "outcome")],
        adjustment=["x"],
    )
    assert identification.scientific_status is ScientificStatus.NOT_IDENTIFIED
    assert eligibility.scientific_status is ScientificStatus.FAIL
    checks = {item["check_code"]: item for item in eligibility.payload["checks"]}
    assert checks["REQUIRED_COLUMNS"]["status"] == "FAIL"
    assert checks["TYPE_COMPATIBILITY"]["status"] == "SKIPPED_DUE_TO_PREREQUISITE"


@pytest.mark.requirement("FR-050", "FR-064", "FR-065")
@pytest.mark.parametrize(
    ("frame", "expected_status", "expected_check", "expected_check_status"),
    [
        (
            _base_frame().assign(treatment=0),
            ScientificStatus.FAIL,
            "CONSTANT_COLUMNS",
            "FAIL",
        ),
        (
            _base_frame(12),
            ScientificStatus.FAIL,
            "SAMPLE_SIZE",
            "FAIL",
        ),
        (
            _base_frame().assign(x=float("nan")),
            ScientificStatus.FAIL,
            "PROPENSITY_ESTIMATION",
            "WARN",
        ),
    ],
    ids=["one-treatment-arm", "small-sample", "propensity-not-estimable"],
)
def test_eligibility_edge_cases_are_results_not_exceptions(
    tmp_path: Path,
    frame: pd.DataFrame,
    expected_status: ScientificStatus,
    expected_check: str,
    expected_check_status: str,
) -> None:
    _, eligibility = _run(
        tmp_path,
        frame,
        nodes=["x", "treatment", "outcome"],
        edges=[_edge("x", "treatment"), _edge("x", "outcome"), _edge("treatment", "outcome")],
        adjustment=["x"],
    )
    checks = {item["check_code"]: item for item in eligibility.payload["checks"]}
    assert eligibility.scientific_status is expected_status
    assert checks[expected_check]["status"] == expected_check_status
    if expected_check == "PROPENSITY_ESTIMATION":
        assert checks[expected_check]["evidence"]["exception_type"]


@pytest.mark.requirement("FR-038", "FR-039", "FR-064", "FR-067")
def test_cpdags_do_not_hide_deterministic_input_errors(tmp_path: Path) -> None:
    identification, _ = _run(
        tmp_path,
        _base_frame(),
        nodes=["x", "outcome"],
        edges=[],
        graph_type="CPDAG",
    )
    codes = {reason["code"] for reason in identification.payload["non_identification_reasons"]}
    assert identification.scientific_status is ScientificStatus.NOT_IDENTIFIED
    assert {"MISSING_TREATMENT_NODE", "UNRESOLVED_GRAPH_ORIENTATION"} <= codes


@pytest.mark.requirement("FR-066", "FR-067")
def test_consistent_cpdags_remain_reviewable(tmp_path: Path) -> None:
    identification, _ = _run(
        tmp_path,
        _base_frame(),
        nodes=["treatment", "outcome"],
        edges=[{
            "source": "treatment",
            "target": "outcome",
            "endpoint_source": "TAIL",
            "endpoint_target": "TAIL",
        }],
        graph_type="CPDAG",
    )
    assert identification.scientific_status is ScientificStatus.REQUIRES_REVIEW


@pytest.mark.requirement("FR-038", "FR-039")
def test_randomized_design_allows_valid_pretreatment_adjustment(tmp_path: Path) -> None:
    identification, _ = _run(
        tmp_path,
        _base_frame(),
        nodes=["x", "treatment", "outcome"],
        edges=[_edge("x", "outcome"), _edge("treatment", "outcome")],
        strategy="RANDOMIZED",
        adjustment=["x"],
    )
    assert identification.scientific_status is ScientificStatus.IDENTIFIED


@pytest.mark.requirement("FR-038", "FR-039")
def test_randomized_design_rejects_post_treatment_adjustment(tmp_path: Path) -> None:
    frame = _base_frame()
    frame["mediator"] = frame["treatment"] + 1
    identification, _ = _run(
        tmp_path,
        frame,
        nodes=["treatment", "mediator", "outcome"],
        edges=[_edge("treatment", "mediator"), _edge("mediator", "outcome")],
        strategy="RANDOMIZED",
        adjustment=["mediator"],
    )
    assert identification.scientific_status is ScientificStatus.NOT_IDENTIFIED
    assert "POST_TREATMENT_ADJUSTMENT" in {
        reason["code"] for reason in identification.payload["non_identification_reasons"]
    }


@pytest.mark.requirement("FR-038", "FR-039")
def test_collider_descendant_adjustment_is_path_relative(tmp_path: Path) -> None:
    frame = _base_frame()
    for column in ["u1", "u2", "collider", "descendant"]:
        frame[column] = [float(i % 5) for i in range(len(frame))]
    identification, _ = _run(
        tmp_path,
        frame,
        nodes=["treatment", "u1", "collider", "u2", "outcome", "descendant"],
        edges=[
            _edge("u1", "treatment"),
            _edge("u1", "collider"),
            _edge("u2", "collider"),
            _edge("u2", "outcome"),
            _edge("collider", "descendant"),
        ],
        adjustment=["descendant"],
    )
    collider_reason = next(
        reason for reason in identification.payload["non_identification_reasons"]
        if reason["code"] == "COLLIDER_ADJUSTMENT"
    )
    assert identification.scientific_status is ScientificStatus.NOT_IDENTIFIED
    assert collider_reason["evidence"]["activated_paths"]


@pytest.mark.requirement("FR-038", "FR-039")
def test_irrelevant_high_indegree_covariate_is_not_called_a_collider(tmp_path: Path) -> None:
    frame = _base_frame()
    for column in ["a", "b", "z"]:
        frame[column] = [float(i % 3) for i in range(len(frame))]
    identification, _ = _run(
        tmp_path,
        frame,
        nodes=["x", "treatment", "outcome", "a", "b", "z"],
        edges=[
            _edge("x", "treatment"),
            _edge("x", "outcome"),
            _edge("treatment", "outcome"),
            _edge("a", "z"),
            _edge("b", "z"),
        ],
        adjustment=["x", "z"],
    )
    codes = {reason["code"] for reason in identification.payload["non_identification_reasons"]}
    assert identification.scientific_status is ScientificStatus.IDENTIFIED
    assert "COLLIDER_ADJUSTMENT" not in codes
