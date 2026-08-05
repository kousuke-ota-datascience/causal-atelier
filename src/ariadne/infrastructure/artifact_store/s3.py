"""S3-compatible immutable artifact store with a worker-local read cache."""

from __future__ import annotations

import hashlib
import shutil
import tempfile
from pathlib import Path, PurePosixPath
from typing import BinaryIO

import boto3
from botocore.exceptions import ClientError

from ariadne.application.ports import ArtifactLocation, ArtifactObject


class S3ArtifactStore:
    backend = "S3"

    def __init__(
        self,
        *,
        bucket: str,
        cache_root: Path,
        endpoint_url: str | None = None,
    ) -> None:
        self.namespace = bucket
        self.cache_root = cache_root.resolve()
        self.cache_root.mkdir(parents=True, exist_ok=True)
        self.client = boto3.client("s3", endpoint_url=endpoint_url)

    def put_file(
        self, source: Path, *, key: str | None = None
    ) -> ArtifactObject:
        digest = _hash_file(source)
        resolved_key = key or f"sha256/{digest[:2]}/{digest}"
        _validate_key(resolved_key)
        try:
            response = self.client.head_object(Bucket=self.namespace, Key=resolved_key)
            stored_digest = response.get("Metadata", {}).get("sha256")
            if stored_digest and stored_digest != digest:
                raise ValueError("S3 object key already contains different content")
        except ClientError as exc:
            if exc.response.get("Error", {}).get("Code") not in {
                "404",
                "NoSuchKey",
                "NotFound",
            }:
                raise
            self.client.upload_file(
                str(source),
                self.namespace,
                resolved_key,
                ExtraArgs={"Metadata": {"sha256": digest}},
            )
        return ArtifactObject(
            ArtifactLocation(self.backend, self.namespace, resolved_key),
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
        key = _key_for(self, location)
        _validate_key(key)
        target = (self.cache_root / Path(*PurePosixPath(key).parts)).resolve()
        if not target.is_relative_to(self.cache_root):
            raise ValueError("object_key escapes the cache root")
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary = target.with_suffix(target.suffix + ".partial")
            self.client.download_file(self.namespace, key, str(temporary))
            temporary.replace(target)
        return target

    def open(self, location: ArtifactLocation | str) -> BinaryIO:
        return self.resolve_local_path(location).open("rb")


def _validate_key(key: str) -> None:
    pure = PurePosixPath(key)
    if pure.is_absolute() or ".." in pure.parts or not pure.parts:
        raise ValueError("object_key must be a safe bucket-relative key")


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _key_for(store: S3ArtifactStore, location: ArtifactLocation | str) -> str:
    if isinstance(location, str):
        return location
    if location.backend != store.backend or location.namespace != store.namespace:
        raise ValueError("artifact location does not belong to this store")
    return location.key


__all__ = ["S3ArtifactStore"]
