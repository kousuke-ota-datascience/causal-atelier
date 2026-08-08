"""Explicit cross-resource lineage edges."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ariadne.product.domain.errors import ProjectBoundaryViolation


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
