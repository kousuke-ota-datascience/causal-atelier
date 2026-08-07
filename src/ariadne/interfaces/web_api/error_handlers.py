"""FastAPI error handlers for domain and infrastructure errors."""

from __future__ import annotations

import uuid

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from ariadne.product.domain.errors import (
    DomainError,
    EntityNotFound,
    GraphAlreadyFixed,
    InvalidAnalysisSpec,
    InvalidStateTransition,
    ProjectBoundaryViolation,
    InvalidGraphSemantics,
    ArtifactHashMismatch,
    ScientificContractViolation,
    GraphOutcomeMismatch,
    GraphOutcomeRequired,
    GraphParentNotFixed,
    InvalidDatasetFile,
    InvalidDatasetMetadata,
    InvalidGraphEditBase,
    ProjectArchived,
    InvalidSchema,
    ResourceImmutable,
)
from ariadne.interfaces.web_api.idempotency import IdempotencyConflict


def _error(request: Request, status: int, code: str, message: str, details: dict | None = None) -> JSONResponse:
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    return JSONResponse(status_code=status, content={"error": {
        "code": code, "message": message, "details": details or {}, "request_id": request_id,
    }})


async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    if isinstance(exc, EntityNotFound):
        return _error(request, 404, "ENTITY_NOT_FOUND", str(exc))
    if isinstance(exc, ProjectBoundaryViolation):
        return _error(request, 422, "PROJECT_BOUNDARY_VIOLATION", str(exc))
    if isinstance(exc, ProjectArchived):
        return _error(request, 409, "PROJECT_ARCHIVED", str(exc))
    if isinstance(exc, IdempotencyConflict):
        return _error(request, 409, "IDEMPOTENCY_CONFLICT", str(exc))
    if isinstance(exc, GraphAlreadyFixed):
        return _error(request, 409, "GRAPH_FIXED_IMMUTABLE", str(exc))
    if isinstance(exc, GraphParentNotFixed):
        return _error(request, 409, "GRAPH_PARENT_NOT_FIXED", str(exc))
    if isinstance(exc, GraphOutcomeRequired):
        return _error(request, 422, "GRAPH_OUTCOME_REQUIRED", str(exc))
    if isinstance(exc, GraphOutcomeMismatch):
        return _error(request, 409, "GRAPH_OUTCOME_MISMATCH", str(exc))
    if isinstance(exc, InvalidGraphEditBase):
        return _error(request, 409, "INVALID_GRAPH_EDIT_BASE", str(exc))
    if isinstance(exc, InvalidDatasetFile):
        return _error(request, 422, "INVALID_DATASET_FILE", str(exc))
    if isinstance(exc, InvalidDatasetMetadata):
        return _error(request, 422, "INVALID_DATASET_METADATA", str(exc))
    if isinstance(exc, InvalidStateTransition):
        return _error(request, 409, "EXECUTION_STATE_CONFLICT", str(exc))
    if isinstance(exc, InvalidGraphSemantics):
        return _error(request, 422, "INVALID_GRAPH_SEMANTICS", str(exc))
    if isinstance(exc, InvalidAnalysisSpec):
        return _error(
            request, 422,
            exc.code if isinstance(exc, ScientificContractViolation) else "INVALID_ANALYSIS_SPEC",
            str(exc),
        )
    if isinstance(exc, InvalidSchema):
        return _error(request, 422, "INVALID_SCHEMA", str(exc))
    if isinstance(exc, ResourceImmutable):
        return _error(request, 409, "RESOURCE_IMMUTABLE", str(exc))
    if isinstance(exc, ArtifactHashMismatch):
        return _error(request, 500, "ARTIFACT_HASH_MISMATCH", str(exc))
    return _error(request, 400, "DOMAIN_ERROR", str(exc))


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return _error(request, 400, "INVALID_REQUEST", "Request validation failed.", {"errors": exc.errors()})
