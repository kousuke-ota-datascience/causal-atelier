"""FastAPI application factory for the causal-atelier control plane."""

from __future__ import annotations

import logging
import time
import uuid
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from causal_atelier import __version__
from causal_atelier.infrastructure.artifact_store import build_artifact_store
from causal_atelier.infrastructure.data_query import PyArrowQueryEngine
from causal_atelier.infrastructure.persistence import Database
from causal_atelier.infrastructure.settings import WebSettings
from causal_atelier.interfaces.api.dependencies import seed_roles

from .routers import configurations, datasets, projects, runs, visualizations


logger = logging.getLogger("causal_atelier.api")


def create_app(
    settings: WebSettings | None = None,
    *,
    database: Database | None = None,
) -> FastAPI:
    resolved_settings = settings or WebSettings.from_env()
    resolved_settings.ensure_directories()
    resolved_database = database or Database(resolved_settings.database_url)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if resolved_settings.auto_create_schema:
            resolved_database.create_schema()
        with resolved_database.session() as session:
            seed_roles(session)
        yield

    app = FastAPI(
        title="causal-atelier Control Plane API",
        version=__version__,
        description=(
            "Versioned datasets and configurations, asynchronous causal-analysis runs, "
            "artifact lineage, and bounded ETL-data visualization. The service does not "
            "automatically prove causal identification."
        ),
        lifespan=lifespan,
    )
    app.state.settings = resolved_settings
    app.state.database = resolved_database
    app.state.artifact_store = build_artifact_store(resolved_settings)
    app.state.query_engine = PyArrowQueryEngine(
        max_result_rows=resolved_settings.query_max_result_rows,
        max_sample_rows=resolved_settings.query_max_sample_rows,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8080", "http://localhost:3000"],
        allow_credentials=False,
        allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=[
            "Authorization",
            "Content-Type",
            "Idempotency-Key",
            "X-User-Subject",
            "X-User-Name",
            "X-Request-ID",
            "X-Correlation-ID",
        ],
        expose_headers=["X-Request-ID", "X-Correlation-ID", "Idempotency-Replayed"],
    )

    @app.middleware("http")
    async def request_context(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        correlation_id = request.headers.get("X-Correlation-ID") or request_id
        request.state.request_id = request_id
        request.state.correlation_id = correlation_id
        started = time.perf_counter()
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Correlation-ID"] = correlation_id
        logger.info(
            "request_complete",
            extra={
                "request_id": request_id,
                "correlation_id": correlation_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": int((time.perf_counter() - started) * 1000),
            },
        )
        return response

    @app.exception_handler(HTTPException)
    async def http_error(request: Request, exc: HTTPException) -> JSONResponse:
        detail = exc.detail
        message = (
            detail if isinstance(detail, str) else "Request could not be completed"
        )
        details = detail if isinstance(detail, dict) else {}
        return _error_response(
            request,
            exc.status_code,
            _status_code_name(exc.status_code),
            message,
            details,
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_error(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return _error_response(
            request,
            422,
            "REQUEST_VALIDATION_ERROR",
            "Request validation failed",
            {"issues": exc.errors()},
        )

    @app.exception_handler(Exception)
    async def unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(
            "unhandled_request_error",
            extra={"request_id": getattr(request.state, "request_id", None)},
        )
        return _error_response(
            request, 500, "INTERNAL_ERROR", "An internal error occurred", {}
        )

    # APIRouter is used directly so the generated root OpenAPI document remains complete.
    for router in (
        projects.router,
        datasets.router,
        configurations.router,
        runs.router,
        visualizations.router,
    ):
        app.include_router(router, prefix="/api/v1")

    @app.get("/health/live", tags=["health"])
    def live() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/health/ready", tags=["health"])
    def ready() -> dict[str, str]:
        with resolved_database.session() as session:
            session.execute(text("SELECT 1"))
        return {"status": "ready"}

    @app.get("/", include_in_schema=False)
    def index() -> dict[str, str]:
        return {
            "service": "causal-atelier",
            "version": __version__,
            "openapi": "/openapi.json",
            "docs": "/docs",
        }

    return app


def _error_response(
    request: Request,
    status_code: int,
    code: str,
    message: str,
    details: dict,
) -> JSONResponse:
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    response = JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "request_id": request_id,
                "details": details,
            }
        },
    )
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Correlation-ID"] = getattr(
        request.state, "correlation_id", request_id
    )
    return response


def _status_code_name(status_code: int) -> str:
    return {
        400: "BAD_REQUEST",
        401: "UNAUTHENTICATED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        409: "CONFLICT",
        413: "PAYLOAD_TOO_LARGE",
        422: "UNPROCESSABLE_ENTITY",
    }.get(status_code, f"HTTP_{status_code}")


app = create_app()


def main() -> None:
    uvicorn.run(
        "causal_atelier.interfaces.api.app:app", host="0.0.0.0", port=8000, reload=False
    )


if __name__ == "__main__":
    main()


__all__ = ["app", "create_app", "main"]
