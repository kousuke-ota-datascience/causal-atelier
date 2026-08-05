"""Database session factory for the product domain."""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ariadne.product.persistence.orm_models import ProductBase
from ariadne.product.persistence.unit_of_work import SqlUnitOfWork


def build_engine(database_url: str, **kwargs: object):  # type: ignore[no-untyped-def]
    return create_engine(database_url, **kwargs)  # type: ignore[arg-type]


def create_all_tables(database_url: str) -> None:
    engine = build_engine(database_url)
    ProductBase.metadata.create_all(engine)


class SessionFactory:
    def __init__(self, database_url: str, **engine_kwargs: object) -> None:
        self._engine = build_engine(database_url, **engine_kwargs)
        self._session_factory = sessionmaker(bind=self._engine)

    @contextmanager
    def unit_of_work(self) -> Generator[SqlUnitOfWork, None, None]:
        session: Session = self._session_factory()
        try:
            yield SqlUnitOfWork(session)
        finally:
            session.close()
