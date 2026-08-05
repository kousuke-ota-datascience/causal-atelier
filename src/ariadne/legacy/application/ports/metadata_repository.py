"""Persistence-neutral metadata repository contract."""

from __future__ import annotations

from typing import Any, Protocol, TypeVar

T = TypeVar("T")


class MetadataRepository(Protocol):
    """Minimal entity operations required by application use cases.

    Query-specific methods live on concrete repository implementations; this
    core contract keeps transaction and entity lifecycle semantics explicit.
    """

    def get(self, entity_type: type[T], entity_id: Any) -> T | None: ...

    def add(self, entity: T) -> None: ...

    def delete(self, entity: T) -> None: ...

    def flush(self) -> None: ...

    def scalar(self, statement: Any) -> Any: ...

    def scalars(self, statement: Any) -> Any: ...

    def execute(self, statement: Any) -> Any: ...

    def merge(self, entity: T) -> T: ...

    def refresh(self, entity: T) -> None: ...

    def commit(self) -> None: ...

    def rollback(self) -> None: ...


__all__ = ["MetadataRepository"]
