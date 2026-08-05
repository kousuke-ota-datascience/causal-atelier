"""AnnotationService – create and update annotations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ariadne.product.domain.annotation import Annotation
from ariadne.product.domain.errors import EntityNotFound
from ariadne.product.ports.clock import ClockPort, SystemClock


@dataclass
class CreateAnnotationCommand:
    project_id: str
    statement: str
    created_by: str
    target_result_id: str | None = None
    target_graph_version_id: str | None = None
    rationale: str | None = None
    assumptions_json: list[Any] = field(default_factory=list)
    limitations_json: list[Any] = field(default_factory=list)


@dataclass
class UpdateAnnotationCommand:
    annotation_id: str
    statement: str | None = None
    rationale: str | None = None
    assumptions_json: list[Any] | None = None
    limitations_json: list[Any] | None = None


class AnnotationService:
    def __init__(self, uow_factory: Any, clock: ClockPort | None = None) -> None:
        self._uow_factory = uow_factory
        self._clock = clock or SystemClock()

    def create_annotation(self, command: CreateAnnotationCommand) -> Annotation:
        now = self._clock.now()
        annotation = Annotation(
            project_id=command.project_id,
            target_result_id=command.target_result_id,
            target_graph_version_id=command.target_graph_version_id,
            statement=command.statement,
            rationale=command.rationale,
            assumptions_json=command.assumptions_json,
            limitations_json=command.limitations_json,
            created_by=command.created_by,
            created_at=now,
            updated_at=now,
        )
        with self._uow_factory() as uow:
            uow.annotations.add(annotation)
            uow.commit()
        return annotation

    def update_annotation(self, command: UpdateAnnotationCommand) -> Annotation:
        now = self._clock.now()
        with self._uow_factory() as uow:
            annotation = uow.annotations.get(command.annotation_id)
            if annotation is None:
                raise EntityNotFound("Annotation", command.annotation_id)
            annotation.update_content(
                statement=command.statement,
                rationale=command.rationale,
                assumptions_json=command.assumptions_json,
                limitations_json=command.limitations_json,
            )
            annotation.updated_at = now
            uow.annotations.update(annotation)
            uow.commit()
        return annotation
