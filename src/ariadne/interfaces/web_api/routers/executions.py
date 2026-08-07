"""Execution router."""

from __future__ import annotations

from fastapi import APIRouter, Header, Request

from ariadne.interfaces.web_api.dependencies import (
    ExecutionServiceDep,
    IdempotencyServiceDep,
    PredictiveWorkflowServiceDep,
    ProductQueryServiceDep,
)
from ariadne.interfaces.web_api.schemas import (
    ExecutionBatchCreate,
    ExecutionBatchResponse,
    ExecutionResponse,
    ExecutionPrefillResponse,
    ExecutionAccepted,
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
        input_result_id=e.input_result_id,
        snapshot_schema_version=e.snapshot_schema_version,
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
        analysis_mode=e.analysis_spec_json.get("analysis_mode"),
        scientific_warnings=e.analysis_spec_json.get("scientific_warnings", []),
        revision_context=e.analysis_spec_json.get("revision_context"),
    )


@router.post("/projects/{project_id}/execution-batches", status_code=201, response_model=ExecutionBatchResponse)
async def create_execution_batch(
    project_id: str,
    body: ExecutionBatchCreate,
    request: Request,
    svc: ExecutionServiceDep,
    idempotency: IdempotencyServiceDep,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> ExecutionBatchResponse:
    requested_by = request.headers.get("X-User-Id", "anonymous")
    def command() -> dict:  # type: ignore[type-arg]
        result = svc.create_execution_batch(CreateExecutionBatchCommand(
            project_id=project_id, dataset_version_id=body.dataset_version_id,
            operation=ExecutionOperation(body.operation),
            variants=[ExecutionVariantSpec(
                algorithm_or_estimator=v.algorithm_or_estimator,
                parameter_json=v.parameters, random_seed=v.random_seed,
                analysis_spec_json=(
                    {**body.analysis_spec, "operation_spec": {
                        **body.analysis_spec["operation_spec"],
                        "estimator": v.algorithm_or_estimator,
                    }} if body.operation == "ESTIMATION" else body.analysis_spec
                ),
                objective_snapshot=body.objective, rationale_snapshot=body.rationale,
            ) for v in body.variants],
            input_graph_version_id=body.input_graph_version_id,
            input_result_id=body.input_result_id,
            code_version=body.code_version, runtime_version_json=body.runtime_versions,
            requested_by=requested_by,
            base_execution_id=body.base_execution_id,
            change_reason=body.change_reason,
        ))
        return ExecutionBatchResponse(
            batch_key=result.batch_key,
            executions=[ExecutionAccepted(
                execution_id=value,
                status="QUEUED",
                scientific_warnings=result.scientific_warnings_by_execution.get(value, []),
            ) for value in result.execution_ids],
        ).model_dump(mode="json")
    response = idempotency.execute(
        project_id=project_id, scope="execution-batch", key=idempotency_key,
        payload=body.model_dump(mode="json"), command=command,
    )
    return ExecutionBatchResponse.model_validate(response)


@router.get("/projects/{project_id}/executions")
async def list_executions(
    project_id: str,
    query: ProductQueryServiceDep,
    predictive: PredictiveWorkflowServiceDep,
) -> dict[str, object]:
    causal = [
        _execution_to_response(execution).model_dump(mode="json")
        for execution in query.list_executions(project_id)
    ]
    return {"items": [*causal, *predictive.list_family_executions(project_id)]}


@router.get("/executions/{execution_id}", response_model=ExecutionResponse)
async def get_execution(execution_id: str, svc: ExecutionServiceDep) -> ExecutionResponse:
    return _execution_to_response(svc.get_execution(execution_id))


@router.get("/executions/{execution_id}/prefill", response_model=ExecutionPrefillResponse)
async def get_execution_prefill(execution_id: str, svc: ExecutionServiceDep) -> ExecutionPrefillResponse:
    return ExecutionPrefillResponse.model_validate(svc.get_prefill(execution_id))


@router.post("/executions/{execution_id}/cancel", status_code=204)
async def cancel_execution(execution_id: str, svc: ExecutionServiceDep) -> None:
    svc.request_cancel(execution_id)


@router.post("/executions/{execution_id}/retry", status_code=204)
async def retry_execution(execution_id: str, svc: ExecutionServiceDep) -> None:
    svc.retry_execution(execution_id)
