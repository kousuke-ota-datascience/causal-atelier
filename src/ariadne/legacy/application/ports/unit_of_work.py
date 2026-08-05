"""Unit-of-work boundary for atomic metadata changes."""

from __future__ import annotations

from types import TracebackType
from typing import Protocol, Self

from .metadata_repository import MetadataRepository


class UnitOfWork(Protocol):
    metadata: MetadataRepository

    def __enter__(self) -> Self: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None: ...

    def commit(self) -> None: ...

    def rollback(self) -> None: ...


__all__ = ["UnitOfWork"]
