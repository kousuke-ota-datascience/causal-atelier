"""ENH-E3 Analysis View and Explore API."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from ariadne.interfaces.web_api.dependencies import ExploratoryWorkspaceServiceDep
from ariadne.product.application.exploratory_service import ExploratoryResultProjection
from ariadne.product.domain.execution import Execution
from ariadne.product.persistence.orm_models import AnalysisViewOrm, FamilyExecutionOrm, FamilyResultOrm

router = APIRouter(tags=["analysis-views", "exploration"])


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class AnalysisViewCreate(StrictModel):
    view_key: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=200)
    spec: dict[str, Any]


class AnalysisViewUpdate(StrictModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    spec: dict[str, Any] | None = None


class AnalysisViewResponse(StrictModel):
    analysis_view_id: str
    project_id: str
    source_dataset_version_id: str
    view_key: str
    version_number: int
    name: str
    status: str
    schema_version: str
    spec: dict[str, Any]
    content_hash: str | None
    manifest: dict[str, Any]
    created_by: str
    created_at: datetime | None
    fixed_at: datetime | None


class AnalysisViewListResponse(StrictModel):
    items: list[AnalysisViewResponse]
    next_cursor: str | None = None


class ExplorationRequest(StrictModel):
    dataset_version_id: str
    analysis_view_id: str | None = None
    family_spec: dict[str, Any]


class ExplorationPreviewResponse(StrictModel):
    schema_version: str
    analysis_family: Literal["EXPLORATORY"]
    result_type: str
    analytical_status: str
    summary: dict[str, Any]
    payload: dict[str, Any]
    warnings: list[Any]
    view_manifest: dict[str, Any]
    saved: Literal[False]


class FamilyExecutionResponse(StrictModel):
    execution_id: str
    project_id: str
    dataset_version_id: str
    analysis_view_id: str | None
    execution_plan_id: str
    analysis_family: str
    specification_schema_version: str
    snapshot_hash: str
    status: str
    requested_at: datetime | None
    started_at: datetime | None
    finished_at: datetime | None
    last_error: dict[str, Any] | None


class FamilyExecutionListResponse(StrictModel):
    items: list[FamilyExecutionResponse]
    next_cursor: str | None = None


class FamilyResultResponse(StrictModel):
    result_id: str
    project_id: str
    execution_id: str
    stage_execution_id: str
    analysis_family: str
    result_type: str
    schema_version: str
    analytical_status: str
    summary: dict[str, Any]
    payload: dict[str, Any]
    diagnostics: dict[str, Any]
    warnings: list[Any]
    created_at: datetime | None


class FamilyResultListResponse(StrictModel):
    items: list[FamilyResultResponse]
    next_cursor: str | None = None


class CreateDraftRequest(StrictModel):
    target_family: Literal["CAUSAL", "PREDICTIVE"]


def _view(row: AnalysisViewOrm) -> AnalysisViewResponse:
    return AnalysisViewResponse(
        analysis_view_id=row.analysis_view_id, project_id=row.project_id,
        source_dataset_version_id=row.source_dataset_version_id, view_key=row.view_key,
        version_number=row.version_number, name=row.name, status=row.status,
        schema_version=row.schema_version, spec=row.spec_json, content_hash=row.content_hash,
        manifest=row.manifest_json, created_by=row.created_by, created_at=row.created_at,
        fixed_at=row.fixed_at,
    )


def _execution(row: FamilyExecutionOrm | Execution) -> FamilyExecutionResponse:
    if isinstance(row, Execution):
        family = row.analysis_spec_json
        return FamilyExecutionResponse(
            execution_id=row.execution_id, project_id=row.project_id,
            dataset_version_id=row.dataset_version_id,
            analysis_view_id=family.get("analysis_view_id"),
            execution_plan_id=family.get("execution_plan_id") or "canonical",
            analysis_family=row.analysis_family.value,
            specification_schema_version="exploratory-analysis-spec/1",
            snapshot_hash=row.snapshot_hash, status=row.status.value,
            requested_at=row.requested_at, started_at=row.started_at,
            finished_at=row.finished_at,
            last_error=(
                {"message": row.last_error_summary} if row.last_error_summary else None
            ),
        )
    return FamilyExecutionResponse(
        execution_id=row.execution_id, project_id=row.project_id,
        dataset_version_id=row.dataset_version_id, analysis_view_id=row.analysis_view_id,
        execution_plan_id=row.execution_plan_id, analysis_family=row.analysis_family,
        specification_schema_version=row.specification_schema_version,
        snapshot_hash=row.snapshot_hash, status=row.status, requested_at=row.requested_at,
        started_at=row.started_at, finished_at=row.finished_at, last_error=row.last_error_json,
    )


def _result(row: FamilyResultOrm | ExploratoryResultProjection) -> FamilyResultResponse:
    return FamilyResultResponse(
        result_id=row.result_id, project_id=row.project_id, execution_id=row.execution_id,
        stage_execution_id=row.stage_execution_id, analysis_family=row.analysis_family,
        result_type=row.result_type, schema_version=row.schema_version,
        analytical_status=row.analytical_status, summary=row.summary_json,
        payload=row.payload_json, diagnostics=row.diagnostics_json,
        warnings=row.warning_json, created_at=row.created_at,
    )


@router.post("/projects/{project_id}/analysis-views", response_model=AnalysisViewResponse, status_code=201)
async def create_analysis_view(
    project_id: str, body: AnalysisViewCreate, svc: ExploratoryWorkspaceServiceDep,
) -> AnalysisViewResponse:
    return _view(svc.create_view(project_id, view_key=body.view_key, name=body.name, spec=body.spec))


@router.get("/projects/{project_id}/analysis-views", response_model=AnalysisViewListResponse)
async def list_analysis_views(
    project_id: str, svc: ExploratoryWorkspaceServiceDep,
) -> AnalysisViewListResponse:
    return AnalysisViewListResponse(items=[_view(row) for row in svc.list_views(project_id)])


@router.get("/projects/{project_id}/analysis-views/{analysis_view_id}", response_model=AnalysisViewResponse)
async def get_analysis_view(
    project_id: str, analysis_view_id: str, svc: ExploratoryWorkspaceServiceDep,
) -> AnalysisViewResponse:
    return _view(svc.get_view(project_id, analysis_view_id))


@router.patch("/projects/{project_id}/analysis-views/{analysis_view_id}", response_model=AnalysisViewResponse)
async def update_analysis_view(
    project_id: str, analysis_view_id: str, body: AnalysisViewUpdate,
    svc: ExploratoryWorkspaceServiceDep,
) -> AnalysisViewResponse:
    return _view(svc.update_view(project_id, analysis_view_id, name=body.name, spec=body.spec))


@router.post("/projects/{project_id}/analysis-views/{analysis_view_id}/validate")
async def validate_analysis_view(
    project_id: str, analysis_view_id: str, svc: ExploratoryWorkspaceServiceDep,
) -> dict[str, Any]:
    return svc.validate_view(project_id, analysis_view_id)


@router.post("/projects/{project_id}/analysis-views/{analysis_view_id}/fix", response_model=AnalysisViewResponse)
async def fix_analysis_view(
    project_id: str, analysis_view_id: str, svc: ExploratoryWorkspaceServiceDep,
) -> AnalysisViewResponse:
    return _view(svc.fix_view(project_id, analysis_view_id))


@router.post("/projects/{project_id}/exploration/preview", response_model=ExplorationPreviewResponse)
async def preview_exploration(
    project_id: str, body: ExplorationRequest, svc: ExploratoryWorkspaceServiceDep,
) -> ExplorationPreviewResponse:
    return ExplorationPreviewResponse.model_validate(svc.preview(
        project_id, dataset_version_id=body.dataset_version_id,
        analysis_view_id=body.analysis_view_id, family_spec=body.family_spec,
    ))


@router.post("/projects/{project_id}/exploration/executions", response_model=FamilyExecutionResponse, status_code=202)
async def submit_exploration(
    project_id: str, body: ExplorationRequest,
    svc: ExploratoryWorkspaceServiceDep,
) -> FamilyExecutionResponse:
    row = svc.submit_execution(
        project_id, dataset_version_id=body.dataset_version_id,
        analysis_view_id=body.analysis_view_id, family_spec=body.family_spec,
    )
    return _execution(row)


@router.get("/projects/{project_id}/exploration/executions", response_model=FamilyExecutionListResponse)
async def list_exploration_executions(
    project_id: str, svc: ExploratoryWorkspaceServiceDep,
) -> FamilyExecutionListResponse:
    return FamilyExecutionListResponse(items=[_execution(row) for row in svc.list_executions(project_id)])


@router.get("/projects/{project_id}/exploration/executions/{execution_id}", response_model=FamilyExecutionResponse)
async def get_exploration_execution(
    project_id: str, execution_id: str, svc: ExploratoryWorkspaceServiceDep,
) -> FamilyExecutionResponse:
    return _execution(svc.get_execution(project_id, execution_id))


@router.get("/projects/{project_id}/exploration/results", response_model=FamilyResultListResponse)
async def list_exploration_results(
    project_id: str, svc: ExploratoryWorkspaceServiceDep,
) -> FamilyResultListResponse:
    return FamilyResultListResponse(items=[_result(row) for row in svc.list_results(project_id)])


@router.get("/projects/{project_id}/exploration/results/{result_id}", response_model=FamilyResultResponse)
async def get_exploration_result(
    project_id: str, result_id: str, svc: ExploratoryWorkspaceServiceDep,
) -> FamilyResultResponse:
    return _result(svc.get_result(project_id, result_id))


@router.post("/projects/{project_id}/exploration/results/{result_id}/create-analysis-draft", status_code=201)
async def create_analysis_draft(
    project_id: str, result_id: str, body: CreateDraftRequest,
    svc: ExploratoryWorkspaceServiceDep,
) -> dict[str, Any]:
    return svc.create_analysis_draft(project_id, result_id, body.target_family)


@router.get("/projects/{project_id}/exploration/capabilities")
async def exploration_capabilities(project_id: str) -> dict[str, Any]:
    return {
        "schema_version": "exploratory-capabilities/1",
        "operations": sorted({"PROFILE", "DISTRIBUTION", "ASSOCIATION", "GROUP_SUMMARY", "TIME_TREND", "CHART"}),
        "chart_marks": ["bar", "line", "point", "box", "histogram", "heatmap"],
        "result_label": "EXPLORATORY",
        "semantic_warning": "Exploratory findings do not establish causal effects.",
    }
