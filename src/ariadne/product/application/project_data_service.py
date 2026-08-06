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
from ariadne.product.domain.errors import (
    ArtifactHashMismatch,
    EntityNotFound,
    InvalidAnalysisSpec,
    InvalidDatasetMetadata,
    ProjectBoundaryViolation,
)
from ariadne.product.domain.project import Project
from ariadne.product.domain.enums import ProjectStatus
from ariadne.product.application.project_policy import require_active_project
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
class ArchiveProjectCommand:
    project_id: str
    requested_by: str = "system"


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
            require_active_project(project)
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

    def get_project(self, project_id: str) -> Project:
        with self._uow_factory() as uow:
            project = uow.projects.get(project_id)
            if project is None:
                raise EntityNotFound("Project", project_id)
            return project

    def list_projects(self, status: ProjectStatus | None = ProjectStatus.ACTIVE) -> list[Project]:
        with self._uow_factory() as uow:
            projects = uow.projects.list()
            return projects if status is None else [item for item in projects if item.status == status]

    def archive_project(self, command: ArchiveProjectCommand) -> None:
        with self._uow_factory() as uow:
            project = uow.projects.get(command.project_id)
            if project is None:
                raise EntityNotFound("Project", command.project_id)
            if project.status == ProjectStatus.ARCHIVED:
                return
            project.archive()
            project.updated_at = self._clock.now()
            uow.projects.update(project)
            uow.commit()

    def get_dataset_version(self, dataset_version_id: str) -> DatasetVersion:
        with self._uow_factory() as uow:
            dataset = uow.dataset_versions.get(dataset_version_id)
            if dataset is None:
                raise EntityNotFound("DatasetVersion", dataset_version_id)
            return dataset

    def list_dataset_versions(self, project_id: str) -> list[DatasetVersion]:
        with self._uow_factory() as uow:
            if uow.projects.get(project_id) is None:
                raise EntityNotFound("Project", project_id)
            return uow.dataset_versions.list_by_project(project_id)

    def get_dataset_preview(self, dataset_version_id: str, limit: int = 20) -> dict[str, Any]:
        if limit < 1 or limit > 100:
            raise InvalidAnalysisSpec("preview limit must be between 1 and 100")
        with self._uow_factory() as uow:
            dataset = uow.dataset_versions.get(dataset_version_id)
            if dataset is None:
                raise EntityNotFound("DatasetVersion", dataset_version_id)
            artifact = uow.artifacts.get(dataset.source_artifact_id)
            if artifact is None:
                raise EntityNotFound("Artifact", dataset.source_artifact_id)
        import tempfile
        import pandas as pd
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / Path(artifact.object_key).name
            self._artifact_store.retrieve(artifact.object_key, path)
            actual_hash = _sha256_file(path)
            if actual_hash != artifact.content_hash or actual_hash != dataset.content_hash:
                raise ArtifactHashMismatch("Dataset Artifact hash mismatch")
            frame = pd.read_parquet(path) if path.suffix.lower() == ".parquet" else pd.read_csv(path)
        preview = frame.head(limit).astype(object).where(frame.head(limit).notna(), None)
        return {
            "dataset_version_id": dataset.dataset_version_id,
            "columns": list(frame.columns),
            "rows": preview.to_dict(orient="records"),
            "limit": limit,
        }

    def register_dataset_version(self, command: RegisterDatasetVersionCommand) -> DatasetVersion:
        now = self._clock.now()
        dataset_key = _required_dataset_text("dataset_key", command.dataset_key, 100)
        name = _required_dataset_text("name", command.name, 200)
        version_label = _required_dataset_text("version_label", command.version_label, 100)
        source_note = _optional_dataset_text("source_note", command.source_note, 4000)

        # Compute content hash from file
        content_hash = _sha256_file(command.source_path)

        with self._uow_factory() as uow:
            # Verify project exists
            project = uow.projects.get(command.project_id)
            if project is None:
                raise EntityNotFound("Project", command.project_id)
            require_active_project(project)

            # Check for duplicate
            if uow.dataset_versions.exists_hash(command.project_id, dataset_key, content_hash):
                raise ProjectBoundaryViolation(
                    f"Dataset version with same content already exists in project {command.project_id!r}"
                )

            # Build object key for artifact store
            artifact_id = str(uuid.uuid4())
            # Dataset metadata is user-controlled and must not become a path segment.
            object_key = (
                f"projects/{command.project_id}/datasets/{artifact_id}"
                f"/source{command.source_path.suffix.lower()}"
            )

            stored = self._artifact_store.store(
                source_path=command.source_path,
                object_key=object_key,
                media_type="text/csv" if command.source_path.suffix.lower() == ".csv" else "application/vnd.apache.parquet",
            )
            if stored.content_hash != content_hash:
                self._artifact_store.delete(stored.object_key)
                raise ArtifactHashMismatch("Stored Dataset Artifact hash mismatch")

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
                dataset_key=dataset_key,
                name=name,
                version_label=version_label,
                content_hash=content_hash,
                schema_json=command.schema_json,
                profile_summary_json=command.profile_summary_json or {},
                row_count=command.row_count,
                column_count=command.column_count,
                source_note=source_note,
                created_at=now,
            )

            try:
                uow.artifacts.add_many([artifact])
                uow.dataset_versions.add(dataset_version)
                uow.commit()
            except Exception:
                self._artifact_store.delete(stored.object_key)
                raise

            return dataset_version


def _required_dataset_text(field: str, value: str, max_length: int) -> str:
    normalized = value.strip()
    if not normalized:
        raise InvalidDatasetMetadata(f"{field} must not be empty")
    if len(normalized) > max_length:
        raise InvalidDatasetMetadata(
            f"{field} must be at most {max_length} characters (received {len(normalized)})"
        )
    return normalized


def _optional_dataset_text(field: str, value: str | None, max_length: int) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    if len(normalized) > max_length:
        raise InvalidDatasetMetadata(
            f"{field} must be at most {max_length} characters (received {len(normalized)})"
        )
    return normalized or None


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()
