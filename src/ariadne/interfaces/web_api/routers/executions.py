"""Execution router."""

from __future__ import annotations

from fastapi import APIRouter, Request

from ariadne.interfaces.web_api.dependencies import ExecutionServiceDep
from ariadne.interfaces.web_api.schemas import (
    ExecutionBatchCreate,
    ExecutionBatchResponse,
    ExecutionListResponse,
    ExecutionResponse,
)
from ariadne.product.application.execution_service import (
    CreateExecutionBatchCommand,
    ExecutionVariantSpec,
)
from ariadne.product.domain.enums import ExecutionOperation
from ariadne.product.domain.execution import Execution

router = APIRouter(tags=["executions"])


def _execution_to_response(e: Execution) -> ExecutionResponse:
    return ExecutionResponse(
        execution_id=e.execution_id,
        project_id=e.project_id,
        dataset_version_id=e.dataset_version_id,
        input_graph_version_id=e.input_graph_version_id,
        batch_key=e.batch_key,
        operation=e.operation.value,
        algorithm_or_estimator=e.algorithm_or_estimator,
        status=e.status.value,
        retry_count=e.retry_count,
        requested_by=e.requested_by,
        requested_at=e.requested_at,
        started_at=e.started_at,
        finished_at=e.finished_at,
        last_error_summary=e.last_error_summary,
    )


@router.post("/projects/{project_id}/execution-batches", status_code=201, response_model=ExecutionBatchResponse)
def create_execution_batch(
    project_id: str,
    body: ExecutionBatchCreate,
    request: Request,
    svc: ExecutionServiceDep,
) -> ExecutionBatchResponse:
    requested_by = request.headers.get("X-User-Id", "anonymous")
    result = svc.create_execution_batch(CreateExecutionBatchCommand(
        project_id=project_id,
        dataset_version_id=body.dataset_version_id,
        operation=ExecutionOperation(body.operation),
        variants=[
            ExecutionVariantSpec(
                algorithm_or_estimator=v.algorithm_or_estimator,
                parameter_json=v.parameter_json,
                random_seed=v.random_seed,
                analysis_spec_json=v.analysis_spec_json,
                objective_snapshot=v.objective_snapshot,
                rationale_snapshot=v.rationale_snapshot,
            )
            for v in body.variants
        ],
        input_graph_version_id=body.input_graph_version_id,
        code_version=body.code_version,
        runtime_version_json=body.runtime_version_json,
        requested_by=requested_by,
    ))
    return ExecutionBatchResponse(
        batch_key=result.batch_key,
        execution_ids=result.execution_ids,
    )


@router.get("/projects/{project_id}/executions", response_model=ExecutionListResponse)
def list_executions(project_id: str) -> ExecutionListResponse:
    from ariadne.interfaces.web_api.dependencies import _uow_context
    with _uow_context() as uow:
        items = uow.executions.list_by_project(project_id)
    return ExecutionListResponse(items=[_execution_to_response(e) for e in items])


@router.get("/executions/{execution_id}", response_model=ExecutionResponse)
def get_execution(execution_id: str, svc: ExecutionServiceDep) -> ExecutionResponse:
    return _execution_to_response(svc.get_execution(execution_id))


@router.post("/executions/{execution_id}/cancel", status_code=204)
def cancel_execution(execution_id: str, svc: ExecutionServiceDep) -> None:
    svc.request_cancel(execution_id)


@router.post("/executions/{execution_id}/retry", status_code=204)
def retry_execution(execution_id: str, svc: ExecutionServiceDep) -> None:
    svc.retry_execution(execution_id)
