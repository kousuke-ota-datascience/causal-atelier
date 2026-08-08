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
from ariadne.product.application.graph_candidate_query_service import GraphCandidateQueryService
from ariadne.product.application.lineage_query_service import LineageQueryService
from ariadne.product.application.project_data_service import ProjectDataService
from ariadne.product.application.query_service import ProductQueryService
from ariadne.product.application.artifact_service import ArtifactService
from ariadne.product.application.exploratory_service import ExploratoryWorkspaceService
from ariadne.product.application.predictive_split_service import PredictiveSplitService
from ariadne.product.application.predictive_workflow_service import PredictiveWorkflowService
from ariadne.product.application.workspace_lifecycle_service import WorkspaceLifecycleService
from ariadne.product.application.product_closure_service import ProductClosureService
from ariadne.interfaces.web_api.idempotency import IdempotencyService
from ariadne.product.persistence.unit_of_work import SqlUnitOfWork


@lru_cache(maxsize=1)
def _get_session_factory() -> Any:
    database_url = os.getenv("ARIADNE_PRODUCT_DATABASE_URL")
    if not database_url:
        raise RuntimeError("ARIADNE_PRODUCT_DATABASE_URL is required")
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


async def get_project_data_service() -> ProjectDataService:
    return ProjectDataService(
        uow_factory=_uow_context,
        artifact_store=_get_artifact_store(),
    )


async def get_execution_service() -> ExecutionService:
    return ExecutionService(uow_factory=_uow_context)


async def get_graph_version_service() -> GraphVersionService:
    return GraphVersionService(uow_factory=_uow_context)


async def get_graph_candidate_service() -> GraphCandidateQueryService:
    return GraphCandidateQueryService(uow_factory=_uow_context)


async def get_annotation_service() -> AnnotationService:
    return AnnotationService(uow_factory=_uow_context)


async def get_comparison_service() -> ComparisonQueryService:
    return ComparisonQueryService(uow_factory=_uow_context)


async def get_lineage_service() -> LineageQueryService:
    return LineageQueryService(uow_factory=_uow_context)


async def get_query_service() -> ProductQueryService:
    return ProductQueryService(uow_factory=_uow_context)


async def get_artifact_service() -> ArtifactService:
    return ArtifactService(uow_factory=_uow_context, artifact_store=_get_artifact_store())


async def get_idempotency_service() -> IdempotencyService:
    return IdempotencyService(_get_session_factory())


async def get_exploratory_workspace_service() -> ExploratoryWorkspaceService:
    return ExploratoryWorkspaceService(_get_session_factory(), _get_artifact_store())


async def get_predictive_split_service() -> PredictiveSplitService:
    return PredictiveSplitService(_get_session_factory(), _get_artifact_store())


async def get_workspace_lifecycle_service() -> WorkspaceLifecycleService:
    return WorkspaceLifecycleService(_get_session_factory())


async def get_predictive_workflow_service() -> PredictiveWorkflowService:
    return PredictiveWorkflowService(_get_session_factory(), _get_artifact_store())


async def get_product_closure_service() -> ProductClosureService:
    return ProductClosureService(_get_session_factory(), _get_artifact_store())


# FastAPI Depends aliases
ProjectDataServiceDep = Annotated[ProjectDataService, Depends(get_project_data_service)]
ExecutionServiceDep = Annotated[ExecutionService, Depends(get_execution_service)]
GraphVersionServiceDep = Annotated[GraphVersionService, Depends(get_graph_version_service)]
GraphCandidateServiceDep = Annotated[GraphCandidateQueryService, Depends(get_graph_candidate_service)]
AnnotationServiceDep = Annotated[AnnotationService, Depends(get_annotation_service)]
ComparisonServiceDep = Annotated[ComparisonQueryService, Depends(get_comparison_service)]
LineageServiceDep = Annotated[LineageQueryService, Depends(get_lineage_service)]
ProductQueryServiceDep = Annotated[ProductQueryService, Depends(get_query_service)]
ArtifactServiceDep = Annotated[ArtifactService, Depends(get_artifact_service)]
IdempotencyServiceDep = Annotated[IdempotencyService, Depends(get_idempotency_service)]
ExploratoryWorkspaceServiceDep = Annotated[
    ExploratoryWorkspaceService, Depends(get_exploratory_workspace_service)
]
PredictiveSplitServiceDep = Annotated[
    PredictiveSplitService, Depends(get_predictive_split_service)
]
WorkspaceLifecycleServiceDep = Annotated[
    WorkspaceLifecycleService, Depends(get_workspace_lifecycle_service)
]
PredictiveWorkflowServiceDep = Annotated[
    PredictiveWorkflowService, Depends(get_predictive_workflow_service)
]
ProductClosureServiceDep = Annotated[
    ProductClosureService, Depends(get_product_closure_service)
]
