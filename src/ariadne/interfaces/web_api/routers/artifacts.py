"""Artifact metadata and verified download endpoints."""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import Response

from ariadne.interfaces.web_api.dependencies import ArtifactServiceDep
from ariadne.interfaces.web_api.schemas import ArtifactResponse

router = APIRouter(tags=["artifacts"])


def _response(item) -> ArtifactResponse:  # type: ignore[no-untyped-def]
    return ArtifactResponse(
        artifact_id=item.artifact_id, project_id=item.project_id,
        execution_id=item.execution_id, result_id=item.result_id,
        artifact_type=item.artifact_type.value, object_key=item.object_key,
        content_hash=item.content_hash, media_type=item.media_type,
        size_bytes=item.size_bytes, metadata=item.metadata_json, created_at=item.created_at,
    )


@router.get("/artifacts/{artifact_id}", response_model=ArtifactResponse)
async def get_artifact(artifact_id: str, service: ArtifactServiceDep) -> ArtifactResponse:
    return _response(service.get(artifact_id))


@router.get("/artifacts/{artifact_id}/download")
async def download_artifact(artifact_id: str, service: ArtifactServiceDep) -> Response:
    artifact, content = service.read_verified(artifact_id)
    return Response(content=content, media_type=artifact.media_type, headers={
        "Content-Disposition": f'attachment; filename="{artifact_id}"',
        "Digest": f"sha-256={artifact.content_hash}",
    })
