"""GraphVersion domain entity."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ariadne.product.domain.enums import GraphType, GraphVersionStatus
from ariadne.product.domain.errors import GraphAlreadyFixed, InvalidStateTransition


def _new_id() -> str:
    return str(uuid.uuid4())


@dataclass
class GraphVersion:
    graph_version_id: str = field(default_factory=_new_id)
    project_id: str = ""
    source_result_id: str = ""
    parent_graph_version_id: str | None = None
    name: str = ""
    graph_type: GraphType = GraphType.DAG
    graph_json: dict[str, Any] = field(default_factory=dict)
    content_hash: str = ""
    edit_rationale: str | None = None
    status: GraphVersionStatus = GraphVersionStatus.DRAFT
    created_by: str = ""
    created_at: datetime | None = None

    def apply_edit(self, graph_json: dict[str, Any], edit_rationale: str | None = None) -> None:
        if self.status == GraphVersionStatus.FIXED:
            raise GraphAlreadyFixed(
                f"GraphVersion {self.graph_version_id!r} is already FIXED"
            )
        self.graph_json = graph_json
        if edit_rationale is not None:
            self.edit_rationale = edit_rationale

    def fix(self) -> None:
        if self.status == GraphVersionStatus.FIXED:
            raise InvalidStateTransition(
                "GraphVersion", self.status, GraphVersionStatus.FIXED
            )
        self.status = GraphVersionStatus.FIXED
