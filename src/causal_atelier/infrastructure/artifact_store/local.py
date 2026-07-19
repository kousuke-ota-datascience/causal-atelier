"""Content-addressable local filesystem artifact store."""

from __future__ import annotations

import hashlib
import shutil
import tempfile
from pathlib import Path, PurePosixPath
from typing import BinaryIO

from causal_atelier.application.ports import ArtifactLocation, ArtifactObject


class LocalArtifactStore:
    backend = "LOCAL"
    namespace = None

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def put_file(
        self, source: Path, *, key: str | None = None
    ) -> ArtifactObject:
        digest = _hash_file(source)
        resolved_key = key or f"sha256/{digest[:2]}/{digest}"
        target = self._safe_path(resolved_key)
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            temporary = target.with_suffix(target.suffix + ".partial")
            shutil.copyfile(source, temporary)
            temporary.replace(target)
        return ArtifactObject(
            ArtifactLocation(self.backend, self.namespace, resolved_key),
            target.stat().st_size,
            digest,
        )

    def put_stream(self, stream: BinaryIO, *, key: str) -> ArtifactObject:
        target = self._safe_path(key)
        target.parent.mkdir(parents=True, exist_ok=True)
        digest = hashlib.sha256()
        with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as temporary:
            temporary_path = Path(temporary.name)
            while chunk := stream.read(1024 * 1024):
                digest.update(chunk)
                temporary.write(chunk)
        temporary_path.replace(target)
        return ArtifactObject(
            ArtifactLocation(self.backend, self.namespace, key),
            target.stat().st_size,
            digest.hexdigest(),
        )

    def resolve_local_path(self, location: ArtifactLocation | str) -> Path:
        key = _key_for(self, location)
        path = self._safe_path(key)
        if not path.is_file():
            raise FileNotFoundError(f"artifact object does not exist: {key}")
        return path

    def open(self, location: ArtifactLocation | str) -> BinaryIO:
        return self.resolve_local_path(location).open("rb")

    def _safe_path(self, object_key: str) -> Path:
        pure = PurePosixPath(object_key)
        if pure.is_absolute() or ".." in pure.parts or not pure.parts:
            raise ValueError("object_key must be a safe artifact-root-relative path")
        resolved = (self.root / Path(*pure.parts)).resolve()
        if not resolved.is_relative_to(self.root):
            raise ValueError("object_key escapes the artifact root")
        return resolved


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _key_for(store: LocalArtifactStore, location: ArtifactLocation | str) -> str:
    if isinstance(location, str):
        return location
    if location.backend != store.backend or location.namespace != store.namespace:
        raise ValueError("artifact location does not belong to this store")
    return location.key


__all__ = ["LocalArtifactStore"]
