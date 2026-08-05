"""Annotation domain entity."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ariadne.product.domain.errors import InvalidAnalysisSpec


def _new_id() -> str:
    return str(uuid.uuid4())


@dataclass
class Annotation:
    annotation_id: str = field(default_factory=_new_id)
    project_id: str = ""
    target_result_id: str | None = None
    target_graph_version_id: str | None = None
    statement: str = ""
    rationale: str | None = None
    assumptions_json: list[Any] = field(default_factory=list)
    limitations_json: list[Any] = field(default_factory=list)
    created_by: str = ""
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        self._validate_target()

    def _validate_target(self) -> None:
        if not (bool(self.target_result_id) ^ bool(self.target_graph_version_id)):
            raise InvalidAnalysisSpec(
                "Exactly one of target_result_id or target_graph_version_id must be set"
            )

    def update_content(
        self,
        statement: str | None = None,
        rationale: str | None = None,
        assumptions_json: list[Any] | None = None,
        limitations_json: list[Any] | None = None,
    ) -> None:
        if statement is not None:
            self.statement = statement
        if rationale is not None:
            self.rationale = rationale
        if assumptions_json is not None:
            self.assumptions_json = assumptions_json
        if limitations_json is not None:
            self.limitations_json = limitations_json
