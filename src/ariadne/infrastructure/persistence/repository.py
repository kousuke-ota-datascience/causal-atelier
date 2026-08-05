"""SQLAlchemy adapters for metadata repository and durable event ports."""

from __future__ import annotations

from typing import Any, TypeVar

from sqlalchemy.orm import Session

from ariadne.infrastructure.persistence import models as m

T = TypeVar("T")


class SqlAlchemyMetadataRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, entity_type: type[T], entity_id: Any) -> T | None:
        return self.session.get(entity_type, entity_id)

    def add(self, entity: T) -> None:
        self.session.add(entity)

    def delete(self, entity: T) -> None:
        self.session.delete(entity)

    def flush(self) -> None:
        self.session.flush()

    def scalar(self, statement: Any) -> Any:
        return self.session.scalar(statement)

    def scalars(self, statement: Any) -> Any:
        return self.session.scalars(statement)

    def execute(self, statement: Any) -> Any:
        return self.session.execute(statement)

    def merge(self, entity: T) -> T:
        return self.session.merge(entity)

    def refresh(self, entity: T) -> None:
        self.session.refresh(entity)

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()


class SqlAlchemyOutboxQueue:
    def __init__(self, repository: SqlAlchemyMetadataRepository) -> None:
        self.repository = repository

    def enqueue(
        self,
        *,
        aggregate_type: str,
        aggregate_id: str,
        event_type: str,
        payload: dict[str, Any],
    ) -> str:
        event = m.OutboxEvent(
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            event_type=event_type,
            payload_json=payload,
        )
        self.repository.add(event)
        self.repository.flush()
        return event.id


__all__ = ["SqlAlchemyMetadataRepository", "SqlAlchemyOutboxQueue"]
