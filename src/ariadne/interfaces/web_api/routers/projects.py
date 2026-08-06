"""Project router."""

from __future__ import annotations

from fastapi import APIRouter, Request, Response

from ariadne.interfaces.web_api.dependencies import ProjectDataServiceDep
from ariadne.interfaces.web_api.schemas import (
    ProjectCreate,
    ProjectResponse,
    ProjectListResponse,
    ProjectUpdate,
)
from ariadne.product.application.project_data_service import (
    CreateProjectCommand,
    ArchiveProjectCommand,
    UpdateProjectCommand,
)
from ariadne.product.domain.enums import ProjectStatus
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
async def create_project(body: ProjectCreate, svc: ProjectDataServiceDep) -> ProjectResponse:
    project = svc.create_project(CreateProjectCommand(
        name=body.name,
        topic=body.topic,
        objective=body.objective,
        memo=body.memo,
    ))
    return _project_to_response(project)


@router.get("", response_model=ProjectListResponse)
async def list_projects(
    svc: ProjectDataServiceDep, status: ProjectStatus | None = ProjectStatus.ACTIVE
) -> ProjectListResponse:
    return ProjectListResponse(items=[_project_to_response(item) for item in svc.list_projects(status)])


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str, svc: ProjectDataServiceDep) -> ProjectResponse:
    return _project_to_response(svc.get_project(project_id))


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
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


@router.delete("/{project_id}", status_code=204)
async def archive_project(
    project_id: str, request: Request, svc: ProjectDataServiceDep
) -> Response:
    svc.archive_project(ArchiveProjectCommand(
        project_id=project_id,
        requested_by=request.headers.get("X-User-Id", "anonymous"),
    ))
    return Response(status_code=204)
