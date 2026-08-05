"""Port for durable asynchronous work publication."""

from __future__ import annotations

from typing import Any, Protocol


class EventQueue(Protocol):
    def enqueue(
        self,
        *,
        aggregate_type: str,
        aggregate_id: str,
        event_type: str,
        payload: dict[str, Any],
    ) -> str: ...


__all__ = ["EventQueue"]
