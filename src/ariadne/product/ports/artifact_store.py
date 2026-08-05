"""ArtifactStore port protocol."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class StoredArtifact:
    object_key: str
    content_hash: str
    size_bytes: int
    media_type: str


class ArtifactStorePort(Protocol):
    def store(
        self,
        source_path: Path,
        object_key: str,
        media_type: str = "application/octet-stream",
    ) -> StoredArtifact: ...

    def retrieve(self, object_key: str, dest_path: Path) -> None: ...

    def exists(self, object_key: str) -> bool: ...

    def delete(self, object_key: str) -> None: ...
