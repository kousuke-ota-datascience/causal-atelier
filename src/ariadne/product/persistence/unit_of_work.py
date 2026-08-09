"""SQLAlchemy-backed Unit of Work for the product domain."""

from __future__ import annotations

from sqlalchemy.orm import Session

from ariadne.product.persistence.repositories import (
    SqlAnnotationRepository,
    SqlArtifactRepository,
    SqlDatasetVersionRepository,
    SqlExecutionRepository,
    SqlGraphVersionRepository,
    SqlProjectRepository,
    SqlResultRepository,
    SqlStageExecutionRepository,
)


class SqlUnitOfWork:
    def __init__(self, session: Session) -> None:
        self._session = session

    def __enter__(self) -> "SqlUnitOfWork":
        return self

    def __exit__(self, exc_type: type | None, *args: object) -> None:
        if exc_type:
            self.rollback()
        else:
            self.commit()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()

    @property
    def projects(self) -> SqlProjectRepository:
        return SqlProjectRepository(self._session)

    @property
    def dataset_versions(self) -> SqlDatasetVersionRepository:
        return SqlDatasetVersionRepository(self._session)

    @property
    def executions(self) -> SqlExecutionRepository:
        return SqlExecutionRepository(self._session)

    @property
    def results(self) -> SqlResultRepository:
        return SqlResultRepository(self._session)

    @property
    def artifacts(self) -> SqlArtifactRepository:
        return SqlArtifactRepository(self._session)

    @property
    def graph_versions(self) -> SqlGraphVersionRepository:
        return SqlGraphVersionRepository(self._session)

    @property
    def annotations(self) -> SqlAnnotationRepository:
        return SqlAnnotationRepository(self._session)

    @property
    def stage_executions(self) -> SqlStageExecutionRepository:
        return SqlStageExecutionRepository(self._session)
