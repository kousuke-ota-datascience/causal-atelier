"""Azure Blob artifact store with a worker-local read-through cache."""

from __future__ import annotations

import hashlib
import shutil
import tempfile
from pathlib import Path, PurePosixPath
from typing import BinaryIO

from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import BlobServiceClient, ContentSettings

from causal_atelier.application.ports import ArtifactLocation, ArtifactObject


class AzureBlobArtifactStore:
    backend = "AZURE_BLOB"

    def __init__(
        self,
        *,
        container: str,
        cache_root: Path,
        connection_string: str | None = None,
        account_url: str | None = None,
        credential: object | None = None,
    ) -> None:
        if connection_string:
            client = BlobServiceClient.from_connection_string(connection_string)
        elif account_url:
            client = BlobServiceClient(account_url, credential=credential)
        else:
            raise ValueError(
                "Azure Blob requires a connection string or an account URL"
            )
        self.namespace = container
        self.container_client = client.get_container_client(container)
        self.cache_root = cache_root.resolve()
        self.cache_root.mkdir(parents=True, exist_ok=True)

    def put_file(self, source: Path, *, key: str | None = None) -> ArtifactObject:
        digest = _hash_file(source)
        resolved_key = key or f"sha256/{digest[:2]}/{digest}"
        _validate_key(resolved_key)
        blob = self.container_client.get_blob_client(resolved_key)
        try:
            properties = blob.get_blob_properties()
            metadata = properties.metadata or {}
            if metadata.get("sha256") not in {None, digest}:
                raise ValueError(
                    "Azure Blob key already contains different content"
                )
            version = properties.version_id
        except ResourceNotFoundError:
            with source.open("rb") as stream:
                response = blob.upload_blob(
                    stream,
                    overwrite=False,
                    metadata={"sha256": digest},
                    content_settings=ContentSettings(
                        content_type="application/octet-stream"
                    ),
                )
            version = response.get("version_id")
        return ArtifactObject(
            ArtifactLocation(self.backend, self.namespace, resolved_key, version),
            source.stat().st_size,
            digest,
        )

    def put_stream(self, stream: BinaryIO, *, key: str) -> ArtifactObject:
        _validate_key(key)
        with tempfile.NamedTemporaryFile(delete=False) as temporary:
            path = Path(temporary.name)
            shutil.copyfileobj(stream, temporary, length=1024 * 1024)
        try:
            return self.put_file(path, key=key)
        finally:
            path.unlink(missing_ok=True)

    def resolve_local_path(self, location: ArtifactLocation | str) -> Path:
        key, version = _location_for(self, location)
        relative = Path(*PurePosixPath(key).parts)
        if version:
            version_key = hashlib.sha256(version.encode("utf-8")).hexdigest()[:24]
            relative = Path("versions") / version_key / relative
        target = (self.cache_root / relative).resolve()
        if not target.is_relative_to(self.cache_root):
            raise ValueError("artifact key escapes the cache root")
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary = target.with_suffix(target.suffix + ".partial")
            downloader = self.container_client.download_blob(key, version_id=version)
            with temporary.open("wb") as stream:
                downloader.readinto(stream)
            temporary.replace(target)
        return target

    def open(self, location: ArtifactLocation | str) -> BinaryIO:
        return self.resolve_local_path(location).open("rb")


def _location_for(
    store: AzureBlobArtifactStore, location: ArtifactLocation | str
) -> tuple[str, str | None]:
    if isinstance(location, str):
        _validate_key(location)
        return location, None
    if location.backend != store.backend or location.namespace != store.namespace:
        raise ValueError("artifact location does not belong to this store")
    _validate_key(location.key)
    return location.key, location.version


def _validate_key(key: str) -> None:
    pure = PurePosixPath(key)
    if pure.is_absolute() or ".." in pure.parts or not pure.parts:
        raise ValueError("artifact key must be a safe namespace-relative path")


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


__all__ = ["AzureBlobArtifactStore"]
