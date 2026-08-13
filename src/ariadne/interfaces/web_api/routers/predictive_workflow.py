"""G4 predictive Execution Plan and asynchronous Execution APIs."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Header, Request
from pydantic import BaseModel, ConfigDict

from ariadne.interfaces.web_api.dependencies import IdempotencyServiceDep, PredictiveWorkflowServiceDep

router = APIRouter(tags=["predictive-workflow"])


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ExecutionPlanCreate(StrictModel):
    analysis_specification_id: str


class PredictiveExecutionSubmit(StrictModel):
    analysis_specification_id: str
    execution_plan_id: str
    seed: int


class PredictiveExecutionRevise(StrictModel):
    analysis_specification_id: str
    seed: int
    change_reason: str


@router.post("/projects/{project_id}/execution-plans", status_code=201)
async def create_execution_plan(
    project_id: str,
    body: ExecutionPlanCreate,
    svc: PredictiveWorkflowServiceDep,
) -> dict[str, Any]:
    return svc.create_plan(project_id, body.analysis_specification_id)


@router.get("/projects/{project_id}/execution-plans/{plan_id}")
async def get_execution_plan(
    project_id: str, plan_id: str, svc: PredictiveWorkflowServiceDep
) -> dict[str, Any]:
    return svc.get_plan(project_id, plan_id)


@router.post("/projects/{project_id}/execution-plans/{plan_id}/validate")
async def validate_execution_plan(
    project_id: str, plan_id: str, svc: PredictiveWorkflowServiceDep
) -> dict[str, Any]:
    return svc.validate_plan(project_id, plan_id)


@router.post("/projects/{project_id}/executions", status_code=202)
async def submit_predictive_execution(
    project_id: str,
    body: PredictiveExecutionSubmit,
    request: Request,
    svc: PredictiveWorkflowServiceDep,
    idempotency: IdempotencyServiceDep,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> dict[str, Any]:
    payload = body.model_dump(mode="json")
    return idempotency.execute(
        project_id=project_id, scope="predictive-execution-submit", key=idempotency_key, payload=payload,
        command=lambda: svc.submit_execution(
            project_id, specification_id=body.analysis_specification_id,
            plan_id=body.execution_plan_id, seed=body.seed,
            requested_by=request.headers.get("X-User-Id", "anonymous"),
        ),
    )


@router.get("/projects/{project_id}/executions/{execution_id}")
async def get_predictive_execution(
    project_id: str, execution_id: str, svc: PredictiveWorkflowServiceDep
) -> dict[str, Any]:
    return svc.get_execution(project_id, execution_id)


@router.get("/projects/{project_id}/executions/{execution_id}/stages")
async def get_predictive_stages(
    project_id: str, execution_id: str, svc: PredictiveWorkflowServiceDep
) -> dict[str, Any]:
    return {"items": svc.get_stages(project_id, execution_id)}


@router.get("/projects/{project_id}/executions/{execution_id}/results")
async def get_predictive_results(
    project_id: str, execution_id: str, svc: PredictiveWorkflowServiceDep
) -> dict[str, Any]:
    return {"items": svc.list_results(project_id, execution_id)}


@router.get("/projects/{project_id}/executions/{execution_id}/artifacts")
async def get_predictive_artifacts(
    project_id: str, execution_id: str, svc: PredictiveWorkflowServiceDep
) -> dict[str, Any]:
    return {"items": svc.list_artifacts(project_id, execution_id)}


@router.get("/projects/{project_id}/executions/{execution_id}/lineage")
async def get_predictive_lineage(
    project_id: str, execution_id: str, svc: PredictiveWorkflowServiceDep
) -> dict[str, Any]:
    return {"items": svc.list_lineage(project_id, execution_id)}


@router.post("/projects/{project_id}/executions/{execution_id}/cancel")
async def cancel_predictive_execution(
    project_id: str, execution_id: str, svc: PredictiveWorkflowServiceDep
) -> dict[str, Any]:
    return svc.cancel(project_id, execution_id)


@router.post("/projects/{project_id}/executions/{execution_id}/retry")
async def retry_predictive_execution(
    project_id: str, execution_id: str, svc: PredictiveWorkflowServiceDep
) -> dict[str, Any]:
    return svc.retry(project_id, execution_id)


@router.post(
    "/projects/{project_id}/executions/{execution_id}/rerun", status_code=202
)
async def rerun_predictive_execution(
    project_id: str,
    execution_id: str,
    request: Request,
    svc: PredictiveWorkflowServiceDep,
) -> dict[str, Any]:
    return svc.rerun(
        project_id,
        execution_id,
        requested_by=request.headers.get("X-User-Id", "anonymous"),
    )


@router.post(
    "/projects/{project_id}/executions/{execution_id}/revise", status_code=202
)
async def revise_predictive_execution(
    project_id: str,
    execution_id: str,
    body: PredictiveExecutionRevise,
    request: Request,
    svc: PredictiveWorkflowServiceDep,
) -> dict[str, Any]:
    return svc.revise(
        project_id,
        execution_id,
        specification_id=body.analysis_specification_id,
        seed=body.seed,
        change_reason=body.change_reason,
        requested_by=request.headers.get("X-User-Id", "anonymous"),
    )


@router.get("/projects/{project_id}/executions/{execution_id}/prefill")
async def get_predictive_prefill(
    project_id: str, execution_id: str, svc: PredictiveWorkflowServiceDep
) -> dict[str, Any]:
    return svc.prefill(project_id, execution_id)
