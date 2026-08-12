"""G6 project-scoped workspace closure APIs."""

from __future__ import annotations

from typing import Any, Literal

from fastapi import APIRouter, Query, Request
from fastapi.responses import Response
from pydantic import BaseModel, ConfigDict, Field

from ariadne.interfaces.web_api.dependencies import ProductClosureServiceDep

router = APIRouter(prefix="/projects/{project_id}", tags=["product-closure"])


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class WorkspaceSelectionUpdate(StrictModel):
    research_context_version_id: str | None = None
    dataset_version_id: str | None = None
    analysis_view_id: str | None = None
    unsaved_draft: bool | None = None


class ProjectMemberUpdate(StrictModel):
    role: Literal["OWNER", "EDITOR", "VIEWER"]


class ComparisonCreate(StrictModel):
    result_ids: list[str] = Field(min_length=2, max_length=20)


class LineageLinkCreate(StrictModel):
    source_type: str = Field(min_length=1, max_length=100)
    source_id: str = Field(min_length=1, max_length=100)
    relation_type: Literal[
        "USED_INPUT", "GENERATED", "DERIVED_FROM", "REVISED_FROM",
        "SUPPORTED_BY", "MOTIVATED", "SELECTED", "REJECTED",
    ]
    target_type: str = Field(min_length=1, max_length=100)
    target_id: str = Field(min_length=1, max_length=100)
    evidence: dict[str, Any] = Field(default_factory=dict)


class WorkspaceAnnotationCreate(StrictModel):
    target_type: Literal[
        "Project", "ResearchContextVersion", "AnalysisView",
        "AnalysisSpecification", "Execution", "Result", "GraphVersion",
    ]
    target_id: str = Field(min_length=1, max_length=100)
    statement: str = Field(min_length=1, max_length=8000)
    rationale: str | None = Field(default=None, max_length=8000)
    assumptions: list[Any] = Field(default_factory=list)
    limitations: list[Any] = Field(default_factory=list)
    decision: Literal["SELECTED", "REJECTED", "DEFERRED"] | None = None
    next_actions: list[Any] = Field(default_factory=list)


class WorkspaceAnnotationUpdate(StrictModel):
    statement: str | None = Field(default=None, min_length=1, max_length=8000)
    rationale: str | None = Field(default=None, max_length=8000)
    assumptions: list[Any] | None = None
    limitations: list[Any] | None = None
    decision: Literal["SELECTED", "REJECTED", "DEFERRED"] | None = None
    next_actions: list[Any] | None = None


class ExportCreate(StrictModel):
    result_ids: list[str] = Field(min_length=1, max_length=100)


def _user(request: Request) -> str:
    return request.headers.get("X-User-Id", "anonymous")


@router.get("/operation-availability")
async def operation_availability(
    project_id: str, request: Request, service: ProductClosureServiceDep,
    resource_type: str | None = None, resource_id: str | None = None,
    route: str | None = None,
) -> dict[str, Any]:
    return service.operation_availability(
        project_id, user_id=_user(request), resource_type=resource_type,
        resource_id=resource_id, route=route,
    )


@router.get("/workspace-state")
async def workspace_state(
    project_id: str, request: Request, service: ProductClosureServiceDep
) -> dict[str, Any]:
    return service.workspace_state(project_id, user_id=_user(request))


@router.put("/workspace-state")
async def update_workspace_state(
    project_id: str, body: WorkspaceSelectionUpdate, request: Request,
    service: ProductClosureServiceDep,
) -> dict[str, Any]:
    return service.update_workspace_state(
        project_id, body.model_dump(exclude_unset=True, mode="json"),
        user_id=_user(request),
    )


@router.put("/members/{user_id}")
async def set_member_role(
    project_id: str, user_id: str, body: ProjectMemberUpdate, request: Request,
    service: ProductClosureServiceDep,
) -> dict[str, Any]:
    return service.set_member_role(project_id, user_id, body.role, actor_id=_user(request))


@router.get("/results")
async def list_results(
    project_id: str, request: Request, service: ProductClosureServiceDep
) -> dict[str, Any]:
    return {"items": service.list_results(project_id, user_id=_user(request))}


@router.get("/results/summary")
async def results_summary(
    project_id: str, request: Request, service: ProductClosureServiceDep
) -> dict[str, Any]:
    return service.results_summary(project_id, user_id=_user(request))


@router.get("/results/{result_id}")
async def result_detail(
    project_id: str, result_id: str, request: Request,
    service: ProductClosureServiceDep,
    include_sensitive: bool = Query(default=False),
) -> dict[str, Any]:
    return service.result_detail(
        project_id, result_id, user_id=_user(request),
        include_sensitive=include_sensitive,
    )


@router.post("/comparisons", status_code=201)
async def create_comparison(
    project_id: str, body: ComparisonCreate, request: Request,
    service: ProductClosureServiceDep,
) -> dict[str, Any]:
    return service.compare_results(project_id, body.result_ids, user_id=_user(request))


@router.get("/results/{result_id}/lineage")
async def result_lineage(
    project_id: str, result_id: str, request: Request,
    service: ProductClosureServiceDep,
) -> dict[str, Any]:
    return service.result_lineage(project_id, result_id, user_id=_user(request))


@router.get("/lineage")
async def project_lineage(
    project_id: str, request: Request, service: ProductClosureServiceDep
) -> dict[str, Any]:
    return service.project_lineage(project_id, user_id=_user(request))


@router.post("/lineage-links", status_code=201)
async def create_lineage_link(
    project_id: str, body: LineageLinkCreate, request: Request,
    service: ProductClosureServiceDep,
) -> dict[str, Any]:
    return service.create_lineage_link(
        project_id, body.model_dump(mode="json"), user_id=_user(request)
    )


@router.get("/workspace-annotations")
async def list_workspace_annotations(
    project_id: str, request: Request, service: ProductClosureServiceDep,
    target_type: str | None = Query(default=None),
    target_id: str | None = Query(default=None),
) -> dict[str, Any]:
    return {"items": service.list_annotations(
        project_id, user_id=_user(request),
        target_type=target_type, target_id=target_id,
    )}


@router.post("/workspace-annotations", status_code=201)
async def create_workspace_annotation(
    project_id: str, body: WorkspaceAnnotationCreate, request: Request,
    service: ProductClosureServiceDep,
) -> dict[str, Any]:
    return service.create_annotation(
        project_id, body.model_dump(mode="json"), user_id=_user(request)
    )


@router.patch("/workspace-annotations/{annotation_id}")
async def update_workspace_annotation(
    project_id: str, annotation_id: str, body: WorkspaceAnnotationUpdate,
    request: Request, service: ProductClosureServiceDep,
) -> dict[str, Any]:
    return service.update_annotation(
        project_id, annotation_id,
        body.model_dump(exclude_unset=True, mode="json"), user_id=_user(request),
    )


@router.get("/artifacts/{artifact_id}")
async def artifact_metadata(
    project_id: str, artifact_id: str, request: Request,
    service: ProductClosureServiceDep,
) -> dict[str, Any]:
    return service.get_artifact(project_id, artifact_id, user_id=_user(request))


@router.get("/artifacts/{artifact_id}/download")
async def download_artifact(
    project_id: str, artifact_id: str, request: Request,
    service: ProductClosureServiceDep,
) -> Response:
    artifact, content = service.download_artifact(
        project_id, artifact_id, user_id=_user(request)
    )
    return Response(
        content=content, media_type=artifact["media_type"],
        headers={
            "Content-Disposition": f'attachment; filename="{artifact_id}"',
            "Digest": f"sha-256={artifact['content_hash']}",
            "X-Content-Type-Options": "nosniff",
            "Cache-Control": "private, no-store",
        },
    )


@router.post("/exports", status_code=201)
async def create_export(
    project_id: str, body: ExportCreate, request: Request,
    service: ProductClosureServiceDep,
) -> dict[str, Any]:
    return service.create_export(project_id, body.result_ids, user_id=_user(request))


@router.get("/exports/{export_id}")
async def get_export(
    project_id: str, export_id: str, request: Request,
    service: ProductClosureServiceDep,
) -> dict[str, Any]:
    return service.get_export(project_id, export_id, user_id=_user(request))


@router.get("/exports/{export_id}/download")
async def download_export(
    project_id: str, export_id: str, request: Request,
    service: ProductClosureServiceDep,
) -> Response:
    artifact, content = service.download_artifact(
        project_id, export_id, user_id=_user(request)
    )
    return Response(
        content=content, media_type="application/json",
        headers={
            "Content-Disposition": f'attachment; filename="ariadne-export-{export_id}.json"',
            "Digest": f"sha-256={artifact['content_hash']}",
            "X-Content-Type-Options": "nosniff",
            "Cache-Control": "private, no-store",
        },
    )
