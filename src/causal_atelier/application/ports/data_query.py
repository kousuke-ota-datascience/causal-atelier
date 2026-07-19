"""Port for bounded tabular inspection and visualization queries."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol


class QueryResult(Protocol):
    def to_dict(self) -> dict[str, Any]: ...


class DataQuery(Protocol):
    def schema(self, path: Path, file_format: str) -> list[dict[str, Any]]: ...

    def preview(
        self, path: Path, file_format: str, *, limit: int
    ) -> dict[str, Any]: ...

    def profile(self, path: Path, file_format: str) -> dict[str, Any]: ...

    def execute(
        self, path: Path, file_format: str, specification: dict[str, Any]
    ) -> QueryResult: ...


__all__ = ["DataQuery", "QueryResult"]
