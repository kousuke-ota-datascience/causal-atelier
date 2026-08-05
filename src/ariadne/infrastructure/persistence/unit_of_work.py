"""SQLAlchemy unit-of-work adapter."""

from __future__ import annotations

from types import TracebackType
from typing import Self

from sqlalchemy.orm import Session, sessionmaker

from .repository import SqlAlchemyMetadataRepository


class SqlAlchemyUnitOfWork:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.session_factory = session_factory
        self.session: Session | None = None
        self.metadata: SqlAlchemyMetadataRepository

    def __enter__(self) -> Self:
        self.session = self.session_factory()
        self.metadata = SqlAlchemyMetadataRepository(self.session)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        try:
            if exc_type is None:
                self.commit()
            else:
                self.rollback()
        finally:
            assert self.session is not None
            self.session.close()
        return False

    def commit(self) -> None:
        assert self.session is not None
        self.session.commit()

    def rollback(self) -> None:
        assert self.session is not None
        self.session.rollback()


__all__ = ["SqlAlchemyUnitOfWork"]
