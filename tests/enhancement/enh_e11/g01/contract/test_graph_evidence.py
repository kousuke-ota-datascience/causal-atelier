"""Pure P03 Graph wire tests using explicit synthetic endpoint expectations."""
import hashlib
from dataclasses import replace

import pytest

from ariadne.causal.discovery.graph_evidence import GraphEvidence
from ariadne.shared.content_ref import ContractViolation
from ariadne.shared.graph_semantics import GraphSemanticsValidator
from ariadne.shared.serialization import jcs

ENDPOINTS = (
    ("TAIL", "TAIL"), ("TAIL", "ARROW"), ("TAIL", "CIRCLE"),
    ("ARROW", "TAIL"), ("ARROW", "ARROW"), ("ARROW", "CIRCLE"),
    ("CIRCLE", "TAIL"), ("CIRCLE", "ARROW"), ("CIRCLE", "CIRCLE"),
)


def _graph(*, source="left", target="right", marks=("CIRCLE", "ARROW")):
    refs = {
        name: {"identity": name, "relative_key": f"inputs/{name}.json", "sha256": "a" * 64,
               "media_type": "application/json", "schema_version": None}
        for name in ("question", "design", "dataset")
    }
    return {
        "schema_version": "e11-local-graph/1", "kind": "PAG", "version_id": None, "parent_version_id": None,
        "nodes": ["right", "left"],
        "edges": [{"source": source, "target": target, "source_mark": marks[0], "target_mark": marks[1], "lag": None}],
        "temporal": None,
        "provenance": {"method_id": "P1-M06", "backend": "causal-learn", "ci_test": "gsq",
                       "assumptions": ["declared-assumption"], "source_refs": refs, "parent_graph_ref": None},
    }


def _encode(graph):
    return jcs.canonical_bytes({**graph, "content_hash": jcs.digest(graph)})


@pytest.mark.parametrize("marks", ENDPOINTS)
@pytest.mark.parametrize("reverse", [False, True])
def test_every_pag_endpoint_pair_and_orientation_round_trips(marks, reverse):
    expected = _graph(source="right", target="left", marks=marks[::-1]) if reverse else _graph(marks=marks)
    raw = _encode(expected)
    graph = GraphEvidence.from_canonical_json(raw)
    assert jcs.canonical_bytes(graph.canonical_payload()) == raw
    assert graph.content_hash == hashlib.sha256(jcs.canonical_bytes(expected)).hexdigest()
    assert graph.content_hash != hashlib.sha256(raw).hexdigest()
    assert graph.provenance.source_refs.dataset.relative_key == "inputs/dataset.json"
    document = GraphSemanticsValidator.to_product_document(graph.kind, graph.nodes, graph.edges)
    expected_edge = expected["edges"][0]
    assert document["edges"] == [{
        "source": expected_edge["source"], "target": expected_edge["target"],
        "endpoint_source": expected_edge["source_mark"], "endpoint_target": expected_edge["target_mark"],
    }]
    assert GraphSemanticsValidator.from_product_endpoints(graph.kind, document) == (graph.nodes, graph.edges)


@pytest.mark.parametrize("replacement", [
    {"version_id": "product-id"}, {"parent_version_id": "product-parent"}, {"kind": "DAG"},
    {"temporal": {"time_index_policy": "index", "lag_direction": "forward"}},
    {"nodes": ["left", "left"]}, {"nodes": []}, {"schema_version": "2.0"}, {"unknown": None},
    {"provenance": {}},
])
def test_rejects_invalid_graph_fields(replacement):
    with pytest.raises(ContractViolation):
        GraphEvidence.from_canonical_json(_encode({**_graph(), **replacement}))


@pytest.mark.parametrize(("key", "value"), [
    ("source", "unobserved"), ("source", "right"), ("lag", 0), ("source_mark", "circle"),
    ("source_mark", "UNKNOWN"), ("target_mark", None), ("target", ["right"]),
])
def test_rejects_invalid_edges(key, value):
    data = _graph()
    data["edges"][0][key] = value
    with pytest.raises(ContractViolation):
        GraphEvidence.from_canonical_json(_encode(data))


@pytest.mark.parametrize("reverse", [False, True])
def test_rejects_duplicate_endpoint_pairs(reverse):
    data = _graph()
    edge = data["edges"][0]
    data["edges"].append(
        {**edge, "source": edge["target"], "target": edge["source"],
         "source_mark": edge["target_mark"], "target_mark": edge["source_mark"]} if reverse else dict(edge)
    )
    with pytest.raises(ContractViolation, match="Duplicate"):
        GraphEvidence.from_canonical_json(_encode(data))


@pytest.mark.parametrize(("field", "value"), [
    ("method_id", "P1-M05"), ("backend", "other"), ("ci_test", None), ("ci_test", "other"),
    ("assumptions", ["same", "same"]), ("assumptions", [False]), ("science_acceptance", "PASS"),
    ("source_refs", {}), ("parent_graph_ref", {"identity": "parent", "relative_key": "runs/id/graph.json",
                                            "sha256": "a" * 64, "media_type": "application/json",
                                            "schema_version": "e11-local-graph/1"}),
])
def test_rejects_invalid_g01_provenance(field, value):
    data = _graph()
    data["provenance"][field] = value
    with pytest.raises(ContractViolation):
        GraphEvidence.from_canonical_json(_encode(data))


def test_strict_json_digest_and_immutable_values():
    data = _graph()
    raw = _encode(data)
    graph = GraphEvidence.from_canonical_json(raw)
    data["provenance"]["assumptions"].append("new")
    exported = graph.canonical_payload()
    exported["provenance"]["source_refs"]["dataset"]["identity"] = "new"
    assert jcs.canonical_bytes(graph.canonical_payload()) == raw
    with pytest.raises(ContractViolation, match="semantic digest"):
        replace(graph, content_hash=hashlib.sha256(raw).hexdigest())
    with pytest.raises(ContractViolation, match="Invalid strict Graph JSON"):
        GraphEvidence.from_canonical_json(raw.replace(b'"kind":"PAG"', b'"kind":"PAG","kind":"PAG"'))


@pytest.mark.parametrize("key", ["relative_key", "sha256"])
def test_rejects_malformed_content_ref(key):
    data = _graph()
    data["provenance"]["source_refs"]["dataset"][key] = "invalid/../hash"
    with pytest.raises(ContractViolation):
        GraphEvidence.from_canonical_json(_encode(data))
