"""FastAPI error handlers for domain and infrastructure errors."""

from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse

from ariadne.product.domain.errors import (
    DomainError,
    EntityNotFound,
    GraphAlreadyFixed,
    InvalidAnalysisSpec,
    InvalidStateTransition,
    ProjectBoundaryViolation,
)


async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    if isinstance(exc, EntityNotFound):
        return JSONResponse(
            status_code=404,
            content={"error_code": "ENTITY_NOT_FOUND", "message": str(exc)},
        )
    if isinstance(exc, ProjectBoundaryViolation):
        return JSONResponse(
            status_code=422,
            content={"error_code": "PROJECT_BOUNDARY_VIOLATION", "message": str(exc)},
        )
    if isinstance(exc, (InvalidAnalysisSpec, InvalidStateTransition, GraphAlreadyFixed)):
        return JSONResponse(
            status_code=422,
            content={"error_code": "INVALID_REQUEST", "message": str(exc)},
        )
    return JSONResponse(
        status_code=400,
        content={"error_code": "DOMAIN_ERROR", "message": str(exc)},
    )
