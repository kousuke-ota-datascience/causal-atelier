"""Application contract for immutable artifact object storage."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Protocol


@dataclass(frozen=True)
class ArtifactLocation:
    """Backend-neutral address of an immutable object."""

    backend: str
    namespace: str | None
    key: str
    version: str | None = None


@dataclass(frozen=True)
class ArtifactObject:
    location: ArtifactLocation
    size_bytes: int
    checksum: str


class ArtifactStore(Protocol):
    backend: str
    namespace: str | None

    def put_file(self, source: Path, *, key: str | None = None) -> ArtifactObject: ...

    def put_stream(self, stream: BinaryIO, *, key: str) -> ArtifactObject: ...

    def resolve_local_path(self, location: ArtifactLocation | str) -> Path: ...

    def open(self, location: ArtifactLocation | str) -> BinaryIO: ...


__all__ = ["ArtifactLocation", "ArtifactObject", "ArtifactStore"]
