"""Project domain entity."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime

from ariadne.product.domain.enums import ProjectStatus
from ariadne.product.domain.errors import InvalidStateTransition


def _new_id() -> str:
    return str(uuid.uuid4())


@dataclass
class Project:
    project_id: str = field(default_factory=_new_id)
    name: str = ""
    topic: str | None = None
    objective: str | None = None
    memo: str | None = None
    status: ProjectStatus = ProjectStatus.ACTIVE
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def update_metadata(
        self,
        name: str | None = None,
        topic: str | None = None,
        objective: str | None = None,
        memo: str | None = None,
    ) -> None:
        if name is not None:
            self.name = name
        if topic is not None:
            self.topic = topic
        if objective is not None:
            self.objective = objective
        if memo is not None:
            self.memo = memo

    def archive(self) -> None:
        if self.status != ProjectStatus.ACTIVE:
            raise InvalidStateTransition("Project", self.status, ProjectStatus.ARCHIVED)
        self.status = ProjectStatus.ARCHIVED
