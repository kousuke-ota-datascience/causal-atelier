"""Unit of Work port protocol."""

from __future__ import annotations

from typing import Protocol

from ariadne.product.ports.repositories import (
    AnnotationRepository,
    ArtifactRepository,
    DatasetVersionRepository,
    ExecutionRepository,
    GraphVersionRepository,
    ProjectRepository,
    ResultRepository,
    StageExecutionRepository,
)


class UnitOfWork(Protocol):
    projects: ProjectRepository
    dataset_versions: DatasetVersionRepository
    executions: ExecutionRepository
    results: ResultRepository
    artifacts: ArtifactRepository
    graph_versions: GraphVersionRepository
    annotations: AnnotationRepository
    stage_executions: StageExecutionRepository

    def __enter__(self) -> "UnitOfWork": ...
    def __exit__(self, *args: object) -> None: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...
