"""Graph version router."""

from __future__ import annotations

from fastapi import APIRouter, Header, Request

from ariadne.interfaces.web_api.dependencies import (
    GraphVersionServiceDep, IdempotencyServiceDep, ProductQueryServiceDep,
)
from ariadne.interfaces.web_api.schemas import (
    GraphVersionCreate,
    GraphVersionListResponse,
    GraphVersionResponse,
    GraphVersionUpdate,
)
from ariadne.product.application.graph_version_service import (
    CreateGraphVersionCommand,
    UpdateDraftCommand,
)
from ariadne.product.domain.enums import GraphType
from ariadne.product.domain.errors import EntityNotFound
from ariadne.product.domain.graph_version import GraphVersion

router = APIRouter(tags=["graph-versions"])


def _gv_to_response(gv: GraphVersion) -> GraphVersionResponse:
    return GraphVersionResponse(
        graph_version_id=gv.graph_version_id,
        project_id=gv.project_id,
        source_result_id=gv.source_result_id,
        parent_graph_version_id=gv.parent_graph_version_id,
        name=gv.name,
        graph_type=gv.graph_type.value,
        graph=gv.graph_json,
        content_hash=gv.content_hash,
        edit_rationale=gv.edit_rationale,
        status=gv.status.value,
        created_by=gv.created_by,
        created_at=gv.created_at,
    )


@router.post("/projects/{project_id}/graph-versions", status_code=201, response_model=GraphVersionResponse)
async def create_graph_version(
    project_id: str,
    body: GraphVersionCreate,
    request: Request,
    svc: GraphVersionServiceDep,
    idempotency: IdempotencyServiceDep,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> GraphVersionResponse:
    created_by = request.headers.get("X-User-Id", "anonymous")
    def command() -> dict:  # type: ignore[type-arg]
        graph = svc.create_from_discovery_result(CreateGraphVersionCommand(
            project_id=project_id, source_result_id=body.source_result_id, name=body.name,
            graph_type=GraphType(body.graph_type), graph_json=body.graph, created_by=created_by,
            parent_graph_version_id=body.parent_graph_version_id, edit_rationale=body.edit_rationale,
        ))
        if body.fix_immediately:
            graph = svc.fix_graph(graph.graph_version_id)
        return _gv_to_response(graph).model_dump(mode="json")
    response = idempotency.execute(
        project_id=project_id, scope="graph-version", key=idempotency_key,
        payload=body.model_dump(mode="json"), command=command,
    )
    return GraphVersionResponse.model_validate(response)


@router.get("/projects/{project_id}/graph-versions", response_model=GraphVersionListResponse)
async def list_graph_versions(project_id: str, query: ProductQueryServiceDep) -> GraphVersionListResponse:
    items = query.list_graph_versions(project_id)
    return GraphVersionListResponse(items=[_gv_to_response(gv) for gv in items])


@router.get("/graph-versions/{graph_version_id}", response_model=GraphVersionResponse)
async def get_graph_version(graph_version_id: str, query: ProductQueryServiceDep) -> GraphVersionResponse:
    return _gv_to_response(query.get_graph_version(graph_version_id))


@router.patch("/graph-versions/{graph_version_id}", response_model=GraphVersionResponse)
async def update_graph_version(
    graph_version_id: str, body: GraphVersionUpdate, svc: GraphVersionServiceDep
) -> GraphVersionResponse:
    gv = svc.update_draft(UpdateDraftCommand(
        graph_version_id=graph_version_id,
        graph_json=body.graph,
        edit_rationale=body.edit_rationale,
    ))
    return _gv_to_response(gv)


@router.post("/graph-versions/{graph_version_id}/fix", response_model=GraphVersionResponse)
async def fix_graph_version(
    graph_version_id: str, svc: GraphVersionServiceDep
) -> GraphVersionResponse:
    gv = svc.fix_graph(graph_version_id)
    return _gv_to_response(gv)
