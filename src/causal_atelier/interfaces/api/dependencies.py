"""FastAPI dependencies for sessions, identities, and project RBAC."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

from fastapi import Depends, Header, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session as SqlAlchemySession

from causal_atelier.application.ports import MetadataRepository
from causal_atelier.application.control_plane import ControlPlaneService
from causal_atelier.domain.metadata import ProjectMember, Role, User, utcnow
from causal_atelier.infrastructure.auth import Identity, TokenVerifier
from causal_atelier.infrastructure.persistence import SqlAlchemyMetadataRepository


ROLE_LEVEL = {
    "VIEWER": 10,
    "ANALYST": 20,
    "MAINTAINER": 30,
    "PROJECT_ADMIN": 40,
    "SYSTEM_ADMIN": 100,
}


@dataclass(frozen=True)
class RequestUser:
    id: str
    identity: Identity


def get_session(request: Request) -> Iterator[ControlPlaneService]:
    session: SqlAlchemySession = request.app.state.database.session_factory()
    repository = SqlAlchemyMetadataRepository(session)
    try:
        yield ControlPlaneService(repository)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_current_user(
    request: Request,
    session: ControlPlaneService = Depends(get_session),
    authorization: str | None = Header(default=None),
    x_user_subject: str | None = Header(default=None),
    x_user_name: str | None = Header(default=None),
    x_user_email: str | None = Header(default=None),
) -> RequestUser:
    settings = request.app.state.settings
    if settings.auth_mode == "development":
        subject = x_user_subject or "local-developer"
        identity = Identity(
            provider="development",
            subject=subject,
            display_name=x_user_name or subject,
            email=x_user_email,
            system_admin=subject == "system-admin",
        )
    else:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, "Bearer token is required"
            )
        try:
            identity = TokenVerifier(settings).verify(
                authorization.removeprefix("Bearer ").strip()
            )
        except Exception as exc:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, "Invalid bearer token"
            ) from exc
    user = session.scalar(
        select(User).where(
            User.identity_provider == identity.provider,
            User.external_subject == identity.subject,
        )
    )
    if user is None:
        user = User(
            identity_provider=identity.provider,
            external_subject=identity.subject,
            display_name=identity.display_name,
            email=identity.email,
        )
        session.add(user)
        session.flush()
    elif user.status != "ACTIVE":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "User is not active")
    else:
        user.display_name = identity.display_name
        user.email = identity.email
        user.updated_at = utcnow()
    return RequestUser(user.id, identity)


def require_project_role(
    session: ControlPlaneService,
    user: RequestUser,
    project_id: str,
    minimum_role: str = "VIEWER",
) -> str:
    if user.identity.system_admin:
        return "SYSTEM_ADMIN"
    role = session.scalar(
        select(Role.code)
        .join(ProjectMember, ProjectMember.role_id == Role.id)
        .where(ProjectMember.project_id == project_id, ProjectMember.user_id == user.id)
    )
    if role is None or ROLE_LEVEL.get(role, 0) < ROLE_LEVEL[minimum_role]:
        # Deliberately do not reveal whether the cross-project resource exists.
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Resource not found")
    return role


def seed_roles(session: MetadataRepository) -> None:
    existing = set(session.scalars(select(Role.code)).all())
    for code in ROLE_LEVEL:
        if code not in existing:
            session.add(
                Role(
                    code=code, name=code.replace("_", " ").title(), system_managed=True
                )
            )


__all__ = [
    "RequestUser",
    "get_current_user",
    "get_session",
    "require_project_role",
    "seed_roles",
]
