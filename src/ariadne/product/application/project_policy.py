"""Shared Project write-state policy."""

from ariadne.product.domain.enums import ProjectStatus
from ariadne.product.domain.errors import ProjectArchived
from ariadne.product.domain.project import Project


def require_active_project(project: Project) -> None:
    if project.status == ProjectStatus.ARCHIVED:
        raise ProjectArchived(project.project_id)
