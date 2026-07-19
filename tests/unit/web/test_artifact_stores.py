from __future__ import annotations

import io
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest
from azure.core.exceptions import ResourceNotFoundError

from causal_atelier.application.ports import ArtifactLocation
from causal_atelier.infrastructure.artifact_store import (
    ARTIFACT_STORE_FACTORIES,
    AzureBlobArtifactStore,
    build_artifact_store,
    register_artifact_store,
)
from causal_atelier.infrastructure.artifact_store.local import LocalArtifactStore


def test_local_store_uses_backend_neutral_location(tmp_path: Path) -> None:
    store = LocalArtifactStore(tmp_path / "objects")
    stored = store.put_stream(io.BytesIO(b"payload"), key="runs/1/result.json")

    assert stored.location == ArtifactLocation(
        backend="LOCAL", namespace=None, key="runs/1/result.json"
    )
    assert store.resolve_local_path(stored.location).read_bytes() == b"payload"
    with pytest.raises(ValueError, match="does not belong"):
        store.resolve_local_path(ArtifactLocation("S3", "bucket", "object"))


def test_artifact_store_factory_is_extensible_registry(tmp_path: Path) -> None:
    marker = object()
    previous = ARTIFACT_STORE_FACTORIES.get("TEST")
    try:
        register_artifact_store("test", lambda settings: marker)
        settings = SimpleNamespace(artifact_backend="TEST")
        assert build_artifact_store(settings) is marker
    finally:
        if previous is None:
            ARTIFACT_STORE_FACTORIES.pop("TEST", None)
        else:
            ARTIFACT_STORE_FACTORIES["TEST"] = previous


def test_azure_blob_store_returns_container_location(tmp_path: Path) -> None:
    service = Mock()
    container = service.get_container_client.return_value
    blob = container.get_blob_client.return_value
    blob.get_blob_properties.side_effect = ResourceNotFoundError("missing")
    blob.upload_blob.return_value = {"version_id": "version-1"}

    source = tmp_path / "result.csv"
    source.write_bytes(b"a,b\n1,2\n")
    with patch(
        "causal_atelier.infrastructure.artifact_store.azure_blob."
        "BlobServiceClient.from_connection_string",
        return_value=service,
    ):
        store = AzureBlobArtifactStore(
            container="analysis-artifacts",
            cache_root=tmp_path / "cache",
            connection_string="UseDevelopmentStorage=true",
        )
        stored = store.put_file(source, key="runs/1/result.csv")

    assert stored.location == ArtifactLocation(
        backend="AZURE_BLOB",
        namespace="analysis-artifacts",
        key="runs/1/result.csv",
        version="version-1",
    )
    blob.upload_blob.assert_called_once()
