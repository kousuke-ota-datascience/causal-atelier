"""Explicit cross-resource lineage edges."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from ariadne.product.domain.errors import InvalidSchema, ProjectBoundaryViolation


class LineageAuthority(str, Enum):
    """Authority assigned to an approved semantic lineage relation."""

    TYPED_STRUCTURAL = "TYPED_STRUCTURAL"
    GENERIC_ONLY = "GENERIC_ONLY"
    PROJECTION_ONLY = "PROJECTION_ONLY"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"


# This is syntactic input validation only.  Generic persistence is additionally
# controlled by ``classify_lineage_authority`` below.
LINEAGE_RELATION_TYPES = frozenset({
    "USED_INPUT", "GENERATED", "DERIVED_FROM", "REVISED_FROM",
    "SUPPORTED_BY", "EVIDENCE_FOR", "DOCUMENTS", "SUMMARIZES",
    "MOTIVATED", "SELECTED", "REJECTED",
})


_TYPED_STRUCTURAL_TUPLES = frozenset({
    ("Execution", "GENERATED", "Result"),
    ("Result", "GENERATED", "Artifact"),
    ("DatasetVersion", "USED_INPUT", "Execution"),
    ("AnalysisView", "USED_INPUT", "Execution"),
    ("Result", "USED_INPUT", "Execution"),
    ("Result", "DERIVED_FROM", "GraphVersion"),
    ("Artifact", "DERIVED_FROM", "DatasetVersion"),
    ("Execution", "DERIVED_FROM", "Execution"),
    ("Execution", "REVISED_FROM", "Execution"),
})

_DOCUMENT_OR_EVIDENCE_TARGET_TYPES = frozenset({
    "Project", "ResearchContextVersion", "DatasetVersion", "AnalysisView",
    "AnalysisSpecification", "Execution", "Result", "Artifact", "GraphVersion",
    "Annotation",
})

_GENERIC_ONLY_TUPLES = frozenset({
    ("Artifact", "DERIVED_FROM", "Artifact"),
    ("Result", "SUMMARIZES", "Result"),
    ("Result", "SUMMARIZES", "Artifact"),
    ("Result", "MOTIVATED", "Execution"),
    ("Result", "MOTIVATED", "AnalysisSpecification"),
    # This existing Product writer is converged in G06-P03.  It is represented
    # here so that P03 can use the same policy without inventing a second one.
    ("Result", "MOTIVATED", "AnalysisSpecificationDraft"),
    *{
        (source_type, relation_type, target_type)
        for source_type in ("Result", "Artifact")
        for relation_type in ("DOCUMENTS", "SUPPORTED_BY", "EVIDENCE_FOR")
        for target_type in _DOCUMENT_OR_EVIDENCE_TARGET_TYPES
    },
    *{
        (source_type, relation_type, "Annotation")
        for source_type in (
            "Project", "ResearchContextVersion", "AnalysisView",
            "AnalysisSpecification", "Execution", "Result", "GraphVersion",
        )
        for relation_type in ("SELECTED", "REJECTED")
    },
})


def classify_lineage_authority(
    source_type: str, relation_type: str, target_type: str,
) -> LineageAuthority | None:
    """Return the authority for an approved semantic lineage tuple.

    ``None`` is an explicit closed-by-default result for an unknown or
    unapproved tuple; it must not be interpreted as generic-write permission.
    """

    semantic_tuple = (source_type, relation_type, target_type)
    if semantic_tuple in _TYPED_STRUCTURAL_TUPLES:
        return LineageAuthority.TYPED_STRUCTURAL
    if semantic_tuple in _GENERIC_ONLY_TUPLES:
        return LineageAuthority.GENERIC_ONLY
    return None


def assert_generic_lineage_allowed(
    source_type: str, relation_type: str, target_type: str,
) -> None:
    """Reject every semantic relation that is not generic-only authority."""

    authority = classify_lineage_authority(source_type, relation_type, target_type)
    if authority is not LineageAuthority.GENERIC_ONLY:
        rendered = f"{source_type} --{relation_type}--> {target_type}"
        if authority is LineageAuthority.TYPED_STRUCTURAL:
            raise InvalidSchema(
                f"Generic lineage persistence is forbidden for typed structural relation: {rendered}"
            )
        raise InvalidSchema(f"Unsupported generic lineage semantic relation: {rendered}")


@dataclass(frozen=True)
class ResourceRef:
    resource_type: str
    resource_id: str
    project_id: str
    schema_version: str | None = None
    content_hash: str | None = None


@dataclass(frozen=True)
class LineageEdge:
    lineage_edge_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    project_id: str = ""
    source: ResourceRef = field(default_factory=lambda: ResourceRef("", "", ""))
    relation_type: str = "DERIVED_FROM"
    target: ResourceRef = field(default_factory=lambda: ResourceRef("", "", ""))
    evidence: dict[str, Any] = field(default_factory=dict)
    created_by: str = ""
    created_at: datetime | None = None

    def __post_init__(self) -> None:
        if self.project_id != self.source.project_id or self.project_id != self.target.project_id:
            raise ProjectBoundaryViolation("Lineage edge cannot cross Project boundaries")
        if not self.source.resource_id or not self.target.resource_id or not self.relation_type:
            raise ValueError("Lineage edge requires source, target, and relation_type")
