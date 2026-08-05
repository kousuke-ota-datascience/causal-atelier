"""Artifact metadata and verified content queries."""

from __future__ import annotations

import hashlib
import tempfile
from pathlib import Path
from typing import Any

from ariadne.product.domain.errors import ArtifactHashMismatch, EntityNotFound
from ariadne.product.ports.artifact_store import ArtifactStorePort


class ArtifactService:
    def __init__(self, uow_factory: Any, artifact_store: ArtifactStorePort) -> None:
        self._uow_factory = uow_factory
        self._artifact_store = artifact_store

    def get(self, artifact_id: str):  # type: ignore[no-untyped-def]
        with self._uow_factory() as uow:
            artifact = uow.artifacts.get(artifact_id)
            if artifact is None:
                raise EntityNotFound("Artifact", artifact_id)
            return artifact

    def read_verified(self, artifact_id: str) -> tuple[object, bytes]:
        artifact = self.get(artifact_id)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "artifact"
            self._artifact_store.retrieve(artifact.object_key, path)
            content = path.read_bytes()
        if hashlib.sha256(content).hexdigest() != artifact.content_hash:
            raise ArtifactHashMismatch(f"Artifact hash mismatch: {artifact_id}")
        return artifact, content
