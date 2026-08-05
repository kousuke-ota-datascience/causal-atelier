"""Dependency injection for the new web API."""

from __future__ import annotations

import os
from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path
from typing import Annotated, Any, Generator

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ariadne.adapters.local_artifact_store import LocalArtifactStore
from ariadne.product.application.annotation_service import AnnotationService
from ariadne.product.application.comparison_query_service import ComparisonQueryService
from ariadne.product.application.execution_service import ExecutionService
from ariadne.product.application.graph_version_service import GraphVersionService
from ariadne.product.application.lineage_query_service import LineageQueryService
from ariadne.product.application.project_data_service import ProjectDataService
from ariadne.product.persistence.unit_of_work import SqlUnitOfWork


@lru_cache(maxsize=1)
def _get_session_factory() -> Any:
    database_url = os.getenv(
        "ARIADNE_PRODUCT_DATABASE_URL",
        os.getenv("ARIADNE_DATABASE_URL", "sqlite:///.ariadne/product.db"),
    )
    engine = create_engine(database_url)
    return sessionmaker(bind=engine)


def _get_artifact_store() -> LocalArtifactStore:
    root = Path(os.getenv("ARIADNE_ARTIFACT_ROOT", ".ariadne/objects"))
    return LocalArtifactStore(root)


@contextmanager
def _uow_context() -> Generator[SqlUnitOfWork, None, None]:
    factory = _get_session_factory()
    session = factory()
    try:
        yield SqlUnitOfWork(session)
    finally:
        session.close()


def get_project_data_service() -> ProjectDataService:
    return ProjectDataService(
        uow_factory=_uow_context,
        artifact_store=_get_artifact_store(),
    )


def get_execution_service() -> ExecutionService:
    return ExecutionService(uow_factory=_uow_context)


def get_graph_version_service() -> GraphVersionService:
    return GraphVersionService(uow_factory=_uow_context)


def get_annotation_service() -> AnnotationService:
    return AnnotationService(uow_factory=_uow_context)


def get_comparison_service() -> ComparisonQueryService:
    return ComparisonQueryService(uow_factory=_uow_context)


def get_lineage_service() -> LineageQueryService:
    return LineageQueryService(uow_factory=_uow_context)


# FastAPI Depends aliases
ProjectDataServiceDep = Annotated[ProjectDataService, Depends(get_project_data_service)]
ExecutionServiceDep = Annotated[ExecutionService, Depends(get_execution_service)]
GraphVersionServiceDep = Annotated[GraphVersionService, Depends(get_graph_version_service)]
AnnotationServiceDep = Annotated[AnnotationService, Depends(get_annotation_service)]
ComparisonServiceDep = Annotated[ComparisonQueryService, Depends(get_comparison_service)]
LineageServiceDep = Annotated[LineageQueryService, Depends(get_lineage_service)]
