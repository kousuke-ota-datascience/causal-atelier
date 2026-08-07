"""Research Context and common Analysis Specification lifecycle APIs."""

from __future__ import annotations

from typing import Any, Literal

from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict, Field

from ariadne.interfaces.web_api.dependencies import WorkspaceLifecycleServiceDep

router = APIRouter(tags=["workspace-lifecycle"])


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ResearchContextCreate(StrictModel):
    context_key: str
    problem_statement: str = ""
    research_questions: list[str] = Field(default_factory=list)
    significance: str | None = None
    hypotheses: list[str] = Field(default_factory=list)
    decision_context: dict[str, Any] = Field(default_factory=dict)
    relations: list[dict[str, str]] = Field(default_factory=list)


class ResearchContextPatch(StrictModel):
    problem_statement: str | None = None
    research_questions: list[str] | None = None
    significance: str | None = None
    hypotheses: list[str] | None = None
    decision_context: dict[str, Any] | None = None
    relations: list[dict[str, str]] | None = None


class AnalysisSpecificationCreate(StrictModel):
    schema_version: Literal["analysis-specification/1"]
    specification_key: str
    analysis_family: Literal["EXPLORATORY", "CAUSAL", "PREDICTIVE"]
    research_context_version_id: str
    dataset_version_id: str
    analysis_view_id: str | None = None
    analysis_mode: Literal["EXPLORATORY", "CONFIRMATORY"]
    family_spec_schema_version: str
    family_spec: dict[str, Any]
    revision_context: dict[str, Any] | None = None
    warnings: list[dict[str, Any]] = Field(default_factory=list)


class AnalysisSpecificationPatch(StrictModel):
    analysis_family: Literal["EXPLORATORY", "CAUSAL", "PREDICTIVE"] | None = None
    research_context_version_id: str | None = None
    dataset_version_id: str | None = None
    analysis_view_id: str | None = None
    analysis_mode: Literal["EXPLORATORY", "CONFIRMATORY"] | None = None
    family_spec_schema_version: str | None = None
    family_spec: dict[str, Any] | None = None
    revision_context: dict[str, Any] | None = None
    warnings: list[dict[str, Any]] | None = None


class AnalysisSpecificationRevise(StrictModel):
    change_reason: str
    changes: dict[str, Any] = Field(default_factory=dict)


@router.post("/projects/{project_id}/research-contexts", status_code=201)
async def create_research_context(
    project_id: str,
    body: ResearchContextCreate,
    request: Request,
    svc: WorkspaceLifecycleServiceDep,
) -> dict[str, Any]:
    return svc.create_research_context(
        project_id,
        body.model_dump(mode="json"),
        created_by=request.headers.get("X-User-Id", "anonymous"),
    )


@router.get("/projects/{project_id}/research-contexts")
async def list_research_contexts(
    project_id: str, svc: WorkspaceLifecycleServiceDep
) -> dict[str, Any]:
    return {"items": svc.list_research_contexts(project_id)}


@router.get("/projects/{project_id}/research-contexts/{context_id}")
async def get_research_context(
    project_id: str, context_id: str, svc: WorkspaceLifecycleServiceDep
) -> dict[str, Any]:
    return svc.get_research_context(project_id, context_id)


@router.patch("/projects/{project_id}/research-contexts/{context_id}")
async def patch_research_context(
    project_id: str,
    context_id: str,
    body: ResearchContextPatch,
    svc: WorkspaceLifecycleServiceDep,
) -> dict[str, Any]:
    return svc.update_research_context(
        project_id, context_id, body.model_dump(exclude_unset=True, mode="json")
    )


@router.post("/projects/{project_id}/research-contexts/{context_id}/fix")
async def fix_research_context(
    project_id: str, context_id: str, svc: WorkspaceLifecycleServiceDep
) -> dict[str, Any]:
    return svc.fix_research_context(project_id, context_id)


@router.get("/projects/{project_id}/research-contexts/{context_id}/usage")
async def research_context_usage(
    project_id: str, context_id: str, svc: WorkspaceLifecycleServiceDep
) -> dict[str, Any]:
    return svc.research_context_usage(project_id, context_id)


@router.post("/projects/{project_id}/analysis-specifications", status_code=201)
async def create_analysis_specification(
    project_id: str,
    body: AnalysisSpecificationCreate,
    request: Request,
    svc: WorkspaceLifecycleServiceDep,
) -> dict[str, Any]:
    payload = body.model_dump(mode="json")
    payload.pop("schema_version")
    return svc.create_analysis_specification(
        project_id,
        payload,
        created_by=request.headers.get("X-User-Id", "anonymous"),
    )


@router.get("/projects/{project_id}/analysis-specifications")
async def list_analysis_specifications(
    project_id: str, svc: WorkspaceLifecycleServiceDep
) -> dict[str, Any]:
    return {"items": svc.list_analysis_specifications(project_id)}


@router.get("/projects/{project_id}/analysis-specifications/{spec_id}")
async def get_analysis_specification(
    project_id: str, spec_id: str, svc: WorkspaceLifecycleServiceDep
) -> dict[str, Any]:
    return svc.get_analysis_specification(project_id, spec_id)


@router.patch("/projects/{project_id}/analysis-specifications/{spec_id}")
async def patch_analysis_specification(
    project_id: str,
    spec_id: str,
    body: AnalysisSpecificationPatch,
    svc: WorkspaceLifecycleServiceDep,
) -> dict[str, Any]:
    return svc.update_analysis_specification(
        project_id, spec_id, body.model_dump(exclude_unset=True, mode="json")
    )


@router.post("/projects/{project_id}/analysis-specifications/{spec_id}/validate")
async def validate_analysis_specification(
    project_id: str, spec_id: str, svc: WorkspaceLifecycleServiceDep
) -> dict[str, Any]:
    return svc.validate_analysis_specification(project_id, spec_id)


@router.post("/projects/{project_id}/analysis-specifications/{spec_id}/fix")
async def fix_analysis_specification(
    project_id: str, spec_id: str, svc: WorkspaceLifecycleServiceDep
) -> dict[str, Any]:
    return svc.fix_analysis_specification(project_id, spec_id)


@router.post(
    "/projects/{project_id}/analysis-specifications/{spec_id}/revise",
    status_code=201,
)
async def revise_analysis_specification(
    project_id: str,
    spec_id: str,
    body: AnalysisSpecificationRevise,
    request: Request,
    svc: WorkspaceLifecycleServiceDep,
) -> dict[str, Any]:
    return svc.revise_analysis_specification(
        project_id,
        spec_id,
        changes=body.changes,
        change_reason=body.change_reason,
        created_by=request.headers.get("X-User-Id", "anonymous"),
    )
