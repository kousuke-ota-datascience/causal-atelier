"""Artifact domain entity."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ariadne.product.domain.enums import ArtifactScope, ArtifactType
from ariadne.product.domain.errors import InvalidAnalysisSpec


def _new_id() -> str:
    return str(uuid.uuid4())


@dataclass
class Artifact:
    artifact_id: str = field(default_factory=_new_id)
    project_id: str = ""
    execution_id: str | None = None
    stage_execution_id: str | None = None
    result_id: str | None = None
    artifact_scope: ArtifactScope = ArtifactScope.SOURCE
    artifact_type: ArtifactType = ArtifactType.LOG
    object_key: str = ""
    content_hash: str = ""
    media_type: str = "application/octet-stream"
    size_bytes: int = 0
    metadata_json: dict[str, Any] = field(default_factory=dict)
    created_at: datetime | None = None

    def __post_init__(self) -> None:
        if self.artifact_scope is ArtifactScope.SOURCE:
            if self.execution_id or self.stage_execution_id or self.result_id:
                raise InvalidAnalysisSpec("SOURCE Artifact cannot have execution output ownership")
        elif self.artifact_scope is ArtifactScope.EXECUTION_OUTPUT and not self.execution_id:
            raise InvalidAnalysisSpec("Execution-output Artifact requires execution_id")
