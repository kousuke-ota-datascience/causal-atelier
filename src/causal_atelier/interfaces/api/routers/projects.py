"""Project and membership endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy import func, select
from causal_atelier.application.control_plane import ControlPlaneService as Session

from causal_atelier.application.run_execution.services import add_audit
from causal_atelier.domain import metadata as m
from causal_atelier.interfaces.api.dependencies import (
    RequestUser,
    get_current_user,
    get_session,
    require_project_role,
)
from causal_atelier.interfaces.api.schemas import (
    MemberCreate,
    ProjectCreate,
    ProjectUpdate,
)

from .common import get_or_404, model_dict


router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_project(
    body: ProjectCreate,
    request: Request,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    if session.scalar(
        select(m.Project).where(func.lower(m.Project.slug) == body.slug.lower())
    ):
        raise HTTPException(status.HTTP_409_CONFLICT, "Project slug already exists")
    project = m.Project(**body.model_dump(), created_by=user.id)
    session.add(project)
    session.flush()
    role = session.scalar(select(m.Role).where(m.Role.code == "PROJECT_ADMIN"))
    session.add(
        m.ProjectMember(project_id=project.id, user_id=user.id, role_id=role.id)
    )
    add_audit(
        session,
        project_id=project.id,
        actor_user_id=user.id,
        action="PROJECT_CREATE",
        resource_type="PROJECT",
        resource_id=project.id,
        request_id=request.state.request_id,
        after=body.model_dump(),
    )
    return model_dict(project)


@router.get("")
def list_projects(
    page: int = 1,
    limit: int = 50,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    page = max(page, 1)
    limit = min(max(limit, 1), 200)
    query = select(m.Project).where(m.Project.deleted_at.is_(None))
    if not user.identity.system_admin:
        query = query.join(m.ProjectMember).where(m.ProjectMember.user_id == user.id)
    total = session.scalar(select(func.count()).select_from(query.subquery())) or 0
    projects = session.scalars(
        query.order_by(m.Project.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    ).all()
    return {
        "items": [model_dict(item) for item in projects],
        "total": total,
        "page": page,
        "limit": limit,
    }


@router.get("/{project_id}")
def get_project(
    project_id: str,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    require_project_role(session, user, project_id)
    project = get_or_404(session, m.Project, project_id)
    if project.deleted_at:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Resource not found")
    return model_dict(project)


@router.patch("/{project_id}")
def update_project(
    project_id: str,
    body: ProjectUpdate,
    request: Request,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    require_project_role(session, user, project_id, "PROJECT_ADMIN")
    project = get_or_404(session, m.Project, project_id)
    before = model_dict(project)
    for name, value in body.model_dump(exclude_unset=True).items():
        setattr(project, name, value)
    project.updated_at = m.utcnow()
    add_audit(
        session,
        project_id=project.id,
        actor_user_id=user.id,
        action="PROJECT_UPDATE",
        resource_type="PROJECT",
        resource_id=project.id,
        request_id=request.state.request_id,
        before=before,
        after=model_dict(project),
    )
    return model_dict(project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: str,
    request: Request,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> Response:
    require_project_role(session, user, project_id, "PROJECT_ADMIN")
    project = get_or_404(session, m.Project, project_id)
    project.status = "DELETED"
    project.deleted_at = m.utcnow()
    add_audit(
        session,
        project_id=project.id,
        actor_user_id=user.id,
        action="PROJECT_DELETE",
        resource_type="PROJECT",
        resource_id=project.id,
        request_id=request.state.request_id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{project_id}/members", status_code=status.HTTP_201_CREATED)
def add_member(
    project_id: str,
    body: MemberCreate,
    request: Request,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    require_project_role(session, user, project_id, "PROJECT_ADMIN")
    get_or_404(session, m.User, body.user_id)
    role = session.scalar(select(m.Role).where(m.Role.code == body.role))
    member = session.get(m.ProjectMember, (project_id, body.user_id))
    if member:
        member.role_id = role.id
        action = "PROJECT_MEMBER_UPDATE"
    else:
        member = m.ProjectMember(
            project_id=project_id, user_id=body.user_id, role_id=role.id
        )
        session.add(member)
        action = "PROJECT_MEMBER_CREATE"
    add_audit(
        session,
        project_id=project_id,
        actor_user_id=user.id,
        action=action,
        resource_type="PROJECT_MEMBER",
        resource_id=body.user_id,
        request_id=request.state.request_id,
        after=body.model_dump(),
    )
    return {"project_id": project_id, "user_id": body.user_id, "role": body.role}


@router.get("/{project_id}/members")
def list_members(
    project_id: str,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> list[dict]:
    require_project_role(session, user, project_id, "VIEWER")
    rows = session.execute(
        select(m.User, m.Role.code)
        .join(m.ProjectMember, m.ProjectMember.user_id == m.User.id)
        .join(m.Role, m.Role.id == m.ProjectMember.role_id)
        .where(m.ProjectMember.project_id == project_id)
    ).all()
    return [{**model_dict(member), "role": role} for member, role in rows]


__all__ = ["router"]
