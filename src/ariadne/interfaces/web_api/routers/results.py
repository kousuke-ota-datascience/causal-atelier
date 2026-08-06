"""Results, comparisons, and lineage router."""

from __future__ import annotations

from fastapi import APIRouter, Header

from ariadne.interfaces.web_api.dependencies import (
    ComparisonServiceDep,
    IdempotencyServiceDep,
    LineageServiceDep,
    ProductQueryServiceDep,
    GraphCandidateServiceDep,
)
from ariadne.interfaces.web_api.schemas import (
    ComparisonQueryRequest,
    ComparisonResponse,
    LineageEdgeResponse,
    LineageNodeResponse,
    LineageResponse,
    ResultListResponse,
    ResultResponse,
    GraphCandidateComparisonRequest,
    GraphCandidateComparisonResponse,
    GraphCandidateListResponse,
    GraphCandidateResponse,
)
from ariadne.product.application.graph_candidate_query_service import CandidateRef, GraphCandidateView
from ariadne.product.domain.errors import EntityNotFound
from ariadne.product.domain.result import Result

router = APIRouter(tags=["results"])


def _candidate_to_response(value: GraphCandidateView) -> GraphCandidateResponse:
    return GraphCandidateResponse(
        candidate_kind=value.candidate_kind,
        candidate_id=value.candidate_id,
        source_result_id=value.source_result_id,
        graph_version_id=value.graph_version_id,
        parent_graph_version_id=value.parent_graph_version_id,
        graph_type=value.graph_type,
        graph_origin=value.graph_origin,
        version_status=value.version_status,
        scientific_status=value.scientific_status,
        fixed=value.fixed,
        designated_outcome_node=value.designated_outcome_node,
        summary=value.summary,
        warnings=value.warnings,
        allowed_actions=value.allowed_actions,
        graph=value.graph,
    )


@router.get(
    "/projects/{project_id}/graph-candidates",
    response_model=GraphCandidateListResponse,
)
async def list_graph_candidates(
    project_id: str, svc: GraphCandidateServiceDep
) -> GraphCandidateListResponse:
    return GraphCandidateListResponse(
        items=[_candidate_to_response(item) for item in svc.list_candidates(project_id)]
    )


@router.get(
    "/projects/{project_id}/graph-candidates/{candidate_kind}/{candidate_id}",
    response_model=GraphCandidateResponse,
)
async def get_graph_candidate(
    project_id: str,
    candidate_kind: str,
    candidate_id: str,
    svc: GraphCandidateServiceDep,
) -> GraphCandidateResponse:
    return _candidate_to_response(svc.get_candidate(project_id, candidate_kind, candidate_id))


@router.post(
    "/projects/{project_id}/graph-candidate-comparisons/query",
    response_model=GraphCandidateComparisonResponse,
)
async def compare_graph_candidates(
    project_id: str,
    body: GraphCandidateComparisonRequest,
    svc: GraphCandidateServiceDep,
) -> GraphCandidateComparisonResponse:
    view = svc.compare(project_id, [
        CandidateRef(item.candidate_kind, item.candidate_id)
        for item in body.candidate_refs
    ])
    return GraphCandidateComparisonResponse(
        candidates=[_candidate_to_response(item) for item in view.candidates],
        compatibility=view.compatibility,
        differences=view.differences,
        warnings=view.warnings,
    )


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
