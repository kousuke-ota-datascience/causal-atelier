"""Results, comparisons, and lineage router."""

from __future__ import annotations

from fastapi import APIRouter

from ariadne.interfaces.web_api.dependencies import (
    ComparisonServiceDep,
    LineageServiceDep,
)
from ariadne.interfaces.web_api.schemas import (
    ComparisonQueryRequest,
    ComparisonResponse,
    LineageNodeResponse,
    LineageResponse,
    ResultListResponse,
    ResultResponse,
)
from ariadne.product.domain.errors import EntityNotFound
from ariadne.product.domain.result import Result

router = APIRouter(tags=["results"])


def _result_to_response(r: Result) -> ResultResponse:
    return ResultResponse(
        result_id=r.result_id,
        execution_id=r.execution_id,
        result_type=r.result_type.value,
        scientific_status=r.scientific_status.value,
        summary_json=r.summary_json,
        payload_json=r.payload_json,
        diagnostics_json=r.diagnostics_json,
        warning_json=r.warning_json,
        created_at=r.created_at,
    )


@router.get("/executions/{execution_id}/results", response_model=ResultListResponse)
def list_results_by_execution(execution_id: str) -> ResultListResponse:
    from ariadne.interfaces.web_api.dependencies import _uow_context
    with _uow_context() as uow:
        items = uow.results.list_by_execution(execution_id)
    return ResultListResponse(items=[_result_to_response(r) for r in items])


@router.get("/results/{result_id}", response_model=ResultResponse)
def get_result(result_id: str) -> ResultResponse:
    from ariadne.interfaces.web_api.dependencies import _uow_context
    with _uow_context() as uow:
        result = uow.results.get(result_id)
        if result is None:
            raise EntityNotFound("Result", result_id)
    return _result_to_response(result)


@router.post("/comparisons/query", response_model=ComparisonResponse)
def query_comparison(body: ComparisonQueryRequest, svc: ComparisonServiceDep) -> ComparisonResponse:
    view = svc.compare(body.result_ids)
    return ComparisonResponse(
        common_conditions=view.common_conditions,
        changed_conditions=view.changed_conditions,
        result_differences=view.result_differences,
        warnings=view.warnings,
        lineage_summary=view.lineage_summary,
    )


@router.get("/results/{result_id}/lineage", response_model=LineageResponse)
def get_lineage(result_id: str, svc: LineageServiceDep) -> LineageResponse:
    view = svc.get_lineage(result_id)
    return LineageResponse(
        nodes=[
            LineageNodeResponse(
                node_type=n.node_type,
                entity_id=n.entity_id,
                label=n.label,
                attributes=n.attributes,
            )
            for n in view.nodes
        ],
        edges=[list(e) for e in view.edges],
    )
