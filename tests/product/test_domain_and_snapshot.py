from __future__ import annotations

import pytest

from ariadne.product.application.execution_service import _compute_snapshot_hash
from ariadne.product.domain.enums import GraphType, ScientificStatus
from ariadne.product.domain.errors import InvalidGraphSemantics, InvalidStateTransition
from ariadne.product.domain.execution import Execution
from ariadne.product.domain.graph_semantics import canonical_graph


def test_scientific_status_is_exact_design_contract():
    assert {item.value for item in ScientificStatus} == {
        "VALID", "NOT_IDENTIFIED", "INSUFFICIENT_OVERLAP",
        "INSUFFICIENT_SAMPLE", "ESTIMATION_UNRELIABLE",
    }


def test_snapshot_hash_is_order_stable_and_includes_context():
    first = _compute_snapshot_hash(objective="q", parameters={"b": 2, "a": 1.0}, null=None)
    second = _compute_snapshot_hash(null=None, parameters={"a": 1, "b": 2.0}, objective="q")
    assert first == second
    assert first != _compute_snapshot_hash(objective="different", parameters={"a": 1, "b": 2}, null=None)
    assert _compute_snapshot_hash(value=-0.0) == _compute_snapshot_hash(value=0)
    assert _compute_snapshot_hash(value=2**60) != _compute_snapshot_hash(value=2**60 + 1)


def test_graph_round_trip_preserves_endpoints():
    graph = {"graph_type": "CPDAG", "nodes": ["y", "x"], "edges": [
        {"source": "x", "target": "y", "endpoint_source": "tail", "endpoint_target": "arrow"}
    ]}
    assert canonical_graph(GraphType.CPDAG, graph) == {
        "graph_type": "CPDAG", "nodes": ["x", "y"], "edges": [
            {"source": "x", "target": "y", "endpoint_source": "TAIL", "endpoint_target": "ARROW"}
        ]
    }
    with pytest.raises(InvalidGraphSemantics):
        canonical_graph(GraphType.DAG, {**graph, "graph_type": "DAG", "edges": [
            {"source": "x", "target": "y", "endpoint_source": "TAIL", "endpoint_target": "TAIL"}
        ]})


def test_execution_state_machine_rejects_invalid_transition():
    execution = Execution()
    with pytest.raises(InvalidStateTransition):
        execution.mark_succeeded(None)  # type: ignore[arg-type]
