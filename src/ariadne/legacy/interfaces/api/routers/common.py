"""Router-level lookup and serialization helpers."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import inspect
from ariadne.application.control_plane import ControlPlaneService as Session

from ariadne.domain import metadata as m


def get_or_404(session: Session, model: type, resource_id: str) -> Any:
    value = session.get(model, resource_id)
    if value is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Resource not found")
    return value


def model_dict(value: Any, *, exclude: set[str] | None = None) -> dict[str, Any]:
    excluded = exclude or set()
    result: dict[str, Any] = {}
    for attribute in inspect(value).mapper.column_attrs:
        name = attribute.key
        if name in excluded:
            continue
        item = getattr(value, name)
        if isinstance(item, datetime):
            if item.tzinfo is None:
                item = item.replace(tzinfo=timezone.utc)
            result[name] = item.isoformat()
        else:
            result[name] = item
    return result


def project_for_dataset_version(session: Session, version: m.DatasetVersion) -> str:
    dataset = get_or_404(session, m.Dataset, version.dataset_id)
    return dataset.project_id


def project_for_table(session: Session, table: m.DatasetTableVersion) -> str:
    version = get_or_404(session, m.DatasetVersion, table.dataset_version_id)
    return project_for_dataset_version(session, version)


def project_for_configuration_version(
    session: Session, version: m.ConfigurationVersion
) -> str:
    configuration = get_or_404(session, m.Configuration, version.configuration_id)
    return configuration.project_id


__all__ = [
    "get_or_404",
    "model_dict",
    "project_for_configuration_version",
    "project_for_dataset_version",
    "project_for_table",
]
