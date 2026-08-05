"""Local filesystem implementation of ArtifactStorePort."""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

from ariadne.product.ports.artifact_store import ArtifactStorePort, StoredArtifact


class LocalArtifactStore:
    """Stores artifacts as files under a configured root directory."""

    def __init__(self, root: Path) -> None:
        self._root = root
        self._root.mkdir(parents=True, exist_ok=True)

    def store(
        self,
        source_path: Path,
        object_key: str,
        media_type: str = "application/octet-stream",
    ) -> StoredArtifact:
        dest = self._root / object_key
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, dest)

        content_hash = _sha256_file(dest)
        size_bytes = dest.stat().st_size

        return StoredArtifact(
            object_key=object_key,
            content_hash=content_hash,
            size_bytes=size_bytes,
            media_type=media_type,
        )

    def retrieve(self, object_key: str, dest_path: Path) -> None:
        src = self._root / object_key
        if not src.exists():
            raise FileNotFoundError(f"Artifact not found: {object_key!r}")
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest_path)

    def exists(self, object_key: str) -> bool:
        return (self._root / object_key).exists()

    def delete(self, object_key: str) -> None:
        path = self._root / object_key
        if path.exists():
            path.unlink()


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()
