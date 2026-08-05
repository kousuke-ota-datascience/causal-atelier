"""Project router."""

from __future__ import annotations

from fastapi import APIRouter

from ariadne.interfaces.web_api.dependencies import ProjectDataServiceDep
from ariadne.interfaces.web_api.schemas import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from ariadne.product.application.project_data_service import (
    CreateProjectCommand,
    UpdateProjectCommand,
)
from ariadne.product.domain.project import Project

router = APIRouter(prefix="/projects", tags=["projects"])


def _project_to_response(p: Project) -> ProjectResponse:
    return ProjectResponse(
        project_id=p.project_id,
        name=p.name,
        topic=p.topic,
        objective=p.objective,
        memo=p.memo,
        status=p.status.value,
        created_at=p.created_at,
        updated_at=p.updated_at,
    )


@router.post("", status_code=201, response_model=ProjectResponse)
def create_project(body: ProjectCreate, svc: ProjectDataServiceDep) -> ProjectResponse:
    project = svc.create_project(CreateProjectCommand(
        name=body.name,
        topic=body.topic,
        objective=body.objective,
        memo=body.memo,
    ))
    return _project_to_response(project)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str, svc: ProjectDataServiceDep) -> ProjectResponse:
    from ariadne.product.domain.errors import EntityNotFound
    from ariadne.product.persistence.database import SessionFactory
    import os
    # Direct query via service (project is returned on update; get requires direct UoW)
    # Use a minimal inline query for now
    from ariadne.interfaces.web_api.dependencies import _uow_context
    with _uow_context() as uow:
        project = uow.projects.get(project_id)
        if project is None:
            raise EntityNotFound("Project", project_id)
    return _project_to_response(project)


@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: str, body: ProjectUpdate, svc: ProjectDataServiceDep
) -> ProjectResponse:
    project = svc.update_project(UpdateProjectCommand(
        project_id=project_id,
        name=body.name,
        topic=body.topic,
        objective=body.objective,
        memo=body.memo,
    ))
    return _project_to_response(project)
