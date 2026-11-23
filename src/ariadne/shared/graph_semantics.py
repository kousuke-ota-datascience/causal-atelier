"""Explicit bridge from E11 endpoint names to the shared Product graph rules."""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from ariadne.product.domain.enums import GraphType
from ariadne.product.domain.errors import InvalidGraphSemantics
from ariadne.product.domain.graph_semantics import validate_graph_document
from ariadne.shared.content_ref import ContractViolation, nonempty_text

GraphKind = GraphType
_MARKS = ("TAIL", "ARROW", "CIRCLE")


@dataclass(frozen=True)
class EndpointEdge:
    source: str
    target: str
    source_mark: str
    target_mark: str
    lag: int | None


def graph_error(message: str, *, code: str = "SCHEMA_INVALID") -> ContractViolation:
    return ContractViolation(code, "graph", message)


class GraphSemanticsValidator:
    @staticmethod
    def to_product_document(
        kind: GraphKind, nodes: Iterable[str], edges: Iterable[EndpointEdge],
    ) -> dict[str, object]:
        """Validate the endpoint projection and preserve node and edge order."""
        if type(kind) is not GraphKind:
            raise graph_error("Unknown graph kind")
        values = list(nodes)
        if not values or not all(nonempty_text(node) for node in values):
            raise graph_error("Expected nonempty graph node identifiers")
        mapped = []
        pairs = set()
        for edge in edges:
            if (
                type(edge) is not EndpointEdge
                or not nonempty_text(edge.source) or not nonempty_text(edge.target)
                or edge.source_mark not in _MARKS or edge.target_mark not in _MARKS
            ):
                raise graph_error("Invalid graph edge endpoints or marks")
            pair = frozenset((edge.source, edge.target))
            if pair in pairs:
                raise graph_error("Duplicate or reversed graph edge")
            pairs.add(pair)
            mapped.append({
                "source": edge.source, "target": edge.target,
                "endpoint_source": edge.source_mark, "endpoint_target": edge.target_mark,
            })
        document = {"graph_type": kind.value, "nodes": values, "edges": mapped}
        try:
            validate_graph_document(kind, document)
        except InvalidGraphSemantics as error:
            raise graph_error(str(error)) from error
        return document

    @staticmethod
    def from_product_endpoints(
        kind: GraphKind, document: dict[str, object],
    ) -> tuple[tuple[str, ...], tuple[EndpointEdge, ...]]:
        """Read the Product endpoint ABI without converting any version IDs."""
        try:
            validate_graph_document(kind, document)
            edges = tuple(
                EndpointEdge(edge["source"], edge["target"], edge["endpoint_source"].upper(),
                             edge["endpoint_target"].upper(), None)
                for edge in document["edges"]
            )
        except (InvalidGraphSemantics, TypeError, AttributeError, KeyError) as error:
            raise graph_error("Invalid Product graph endpoint document") from error
        nodes = tuple(document["nodes"])
        GraphSemanticsValidator.to_product_document(kind, nodes, edges)
        return nodes, edges
