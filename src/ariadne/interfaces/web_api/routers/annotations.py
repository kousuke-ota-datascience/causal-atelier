"""Annotation router."""

from __future__ import annotations

from fastapi import APIRouter, Request

from ariadne.interfaces.web_api.dependencies import AnnotationServiceDep, ProductQueryServiceDep
from ariadne.interfaces.web_api.schemas import (
    AnnotationCreate,
    AnnotationResponse,
    AnnotationUpdate,
)
from ariadne.product.application.annotation_service import (
    CreateAnnotationCommand,
    UpdateAnnotationCommand,
)
from ariadne.product.domain.annotation import Annotation
from ariadne.product.domain.errors import EntityNotFound

router = APIRouter(tags=["annotations"])


def _ann_to_response(a: Annotation) -> AnnotationResponse:
    return AnnotationResponse(
        annotation_id=a.annotation_id,
        project_id=a.project_id,
        target_result_id=a.target_result_id,
        target_graph_version_id=a.target_graph_version_id,
        statement=a.statement,
        rationale=a.rationale,
        assumptions=a.assumptions_json,
        limitations=a.limitations_json,
        created_by=a.created_by,
        created_at=a.created_at,
        updated_at=a.updated_at,
    )


@router.post("/projects/{project_id}/annotations", status_code=201, response_model=AnnotationResponse)
async def create_annotation(
    project_id: str,
    body: AnnotationCreate,
    request: Request,
    svc: AnnotationServiceDep,
) -> AnnotationResponse:
    created_by = request.headers.get("X-User-Id", "anonymous")
    ann = svc.create_annotation(CreateAnnotationCommand(
        project_id=project_id,
        statement=body.statement,
        created_by=created_by,
        target_result_id=body.target_result_id,
        target_graph_version_id=body.target_graph_version_id,
        rationale=body.rationale,
        assumptions_json=body.assumptions,
        limitations_json=body.limitations,
    ))
    return _ann_to_response(ann)


@router.get("/annotations/{annotation_id}", response_model=AnnotationResponse)
async def get_annotation(annotation_id: str, query: ProductQueryServiceDep) -> AnnotationResponse:
    return _ann_to_response(query.get_annotation(annotation_id))


@router.patch("/annotations/{annotation_id}", response_model=AnnotationResponse)
async def update_annotation(
    annotation_id: str, body: AnnotationUpdate, svc: AnnotationServiceDep
) -> AnnotationResponse:
    ann = svc.update_annotation(UpdateAnnotationCommand(
        annotation_id=annotation_id,
        statement=body.statement,
        rationale=body.rationale,
        assumptions_json=body.assumptions,
        limitations_json=body.limitations,
    ))
    return _ann_to_response(ann)
