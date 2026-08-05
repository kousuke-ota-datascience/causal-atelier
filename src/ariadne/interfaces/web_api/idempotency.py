"""DB-backed replay records for HTTP creation commands."""

from __future__ import annotations

import hashlib
import json
import uuid
import threading
from datetime import datetime, timezone
from typing import Any, Callable

from sqlalchemy import select, text

from ariadne.product.domain.errors import DomainError
from ariadne.product.persistence.orm_models import IdempotencyRecordOrm


class IdempotencyConflict(DomainError):
    pass


class IdempotencyService:
    _process_lock = threading.RLock()

    def __init__(self, session_factory: Any) -> None:
        self._session_factory = session_factory

    def execute(
        self,
        *,
        project_id: str,
        scope: str,
        key: str | None,
        payload: Any,
        command: Callable[[], dict[str, Any]],
    ) -> dict[str, Any]:
        if not key:
            return command()
        request_hash = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
        ).hexdigest()
        # The in-process lock covers SQLite/component tests. PostgreSQL's
        # transaction-scoped advisory lock provides cross-process exclusion.
        with self._process_lock, self._session_factory() as session:
            if session.bind.dialect.name == "postgresql":
                lock_id = int.from_bytes(
                    hashlib.sha256(f"{project_id}:{scope}:{key}".encode()).digest()[:8],
                    byteorder="big", signed=True,
                )
                session.execute(text("SELECT pg_advisory_xact_lock(:lock_id)"), {"lock_id": lock_id})
            existing = session.scalars(
                select(IdempotencyRecordOrm).where(
                    IdempotencyRecordOrm.project_id == project_id,
                    IdempotencyRecordOrm.scope == scope,
                    IdempotencyRecordOrm.idempotency_key == key,
                )
            ).first()
            if existing:
                if existing.request_hash != request_hash:
                    raise IdempotencyConflict("Idempotency-Key was reused with a different request")
                return dict(existing.response_json)
            response = command()
            session.add(IdempotencyRecordOrm(
                idempotency_id=str(uuid.uuid4()), project_id=project_id, scope=scope,
                idempotency_key=key, request_hash=request_hash, response_json=response,
                created_at=datetime.now(timezone.utc),
            ))
            session.commit()
            return response
