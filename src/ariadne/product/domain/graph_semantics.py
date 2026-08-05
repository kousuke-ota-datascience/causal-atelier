"""Canonical graph document validation shared by domain services and adapters."""

from __future__ import annotations

from typing import Any

from ariadne.product.domain.enums import GraphType
from ariadne.product.domain.errors import InvalidGraphSemantics

_ENDPOINTS = {"TAIL", "ARROW", "CIRCLE"}
_ALLOWED_BY_TYPE = {
    GraphType.DAG: {("TAIL", "ARROW")},
    GraphType.CPDAG: {("TAIL", "ARROW"), ("ARROW", "TAIL"), ("TAIL", "TAIL")},
    GraphType.PAG: {(left, right) for left in _ENDPOINTS for right in _ENDPOINTS},
}


def validate_graph_document(graph_type: GraphType, graph: dict[str, Any]) -> None:
    """Reject graph documents that lose node or endpoint semantics."""
    declared = graph.get("graph_type")
    if declared is not None and declared != graph_type.value:
        raise InvalidGraphSemantics(
            f"graph.graph_type={declared!r} does not match {graph_type.value!r}"
        )
    nodes = graph.get("nodes")
    edges = graph.get("edges")
    if not isinstance(nodes, list) or not all(isinstance(node, str) and node for node in nodes):
        raise InvalidGraphSemantics("graph.nodes must be a list of non-empty strings")
    if len(nodes) != len(set(nodes)):
        raise InvalidGraphSemantics("graph.nodes must be unique")
    if not isinstance(edges, list):
        raise InvalidGraphSemantics("graph.edges must be a list")
    node_set = set(nodes)
    seen: set[tuple[str, str, str, str]] = set()
    for edge in edges:
        if not isinstance(edge, dict):
            raise InvalidGraphSemantics("each graph edge must be an object")
        source = edge.get("source")
        target = edge.get("target")
        left = str(edge.get("endpoint_source", "")).upper()
        right = str(edge.get("endpoint_target", "")).upper()
        if source not in node_set or target not in node_set or source == target:
            raise InvalidGraphSemantics("edge endpoints must be distinct declared nodes")
        if left not in _ENDPOINTS or right not in _ENDPOINTS:
            raise InvalidGraphSemantics("edge endpoints must be TAIL, ARROW, or CIRCLE")
        if (left, right) not in _ALLOWED_BY_TYPE[graph_type]:
            raise InvalidGraphSemantics(
                f"endpoint pair {(left, right)!r} is invalid for {graph_type.value}"
            )
        key = (str(source), str(target), left, right)
        reverse = (str(target), str(source), right, left)
        if key in seen or reverse in seen:
            raise InvalidGraphSemantics("duplicate graph edge")
        seen.add(key)


def canonical_graph(graph_type: GraphType, graph: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic graph representation after validation."""
    validate_graph_document(graph_type, graph)
    nodes = sorted(graph["nodes"])
    edges = [
        {
            **edge,
            "endpoint_source": str(edge["endpoint_source"]).upper(),
            "endpoint_target": str(edge["endpoint_target"]).upper(),
        }
        for edge in graph["edges"]
    ]
    edges.sort(
        key=lambda edge: (
            edge["source"], edge["target"], edge["endpoint_source"], edge["endpoint_target"]
        )
    )
    return {**graph, "graph_type": graph_type.value, "nodes": nodes, "edges": edges}
