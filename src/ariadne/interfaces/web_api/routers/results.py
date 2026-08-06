"""Results, comparisons, and lineage router."""

from __future__ import annotations

from fastapi import APIRouter, Header

from ariadne.interfaces.web_api.dependencies import (
    ComparisonServiceDep,
    IdempotencyServiceDep,
    LineageServiceDep,
    ProductQueryServiceDep,
)
from ariadne.interfaces.web_api.schemas import (
    ComparisonQueryRequest,
    ComparisonResponse,
    LineageEdgeResponse,
    LineageNodeResponse,
    LineageResponse,
    ResultListResponse,
    ResultResponse,
)
from ariadne.product.domain.errors import EntityNotFound
from ariadne.product.domain.result import Result

router = APIRouter(tags=["results"])


def _result_to_response(r: Result, artifact_ids: list[str] | None = None) -> ResultResponse:
    return ResultResponse(
        result_id=r.result_id,
        execution_id=r.execution_id,
        result_type=r.result_type.value,
        scientific_status=r.scientific_status.value,
        summary=r.summary_json,
        payload=r.payload_json,
        diagnostics=r.diagnostics_json,
        warnings=r.warning_json,
        artifact_ids=artifact_ids or [],
        created_at=r.created_at,
    )


@router.get("/executions/{execution_id}/results", response_model=ResultListResponse)
async def list_results_by_execution(execution_id: str, query: ProductQueryServiceDep) -> ResultListResponse:
    items = query.list_results(execution_id)
    return ResultListResponse(
        items=[_result_to_response(r, query.result_artifact_ids(r.result_id)) for r in items]
    )


@router.get("/results/{result_id}", response_model=ResultResponse)
async def get_result(result_id: str, query: ProductQueryServiceDep) -> ResultResponse:
    return _result_to_response(query.get_result(result_id), query.result_artifact_ids(result_id))


@router.post("/comparisons/query", response_model=ComparisonResponse)
async def query_comparison(body: ComparisonQueryRequest, svc: ComparisonServiceDep) -> ComparisonResponse:
    view = svc.compare(body.result_ids, body.project_id)
    return ComparisonResponse(
        operation=view.operation,
        common_conditions=view.common_conditions,
        changed_conditions=view.changed_conditions,
        result_differences=view.result_differences,
        warnings=view.warnings,
        lineage_summary=view.lineage_summary,
    )


@router.get("/results/{result_id}/lineage", response_model=LineageResponse)
async def get_lineage(result_id: str, svc: LineageServiceDep) -> LineageResponse:
    view = svc.get_lineage(result_id)
    node_types = {node.entity_id: node.node_type for node in view.nodes}
    return LineageResponse(
        root_result_id=result_id,
        nodes=[
            LineageNodeResponse(
                node_type=n.node_type,
                entity_id=n.entity_id,
                label=n.label,
                attributes=n.attributes,
            )
            for n in view.nodes
        ],
        edges=[LineageEdgeResponse(
            relation_type=_lineage_relation(node_types.get(source), node_types.get(target)),
            from_id=source,
            to_id=target,
        ) for source, target in view.edges],
    )


def _lineage_relation(source_type: str | None, target_type: str | None) -> str:
    return {
        ("Project", "Execution"): "CONTEXT_FOR",
        ("Artifact", "DatasetVersion"): "SOURCE_OF",
        ("DatasetVersion", "Execution"): "INPUT_TO",
        ("Execution", "Result"): "GENERATED",
        ("Result", "GraphVersion"): "SOURCE_OF",
        ("GraphVersion", "Execution"): "INPUT_TO",
        ("Result", "Artifact"): "HAS_ARTIFACT",
        ("Result", "Annotation"): "HAS_ANNOTATION",
        ("GraphVersion", "Annotation"): "HAS_ANNOTATION",
        ("Execution", "Execution"): "REVISED_FROM",
    }.get((source_type, target_type), "RELATED_TO")


@router.post("/results/{result_id}/export")
async def export_result(
    result_id: str,
    query: ProductQueryServiceDep,
    idempotency: IdempotencyServiceDep,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> dict:
    return idempotency.execute(
        project_id=query.result_project_id(result_id),
        scope="result-export",
        key=idempotency_key,
        payload={"result_id": result_id},
        command=lambda: query.export_result(result_id),
    )
