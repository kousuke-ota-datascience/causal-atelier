"""Versioned Research Context aggregate."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ariadne.product.domain.enums import VersionedResourceStatus
from ariadne.product.domain.errors import InvalidSchema, ResourceImmutable
from ariadne.product.domain.schemas import canonical_hash

RELATION_TYPES = frozenset({"REFINES", "DERIVED_FROM", "SUPERSEDES", "RELATED_TO"})


@dataclass
class ResearchContextVersion:
    research_context_version_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    project_id: str = ""
    context_key: str = ""
    version_number: int = 1
    status: VersionedResourceStatus = VersionedResourceStatus.DRAFT
    problem_statement: str = ""
    research_questions: list[str] = field(default_factory=list)
    significance: str | None = None
    hypotheses: list[str] = field(default_factory=list)
    decision_context: dict[str, Any] = field(default_factory=dict)
    relations: list[dict[str, str]] = field(default_factory=list)
    canonical_hash: str | None = None
    created_by: str = ""
    created_at: datetime | None = None

    def update(self, **changes: Any) -> None:
        if self.status is VersionedResourceStatus.FIXED:
            raise ResourceImmutable("FIXED Research Context cannot be updated")
        mutable = {
            "problem_statement", "research_questions", "significance", "hypotheses",
            "decision_context", "relations",
        }
        unknown = set(changes) - mutable
        if unknown:
            raise InvalidSchema(f"Unknown Research Context fields: {sorted(unknown)}")
        for name, value in changes.items():
            setattr(self, name, value)

    def fix(self) -> None:
        if self.status is VersionedResourceStatus.FIXED:
            return
        self._validate()
        self.canonical_hash = canonical_hash(self.snapshot())
        self.status = VersionedResourceStatus.FIXED

    def snapshot(self) -> dict[str, Any]:
        return {
            "schema_version": "research-context/1",
            "context_key": self.context_key,
            "version_number": self.version_number,
            "problem_statement": self.problem_statement,
            "research_questions": self.research_questions,
            "significance": self.significance,
            "hypotheses": self.hypotheses,
            "decision_context": self.decision_context,
            "relations": self.relations,
        }

    def _validate(self) -> None:
        if not self.project_id or not self.context_key.strip() or self.version_number < 1:
            raise InvalidSchema("project_id, context_key, and positive version_number are required")
        if not self.problem_statement.strip():
            raise InvalidSchema("problem_statement is required")
        if not self.research_questions or any(
            not isinstance(question, str) or not question.strip() for question in self.research_questions
        ):
            raise InvalidSchema("research_questions must contain at least one non-empty question")
        if any(not isinstance(item, str) or not item.strip() for item in self.hypotheses):
            raise InvalidSchema("hypotheses must be non-empty strings")
        for relation in self.relations:
            if set(relation) != {"relation_type", "target_context_version_id"}:
                raise InvalidSchema("Context relation has an invalid shape")
            if relation["relation_type"] not in RELATION_TYPES:
                raise InvalidSchema("Context relation_type is invalid")
