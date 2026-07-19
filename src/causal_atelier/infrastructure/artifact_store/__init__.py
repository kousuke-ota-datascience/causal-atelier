"""Registry-driven artifact store adapter construction."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from causal_atelier.application.ports import ArtifactLocation, ArtifactStore

from .azure_blob import AzureBlobArtifactStore
from .local import LocalArtifactStore
from .s3 import S3ArtifactStore

ArtifactStoreFactory = Callable[[Any], ArtifactStore]
ARTIFACT_STORE_FACTORIES: dict[str, ArtifactStoreFactory] = {}


def register_artifact_store(backend: str, factory: ArtifactStoreFactory) -> None:
    """Register or replace an adapter factory for a backend code."""

    normalized = backend.upper()
    if not normalized:
        raise ValueError("artifact backend code must not be empty")
    ARTIFACT_STORE_FACTORIES[normalized] = factory


def build_artifact_store(settings: Any) -> ArtifactStore:
    backend = settings.artifact_backend.upper()
    try:
        factory = ARTIFACT_STORE_FACTORIES[backend]
    except KeyError as exc:
        supported = ", ".join(sorted(ARTIFACT_STORE_FACTORIES))
        raise ValueError(
            f"Unsupported artifact backend: {backend}; supported: {supported}"
        ) from exc
    return factory(settings)


def artifact_location(record: Any) -> ArtifactLocation:
    """Translate the legacy persistence columns into a neutral locator."""

    return ArtifactLocation(
        backend=record.backend,
        namespace=record.bucket,
        key=record.object_key,
        version=record.object_version or None,
    )


def _build_local(settings: Any) -> ArtifactStore:
    return LocalArtifactStore(settings.artifact_root)


def _build_s3(settings: Any) -> ArtifactStore:
    if not settings.s3_bucket:
        raise ValueError(
            "CAUSAL_ATELIER_S3_BUCKET is required for the S3 artifact backend"
        )
    return S3ArtifactStore(
        bucket=settings.s3_bucket,
        cache_root=settings.workspace_root / "s3-cache",
        endpoint_url=settings.s3_endpoint_url,
    )


def _build_azure_blob(settings: Any) -> ArtifactStore:
    if not settings.azure_blob_container:
        raise ValueError(
            "CAUSAL_ATELIER_AZURE_BLOB_CONTAINER is required for Azure Blob"
        )
    return AzureBlobArtifactStore(
        container=settings.azure_blob_container,
        cache_root=settings.workspace_root / "azure-blob-cache",
        connection_string=settings.azure_storage_connection_string,
        account_url=settings.azure_storage_account_url,
        credential=settings.azure_storage_credential,
    )


register_artifact_store("LOCAL", _build_local)
register_artifact_store("S3", _build_s3)
register_artifact_store("AZURE_BLOB", _build_azure_blob)


__all__ = [
    "ARTIFACT_STORE_FACTORIES",
    "ArtifactStoreFactory",
    "AzureBlobArtifactStore",
    "LocalArtifactStore",
    "S3ArtifactStore",
    "build_artifact_store",
    "artifact_location",
    "register_artifact_store",
]
