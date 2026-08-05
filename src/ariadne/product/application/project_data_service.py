"""ProjectDataService – create/update projects and register dataset versions."""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from ariadne.product.domain.artifact import Artifact
from ariadne.product.domain.dataset_version import DatasetVersion
from ariadne.product.domain.enums import ArtifactType
from ariadne.product.domain.errors import EntityNotFound, ProjectBoundaryViolation
from ariadne.product.domain.project import Project
from ariadne.product.ports.artifact_store import ArtifactStorePort
from ariadne.product.ports.clock import ClockPort, SystemClock
from ariadne.product.ports.unit_of_work import UnitOfWork


@dataclass
class CreateProjectCommand:
    name: str
    topic: str | None = None
    objective: str | None = None
    memo: str | None = None
    requested_by: str = "system"


@dataclass
class UpdateProjectCommand:
    project_id: str
    name: str | None = None
    topic: str | None = None
    objective: str | None = None
    memo: str | None = None


@dataclass
class RegisterDatasetVersionCommand:
    project_id: str
    dataset_key: str
    name: str
    version_label: str
    source_path: Path
    schema_json: dict[str, Any]
    row_count: int
    column_count: int
    source_note: str | None = None
    profile_summary_json: dict[str, Any] | None = None
    requested_by: str = "system"


class ProjectDataService:
    def __init__(
        self,
        uow_factory: Any,
        artifact_store: ArtifactStorePort,
        clock: ClockPort | None = None,
    ) -> None:
        self._uow_factory = uow_factory
        self._artifact_store = artifact_store
        self._clock = clock or SystemClock()

    def create_project(self, command: CreateProjectCommand) -> Project:
        now = self._clock.now()
        project = Project(
            name=command.name,
            topic=command.topic,
            objective=command.objective,
            memo=command.memo,
            created_at=now,
            updated_at=now,
        )
        with self._uow_factory() as uow:
            uow.projects.add(project)
            uow.commit()
        return project

    def update_project(self, command: UpdateProjectCommand) -> Project:
        with self._uow_factory() as uow:
            project = uow.projects.get(command.project_id)
            if project is None:
                raise EntityNotFound("Project", command.project_id)
            project.update_metadata(
                name=command.name,
                topic=command.topic,
                objective=command.objective,
                memo=command.memo,
            )
            project.updated_at = self._clock.now()
            uow.projects.update(project)
            uow.commit()
        return project

    def register_dataset_version(self, command: RegisterDatasetVersionCommand) -> DatasetVersion:
        now = self._clock.now()

        # Compute content hash from file
        content_hash = _sha256_file(command.source_path)

        with self._uow_factory() as uow:
            # Verify project exists
            project = uow.projects.get(command.project_id)
            if project is None:
                raise EntityNotFound("Project", command.project_id)

            # Check for duplicate
            if uow.dataset_versions.exists_hash(command.project_id, command.dataset_key, content_hash):
                raise ProjectBoundaryViolation(
                    f"Dataset version with same content already exists in project {command.project_id!r}"
                )

            # Build object key for artifact store
            artifact_id = str(uuid.uuid4())
            object_key = f"projects/{command.project_id}/datasets/{command.dataset_key}/{artifact_id}/{command.source_path.name}"

            # Store file
            stored = self._artifact_store.store(
                source_path=command.source_path,
                object_key=object_key,
                media_type="application/octet-stream",
            )

            # Create artifact entity
            artifact = Artifact(
                artifact_id=artifact_id,
                project_id=command.project_id,
                artifact_type=ArtifactType.DATASET_FILE,
                object_key=stored.object_key,
                content_hash=stored.content_hash,
                media_type=stored.media_type,
                size_bytes=stored.size_bytes,
                created_at=now,
            )

            # Create dataset version entity
            dataset_version = DatasetVersion(
                project_id=command.project_id,
                source_artifact_id=artifact_id,
                dataset_key=command.dataset_key,
                name=command.name,
                version_label=command.version_label,
                content_hash=content_hash,
                schema_json=command.schema_json,
                profile_summary_json=command.profile_summary_json or {},
                row_count=command.row_count,
                column_count=command.column_count,
                source_note=command.source_note,
                created_at=now,
            )

            uow.artifacts.add_many([artifact])
            uow.dataset_versions.add(dataset_version)
            uow.commit()

        return dataset_version


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()
