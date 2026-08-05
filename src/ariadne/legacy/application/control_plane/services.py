"""Application boundary for metadata reads and writes used by API adapters."""

from __future__ import annotations

from typing import Any, TypeVar

from ariadne.application.ports import MetadataRepository

T = TypeVar("T")


class ControlPlaneService:
    """Expose metadata lifecycle operations without leaking a DB session."""

    def __init__(self, repository: MetadataRepository) -> None:
        self.repository = repository

    def get(self, entity_type: type[T], entity_id: Any) -> T | None:
        return self.repository.get(entity_type, entity_id)

    def add(self, entity: T) -> None:
        self.repository.add(entity)

    def delete(self, entity: T) -> None:
        self.repository.delete(entity)

    def flush(self) -> None:
        self.repository.flush()

    def scalar(self, specification: Any) -> Any:
        return self.repository.scalar(specification)

    def scalars(self, specification: Any) -> Any:
        return self.repository.scalars(specification)

    def execute(self, specification: Any) -> Any:
        return self.repository.execute(specification)

    def merge(self, entity: T) -> T:
        return self.repository.merge(entity)

    def refresh(self, entity: T) -> None:
        self.repository.refresh(entity)

    def commit(self) -> None:
        self.repository.commit()

    def rollback(self) -> None:
        self.repository.rollback()


__all__ = ["ControlPlaneService"]
