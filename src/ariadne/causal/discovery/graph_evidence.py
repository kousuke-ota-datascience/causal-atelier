"""Strict immutable E11 Graph evidence and its declared provenance."""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass

from ariadne.causal.design.study import ValidatedStudy
from ariadne.shared.content_ref import ContentRef, nonempty_text, valid_sha256
from ariadne.shared.graph_semantics import EndpointEdge, GraphKind, GraphSemanticsValidator, graph_error
from ariadne.shared.serialization import jcs

GRAPH_VERSION = "e11-local-graph/1"
_SOURCE_NAMES = ("question", "design", "dataset")
_CI_TESTS = ("fisherz", "chisq", "gsq")


def _exact_object(value: object, fields: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping) or set(value) != set(fields.split()):
        raise graph_error(f"Expected exactly these Graph fields: {fields}")
    return value


@dataclass(frozen=True)
class GraphSourceRefs:
    question: ContentRef
    design: ContentRef
    dataset: ContentRef

    def __post_init__(self) -> None:
        if any(type(getattr(self, name)) is not ContentRef for name in _SOURCE_NAMES):
            raise graph_error("Graph sources must be validated ContentRefs")

    @classmethod
    def from_payload(cls, value: object) -> GraphSourceRefs:
        fields = _exact_object(value, "question design dataset")
        return cls(**{name: ContentRef.from_payload(fields[name]) for name in _SOURCE_NAMES})

    def to_payload(self) -> dict[str, object]:
        return {name: getattr(self, name).to_payload() for name in _SOURCE_NAMES}


@dataclass(frozen=True)
class GraphProvenance:
    method_id: str
    backend: str
    ci_test: str | None
    assumptions: tuple[str, ...]
    source_refs: GraphSourceRefs
    parent_graph_ref: ContentRef | None

    def __post_init__(self) -> None:
        if not nonempty_text(self.method_id) or not nonempty_text(self.backend):
            raise graph_error("Missing Graph Method or Backend")
        if self.ci_test is not None and not nonempty_text(self.ci_test):
            raise graph_error("Invalid Graph CI test")
        if (
            type(self.assumptions) is not tuple or not all(nonempty_text(label) for label in self.assumptions)
            or len(set(self.assumptions)) != len(self.assumptions)
        ):
            raise graph_error("Invalid or duplicate Graph assumption label")
        if type(self.source_refs) is not GraphSourceRefs:
            raise graph_error("Invalid Graph source reference group")
        if self.parent_graph_ref is not None and type(self.parent_graph_ref) is not ContentRef:
            raise graph_error("Invalid parent Graph reference")

    @classmethod
    def from_payload(cls, value: object) -> GraphProvenance:
        items = _exact_object(value, "method_id backend ci_test assumptions source_refs parent_graph_ref")
        assumptions = items["assumptions"]
        if type(assumptions) is not list:
            raise graph_error("Graph assumption labels must be a JSON array")
        parent = items["parent_graph_ref"]
        return cls(
            items["method_id"], items["backend"], items["ci_test"], tuple(assumptions),
            GraphSourceRefs.from_payload(items["source_refs"]),
            None if parent is None else ContentRef.from_payload(parent),
        )

    def to_payload(self) -> dict[str, object]:
        return {
            "method_id": self.method_id, "backend": self.backend, "ci_test": self.ci_test,
            "assumptions": list(self.assumptions), "source_refs": self.source_refs.to_payload(),
            "parent_graph_ref": self.parent_graph_ref.to_payload() if self.parent_graph_ref is not None else None,
        }

    def validate_g01(self) -> None:
        if (
            (self.method_id, self.backend) != ("P1-M06", "causal-learn")
            or self.ci_test not in _CI_TESTS or self.parent_graph_ref is not None
        ):
            raise graph_error("Invalid Method, Backend, CI or parent for standalone G01 DISCOVER")

    def validate_lineage(
        self, study: ValidatedStudy, *, lineage: Mapping[str, object], execution: Mapping[str, object],
    ) -> None:
        """Compare declared scientific values. Trusted file-byte verification is an I/O responsibility."""
        method = study.to_payload()["method"]
        if (
            (self.method_id, self.backend, self.ci_test)
            != (method["id"], method["backend"], method["config"]["indep_test"])
            or (self.method_id, self.backend) != (execution["method"], execution["backend"])
        ):
            raise graph_error("Graph Method, Backend or CI does not agree with Study and Manifest")
        for name in _SOURCE_NAMES:
            ref = getattr(self.source_refs, name)
            if ref != getattr(study, name) or ref.to_payload() != lineage[name]:
                raise graph_error(f"Graph {name} ContentRef does not agree with Study and Manifest")


@dataclass(frozen=True)
class GraphEvidence:
    kind: GraphKind
    nodes: tuple[str, ...]
    edges: tuple[EndpointEdge, ...]
    temporal: None
    source_graph_version_id: None
    source_graph_parent_version_id: None
    provenance: GraphProvenance
    content_hash: str

    def __post_init__(self) -> None:
        if (
            self.kind is not GraphKind.PAG or self.temporal is not None
            or self.source_graph_version_id is not None or self.source_graph_parent_version_id is not None
        ):
            raise graph_error("G01 requires an unversioned, non-temporal local PAG")
        if type(self.nodes) is not tuple or type(self.edges) is not tuple:
            raise graph_error("Expected immutable Graph nodes and edges")
        GraphSemanticsValidator.to_product_document(self.kind, self.nodes, self.edges)
        if any(edge.lag is not None for edge in self.edges):
            raise graph_error("Standalone G01 edges require null lag")
        if type(self.provenance) is not GraphProvenance:
            raise graph_error("Expected typed Graph provenance")
        self.provenance.validate_g01()
        if not valid_sha256(self.content_hash) or self.content_hash != jcs.digest(self._meaning()):
            raise graph_error("Graph semantic digest mismatch", code="HASH_INVALID")

    @classmethod
    def from_canonical_json(cls, raw: bytes) -> GraphEvidence:
        try:
            payload = jcs.parse_json(raw)
        except (ValueError, RecursionError) as error:
            raise graph_error("Invalid strict Graph JSON") from error
        items = _exact_object(payload, "schema_version kind version_id parent_version_id nodes edges "
                                      "temporal provenance content_hash")
        if items["schema_version"] != GRAPH_VERSION:
            raise graph_error("Unsupported Graph schema version", code="VERSION_UNSUPPORTED")
        nodes, edges = items["nodes"], items["edges"]
        if type(nodes) is not list or type(edges) is not list:
            raise graph_error("Graph nodes and edges must be JSON arrays")
        try:
            kind = GraphKind(items["kind"])
        except ValueError as error:
            raise graph_error("Unknown Graph kind") from error
        return cls(
            kind, tuple(nodes),
            tuple(EndpointEdge(**_exact_object(edge, "source target source_mark target_mark lag")) for edge in edges),
            items["temporal"], items["version_id"], items["parent_version_id"],
            GraphProvenance.from_payload(items["provenance"]), items["content_hash"],
        )

    def _meaning(self) -> dict[str, object]:
        return {
            "schema_version": GRAPH_VERSION, "kind": self.kind.value,
            "version_id": self.source_graph_version_id, "parent_version_id": self.source_graph_parent_version_id,
            "nodes": list(self.nodes), "edges": [asdict(edge) for edge in self.edges], "temporal": self.temporal,
            "provenance": self.provenance.to_payload(),
        }

    def canonical_payload(self) -> dict[str, object]:
        return {**self._meaning(), "content_hash": self.content_hash}
